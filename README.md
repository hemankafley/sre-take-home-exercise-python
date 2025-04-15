# Fetch Take Home Exercise – SRE Endpoint Monitoring

This script monitors the availability of a list of HTTP endpoints defined in a YAML configuration file. It checks their status and response time every 15 seconds and prints the overall availability percentage by domain.

---

## Requirements

- Python 3.7 or newer
- Install the required Python packages:

```bash
pip install requests pyyaml
```

---

## How to Run

1. Prepare a YAML file containing your endpoints (see format below).
2. Run the script from the command line:

```bash
python main.py config.yaml
```

Replace `config.yaml` with the path to your actual configuration file.

To stop the script, press Ctrl + C.

---

## YAML Configuration Format

```yaml
- name: sample POST
  url: https://example.com/body
  method: POST
  headers:
    content-type: application/json
  body: '{"foo":"bar"}'

- name: sample GET
  url: https://example.com/
```

Field explanations:

- `name`: A label for the check.
- `url`: Full URL of the endpoint.
- `method`: HTTP method to use (optional, defaults to GET).
- `headers`: Any custom headers (optional).
- `body`: Request body for POST/PUT (optional).

---

## Output

The script prints and logs messages like the following every 15 seconds:

```
example.com has 90% availability
---
```

Results are also saved in a log file called `availability.log`.

---

## Changes Made from the Original Code

1. Defaulted the HTTP method to 'GET' if not provided.
2. Ensured HTTP methods are uppercase using .upper().
3. Used urlparse to extract the hostname (ignoring port) for consistent domain tracking.
4. Added a timeout of 0.5 seconds to all requests.
5. An endpoint is only considered "UP" if:
   - The HTTP status code is in the 2xx range.
   - The response time is less than or equal to 500 milliseconds.
6. Used headers = {} as default if headers are not specified.
7. Added logging to availability.log for all availability updates.
