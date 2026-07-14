#!/usr/bin/env python3
"""Fetch full GitHub pull-request review threads through the gh CLI."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


QUERY = r"""
query ReviewThreads($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      id
      number
      url
      headRefName
      headRefOid
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          originalLine
          startLine
          originalStartLine
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              databaseId
              author { login }
              body
              url
              createdAt
              updatedAt
            }
          }
        }
      }
    }
  }
}
"""

COMMENTS_QUERY = r"""
query ReviewThreadComments($threadId: ID!, $cursor: String!) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          databaseId
          author { login }
          body
          url
          createdAt
          updatedAt
        }
      }
    }
  }
}
"""


def run_gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], check=False, text=True, capture_output=True
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip() or "gh command failed"
        raise RuntimeError(message)
    return result.stdout


def infer_repo() -> str:
    return run_gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").strip()


def graphql(owner: str, name: str, number: int, cursor: str | None) -> dict[str, Any]:
    args = [
        "api",
        "graphql",
        "-f",
        f"query={QUERY}",
        "-F",
        f"owner={owner}",
        "-F",
        f"name={name}",
        "-F",
        f"number={number}",
    ]
    if cursor:
        args.extend(["-F", f"cursor={cursor}"])
    return json.loads(run_gh(*args))


def fetch_remaining_comments(thread: dict[str, Any]) -> None:
    comments = thread["comments"]
    page_info = comments["pageInfo"]
    while page_info["hasNextPage"]:
        cursor = page_info.get("endCursor")
        if not cursor:
            raise RuntimeError("GitHub reported more comments without an end cursor")
        payload = json.loads(
            run_gh(
                "api",
                "graphql",
                "-f",
                f"query={COMMENTS_QUERY}",
                "-F",
                f"threadId={thread['id']}",
                "-F",
                f"cursor={cursor}",
            )
        )
        connection = payload.get("data", {}).get("node", {}).get("comments")
        if not connection:
            raise RuntimeError(f"could not paginate comments for thread {thread['id']}")
        comments["nodes"].extend(connection.get("nodes") or [])
        page_info = connection["pageInfo"]
    comments.pop("pageInfo", None)


def fetch(owner: str, name: str, number: int) -> dict[str, Any]:
    threads: list[dict[str, Any]] = []
    cursor: str | None = None
    pull_request: dict[str, Any] | None = None

    while True:
        payload = graphql(owner, name, number, cursor)
        pull_request = payload.get("data", {}).get("repository", {}).get("pullRequest")
        if not pull_request:
            raise RuntimeError(f"pull request {owner}/{name}#{number} was not found")

        connection = pull_request["reviewThreads"]
        page_threads = connection.get("nodes") or []
        for thread in page_threads:
            fetch_remaining_comments(thread)
        threads.extend(page_threads)
        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            raise RuntimeError("GitHub reported another page without an end cursor")

    assert pull_request is not None
    return {
        "repository": f"{owner}/{name}",
        "pullRequest": {key: value for key, value in pull_request.items() if key != "reviewThreads"},
        "threads": threads,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", type=int, required=True, help="pull-request number")
    parser.add_argument("--repo", help="owner/name; inferred from the current repository")
    parser.add_argument(
        "--active-only", action="store_true", help="emit unresolved threads only"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo = args.repo or infer_repo()
        owner, name = repo.split("/", 1)
        result = fetch(owner, name, args.pr)
        if args.active_only:
            result["threads"] = [thread for thread in result["threads"] if not thread["isResolved"]]
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except (RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
