import plivo

# --- CONFIGURATION ---
AUTH_ID = ""
AUTH_TOKEN = ""

# The number people see when you call (From your list)
SOURCE_NUMBER = "14692463987" 

# --- UPDATE THESE TWO VARIABLES ---
# The number you want to test call (YOUR REAL MOBILE NUMBER)
# Format: Country code + Number (e.g., 919876543210)
DESTINATION_NUMBER = "916364103939"  

# YOUR NGROK URL (Copy from Step 1 window)
# Example: "https://a1b2-c3d4.ngrok-free.app"
NGROK_URL = "https://stefani-semifixed-pockily.ngrok-free.dev" 
# ----------------------------------

def make_call():
    client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)
    
    print(f"Initiating call to {DESTINATION_NUMBER}...")
    
    try:
        response = client.calls.create(
            from_=SOURCE_NUMBER,
            to_=DESTINATION_NUMBER,
            answer_url=f"{NGROK_URL}/ivr",
            answer_method='GET'
        )
        print(f"Call initiated! Call UUID: {response.request_uuid}")
    except Exception as e:
        print(f"Error making call: {e}")

if __name__ == "__main__":
    make_call()