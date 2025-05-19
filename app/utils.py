import json
import os
import requests

def fetch_meme_templates():
    try:
        # Check if the file exists and is not empty
        if os.path.exists("templates.json") and os.path.getsize("templates.json") > 0:
            with open("templates.json", "r") as file:
                return json.load(file)
        response = requests.get("https://api.memegen.link/templates")
        if response.status_code == 200:
            # write the response to a file
            with open("templates.json", "w") as file:
                file.write(response.text)
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching templates: {e}")
        return []
