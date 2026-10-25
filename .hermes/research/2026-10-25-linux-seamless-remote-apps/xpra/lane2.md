# SQ3 (xpra) + SQ6 (KDE menu icon) — Lane 2 findings
Research date: 2026-10-25 (Europe/Zurich). All probes performed on this date.
Target scenario: GUI app on Ubuntu 24.04 server → seamless window on CachyOS/KDE Plasma 6 client.

## Findings

1. Xpra's core model is "screen for X": run X11 apps remotely, each appears as its own client-side window, disconnect/reconnect without losing state.
   - Source: https://wiki.archlinux.org/title/Xpra · official-community (ArchWiki, quoting upstream README)
   - Quote: "its seamless mode allows you to run X11 programs, usually on a remote host, direct their display to your local machine, and then to disconnect from these programs and reconnect from the same or another machine(s), without losing any state."
   - Tier: Verified

2. Seamless mode = real client-side windows managed by the local window manager (move, resize, minimize, taskbar/alt-tab, span monitors) — explicitly NOT a full-desktop-in-one-window.
   - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/Seamless.md · official docs
   - Quote: "Each remote application gets its own window on your desktop: you can move, resize, minimize, and switch to it alongside your local applications." / "Remote windows are managed by your local operating system and window manager. Place them across your monitors, switch between them normally, and use them alongside local applications."
   - Tier: Verified

3. One-step start+attach over SSH (the ssh mode): `xpra seamless ssh://USER@HOST/ --start-child=firefox`; persistent variant: server-side `xpra seamless :100 --start-child=xterm` then client `xpra attach ssh://USER@HOST/100`.
   - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/Seamless.md and docs/Usage/README.md · official docs
   - Quote: "xpra seamless ssh://USER@HOST/ --start-child=xterm ... The application window should appear on your desktop. You can disconnect and later reconnect without stopping the remote application: `xpra attach ssh://USER@HOST/`"
   - Tier: Verified

4. xpra.org positions ssh mode against ssh -X: same workflow, better performance, plus persistent reconnect (xpra must be installed on the server).
   - Source: https://xpra.org/index.html · official site
   - Quote: "xpra start ssh://USERNAME@HOST/ --start=xterm This is similar to ssh -X, except that performance will be noticeably better and you can disconnect and re-connect to this session as many times as you like."
   - Tier: Verified (vendor claim; direction corroborated by community, see #22)

5. Modes: `seamless` (per-app windows), `desktop` (full remote DE in one window, e.g. `xpra desktop --start-child=fluxbox`), `shadow` (mirror an existing display). Attach also accepts a session name instead of display number.
   - Source: docs/Usage/README.md, docs/Usage/Seamless.md, ArchWiki (start-desktop example) · official docs / ArchWiki
   - Quote: "xpra desktop --start-child=fluxbox" · "xpra shadow ssh://SERVERHOST/" · ArchWiki: "xpra start-desktop :7 --start-child=xfce4-session --exit-with-children"
   - Tier: Verified

6. Server side is X11: a seamless session runs its own private X server using the patched dummy driver (Xdummy); Xvfb-style fallback exists (`--xvfb=/usr/bin/Xorg`). No real display or GPU needed on the server.
   - Source: https://xpra-org.github.io/xpra/Download/Linux.html (dependency table) · official docs; https://wiki.archlinux.org/title/Xpra (troubleshooting)
   - Quote: "xorg-x11-drv-dummy / xserver-xorg-video-dummy — the patched dummy driver used by seamless and desktop servers"; ArchWiki: "To solve it is necessary run with `--xvfb=/usr/bin/Xorg`."
   - Tier: Verified

7. Wayland status (server): X11 backend is the default and "broadest compatibility"; a Wayland backend exists but is **experimental** (`--backend=wayland --start-child=weston-terminal`, may need separate `xpra-server-wayland` package). Wayland app-forwarding via window-selective shadowing is "not reliable enough to recommend for general use" (issue #3476).
   - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/Seamless.md · official docs
   - Quote: "The Wayland backend is experimental and may require the separate `xpra-server-wayland` package. Use the X11 backend unless you need Wayland specifically." / "They are not reliable enough to recommend for general use; see issue #3476"
   - Tier: Verified. Practical consequence: Wayland-native apps can't be forwarded today; run them via X11/XWayland or use X11-capable apps.

8. Wayland server-backend is under active development as of late 2026: maintainer (totaam, Jan 26 2026) confirms "we do have a wayland backend via pipewire, and now also a WIP wayland seamless mode"; commits referencing issue #387 land Sep/Oct 2026 (keymap, content types, PIDs).
   - Source: https://github.com/orgs/Xpra-org/discussions/4769 and https://github.com/Xpra-org/xpra/issues/387 · official (maintainer statements, commit trail)
   - Quote: "We do have a wayland backend via pipewire, and now also a WIP wayland seamless ... (the latter is more promising - but that's for `seamless` mode, not shadow)"; on pipewire backend: "it's just giving us a file descriptor we can use with gstreamer - big meh ... Support in xpra was incomplete IIRC (ie: never got around to wire the keyboard properly)"
   - Tier: Verified (as of 2026-10-25)

9. Wayland status (client): xpra clients run on X11 and Wayland, "but Wayland clients are inherently limited". Shadowing an existing Wayland session is not supported.
   - Source: https://github.com/Xpra-org/xpra/wiki/Platforms · official wiki
   - Quote: "Both X11 and Wayland are supported, but Wayland clients are inherently limited."
   - Tier: Verified

10. Clipboard caveat that hits a Plasma 6/Wayland client directly: Wayland restricts clipboard access so xpra cannot synchronize it properly; on X11 clipboard is bidirectional (CLIPBOARD + PRIMARY, `clipboard-direction` option, filters).
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Clipboard.md · official docs
    - Quote: "Wayland severely restricts access to the clipboard, making it impossible to synchronize it properly"; "`clipboard-direction`: can be used to restrict the direction of the clipboard data transfers."
    - Tier: Verified. Practical: run the client session where xpra has X11 (XWayland) or expect degraded clipboard; test before committing.

11. File copy between client and server is only explicit transfer (tray "upload" menu, `xpra send-file` / `xpra control :N send-file`), with size limits and confirmation; "not meant to replace a network filesystem".
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/File-Transfers.md · official docs
    - Quote: "This is not meant to replace a network filesystem, it is only there to facilitate the transfer of individual files between the client and server."
    - Tier: Verified. Drag-and-drop file copy via clipboard: not documented (see gaps).

12. Audio forwarding both directions: server app audio → client speakers, client microphone → server app; GStreamer pipelines, opus/vorbis/flac/mp3 codecs, PulseAudio/PipeWire integration (pavucontrol screenshots show the client on local pulseaudio; `audio-source=pulse:...`).
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Audio.md · official docs
    - Quote: "The most widely tested and supported codecs are opus, vorbis, flac and mp3." / "A Linux client's pavucontrol showing the Xpra application connected to the local pulseaudio server"
    - Tier: Verified (PipeWire specifically works via pulse compat — that hop is Plausible, not quoted).

13. Printing: client printers appear as virtual printers on the server (CUPS forwarding, PDF transport); on Ubuntu server install `cups-filters cups-common cups-pdf python3-cups` and add server user to `lpadmin`.
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Printing.md · official docs
    - Quote: "printers connected to the client to show as virtual printers on the server so that printing can transparently be forwarded back to the client's printer(s)"; "for Debian and Ubuntu the lpadmin group: usermod -a -G lpadmin $USER"
    - Tier: Verified

14. Webcam forwarding client→server exists (Linux server only, needs v4l2loopback kernel module) but is flagged WIP: low framerate, low resolution, high bandwidth; Ubuntu loads v4l2loopback with wrong `exclusive_caps=1` (issue #1596).
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Webcam.md · official docs
    - Quote: "work in progress, see #1030 ... framerate is low ... excessive bandwidth usage ... (ie: Ubuntu, see #1596)"
    - Tier: Verified

15. GPU/3D: OpenGL apps "work by default" but on the virtual framebuffer that is software rendering (llvmpipe). Hardware GPU inside the session requires VirtualGL (`vglrun`, recommended), an existing display (`--use-display=yes`), or Xwayland-with-GPU.
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/OpenGL.md · official docs
    - Quote: "OpenGL applications work by default, but a normal virtual framebuffer uses a software renderer. To use a physical GPU, choose one of the display setups below." / "VirtualGL (recommended) ... runs them on a real GPU while Xpra forwards the resulting frames."
    - Tier: Verified

16. Framebuffer compression: automatic per-window encoding (webp/jpeg/png picture encodings; vp8/vp9/h264/hevc/av1 video), encoder modules vpx/x264/nvenc; "best performance" = NVENC or libva hardware encoders; NVENC "offers the best latency" but needs NVIDIA + PyCUDA (nouveau unsupported; consumer cards need license key or nvidia-patch). Note: NVIDIA codecs officially supported only on tier-1 platforms (Windows/macOS/Fedora), not Ubuntu servers.
    - Source: https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/Encodings.md · docs/Usage/NVENC.md · wiki/Platforms · official docs
    - Quote: "Use NVENC or another hardware encoder supported by libva when available. Hardware encoders compress very well and do so extremely quickly." / "This encoder offers the best latency" / Platforms: "NVIDIA codecs are supported only on tier-1 platforms."
    - Tier: Verified

17. MAINTENANCE (probe 2026-10-25 via GitHub API): repo Xpra-org/xpra `pushed_at: 2026-10-25T13:44:26Z`, last commit 2026-10-25 ("new download pages..."), latest release **v6.5.5 published 2026-10-12**, 124 open issues, ~3030 stars. Very much alive; branches v5.x (LTS), v6.x stable, v7/v8 in flight (v8 needs Python 3.12+).
    - Source: https://api.github.com/repos/Xpra-org/xpra , /releases/latest , /commits · official API
    - Quote: "\"pushed_at\": \"2026-10-25T13:44:26Z\"" / "latest release: v6.5.5 2026-10-12T16:05:48Z"
    - Tier: Verified

18. Platform support tiers (official): Fedora/RHEL 8/9 = tier 1; "Debian and Ubuntu clients" = tier 2; **"Debian or Ubuntu servers" are tier 3 ("Everything else")**; third-party/downstream builds = tier 3.
    - Source: https://github.com/Xpra-org/xpra/wiki/Platforms · official wiki
    - Quote: "'Everything else' includes all 32-bit builds, architectures not listed above, and Debian or Ubuntu servers."
    - Tier: Verified. Practical: an Ubuntu 24.04 *server* is officially unsupported (tier 3) — works in practice, but no upstream guarantees.

19. Ubuntu 24.04 archive xpra is dead: noble ships **3.1.5** — "Unsupported upstream since August 2023; known to be broken with its Pillow version" (Launchpad #2083096); Ubuntu 26.04 doesn't package xpra at all; 3.1.x can't talk to 6.x clients.
    - Source: https://github.com/Xpra-org/xpra/wiki/Distribution-Packages · official wiki
    - Quote: "Ubuntu | Noble aka 24.04 | 3.1.5 | Unsupported upstream since August 2023; known to be broken with its Pillow version"
    - Tier: Verified

20. Server install on Ubuntu 24.04 should use the official xpra.org apt repo (LTS v5.1.x / stable v6.x / beta channels explicitly list Ubuntu 24.04 Noble; DEB repo needs `universe` enabled for all features).
    - Source: https://xpra-org.github.io/xpra/Download/Linux.html · official docs
    - Quote: "Ubuntu 24.04 Noble Numbat ... curl https://xpra.org/get-xpra.sh | bash ... the DEB repositories may require the universe repository to be enabled to get all the features"
    - Tier: Verified

21. Client side on Arch/CachyOS: community repo [extra] carries xpra **6.4.4** (current upstream 6.5.5) — close but lags; upstream wiki (Aug 2026 snapshot) lists Arch "6.4.4 ... flagged out of date". Community confirms chronic lag: "On Archlinux the package is always behind the current release. Sometimes for month." Rolling-release friction: codec breakages after updates, occasional Python downgrade.
    - Source: https://archlinux.org/packages/search/json/?name=xpra (queried 2026-10-25) · https://github.com/Xpra-org/xpra/wiki/Distribution-Packages · https://www.tauceti.blog/posts/ssh-x-vs-xpra-vs-waypipe-remote-display-comparison-single-window/ · official API / wiki / community
    - Quote: "xpra 6.4.4 extra" (API) / "with every update, one codec or another wasn't working anymore that I previously used."
    - Tier: Verified (version), Plausible (severity of Arch breakage — single-source anecdote)

22. Community comparison (TauCeti blog, 2026-01-26; long-time xpra user on Arch + Ubuntu 22.04/24.04, LAN/GBit): xpra "has served me quite well over the years" and is "still a very good solution" esp. on slow links, BUT: window snapping doesn't work on xpra windows, special keys failed in VS Code even with `--keyboard-layout=de --keyboard-variant=nodeadkeys`, and they ultimately switched to waypipe for LAN feel ("nearly no latency when typing"; waypipe startup "faster than with Xpra"). Documented LAN workflow command: `xpra start ssh:remote-host-name --keyboard-layout=de --keyboard-variant=nodeadkeys --microphone=disabled --exit-with-client=yes --clipboard=yes --clipboard-direction=both --daemon=no --printing=no --start-child=vivaldi`.
    - Source: https://www.tauceti.blog/posts/ssh-x-vs-xpra-vs-waypipe-remote-display-comparison-single-window/ · community/practice
    - Quote: "Xpra has served me quite well over the years on Archlinux and Ubuntu (22.04/24.04) and if you want to forward the UI of an application on a remote host with slow Internet connection it's most probably still a very good solution." / "This 'snapping' doesn't work with Xpra."
    - Tier: Plausible (single practitioner, but concrete and recent; ssh -X latency complaints on LAN are a known pattern)

23. Reliability signals last 2 years (GitHub): recurring but generally fixed window-management/edge-case bugs — thick black borders on popups/right-click menus (#4380, closed), window positions/states reset on resume (#4634, closed 2025-07), HiDPI mixed scaling (#4242), "Start menu grayed out on Arch" (#4411, 2024), clipboard broken with gtk backend + GDK_BACKEND=x11 (#5048, closed 2026-09). No mega-thread declaring the seamless use-case broken; 124 open issues on a very active repo.
    - Source: https://api.github.com/search/issues?q=repo:Xpra-org/xpra+... (2026-10-25) · official API
    - Quote: "4634 closed 2025-07-30 Window positions/states reset on resume"
    - Tier: Verified (issue existence), Plausible (overall reliability judgement)

24. SQ6 — xpra's own launcher tooling: the `xpra` GUI ("Xpra" entry installed in the desktop application menu; CLI: `xpra launcher [session-file.xpra]`) provides Browse/Connect/Start/Shadow dialogs; connections can be saved as `.xpra` session files that **double-click to connect** (`autoconnect=true`), and the client Start dialog can list the *server's* .desktop applications (python-xdg, issue #1961).
    - Source: docs/Usage/README.md · docs/Usage/Client.md · https://github.com/Xpra-org/xpra/issues/1961 · official docs
    - Quote: "Open Xpra from your desktop's application menu to get started." / "Double-click an .xpra session file to open its saved connection details. If it is set to connect automatically, Xpra connects without showing the dialog." / issue #1961: "We can use python-xdg Menu to get the list of .desktop applications ... Then the start-command dialog can offer a menu."
    - Tier: Verified

25. SQ6 — KDE start-menu icon: xpra has **no documented feature that generates a KDE menu entry for a remote app** (its menu integration is: install its own launcher entry, register `.xpra`/`xpra+ssl://` handlers, and read the server's menu inside the Start dialog). The documented-practice path is a hand-written freedesktop .desktop file in `~/.local/share/applications/` whose Exec uses the official one-step command, e.g.:
    `[Desktop Entry] Type=Application Name=Remote Firefox Exec=xpra seamless ssh://user@server/ --start-child=firefox Icon=firefox StartupNotify=false`
    — for an already-running session instead use `Exec=xpra attach ssh://user@server/SESSION_NAME`. No terminal popup is needed (KDE doesn't spawn terminals for .desktop apps; `Terminal=false` default); auth is plain SSH keys (`ssh-agent`/`~/.ssh/id_*`; if paramiko rejects them, `--ssh=ssh` forces system ssh — ArchWiki). `--exit-with-client`/`--exit-with-children` control teardown.
    - Source: Exec forms Verified from docs/Usage/Seamless.md + ArchWiki (`xpra start --ssh="ssh" ssh://user@host --exit-with-children --start-child="command"`); the .desktop wrapping itself is standard XDG practice, **not** upstream-documented → this specific recipe: Plausible
    - Quote: "If you see Public Key not accepted by remote side, .ssh/config not used correctly, try to use your normal system ssh client: `xpra start --ssh=\"ssh\" ssh://user@host --exit-with-children --start-child=\"command\"`"
    - Tier: Plausible (assembly of Verified pieces; no upstream example found — see gaps)

26. Session naming + reattach make the icon idempotent-ish: attach by session name (`xpra attach ssh://user@host/myapp`), and the server can be told `--exit-with-children` so the session dies with the app; ArchWiki documents boot-time persistence both server-side (systemd template unit `xpra@.service`) and client-side (`xpra-client@.service` user unit, `xpra attach %i $OPTS`).
    - Source: docs/Usage/Client.md ("Xpra display number or session name") · ArchWiki systemd examples · official docs / ArchWiki
    - Quote: "~/.config/systemd/user/xpra-client@.service ... ExecStart=/usr/bin/xpra attach %i $OPTS"
    - Tier: Verified

27. Latency/compression vs ssh -X: official docs claim xpra adapts encodings to window content and network and "often more comfortable and uses less bandwidth than a complete remote desktop"; ssh -X suffers typing latency and stalls on WAN (xpra.org home page and TauCeti both frame xpra as the fix for slow links; waypipe is the LAN-feel winner when both ends are Wayland, but is a different lane's topic).
    - Source: docs/Usage/Seamless.md · xpra.org home · TauCeti blog
    - Quote: "This is often more comfortable and uses less bandwidth than a complete remote desktop when you only need a few applications."
    - Tier: Verified (docs) / Plausible (LAN-vs-WAN ranking — no published benchmark found in this lane)

28. Non-GTK/other clients: HTML5 browser client exists but keeps windows inside the browser ("Use a regular Xpra client when you want them to behave as native windows"); go-xpra and rust-xpra (client, X11+Wayland) ship in the same official repos.
    - Source: docs/Usage/Seamless.md, Download/Linux.html notes · official docs
    - Quote: "In the HTML5 client, remote windows stay inside the browser page. Use a regular Xpra client when you want them to behave as native windows on your desktop."
    - Tier: Verified

## Searched, found nothing
- Upstream-documented `.desktop`/KDE-menu **generation** feature (auto-create client start-menu icons for remote apps); closest official pieces are the launcher GUI, `.xpra` file association, and server-menu browsing in the Start dialog (issue #1961).
- Clipboard drag-and-drop **file copy** between local desktop and remote app (only tray upload / `send-file` are documented).
- Generic **USB device forwarding** in current docs (only webcam/audio/printer devices are covered; `--usb` not in current feature docs).
- Published quantitative latency benchmark xpra vs ssh -X vs waypipe (only qualitative accounts, e.g. TauCeti).
- Any statement that xpra's Wayland *server* backend is release-ready — it remains experimental/WIP as of the 6.5.5 release (2026-10-12).

Sub-question status from this lane's view: answered
