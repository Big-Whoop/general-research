Sandbox = k3s pod on wrk (/opt/data iSCSI); CLI /opt/hermes/bin/hermes (not on PATH), config /opt/data/config.yaml, vision=true; no kubectl. MEDIA: files under /opt/data only. GitHub -> skill peters-github.
§
Suite source /workspace/dev/repos/ours/custom-hermes-suite (NEVER ~/hermes-reorg); deploy = Flux, tag-pinned (D29). Rollout kills sessions+workers. Skill hermes-suite-image.
§
config set UNSAFE for nested YAML; edit config.yaml directly (patch/write_file blocked, sed OK).
§
Kanban: ONLY skill = hermes-kanban-workers. Card PRs -> feat/<feature>, one feature PR -> main (user merges; infra repos never by an agent); deploy via tags (D29); no chat watcher inside a wave.
§
Crucial Rules - each of the following is a standing rule; do NOT change or remove any of them without user confirmation.
§
Critical: write EVERYTHING in English (memory entries + all AI-facing text: prompts, skill files, agent instructions). Exception: research results stay in the language they were produced in (2026-10-16).
§
Critical: NEVER change foreign Sourcecode unless it is meant to be changed by the user like .env AND already included in .gitignore OR the user decided to make a contribution.
§
Critical: Docs-before-code GATE (user rule 2026-10-08, every session): BEFORE reading foreign source code for research, state which official doc / issue / KB / skill you already tried; source code is ONLY the fallback when docs give no answer. Coding/programming tasks are the exception (code is primary there). Never use foreign sourcecode as documentation; ask user if no other way.
§
Critical: NEVER make changes to users infrastructure without making a plan and presenting it to the user for confirmation or modification.
§
Critical: prefer fresh research over your trained knowledge.
§
Critical: prefer asking over assuming - better ask one time too many than too few.
§
Critical: no create-then-delete/undo churn — don't build something then tear it down.
§
NixOS-infra (Big-Whoop): self-boot id = PTR after DHCP, no MACs. k3s: cpl .20 (kubectl ONLY here), wrk .21, llmp=ryzen .30 (hermes@, sudo whitelist). ServiceLB cpl. DNS lan=router .5 Unbound 1.21.1. SSH ~/.ssh/id_ed25519_probe, user nixos. TrueNAS .4: no agent SSH.
§
nixos-infra invariant (Peter, 2026-10-17): internal domains ALWAYS resolve to 192.168.10.x, internal traffic NEVER via the gate. Gate (VPS 83.228.246.66) = edge for remote access only (*.homelab.fahsel.ch, D10). Gate->homelab = 7b (cpl WG), not built.
§
Decision pipeline: deep-research -> decision-narrowing (feature-spec-qa = no-corpus sibling) -> decision-topic-execution; kanban NOT for research. Bundled skills never edited: Hermes sandbox specifics -> skill hermes-sandbox-quirks; other local add-ons -> local-skill-addenda.