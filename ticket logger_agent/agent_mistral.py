import os
import sys
import dotenv
import ollama

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets_handler import SheetsHandler
from browser_handler import BrowserHandler

dotenv.load_dotenv()

# Initialize handlers
sheets_handler = SheetsHandler()
browser_handler = BrowserHandler(headless=False)

def process_tickets(sheet_name: str, base_url: str) -> str:
    """
    Reads ticket numbers from the specified Google Sheet and checks each one in the internal application.
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
        return f"Error processing tickets: {str(e)}"

# Define Tool Schema for Ollama
tools_schema = [
    {
        'type': 'function',
        'function': {
            'name': 'process_tickets',
            'description': 'Reads ticket numbers from a Google Sheet and checks them in an internal application via browser.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'sheet_name': {
                        'type': 'string',
                        'description': 'The name of the Google Sheet.'
                    },
                    'base_url': {
                        'type': 'string',
                        'description': 'The base URL of the ticket system (e.g., https://app.com/ticket/).'
                    },
                },
                'required': ['sheet_name', 'base_url'],
            },
        },
    }
]

# Map names to functions
available_functions = {
    'process_tickets': process_tickets,
}

def run_agent():
    print("Mistral Ticket Agent (Ollama Native) Started. Type 'exit' to quit.")
    messages = []

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            messages.append({'role': 'user', 'content': user_input})
            
            print("Agent thinking...")
            response = ollama.chat(
                model='mistral',
                messages=messages,
                tools=tools_schema,
            )
            
            messages.append(response['message'])

            # Check if the model wants to call a tool
            if response['message'].get('tool_calls'):
                for tool in response['message']['tool_calls']:
                    function_name = tool['function']['name']
                    function_args = tool['function']['arguments']
                    
                    print(f"Calling tool: {function_name} with args: {function_args}")
                    
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        try:
                            tool_output = function_to_call(**function_args)
                        except Exception as e:
                            tool_output = f"Error executing tool: {e}"
                            
                        print(f"Tool Output: {tool_output}")
                        
                        # Add tool response to messages
                        messages.append({
                            'role': 'tool',
                            'content': str(tool_output),
                            # Ollama might expect tool_call_id linkage differently or just sequence.
                            # Standard OpenAI format uses tool_call_id, Ollama usually just follows sequence.
                            # 'tool_call_id': tool['id'] # Ollama currently doesn't strictly enforce IDs in some versions but good practice.
                        })
                    else:
                        print(f"Tool {function_name} not found.")

                # Get final response after tool execution
                final_response = ollama.chat(
                    model='mistral',
                    messages=messages,
                )
                print(f"Agent: {final_response['message']['content']}")
                messages.append(final_response['message'])
            
            else:
                print(f"Agent: {response['message']['content']}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_agent()
