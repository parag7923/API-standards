from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
import json
from dotenv import load_dotenv
import uuid
import datetime
import requests
import threading

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# SambaNova API credentials
sambanova_api_key = os.getenv('SAMBANOVA_API_KEY')
sambanova_api_url = os.getenv('SAMBANOVA_API_URL')

# Spotify API credentials
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Spotify authentication
auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Webhook URL (if applicable)
webhook_url = "http://localhost:8000/callback"  # Replace with your webhook URL if needed

# Load JSON configuration
with open('config.json') as f:
    config = json.load(f)

############### ENV VARIABLES ###############
SUPPORTED_METHOD = ["example_method", "another_method"]
PROMT_LEN = 10

############### ADD YOUR CUSTOM AI AGENT CALL HERE ###############
def hello_world():
    start_time = time.time()
    time.sleep(5)  # Placeholder for actual task processing
    end_time = time.time()
    processing_duration = end_time - start_time  # Calculate processing duration in seconds
    datatype = "META_DATA"
    return "Hello World", processing_duration, datatype

############### FUNCTION TO DETECT EMOTION USING SAMBANOVA API ###############
def detect_emotion(text):
    try:
        headers = {
            'Authorization': f'Bearer {sambanova_api_key}',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({"text": text})
        response = requests.post(sambanova_api_url, headers=headers, data=payload)
        response_data = response.json()
        emotion = response_data.get('emotion', 'unknown').lower()
        return emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return "unknown"

############### FUNCTION TO FIND SPOTIFY PLAYLISTS BASED ON KEYWORD ###############
def find_playlists_for_keyword(keyword, limit=10):
    try:
        random_queries = [f"{keyword} playlist", f"best {keyword} playlists", f"{keyword} hits"]
        query = random.choice(random_queries)
        results = sp.search(q=query, type='playlist', limit=limit)
        playlists = results['playlists']['items']
        return [{
            'name': playlist['name'],
            'description': playlist['description'],
            'link': playlist['external_urls']['spotify']
        } for playlist in playlists]
    except Exception as e:
        print(f"Error finding playlists: {e}")
        return []

############### FUNCTION TO FIND SPOTIFY PLAYLISTS BASED ON EMOTION ###############
def find_playlists_for_emotion(emotion, limit=10):
    emotion_to_query = {
        "joy": "happy",
        "anger": "angry",
        "fear": "fearful",
        "sadness": "sad",
        "surprise": "surprised",
        "disgust": "disgusted",
        "trust": "trusting",
        "anticipation": "anticipating",
        "boredom": "bored",
        "frustration": "frustrated",
        "confusion": "confused",
        "excitement": "excited",
        "contentment": "content",
        "relief": "relieved",
        "nostalgia": "nostalgic",
        "pride": "proud",
        "guilt": "guilty",
        "shame": "ashamed",
        "embarrassment": "embarrassed",
        "hope": "hopeful",
        "unknown": "mood",
        "mixed": "mixed emotions",
        "indifference": "indifferent"
    }

    query = emotion_to_query.get(emotion, "mood")
    
    try:
        random_queries = [f"{query} playlist", f"best {query} playlists", f"{query} hits"]
        query = random.choice(random_queries)
        results = sp.search(q=query, type='playlist', limit=limit)
        playlists = results['playlists']['items']
        return [{
            'name': playlist['name'],
            'description': playlist['description'],
            'link': playlist['external_urls']['spotify']
        } for playlist in playlists]
    except Exception as e:
        print(f"Error finding playlists: {e}")
        return []

############### CHECK IF ALL INFORMATION IS IN REQUEST ###############
def check_input_request(request):
    reason = ""
    status = ""
    user_id = request.headers.get('X-User-ID', None)
    if user_id is None or not user_id.strip():
        status = "INVALID_REQUEST"
        reason = "userToken is invalid"
    
    request_id = request.headers.get('x-request-id', None)
    request_data = request.get_json()
    
    if request_id is None or not request_id.strip():
        status = "INVALID_REQUEST"
        reason = "requestId is invalid"
    if status != "":
        trace_id = uuid.uuid4().hex
        error_code = {
            "status": status,
            "reason": reason
        }
        response_data = {
            "requestId": request_id,
            "traceId": trace_id,
            "processDuration": -1,
            "isResponseImmediate": True,
            "response": {},
            "errorCode": error_code
        }
        return response_data
    return None

############### API ENDPOINT TO RECEIVE REQUEST ###############
@app.route('/call', methods=['POST'])
def call_endpoint():
    user_id = request.headers.get('X-User-ID', None)
    request_data = request.get_json()
    method = request_data.get('method')
    ret = check_input_request(request)
    if ret is not None:
        return jsonify(ret), 400

    task_id = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    if method == "example_method":
        # Response preparation
        response = {"taskId": task_id}
        error_code = {"status": "PENDING", "reason": "Pending"}
        respose_data = {
            "requestId": requestId,
            "traceId": trace_id,
            "processDuration": -1,
            "isResponseImmediate": False,
            "response": response,
            "errorCode": error_code
        }

        # Task processing in a separate thread
        threading.Thread(target=process_task, args=(task_id, requestId, user_id)).start()

    # Immediate response to the client
    return jsonify(respose_data), 200

############### PROCESS THE CALL TASK HERE ###############
def process_task(task_id, requestId, user_id):
    data, processing_duration, datatype = hello_world()
    # Send the callback
    send_callback(user_id, task_id, requestId, processing_duration, data, datatype)

############### SEND CALLBACK TO YOUR APP MARKETPLACE ENDPOINT WITH TASK RESPONSE ###############
def send_callback(user_id, task_id, requestId, processing_duration, data, datatype):
    callback_message = {
        "apiVersion": "1.0",
        "service": "EmotionMusicPlayer",
        "datetime": datetime.datetime.now().isoformat(),
        "processDuration": processing_duration,
        "taskId": task_id,
        "isResponseImmediate": False,
        "response": {
            "dataType": datatype,
            "data": data
        },
        "errorCode": {
            "status": "AC_000",
            "reason": "success"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-marketplace-token": "1df239ef34d92aa8190b8086e89196ce41ce364190262ba71964e9f84112bc45",
        "x-request-id": requestId,
        "x-user-id": user_id
    }

    response = requests.post(webhook_url, json=callback_message, headers=headers)

############### /GET_PLAYLIST ENDPOINT ###############
@app.route('/get_playlist', methods=['POST'])
def get_playlist():
    ret = check_input_request(request)
    if ret is not None:
        return jsonify(ret), 400

    data = request.json
    user_text = data.get('text', '')

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Detect emotion from the text
    emotion = detect_emotion(user_text)
    
    # Find playlists based on emotion and keyword
    emotion_playlists = find_playlists_for_emotion(emotion)
    keyword_playlists = find_playlists_for_keyword(user_text)

    # Combine and randomize the playlists
    all_playlists = emotion_playlists + keyword_playlists
    random.shuffle(all_playlists)
    
    # Select up to 4 playlists
    selected_playlists = all_playlists[:4]

    response = {
        "playlists": selected_playlists
    }

    # Send callback if needed
    def send_callback(response):
        callback_message = {
            "apiVersion": "1.0",
            "service": "EmotionMusicPlayer",
            "datetime": datetime.datetime.now().isoformat(),
            "processDuration": 0,
            "taskId": str(uuid.uuid4()),
            "isResponseImmediate": True,
            "response": response,
            "errorCode": {
                "status": "SUCCESS",
                "reason": "Success"
            }
        }
        headers = {
            "Content-Type": "application/json",
            "x-request-id": str(uuid.uuid4()),
            "x-user-id": data.get('user_id', 'anonymous')
        }
        requests.post(webhook_url, json=callback_message, headers=headers)
    
    threading.Thread(target=send_callback, args=(response,)).start()

    return jsonify(response)

############### INDEX ROUTE ###############
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
