import streamlit as st
import requests
import json
import folium
from streamlit_folium import folium_static
import pydeck as pdk
from streamlit.components.v1 import html
# Constants
API_BASE_URL = 'https://volund-backend.onrender.com/'
SESSION_HISTORY_ENDPOINT = '/session-history/'
SESSION_BY_ID_ENDPOINT = '/session-history/{session_id}'
QUERY_LOCATION_ENDPOINT = '/query_location'
QUERY_PLACE_ENDPOINT = '/query_place'
GET_ALL_PLACES_ENDPOINT = '/get_all_places/{session_id}'
SIGN_UP_ENDPOINT = '/sign_up'
LOGIN_ENDPOINT = '/login'

def validate_latitude(lat):
    if lat is None:
        return False
    return -90 <= lat <= 90

def validate_longitude(lon):
    if lon is None:
        return False
    return -180 <= lon <= 180

# Function to get the JWT token
def get_jwt_token(username, password):
    response = requests.post(API_BASE_URL + LOGIN_ENDPOINT, json={
        'username': username,
        'password': password
    })
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        st.error("Login failed!")
        return None

# Function to sign up a new user
def sign_up(username, password):
    response = requests.post(API_BASE_URL + SIGN_UP_ENDPOINT, json={
        'username': username,
        'password': password
    })
    if response.status_code == 200:
        st.success("Sign up successful! Please log in.")
        st.session_state['signup_success'] = True
    else:
        st.error("Sign up failed!")

# Function to get session history
def get_session_history(token):
    response = requests.get(API_BASE_URL + SESSION_HISTORY_ENDPOINT, params={
        'token': token
    })
    if response.status_code == 200:
        try:
            # Parse JSON response
            data = response.json()
            
            # Check if 'sessions' key exists and is a list
            sessions = data.get('sessions', [])
            if not isinstance(sessions, list):
                st.error("Invalid format for sessions.")
                return []

            # Extract session IDs
            session_ids = [session.get('session_id') for session in sessions if isinstance(session, dict)]
            return session_ids

        except ValueError as e:
            st.error("Failed to parse JSON response.")
            return []
    else:
        st.error("Failed to retrieve session history.")
        return []

# Function to get session messages by ID
def get_session_by_id(session_id, token):
    response = requests.get(API_BASE_URL + SESSION_BY_ID_ENDPOINT.format(session_id=session_id), params={
        'token': token
    })
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve session details.")
        return []

# Function to query location
def query_location(longitude, latitude, token, session_id=None, question=None):
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'token': token,
    }
    if session_id:
        data['session_id'] = session_id
    if question:
        data['question'] = question
    response = requests.post(API_BASE_URL + QUERY_LOCATION_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to query location.")
        return None

# Function to query place
def query_place(place_name, token, session_id, question=None):
    data = {
        'place_name': place_name,
        'token': token,
        'session_id': session_id
    }
    if question:
        data['question'] = question
    response = requests.post(API_BASE_URL + QUERY_PLACE_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to query place.")
        return None
    
def query_ai(query, token, session_id=None):
    data = {
        'query': query,
        'token': token,
        'session_id': session_id if session_id else ''
    }
    print("Request data:", data)
    try:
        response = requests.post(f"{API_BASE_URL}query_ai", json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to query AI: {e}")
        return None

# Function to get all places
def get_all_places(session_id, token):
    response = requests.get(API_BASE_URL + GET_ALL_PLACES_ENDPOINT.format(session_id=session_id), params={
        'token': token
    })
    
    if response.status_code == 200:
        data = response.json()
        print("Data fetched:", data)  # Add this line for debugging
        return data
    else:
        # Print error details for debugging
        print(f"Failed to get all places. Status code: {response.status_code}, Response: {response.text}")
        return {}

# Authentication page
def authentication_page():
    # Apply custom CSS for styling
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #e3f2fd;  /* Light blue background for a fresh look */
            font-family: 'Verdana', sans-serif;  /* Clean and modern font */
        }
        .header {
            color: #0288d1;  /* Bright blue color for the header */
            font-size: 2.2em;
            text-align: center;
            margin-top: 20px;
            padding: 10px;
        }
        .subheader {
            color: #01579b;  /* Darker blue color for the subheader */
            font-size: 1.4em;
            margin-bottom: 20px;
        }
        .form-container {
            background-color: #ffffff;  /* White background for forms */
            border-radius: 8px;  /* Rounded corners */
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);  /* Subtle shadow */
            margin: auto;
            max-width: 400px;  /* Fixed width for the form */
        }
        .form-button {
            background-color: #039be5;  /* Bright blue for buttons */
            color: #ffffff;  /* White text color */
            border-radius: 4px;  /* Rounded corners */
            padding: 10px;
            font-size: 1em;
            width: 100%;
            text-align: center;
            cursor: pointer;
            border: none;
            transition: background-color 0.3s;  /* Smooth color transition */
        }
        .form-button:hover {
            background-color: #0288d1;  /* Darker blue on hover */
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 4px;  /* Rounded corners */
            border: 1px solid #b0bec5;  /* Light grey border */
            background-color: #fafafa;  /* Light grey background for inputs */
            box-sizing: border-box;
            transition: border-color 0.3s;  /* Smooth border color transition */
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #039be5;  /* Highlight border color matching button */
            outline: none;
            background-color: #ffffff;  /* White background on focus */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown('<div class="header">Authentication</div>', unsafe_allow_html=True)

    # Tabs for signup and login
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login Tab
    with tab1:
        st.markdown('<div class="subheader">Login</div>', unsafe_allow_html=True)
        with st.container():
            with st.form(key='login_form', clear_on_submit=True):
                username = st.text_input('Username', key='login')
                password = st.text_input('Password', type='password', key='password')
                login_button = st.form_submit_button('Login', use_container_width=True, help='Click to log in')
                if login_button:
                    token = get_jwt_token(username, password)
                    if token:
                        st.session_state['token'] = token
                        st.session_state['selected_session_id'] = None
                        st.session_state['username'] = username
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Sign Up Tab
    with tab2:
        st.markdown('<div class="subheader">Sign Up</div>', unsafe_allow_html=True)
        with st.container():
            with st.form(key='signup_form', clear_on_submit=True):
                username = st.text_input('Username')
                password = st.text_input('Password', type='password')
                signup_button = st.form_submit_button('Sign Up', use_container_width=True, help='Click to sign up')
                if signup_button:
                    sign_up(username, password)
                    if 'signup_success' in st.session_state and st.session_state['signup_success']:
                        st.session_state['signup_success'] = False
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


def chat_page():
    st.title('Chat Application')

    if 'token' in st.session_state:
        token = st.session_state['token']
        selected_session_id = st.session_state.get('selected_session_id', None)
        username = st.session_state['username'] # Ensure you have the username in session state

        st.markdown("""
        <style>
        .sidebar {
            padding: 20px;
            background-color: #4caf50; /* Fresh green background for the sidebar */
            border-right: 1px solid #388e3c; /* Darker green border */
            height: 100vh;
            overflow-y: auto;
        }
        .sidebar-username {
            padding: 10px;
            border-radius: 8px;
            background-color: #ffffff; /* White background for username */
            color: #4caf50; /* Fresh green color for text */
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px; /* Reduced margin to fit logout button */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtle shadow */
        }
        .sidebar-logout {
            background-color: #ff5722; /* Vibrant orange for logout button */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            cursor: pointer;
            font-size: 16px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtle shadow */
        }
        .sidebar-logout:hover {
            background-color: #e64a19; /* Darker orange on hover */
        }
        .sidebar-button {
            background-color: #ffffff; /* White background for session buttons */
            border: 1px solid #b0bec5; /* Light grey border */
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            text-align: center;
            color: #333;
            font-weight: bold;
            transition: background-color 0.3s, border-color 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtle shadow */
        }
        .sidebar-button:hover {
            background-color: #f5f5f5; /* Light grey on hover */
        }
        .sidebar-button.selected {
            background-color: #388e3c; /* Dark green for selected session */
            color: white;
            border-color: #388e3c;
        }
        </style>
        """, unsafe_allow_html=True)


        with st.sidebar:
            # Display username and logout button
            st.markdown(f'<div class="sidebar-username">{username}</div>', unsafe_allow_html=True)
            
            if st.button('Logout', key='logout', help='Log out of the application'):
                st.session_state.clear()  # Clears all session state variables
                st.rerun()  # Refresh the page

            # Display chat history
            st.header('Chat History')
            session_ids = get_session_history(token)

            if st.button('New Chat'):
                st.session_state['selected_session_id'] = None
                selected_session_id = None
                st.session_state['location_query_done'] = False  # Reset location query status
                st.session_state['all_places_data'] = None  # Clear stored place data
                st.rerun()

            # Display sessions as a reversed list with styling
            for session_id in reversed(session_ids):
                button_class = 'sidebar-button'
                if session_id == selected_session_id:
                    button_class += ' selected'
                if st.button(f"Session {session_id}", key=session_id):
                    st.session_state['selected_session_id'] = session_id
                    selected_session_id = session_id
                    st.session_state['location_query_done'] = False  # Reset location query status
                    st.session_state['all_places_data'] = None  # Clear stored place data
                    st.session_state['longitude']=None
                    st.session_state['latitude']=None
                    st.rerun()

        if selected_session_id:
            session_details = get_session_by_id(selected_session_id, token)
            st.session_state['selected_session_id'] = selected_session_id

            # Apply beautiful styling for chat messages
            st.markdown("""
            <style>
            .chat-box {
                display: flex;
                flex-direction: column;
                max-height: 600px;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .chat-message {
                margin: 5px 0;
                padding: 10px;
                border-radius: 10px;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                position: relative;
                max-width: 75%;
            }
            .chat-message.ai {
                background-color: #e0f7fa;
                align-self: flex-start;
            }
            .chat-message.user {
                background-color: #c8e6c9;
                align-self: flex-end;
                border-radius: 10px 10px 0 10px;
            }
            .chat-message::before {
                content: '';
                position: absolute;
                width: 0;
                height: 0;
                border: 10px solid transparent;
            }
            .chat-message.ai::before {
                border-right-color: #e0f7fa;
                top: 10px;
                left: -10px;
                border-width: 10px 10px 10px 0;
            }
            .chat-message.user::before {
                border-left-color: #c8e6c9;
                top: 10px;
                right: -10px;
                border-width: 10px 0 10px 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            for message in session_details.get('conversation', []):
                if message['query']:
                    st.markdown(f'<div class="chat-message user">{message["query"]}</div>', unsafe_allow_html=True)
                if message['response']:
                    st.markdown(f'<div class="chat-message ai">{message["response"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Retrieve persisted longitude and latitude
            longitude = st.session_state.get('longitude', None)
            latitude = st.session_state.get('latitude', None)
            all_places_data = st.session_state.get('all_places_data', None)

            # Input for longitude and latitude
            longitude_input = st.number_input('Longitude', format="%.6f", value=longitude)
            latitude_input = st.number_input('Latitude', format="%.6f", value=latitude)
            if latitude_input is not None and not validate_latitude(latitude_input):
                st.error("🚫 Invalid latitude value. Latitude must be between -90 and 90.")
            elif longitude_input is not None and not validate_longitude(longitude_input):
                st.error("🚫 Invalid longitude value. Longitude must be between -180 and 180.")
            else :
                if st.button('Query Location'):
                    if not (longitude_input and latitude_input and token and selected_session_id):
                        st.error('Please enter longitude, latitude, token, and session ID.')
                    else:
                        st.session_state['longitude'] = longitude_input
                        st.session_state['latitude'] = latitude_input
                        
                        st.session_state['location_query_done'] = False
                        st.session_state['all_places'] = []
                        st.session_state['location_data'] = None
                        
                        # Query locations
                        location_data = query_location(longitude_input, latitude_input, token, selected_session_id)
                        if location_data:
                            st.session_state['location_data'] = location_data
                            st.session_state['location_query_done'] = True
                            all_places_data = get_all_places(selected_session_id, token)
                            st.session_state['all_places_data'] = all_places_data
                            print(all_places_data)
                            if all_places_data:
                                st.session_state['all_places'] = all_places_data.get('places', [])
                            else:
                                st.error('No places found for this location.')
                            st.rerun()
                        else:
                            st.error('Failed to fetch location data.')

                # Handling location query
                if 'location_query_done' in st.session_state and st.session_state['location_query_done'] and all_places_data:
                    if st.session_state['location_data']:

                        # Display all places on the map
                        location_map = folium.Map(location=[latitude_input, longitude_input], zoom_start=10)
                        for place in st.session_state['all_places']:
                            folium.Marker(
                                location=[place['latitude'], place['longitude']],
                                popup=folium.Popup(f'<b>{place["name"]}</b><br><img src="{place["pictures"][0]}" width="100">', max_width=300),
                                icon=folium.Icon(color='blue')
                            ).add_to(location_map)
                        folium_static(location_map)

                        # Query a specific place
                        st.subheader('Query Place')
                        place_names = [place['name'] for place in st.session_state['all_places']]
                        selected_place = st.selectbox('Select a place', place_names)
                                
                        if st.button('Query Place') and selected_place:
                            place = next((p for p in st.session_state['all_places'] if p['name'] == selected_place), None)
                            if place:
                                response = query_place(place['name'], token, selected_session_id)
                                if response:
                                    st.markdown(f'<div class="chat-message ai">{response}</div>', unsafe_allow_html=True)
                                else:
                                    st.error('Failed to fetch place details.')
                            else:
                                st.error('Place not found in the list.')
                # New chat input
                with st.form(key='new_chat_form'):
                    user_input = st.text_input('Type your message', '')
                    submit_button = st.form_submit_button('Send')

                    if submit_button and user_input:
                        response = query_ai(user_input, token, selected_session_id)
                        st.rerun()

                    elif submit_button and not user_input:
                        st.warning("Please enter a message to start the conversation.")
        else:
            # No selected session ID: Show empty input and handle new session creation
            st.info("Start a new chat by entering a message below:")
            st.session_state['longitude']=None
            st.session_state['latitude']=None
            # Display a text input field for new queries
            with st.form(key='new_chat_form'):
                user_input = st.text_input('Type your message', '')
                submit_button = st.form_submit_button('Send')

                if submit_button and user_input:
                    response = query_ai(user_input, token)
                    if response:
                        new_session_id = response.get('session_id', None)
                        print(new_session_id)
                        if new_session_id:
                            st.session_state['selected_session_id'] = new_session_id
                            st.rerun()

                elif submit_button and not user_input:
                    st.warning("Please enter a message to start the conversation.")

    else:
        st.error("You need to be logged in to access this page.")

# Main function
def main():
    st.set_page_config(page_title='AI Chat Application', layout='wide')
    
    if 'token' not in st.session_state:
        authentication_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
