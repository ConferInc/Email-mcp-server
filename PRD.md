# Product Requirements Document: FastMCP Custom Email Server

**Version:** 1.0.0
**Status:** Approved for Implementation
**Tech Stack:** Python (FastMCP, AsyncIO)

## 1. Product Overview

**Title:** Universal Custom Domain Email MCP Server
**Vision:** A high-performance, asynchronous MCP server enabling LLMs to interact with any standard SMTP/IMAP email provider (Zoho, Outlook, Gmail, Postfix) securely and efficiently.

**Key Differentiator:** Unlike basic scripts, this server uses **Async I/O** to prevent timeouts during large email fetches and utilizes **FastMCP** for rapid, type-safe tool deployment.

## 2. User Stories

* **As an AI Assistant:** I want to search a user's inbox for specific keywords so I can answer questions about recent orders or alerts.
* **As a User:** I want my AI to draft a reply and save it to my "Drafts" folder so I can review it on my phone before sending.
* **As a Developer:** I want to run this server using a simple Docker container with environment variables for credentials.

## 3. Technical Architecture

### 3.1 High-Level Flow

```mermaid
graph LR
    A[LLM Client (Cursor/Claude)] <-->|JSON-RPC via Stdio/SSE| B(FastMCP Server)
    B <-->|Async IMAP / TLS| C[IMAP Server (Read/Drafts)]
    B <-->|Async SMTP / TLS| D[SMTP Server (Send)]

```

### 3.2 Technology Stack

* **Core Framework:** `fastmcp` (Python)
* **Runtime:** Python 3.11+ (Required for advanced asyncio features)
* **IMAP Client:** `aioimaplib` (Asynchronous IMAP)
* **SMTP Client:** `aiosmtplib` (Asynchronous SMTP)
* **Parsing:** `email` (Standard lib), `beautifulsoup4` (For cleaning HTML body text)
* **Configuration:** `pydantic-settings` (Type-safe env loading)

## 4. Configuration & Security

The server must **never** accept credentials as arguments in MCP tool calls. All authentication is handled via Environment Variables.

| Variable | Description | Required | Example |
| --- | --- | --- | --- |
| `SMTP_HOST` | Hostname for sending | Yes | `smtp.zoho.com` |
| `SMTP_PORT` | Port for sending | Yes | `587` (TLS) or `465` (SSL) |
| `IMAP_HOST` | Hostname for reading | Yes | `imap.zoho.com` |
| `IMAP_PORT` | Port for reading | Yes | `993` |
| `EMAIL_USER` | Full email address | Yes | `user@customdomain.com` |
| `EMAIL_PASS` | App Password/Password | Yes | `xc9-s8d-s9d` |

## 5. Functional Requirements (Tools)

### 5.1 Tool: `check_connection`

* **Description:** validatesthe ability to connect and authenticate with both SMTP and IMAP servers.
* **Inputs:** None.
* **Returns:** JSON object with status checks and latency stats.

### 5.2 Tool: `list_emails`

* **Description:** Fetches email metadata from a specific folder.
* **Inputs:**
* `folder` (string, default="INBOX"): The folder to search.
* `limit` (int, default=10): Max number of emails.
* `query` (string, optional): specific search criteria (e.g., `FROM "amazon.com"`).


* **Returns:** List of `EmailSummary` objects (ID, Sender, Subject, Date).
* **Technical constraint:** Must use `IMAP SEARCH` commands, not fetch all and filter in Python.

### 5.3 Tool: `read_email`

* **Description:** Fetches the full content of a specific email.
* **Inputs:**
* `email_id` (string): The unique ID from `list_emails`.
* `folder` (string, default="INBOX").


* **Returns:** Full text body (HTML stripped to Markdown) and list of attachment filenames (content excluded for MVP).

### 5.4 Tool: `draft_email`

* **Description:** Creates a new email and saves it to the provider's **Drafts** folder on the server.
* **Inputs:**
* `to_recipients` (List[str])
* `subject` (str)
* `body_text` (str)


* **Returns:** `Confirmation` string ("Saved to Drafts folder with ID #123").

### 5.5 Tool: `send_email`

* **Description:** Sends an email immediately.
* **Inputs:**
* `to_recipients` (List[str])
* `cc_recipients` (List[str], optional)
* `subject` (str)
* `body_text` (str)


* **Returns:** `DeliveryStatus` (Success/Fail).

## 6. Error Handling Strategy

The FastMCP server must catch specific exceptions and return user-friendly strings to the LLM, not stack traces.

1. **AuthError:** "Authentication failed. Please check EMAIL_USER and EMAIL_PASS environment variables."
2. **NetworkError:** "Could not reach https://www.google.com/url?sa=E&source=gmail&q=imap.zoho.com. Check your internet connection or DNS."
3. **FolderError:** "Folder 'Important' does not exist. Available folders: Inbox, Sent, Drafts."

## 7. Development Phases

### Phase 1: Skeleton & Auth (Day 1)

* Setup `FastMCP` server structure.
* Implement `pydantic` settings.
* Implement `check_connection` with `aiosmtplib` and `aioimaplib`.

### Phase 2: Reading (Day 2)

* Implement `list_emails` and `read_email`.
* Implement MIME parsing logic (handle multipart/alternative).
* **Milestone:** Cursor can read your latest 5 emails.

### Phase 3: Writing (Day 3)

* Implement `send_email`.
* Implement `draft_email` (IMAP APPEND command).
* Dockerize.

## 8. Risks & Mitigations

* **Risk:** IMAP IDs change (UIDVALIDITY).
* *Mitigation:* Use UIDs (Unique IDs) instead of sequence numbers in all IMAP calls.


* **Risk:** HTML Emails are too large for LLM Context.
* *Mitigation:* Use `BeautifulSoup` to extract text-only representation. Truncate body if > 50,000 characters.
