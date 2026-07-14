---
name: review-pilot
description: Proactively analyze and resolve active GitHub pull-request review threads with low-friction human approval, root-cause clustering, optional subagent workstreams, proportional verification, Git publication, and contextual thread replies. Use when the user asks to review, address, fix, or resolve PR comments or active review threads.
---

# Review Pilot

Resolve active PR feedback end to end while preserving human control over code changes and external actions.

## Operating rules

- Ask only for the PR URL, number, or branch when none is supplied and it cannot be inferred.
- Keep the full inventory internal. Present only the current thread or cluster.
- Read broadly for context; change code only on behalf of active, unresolved threads.
- Never overwrite pre-existing local changes.
- Never commit, push, reply, resolve, switch branches, stash, merge, or rebase without the applicable explicit authorization.
- Continue automatically after each decision. Do not ask ceremonial questions such as whether to continue.
- Keep options concise and easy to scan. Present only genuine alternatives and mark one recommendation.

Read [references/github-operations.md](references/github-operations.md) before querying or mutating GitHub review threads.

## 1. Establish the PR target

1. Use a supplied PR URL/number/branch. Otherwise infer the PR from the current branch.
2. If inference fails or is ambiguous, ask one short question for the PR or branch.
3. Check GitHub authentication, repository identity, PR head branch, current branch, HEAD, and working-tree status.
4. Permit read-only analysis from another branch, but require the PR head branch before editing.
5. Inventory pre-existing changes. If they overlap the expected change surface, pause before editing.
6. Do not update or switch the local branch automatically.

## 2. Collect full-fidelity context

Use `scripts/fetch_review_threads.py` when `gh` is available. Accept an alternative GitHub connector only when it exposes the complete thread conversation plus `isResolved`, `isOutdated`, file, line, and thread/node IDs.

Collect:

- PR metadata and diff
- every unresolved review thread, including outdated threads
- resolved threads and general PR discussion as context evidence when useful
- repository instructions and relevant code/history

Never treat a flat list of comments as equivalent to review threads. Never treat `outdated` as `resolved`.

## 3. Build the internal inventory

Classify each active thread as:

- change request
- question
- already addressed
- blocked or ambiguous
- non-actionable

Group change requests only when they share a demonstrated root cause, a coherent shared change, a dependency, or a contradiction that requires joint design. File proximity, reviewer identity, or similar wording is not enough.

Keep a thread independent when clustering is uncertain. Detect conflicting reviewer intent and ask for a human decision before implementation.

Order the inventory by dependencies, risk, and ability to unlock other work. Show at most one short count line, then proceed directly to the current item.

## 4. Propose the current item

For an independent thread, show its intent, evidence, concise options, and recommendation.

For a cluster, show:

- included threads and cluster rationale
- root cause
- concise viable options and recommendation
- expected files, modules, contracts, and auxiliary changes
- proportional verification
- proposed independent workstreams, if useful

Do not fabricate multiple options when only one is reasonable. Include “no code change” when evidence or a reply can legitimately satisfy the thread.

Request one cluster approval before editing any part of a cluster. Approval covers only the declared change surface. Pause for renewed approval if implementation expands materially into another module, public contract, migration, or behavior.

## 5. Implement with controlled parallelism

Use subagents when the work is large and can be divided into independent workstreams:

- Run investigators in parallel for distinct read-only areas.
- Give every delegated workstream an explicit objective, write surface, constraints, and verification.
- Run implementers in parallel only when write surfaces are disjoint.
- Serialize work that may touch the same file or contract.
- Instruct subagents not to commit, push, mutate GitHub, or expand scope.
- Require them to report modified files, decisions, checks, and remaining risks.

The lead agent owns root-cause coherence, inspects the combined diff, reconciles conflicts, and runs integrated verification. Treat out-of-scope findings as incidental findings: report them separately without fixing them under the current approval.

Process one approved cluster at a time. Recalculate the internal inventory after each cluster because one fix may absorb or invalidate others.

## 6. Verify proportionally

Do not run broad tests, typechecks, lint, or unused-code tools during initial analysis.

After implementation, run the checks declared in the proposal, starting with the narrowest useful signal. Broaden only when the change surface or repository instructions justify it. Separate pre-existing or unrelated failures from regressions caused by the session; do not repair external failures without authorization.

Do not mark a cluster ready unless its planned checks pass or the user explicitly accepts a documented limitation.

## 7. Detect drift

Refresh remote PR state before each implementation and before responding:

- new commits
- new or resolved threads
- changed anchors or status

Continue silently when drift does not affect the current decision. Pause only when it changes intent, evidence, cluster membership, or change surface. Never pull, merge, or rebase automatically.

## 8. Publish code

After all approved implementations and verification:

1. Show session changes separately from pre-existing changes.
2. Ask whether Review Pilot should prepare the commit and push, or the user will publish manually.
3. Treat commit and push as separate explicit permissions.
4. If the user publishes manually, wait for confirmation that the changes are visible on the PR.

Never claim a local-only change is available to reviewers.

## 9. Respond to threads

Ask once for the response mode:

- **Automatic (recommended):** draft, publish, and resolve each eligible thread without previewing every draft.
- **Review first:** present each draft for adjustment before publication.

Write every response independently in the thread’s predominant language. Address its exact request, state what changed, and mention verification only when useful. Do not mention clusters, subagents, approvals, or internal tooling. Avoid generic “done” replies when context is needed.

Resolve only threads fully addressed by published changes or conclusive evidence. Keep partial, ambiguous, or limited resolutions open. Refresh thread status immediately before every mutation and skip threads another participant already resolved.

Finish when every active thread is resolved, responded to, explicitly deferred, or blocked with a concrete reason. Do not add a redundant closing summary.
