import yaml
import requests
import time
import logging   # Imported logging for file logging 
from collections import defaultdict
from urllib.parse import urlparse  #Imported URLPARSE to correctly extract domain without the port number


# Configure logging to write results to a file (availability.log)
logging.basicConfig(filename='availability.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper() # Make the Default to GET method if not provided
    headers = endpoint.get('headers', {})  #Used empty headers if not provided
    body = endpoint.get('body')

    try:
        start = time.time()  #start timing the request
        response = requests.request(method, url, headers=headers, json=body, timeout=0.5) #Added 0.5s timeout per requirements
        duration = (time.time() - start) * 1000  # we can convert this to ms

        if 200 <= response.status_code < 300 and duration <= 500: #Endpoint is UP only if status is between 200 and 299 AND duration is <= 500ms
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = urlparse(endpoint["url"]).hostname # We can ignore port numbers when calculating domain
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            message = f"{domain} has {availability}% availability"
            print(message) #prints to terminal
            logging.info(message) #logs the result to logging file (availibility.log)

        print("---")
        time.sleep(15) #runs every 15 sec as required

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")