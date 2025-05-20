from flask import Flask,render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Ticketmaster API Key from environment variables
TM_API_KEY = os.getenv("TICKETMASTER_API_KEY")


@app.route('/')
def home():
    return render_template('index.html')

# Define the events route
@app.route('/events', methods=['GET'])
def get_events():
    # Get city name from query parameters
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City name is required"}), 400
    
    # Ticketmaster Discovery API URL with city and API key embedded
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&city={city}"
    
    try:
        # Make the API request to Ticketmaster
        response = requests.get(url)
        if response.status_code == 200:
            event_data = response.json()
            return jsonify(event_data)
        else:
            return jsonify({"Error": "Failed to retrieve events"})
       # response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
      
        
        # Extract event data
        # events = data.get('_embedded', {}).get('events', [])
        # result = [
        #     {
        #         "name": event['name'],
        #         "date": event['dates']['start']['localDate'],
        #         "venue": event['_embedded']['venues'][0]['name'] if '_embedded' in event and 'venues' in event['_embedded'] else "Unknown Venue"
        #     }
        #     for event in events
        # ]
        
        # Return the event data as JSON
        # return jsonify(result)
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return jsonify({"error": str(e)}), 500
    
    

# Define the route to get event details
@app.route('/event/<event_id>', methods=['GET'])
def get_event_details(event_id):
    """
    Retrieve event details using Ticketmaster's Event Details API.
    :param event_id: The unique ID of the event
    """
    # Base URL for Ticketmaster API
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}/images.json"
    
    # Query parameters
    params = {
        "apikey": TM_API_KEY,  # API Key
        "locale": request.args.get("locale", "*"),  # Locale (default: all)
        "domain": request.args.get("domain")        # Optional: Filter by domain
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)

        # Parse the JSON response
        event_data = response.json()
        
        # Return the event data
        return jsonify(event_data)

    except requests.exceptions.RequestException as e:
        # Handle request errors
        return jsonify({"error": str(e)}), 500


    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
  


