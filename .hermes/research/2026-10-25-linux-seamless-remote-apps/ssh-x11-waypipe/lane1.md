# Lane L1 — SSH X11 forwarding (`ssh -X/-Y`) and waypipe for seamless remote GUI apps

Research date: 2026-10-25. Client = CachyOS / KDE Plasma 6 / Wayland (XWayland available); server = Ubuntu/Kubuntu 24.04, possibly headless. Sub-questions: SQ1 (ssh -X), SQ2 (waypipe), SQ6 (.desktop integration) for these two transports.

---

## A. SSH X11 forwarding (`ssh -X` / `ssh -Y`)

**1. Mechanism: sshd on the server allocates a proxy X display (localhost:10+offset) and tunnels the X11 protocol over the SSH connection; X traffic appears to apps as a normal DISPLAY.**
- Source: https://man.openbsd.org/sshd_config (official docs)
- Quote: "`sshd_config` — OpenSSH daemon configuration file … `X11DisplayOffset` … 's X11 forwarding. This prevents sshd from interfering with real X11 servers. The default is 10."
- Tier: Verified

**2. Server-side prerequisite #1: OpenSSH upstream disables X11 forwarding by default (`X11Forwarding no`), but the Ubuntu/Debian openssh-server package ships it enabled.**
- Source: https://man.openbsd.org/sshd_config (official) and https://manpages.ubuntu.com/manpages/noble/man5/sshd_config.5.html (official, Ubuntu noble build of openssh 1:9.6p1-3ubuntu13.20)
- Quote (OpenBSD): "Specifies whether X11 forwarding is permitted. The argument must be `yes` or `no`. The default is `no`."
- Quote (Ubuntu): "Note that the Debian `openssh-server` package sets several options as standard in /etc/ssh/sshd_config which are not the default in sshd(8): … `X11Forwarding` yes"
- Tier: Verified

**3. Server-side prerequisite #2: on a headless server (no desktop session, no X server installed) X11 forwarding works — the server needs only `xauth`, not a full X11 stack; it never needs a display of its own.**
- Source: https://wiki.archlinux.org/title/OpenSSH#X11_forwarding (official wiki)
- Quote: "For X11 forwarding the remote host does not need to have a full X11 system installed; however, it needs at least to have _xauth_ installed. _xauth_ is a utility that maintains `Xauthority` configurations used by server and client for authentication of X11 session"
- Cross-ref (client-side requirement mirror): sshd_config `XAuthLocation` "Specifies the full pathname of the xauth(1) program, or `none` to not use one."
- Tier: Verified
- Practical Ubuntu note: install `xauth` (package `xauth`; often already present via desktop/sudo recommends — if `X11 forwarding request failed on channel 0` appears with sshd OK, missing xauth is the classic cause; Arch wiki: "If you get 'X11 forwarding request failed on channel 0' … make sure package xorg-xauth [is installed]").

**4. Client config for -X vs -Y vs -Y trusted: `-X` = opportunistic ForwardX11 with *untrusted* clients under the X11 SECURITY extension; `-Y`/`ForwardX11Trusted yes` = trusted, no security-extension restrictions; untrusted forwarding additionally has a 20-minute idle timeout by default.**
- Source: https://man.openbsd.org/ssh_config (official docs)
- Quote: "If this option is set to `no` (the default), remote X11 clients will be considered untrusted and prevented from stealing or tampering with data belonging to trusted X11 clients. Furthermore, the xauth(1) [cookie is substituted/destroyed] … See the X11 SECURITY extension specification for full details on the restrictions imposed on untrusted clients." and "Specify a timeout for untrusted X11 forwarding … The default is to disable untrusted X11 forwarding after twenty minutes has elapsed."
- Tier: Verified
- Arch wiki tip: "You can enable the `ForwardX11Trusted` option (`-Y` switch on the command line) if GUI is drawing badly or you receive errors; this will prevent X11 forwardings from being subjected to the X11 SECURITY extension" — use `-Y` for long-running app use, `-X` otherwise.

**5. Behavior on a Plasma 6 Wayland client: forwarded X11 apps are ordinary X11 clients of the client machine; XWayland presents them as normal managed windows (taskbar, snapping, decorations work). ssh -X cannot forward *native Wayland* apps at all, because it only proxies the X11 protocol; Wayland was not designed as a network protocol (shared-memory buffers).**
- Source (community, high-quality): https://unix.stackexchange.com/questions/776767/what-is-the-ssh-x-equivalent-for-wayland (community) — accepted answer, score 14:
- Quote: "waypipe is the closest equivalent. It is not raw Wayland-over-SSH, as Wayland is not primarily a network-oriented protocol – as I understand, it relies heavily on shared memory (whereas in X11 that's completely optional) – but it's probably as close as you can get."
- Corroboration: https://askubuntu.com/questions/1466109/recommended-current-22-04-way-to-forward-apps-gui-wayland-to-wayland (community) shows users on Ubuntu 22.04 Wayland still using `ssh -X` for X11 apps and hitting issues only with Wayland-native ones; TauCeti practice blog: "This is more or less the solution that always works."
- Tier: Plausible (no official KDE doc states the XWayland-integration claim; mechanism + multiple community confirmations)

**6. Clipboard over ssh -X: works for free, because the remote app talks to the *client's* X server (XWayland) — CLIPBOARD/PRIMARY selections never leave the client; KDE Klipper/clipboard tools see the remote app as a local X client.**
- Source: mechanism implied by official docs (client-side proxy display): https://man.openbsd.org/sshd_config — "the client's X11 display server may be exposed to attack when the SSH client requests forwarding"; community: TauCeti blog uses ssh -X apps "as they were local ones" on KDE 6.
- Quote (supporting the single-X-server property): OpenBSD ssh_config: "Users with the ability to bypass file permissions on the remote host (for the user's X11 authorization database) can access the local X11 display through the forwarded connection."
- Tier: Plausible (no dedicated official "clipboard" doc; universally reported working; caveat: clipboard races on connect with systemd-activated XWayland occasionally reported in community threads)

**7. Audio is NOT forwarded by ssh -X itself; the standard recipe is a reverse SSH tunnel to the client's PulseAudio/PipeWire native TCP protocol: on the client `pactl load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1`, connect with `ssh -R 4713:localhost:4713`, and on the remote set `PULSE_SERVER=tcp:127.0.0.1:4713`. PipeWire (pipewire-pulse) serves the same PulseAudio protocol, so the identical recipe works on PipeWire clients.**
- Source: https://wiki.archlinux.org/title/PulseAudio#Network_sharing (official wiki) and https://wiki.archlinux.org/title/PipeWire (official wiki)
- Quote (PulseAudio wiki): "It is also possible to authenticate based on client IP address: load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24"; (PipeWire wiki): "Then set the environment variable `PULSE_SERVER=tcp:127.0.0.1:4713` in the inner user's session."
- Quote (PipeWire serves Pulse protocol): "Install pipewire-pulse. It will replace pulseaudio and pulseaudio-bluetooth." + "`$ pactl info` … Server Name: PulseAudio (on PipeWire x.y.z)"
- Tier: Verified (recipe documented); Plausible for the ssh -R 4713 tunnel variant (documented in many community guides; the wiki pages show the module + env var, the tunnel is a plain SSH port-forward)
- Note: server-side app only needs libpulse/PulseAudio-compatible client libs; no sound hardware required on a headless Ubuntu server.

**8. 3D/GPU apps over ssh -X are slow (indirect GLX sends all GL commands over the wire); the documented acceleration recipe is VirtualGL: `vglconnect user@server` (ssh -X wrapper that also starts vglclient) then `vglrun app` on the server — rendered frames, not GL commands, cross the network.**
- Source: https://www.virtualgl.org/vgldoc/2_1_3/ (official VirtualGL User's Guide; also 2_1_2/2_1_1)
- Quote: "This mode is recommended for use on secure local-area networks. The X11 traffic is encrypted, but the VirtualGL image stream is left unencrypted to maximize performance." and procedure: "/opt/VirtualGL/bin/vglconnect {user}@{server} … In the SSh session, start a 3D application using VirtualGL: /opt/VirtualGL/bin/vglrun [vglrun options] {application_executable_or_script}"
- Also: "With VirtualGL, the OpenGL commands and 3D data are instead redirected to a 3D graphics accelerator on the application server, and only the rendered 3D images are sent to the client machine." And "Traditional … indirect rendering … causes all of the OpenGL commands and 3D data to be sent over the network to be rendered on the client machine. This is not a tenable proposition unless … the network is very fast."
- Tier: Verified
- Subtlety (official): pure `vglconnect` opens the VGL image transport on dedicated TCP ports 4200-4299 (firewall); `vglconnect -s` tunnels the image stream through SSH at a cost: "using SSh tunneling can reduce VirtualGL's performance by anywhere from 20-40% on high-speed networks such as Ethernet." VirtualGL + TurboVNC (X proxy mode, `vglrun +s`) is the official recommendation for high-latency links.

**9. Latency/quality of ssh -X: chatty X11 protocol, noticeable typing lag and periodic UI freezes; tolerable on LAN, poor on WAN.**
- Source: https://www.tauceti.blog/posts/ssh-x-vs-xpra-vs-waypipe-remote-display-comparison-single-window/ (practice blog, 2026-01-26)
- Quote: "While it works quite well it's not really the fastest solution esp. if your remote host is only accessible via some slow Internet connection… My main problem with this solution was always that sometimes the UI stuck. You can't type anything anymore and have to wait a few seconds before it works again. Also the latency when typing is noticeable… Using `ssh -X` for a temporary solution is fine. But using it all the time with lots of remote applications isn't that much fun."
- Tier: Plausible (single practitioner, consistent with VirtualGL's official characterization of X11 as chatty)

**10. Security caveat of ssh -X on untrusted servers: with ForwardX11Trusted a compromised server can snoop/inject into the client display; untrusted mode + ForwardX11Timeout exist to bound this.**
- Source: https://man.openbsd.org/ssh_config (official)
- Quote: "X11 forwarding should be enabled with caution. Users with the ability to bypass file permissions on the remote host (for the user's X11 authorization database) can access the local X11 display through the forwarded connection. An attacker may then be able to perform activities such as keystroke monitoring if the ForwardX11Trusted option is also enabled."
- Tier: Verified

## B. waypipe (Wayland application forwarding over SSH)

**11. Mechanism: waypipe is a Wayland-client proxy; `waypipe ssh user@host app` runs waypipe on both ends, wraps ssh with Unix-socket forwarding, and the *remote* waypipe instance itself acts as a fake Wayland compositor for the app — the client-side waypipe connects to the real local compositor and shuttles messages + shm buffer deltas.**
- Source: https://manpages.debian.org/unstable/waypipe/waypipe.1.en.html (official man page, v0.11.2) and https://gitlab.freedesktop.org/mstoeckl/waypipe README (official)
- Quote (man page): "Prefixing an **ssh ...** command to become **waypipe ssh ...** will automatically run **waypipe** both locally and remotely, and modify the ssh command to set up forwarding between the two instances of **waypipe**. The remote instance will act like a Wayland compositor, letting Wayland applications that are run remotely be displayed locally."
- Quote (README): "`waypipe ssh user@theserver weston-terminal` will run `ssh`, connect to `theserver`, and remotely run `weston-terminal`, using local and remote `waypipe` processes to synchronize the shared memory buffers used by Wayland clients between both computers."
- Tier: Verified

**12. Server-side prerequisites: waypipe installed on BOTH ends plus OpenSSH ≥ 6.7 (for Unix-domain-socket forwarding); the server needs NO Wayland compositor session and NO GPU session — the remote waypipe *is* the app's "compositor". Client needs a running Wayland compositor (Plasma 6 = fine).**
- Source: https://manpages.debian.org/unstable/waypipe/waypipe.1.en.html (official) — BUGS/Common issues + DESCRIPTION
- Quote: "The **waypipe ssh** command requires that the **ssh** executable supports Unix socket forwarding; this is only supported in OpenSSH since version 6.7 (from 2014), and may require specific configuration." and "When run as **waypipe server**, it will run the command that follows in its command line invocation, set up its own Wayland compositor socket, and try to connect to its matching **waypipe client** socket"
- Headless-viability corroboration (practice): TauCeti blog: "Waypipe should be installed on both the local and remote computers… The requirements are way less than for Xpra. It's mainly ffmpeg, lz4, zstd and OpenSSH (obviously). Of course you need Wayland running. In my case it's KDE 6.x running on Wayland." (the "you need Wayland" refers to the display side = client).
- Tier: Verified for the no-compositor-needed-on-server architecture (man page); Plausible for full practical headless-server experience (reported working; portal/dbus caveats below)

**13. Ubuntu/Kubuntu packaging: waypipe is in Ubuntu 24.04 (noble) universe as 0.8.6-2build1 — markedly older than upstream 0.11.x; Debian trixie ships 0.9.2, unstable 0.11.2.**
- Source: https://launchpad.net/ubuntu/noble/+package/waypipe (official) + https://manpages.debian.org/unstable/waypipe/waypipe.1.en.html (official)
- Quote: "Binary package "waypipe" in ubuntu noble … waypipe 0.8.6-2build1 in amd64 (Release)"
- Tier: Verified
- Consequence (plausible): 0.8.6 predates the Rust rewrite (0.10+) and newer flags such as `--xwls`/`--secctx`; for X11-app-via-waypipe or DMABUF/video features you may need a backport/self-build.

**14. X11-only apps can also be forwarded through waypipe using `--xwls` + xwayland-satellite (Xwayland run remotely as a Wayland client of the waypipe fake compositor).**
- Source: https://gitlab.freedesktop.org/mstoeckl/waypipe README (official; README.md fetched 2026-10-25) and man page; https://github.com/Supreeeme/xwayland-satellite (official)
- Quote (waypipe man page): "**--xwls** Use **xwayland-satellite** to run X clients under Wayland; for server or ssh modes. This binds X display sockets for the next available display number and sets the DISPLAY environment variable for the program run under **waypipe server**. This option will only work if xwayland-satellite is installed and in PATH."
- Quote (satellite README): "xwayland-satellite grants rootless Xwayland integration to any Wayland compositor implementing xdg_wm_base and viewporter."
- Tier: Verified (feature documented). Note availability requires waypipe ≥ 0.10-ish → NOT in noble's 0.8.6 (Plausible).

**15. GPU/3D under waypipe: real dmabuf/GPU rendering is supported (vulkan/gbm path) but is the flakiest area; official guidance is the `--no-gpu` software-rendering fallback; optional lossy `--video h264/vp9/av1[,hw]` DMABUF encoding exists.**
- Source: README (official): "A workaround that may help for some programs using OpenGL or Vulkan is to run Waypipe with the `--no-gpu` flag, which may force them to use software rendering and shared memory buffers. (Please still file a bug.)" and "dmabuf support: vulkan (to support programs using GPU rendering and DMABUFs)"; man page: "**--video V** Compress specific DMABUF formats using a lossy video codec. Opaque, 10-bit, and multiplanar formats, among others, are not supported."
- Tier: Verified
- Practice data point: TauCeti: "Then the application really 'feels' like it's running locally. You don't see much of a difference." (2D workloads, KDE 6 client).

**16. Clipboard under waypipe: clipboard/primary-selection are Wayland protocols proxied like any other, and generally work; the common gotchas are single-instance apps and apps that refuse the fake compositor, for which `wl-clipboard` (wl-copy/wl-paste) via an SSH tunnel is the documented community workaround.**
- Source (community): https://gist.github.com/dcode/912be128174c468a2dc28f263bdb7328 "Automatic waypipe setup for SSH remote forwarding of clipboard (via wl-copy/paste) and other Wayland clients" (practice)
- Quote: title itself: "Automatic waypipe setup for SSH remote forwarding of clipboard (via wl-copy/paste) and other Wayland clients"
- Tier: Plausible (waypipe's own docs don't enumerate clipboard; forwarding follows from full protocol proxying: "It does not filter which Wayland protocols the compositor makes available to the client")

**17. Compression/quality knobs: `-c none|lz4|zstd[=N]` (default lz4; zstd recommended for slow links), `--threads`, and `waypipe bench` to pick a setting for your bandwidth.**
- Source: https://manpages.debian.org/unstable/waypipe/waypipe.1.en.html (official)
- Quote: "Select the compression method applied to data transfers. Options are _none_ (for high-bandwidth networks), _lz4_ (intermediate), _zstd_ (slow connection). The default compression is _lz4_." and "The **waypipe bench** mode can be used to estimate which compression options produce the lowest latency, for a given connection bandwidth and number of threads."
- Tier: Verified

**18. Latency/quality of waypipe on LAN: near-local feel, fast startup, no typing lag; practice reports contrast it favorably against both ssh -X and xpra. On WAN, lz4/zstd compression mitigates, but timing/traffic analysis is inherent (security note).**
- Source: https://www.tauceti.blog/posts/ssh-x-vs-xpra-vs-waypipe-remote-display-comparison-single-window/ (practice blog)
- Quote: "Running the command above for the first time already makes it obvious that the remote application startup is pretty fast (faster than with Xpra). Then the application really 'feels' like it's running locally. You don't see much of a difference. It behaves like a local application and there is nearly no latency when typing."
- Tier: Plausible (single practitioner; consistent with the buffer-delta proxy architecture)

**19. Known waypipe pitfalls (documented): (a) single-instance apps (firefox, kate, gnome-terminal) started under waypipe may just focus/talk to the instance already running on the server; (b) xdg-desktop-portal dialogs (e.g. KDE file picker) pop up on the *server*, hanging the app; (c) no strong security model — the client's compositor protocols are blindly exposed to remote apps.**
- Source: man page BUGS (official): "Some programs (gnome-terminal, firefox, kate, among others) have special mechanisms to ensure that only one process is running at a time. Starting those programs under Waypipe while they are running under a different Wayland compositor may silently open a window or tab in the original instance of the program."
- Source: https://discuss.kde.org/t/file-picker-dialog-opens-on-wrong-remote-screen-when-running-applications-via-waypipe/41160 (community, 2025-10-30): "opening a file (via Ctrl-O) opens the file picker dialog on the host machine's monitor, rather than on the waypipe session on the remote machine, resulting in the waypipe application effectively hanging… If the default (GTK) file picker implementation is enabled, it opens correctly."
- Source: man page SECURITY: "Waypipe does not provide any strong security guarantees, and connecting to untrusted servers is not recommended. It does not filter which Wayland protocols the compositor makes available to the client."
- Tier: Verified (a, c) / Plausible (b, single report but concrete workaround)
- Extra (plausible, community): app env quirks — man page documents `waypipe ssh user@host env XDG_SESSION_TYPE=wayland dolphin` to force Wayland backends; Java apps under --xwls need `_JAVA_AWT_WM_NONREPARENTING=1` (xwayland-satellite README).

**20. MAINTENANCE of waypipe (probe date 2026-10-25): the brief's GitHub URL github.com/soffrey/waypipe is dead — `https://api.github.com/repos/soffrey/waypipe` returns `{"message": "Not Found", "status": "404"}` (same for /releases); upstream has long been gitlab.freedesktop.org/mstoeckl/waypipe. There it is very actively maintained: last_activity_at = 2026-10-20T01:06:28Z; latest release v0.11.3 (2026-10-20), with v0.11.2 (2026-08-25), v0.11.1 (2026-08-16), v0.11.0 (2025-12-20), 0.10.x line through 2025. Rust rewrite current; C version kept as `waypipe-c` for old systems.**
- Source: probes via https://api.github.com/repos/soffrey/waypipe and https://gitlab.freedesktop.org/api/v4/projects/3237 (+ /releases) (official APIs), plus README "Waypipe is developed at gitlab.freedesktop.org/mstoeckl/waypipe; file bug reports or submit patches here."
- Tier: Verified

## C. SQ6 — normal KDE start-menu entry for each transport

**21. Mechanism for both transports: a user .desktop file (e.g. ~/.local/share/applications/remote-firefox.desktop) with `Terminal=false` and an `Exec=` that wraps the whole launcher; KDE menus read these directories automatically; `Icon=` takes an icon name or path.**
- Source: https://develop.kde.org/docs/features/desktop-file/ (official KDE docs)
- Quote: "Icon can use the path to an icon shipped with your application or a file name available in the system. Terminal=false states your application doesn't need to be run in a terminal before it is executed, and it is commonly used for GUI applications."
- Tier: Verified (generic mechanism)

**22. ssh -X .desktop pattern (constructed from documented pieces; no verbatim official example found): `Exec=ssh -Y -f -N -o ExitOnForward=yes user@server app`-style or `Exec=sh -c 'ssh -Y user@server app'` with key auth so no password prompt appears; `-f`/`-n` + no terminal window because `Terminal=false` makes KWin launch it detached.**
- Source (documented components): https://man.openbsd.org/ssh_config (official) — "BatchMode … If set to `yes`, user interaction such as password prompts and host key confirmation requests will be disabled. This option is useful in scripts and other batch jobs where no user is present" (use `BatchMode yes`/`IdentityFile` in `~/.ssh/config` Host stanza); Arch wiki SSH keys for key auth.
- Tier: Plausible (each piece documented; the exact assembled Exec line is my construction, not a quoted example)

**23. waypipe .desktop pattern: `Exec=waypipe ssh user@server app` (command-line args before `ssh` belong to waypipe, after belong to ssh), again with key auth; the KDE community uses exactly the `waypipe ssh host app` one-liner for per-app launching.**
- Source: README (official): "Command line arguments before `ssh` apply only to `waypipe`; those after `ssh` belong to `ssh`."; TauCeti (practice): "Starting Vivaldi web browser on a remote host is now as simple as (I created an 'alias' for this and a lot of other commands): `waypipe ssh remote-host-name vivaldi`"
- Tier: Plausible for the .desktop wrapper itself (constructed); Verified that the wrapped command is the documented per-app launcher form.
- Caveat (plausible): if ssh/waypipe errors, the menu launch dies silently — wrap in a script with logging (`Exec=sh -c 'waypipe ssh … >> ~/.waypipe.log 2>&1'`).

**24. Terminal-window pitfall: without `Terminal=false` (or a konsole-specific launcher), KDE may open a terminal for console commands; community threads cover ssh-launcher desktop files specifically in the konsole variant.**
- Source: https://www.reddit.com/r/kde/comments/fa012e/start_ssh_desktop_launcher_in_own_konsole/ (community) + develop.kde.org quote above.
- Tier: Plausible

## D. Cross-cutting comparison for this use case (seamless single window on Plasma 6 Wayland client)

**25. For X11 apps both transports land the window on the client desktop seamlessly; for Wayland-native apps only waypipe works; ssh -X wins on "always works, zero extra server deps beyond xauth", waypipe wins on latency/feel.**
- Source: TauCeti blog (practice): ssh -X — "This is more or less the solution that always works"; waypipe — "that was exactly what I was searching for… for me it's perfect."
- Tier: Plausible

**26. Ubuntu 24.04 server readiness differs: ssh -X works out of the box of the Ubuntu OpenSSH package (X11Forwarding yes pre-set) once `xauth` is installed; waypipe needs `apt install waypipe` on server (0.8.6 in noble) + client (CachyOS: extra repo, current) but no compositor/dbus session for basic apps.**
- Sources: Ubuntu manpages noble sshd_config (Verified, see finding 2); launchpad noble waypipe 0.8.6-2build1 (Verified, finding 13); TauCeti: "Luckily for me Ubuntu 24.04 and 22.04 already offer a package and same for Archlinux." (Plausible).
- Tier: Verified / Plausible as cited

---

## Searched, found nothing
- `https://api.github.com/repos/soffrey/waypipe` (official API) — 404; the GitHub-hosted waypipe repo named in the brief does not exist; only freedesktop GitLab upstream.
- Official OpenSSH / Ubuntu documentation of *clipboard* behavior for X11 forwarding (none exists; only mechanism inference + community reports).
- Official KDE/Plasma documentation stating that ssh -X forwarded apps integrate via XWayland (only community confirmations; r/wayland "Running Remote GUI Applications on Wayland", unix.SE 776767, askubuntu 1466109).
- Verbatim official documentation example of a `.desktop` file whose `Exec=` wraps `ssh -X` or `waypipe ssh` (searched official KDE docs, waypipe docs/README, waypipe man page; only the generic KDE desktop-file spec + community launchers/aliases found).
- Headless-server (pure TTY, no login session) end-to-end waypipe success report with full environment on Ubuntu 24.04 specifically (closest: TauCeti LAN/VM setup, Manjaro forum thread, waypipe man page architecture claims).
- waypipe clipboard protocol-support statement in waypipe's own docs (no explicit "clipboard" section in README/man page).
- Any official statement on waypipe WAN latency numbers (only qualitative `--compress zstd (slow connection)` + `waypipe bench`).

Sub-question status from this lane's view: answered
