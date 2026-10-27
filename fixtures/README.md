# fixtures/

Inert, harmless simulations of every threat in the threat model, owned by **WS-L**.

Safety rules (D-11):
- "Exfiltration" fixtures POST only to a sink inside the sandbox network (`http://egress-sink:9999`).
- "Malware download" fixtures fetch a harmless local marker file.
- "Secret theft" fixtures read only planted canary files (e.g. `/canary/.env`).
- No real secrets. No real third-party endpoints. Safe to run anywhere.

Each fixture directory contains:
- `README.md` — what it simulates
- the MCP source (Python or Node)
- `expected.yaml` — expected findings (categories, min severities) and expected verdict

Corpus plan (one row per threat-model item, plus benign controls and obfuscated variants):

| Fixture | Simulates | Expected verdict |
|---|---|---|
| `benign/echo` | Plain echo MCP | VERIFIED_SAFE / LOW_RISK |
| `benign/notes` | File-notes MCP, narrow scope | LOW_RISK |
| `secret-harvester` | Reads canary `.env`, `~/.ssh` paths | DANGEROUS (hard fail if exfil confirmed) |
| `exfil-unknown-host` | Sends data to sandbox sink | HIGH/DANGEROUS |
| `download-exec-dropper` | Downloads marker + execs it | DANGEROUS (hard fail) |
| `malicious-postinstall` | npm postinstall hook payload | HIGH/DANGEROUS |
| `typosquat-dep` | Depends on typosquatted package name | HIGH+ |
| `poisoned-tool-desc` | Injection in tool description | HIGH/DANGEROUS (hard fail if host-targeted) |
| `poisoned-tool-desc-unicode` | Zero-width/unicode-hidden injection | HIGH/DANGEROUS |
| `tool-shadowing` | Tool impersonating another server's tool | HIGH |
| `rug-pull` | v1 benign → v2 malicious | Drift detection, score drop |
| `over-privileged` | Shell+fs+net for a "calculator" | MODERATE/HIGH |
| `remote-drifting` | Remote MCP whose tool list changes | Drift finding |
| `obfuscated/*` | Obfuscated variants of the above | Same as plain variants |
