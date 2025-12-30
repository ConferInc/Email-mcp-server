# Gmail MCP Server

MCP server for Gmail integration with Claude, Cursor, Kiro, and other MCP clients.

## Tools
| Tool | Description |
|------|-------------|
| `list_emails` | List/search emails (returns id, snippet, subject, from, date) |
| `read_email` | Read full email content by ID |
| `send_email` | Send a real email ⚠️ |

## Prompts
| Prompt | Description |
|--------|-------------|
| `summarize_unread` | Summarize unread emails with priority |
| `draft_reply` | Draft reply to an email |
| `compose_email` | Compose new email |
| `search_emails` | Natural language email search |
| `daily_digest` | Daily email digest by category |

---

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable **Gmail API**
3. **APIs & Services** → **Credentials** → **Create OAuth Client ID** → **Desktop App**
4. Download JSON → rename to `credentials.json` → place in this folder

### 3. Authenticate (one-time)
```bash
python authenticate.py
```
This opens browser for Google login and creates `token.json`.

---

## Running the Server

### With Kiro
Add to `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["D:/path/to/gmail-mcp-server/server.py"]
    }
  }
}
```

### With Cursor
Open this folder in Cursor - `.cursor/mcp.json` is pre-configured.

### With Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["D:/path/to/gmail-mcp-server/server.py"]
    }
  }
}
```

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector python "D:/path/to/gmail-mcp-server/server.py"
```

---

## File Structure
```
gmail-mcp-server/
├── server.py          # MCP server (FastMCP)
├── gmail_client.py    # Gmail API wrapper
├── auth.py            # OAuth2 handling
├── authenticate.py    # One-time auth script
├── credentials.json   # Google OAuth creds (you provide)
├── token.json         # Auth token (auto-generated)
└── requirements.txt   # Dependencies
```

## Security
- Keep `credentials.json` and `token.json` private
- `send_email` sends real emails - use carefully
