from flask import Flask, request, g, render_template, redirect, jsonify
import requests
import time
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Function to read API key from file
def read_api_key(filepath):
    with open(filepath, 'r') as file:
        return file.readline().strip()
    
# Setup for logging
logging.basicConfig(filename='sayonarakuso.log', level=logging.INFO)

# Alt method to read API
# Uncomment this if you want to use the environment variable instead of a file
#MYANIMELIST_CLIENT_ID = os.environ.get('MYANIMELIST_CLIENT_ID')


# Path to your API key file
# Comment this if you want to use the environment variable instead of a file
api_key_file = '/srv/applist/api_key.txt'

# Kept this here for consistancy.
#MYANIMELIST_CLIENT_ID = read_api_key(api_key_file)

# Rate Limiter function. One request per second, per IP
def rate_limiter():
    """Simple rate limiter: one request per second per client IP."""
    client_ip = request.remote_addr
    last_request = g.get('last_request', {})
    current_time = time.time()

    if client_ip in last_request and current_time - last_request[client_ip] < 1:
        return False  # Block the request

    last_request[client_ip] = current_time
    g.last_request = last_request
    return True

# Return for rate limit exceed
@app.before_request
def before_request_func():
    if not rate_limiter():
        return "Rate limit exceeded. Please wait a moment before trying again.", 429
    
# Version 2 of current-season on JikanAPI
# No need for get_current_season function since Jikan directly provides the current season's anime

@app.route('/')
def home():
    return redirect('/current-season')

@app.route('/current-season')
def current_season_anime():
    page = request.args.get('page', 1, type=int)  # Get page from query string, default to 1
    limit = 10  # Limit of items per page, adjust as needed

    # Jikan API endpoint for the current season with pagination
    url = f"https://api.jikan.moe/v4/seasons/now?page={page}&limit={limit}"

    response = requests.get(url)
    if response.ok:
        data = response.json()['data']
        pagination = response.json().get('pagination', {})
        has_next = pagination.get('has_next_page', False)
        has_previous = page > 1

        return render_template('anime_list.html', anime_data=data, has_next=has_next, has_previous=has_previous, current_page=page)
    else:
        return f"Could not fetch data from Jikan API, status code: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)