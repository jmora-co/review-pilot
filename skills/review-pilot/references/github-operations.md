# GitHub review-thread operations

Use GitHub review-thread nodes rather than flat pull-request comments.

## Read contract

The minimum usable thread record contains:

- thread node ID
- `isResolved`
- `isOutdated`
- path and current/original line data
- every comment in chronological order
- comment node/database ID, author, body, URL, and timestamps

Run:

```sh
python3 scripts/fetch_review_threads.py --pr 123 --repo owner/name
```

Omit `--repo` inside the target repository. The script uses `gh repo view` to infer it.

## Reply mutation

Before replying, refresh the thread and confirm it remains unresolved. Use GraphQL mutation `addPullRequestReviewThreadReply` with the thread node ID and the independently drafted body.

```graphql
mutation Reply($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $threadId, body: $body}) {
    comment { id url }
  }
}
```

## Resolve mutation

Resolve only after the reply succeeds when a reply is required.

```graphql
mutation Resolve($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
```

Do not retry a mutation blindly after an ambiguous network failure. Refresh first to avoid duplicate replies.
