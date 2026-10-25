# Lane L4 — RDP RemoteApp path (Linux server → Linux client): xrdp server-side RAIL + FreeRDP/Remmina client; SQ6 start-menu icon; SQ7 WSLg-equivalent status 2026

Research date: 2026-10-25 (GitHub/GitLab liveness probes run 2026-10-25T14:23Z).

## Findings

### Server side (xrdp)

1. **xrdp's RAIL (RemoteApp) support is officially "incomplete" and was built for one commercial use-case, not for general RemoteApp publishing.**
   - Source: https://github.com/neutrinolabs/xrdp/wiki/RAIL-support-in-xrdp (official wiki, last edited Aug 24 2020)
   - Quote: "Current RAIL support in xrdp was done for Authentic8. Authentic8 wanted the RAIL support to allow drawing the window borders locally. Microsoft RAIL draws the window borders on the server. ... This makes the general RAIL support in xrdp incomplete. We need to complete this to be MS client compatible."
   - Tier: **Verified**

2. **Maintainers confirm the code parses RemoteApp exec requests but the feature is not usable: "XRDP doesn't support RAIL ... but does have some code for RAIL connections that is incomplete."**
   - Source: https://github.com/neutrinolabs/xrdp/issues/1748 (official tracker; contributor aquesnel, the RAIL code author, Dec 2020)
   - Quote: "The remoteapplicationprogram is used for defining the application to start when using a RAIL RDP session. XRDP doesn't support RAIL as of version 0.9.14 but does have some code for RAIL connections that is incomplete."
   - Tier: **Verified**

3. **The effort is stalled: xrdp maintainer matt335672 (2022): RAIL won't move because the team is working on GFX/sesman; (2024): "We haven't made any progress on this lately."**
   - Source: https://github.com/neutrinolabs/xrdp/discussions/2238 and https://github.com/neutrinolabs/xrdp/discussions/3071 (official trackers, maintainer replies Apr 2022 / May 2024)
   - Quotes: "At the moment the team members are focussing on GFX support and improving sesman, so this isn't going to change for a while I'm afraid, unless we get more effort on the project." / "We haven't made any progress on this lately."
   - Tier: **Verified**

4. **Documented server config for RemoteApp is only a channel toggle `rail=true` in xrdp.ini [Channels]; there is NO documented "published applications" allow-list / secrets file of permitted binaries in xrdp** (the allow-list concept in the FreeRDP wiki refers to the Windows server side: "arguments ... it has to be allowed on the server explicitly"). No xrdp doc mentions a RDPGFX requirement for RAIL; RDPGFX/GFX was the separate unfinished work item cited in finding 3.
   - Source: https://manpages.opensuse.org/Tumbleweed/xrdp/xrdp.ini.5.en.html (official man page, xrdp 0.10.6.1); FreeRDP RemoteApp wiki (finding 6)
   - Quote: "rail=[true|false] — If set to 1, true or yes using the RDP channel for remote applications integrated locally (RAIL) is allowed."
   - Tier: **Verified** (absence of any allow-list doc: search-based negative)

5. **Practice: the community's only concrete "single app over xrdp" report shows the incomplete flattening — the app floats inside a full-resolution black desktop box; X2Go was recommended instead.**
   - Source: https://www.reddit.com/r/linux/comments/1092p3y/remoteapplike_functionality_with_xrdp/ (community, ~2023)
   - Quote: "I was able to get XRDP to share a single application, but it presented as a big black box the size of the remote session's resolution with the application floating in it. If I shrank the size of the RDP session's resolution, then I couldn't maximize the remote app beyond that. It was janky at best."
   - Tier: **Plausible**

6. **aquesnel/xrdp (the fork that carried the RAIL work) is stale — last push 2022-01-23, no rail branch among its branches (GitHub API, probed 2026-10-25).**
   - Source: https://api.github.com/repos/aquesnel/xrdp (probe)
   - Tier: **Verified** (probe output)

### Client side (FreeRDP / Remmina)

7. **FreeRDP client RemoteApp is officially documented and mature against MS-RDPERP (Windows) servers; usage: `xfreerdp /u:user /p:pass /app:"||calc" /v:server`, newer syntax `/app:program:'<path>'`; colon-in-path conflicts with the old `--data` separator.**
   - Source: https://github.com/FreeRDP/FreeRDP/wiki/RemoteApp (official wiki, edited Feb 19 2025)
   - Quote: "RemoteApp support was introduced in FreeRDP 1.0 ... You may also want to try newer syntax: xfreerdp /u:user /d:domain /p:password /app:\"||calc\" /v:server ... there is currently an issue where the usage of the colon ':' conflicts with the --data argument separator"
   - Community confirmation of the working modern syntax on a Wayland client: "Thank you, with /app:program:'%windir%\explorer.exe' it is finally working now." (https://forum.level1techs.com/t/seamless-rdp-with-remoteapp-tool-and-freerdp/215922, community, Aug 2024)
   - Tier: **Verified**

8. **No Wayland-native RemoteApp client: wlfreerdp does not support RemoteApp; official wiki says use xfreerdp (X11 → runs via XWayland on KDE Plasma 6 Wayland; KWin then gives normal window decorations/taskbar/alt-tab like any XWayland app).**
   - Source: https://github.com/FreeRDP/FreeRDP/wiki/RemoteApp (official wiki) + https://github.com/FreeRDP/FreeRDP/issues/6573
   - Quote: "It seems wlfreerdp doesn't support remoteapp. See Ticket 6573 ... So if you want to use remoteapp use xfreerdp."
   - XWayland window-integration consequence: inference from general KDE/XWayland behavior, not quoted from FreeRDP docs.
   - Tier: **Verified** (no Wayland RAIL) / **Plausible** (XWayland integration quality)

9. **wlfreerdp is deprecated in FreeRDP 3 in favor of the SDL client (sfreerdp); the RAIL-relevant recommendation remains the X11 client. (wlfreerdp3 also emits a deprecation warning per Level1Techs user report.)**
   - Source: https://www.phoronix.com/forums/forum/software/desktop-linux/1428051-... (community forum, FreeRDP devs quoted) + Level1Techs thread above
   - Quote: "Yes, they deprecated wlfreerdp in favor of the SDL client, but the latter is ..."
   - Tier: **Plausible**

10. **Client-side RAIL in 2026 is alive but brittle: xfreerdp3 lost RemoteApp windows in 3.23.0 (issue #12391, opened 2026-02-27), fixed by akallabeth in master via PR #12392 the same week (issue closed 2026-02-27, label fixed-waiting-test).**
    - Source: https://github.com/FreeRDP/FreeRDP/issues/12391 (official tracker; GitHub API probe 2026-10-25)
    - Quote: "After upgrading from FreeRDP 3.22.0 to 3.23.0, RemoteApp (RAIL) windows no longer appear on the X11 client (xfreerdp3) ... Downgrading to 3.22.0 immediately resolves the issue." / akallabeth: "with some more testing I think I have identified your issue. Please give PR #12392 a try."
    - Tier: **Verified**

11. **Remmina has NO RemoteApp/RAIL connection mode; the feature request was closed 'help wanted' (never implemented) because Remmina is a single-window-per-connection UI; community answer confirms.**
    - Source: https://gitlab.com/Remmina/Remmina/-/issues/2578 (official tracker; API probe: state=closed, labels ['FreeRDP','Plugins::RDP','help wanted'], last update 2022-06-08) + https://askubuntu.com/questions/148159/remmina-remoteapp-over-rdp (community)
    - Quotes: "It seems hard to implement such feature based on current framework, since Remmina currently uses a single window styled interface for each connection." / "As far to I know, Remmina doesn't allow for RemoteApp client access. You can however do it with xfreerdp." (sic: "As far as I know...")
    - Tier: **Verified**

12. **FreeRDP maintainers confirm the reverse direction (Linux server publishing apps to any RDP client, incl. mstsc) is "currently no" (Sep 2024) — i.e., no supported Linux-RemoteApp-server in the FreeRDP world either; desktop session with dynamic resizing is the offered fallback.**
    - Source: https://github.com/FreeRDP/FreeRDP/discussions/10586 (official tracker, maintainer akallabeth)
    - Quote: "currently no. (that is you want to run mstsc on windows and the remote app would be running on your linux server ...)"; "you can simply run a normal RDP desktop session with dynamic resizing enabled. Not as comfortable as direct per application windows but usable."
    - Tier: **Verified**

### Liveness probes (recorded 2026-10-25T14:23Z, via api.github.com)

13. **xrdp: active — pushed_at 2026-10-22T17:48:54Z, latest release v0.10.6.1 published 2026-07-07, 302 open issues. FreeRDP: very active — pushed_at 2026-10-23T17:58:30Z, latest release 3.32.2 published 2026-10-12. Weston: active — last commit 2026-10-23 (gitlab.freedesktop.org API).**
    - Source: https://api.github.com/repos/neutrinolabs/xrdp, /releases/latest; https://api.github.com/repos/FreeRDP/FreeRDP, /releases/latest; weston commits endpoint
    - Tier: **Verified** (probe output)

### xrdp session features (clipboard/audio) — relevant if RAIL ever works; these are desktop-session features

14. **xrdp officially supports two-way clipboard, audio redirection and drive redirection (via xrdp-chansrv) for normal sessions; whether these work inside its broken RAIL mode is undocumented.**
    - Source: https://www.xrdp.org/ (official site)
    - Quote: "xrdp supports not only graphics remoting but also two-way clipboard transfer (text, bitmap, file), audio redirection, drive redirection (mount local client drives on remote machine)"
    - Tier: **Verified** (desktop session) / **Speculative** (inside RAIL mode)

### SQ6 — KDE start-menu icon for this path

15. **A `.desktop` entry in `~/.local/share/applications` wrapping `xfreerdp3` gives a normal KDE start-menu icon; `Terminal` is an Application-type key whose absence means no terminal window is spawned (default false), so no terminal popup.**
    - Source: https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html (official spec)
    - Quote: "For example, the `Terminal` key can only be used when the value of the `Type` key is `Application`." (spec Table 2 defines Terminal as boolean, not required → default no terminal)
    - Example Exec line assembled from documented usage (xfreerdp /app syntax from FreeRDP wiki finding 7; works against Windows — UNTESTED against xrdp because of findings 1–5):
      `[Desktop Entry] Type=Application Name=Server App Comment=Remote app via RDP Exec=xfreerdp3 /u:myuser /v:srv.lan /cert:tofu /app:program:/usr/bin/firefox --async-channels`
    - Tier: **Verified** (mechanism) / **Plausible** (exact exec for Linux→Linux, untestable today)

16. **Credentials handling: putting /p: in the .desktop Exec is readable by anyone — better documented options: (a) xrdp presents its own login dialog at connect ("username=ask/password=ask" session sections, documented in xrdp.ini man page EXAMPLES), so no secret in the entry; (b) Remmina profiles store passwords via kwallet/gnome-keyring — but Remmina offers no RemoteApp mode (finding 11), only full-desktop profiles launchable from CLI: `remmina -c file.remmina` ("Connect directly either to a desktop using options described in a file").**
    - Source: https://manpages.opensuse.org/Tumbleweed/xrdp/xrdp.ini.5.en.html (official; EXAMPLES shows username=ask/password=ask, and {base64} password obfuscation is in the format), https://remmina.gitlab.io/remminadoc.gitlab.io/md__builds__remmina_remmina-ci__remmina_8wiki__usage__remmina-command-line-examples.html (official docs), https://www.mankier.com/1/remmina (man page)
    - Quote (Remmina docs): "If you want to be safe, use kwallet or gnome-keyring, in the password field use a . (dot) and search how to add secrets from the command line in kwallet or gnome-keyring"
    - Tier: **Verified** (each piece) / **Plausible** (as an integrated recipe)

17. **Historic wrapper precedent: WinConn (Ubuntu) "simplifies creation, management and desktop integration of remote windows applications ... uses RemoteApp technology, implemented by FreeRDP" — a GUI front-end producing menu entries around xfreerdp /app; old, Windows-server oriented.**
    - Source: https://askubuntu.com/questions/148159/remmina-remoteapp-over-rdp (community answer)
    - Tier: **Plausible** (existence; maintenance status of WinConn not verified)

### SQ7 — WSLg-equivalent for Linux→Linux in 2026

18. **WSLg architecture (docs, not code): headless Weston with libweston RDP backend (built on FreeRDP) + purpose-built 'RAIL-Shell'; RAIL support was deliberately kept in weston for non-Windows scenarios, explicitly including "remoting application from a Pi running Linux"; audio via PulseAudio RDP sink/source plugins; start-menu icons via custom DVC channel + WSLDVCPlugin on the mstsc (Windows) side.**
    - Source: https://github.com/microsoft/wslg README (official docs) and https://devblogs.microsoft.com/commandline/wslg-architecture/ (official blog)
    - Quote: "We've added support for both RAIL and VAIL to the libweston RDP backend, although for WSLg only the VAIL support is effectively used. We decided to keep that support in as it could reuse in other interesting scenarios outside of WSLg, for example for remoting application from a Pi running Linux." / "For WSLg we introduced a new shell called the RAIL Shell. The purpose of the RAIL Shell is to help with the remoting of individual windows from Linux to Windows"
    - Tier: **Verified**

19. **So the WSLg "engine" is Linux-side and maintained in-tree (weston backend-rdp still receives commits — last weston commit 2026-10-23), and a native-Linux RDP backend is officially documented: "The RDP backend allows to run a weston environment without the need of specific graphic hardware, or input devices." (weston-rdp(7) man page; also hardening-consulting overview, community).**
    - Source: https://manpages.ubuntu.com/manpages/focal/man7/weston-rdp.7.html (official man page), https://www.hardening-consulting.com/en/posts/20131006an-overview-of-the-rdp-backend-in-weston.html (community/vendor)
    - Tier: **Verified** (backend exists/maintained)

20. **But no maintained, packaged Linux→Linux 'WSLg-equivalent' project exists as of 2026: only DIY explorations — (a) Jacob Stoner's blog "Wayland RDP Server with audio using Microsoft's WSLg stack" (community experiment with the modified weston/pulse/freerdp stack on native Linux; article since moved offline from that URL), (b) microsoft/wslg discussion #177 "Weston RDP example" (native-Linux usage question in the official repo, showing it's user-explored, not a product), (c) qq1038765585/wsland — "use wlroots + freerdp server implement wslg like", explicitly experimental and still targeting WSL/Windows, not LAN Linux→Linux.**
    - Source: https://blog.jacobstoner.com/wayweston-rdp/ (search-index snippet: "I spent some time playing with the Microsoft's modified Weston/PulseAudio/FreeRDP stack. This is what Windows is using to display GUI Linux apps under WSL."), https://github.com/microsoft/wslg/discussions/177, https://github.com/qq1038765585/wsland
    - Tier: **Plausible** (negative existence claim rests on search coverage + no hits for any productized project; components verified separately)

### Known blockers that make RDP RemoteApp Linux→Linux impractical today (synthesis)

21. **Blockers, grounded in findings 1–5, 8, 10, 12:** xrdp's RAIL server is officially incomplete/stalled (windows not flattened → black-box desktop per finding 5; "not MS client compatible"), has no documented published-application allow-list (any exec gating would need patching); client RAIL is X11-only (XWayland on KDE Wayland) and periodically regresses even against Windows (finding 10); no client ever verified working end-to-end against xrdp was found. Practical alternatives flagged repeatedly in the same threads: X2Go published applications, NoMachine, or the weston-RDP-backend DIY stack.
    - Sources: as cited per finding; X2Go recommendation in https://serverfault.com/questions/674176/remoteapp-seamless-rdp-linux-server (community: "x2go also has a 'remoteapp' type capability ... wiki.x2go.org/doku.php/wiki:advanced:published-applications")
    - Tier: **Verified** (each blocker) / **Plausible** (overall verdict)

## Searched, found nothing
- **NeRDP** vendor/product pages (RemoteApp for Linux servers): two targeted searches returned no product page — could not verify existence/status; treated as defunct/unfindable.
- **WinFlexRM** vendor page: targeted search returned no product page (only mirrors/lists).
- **xrdp RemoteApp "secrets file of allowed binaries"**: no such documented mechanism exists in xrdp man pages/wiki (only the `rail=` channel toggle); the "allowed on the server explicitly" concept belongs to Windows' RemoteApp deployment, not xrdp.
- **No report of `xfreerdp3 /app:` successfully producing flattened windows against an xrdp server** (closest: Reddit black-box report, finding 5).
- No maintained Linux→Linux seamless-RDP product built on weston RDP backend found in 2026 searches (see finding 20).

Sub-question status from this lane's view: partial
