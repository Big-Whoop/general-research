# Server-Apps nahtlos auf dem Client-Desktop (CachyOS KDE ⇄ Ubuntu/Kubuntu) — Recherchebericht

Datum: 2026-10-25 · Methode: Deep-Research (2 Runden, 6 Lanes) · Corpus: `.hermes/research/2026-10-25-linux-seamless-remote-apps/`
Sprache: Bericht DE (Erstellungssprache der Anfrage); Lane-Dateien EN mit Voll-Zitaten (Detailschicht der Belege).

## Kurzantwort

**Ja — das geht, auf mehreren Wegen, aber es gibt keinen einzelnen „offiziellen" Mechanismus dafür.** Linux hat 2026 kein eingebautes Feature und kein gepflegtes Produkt, das „App auf dem Server starten, Fenster auf dem Client-Desktop + normales Startmenü-Icon" als Ganzes liefert (harte, positiv belegte Negativ-Aussage — siehe „Sackgassen"). Es existieren aber vier real gangbare Wege, die genau das erreichbare Ergebnis liefern: **X2Go Published Applications**, **waypipe**, **xpra** und als Schnellweg **SSH-X11-Forwarding**. Das Startmenü-Icon entsteht bei allen Wegen über eine `.desktop`-Datei in `~/.local/share/applications/` — ein verifiziertes funktionierendes Beispiel dafür existiert in den Quellen[10].

## Empfehlung (rangiert)

1. **X2Go „Published Applications"** — der einzige Weg mit *offiziell dokumentiertem* zentralem App-Menü vom Server auf den Client[17]. Beste Wahl, wenn du viele Server-Apps mit Menü, Drucken, Clipboard und solider WAN-Kompression willst. Caveats: alter nxagent-X-Server (GLX nur 1.2[20]) und ruhender Upstream.
2. **waypipe** — das „WSLg-Gefühl" im LAN: native Wayland-App-Forwarding über SSH, bei Praktikern als kaum von lokal unterscheidbar bewertet[4], aktiv gepflegt (v0.11.3, 2026-10-20)[5]. Caveats: Ubuntu 24.04 bringt nur waypipe 0.8.6[7] (für X11-Apps via `--xwls`[6] brauchst du ein aktuelleres Build), kein Drucken, Portal-Dateidialog-Falle[36].
3. **xpra** — der Funktionsbaukasten: echte Einzel-Fenster[11], bidirektionaler Ton[37], Drucken, persistent/reconnectbare Sessions, sehr aktiv (v6.5.5, 2026-10-12)[16]. Caveats: Ubuntu-*Server* offiziell nur Tier 3[12], Clipboard-Sync unter Wayland-Clienten offiziell „unmöglich"[13]. Das Archiv-Paket in 24.04 ist tot[15] → xpra.org-Apt-Repo benutzen.
4. **SSH X11-Forwarding (`ssh -X/-Y`)** — Null-Setup-Fallback (Server braucht nur `xauth`[3], Ubuntu schaltet `X11Forwarding` per Default an[1]), aber „chatty": Tipp-Latenz und Einfrieren, auf WAN schlecht[4].
5. **RDP RemoteApp über xrdp** — **funktionslos** Linux→Linux (verifizierte Negativa[22][24][25]); nur als „Voll-Desktop" brauchbar.

**Begründung der Rangfolge:** Deine Anforderung hat zwei Hälften — nahtlose Fenster *und* Startmenü-Icon. X2Go deckt beide offiziell ab (Server-Menü aus `.desktop`-Dateien[17], Client-Fenster integrieren lokal), läuft aus Ubuntu-24.04-Paketen[21] und hat NX-Kompression für gute WAN-Tauglichkeit. Der Preis: nxagent ist ein X.org-6.9-Fork ohne Xcomposite, GLX 1.2 — moderne Browser/GL-Apps brauchen dort Hacks[20]. Wenn deine Server-Apps GL-nah sind oder du die beste LAN-Response willst, ist **waypipe** überlegen (Punkt 2); wenn du Drucken/Ton/Session-Persistenz ohne X2Gos Alterslast willst, **xpra** (Punkt 3). Für den Einstieg: 10 Minuten mit `ssh -X` (Punkt 4) testen, dann gezielt aufbauen.

## Optionen-Matrix

| | X2Go Published Apps | waypipe | xpra | ssh -X | RDP/xrdp RemoteApp |
|---|---|---|---|---|---|
| **Mechanismus** | NX über SSH; je App ein „Clone"-Fenster auf dem Client[17][20] | Wayland-Client-Proxy; Remote-waypipe ist der Fake-Compositor der App[5][6] | „Screen for X": privater Xdummy-Server, Client zieht sich die Fenster[11][14] | sshd tunnel X11-Protokoll zu Client-X-Server[1][3] | RDP RAIL-Kanal — serverseitig unvollständig[22] |
| **Headless-Server** | ja (braucht `x2goserver-xsession` + WM-Binary)[20] | ja, ohne Compositor/GPU auf dem Server[6] | ja (eigener Xdummy/Xvfb)[14] | ja, nur `xauth`[3] | (Desktop-Sitzung nötig) |
| **Einzel-App-Fenster** | ja, offizieller Modus[17] | ja (Kernzweck)[5] | ja, offiziell[11] | ja | nein — verifiziert defekt[22][23] |
| **Ton** | ja, PulseAudio (`--sound`)[18]; PipeWire-Client unbestätigt ⚠ | nicht integriert; via `PULSE_SERVER`-Env/WaypipeDesktop[31] | ja, bidirektional (opus/vorbis/flac/mp3)[37] | nur Bastel-Rezept (Reverse-Tunnel 4713)[8] | (nur im Desktop-Modus offiziell) |
| **Clipboard** | bidirektional (`--clipboard=both`)[18] | folgt der Protokoll-Weiterleitung; Portal-Falle[36] | unter Wayland-Client eingeschränkt[12][13] | „gratis", da Client-X-Server (Community)[4] | n/a |
| **Drucken** | ja (cups-x2go)[18][21] | nein | ja (CUPS-Forwarding)[14] | nein | n/a |
| **3D/GL** | schwach: GLX 1.2[20] | dmabuf/Vulkan möglich aber „flakiest"; `--no-gpu` Fallback[5] | llvmpipe default; VirtualGL empfohlen[38] | indirektes GLX langsam; VirtualGL[9] | n/a |
| **Latenz-Eindruck** | gut (NX-Codecs, Link-Profile[18]) | „like local" im LAN (Praktiker)[4] | gut, für langsame Links gebaut[4] | spürbar, WAN schlecht[4] | n/a |
| **Startmenü-Icon** | Server-Menü offiziell[17] + eigene `.desktop` (Flags verifiziert[18][20]) | `.desktop`-Generator WaypipeDesktop[31] oder eigene Exec | eigene `.desktop` um offizielle Exec-Form[11] | verifiziertes `.desktop`-Beispiel[10] | — |
| **Pakete 24.04-Server** | `x2goserver` 4.1.0.6 in universe[21] | `waypipe` 0.8.6 — veraltet[7] | Archiv 3.1.5 tot[15] → Apt-Repo[14] | out of the box[1] | xrdp aktiv[22] aber RAIL frozen |
| **Upstream-Status (Probedatum 2026-10-25)** | „alive but dormant" (Releases 2023; Distro-Pflege)[18][21] | sehr aktiv[5] | sehr aktiv[16] | (OpenSSH — aktiv) | xrdp aktiv, RAIL-Anteil frozen[22][23] |

## Die Wege im Detail

### 1. X2Go „Published Applications" (empfohlen für App-Flotte + Menü)

**Mechanismus:** Der Server verwaltet ein App-Menü aus `.desktop`-Dateien in `/etc/x2go/applications/` (per Default Symlink auf `/usr/share/applications`); Zugriffssteuerung über Dateirechte[17]. Gestartete Apps öffnen je Fenster einen „Clone" auf dem Client und „integrieren sich in your local desktop environment like it was locally installed"[17]; NX komprimiert über SSH mit konfigurierbaren Codecs/Link-Profilen[18]. Server braucht `x2goserver` + `x2goserver-xsession` plus ein WM/DE-Binary, aber keinen angemeldeten Desktop[20][21]. Client auf Plasma 6/Wayland: x2goclient (Qt5) stürzt unter Wayland ab (Bug #1414[19]) — dokumentierter Workaround `env QT_QPA_PLATFORM=xcb` (ArchWiki[20], institutional bestätigt).

**Vertrauen:** Modus, Menü-Definition, Flags, Pakete, Crash+Workaround: **Verified** (offizielle Wiki/Manpages/Tracker). Ton unter PipeWire-Client: **Speculative** (kein offizielles Statement; einziger Datenpunkt ein Debian-Bug 2022 — Lane3 #13). WAN-Vorteil ggü. ssh -X: **Plausible** (Mechanismus belegt, kein Benchmark).

**Startmenü:** Das Server-Menü ist eingebaut[17]; für eigene KDE-Icons pro App die (aus verifizierten Einzelteilen zusammengesetzte, **Plausible**) Exec: `env QT_QPA_PLATFORM=xcb x2goclient --session=pubsrv --autostart=<app> --hide --close-disconnect` mit einmalig in der GUI angelegtem „Published Applications"-Profil `pubsrv` (Schlüssel-Auth via `--autologin`/ssh-agent[18]).

### 2. waypipe (empfohlen für moderne Apps / beste LAN-Response)

**Mechanismus:** `waypipe ssh user@server app` startet waypipe auf beiden Seiten; die Remote-Instanz „acts like a Wayland compositor"[6], teilt shm-Buffer mit dem echten Compositor des Clients[5]. Der Server braucht **keinen** Compositor und keine GPU-Sitzung, nur waypipe + OpenSSH ≥ 6.7 (Unix-Socket-Forwarding)[6]. X11-Apps laufen über `--xwls` + `xwayland-satellite`[6]; GPU/dmabuf wird unterstützt, ist aber der anfälligste Bereich — offizieller Fallback `--no-gpu`, optional verlustbehaftetes `--video`[5]; Kompression `lz4`/`zstd` + `waypipe bench`[6]. Sehr aktiv gepflegt: v0.11.3 vom 2026-10-20[5] (Probe 2026-10-25).

**Praktiker-Urteil:** Auf KDE-6-Wayland-Client „really 'feels' like it's running locally … nearly no latency when typing", schneller als xpra[4] (**Plausible**, ein Praktiker, architekturkonsistent).

**Fallen:** Single-Instance-Apps (firefox, kate…) reden die Server-Instanz an statt ein Fenster zu öffnen[6] (**Verified**); Portal-Dateidialoge (KDE-Dateipicker) erscheinen auf dem *Server* — GTK-Picker funktioniert[36] (**Plausible**, konkreter Workaround dokumentiert); Ubuntu 24.04 liefert nur 0.8.6[7] — für `--xwls` aktuelleres Build nötig (**Verified** versionsstand / **Plausible** Notwendigkeit).

**Startmenü:** Entweder eigene `.desktop` mit `Exec=waypipe ssh user@server app` (Exec-Form offiziell dokumentiert[5], Wrapper selbst **Plausible**), oder das Tool **WaypipeDesktop**, das pro App `Exec=waypipe-desktop run <app>`-Einträge samt systemd-User-Service generiert und Ton über `PULSE_SERVER`-Env durchreicht[31] (Author-dokumentiert **Verified**, Einzel-Autor ohne unabhängige Nutzer — **Plausible**).

### 3. xpra (Funktionsbaukasten: Ton/Drucken/Persistenz)

**Mechanismus:** Seamless-Modus = „Each remote application gets its own window on your desktop … managed by your local operating system and window manager"[11] (**Verified**, offizielle Doku). One-Step: `xpra seamless ssh://USER@HOST/ --start-child=firefox`, Wiederverbindung per `xpra attach ssh://HOST/NAME`[11]. Serverseitig privater Xdummy-X-Server, headless-tauglich[14][35]. Ton bidirektional[37], Drucken via CUPS[14], OpenGL standardmäßig llvmpipe, VirtualGL offiziell empfohlen[38] (alle **Verified**). Wayland-*Backend* auf dem Server experimentell — „Use the X11 backend unless you need Wayland specifically"[11]; Wayland-native Apps sind heute nicht forwardbar.

**Kritische Caveats:** Plattform-Tiers: Debian/Ubuntu-*Server* = Tier 3[12]. Ubuntu 24.04-Archiv xpra 3.1.5 „Unsupported upstream since August 2023; known to be broken"[15] → offizielles Apt-Repo benutzen[14]. „Wayland clients are inherently limited"[12] und Clipboard „impossible to synchronize it properly"[13] → unter Plasma 6 den xpra-Client gezielt über XWayland laufen lassen (z. B. `GDK_BACKEND=x11`) — auf deinem Ziel **ungetestet** (Praxisbeleg: Praktiker nutzt xpra seit Jahren auf Arch+Ubuntu[4], aber mit Snapping-/Keyboard-Quirks).

**Startmenü:** xpra bringt nur sein eigenes Launcher-Entry + `.xpra`-Sessiondateien[11]; keine dokumentierte .desktop-Generierung für Remote-Apps (doku­mentierte Abwesenheit, Lane5). Rezept (**Plausible**, Bausteine Verified): `Exec=xpra seamless ssh://user@server/ --start-child=firefox` bzw. `Exec=xpra attach ssh://user@server/meineSession` in `~/.local/share/applications/`; SSH-Schlüssel, ggf. `--ssh=ssh`[35]; Backgrounding-Hazard dokumentiert (Foreground nach Detach; Maintainer-Auskunft Lane2/Lane5 C3).

### 4. SSH X11-Forwarding (Schnellweg/Fallback)

**Mechanismus & Prereqs:** sshd allokieren einen Proxy-Display-Tunnel[1]; Ubuntu/Debian liefern `X11Forwarding yes` vor[1]; auf dem (auch headless) Server genügt `xauth`[3] — alles **Verified**. `-X` = untrusted (SECURITY-Extension, 20-min-Idle-Timeout), `-Y` = trusted für Apps, die sonst falsch zeichnen[2] (**Verified**). Clipboard funktioniert „gratis", weil die App den *Client-*-X-Server bedient (Community-Konsens[4]; kein offizielles Dokument — **Plausible**). Ton nicht integriert: Reverse-Tunnel-Rezept `pactl load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1` + `ssh -R 4713:localhost:4713` + `PULSE_SERVER=tcp:127.0.0.1:4713`[8] (PipeWire bedient dasselbe Protokoll). 3D nur mit VirtualGL (`vglconnect`/`vglrun`)[9]. Latenz: „not really the fastest … using ssh -X for a temporary solution is fine"[4].

**Startmenü — verifiziertes Beispiel:** unix.SE-Antwort (Mai 2026) auf KDE Plasma mit Ubuntu-Server: Desktop-Eintrag mit `Exec=/usr/bin/ssh -nTX <host> xterm`, Klick öffnet `ksshaskpass` und startet die App ohne Terminal[10] (**Verified**, inkl. Screenshot-Beleg). Bedingung: funktionierendes `ssh-askpass`-Alternativ-Setup bzw. `SSH_ASKPASS=/usr/bin/ksshaskpass`, oder passphraseloser Schlüssel + ssh-agent[10].

## Sackgassen (Verified-Negativa — Zeitersparnis)

- **RDP RemoteApp (xrdp als Server, FreeRDP/Remmina als Client), Linux→Linux:** xrdps RAIL ist selbst deklariert „incomplete", gebaut nur für Authentic8, „We haven't made any progress on this lately" (Maintainer, 2024)[22][23]; kein dokumentiertes Published-Apps-Allowlist-Konzept; Community-Praxis zeigt die App in schwarzem Vollbild-Kasten (Lane4 #5). Auf Client-Seite: `wlfreerdp` unterstützt kein RemoteApp[24], Remmina hat nie einen RemoteApp-Modus bekommen („help wanted" geschlossen)[25]; FreeRDP-Maintainer zu Linux-Server-RemoteApp: „currently no"[39]. Kein einziger dokumentierter End-to-End-Erfolg gefunden. **Nicht verfolgen.**
- **„WSLg für Linux":** Es gibt 2026 kein gepflegtes Produkt, das pro-App-RAIL Linux→Linux liefert (positiv gehärtete Negativausbilanz: GNOME Remote Desktop und KDEs krdp sind offiziell Voll-Sitzung-only[28][29]; der wlroots-RDP-Backend wurde upstream entfernt, der waylib-Fork ist verschwunden (Lane6 #10); wsland ist Windows/WSL-only[34]). Die WSLg-*Bausteine* leben und werden gepflegt — Microsoft behielt RAIL im libweston-RDP-Backend u. a. ausdrücklich für „remoting application from a Pi running Linux"[26], FreeRDPS Server-RAIL-Channel liegt im Tree, IronRDPs RAIL-Client wird 2026 aktiv entwickelt[30] — aber niemand integriert sie; der beste dokumentierte DIY-Versuch (MS-WSLg-Stack nativ auf Debian) erreichte nur Voll-Desktop: „It would be cool to get rail support in the freerdp client"[27].
- **KDE-eigene Funktion:** Plasma hat kein Feature zum Einblenden von Server-App-Menüs (KIO = nur Dateisysteme; krfb/krdp = Gegenrichtung) — dokumentierte Abwesenheit nach gezielten Suchen (Lane5).

## Startmenü: das übergreifende Muster

Mechanismus (**Verified**, KDE-Spezifikation[33]): `~/.local/share/applications/<name>.desktop` mit `[Desktop Entry]`, `Type=Application`, `Name=…`, `Icon=…`, `Terminal=false`, `Exec=<Transport-Befehl …>` — KDE-Menüs lesen dieses Verzeichnis automatisch. Für alle vier Wege gilt: SSH-**Schlüssel**-Auth ist Pflicht für „kein Terminal-Popup, kein Passwort-Prompt"; Fehler im Exec sterben sonst lautlos → zum Debuggen zunächst aus dem Terminal testen (Lane1 #22-24). Status je Transport: ssh -X **Verified-Beispiel**[10]; x2go Flags **Verified**, Assembly **Plausible**; xpra Exec-Form **Verified**, Wrapper **Plausible**; waypipe Exec **Verified**(Tool-generiert)[31][32] bzw. handgeschrieben **Plausible**.

## Was auf deinem Ziel (CachyOS KDE / Ubuntu 24.04) noch ungetestet ist

Explizit **nicht on-target verifiziert**, sondern Mechanismus/Community-Plausibilität:
1. x2go-Ton am PipeWire-Client (CachyOS) — kein offizielles Statement; ArchWiki rät bei Problemen Ton abzuschalten[20].
2. xpra-Clipboard-Qualität, wenn der xpra-Client unter Plasma 6 erzwungen über XWayland läuft[13].
3. waypipe-X11-Apps via `--xwls`+xwayland-satellite mit selbstgeбаутem waypipe ≥ 0.10 auf noble[6][7].
4. Die zusammengesetzten `.desktop`-Execs für x2go/xpra (alle Einzelteile belegt, die Kombi nirgends veröffentlicht — Lane5 „documented gaps").
5. quantitative Latenz-Vergleiche (Kein einziger publizierter Benchmark ssh -X vs xpra vs waypipe vs x2go; Rangfolge basiert auf Praxisberichten[4]).

## Methodik & Belegschichten

Zwei Fan-out-Runden (Runde 1: 4 Lanes; Runde 2: 2 Lanes auf die offenen Zeilen), Gap-Bewertungsmatrizen und Dispatch-Logs in `README.md`; jede Detail-Behauptung mit URL+Originalzitat+Tier in den Lane-Dateien (Vollbelege): `ssh-x11-waypipe/lane1.md`, `xpra/lane2.md`, `x2go/lane3.md`, `rdp-remoteapp/lane4.md`, `menu-integration/lane5-r2.md`, `wslg-diy/lane6-r2.md`. Liveness-Probes (GitHub-/GitLab-API) alle am 2026-10-25 ausgeführt. Tier-Legende: **Verified** = autoritative Quelle für exakt dieses Ziel; **Plausible** = sounder Mechanismus/Community, nicht on-target demonstriert; **Speculative** = inferiert.

## Sources

[1] https://man.openbsd.org/sshd_config — OpenBSD sshd_config(5)
[2] https://man.openbsd.org/ssh_config — OpenBSD ssh_config(5)
[3] https://wiki.archlinux.org/title/OpenSSH — ArchWiki OpenSSH X11 forwarding
[4] https://www.tauceti.blog/posts/ssh-x-vs-xpra-vs-waypipe-remote-display-comparison-single-window — TauCeti: ssh -X vs xpra vs waypipe
[5] https://gitlab.freedesktop.org/mstoeckl/waypipe — waypipe upstream README
[6] https://manpages.debian.org/unstable/waypipe/waypipe.1.en.html — waypipe(1) man page
[7] https://launchpad.net/ubuntu/noble/+package/waypipe — Launchpad noble waypipe 0.8.6
[8] https://wiki.archlinux.org/title/PulseAudio — ArchWiki PulseAudio network sharing
[9] https://www.virtualgl.org/vgldoc/2_1_3 — VirtualGL User's Guide
[10] https://unix.stackexchange.com/questions/805954/how-to-start-a-remote-x11-application-via-ssh-with-one-click-on-an-icon — unix.SE: one-click remote X11 app .desktop
[11] https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/Seamless.md — xpra Seamless.md
[12] https://github.com/Xpra-org/xpra/wiki/Platforms — xpra Platforms wiki
[13] https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Clipboard.md — xpra Clipboard.md
[14] https://xpra-org.github.io/xpra/Download/Linux.html — xpra Linux download docs
[15] https://github.com/Xpra-org/xpra/wiki/Distribution-Packages — xpra Distribution-Packages
[16] https://github.com/Xpra-org/xpra — xpra repo (liveness probe)
[17] https://wiki.x2go.org/doku.php/wiki:advanced:published-applications — X2Go Published Applications wiki
[18] https://manpages.debian.org/bookworm/x2goclient/x2goclient.1.en.html — x2goclient(1) man page
[19] https://bugs.x2go.org/cgi-bin/bugreport.cgi?bug=1414 — X2Go bug 1414 Wayland crash
[20] https://wiki.archlinux.org/title/X2Go — ArchWiki X2Go
[21] https://launchpad.net/ubuntu/noble/+source/x2goserver — Launchpad noble x2goserver
[22] https://github.com/neutrinolabs/xrdp/wiki/RAIL-support-in-xrdp — xrdp RAIL support wiki
[23] https://github.com/neutrinolabs/xrdp/discussions/3071 — xrdp discussion 3071 RemoteApp guidance
[24] https://github.com/FreeRDP/FreeRDP/wiki/RemoteApp — FreeRDP RemoteApp wiki
[25] https://gitlab.com/Remmina/Remmina/-/issues/2578 — Remmina issue 2578 RemoteApp
[26] https://github.com/microsoft/wslg — WSLG README (architecture)
[27] http://web.archive.org/web/20260519182604/https://blog.jacobstoner.com/wayweston-rdp — jacobstoner WSLg-DIY (Wayback)
[28] https://gitlab.gnome.org/GNOME/gnome-remote-desktop/-/raw/main/README.md — GNOME Remote Desktop README
[29] https://raw.githubusercontent.com/KDE/krdp/master/README.md — KDE krdp README
[30] https://github.com/Devolutions/IronRDP/pull/2200 — IronRDP RAIL client PR 2200
[31] https://github.com/BeatLink/WaypipeDesktop — WaypipeDesktop (per-app .desktop generator)
[32] https://pypi.org/project/remote-app-launcher — remote-app-launcher (waypipe gtk-launch)
[33] https://develop.kde.org/docs/features/desktop-file — KDE desktop-file docs
[34] https://github.com/qq1038765585/wsland — wsland (WSL-only wslg-like)
[35] https://wiki.archlinux.org/title/Xpra — ArchWiki Xpra
[36] https://discuss.kde.org/t/file-picker-dialog-opens-on-wrong-remote-screen-when-running-applications-via-waypipe/41160 — KDE discuss: waypipe portal file-picker on server
[37] https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Features/Audio.md — xpra Audio.md
[38] https://raw.githubusercontent.com/Xpra-org/xpra/master/docs/Usage/OpenGL.md — xpra OpenGL.md
[39] https://github.com/FreeRDP/FreeRDP/discussions/10586 — FreeRDP maintainer: Linux RemoteApp server 'currently no'
