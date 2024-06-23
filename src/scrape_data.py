import os
import requests
import json

def scrape(client_id, bearer_token):
    # Define the base URL
    base_url = f"https://app.truecoach.co/proxy/api/clients/{client_id}/workouts"

    # Define the headers
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Authorization": f"Bearer {bearer_token}",
        "Role": "Client",
    }

    # Define the parameters
    params = {
        "order": "desc",
        "per_page": 10,
        "states": "completed,missed"
    }

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Get the path to the 'data' directory
    data_dir = os.path.join(script_dir, '..', 'data')

    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Scrape the data from the API
    page = 1
    while True:
        params["page"] = page
        response = requests.get(base_url, headers=headers, params=params)

        if response.json()['meta']['total_pages'] == page - 1:
            break

        file_path = os.path.join(data_dir, f'page{page}.json')
        with open(file_path, 'w') as file:
            json.dump(response.json(), file)
        page += 1

if __name__ == "__main__":
    scrape()