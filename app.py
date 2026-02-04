from flask import Flask, request, make_response
from plivo import plivoxml

app = Flask(__name__)

@app.route('/debug', methods=['GET', 'POST'])
def debug():
    """Debug endpoint to test ngrok connectivity"""
    return f"Ngrok is working! Method: {request.method}, Args: {request.args}, Form: {request.form}"

@app.route('/test-xml', methods=['GET'])
def test_xml():
    """Test endpoint to see the generated XML"""
    response = plivoxml.ResponseElement()
    response.add_wait(length=1)
    
    action_url = f"{NGROK_URL}/ivr/level2"
    get_digits = response.add_get_digits(
        action=action_url,
        method='POST',
        num_digits=1,
        timeout=10,
        finish_on_key='#'
    )
    get_digits.add_speak("Welcome to Inspire Works. Press 1 for English. Press 2 for Spanish.")
    response.add_speak("Sorry, I didn't hear your selection. Please try calling again. Goodbye.")
    
    return f"<pre>{response.to_string()}</pre>"

# --- CONFIGURATION ---
ASSOCIATE_NUMBER = "918031274121" 

# *** UPDATE THIS WITH YOUR CURRENT NGROK URL ***
NGROK_URL = "https://stefani-semifixed-pockily.ngrok-free.dev"

@app.route('/ivr', methods=['GET', 'POST'])
def ivr_root():
    """Level 1: Language Selection"""
    print(f"DEBUG: IVR Root - Method: {request.method}, Form data: {request.form}, Args: {request.args}")
    
    # Build XML manually to ensure correct structure
    action_url = f"{NGROK_URL}/ivr/level2"
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Wait length="1"/>
    <GetDigits action="{action_url}" method="POST" timeout="15" numDigits="1" finishOnKey="#">
        <Speak>Welcome to Inspire Works. Press 1 for English. Press 2 for Spanish.</Speak>
    </GetDigits>
    <Speak>Sorry, I didn't hear your selection. Please try calling again. Goodbye.</Speak>
</Response>"""
    
    return make_response(xml_response, 200, {'Content-Type': 'application/xml'})

@app.route('/ivr/level2', methods=['POST'])
def ivr_level2():
    """Level 2: Action Selection based on Language"""
    digits = request.form.get('Digits')
    print(f"DEBUG: Level 2 received digits: {digits}")
    
    action_url = f"{NGROK_URL}/ivr/action"

    # Determine prompt
    if digits == '1': # English
        prompt = "For a short audio message, press 1. To speak to an associate, press 2."
        language = "en-US"
    elif digits == '2': # Spanish
        prompt = "Para un mensaje de audio, presione 1. Para hablar con un asociado, presione 2."
        language = "es-ES" 
    else:
        # Handle invalid selection
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Invalid selection.</Speak>
    <Redirect>{NGROK_URL}/ivr</Redirect>
</Response>"""
        return make_response(xml_response, 200, {'Content-Type': 'application/xml'})

    # Build XML manually with proper nesting
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <GetDigits action="{action_url}" method="POST" timeout="15" numDigits="1" finishOnKey="#">
        <Speak language="{language}">{prompt}</Speak>
    </GetDigits>
    <Speak>Sorry, I didn't receive your selection. Returning to main menu.</Speak>
    <Redirect>{NGROK_URL}/ivr</Redirect>
</Response>"""
    
    return make_response(xml_response, 200, {'Content-Type': 'application/xml'})

@app.route('/ivr/action', methods=['POST'])
def ivr_action():
    """Final Step"""
    digits = request.form.get('Digits')
    print(f"DEBUG: Action received digits: {digits}")
    
    if digits == '1':
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Here is the short audio message. Thank you for calling Inspire Works.</Speak>
</Response>"""
    elif digits == '2':
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Connecting you to an associate. Please hold.</Speak>
    <Dial>
        <Number>{ASSOCIATE_NUMBER}</Number>
    </Dial>
</Response>"""
    else:
        xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Speak>Invalid input.</Speak>
</Response>"""
    
    return make_response(xml_response, 200, {'Content-Type': 'application/xml'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)