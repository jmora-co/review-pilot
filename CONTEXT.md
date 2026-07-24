# Review Pilot

This context defines the language of Review Pilot, the skill that analyzes and resolves active pull-request feedback without losing the intent of each thread.

## Language

**Resolution Session**:
A skill run over the active threads of a single pull request, from gathering context through proposing or applying resolutions.
_Avoid_: Review run, batch

**Active Thread**:
A pull-request review conversation that GitHub still reports as unresolved, including all of its comments and associated code context.
_Avoid_: Comment, pending comment

**Comment Cluster**:
An internal analysis group of Active Threads that share a root cause or require a coordinated strategy, even when anchored to different files or lines. It does not replace each thread's individual context or response.
_Avoid_: Duplicate comments, batch

**Cluster Proposal**:
A consolidated explanation of the root cause, affected Active Threads, considered alternatives, and recommended change for a Comment Cluster.
_Avoid_: Per-comment recommendation, implementation plan

**Cluster Approval**:
Human authorization in `guided` mode to implement a complete Cluster Proposal. One approval covers every Active Thread explicitly included in that Comment Cluster, but does not authorize posting replies or resolving GitHub threads. Automatic Execution Modes do not require Cluster Approval.
_Avoid_: Comment approval, blanket approval

**Workstream**:
An independent portion of investigation, implementation, or verification within a Comment Cluster that can be delegated without breaking a sequential dependency on other changes.
_Avoid_: Subtask, comment assignment

**Resolution Lead**:
The primary agent in a Resolution Session, responsible for forming Comment Clusters, preserving the shared root cause, coordinating Workstreams, and synthesizing a coherent solution.
_Avoid_: Coordinator, parent agent

**Context Evidence**:
Information from the diff, history, code, general discussion, and resolved or outdated threads that helps interpret an Active Thread but does not constitute authorized work by itself.
_Avoid_: Pending feedback, hidden scope

**Incidental Finding**:
A defect or opportunity discovered during a Resolution Session that no Active Thread requests. It is reported separately and remains outside every existing Cluster Approval.
_Avoid_: Bonus fix, related comment

**Change Surface**:
The set of modules, contracts, and checks likely to be affected by a proposed resolution. In `guided` mode Cluster Approval authorizes its declared surface; in an automatic Execution Mode active-thread authority permits coherent changes within it.
_Avoid_: Changed lines, unrestricted scope

**Material Expansion**:
An unanticipated growth of the Change Surface that introduces another module, public contract, migration, or significant behavior. It requires an updated Cluster Proposal and approval in `guided` mode; in an automatic Execution Mode it becomes an Autonomy Stop Condition when not clearly required by active feedback.
_Avoid_: Minor adjustment, implementation detail

**Verification Evidence**:
The results of proportional checks that show whether an implemented resolution satisfies its Active Threads without introducing detectable regressions.
_Avoid_: Full test suite, confidence statement

**External Failure**:
A pre-existing verification failure or one unrelated to the Change Surface. It is documented separately from the Comment Cluster result and does not automatically become authorized work.
_Avoid_: Cluster regression, bonus fix

**Cluster Inventory**:
The complete, prioritized internal view of Comment Clusters detected at the start of a Resolution Session. It is updated after each resolution but is not necessarily shown to the user before work begins.
_Avoid_: Comment list, fixed backlog

**Current Cluster**:
The only Comment Cluster currently being implemented. In `guided` mode it is the approved cluster; automatic Execution Modes select it internally. It may contain parallel Workstreams, but other clusters remain unchanged until it closes.
_Avoid_: Active comments, parallel batch

**Thread Resolution**:
An independent explanation of how a specific Active Thread was addressed, based on its request, conversation, location, and corresponding change. It may share implementation with other resolutions but never relies on a collective response to be understandable.
_Avoid_: Cluster response, shared reply

**Thread Approval**:
Authorization to publish a Thread Resolution. In `guided` mode it is granted either for the exact no-change draft at the Current Item or through the selected Response Mode for eligible change-backed drafts; in `auto-publish` it is granted by the explicitly selected Execution Mode. It never authorizes thread resolution and is never inherited from Cluster Approval.
_Avoid_: Cluster Approval, implicit publication

**Cluster Rationale**:
The demonstrable root-cause, shared-solution, or dependency relationship that justifies treating multiple Active Threads as a Comment Cluster. Proximity of files, authorship, or vocabulary is not sufficient justification by itself.
_Avoid_: Similarity, heuristic match

**Session Change**:
A modification produced during the Resolution Session under the selected Execution Mode and attributable to an Active Thread and, when applicable, its Current Cluster or Workstream.
_Avoid_: Working tree change, PR change

**Pre-existing Change**:
A local modification that existed before the Resolution Session. It must be preserved and remains outside the skill's authority even when it overlaps the Change Surface.
_Avoid_: Session Change, dirty file

**Published Change**:
A Session Change that has been pushed to the pull request's remote branch and can be inspected by its participants. A local-only modification is not a Published Change.
_Avoid_: Implemented change, local fix

**Outdated Thread**:
An Active Thread whose anchor belongs to an earlier version of the diff. Its status does not prove that the feedback's intent has been addressed; it must be checked against the current code.
_Avoid_: Resolved thread, irrelevant comment

**Feedback Conflict**:
An incompatibility between intentions expressed in Active Threads or between a thread and a verifiable repository contract. It requires an explicit human decision before implementing either direction.
_Avoid_: Reviewer priority, majority decision

**Workstream Contract**:
The explicit assignment of an objective, write surface, constraints, and checks for a delegated Workstream. A finding outside that contract is returned to the Resolution Lead without automatically expanding the work.
_Avoid_: Subagent prompt, informal task

**Thread Disposition**:
The initial classification of an Active Thread as a change request, question, already addressed, blocked or ambiguous, or non-actionable item. It determines whether the thread participates in implementation, advances directly to a Thread Resolution, or suspends for clarification.
_Avoid_: Priority, reviewer type

**PR Target**:
The pull request and branch associated with a Resolution Session, identified from the initial prompt or, when missing, through a single startup question.
_Avoid_: Session configuration, repository setup

**Current Item**:
The only independent comment or Comment Cluster that the skill presents to the user at a given time. The rest of the Cluster Inventory remains internal until it is ready to be processed.
_Avoid_: Full inventory, review dashboard

**Resolution Option**:
A viable, concise alternative for addressing the Current Item, described by its essential difference, impact, and risk. Only genuine options are presented; variants are not invented to meet a minimum count.
_Avoid_: Exhaustive design, artificial alternative

**Publication Decision**:
The explicit `guided`-mode choice between authorizing the skill to publish Session Changes to the remote branch or leaving that action to the user. Automatic modes define publication authority at session startup instead.
_Avoid_: Cluster Approval, implicit push

**Response Phase**:
The response work in which an independent Thread Resolution is drafted and presented for each addressed Active Thread after determining whether its changes are local or published. In Guided, a selected no-change option advances through this work immediately for its Current Item instead of waiting for the end of the session.
_Avoid_: Cluster response, implementation phase

**Response Mode**:
The `guided`-mode preference between automatically publishing eligible change-backed Thread Resolutions or reviewing them individually before publication. A selected no-change option uses immediate approval of its exact draft instead. In every Execution Mode, each response retains independent context and content.
_Avoid_: Shared reply, implicit approval

**Session Drift**:
A remote change to pull-request commits, threads, or statuses that occurs during a Resolution Session. It invalidates a decision only when it materially changes its intent, evidence, or Change Surface.
_Avoid_: Any remote update, automatic rebase

**Execution Mode**:
The explicit operating policy selected at the start of each Resolution Session through a structured question or numbered list when absent. Auto Review (`auto-local`) authorizes autonomous analysis, implementation, and verification without publication; Auto Pilot (`auto-publish`) additionally authorizes committing, pushing, responding to, and resolving eligible threads; Guided (`guided`) preserves human approval boundaries. Human-facing names and common aliases are accepted. The mode applies only to the current session and is never inferred from ambiguous intent.
_Avoid_: Remembered preference, implicit autonomy, response mode

**Applicable Project Rule**:
A repository instruction that governs the current Active Thread, file, Change Surface, or verification. Rules are discovered progressively from root policy files and nearer scoped instruction files, loaded only when relevant, indexed for reuse, and resolved in favor of the most specific applicable scope.
_Avoid_: Preloaded documentation corpus, ignored repository guidance

**Autonomy Stop Condition**:
A condition that suspends an automatic Execution Mode because proceeding requires human authority or judgment: conflicting feedback or repository contracts, destructive history or worktree operations, scope outside active threads, high-impact changes not clearly required by those threads, insufficient verification evidence, any External Failure encountered during verification, unavailable credentials or permissions, or material Session Drift. It is internal operating state and is never disclosed in pull-request comments. Ordinary technical choices within the authorized feedback remain the agent's responsibility.
_Avoid_: Cluster approval, routine uncertainty, implementation preference

**Eligible Thread**:
An Active Thread that may advance in a specific phase. Implementation eligibility requires an authorized supported change; response eligibility requires enough published evidence for a truthful independent reply; resolution eligibility requires the thread's intent to be fully satisfied.
_Avoid_: Globally eligible comment, automatically resolved thread

**Publication Gate**:
The all-local checkpoint in `auto-publish` that must pass before any remote mutation begins. The gate is atomic, but the subsequent commit, push, reply, and resolution operations are not transactional and may require idempotent recovery from partial success.
_Avoid_: Transactional publication, guaranteed rollback

**Response Style**:
The required voice of every Thread Resolution: one short paragraph when possible, friendly, neutral, professional, and factual. It states the concrete change or decision directly, mentions verification only when useful, and excludes flattery, praise, thanks, reviewer evaluation, ceremonial openings, unnecessary closings, and internal process details.
_Avoid_: Great catch, good point, thanks for noticing, let me know what you think

**Guided Thread Resolution**:
The response draft produced after a Guided Resolution Option has been verified. For an implemented option, it describes the concrete change and relevant verification and may be shown while changes are local without claiming publication. For a no-change option, it states the verified answer or current behavior and is presented immediately for exact-draft approval. Posting and resolving always require separate authority.
_Avoid_: Implementation summary, automatically published reply

**Auth Environment Mismatch**:
A condition where a sandboxed process cannot access the GitHub CLI authentication, keychain state, environment, socket, or network available to the user's host session. It requires a narrow host-environment probe through the runtime's native escalation mechanism before authentication is declared unavailable, and it never expands mutation authority.
_Avoid_: Invalid token without host verification, authentication bypass
