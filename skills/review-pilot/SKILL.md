---
name: review-pilot
description: Analyze and resolve active GitHub pull-request review threads in guided, autonomous local, or autonomous publication mode, with evidence-backed decisions, proportional verification, optional subagent workstreams, and independent contextual replies. Use when the user asks to review, address, fix, or resolve PR comments or active review threads.
---

# Review Pilot

Resolve active PR feedback end to end. The user chooses how much authority to grant at the start; automatic modes make ordinary technical decisions without human intervention and pause only at explicit safety boundaries.

## Operating rules

- Ask only for information that cannot be inferred safely.
- Keep the full inventory internal. Present only the current item in `guided` mode.
- Read broadly for context; change code only on behalf of active, unresolved threads.
- Preserve pre-existing local changes and attribute every session change.
- Never expose clusters, subagents, tools, internal evidence logs, or autonomy stop conditions in PR replies.
- Continue automatically after each decision. Do not ask ceremonial questions.
- Do not weaken types, checks, or coverage merely to make verification pass.

Read [references/github-operations.md](references/github-operations.md) before querying or mutating GitHub review threads.

## 1. Select the execution mode

Use an execution mode explicitly named in the prompt. Otherwise ask once before expensive analysis or mutation:

- **`guided`**: present decisions and preserve separate human approval for code changes, commit, push, replies, and thread resolution.
- **`auto-local` (recommended)**: autonomously analyze, implement, and verify every eligible active thread. Do not commit, push, reply, or resolve threads.
- **`auto-publish`**: do everything in `auto-local`, cross the all-local publication gate, then commit and push session changes and independently reply to and resolve eligible threads.

An automatic mode is opt-in for the current session only. Never infer `auto-publish` from ambiguous language or remember it across sessions. The user may reduce authority at any time. Moving from `auto-local` to `auto-publish` requires explicit authorization.

## 2. Establish the PR target

1. Use a supplied PR URL, number, or branch. Otherwise infer the PR from the current branch.
2. If inference fails or is ambiguous, ask one short question for the PR or branch.
3. Check GitHub authentication, repository identity, PR head branch, current branch, HEAD, and working-tree status.
4. Permit read-only analysis from another branch, but require the PR head branch before editing. In an automatic mode, a mismatch is an autonomy stop condition; ask the user to switch or explicitly authorize the exact safe action.
5. Record pre-existing changes before editing. Never include them in a session commit.
6. Continue when pre-existing and session changes can be separated safely, including by exact hunks. Pause when attribution is uncertain.
7. Never switch branches, stash, merge, rebase, reset, amend, discard changes, or force-push automatically.

## 3. Collect full-fidelity context

Use `scripts/fetch_review_threads.py` when `gh` is available. Accept an alternative GitHub connector only when it exposes the complete conversation plus `isResolved`, `isOutdated`, file, line, and thread/node IDs.

Collect PR metadata and diff; every unresolved thread, including outdated threads; useful resolved threads and general discussion; repository instructions; relevant code, tests, and history.

Never treat a flat comment list as equivalent to review threads. Never treat `outdated` as `resolved`.

Ground technical decisions in this order:

1. repository instructions and verifiable contracts
2. current code, tests, history, and PR diff
3. complete thread and PR conversation
4. official dependency documentation
5. trustworthy MCPs, connectors, and technical sources
6. general engineering conventions

Keep evidence and alternatives internal. If authoritative sources conflict or evidence is insufficient for a material decision, pause under an autonomy stop condition.

## 4. Build the internal inventory

Classify every active thread as a change request, question, already addressed, blocked or ambiguous, or non-actionable.

Group change requests only when they share a demonstrated root cause, coherent shared change, dependency, or contradiction. File proximity, reviewer identity, or similar wording is not enough. Every GitHub reply must remain independently understandable.

Order the inventory by dependencies, risk, and ability to unlock other work. Recalculate it after every resolution and after relevant remote drift.

Determine eligibility per phase:

- **implementation-eligible**: an active thread authorizes a supported code or documentation change that is not blocked or deferred
- **response-eligible**: the current published PR state provides enough evidence for an independent, truthful reply
- **resolution-eligible**: the thread's intent is fully satisfied by published changes or conclusive evidence

A thread may be response-eligible without requiring implementation. Local-only changes never make a thread response-eligible for a claim that the PR was updated.

In automatic modes, choose and execute the best-supported resolution without presenting options. In `guided`, present the current independent thread or cluster with concise genuine options, evidence, expected change surface, proportional verification, and a recommendation; obtain approval before editing.

## 5. Autonomy stop conditions

In `auto-local` and `auto-publish`, pause and ask for one focused human decision when any of these occurs:

- conflicting reviewer intent or conflict with a verifiable repository contract
- destructive history/worktree action or an unsafe branch operation would be required
- work outside the authority created by active threads would be required
- a migration, secret, permission, infrastructure change, or public-contract change is not clearly required by the feedback
- verification evidence is insufficient
- any external or pre-existing verification failure is observed
- authentication or permissions are unavailable
- session drift materially changes intent, evidence, cluster membership, branch safety, or change surface
- pre-existing and session changes cannot be attributed safely
- repeated attempts no longer produce evidence-backed progress

This is internal operating state. Do not post it to the PR. Show the user the relevant evidence and concrete choices. They may authorize the exact action, choose an alternative, change scope or mode, defer the affected thread, or repair access. Resume automatically after the condition is resolved.

Ordinary technical choices, coherent internal auxiliary changes, and selection among supported implementations are not stop conditions.

## 6. Implement and delegate

In automatic modes, process all eligible threads without cluster approvals. In `guided`, approval covers only the declared change surface and material expansion requires renewed approval.

Use subagents automatically for large independent workstreams when available:

- Give each one a Workstream Contract containing its objective, allowed write surface, constraints, and checks.
- Parallelize read-only investigation across distinct areas.
- Parallelize implementation only across disjoint write surfaces.
- Require findings outside the contract to return to the Resolution Lead without expanding scope.
- Forbid subagents from committing, pushing, replying, resolving threads, changing branches, or mutating GitHub.

The Resolution Lead owns decisions, root-cause coherence, combined-diff review, integrated verification, and all publication.

Treat incidental findings as out of scope. Do not fix them merely because they were discovered.

## 7. Verify and converge

Choose proportional checks from repository instructions and risk. Start with the narrowest useful test, lint, typecheck, or build signal and broaden only when justified.

When a session change causes a failure, diagnose and correct it automatically. Require a new diagnosis before each new edit, do not repeat a failed strategy without new evidence, and after two consecutive attempts without measurable progress, change source, tool, or approach. If no reasonable supported alternative remains, pause.

Any pre-existing or external failure is an autonomy stop condition in automatic modes. Do not repair it outside the active-thread scope. Mention verification in PR replies only when it helps explain the resolution.

## 8. Detect drift

Refresh remote PR commits and thread state before implementation and before publication. Incorporate new active threads on the same PR automatically when they remain within the session's authority. Recalculate affected clusters, dependencies, and checks when the diff changes.

Ignore irrelevant drift. Pause only when drift meets an autonomy stop condition. Never pull, merge, or rebase automatically. Before publication, require a stable inventory in which every eligible active thread is covered.

## 9. Pass the publication gate

`auto-local` stops after local implementation and verification. Report session changes, checks, and the threads they would address.

`auto-publish` uses a two-phase publication gate:

1. Implement and verify all eligible threads locally.
2. Only when no autonomy stop condition remains, begin remote mutation: create coherent new commit(s), push normally to the PR head branch, then reply to and resolve eligible threads.

The gate is atomic; the remote mutations are not transactional. Do not begin partial publication by default. If a stop condition appears before the gate, leave all session changes local until the user resolves it, explicitly defers the blocked thread, or authorizes publication of the completed subset. After remote mutation begins, recover idempotently from partial success and report the exact state.

Stage only attributable session files or hunks. Never amend existing commits, include pre-existing changes, or force-push. Refresh after ambiguous network failures before retrying any mutation.

When no Session Changes exist because every thread requires only an evidence-backed reply, verify the current PR head and stable inventory, skip empty commit/push work, and proceed directly to eligible replies and resolutions.

In `guided` mode after approved implementation and verification:

1. Show Session Changes separately from Pre-existing Changes.
2. Ask whether Review Pilot or the user will publish.
3. If Review Pilot publishes, obtain separate authorization for commit and push, stage only attributable changes, and verify the pushed head.
4. If the user publishes, wait until they confirm the changes are visible on the PR.
5. Ask once whether eligible Thread Resolutions should be published automatically or reviewed one at a time.

## 10. Respond to threads

In `guided`, obtain the selected response mode before mutations. In `auto-publish`, independent replies and eligible thread resolution are authorized by the initial execution mode.

For every active thread:

- **change request**: state the published change that addresses its exact request
- **question**: answer from verified evidence
- **already addressed**: point to the current behavior or published change
- **non-actionable or incorrect**: respond respectfully with concise evidence
- **partial or ambiguous**: explain only the relevant limitation and leave it open
- **blocked internally**: publish nothing about the stop condition and leave it open

Write each reply in the thread's predominant language. Do not mention clusters, agents, approvals, internal sources, or tools. Resolve only after a required reply succeeds and only when published changes or conclusive evidence fully address the thread. Refresh immediately before mutation and skip a thread another participant already resolved.

## Completion and traceability

Maintain an internal session record of thread dispositions, clusters, evidence, files, checks, commits, replies, and resolutions. Do not write this record into the reviewed repository or PR discussion.

- `auto-local`: report local changes, checks, and threads covered.
- `auto-publish`: report commits/push and counts of replied, resolved, and intentionally open threads.
- suspended session: report only the stop condition, relevant evidence, and concrete choices.

A session is **completed** only when every active thread is resolved, responded to, or explicitly deferred. An unresolved autonomy stop condition makes the session **suspended**, not completed. If remote publication has begun but cannot finish, report it as **partially published** with exact successful and pending mutations. Avoid a redundant narrative recap.
