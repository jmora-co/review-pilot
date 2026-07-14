# Review Pilot functional specification

Review Pilot resolves active GitHub pull-request feedback with an explicit per-session authority policy. It supports guided decisions, autonomous local resolution, and autonomous end-to-end publication while keeping every GitHub response independent and evidence-based.

## Execution modes

- `guided`: analyze one current item at a time and preserve separate approvals for implementation, publication, replies, and resolution.
- `auto-local`: autonomously analyze, implement, and verify all eligible active threads; leave every change local.
- `auto-publish`: perform the complete local phase, cross the publication gate, then commit, push, reply to, and resolve eligible threads with idempotent recovery.

The mode is explicitly selected at startup and applies only to the current session. When absent, Review Pilot asks once and recommends `auto-local`. Publication authority is never inferred or remembered. Authority may be reduced at any time; expanding from local to publication requires explicit authorization.

## Session flow

1. Select the execution mode and identify the PR.
2. Validate authentication, PR identity, branch position, and pre-existing changes.
3. Read full review threads and evidence from the repo, PR, official docs, and available trusted tools.
4. Build an internal inventory, dispositions, clusters, dependencies, and order.
5. In automatic modes, choose the strongest supported resolution and work through all eligible threads without approval gates.
6. Delegate only large independent workstreams under explicit contracts; the lead owns synthesis and publication.
7. Verify proportionally and correct failures caused by session changes.
8. Refresh remote state and incorporate eligible new threads or material drift.
9. In `auto-local`, stop with attributable local changes and verification evidence.
10. In `auto-publish`, cross the publication gate only after the complete local phase succeeds without an outstanding stop condition.
11. Draft an independent contextual response for every addressed thread and resolve only eligible threads.

## Decision evidence

Technical decisions prefer repository contracts; current code, tests, history, and diff; complete PR conversations; official dependency documentation; trusted MCPs/connectors; and finally general engineering conventions. Reasoning and operational tooling remain internal. Conflicting authoritative evidence or insufficient proof for a material decision suspends automatic execution.

## Autonomy boundaries

Automatic modes stop for reviewer or contract conflicts, destructive operations, unsafe branch state, work outside active-thread authority, unclear high-impact changes, insufficient verification, any external or pre-existing verification failure, unavailable permissions, material remote drift, unsafe attribution of local changes, or lack of evidence-backed progress.

A stop condition is internal and never appears in PR comments. The user receives the relevant evidence and concrete choices, then the session resumes from the suspended point after the condition is resolved.

## Local-change safety

Review Pilot snapshots the initial worktree and distinguishes session changes from pre-existing changes. It may continue when attribution is certain, including exact hunk separation, but never stages unrelated work. It never automatically switches branches, stashes, rebases, merges, resets, amends, discards changes, or force-pushes.

## Clustering and delegation

Clusters are internal analysis and implementation units justified by a shared cause, coherent solution, dependency, or conflict. They never replace thread-specific replies. Automatic modes do not require cluster approval.

Subagents may investigate distinct areas or edit disjoint surfaces under Workstream Contracts. They cannot commit, push, change branches, mutate GitHub, or expand scope. The Resolution Lead reviews the combined diff and owns integrated verification and all remote actions.

## Verification and convergence

Checks are proportional to repository guidance and change risk. Session-caused failures are diagnosed and repaired autonomously. An unchanged failed strategy is not repeated without new evidence; stalled work changes approach and eventually suspends when no supported route remains. Any external or pre-existing failure suspends automatic execution and is not repaired under incidental authority.

## Publication gate

`auto-publish` completes implementation and verification for all implementation-eligible threads before any remote mutation. With no outstanding stop condition, it crosses an atomic gate: stage only attributable session changes, create coherent new commits, push normally to the PR head, then reply to and resolve eligible threads. When no Session Changes are needed, it verifies the current PR head and proceeds without an empty commit.

The gate prevents intentionally starting a partial publication; Git and GitHub mutations themselves are not transactional. Partial publication requires idempotent recovery and exact reporting. A pre-gate stop requires a new explicit decision. Ambiguous mutation failures are refreshed before retry to prevent duplicate commits or replies.

Eligibility is phase-specific: implementation eligibility requires an authorized supported change; response eligibility requires enough published evidence for a truthful independent reply; resolution eligibility requires the thread's intent to be fully satisfied.

## Thread outcomes

Change requests receive published changes; questions receive evidence-backed answers; already-addressed or non-actionable threads receive concise explanations. Partial or ambiguous threads stay open. Internal stop conditions are never disclosed or replied to. Every response stands alone, uses the thread's language, and omits clusters, tools, agents, and internal reasoning.

## Traceability and completion

The session internally tracks dispositions, evidence, files, checks, commits, replies, and resolutions without writing an audit artifact into the reviewed repo or PR. User-facing completion is compact and mode-specific. A session is complete only when each active thread is resolved, responded to, or explicitly deferred. An outstanding stop condition suspends the session; a remote phase interrupted after a successful mutation is partially published.
