# Lane L6 (round 2) — Hardening the 2026 negative: "no maintained Linux→Linux seamless remote-app (WSLg-equivalent) project"

Probe date for all GitHub API calls: 2026-10-25. Verdict on the lane's open row: **negative HOLDING, now positively evidenced** (liveness-probed DIY candidates + official docs for GNOME/KDE showing full-desktop-only + xrdp RAIL stall confirmed against primary sources). Nothing overturns it; nothing found assembles server-side RAIL + a Linux client shell for Linux→Linux.

## Findings

### 1. qq1038765585/wsland — alive, but Windows/WSL-only (does NOT target Linux clients)
- **What**: "use wlroots + freerdp server implement wslg like" — experimental WSLg replacement.
- **Liveness**: `pushed_at` 2026-10-13T13:03:52Z ("add sway compositor version"), created 2026-03-09, release `1.2` published 2026-09-26, 4 stars, 3 forks, 0 open issues. ALIVE.
- **Source**: https://api.github.com/repos/qq1038765585/wsland (GitHub API, probed 2026-10-25); README https://raw.githubusercontent.com/qq1038765585/wsland/master/readme.md.
- **Quotes**: "A custom Wayland GUI environment for WSL based on **wlroots** and **FreeRDP Server**." · "`wsland` is currently distributed as a pre-built **WSL VHD image**. This project does not provide source code." · "Requirements: Windows with WSL support … The Linux GUI applications will be displayed through the windows desktop session." · config lives at `C:\ProgramData\Microsoft\WSL\wsland.ini`.
- **Verdict**: Alive DIY hobby project, target = Windows hosts running WSL; zero Linux-client support → does not overturn the negative. Side value: its stated basis "FreeRDP Server - RDP backend and RemoteApp support" shows a third party in 2026 building RAIL on the FreeRDP *server* library (see finding 6). Tier: **Verified**.

### 2. jacobstoner "Wayland RDP Server with audio using Microsoft's WSLg stack" — recovered via Wayback; DIY worked Linux→Linux but WITHOUT seamless windows
- **What**: the round-1 missing primary source. Author ran Microsoft's WSLg forks (weston, PulseAudio, FreeRDP) natively on "a minimal Debian bullseye install".
- **Source**: http://web.archive.org/web/20260519182604/https://blog.jacobstoner.com/wayweston-rdp/ (Wayback snapshot 2026-05-19; live blog offline). Original date ~Dec 2022 (featured in "HN blogs - 13/12/22", https://hnblogs.substack.com/p/hn-blogs-131222).
- **Quotes**: "I got them up and running on a minimal Debian bullseye install." · "Firefox works great. I can stream youtube videos in 1080p with audio on the same network and can't even tell it's remote." · connection command is full-screen only: `xfreerdp /v:10.0.1.135 /cert-ignore /size:1024x768 /f /floatbar:sticky:off,show:always /sound:latency:200 -gfx /rfx` · **the decisive line**: "It would be cool to get rail support in the freerdp client, that would open up some interesting options for virtualizing apps."
- **Verdict**: DIY — proves the weston-RDP half of WSLg works on native Linux→Linux (audio+RemoteFX, fullscreen session), but per-app/seamless was NOT achieved: xfreerdp never negotiated RAIL against MS's weston backend. This *strengthens* the negative: even the best-documented DIY attempt stopped at full-desktop. Tier: **Verified** (archived primary source, read in full).

### 3. GNOME Remote Desktop (grd) — official: full-session modes only, no RAIL/published-app mode
- **Source**: official README, https://gitlab.gnome.org/GNOME/gnome-remote-desktop/-/raw/main/README.md (fetched 2026-10-25).
- **Quote**: "It supports operating as a remote assistance remote desktop server, as a single user headless remote desktop server, and as a headless remote login remote desktop server. It has two protocol backends, RDP and VNC." Uses PipeWire for "streaming pixel content", libei for input, Mutter remote desktop API — i.e., whole-session screen streaming only; no per-app windowing anywhere in the README or docs (configuration.md, kerberos.md, smartcard-redirection.md).
- **Verdict**: maintained (GNOME core) but full-desktop only → supports the negative. Tier: **Verified**.

### 4. KDE krdp / KWin remote desktop — official: full Plasma session only, no RAIL anywhere in the repo
- **Source**: https://raw.githubusercontent.com/KDE/krdp/master/README.md (official KDE mirror, fetched 2026-10-25); repo file tree via GitHub API `git/trees/master?recursive=1` — zero paths matching "rail".
- **Quotes**: "KRdp — Library and examples for creating an RDP server." KCM features = toggle `krdpserver`, users/passwords, port, certificates, "Video quality can be changed between responsiveness and quality" — i.e., one shared session, no app allow-list/publishing concept.
- **Verdict**: maintained (KDE, ships in Plasma's Remote Desktop settings) but exposes the whole logged-in Wayland session; no single-app/RAIL mode exists → supports the negative. Tier: **Verified**.

### 5. xrdp RAIL — stall re-confirmed against the primary wiki; still "incomplete", no movement since 2020/2024
- **Sources**: https://github.com/neutrinolabs/xrdp/wiki/RAIL-support-in-xrdp (last edited by "JUN JIE NAN", Aug 24, 2020, 9 revisions); discussions #3020 (created 2024-03-28, "XRDP Remote App Support?") and #3071 (2024-05-12, "Guidance for RemoteApp") via GitHub API.
- **Quotes (wiki)**: "Current RAIL support in xrdp was done for Authentic8 … Allowing the borders to draw locally, you might not even know you are running a remote app. This makes the general RAIL support in xrdp incomplete. We need to complete this to be MS client compatible." · (#3071 body): "I'm running xrdp on Rocky9, and I see the channel available, but when I specify the full path to an application using the client-side Remote App commands, I'm unable to get it to work."
- **Verdict**: xrdp's RAIL remains partial/Unusable for per-app today (channel toggle + incomplete server code); no new maintainer activity since the round-1 May-2024 "no progress" statements. Tier: **Verified**.

### 6. FreeRDP component-level: RAIL client actively maintained into late 2025; server-side rail channel code exists in-tree
- **Sources**: FreeRDP issue #11816 "xfreerdp remote app fail" opened 2025-08-27, closed via PR #11866 on 2025-09-16, milestone 3.17.2 (https://github.com/FreeRDP/FreeRDP/issues/11816); tree listing `channels/rail/` = `client/ server/ rail_common.c` via GitHub API.
- **Note**: #11816 targets a Windows server (`/app:"program:C:\Users\...\TypeEasy.exe"`) — confirms the client RAIL path is Windows-server-oriented but alive; `channels/rail/server` confirms FreeRDP's server library carries server-side RAIL code (what wsland claims to exploit). Round-1 facts 3–4 stand; these are components, not a Linux→Linux product. Tier: **Verified**.

### 7. IronRDP (Devolutions) — RAIL client under active 2026 development; client-only (vs Windows servers)
- **Sources**: https://github.com/Devolutions/IronRDP/pull/2195 ("decode RemoteApp windowing orders into typed structs", MS-RDPERP), /pull/2196 ("complete the RAIL client channel messages", `ironrdp-client/src/rail.rs`), /pull/2200 ("make RemoteApp windows behave like mstsc's").
- **Verdict**: most active RAIL engineering anywhere in the FOSS scene right now — but it's a Rust protocol library whose RAIL work is client-side against MS servers; no Linux-display-server component. A future DIY building block, not a product today. Tier: **Verified**.

### 8. Duneathor/waydisplay — NEW (2026) Linux→Linux remote display with per-app *launch*, but single-window experimental DIY
- **What**: "WayDisplay is an experimental low-latency remote display system for Linux. The server runs a headless wlroots compositor and streams tiles, video, audio, clipboard data, and input events to an SDL client." H.265/H.264/AV1, io_uring, no RDP at all (own protocol).
- **Liveness**: created 2026-06-01, `pushed_at` 2026-10-04T17:40:19Z, 0 stars, 0 issues, C. Active solo project.
- **Source**: https://api.github.com/repos/Duneathor/waydisplay + README https://raw.githubusercontent.com/Duneathor/waydisplay/main/README.md.
- **Quotes**: "`konsole` is the default app and must be installed on the server; use `--launch-command` to choose another command." · "**Ctrl+Alt+right-click** in the client opens a launcher menu … **LAUNCH APPLICATION** prompts for a server-side command." · "The project is not deployed and the protocol is intentionally unstable." · "WayDisplay currently provides **no authentication or encryption**."
- **Verdict**: closest NEW Linux→Linux thing to WSLg ergonomics (you launch individual apps remotely), but output is one composited SDL client window, not per-window integration with the client desktop; experimental, insecure by design → DIY, does not overturn the negative. Tier: **Verified**.

### 9. cid-chan/wayrdp — brand-new wlroots RDP server, explicitly shares the whole running session
- **Source**: GitHub API (created 2026-09-15, pushed same day, 0 stars); description: "wayrdp is a small native RDP server for wlroots-based Wayland compositors. It shares the desktop session that is already running."
- **Verdict**: embryonic DIY, full-session only. Tier: **Verified**.

### 10. Historical corroboration: upstream wlroots killed its RDP backend; the RDP-fork (waylib) has disappeared
- **Sources**: wlroots 0.10.0 release notes: "The RDP backend has been removed entirely in favor of solutions like wayvnc" (https://github.com/swaywm/wlroots/releases/tag/0.10.0); drop commit "Drop RDP backend … Users interested in remote access to wlroots compositors should use wayvnc" (commit ebdbe177). The `waylessos/waylib` GitHub org/repo (the wlroots fork with an RDP display backend used for Anolis/UWD cloud-desktop demos) now returns 404 on the GitHub API (2026-10-25); only a mirror fork (SunRain/waylib-wlroots) remains.
- **Verdict**: the one serious wlroots-side RDP-server effort is gone upstream and orphaned as a fork → supports the negative. Tier: **Verified** (official release notes + API 404); the "who used waylib" attribution: **Plausible**.

### 11. Sweep confirmation (what this lane searched and what the near-misses actually are)
- `GNOME Remote Desktop RAIL single app`, `krdp KWin remote desktop single application RAIL`, `waylib wlroots RDP display backend headless`, `waylib anolis wlroots RDP backend uwd`, `xrdp RAIL RemoteApp support status 2025`, `IronRDP RAIL MS-RDPERP`, `jacobstoner wayweston`, plus GitHub repo searches (`remote app wayland rdp`, `waylib rdp`).
- Near-misses correctly excluded: kihyun1998/justrdp = "A pure-Rust RDP client library, built as a sans-IO state machine" (alive, pushed 2026-10-23) — client vs Windows; kernalix7/winpodx = per-app RemoteApp of *Windows* apps on Linux, and its issue #299 re-confirms "RemoteApp … is currently implemented only in the X11 backend (xfreerdp / xfreerdp3)" (i.e., wlfreerdp gap, round-1 fact 4 unchanged); rcarmo/go-rdp = RDP client in Go, RAIL only an open wish.
- Existence note only (per scope): proprietary NoMachine (NX) exists as an alternative remote-display product; deliberately not probed.
- Tier: **Verified** for the probe set itself; the negative remains a hardened Plausible→near-certain claim (can never be proven, only coverage-hardened — coverage this round: official docs of the two desktop stacks' RDP servers, the two RAIL server codebases, both RAIL client stacks, GitHub repo search, 7 query families).

## Bottom line
- Overturned? No. As of 2026-10-25 there is still **no maintained project serving per-app (RAIL/seamless) remote applications Linux→Linux**.
- Hardened: the negative now rests on positive evidence, not just search coverage — (a) both official Linux RDP servers (grd, krdp) are documented full-session-only; (b) xrdp RAIL is self-declared "incomplete" and frozen since 2020/2024; (c) the only alive-and-working WSLg DIY (jacobstoner) demonstrably never got seamless windows; (d) the two alive "wslg-like" projects target Windows hosts (wsland) or use a custom single-window protocol (waydisplay); (e) upstream wlroots removed its RDP backend and the waylib fork vanished.
- New nuance for the parent report: all RAIL *ingredients* are being actively maintained in 2025–2026 (FreeRDP client RAIL fixed Sep-2025, FreeRDP server rail channel in-tree, IronRDP RAIL client PRs, MS weston RDP backend kept alive) — the gap is purely that nobody integrates them into a Linux→Linux product. A DIY path remains weston --backend=rdp-backend.so (server-side RAIL retained from MS) + any RAIL-capable Linux client; jacobstoner showed even that client negotiation was unsolved.

## Searched, found nothing
- Any maintained Linux→Linux published-app/seamless RDP server (searched: GNOME Remote Desktop, KDE krdp/KWin, xrdp, weston, wlroots, wayrdp, waylib, waydisplay, justrdp, winpodx, go-rdp, GitHub repo search, 7+ query families in 2025/2026 vocabulary).
- A Linux port or fork of wsland for non-WSL hosts; a revived waylessos/waylib (GitHub 404).
- Any issue/discussion/commit in xrdp or krdp post-dating 2024 indicating RAIL progress.

Sub-question status from this lane's view: answered
