# Agent.py Documentation

## Overview

This module implements a network specialist AI agent that retrieves and analyzes IP address information. The agent uses Google's ADK (Agent Development Kit) to provide IP geolocation, ISP details, and abuse reporting capabilities.

## Dependencies

- `os` - Operating system interface
- `dotenv` - Environment variable management
- `requests` - HTTP library for API calls
- `google.adk.agents` - Google Agent Development Kit
- `google.adk.tools` - Tools for agent functionality (FunctionTool, google_search)

## Environment Variables

The module requires the following environment variables to be set (typically in a `.env` file):

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | API key for Google services |
| `ABUSEIPDB_API_KEY` | API key for AbuseIPDB service |

## Functions

### `fetch_ip_data(ip: str) -> str`

Fetches location and ISP details for a given IP address using the ip-api.com service.

**Parameters:**
- `ip` (str): The IP address to query

**Returns:**
- (str): Formatted string containing:
  - IP address
  - City and Country
  - ISP information
  - Latitude and Longitude coordinates

**Exceptions:**
- Returns error message if the IP cannot be found or request fails
- Includes timeout handling (5 seconds)

**API Used:** ip-api.com (free tier)

---

### `fetch_abuse_ip_data(ip: str) -> str`

Fetches abuse reports and malicious activity data for a given IP address using the AbuseIPDB service.

**Parameters:**
- `ip` (str): The IP address to query

**Returns:**
- (str): JSON-formatted response containing abuse reports and malicious activity data

**Query Parameters:**
- `ipAddress`: The IP address to check
- `maxAgeInDays`: Set to 90 days for recent reports

**Headers:**
- `Accept`: application/json
- `Key`: AbuseIPDB API key for authentication

**Exceptions:**
- Returns error message if the request fails

**API Used:** AbuseIPDB API v2

---

## Agent Configuration

### Root Agent (`root_agent`)

**Type:** Google ADK Agent

**Properties:**
| Property | Value |
|----------|-------|
| Name | `search_assistant` |
| Model | `gemini-2.5-flash` |
| Description | An assistant that can search a specific website for IP details |

**Instruction:**
> "You are a network specialist. When a user provides an IP address, use the fetch_ip_data tool to get details and present them in a professional report."

**Tools:**
- `fetch_abuse_ip_data` - Function tool for retrieving abuse IP data

---

## Usage Example

```python
# The agent can be used to process IP addresses and return professional reports
# Example: User provides an IP address
# The agent uses fetch_ip_data to retrieve location and ISP details
# Results are formatted as a professional network security report
```

## Notes

- The `fetch_ip_data` function is defined but not explicitly registered as a tool in the agent
- Only `fetch_abuse_ip_data` is currently added to the agent's tools list
- Consider adding `fetch_ip_data` as a FunctionTool for full functionality
- IP-API has rate limits on the free tier (45 requests per minute)
- AbuseIPDB requires a valid API key with appropriate permissions

## Potential Improvements

1. **Tool Registration:** Add `fetch_ip_data` as a FunctionTool to the agent
2. **Error Handling:** Implement more granular exception handling
3. **Rate Limiting:** Implement caching to avoid hitting API rate limits
4. **Response Formatting:** Consider structured responses instead of string formatting
5. **Data Validation:** Add IP address validation before making API requests
6. **Configuration:** Move hardcoded values to configuration files

## Related Files

- `requirements.txt` - Project dependencies
- `.env` - Environment configuration file
- `my_cyber_agent/` - Agent module directory
