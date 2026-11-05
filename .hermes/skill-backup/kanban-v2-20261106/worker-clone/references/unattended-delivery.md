# Unattended delivery

## Procedure

1. Establish the approved outcome and safety boundary once: implementation, review, merge, release, deployment and live verification. Treat unattended as orchestration responsibility, not permission to bypass checks or introduce downtime.
2. Put programming and executable configuration changes on Kanban, including small fixes discovered during feasibility work. Reuse existing uncommitted work as seeded input; instruct the worker to inspect and finish it rather than recreate it.
3. Seed real dependency-linked implementation cards. Do not substitute a coordinator's completed plan for the requested working platform. Require runtime availability before migrating consumer workflows; an inventory is a prerequisite, not completion.
4. Persist authorization in card bodies and propagate subsequent user overrides to every pending merge, release, verification and documentation card. Update existing gate wording where possible; a comment on a completed coordinator alone never reaches downstream workers reliably. A campaign-specific merge override does not change unrelated repositories' standing policy.
5. Run an in-chat background board watcher and restart it after each handled event. Inspect full blocked-card state rather than acting on truncated notifications. Inspect only new evidence needed for the decision. Suppress repetitive watcher-start/card-created chat updates; report meaningful milestones, user-impacting blockers and completion.
6. Resolve ordinary retries, test harness defects and approved isolated configuration variations without asking permission again. A request to try a mechanism authorizes sensible bounded variants inside the same safety envelope, not endless repetition. Stop for actual broader privileges, persistent host changes or downtime not already authorized.
7. Route hosted-CI resource exhaustion to a focused fix card when unattended delivery includes fixes. Preserve coverage and required status names; reclaim only verified disposable hosted-runner assets. Do not repeatedly rerun the same disk-exhausting job, ask the user to choose routine remediation, fabricate green checks or bypass rules. If a safe remedy genuinely requires new authority, report the exact missing scope.
8. After review and real exact-head required CI, perform authorized merges and releases, read back remote state, and verify the deployed target. Preserve tag-based rollback and concurrent releases; do not equate merge/tag success with rollout success.

## Evidence and capability checks

- Before claiming system access is missing, load the task's access skill/handover and search recent successful sessions. Reuse the documented credential handle/path without printing key contents; do not guess from HOME. After a denial, honor the stop rule and resolve the source discrepancy before another authorized attempt.
- Probe the actual API capability needed using existing authorized tooling before asking for another token. Record endpoint/status without values. Successful runner registration does not imply repository deletion scope or every other administrative privilege.
- Keep credential provision/read-back machine-side and verify names/status only. Reusing an authorized credential creates a rotation dependency; record it without claiming that credential is least-privilege.
- Distinguish host-rootless container proof, rootless Kubernetes test-cluster proof, unprivileged runner-pod proof, and real application pipeline proof. Each is a separate acceptance boundary; never promote one into evidence for the next.
