Quality-Gate (Board-Regeln): Verteilungsregel, PR-Pflicht, Kein-Push-master, Input-Gate apply.
Integration branch: main (single-card change).
Repo AGENTS.md applies. Decision authority: the infra repo's release decision (deploy by annotated release tags; main is NOT live) and its image-pin convention (commit SHA tag). Blanket sign-off by the user (<DATE>): the orchestrator runs the <APP> features through to deployment; the reviewer merges this PR; the orchestrator creates the deploy tag afterwards. No needs_input for in-plan steps.
## Goal (execute, don't design) — pin <APP> <VERSION> (<ONE-LINE WHAT>) in <INFRA-APP-DIR>
Released: <ORG>/<APP> main @ <FULL-SHA>, tag <VERSION> (PR #<N>). CI pushes <REGISTRY>/<APP>:<FULL-SHA> and :<VERSION>. First action: `gh run list --repo <ORG>/<APP> --branch <VERSION> --json status,conclusion` must show the tag run completed+success (image published); if still in progress, wait (poll every 60 s up to 20 min), do not block.
1. <INFRA-APP-DIR>/kustomization.yaml: `images[].newTag: <FULL-SHA> # commit SHA tag, <VERSION> (<SHORT WHAT>)`.
2. deploy/ delta between the previous pin <OLD-SHA> and <FULL-SHA>: <NONE | list the changed files and WHY they matter at runtime, e.g. new RBAC verbs, renamed env vars>. Re-sync the vendored manifests from the app repo at <FULL-SHA> (`gh api repos/<ORG>/<APP>/contents/deploy/<file>?ref=<FULL-SHA>`), keeping the documented local deltas (<imagePullSecrets, namespace labels, image pin, ...>); update the per-file header SHA comment.
3. <INFRA-APP-DIR>/README.md: pin line + one sentence on what changes for operators/users.
4. `kustomize build <INFRA-APP-DIR>` renders without error; paste the image line into the PR.
5. PR to main; reviewer merges. Do NOT create deploy-* tags yourself; the orchestrator does.
## Done-Kriterien
- [ ] newTag = <FULL-SHA>; manifest delta applied; kustomize renders.
- [ ] README updated; PR on main handed to reviewer=reviewer.
Dependencies: keine on this board (consumes <APP> tag <VERSION>, already pushed).
## User-facing text (needs_input block, completion summary, PR description)
Heading "Für Peter zu tun:" or "Entscheidung nötig:"; numbered steps with WHERE (full URL / absolute path + host), WHAT (complete one-line command or exact value), HOW TO VERIFY (command + expected output); no card ids, no chat references; say what happens if the user does nothing. For this card the "Für Peter zu tun" is informational: the orchestrator tags the release after the merge; nothing is live until then.
## Review-Handoff (2-Lane)
Arbeite in deinem isolierten Worktree. Nie in dir: schreiben.
Am Ende: PR auf GitHub öffnen (gh pr create --base main), dann kanban_request_review (reviewer=reviewer) aufrufen. NICHT kanban_complete — das überspringt die Review-Lane.
