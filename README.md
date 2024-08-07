Streamlit Chat and Location Query Application

This application is a Streamlit-based web app that allows users to authenticate, manage chat sessions, and query location data. It leverages various APIs for authentication, session management, and location querying, and integrates with Folium and Pydeck for mapping and visualization.
Features

    User Authentication: Users can sign up, log in, and manage their sessions.
    Session Management: Users can view their chat history and start new chats.
    Location Query: Users can query location data based on longitude and latitude.
    Place Visualization: Displays queried locations on an interactive map using Folium.
    AI Interaction: Communicates with an AI backend to process and respond to queries.

Requirements

    Python 3.x
    Streamlit
    Requests
    Folium
    Pydeck
    Streamlit-Folium

Installation

    Clone the repository:

    bash

git clone https://github.com/chakibo004/Volund_FrontEnd
cd your-repo

Install the required packages:

bash

pip install -r requirements.txt

Create a .env file in the root directory of the project to store your environment variables. Add the following lines, replacing the placeholders with your actual values:

plaintext

    API_BASE_URL=https://volund-backend.onrender.com/

Usage

    Run the Streamlit app:

    bash

    streamlit run app.py

    Navigate to the app in your browser (typically http://localhost:8501).

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

    The app provides feedback on invalid input (e.g., incorrect latitude or longitude) and API call failures.

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