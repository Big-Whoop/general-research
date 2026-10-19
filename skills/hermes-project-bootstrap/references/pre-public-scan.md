# Pre-Public-Push Secret Scan

Run from the repo root before `gh repo create ... --public ... --push`.

## Patterns

```bash
# keys / tokens
grep -rniE "(sk-[a-z0-9]{10,}|ghp_[a-z0-9]{20,}|gho_[a-z0-9]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|Bearer [a-z0-9]|api[_-]?key[\"']?\s*[:=]\s*[\"'][a-z0-9]|password[\"']?\s*[:=]\s*[\"'][^\"']{4,}|secret[\"']?\s*[:=]\s*[\"'][a-z0-9]{8,})" --include="*.md" --include="*.json" .
# IPv4 (filter standard placeholders)
grep -rnoE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" --include="*.md" --include="*.json" . | grep -vE "127\.0\.0\.1|0\.0\.0\.0|255\.255|192\.168\.0\.0|10\.0\.0\.0"
# internal / non-https URLs
grep -rhoE "http://[a-zA-Z0-9._-]+(:[0-9]+)?" --include="*.md" --include="*.json" . | sort -u
```

## Interpreting hits

- The case-insensitive `sk-[a-z0-9]{10,}` pattern matches words like
  "task-Completion", "Task-Klassifikation", "per-task-delegation" — read
  every hit before acting; never auto-scrub on pattern match.
- `http://localhost` and `http://your-server` placeholders are fine.
- Real secrets (API keys, tokens, internal IPs, internal host URLs) block
  the push — remove or redact, then re-scan.
- Internal model names / hostnames are not secrets: flag them in the report
  and let the user decide (research stays as-is per the language rule).
