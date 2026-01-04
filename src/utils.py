import re
import email
from email.policy import default
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def find_folder(client, candidates: list[str]) -> str:
    """Helper to find the first existing folder from a list of candidates."""
    try:
        status, folders = await client.list('""', '*')
        if status != 'OK':
            return candidates[0]
            
        folder_names = []
        for f in folders:
            if isinstance(f, (bytes, bytearray)):
                f_str = f.decode()
            else:
                f_str = str(f)
                
            # Parse using the robust logic matching server.py
            # Simple fallback or regex
            if '"' in f_str:
                parts = f_str.split('"')
                folder_names.append(parts[-2])
            else:
                folder_names.append(f_str.split()[-1])
        
        for cand in candidates:
            if cand in folder_names:
                return cand
        
        return candidates[0]
    except Exception as e:
        logger.error(f"Error finding folder: {e}")
        return candidates[0]

def check_attachment(content_disposition: str) -> bool:
    return "attachment" in str(content_disposition).lower()

def extract_email_body(msg) -> str:
    """Extracts plain text or HTML (converted to text) from an email message."""
    body_text = ""
    html_text = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            
            if check_attachment(cdispo):
                continue
                
            if ctype == "text/plain":
                 payload = part.get_payload(decode=True)
                 if payload:
                    body_text += payload.decode(errors='ignore')
            elif ctype == "text/html":
                 payload = part.get_payload(decode=True)
                 if payload:
                    html_text += payload.decode(errors='ignore')
    else:
        ctype = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            decoded = payload.decode(errors='ignore')
            if ctype == "text/plain":
                body_text = decoded
            elif ctype == "text/html":
                html_text = decoded
    
    # Prioritize HTML -> Markdown if available, else Plain
    if html_text:
        try:
            soup = BeautifulSoup(html_text, "html.parser")
            return soup.get_text('\n')
        except Exception:
            return html_text if html_text else body_text
    
    return body_text

def parse_folder_line(folder_line):
    """Parses an IMAP LIST response line into name, flags, delimiter."""
    if isinstance(folder_line, (bytes, bytearray)):
        folder_str = folder_line.decode()
    else:
        folder_str = str(folder_line)

    pattern = re.compile(r'\((?P<flags>[^)]*)\)\s+(?P<delim>"[^"]+"|\S+)\s+(?P<name>.+)')
    match = pattern.search(folder_str)
    
    if match:
        flags = match.group("flags").strip()
        delimiter = match.group("delim").replace('"', '')
        name = match.group("name").strip()
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
            
        return {
            "name": name,
            "flags": flags,
            "delimiter": delimiter
        }
    else:
        # Fallback
        parts = folder_str.split('"')
        if len(parts) >= 2:
             return {
                "name": parts[-2] if len(parts) > 2 else parts[0],
                "flags": "",
                "delimiter": "/"
            }
    return None
