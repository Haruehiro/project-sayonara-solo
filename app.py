from flask import Flask, jsonify, redirect, render_template
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Function to read API key from file
def read_api_key(filepath):
    with open(filepath, 'r') as file:
        return file.readline().strip()
    
# Alt method to read API
# Uncomment this if you want to use the environment variable instead of a file
#MYANIMELIST_CLIENT_ID = os.environ.get('MYANIMELIST_CLIENT_ID')


# Path to your API key file
# Comment this if you want to use the environment variable instead of a file
api_key_file = '/srv/applist/api_key.txt'
MYANIMELIST_CLIENT_ID = read_api_key(api_key_file)

# Get the seasons based on the current month
def get_current_season():
    month = datetime.now().month
    if 1 <= month <= 3:
        return "winter"
    elif 4 <= month <= 6:
        return "spring"
    elif 7 <= month <= 9:
        return "summer"
    elif 10 <= month <= 12:
        return "fall"

# Function to fetch all pages of data from the MyAnimeList API
def fetch_all_pages(initial_url, headers):
    all_data = []
    url = initial_url
    while url:  # Loop until there are no more pages
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            all_data.extend(data['data'])  # Add the data from the current page to all_data
            url = data['paging'].get('next')  # Get the URL for the next page
        else:
            break  # Stop fetching if there's an error
    return all_data

# Route to redirect the base URL to the current season's anime list
@app.route('/')
def home():
    return redirect('/current-season')

# Route to display the current season's anime
from flask import request

# Route to display the current season's anime with pagination
@app.route('/current-season')
def current_season_anime():
    year = datetime.now().year
    season = get_current_season()
    page = request.args.get('page', 1, type=int)  # Get page from query string, default to 1
    limit = 10  # Define the limit of items per page

    # Adjust the URL to include page offset based on the current page
    offset = (page - 1) * limit
    url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season}?limit={limit}&offset={offset}"
    headers = {'X-MAL-CLIENT-ID': MYANIMELIST_CLIENT_ID}

    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()['data']
        # Check if there's a next page
        has_next = 'next' in response.json().get('paging', {})
        # Determine if the "Previous" button should be shown
        has_previous = page > 1

        # Pass data along with pagination flags and current page to the template
        return render_template('anime_list.html', data=data, season=season, year=year, has_next=has_next, has_previous=has_previous, current_page=page)
    else:
        return f"Could not fetch data from MyAnimeList API, status code: {response.status_code}"

#if __name__ == '__main__':
#    app.run(debug=False) # Switching this to fasle since it seems to work and we shouldnt leave it enabled unless we are failing to pull data.
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
