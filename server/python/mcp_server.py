from fastmcp import FastMCP
import requests
import urllib.parse

# Define API server base URL
API_BASE_URL = "http://127.0.0.1:5000/api"

mcp = FastMCP("CARE_NAVIGATOR")


# ---- Demographics Tools/Resources ----
@mcp.tool()
def get_patient_demographics(first_name: str, last_name: str, dob: str) -> dict:
    """Retrieve basic demographic information for a patient
       demographics API returns Age, email, phone, address, and insurance information.
    """
    try:
        # Call the API with demographic parameters directly
        response = requests.get(f"{API_BASE_URL}/demographics", 
                               params={"first_name": first_name, "last_name": last_name, "dob": dob})
        response.raise_for_status()
        data = response.json()
        
        # Handle empty results
        if not data:
            return {"error": f"No demographic information found for patient {first_name} {last_name}"}
            
        return data[0]  # Return the first (and should be only) result
    except requests.exceptions.RequestException as e:
        return {"error": f"API request error: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)