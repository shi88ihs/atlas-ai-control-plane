# Security Publication Checklist

Before committing any code or configuration to this public repository, verify that the following items are **NOT** included:

1. **IP Addresses:**
   - No public IPv4/IPv6 addresses that identify our servers.
   - No private/internal IP addresses (e.g., VPC networks, Docker bridge IPs) that map out our internal topology.
   - Use safe placeholders like `203.0.113.10` (Public) or `10.0.0.10` (Private).

2. **Hostnames and Domains:**
   - No real server hostnames or domain names.
   - Use safe placeholders like `atlas-server` or `atlas.example.com`.

3. **Cloud Infrastructure IDs:**
   - No AWS Account IDs.
   - No EC2 Instance IDs (`i-...`).
   - No VPC IDs, Subnet IDs, or Security Group IDs.
   - Replace with placeholders like `vpc-placeholder`, `i-placeholder`.

4. **Network and VPN Details:**
   - No Tailscale URLs, Tailnet names, or Tailscale IP addresses (`100.x.x.x`).

5. **Server Usernames and System Details:**
   - Avoid revealing specific SSH usernames unless they are generic (`atlas-admin`).
   - Remove kernel versions or exact OS versions.

6. **Credentials and Secrets:**
   - No `.env` files or API keys (OpenAI, AWS, Telegram, etc.).
   - No private keys (`.pem`, `.key`, `id_rsa`, etc.).
   - Ensure the `.gitignore` catches these.

7. **Other Identifiers:**
   - No Telegram bot tokens, user IDs, or chat IDs.
   - No live service ports if they map to the exact internal deployment logic.

**How to verify before pushing:**
Run the standard pre-push scan:
```bash
rg -n --hidden --glob '!.git' \
'([0-9]{1,3}\.){3}[0-9]{1,3}|i-[a-f0-9]{8,17}|vpc-[a-f0-9]+|subnet-[a-f0-9]+|sg-[a-f0-9]+|AKIA[0-9A-Z]{16}|BEGIN .*PRIVATE KEY|bot[0-9]+:[A-Za-z0-9_-]+|sk-[A-Za-z0-9_-]+'
```