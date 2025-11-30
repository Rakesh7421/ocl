import requests
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("NOIP_USERNAME")
PASS = os.getenv("NOIP_PASSWORD")
HOST = os.getenv("NOIP_HOST")

def update_noip():
    url = f"https://dynupdate.no-ip.com/nic/update?hostname={HOST}"
    response = requests.get(url, auth=(USER, PASS))
    print("NO-IP Response:", response.text)
    return response.text

if __name__ == "__main__":
    update_noip()
