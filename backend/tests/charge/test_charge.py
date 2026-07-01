import requests
import threading
import time

URL = "http://localhost:8000/api/chat"

payload = {
    "prompt": "C'est quoi la jungle ?",
    "character": "ornn",
}

def send_request():
    start = time.time()
    try:
        r = requests.post(URL, json=payload)
        latency = time.time() - start
        print(f"Status: {r.status_code} - {latency:.2f}s")
    except Exception as e:
        print("Erreur:", e)

threads = []

# 50 utilisateurs simultanés
for i in range(50):
    t = threading.Thread(target=send_request)
    threads.append(t)
    t.start()

for t in threads:
    t.join()