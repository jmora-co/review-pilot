<div align="center">

# 🤖 Review Pilot

**PR feedback in. Verified fixes out.**

An agent skill that reads active GitHub review threads, understands their context, fixes the code, verifies the result, and—when authorized—publishes the changes and replies.

</div>

## Install

```bash
npx skills add jmora-co/review-pilot --skill review-pilot
```

Review Pilot uses the GitHub CLI to read and update PR threads:

```bash
gh auth login
```

## Choose your flight mode

| Mode           | What it does                                                               |
| -------------- | -------------------------------------------------------------------------- |
| `guided`       | Recommends a resolution and asks before each meaningful action.            |
| `auto-local`   | Resolves and verifies every eligible thread locally. No commit or push.    |
| `auto-publish` | Resolves, verifies, commits, pushes, replies, and closes eligible threads. |

Automatic modes stop when human authority is genuinely required—conflicting feedback, unsafe Git operations, scope expansion, missing access, or failed verification.

## Use it

From the repository and branch associated with the pull request:

```text
Use $review-pilot in auto-local mode for the PR on my current branch.
```

```text
Use $review-pilot in auto-publish mode for PR #2841.
```

```text
Use $review-pilot in guided mode for https://github.com/acme/store/pull/42.
```

If you omit the mode, Review Pilot asks once and recommends `auto-local`.

## What stays safe

- Pre-existing local changes are preserved and never mixed into session commits.
- Every thread gets its own contextual response.
- Subagents can help with large changes, but only the lead agent may publish.
- Internal reasoning, tools, and stop conditions never leak into PR comments.
- No stash, rebase, reset, force-push, or branch switch happens automatically.

<div align="center">

**You review the destination. Review Pilot flies the route.**

</div>
