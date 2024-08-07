Streamlit Chat and Location Query Application

Backend Link : https://github.com/chakibo004/Volund_BackEnd

This application is a Streamlit-based web app that enables users to authenticate, manage chat sessions, and query location data. It leverages various APIs for authentication, session management, and location querying, and integrates with Folium and Pydeck for mapping and visualization.
Features

    User Authentication: Sign up, log in, and manage user sessions.
    Session Management: View chat history and start new chats.
    Location Query: Query location data based on longitude and latitude.
    Place Visualization: Display queried locations on an interactive map using Folium.
    AI Interaction: Communicate with an AI backend to process and respond to queries.

Requirements

    Python 3.x
    Streamlit
    Requests
    Folium
    Pydeck
    Streamlit-Folium

Installation

    Clone the Repository:

    bash

git clone https://github.com/chakibo004/Volund_FrontEnd
cd Volund_FrontEnd

Install the Required Packages:

bash

pip install -r requirements.txt

Set Up Environment Variables:

Create a .env file in the root directory of the project and add the following lines, replacing the placeholders with your actual values:

plaintext

    API_BASE_URL=https://volund-backend.onrender.com/

Usage

    Run the Streamlit App:

    bash

    streamlit run app.py

    Navigate to the App:

    Open your browser and go to http://localhost:8501.

App Features
Authentication Page

    Login: Enter your username and password to log in. Successful login stores a JWT token for session management.
    Sign Up: Create a new account by entering a username and password.

Chat Page

    Chat History: View and select previous chat sessions.
    New Chat: Start a new chat session.
    Location Query: Enter longitude and latitude to query location data and display results on a map.
    Map Visualization: Interactive map displaying queried locations with markers.

Error Handling

    Invalid Input: The app provides feedback on incorrect latitude or longitude values.
    API Call Failures: Errors in API calls are handled with appropriate messages.

API Endpoints

    Login Endpoint: /login - Authenticates users and returns a JWT token.
    Sign Up Endpoint: /sign_up - Creates a new user account.
    Session History Endpoint: /session-history/ - Retrieves a list of session IDs.
    Session Details Endpoint: /session-history/{session_id} - Retrieves messages for a specific session.
    Location Query Endpoint: /query_location - Queries location data based on latitude and longitude.
    Place Query Endpoint: /query_place - Queries information about a specific place.
    Get All Places Endpoint: /get_all_places/{session_id} - Retrieves all places related to a session.

Troubleshooting

    Login Issues: Ensure your username and password are correct. Check the server status.
    Map Display Problems: Verify the validity of longitude and latitude values. Ensure your API endpoint is correctly configured.

