# File to store functions the genai can use as tools
import json
import requests
import datetime

def get_wikipedia_summary(topic: str):
    """Fetches the summary of a Wikipedia article."""
    try:
        endpoint = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": topic,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
        }
        headers = {
            'User-Agent': 'MyChatbot/1.0'
        }
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        
        # Check if the extract key exists
        if 'extract' in page and page['extract']:
            return json.dumps({"topic": page.get("title", topic), "summary": page['extract']})
        else:
            return json.dumps({"error": f"Could not find a Wikipedia summary for '{topic}'."})
            
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_current_datetime(timezone_str: str = "UTC"):
    """
    Gets the current date and time for a given timezone.
    If no timezone is provided, it defaults to UTC.
    """
    try:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        
        if timezone_str.upper() == "PST":
            offset = datetime.timedelta(hours=-8)
            tz = datetime.timezone(offset)
            final_time = now_utc.astimezone(tz)
        elif timezone_str.upper() == "EST":
            offset = datetime.timedelta(hours=-5)
            tz = datetime.timezone(offset)
            final_time = now_utc.astimezone(tz)
        else:
            final_time = now_utc

        return json.dumps({"datetime": final_time.isoformat()})
    except Exception as e:
        return json.dumps({"error": str(e)})


def calculate_expression(expression: str):
    """
    Calculates a mathematical expression safely.
    Supports basic arithmetic operators: +, -, *, /.
    """
    try:
        allowed_chars = "0123456789.+-*/() "
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Expression contains invalid characters.")
        
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_random_joke():
    """Fetches a random programming joke."""
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status() 
        joke = response.json()
        return json.dumps({"setup": joke['setup'], "punchline": joke['punchline']})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_public_ip_address():
    """Gets the public IP address of the machine running the code."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return json.dumps(response.json())
    except Exception as e:
        return json.dumps({"error": str(e)})