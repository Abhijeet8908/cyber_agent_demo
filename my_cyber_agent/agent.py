import os
import dotenv
import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search
dotenv.load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def fetch_ip_data(ip: str) -> str:
    """Fetches location and ISP details for a given IP address."""
    try:
        # Constructing the lookup URL
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data.get("status") == "fail":
            return f"Could not find data for {ip}."
        
        return (f"IP: {data['query']}\nLocation: {data['city']}, {data['country']}\n"
                f"ISP: {data['isp']}\nLat/Lon: {data['lat']}, {data['lon']}")
    except Exception as e:
        return f"Error: {str(e)}"
    
def fetch_abuse_ip_data(ip: str) -> str:
    """Fetches abuse contact details for a given IP address."""
    try:
        import requests
        import json

        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': ABUSEIPDB_API_KEY
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)

        # Formatted output
        decodedResponse = json.loads(response.text)
        return json.dumps(decodedResponse, sort_keys=True, indent=4)
    except Exception as e:
        return f"Error: {str(e)}"

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.5-flash", 
    instruction="""You are a network specialist. When a user provides an IP address, 
    use the fetch_ip_data tool to get details and present them in a professional report.""",
    description="An assistant that can search a specific website for IP details.",
    tools=[FunctionTool(fetch_abuse_ip_data)]
)

# Extract the Domain from the output of the fetch_ip_data tool and show only that part.