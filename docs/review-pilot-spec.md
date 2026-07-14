# Review Pilot functional specification

Review Pilot resolves active GitHub pull-request feedback with guided autonomy. It minimizes setup interaction, detects shared causes across threads, coordinates approved changes, verifies them proportionally, publishes code only with permission, and responds to each thread in its own context.

## Session flow

1. Identify the PR from the prompt or ask once for its branch/URL/number.
2. Validate authentication, PR identity, branch position, and pre-existing changes.
3. Read full review threads and relevant repository context.
4. Build an internal inventory, dispositions, clusters, dependencies, and order.
5. Present only the current independent thread or cluster with concise options and a recommendation.
6. Obtain cluster approval, implement its declared change surface, and verify proportionally.
7. Recalculate the inventory and continue automatically until implementation work is complete.
8. Ask whether Review Pilot should commit/push or the user will publish manually.
9. After changes are visible in the PR, choose automatic or review-first response mode.
10. Draft and publish an independent contextual response for every addressed thread; resolve only eligible threads.

## Approval boundaries

- Cluster approval authorizes only the declared change surface.
- Material expansion requires renewed approval.
- Commit and push are separately authorized actions.
- Response mode explicitly authorizes automatic publication or per-thread preview.
- Branch changes, stash, merge, rebase, and destructive worktree operations always require authorization.

## Clustering

A cluster is an internal analysis and implementation unit. Threads may cluster only through a demonstrated shared cause, coherent shared solution, dependency, or conflict. Every GitHub response remains independent and understandable without knowledge of the cluster.

## Delegation

Use subagents for large, independent workstreams. Parallel investigators may read distinct areas. Parallel implementers require disjoint write surfaces. The lead agent owns synthesis, combined diff review, and integrated verification.

## Completion

A session ends only when every active thread is resolved, responded to, explicitly deferred, or blocked with a concrete reason. It does not emit a redundant final recap.
