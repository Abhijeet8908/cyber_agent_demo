import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_mistral import process_tickets, tools_schema
    print("Agent Mistral imported successfully.")
    print(f"Tools Schema Loaded: {len(tools_schema)} tools.")
except Exception as e:
    print(f"Failed to import Agent Mistral: {e}")
