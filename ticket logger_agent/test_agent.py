import sys
import os

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from sheets_handler import SheetsHandler
    print("SheetsHandler imported successfully.")
except Exception as e:
    print(f"Failed to import SheetsHandler: {e}")

try:
    from browser_handler import BrowserHandler
    print("BrowserHandler imported successfully.")
    
    # Try initializing (not starting browser to avoid hanging if install is incomplete)
    bh = BrowserHandler(headless=True)
    print("BrowserHandler initialized.")
except Exception as e:
    print(f"Failed to import/init BrowserHandler: {e}")
