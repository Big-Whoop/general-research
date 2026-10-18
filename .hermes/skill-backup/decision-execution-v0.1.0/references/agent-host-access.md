# Agent access to a user-owned host (non-fleet, not config-managed)

Use when a plan needs recon and later setup on a machine the user administers
by hand (desktop, rolling-release box). The user runs every script himself;
the agent only verifies afterwards.

## Stage 1 — read-only whitelist (before any plan question needs facts)

Script `scripts/<host>-hermes-user.sh`, run as root, idempotent:
- user `hermes`, shell bash, password locked (key-only), group `kvm` if VMs
  are in scope;
- `authorized_keys`: the user's personal key FIRST, then the agent key (take
  both from the fleet's shared admin-user module, never retype);
- `/etc/sudoers.d/10-hermes-readonly`: `Cmnd_Alias` of absolute-path read
  commands only (`virt-host-validate`, `btrfs subvolume list/show`,
  `btrfs filesystem usage/df`, `lsblk`, `blkid`, `nvidia-smi`, `dmesg`,
  `journalctl -u *`, `systemctl status *`, `ss -tulpn`, `pacman -Q *`,
  `cat /proc/*`), `NOPASSWD`;
- `visudo -cf` on the drop-in; on failure `rm` it and exit 1 — a broken
  drop-in locks sudo for everyone;
- enable sshd if inactive; print the one-line verification ssh command.

Verify from the sandbox right after the user says "done":
`ssh -i ~/.ssh/<agent-key> -o IdentitiesOnly=yes hermes@<fqdn> 'id; sudo -n <one whitelisted cmd>'`
and fold the recon facts into the next plan question — this closes handoff
open items without a card.

## Stage 2 — setup rights (after plan sign-off)

The recon card's last item is "collect every sudo command Track B needs" —
the list goes into the research note, the plan's sudo section points at it.
The script `scripts/<host>-hermes-setup-sudoers.sh` writes
`/etc/sudoers.d/20-hermes-setup` from that list:
- one `Cmnd_Alias` per concern (k3s lifecycle, packages, modules/sysctl,
  btrfs top-level, project tree), every entry absolute-path and path-bound
  (`/usr/bin/btrfs subvolume delete /var/lib/<proj>/*`, not `btrfs *`);
- installers are never `curl | sudo sh`: the setup card downloads and
  checksum-pins the installer into a root-owned path, sudo allows only
  `/usr/bin/sh /var/lib/<proj>/setup/<installer>.sh *`; pass its
  `INSTALL_*` env via `Defaults:hermes env_keep`;
- `systemctl` verbs listed per unit, `tee` per exact file, `install -d`
  per directory; `chown` to the workload's uid (e.g. 107 for KubeVirt qemu)
  only under the project tree;
- same `visudo -cf` + self-remove guard; the read-only drop-in is untouched.

The sandbox has no `visudo`; the only validation is on the host. Keep the
script's sudoers text in a single heredoc so the user can read it in one
screen. Deliver from `/opt/data/downloads/` (the desktop preview refuses
repo paths). The rights STAY after setup — the user rejects
create-then-remove churn; say so in the script header.

After the user runs it: one non-persistent probe per alias class
(`sudo -n modprobe br_netfilter`, `sudo -n sysctl -w net.ipv4.ip_forward=1`)
and note that the persistent form is the setup card's job.