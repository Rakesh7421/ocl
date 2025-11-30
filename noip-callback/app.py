from flask import Flask, request, jsonify, render_template
import datetime
import os
import threading
import requests
from noip_update import update_noip
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("NOIP_HOST")

app = Flask(__name__, template_folder='template')

startup_executed = False     # Ensures startup code runs only once


def curl_test(domain):
    try:
        response = requests.head(domain, timeout=10)
        headers_str = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        return f"HTTP/1.1 {response.status_code} {response.reason}\n{headers_str}"
    except requests.exceptions.ConnectTimeout:
        return "requests error: Connection timed out - this may be due to NAT loopback not supported by your router. The service may still be accessible from outside."
    except Exception as e:
        return f"requests error: {e}"


def startup_tasks():
    """Runs NO-IP update + HTTP tests"""
    global startup_executed
    if startup_executed:
        return
    startup_executed = True

    print("\n=== STARTUP: Updating NO-IP ===")
    update_res = update_noip()
    print("NO-IP update result:", update_res)

    print("\n=== STARTUP: HTTP test (localhost) ===")
    curl_res_local = curl_test("http://localhost:8080")
    print(curl_res_local)

    print("\n=== STARTUP: HTTP test (domain) ===")
    curl_res_domain = curl_test(f"http://{HOST}:8080")
    print(curl_res_domain)
    print("================================\n")


@app.before_request
def trigger_startup():
    """Run startup tasks only once using a separate thread."""
    if not startup_executed:
        threading.Thread(target=startup_tasks).start()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/callback", methods=["GET", "POST"])
def callback():
    data = request.args if request.method == "GET" else request.form
    timestamp = datetime.datetime.now()

    log = f"\n[{timestamp}] Callback Received:\n{data}\n"
    print(log)

    with open("callback_log.txt", "a") as f:
        f.write(log)

    return {"status": "ok", "received": data}


@app.route("/update-noip")
def manual_update():
    update_res = update_noip()
    curl_res = curl_test(f"http://{HOST}:8080")

    return jsonify({
        "noip_update": update_res,
        "curl_test": curl_res
    })


if __name__ == "__main__":
    # Thread-safe startup for Flask 3.x
    threading.Thread(target=startup_tasks).start()

    app.run(host="0.0.0.0", port=8080)
