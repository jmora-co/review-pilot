# GitHub review-thread operations

Use GitHub review-thread nodes rather than flat pull-request comments.

Only the Resolution Lead may mutate GitHub. `auto-local` performs read operations only. `auto-publish` authorizes the mutations below only after the complete local implementation and verification phase succeeds without an outstanding autonomy stop condition.

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

## Publication contract

Immediately before publication, refresh PR head SHA, head branch, thread states, and the local worktree. Stop when drift makes the prepared changes or target unsafe.

Stage only session-attributable files or hunks. Create new coherent commits; never amend, rebase, merge, reset, stash, discard changes, or force-push automatically. Push only to the verified PR head branch.

After push, verify that the new head contains the published commits before claiming that changes are visible or replying that a change was made. If commit or push outcome is ambiguous, refresh local and remote state before any retry.

Reply to each thread independently after the push is verified. Refresh the thread before every mutation, skip it if another participant resolved it, and resolve only after any required reply succeeds. A partially completed response phase must be reported accurately; never duplicate successful replies while recovering.
