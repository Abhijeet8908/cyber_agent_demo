import os
import dotenv
import sys

# Add current directory to path to allow local imports if run from outside
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from sheets_handler import SheetsHandler
from browser_handler import BrowserHandler

dotenv.load_dotenv()

# Initialize handlers
# Note: In a real persistent agent, we might want to initialize these inside the tool or manage lifecycle better.
sheets_handler = SheetsHandler() 
browser_handler = BrowserHandler(headless=False) 

def process_tickets(sheet_name: str, base_url: str) -> str:
    """
    Reads ticket numbers from the specified Google Sheet and checks each one in the browser.
    
    Args:
        sheet_name: The name or ID of the Google Sheet.
        base_url: The base URL of the internal application (e.g., https://internal-app.com/ticket/).
                  The ticket ID will be appended to this URL.
                  
    Returns:
        A summary of the processed tickets.
    """
    try:
        # 1. Get Tickets
        print(f"Fetching tickets from {sheet_name}...")
        tickets = sheets_handler.get_ticket_numbers(sheet_name)
        
        if isinstance(tickets, str) and tickets.startswith("Error"):
            return tickets 
            
        if not tickets:
            return "No tickets found in Column A."

        # 2. Ensure Login
        print(f"Ensuring login to {base_url}...")
        browser_handler.ensure_login(base_url)
        
        # 3. Check Tickets
        results = []
        for ticket in tickets:
            if not ticket: continue 
            ticket_url = f"{base_url}{ticket}"
            result = browser_handler.check_ticket(ticket_url)
            results.append(result)
            
        return "\n".join(results)

    except Exception as e:
        return f"Error during processing: {str(e)}"

# Define the Agent
ticket_agent = Agent(
    name="ticket_processor",
    model="gemini-2.5-flash",
    instruction="""You are a ticket processing assistant. 
    Your goal is to help the user check ticket details from a Google Sheet.
    Use the process_tickets tool to read from the sheet and check the internal application.
    If the user hasn't provided the sheet name or base URL, ask for them.
    """,
    tools=[FunctionTool(process_tickets)]
)

if __name__ == "__main__":
    print("Ticket Agent Started. Type 'exit' to quit.")
    # Simple loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            response = ticket_agent.run(user_input)
            print(f"Agent: {response.text}")
        except KeyboardInterrupt:
            break
