# Research: Seamless remote apps on Linux (server→client window integration + start-menu entry)

Date: 2026-10-25 · Mode: standalone deep-research (no decision topic) · Language: lane files EN, REPORT.md DE

## Question

Client = CachyOS KDE, server = Ubuntu or Kubuntu. Can an application be started ON THE SERVER yet
appear as a normal window on the CLIENT desktop (seamless — no full-desktop session), and have a
normal icon in the client's start menu (KDE application launcher)?

## Premise

Subjects named by the user (verified 2026-10-25, in-session lookup): CachyOS = real Arch-based rolling
distro; KDE Plasma 6 defaults to Wayland (XWayland available); Ubuntu/Kubuntu = real (LTS 24.04 baseline
assumed). User named no specific tool, so candidate tools are ours to propose — premise risk low.
Seed search anchor: candidates x2go published apps, xrdp RemoteApp, waypipe, xpra, ssh -X all surfaced.

## Dichotomy (the axis that produces confusion)

1. X11-era vs Wayland-era forwarding, on BOTH ends (client Plasma6-Wayland ≠ X11 client; headless server
   has no native display server).
2. "Seamless single app" vs "full remote desktop in one window" — only the former satisfies the question.
3. Documented capability vs actually maintained/working on 2026 versions (xrdp RemoteApp, xpra, x2go all
   need a liveness check).

## Environment context block (repeated verbatim in every lane brief)

- Client: CachyOS (Arch-based, rolling), KDE Plasma 6, default session Wayland (XWayland available),
  likely PipeWire audio.
- Server: Ubuntu or Kubuntu, assume 24.04 LTS unless a lane says otherwise; possibly headless.
- Use case: GUI app started on server shows as normal window(s) on client desktop (seamless, no full
  desktop session); ALSO needs a normal KDE start-menu icon on the client.
- LAN primary; note WAN/latency where relevant. SSH access assumed (keys).

## Step 0 — source universe checklist

(status: pending → covered / skipped (reason) / searched, no results)

- [ ] Official docs: OpenSSH/Arch Wiki (X11 forwarding), waypipe GitHub, xpra.org wiki, x2go.org wiki,
      xrdp GitHub docs (RemoteApp), FreeRDP docs, Remmina docs, PipeWire/PulseAudio docs.
- [ ] Semi-official: AUR package pages (xpra, waypipe, x2go client), Ubuntu packages.
- [ ] Community: Reddit (r/linux, r/linuxquestions, r/kde), ServerFault/Unix.SE, Level1Techs forum.
- [ ] Code: GitHub issues of xpra, x2go, xrdp, FreeRDP, waypipe (limitations/workarounds); liveness
      probes (last release/commit via GitHub API).
- [ ] Practice: blog posts (TauCeti "ssh -X vs xpra vs waypipe" is a known anchor), homelab writeups.
- [ ] Upstream: MS-RDPERP/RDPGFX (what RemoteApp requires), NX protocol (x2go/xpra base).

## Coverage table (sub-questions; rows drive round decisions)

| # | sub-question | lanes | best tier | ≥2 indep. sources | workaround space | lane verdicts | status |
|---|---|---|---|---|---|---|---|
| SQ1 | SSH X11 forwarding (ssh -X/-Y) under Plasma6-Wayland client + headless Ubuntu server: clipboard, audio, 3D, latency, pitfalls | L1 | — | — | — | — | OPEN |
| SQ2 | waypipe (Wayland-native forwarding): prereqs, limitations (GPU), client/server support, maintenance | L1 | — | — | — | — | OPEN |
| SQ3 | xpra seamless app streaming: mechanism, X11+Wayland support, clipboard/audio/print, GPU, maintenance 2026 | L2 | — | — | — | — | OPEN |
| SQ4 | X2Go published-applications mode: server setup Ubuntu/Kubuntu, published app UX on client, Wayland status, audio/clipboard/print, maintenance | L3 | — | — | — | — | OPEN |
| SQ5 | RDP RemoteApp via xrdp + FreeRDP/Remmina client: does it work Linux→Linux, config, seamlessness quality, maintenance | L4 | — | — | — | — | OPEN |
| SQ6 | Start-menu icon on KDE client for each viable path (.desktop Exec wrapping the transport, key auth, no terminal popup) — cross-cutting, required item in EVERY lane brief | all | — | — | — | — | OPEN |
| SQ7 | "WSLg-equivalent for Linux" in 2026: is there a first-class/native answer beyond the DIY paths? | L4 | — | — | — | — | OPEN |

## Round 1 plan (4 lanes; Peter's parallelism cap 4)

- L1 ssh-x11-waypipe → ssh-x11-waypipe/lane1.md (SQ1, SQ2, SQ6@)
- L2 xpra → xpra/lane2.md (SQ3, SQ6@)
- L3 x2go → x2go/lane3.md (SQ4, SQ6@)
- L4 rdp-remoteapp → rdp-remoteapp/lane4.md (SQ5, SQ7, SQ6@)
(@ = must answer the start-menu item for its own path)

## Round assessment tables

### Round 1 assessment (2026-10-25)

| sub-question | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts | status |
|---|---|---|---|---|---|
| SQ1 ssh -X under Plasma6-Wayland | Verified (prereqs, -X/-Y, audio recipe, VirtualGL); integration-under-XWayland claim Plausible w/ 3 community sources (unix.SE 776767, askubuntu 1466109, TauCeti) | yes (≥2 community for integration; official for prereqs) | yes (VirtualGL, PulseAudio tunnel) | answered | CLOSED |
| SQ2 waypipe | Verified (man/README official; maint probe v0.11.3 2026-10-20) | yes (official + TauCeti + LinuxLinks + gist) | yes (--no-gpu, --xwls, wl-clipboard, single-instance) | answered | CLOSED |
| SQ3 xpra | Verified (official docs, GitHub probes; very alive v6.5.5 2026-10-12) | yes (official docs ×multiple pages + community) | yes (backend Wayland WIP, --ssh=ssh, VirtualGL, apt repo vs dead noble 3.1.5) | answered | CLOSED |
| SQ4 X2Go published apps | Verified (official wiki + man pages; Wayland crash #1414 + xcb workaround dual-sourced) | yes | yes (QT_QPA_PLATFORM=xcb, sleep=0, pyhoca-cli) | answered | CLOSED (audio-on-PipeWire flagged Speculative in report) |
| SQ5 RDP RemoteApp Linux→Linux | Verified negative (xrdp RAIL 'incomplete'/stalled maint statements; Remmina no RAIL #2578; wlfreerdp no RAIL #6573; FreeRDP maint 'currently no') | yes (xrdp wiki + issues + FreeRDP discussions + Remmina tracker) | yes (NeRDP/WinFlexRM defunct, black-box report) | partial (lane verdict) but blockers each Verified | CLOSED as Verified-negative |
| SQ6 .desktop start-menu recipes per path | Plausible — every lane: mechanism Verified (XDG/KDE spec) but **assembled** Exec recipes; no published third-party working example found by any lane | no (0 documented working examples found) | partially (each lane searched own path only) | all lanes self-flagged | **OPEN** |
| SQ7 WSLg-equivalent status | Plausible negative + Verified components (weston RDP backend maintained) | negative rests on search coverage only | DIY candidates found, liveness unprobed (jacobstoner blog moved offline, wsland unprobed) | partial | **OPEN** |

Source-universe checklist after round 1:
- [x] Official docs — covered (all lanes)
- [x] Semi-official (AUR/archlinux.org/launchpad) — covered (L2, L3)
- [x] Community (Reddit, SE, forums, KDE discuss) — covered (all lanes)
- [x] Code (GitHub/GitLab API liveness probes, issue trackers) — covered (all lanes; x2go code.x2go.org Anubis-walled — recorded as no-results; x2go GitHub org 0 repos — Verified finding)
- [x] Practice (TauCeti blog, institutional how-tos) — covered (L1, L2, L3)
- [x] Upstream (MS-RDPERP context via FreeRDP wiki, NX codecs via man pages) — covered (L4, L3)

## Round dispatch logs

Round 1: 2026-10-25, 4 lanes as planned above (L1 ssh-x11-waypipe, L2 xpra, L3 x2go, L4 rdp-remoteapp). All completed; files read whole by orchestrator.

### Round 2 dispatch (2026-10-25, autonomous — 2 OPEN rows → 2 lanes)

- OPEN row SQ6 → **L5 menu-integration** (menu-integration/lane5-r2.md): expects to find published third-party working `.desktop` examples (ArchWiki, askubuntu/SE, blogs, r/kde) for ssh -X / waypipe / xpra / x2goclient launcher entries; if none exist for a transport, that absence becomes the documented finding.
- OPEN row SQ7 → **L6 wslg-diy** (wslg-diy/lane6-r2.md): expects liveness probes (GitHub API on qq1038765585/wsland; web.archive.org for jacobstoner blog) + fresh 2025/2026 searches for any maintained weston-RDP/seamless project; negative claim to be hardened or overturned.
- Round 2 lanes must not re-search round-1 Verified facts (seeded verbatim in briefs).

### Round 2 assessment (2026-10-25)

| sub-question | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts | status |
|---|---|---|---|---|---|
| SQ6 .desktop start-menu recipes | Verified — ssh -X: unix.SE 805954 working KDE example (Exec=/usr/bin/ssh -nTX host app, ksshaskpass, May 2026); waypipe: WaypipeDesktop + remote-app-launcher generate per-app entries (author-documented); xpra: shipped xpra.desktop attach handler (Synacktiv quote); x2go: official published-apps menu from server .desktop files | yes per path (verified example/tool artifact + official docs + community practice) | yes (8+ query families per transport; absences documented with query lists) | partial (lane verdict; residual = assembled-only Exec for xpra/x2go with every component individually sourced) | CLOSED |
| SQ7 WSLg-equivalent status | Negative hardened to positively-evidenced: grd + krdp documented full-session-only (official READMEs, repo-tree probe); xrdp RAIL self-declared incomplete, frozen; jacobstoner DIY (Wayback, read full) reached full-desktop only, "would be cool to get rail support"; wsland Windows/WSL-only (probe); wlroots RDP backend removed upstream, waylib 404; IronRDP/FreeRDP RAIL = components vs Windows | yes (official docs of both desktop stacks + liveness probes + 7 query families + GH search) | yes (DIY candidates probed; near-misses excluded with evidence) | answered | CLOSED (documented absence; negative existence claims cannot be more than coverage-hardened) |

No OPEN rows remain after round 2 → no round-3 gate question required (rule: ask only while OPEN rows justify another round). Proceeding to synthesis.

## Corpus manifest

| file | axis | claim summary | tier scheme | status |
|---|---|---|---|---|
| ssh-x11-waypipe/lane1.md | SQ1, SQ2, SQ6(a,b) | ssh -X prereqs/-X-vs-Y/audio/VirtualGL; waypipe architecture/prereqs/GPU/pitfalls/maintenance (v0.11.3); .desktop patterns | Verified/Plausible/Speculative | complete, read whole |
| xpra/lane2.md | SQ3, SQ6(c) | xpra seamless model/commands, X11 backend headless OK, Wayland backend WIP, clipboard caveat Wayland-client, audio/print/webcam, tiers (Ubuntu server tier 3), noble 3.1.5 dead → apt repo, alive v6.5.5 | Verified/Plausible/Speculative | complete, read whole |
| x2go/lane3.md | SQ4, SQ6(d) | published-apps mode + /etc/x2go/applications .desktop files, clone-window mechanism, NX codecs, noble packages, Wayland crash #1414 + xcb workaround, nxagent GLX limits, alive-but-dormant | Verified/Plausible/Speculative | complete, read whole |
| rdp-remoteapp/lane4.md | SQ5, SQ7, SQ6(RDP) | xrdp RAIL incomplete/stalled (maintainer quotes), no allow-list, black-box community report; FreeRDP /app mature vs Windows only; Remmina no RAIL; blockers → impractical | Verified/Plausible/Speculative | complete, read whole |
| menu-integration/lane5-r2.md | SQ6 | verified ssh-X .desktop example (unix.SE 805954); waypipe .desktop generators (B1/B2); xpra shipped entry + foreground caveat; x2go official menu + assembled wrapper gap; KDE has no remote-app menu feature | Verified/Plausible/Speculative | complete, read whole |
| wslg-diy/lane6-r2.md | SQ7 | negative hardened: grd/krdp full-session only; xrdp RAIL frozen; jacobstoner DIY no-seamless; wsland Windows-only; wlroots RDP removed; IronRDP = client components | Verified/Plausible/Speculative | complete, read whole |
| REPORT.md | synthesis | options matrix, ranked recommendation, DE deliverable | inherits lane tiers | final |

## On-target validation (2026-10-25, live test by user on CachyOS KDE client -> Ubuntu VM 'agents.vm')

Setup that works: client `waypipe --no-gpu [--xwls] ssh peter@agents.vm.homelab.fahsel.ch <app>` (server waypipe = Rust 0.11.x per mainloop.rs/dmabuf.rs error signatures).

1. CONFIRMED (was Verified-by-docs, now on-target): headless server without /dev/dri kills the remote waypipe dmabuf init (`dmabuf.rs Failed to get physical devices: ERROR_INITIALIZATION_FAILED`, then `we don't have any display`) -> `-n/--no-gpu` is the required and sufficient fix (official flag semantics: "Block protocols like wayland-drm and linux-dmabuf which require access to e.g. render nodes").
2. NEW pitfall, on-target Verified: **GTK3 apps need explicit `GDK_BACKEND=wayland` when waypipe runs with `--xwls`** — with DISPLAY set (xwayland-satellite), GTK3's autodetect prefers X11 and gtk::init fails inside Tauri/tao apps (BoolError "Failed to initialize GTK"); GTK_A11Y=none, GDK_BACKEND=x11 and --appimage-extract-and-run did NOT help, `env GDK_BACKEND=wayland` did. Qt/firefox apps pick Wayland via XDG_SESSION_TYPE and were unaffected. Persist via fish `set -Ux GDK_BACKEND wayland` or env in the .desktop Exec.
3. fork/exec child apps under waypipe inherit the fake compositor (WAYLAND_DISPLAY=wayland-<rand>, socket in server XDG_RUNTIME_DIR=/run/user/1000) — child-window follow-up works for direct spawns; portal/D-Bus-activated starts remain the known gap (see lane1/lane5).
