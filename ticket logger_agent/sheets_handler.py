import gspread
import os
from google.oauth2.service_account import Credentials

class SheetsHandler:
    def __init__(self, credentials_path="credentials.json"):
        self.credentials_path = credentials_path
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.client = None

    def connect(self):
        """Authenticates with Google Sheets API."""
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")
        
        creds = Credentials.from_service_account_file(self.credentials_path, scopes=self.scope)
        self.client = gspread.authorize(creds)

    def get_ticket_numbers(self, sheet_name_or_id):
        """Reads ticket numbers from Column A of the specified sheet."""
        if not self.client:
            self.connect()

        try:
            # Try opening by name first, if fails, try by key
            try:
                sheet = self.client.open(sheet_name_or_id).sheet1
            except gspread.SpreadsheetNotFound:
                sheet = self.client.open_by_key(sheet_name_or_id).sheet1
            
            # Get all values from column A
            # Assuming row 1 might be a header, we can filter it out later or returning all
            values = sheet.col_values(1)
            return values
        except Exception as e:
            return f"Error reading sheet: {str(e)}"
