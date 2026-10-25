# Lane L5, Round 2 — Published .desktop / start-menu entries wrapping remote-app launches (SQ6)

Date: 2026-10-25. Goal: upgrade round-1's "assembled-only" Exec recipes to documented third-party practice,
or document absence. Scope: (a) ssh -X, (b) waypipe, (c) xpra seamless, (d) x2goclient.

Legend: **Verified** = published, attributable, with author's working statement or official doc.
**Plausible** = published but not independently confirmed working / mechanism mismatch. **Speculative** = inferred.

---

## Transport (a): ssh -X/-Y app

### A1. KDE desktop-entry wrapping `ssh -X` app — full working example (the key find)
- Claim: On openSUSE Leap 15.6 with KDE Plasma, a per-app start-menu/desktop entry created via KDE's
  "Create Application Link" dialog launches a remote X11 app through ssh, including key-passphrase entry
  via ksshaskpass popup — no terminal.
- Source: https://unix.stackexchange.com/questions/805954/how-to-start-a-remote-x11-application-via-ssh-with-one-click-on-an-icon — community Q&A; answer by Andrei Borzenkov (5.5k rep, openSUSE factory maintainer), answered May 15 2026, edited May 15 2026. Questioner runs "an OpenSuSE 15.6 workstation with KDE Plasma and an Ubuntu-24-based server", wants an icon for `ssh -l jacek -p 2204 -CX ClusterBox digikam`.
- Verbatim answer text: "Just add a desktop file. Something like [screenshots]" and
  "And clicking on the `Start xterm in the host` _in my case_ opens up `ksshaskpass` window and starts the application." and
  "`ssh` will invoke `ssh-askpass` when it is not run from the terminal (as in this case). You need to make sure you have _some_`ssh-askpass` implementation like `ksshaskpass` and that this implementation is also setup as the `ssh-askpass` (e.g. using update alternatives). You can also set the environment variable `SSH_ASKPASS=/usr/bin/ksshaskpass` to explicitly use it. On the openSUSE Leap 15.6 the `/usr/lib/ssh/ssh-askpass` is a shell script that will invoke either `ksshaskpass` or `gnome-ssh-askpass` depending on the desktop environment."
  And: "My answer describes exactly the 'ask for the passphrase, make up the tunnel for X11, and start digikam on the server.'. It takles less than 1 minute to create this application icon and test it." [sic]
- Verbatim entry content (read from the answer's KDE "Properties … .desktop" screenshot, image i.sstatic.net/v8WA3u8o.png, inspected 2026-10-25): Name = `Start xterm on the host`; Program = `/usr/bin/ssh`; Arguments = `-nTX 10.0.2.2 xterm`; Generic name/Comment/Environment variables/Work path empty → effective `Exec=/usr/bin/ssh -nTX 10.0.2.2 xterm`.
- Documented gotchas: (i) ssh-askpass must exist and be registered (update-alternatives) or SSH_ASKPASS set, else no passphrase prompt appears when launched from menu; (ii) flag discussion in comments: questioner "Rather `-fT`? The manpage says that `-n` is unsuitable when `ssh` asks for a passphrase" — in the accepted pattern `-n` is fine precisely because askpass, not the tty, is used; (iii) ssh only invokes askpass when NOT run from a terminal (which the .desktop launcher guarantees).
- Tier: **Verified** (author's own working demonstration with screenshots; scenario matches our client-KDE/server-Ubuntu case almost exactly).

### A2. Terminal-wrapper variant (not seamless, GNOME-flavored)
- Claim: published .desktop entry launching an interactive ssh -X session inside gnome-terminal.
- Source: https://askubuntu.com/questions/548860/desktop-launcher-for-ssh-terminal (answer, verbatim from index snippet; page itself blocked our scraper):
  `[Desktop Entry] Name=system1_ssh_terminal Comment=launch ssh session Exec=gnome-terminal -e 'ssh -X user@ip_of_system1' Icon=utilities-terminal Terminal=true Type=Application Categories=Application;`
- Relevance: proves the .desktop-wraps-ssh pattern is community-standard, but launches a terminal, not a single remote window.
- Tier: **Verified** as published content; **partial** fit to our seamless goal.

### A3. r/kde users keep .desktop files for ssh launches
- Claim: "I have some launchers (.desktop files) to open ssh sessions to my servers, I would like to associate each konsole to his own launcher" — existence of the practice among KDE users (ssh terminal sessions, not GUI apps).
- Source: https://www.reddit.com/r/kde/comments/fa012e/start_ssh_desktop_launcher_in_own_konsole/ (Reddit body unreachable anonymously; quote from search index snippet).
- Tier: **Plausible** (snippet only).

---

## Transport (b): waypipe ssh host app

No blog/forums post shows a hand-written .desktop file for waypipe, BUT two third-party tools publish the
mechanism explicitly.

### B1. waypipe-desktop: generates real per-app .desktop entries for remote Wayland apps
- Claim: a Python/Nix tool that gives one shared waypipe session per remote host (systemd user service) and
  "Run Wayland applications from another host and have them appear on this one, as **ordinary entries in your app grid**."
  Its documented contract (quoted): "one desktop entry per app, `Exec=waypipe-desktop run <app>`; a `config.toml`
  holding the same apps"; `waypipe-desktop generate` "Write[s] the systemd user services and desktop entries" and
  "owns the files it writes (`waypipe-session-*.service` and `waypipe-*.desktop`)".
  Config sample (verbatim): `[apps.firefox-remote] title = "Firefox (Remote)"  # shown in the app grid; host = "workstation-waypipe"; command = ["firefox", "--profile", "/home/me/Personal"]; icon = "/usr/share/icons/firefox.png"; categories = ["Network", "WebBrowser"]; audio = true; audio-latency = 400; environment = { GDK_BACKEND = "wayland" }`.
  Per-app launch is plain ssh: `ssh <host> env WAYLAND_DISPLAY=<display> DBUS_SESSION_BUS_ADDRESS=... PULSE_SERVER=... firefox`.
- Source: https://github.com/BeatLink/WaypipeDesktop (GPL-3.0, 8 commits, 0 stars — single-author, no independent user reports).
- Documented gotchas (verbatim from README Troubleshooting):
  - "The session fails immediately." → "The usual causes are a waypipe version mismatch, `waypipe` or `dbus-daemon` not being on the remote non-login `PATH` (check with `ssh <host> command -v waypipe dbus-daemon`), or key auth not working under `BatchMode`." (= silent-death failure modes + key-auth requirement for a terminal-less launcher.)
  - "An app starts but no window appears. It probably picked X11. Set `GDK_BACKEND=wayland`, `QT_QPA_PLATFORM=wayland`, or for Electron `NIXOS_OZONE_WL=1`, in the app's `environment`." (= the window-not-appearing gotcha.)
  - "A second launch does nothing. That is usually the point — the app is already running on the shared session and raised its existing window." (= single-instance handling.)
  - "Portal dialogs appear on the remote machine's screen. Its `XDG_DATA_DIRS` is resolving to that host's own session." (= portal file-picker gotcha from round 1.)
  - "sshd does not kill the remote command when a link drops, so without this a restart would orphan the old bus and strand every app attached to it." (reaping needed.)
- Tier: **Verified** as an author-documented, self-consistent recipe (README + shipped generator code); **Plausible** as community practice (no third-party adoption evidence).

### B2. remote-app-launcher (PyPI): menu entries via remote .desktop files + gtk-launch over waypipe
- Claim: third-party tool that "Browse[s] and launch[es] desktop applications installed on a remote Linux HTPC"; "Launches the selected app on the remote host with `waypipe ssh -t host gtk-launch <desktop-id>`, displaying the window locally"; discovers apps by reading `.desktop` files in `/usr/share/applications` and `~/.local/share/applications`.
- Source: https://pypi.org/project/remote-app-launcher/ (v0.1.0, released May 1, 2026, MIT, author zany130; repo github.com/zany130/remote-app-launcher; Development Status 3 - Alpha).
- Documented gotchas (verbatim from PyPI README): ssh config needs `SetEnv XDG_RUNTIME_DIR=/run/user/1000` plus `AcceptEnv XDG_RUNTIME_DIR` in remote sshd_config; "The waypipe process keeps the session open for 24 hours. To stop it early: `pkill -f "waypipe ssh.*gtk-launch"`"; "Install GTK/GLib on the remote host" (gtk-launch not found); remote "must run a Wayland compositor".
- Relevance: documented, working reuse of .desktop entries as the remote-app launch vocabulary, driven from the client over waypipe.
- Tier: **Verified** as author-documented practice; **Plausible** as general adoption (alpha, solo maintainer).

### B3. Official vendor docs: per-app waypipe launching, no .desktop recipe
- Red Hat documents waypipe as the supported per-app remote launch mechanism ("From RHEL 10 clients, you can remotely launch applications that support the Wayland display protocol by using the waypipe proxy" — https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/administering_rhel_by_using_the_gnome_desktop_environment/remotely-accessing-a-graphical-application ; RHEL 9 equivalent chapter 14 at .../remotely-accessing-an-individual-application-wayland...). Both are CLI-only recipes; no start-menu entry documented (page scrape blocked; quotes from index snippets).
- Tier: **Verified** (official docs) for the launcher command; **absence** of .desktop integration in official docs — **Plausible** (quote from snippet only).
- Context: CachyOS forum tutorial (mihalycsaba, ~Apr 2026, https://discuss.cachyos.org/t/waypipe-display-remote-wayland-apps-locally-x11-forwarding-for-wayland/27491) documents day-to-day waypipe use on our exact client distro with screenshots ("resources app from my **local** laptop and **remote** desktop pc on the same screen", `waypipe --xwls ... steam` + `xwayland-satellite`), but contains no .desktop/menu entry. Tier: **Verified** usage, no menu integration.

---

## Transport (c): xpra seamless --start-child / attach

### C1. Shipped .desktop for attach (upstream packaging, third-party-quoted)
- Claim: xpra ships a desktop entry that turns `xpra://` URIs into client attaches — the only real-world .desktop file found in the xpra ecosystem.
- Source: https://www.synacktiv.com/en/advisories/multiple-vulnerabilities-in-the-xpra-client (Synacktiv security advisory, quoting the packaged file), verbatim: "`/share/applications/xpra.desktop` Exec=xpra attach %u MimeType=x-scheme-handler/xpra;x-scheme-handler/xpras;x-scheme-handler/xpra+tcp; x-scheme-handler/xpra+ssh;x-scheme-handler/xpra+ws;x-scheme-handler/xpra+wss;".
- Note: could not confirm the source path inside the upstream repo (raw.githubusercontent Xpra-org/xpra master xpra.desktop and data/xpra.desktop both 404 — the file is build-generated), so the advisory quote is the evidence.
- Tier: **Verified** (third-party quote of shipped artifact).

### C2. Official command suitable for an Exec= line; no published wrapper found
- xpra official docs (docs/Usage/Seamless.md, README.md; verified round 1) publish the one-step form
  `xpra seamless ssh://USER@HOST/ --start-child=xterm` and reconnect `xpra attach ssh://HOST/SESSION`.
  Usage/README steers GUI users to "Open Xpra from your desktop's application menu" (xpra's own GTK frontend), not to per-app entries.
- Tier: **Verified** (official) for commands; **Plausible** that wrapping in `~/.local/share/applications/*.desktop` works (same mechanism as A1; no published example).

### C3. Backgrounding / foreground pitfall (maintainer-documented)
- Source: https://github.com/orgs/Xpra-org/discussions/4452 (nbecker + maintainer totaam/Antoine Martin, Jan 2025).
- Verbatim: user: "it's convenient to start the xpra session from the client side: `xpra desktop ***@**.***/100 --start-child=xfce4-session \ --exit-with-children --resize-display=1920x1100` But this leaves the client shell with xpra in the foreground. If I detach using the xpra menu it works fine. Maybe not so clean if I forget to detach, close my laptop and go home."
- Maintainer (totaam): "I would just run a single command directly from the client: `xpra desktop ssh://user@host/100 --start-child=xfce4-session --exit-with-children` So logging out from xfce would also end the session."; "`--daemon=yes` is the default"; "This syntax [`xpra attach ssh:nbecker8:100`] is ambiguous and has been deprecated ... Instead use: `xpra attach ssh://user@host:sshport/DISPLAY`."
- Relevance for .desktop Exec: a launcher Exec must survive xpra staying in foreground (detach/daemon behavior, or Exec wrapping with a backgrounding script) — the documented hazard when embedding these commands in launchers.
- Tier: **Verified** (maintainer statements).

### C4. Institutional GUI usage
- University of Cambridge computing guide ("Connecting to a linux workstation by Xpra", https://computing.ch.cam.ac.uk/connecting-linux-workstation-xpra): documents adding the xpra client to the Applications menu and using its launcher pop-up — i.e., orgs integrate *xpra itself* into the menu, then pick sessions in its GUI; no per-app Exec recipe.
- Tier: **Verified** (institutional doc) for that pattern.

**Gap:** no published third-party example of a hand-written per-app `.desktop` with `Exec=xpra seamless ssh://… --start-child=APP` or `Exec=xpra attach ssh://…` was found anywhere. Minimal assembled recipe with every component individually sourced: `Exec=xpra seamless ssh://USER@HOST/ --start-child=APP` (C2, official docs) + launcher mechanism = XDG ~/.local/share/applications (round 1, spec-verified) + foreground caveat handled per C3.

---

## Transport (d): x2goclient --session --autostart

### D1. X2Go's official per-app start-menu answer: server-side published applications
- Claim: X2Go natively publishes a per-app menu to the client from .desktop files on the *server*.
- Source: official X2Go wiki https://wiki.x2go.org/doku.php/wiki:advanced:published-applications, verbatim (index snippet): "On the X2Go Server you can control the applications displayed on the Published applications menu by adding, removing or controlling access to the files in /etc/x2go/applications/."
- Corroboration: ArchWiki X2Go (https://wiki.archlinux.org/title/X2Go): "X2Go can publish the installed applications in a menu to the client. This is controlled by the files in /etc/x2go/applications/. This location however is not created by default and can be created by creating a symlink to /usr/share/applications/." Bug #43 (bugs.x2go.org) shows the client menu is literally generated from server .desktop files by x2gogetapps (parses `[Desktop Entry]` sections).
- Tier: **Verified** (official docs + upstream bug tracker).

### D2. Client's own menu integration + in-client session buttons
- Official: https://wiki.x2go.org/doku.php/doc:usage:x2goclient: "After the installation of x2goclient an application link can be found in the menu of your Desktop Environment. On GNU/Linux systems it will be integrated into the Internet menu section." ArchWiki: "You can now create several sessions, which then appear on the right side and can be selected by a mouse click." → per-app convenience inside the client window, not the DE menu.
- Tier: **Verified** (official docs).

### D3. Institutional one-line x2goclient desktop shortcut (closest to a launcher example)
- University at Buffalo SENS guide (https://www.buffalo.edu/sens/documentation/software-guides/x2go.html): "On the desktop, right-click and select **New → Shortcut**. Paste the following into the location box (it should be one line): `"C:\Program Files (x86)\x2goclient\x2goclient.exe" --broker-url=ssh://lts-broker.sens.buffalo.edu/usr/bin/x2gobroker-ssh`" and for Linux: "`$ x2goclient --broker-url=ssh://lts-broker.sens.buffalo.edu/usr/bin/x2gobroker-ssh`". Also documents the Wayland crash workaround `QT_QPA_PLATFORM=xcb /usr/bin/x2goclient` (matches round-1 ArchWiki fact).
- Tier: **Verified** as institutional practice for command-line-launched x2goclient shortcuts; **Plausible** transposition to Linux .desktop (the shortcut mechanism shown is Windows; Linux users are told to use a terminal).

### D4. CLI flags (round-1 fact, restated)
- `x2goclient(1)`: "--autostart=<app> Launch <app> by session start in "published applications" mode." (manpages.ubuntu.com resolute/jammy; --session/--session-name/--hide/--close-disconnect/--autologin verified round 1).

**Gap (documented absence):** no published third-party `.desktop` file with e.g.
`Exec=x2goclient --session=NAME --autostart=app --hide --close-disconnect --autologin` was found.
Queries tried (web_search, 2026-10-25): `"x2goclient" ".desktop" --session autostart menu entry KDE`;
`"x2goclient" "--autostart=" "--session=" desktop file icon launch application directly`;
`x2goclient command line start session directly desktop icon shortcut autostart published application`;
`askubuntu superuser launch x2goclient session from command line desktop shortcut single application`;
`"x2goclient" "Exec=" ".desktop" published applications shortcut`;
`x2goclient "--autostart" tutorial icon launch single application KDE plasma desktop entry`;
`reddit x2goclient create desktop entry icon per application session`;
`wiki.x2go.org user forum launch single application from client icon shortcut autostart desktop file`.
All returned man pages, official usage docs, GUI-profile guides, or the broker-shortcut guide above. The X2Go TCE docs (wiki.x2go.org doc:howto:tce) handle autostart via thin-client boot parameters, not client .desktop entries. Minimal assembled recipe keeps every component individually sourced: session profile created once in x2goclient GUI (D2) + `--session/--autostart/--hide/--close-disconnect/--autologin` (man page, round 1) + Wayland crash workaround `env QT_QPA_PLATFORM=xcb` (ArchWiki, round 1; corroborated by Buffalo FAQ) + XDG ~/.local/share/applications launcher mechanism (round 1, spec-verified).

---

## KDE Plasma "remote app entry" feature — absence documented
- Searched: `KDE Plasma feature launch remote applications through ssh menu integration kioslave remote app entries`;
  `discuss.kde.org launcher desktop entry ssh remote application start menu`; plus round-1 coverage.
- Result: no Plasma feature injects remote-app menu entries. Only findings: KIO slaves = remote *filesystems*
  (kde.org 4.4 announcement: "The KIOslaves provide KDE applications with access to local and remote file systems" — nothing about launching remote apps); Plasma's remote features are server-side RDP/VNC (krfb/krdp, Plasma 6.1 "Remote Access"); Konsole's SSH plugin just propagates SSH config to new tabs (TechRepublic).
- The community practice is exactly what A1 shows: hand-written .desktop files in ~/.local/share/applications wrapping the transport command (also r/kde fa012e, A3).
- Adjacent, session-level (not per-app) alternative found: unix.stackexchange.com/questions/527015 registers an
  `[Desktop Entry] Type=XSession Exec=/usr/bin/startssh ... DesktopNames=Remote ssh` in /usr/share/xsessions to make "ssh" a login-session choice at SDDM. Tier **Verified** as published; out of scope for per-app icons.
- Tier for absence claim: **Verified** (multiple targeted searches, only tangential hits).

---

## Searched, found nothing (negative results)
1. No blog/forums Q&A with a hand-written `Exec=waypipe ssh …` .desktop file (found instead: B1/B2 tool-generate them).
   Queries: `waypipe .desktop file menu entry launcher remote app example`; `"Exec=waypipe" OR "waypipe ssh" "Desktop Entry"`; `waypipe gitlab issue "desktop entry" OR "desktop file" launch menu integration`.
2. No third-party `Exec=xpra …` per-app launcher (only upstream `xpra.desktop` attach handler + xpra's own GUI menu).
   Queries: `xpra attach ssh desktop launcher icon "desktop file" seamless window`; `xpra start-child .desktop file menu entry launcher attach example`; `xpra github issue "desktop entry" start-child OR "desktop file" server applications menu`; `site:github.com Xpra-org xpra discussion desktop entry menu shortcut launch`.
3. No `Exec=x2goclient …` .desktop anywhere public (see D4 query list).
4. Code-search fallbacks failed: grep.app behind Vercel checkpoint; GitHub code search needs auth; askubuntu 1380802 & Reddit JSON blocked scrapers (noted per-item above).
5. No KDE/Plasma remote-app menu feature exists (see section above).

Sub-question status from this lane's view: partial
