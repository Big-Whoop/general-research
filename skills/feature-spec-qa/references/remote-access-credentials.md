# Remote-access credential delivery: what clients actually honour

Use when a feature promises "connect without a password prompt" for RDP/SSH to
throwaway machines. Check the client the user runs before promising a format.

## RDP `.rdp` files
- `password 51:b:<hex>` is DPAPI-encrypted and bound to the Windows user +
  machine that created it. A server (Linux, Java, anything) cannot produce a
  blob mstsc will accept. Plaintext `password:s:` is IGNORED by mstsc: it
  prompts once. So on a Windows laptop the floor is one prompt; pre-fill
  `full address:s:host:port`, `username:s:<user>`, `prompt for credentials:i:0`.
- FreeRDP-based clients (xfreerdp, Thincast, Remmina's RDP plugin when
  importing) parse the same `.rdp` grammar and accept plaintext `password:s:`
  — verify per client once in a manual step; offer two downloads
  (with/without password) rather than a checkbox when the user uses both
  client families.
- `.remmina` profiles carry a 3DES-encrypted password keyed by the user's
  `remmina.pref` secret — only viable if the server knows that secret.
- Serve files with `Cache-Control: no-store`, `application/x-rdp`,
  `Content-Disposition: attachment`; never log the body.

## SSH
- No file format carries a password into OpenSSH. Offer the copy-pasteable
  line `ssh -p <port> <user>@<host>` next to a masked password with a copy
  button; a web terminal (xterm.js over the service's own WebSocket) is the
  real "no prompt" path.

## Generated per-machine passwords (cloud-init / sysprep)
- Linux: cloud-init `chpasswd: {expire: false, users: [{name, password, type: text}]}`
  + `ssh_pwauth: true`; leave `PermitRootLogin` alone, root via `sudo -i`.
- Windows: per-VM sysprep answer file (KubeVirt `sysprep` volume from a
  Secret: `unattend.xml` with `<AdministratorPassword>` + `customize.ps1`
  for `administrators_authorized_keys` with the documented icacls ACL). The
  golden image must be sealed WITHOUT `/unattend:` — a cached
  `Panther\Unattend.xml` beats the attached CD and the per-VM password is
  silently ignored.
- Password charset `[A-Za-z0-9]`, 20 chars, guarantee upper+lower+digit:
  satisfies Windows complexity and needs no quoting in YAML/XML.
