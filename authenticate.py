"""
Run this script manually to authenticate with Gmail.
This creates token.json so the MCP server doesn't need to open a browser.
"""

from auth import get_gmail_credentials

if __name__ == "__main__":
    print("Starting Gmail authentication...")
    print("A browser window will open. Please sign in and authorize the app.")
    
    try:
        creds = get_gmail_credentials()
        print("\n✅ Authentication successful!")
        print("token.json has been created. You can now use the MCP server.")
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
