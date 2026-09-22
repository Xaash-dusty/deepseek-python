import os

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GOREST_TOKEN")

if TOKEN is None:
    raise SystemExit("GOREST_TOKEN не задан")


print("------------------------- Get without token #1 ----------------------")
try:
    r = requests.get("https://gorest.co.in/public/v2/users", timeout=5)
    r.raise_for_status()
    data = r.json()
except requests.exceptions.HTTPError as e:
    print(f"Error {e.response.status_code}")
else:
    print(f"Status: {r.status_code}")
    print(f"Всего пользователей: {len(data)}")
    print(f"Первый пользователь: {data[0]}")
    print(r.request.headers)

print("------------------------- Get without token #2 ----------------------")
try:
    r = requests.get("https://gorest.co.in/public/v2/users/1", timeout=5)
    r.raise_for_status()
    data = r.json()
except requests.exceptions.HTTPError as e:
    print(f"Error {e.response.status_code}")
else:
    print(f"Status: {r.status_code}")
    print(f"Имя пользователя: {data['name']}")

print("------------------------ Post without token -------------------------------")
try:
    r = requests.post(
        "https://gorest.co.in/public/v2/users",
        json={
            "name": "Xaash",
            "email": "xaash@example.com",
            "gender": "male",
            "status": "active",
        },
        timeout=5,
    )
    r.raise_for_status()
    data = r.json()
except requests.exceptions.HTTPError as e:
    print(f"Error {e.response.status_code}")
else:
    print(data)

headers = {"Authorization": f"Bearer {TOKEN}"}
print("------------------------ Post with token -------------------------------")
try:
    r = requests.post(
        "https://gorest.co.in/public/v2/users",
        json={
            "name": "Xaash",
            "email": "xaash1hf1uafjen23rkq@example.com",
            "gender": "male",
            "status": "active",
        },
        headers=headers,
        timeout=5,
    )
    r.raise_for_status()
    data = r.json()
    user_id = data["id"]
except requests.exceptions.HTTPError as e:
    print(f"Error {e.response.status_code}")
    print(e)
    print(f"Body: {e.response.text}")
else:
    print(f"Status: {r.status_code}")
    print(f"Data: {data}")
    print(f"Headers: {r.request.headers}")


try:
    r = requests.get(f"https://gorest.co.in/public/v2/users/{user_id}")
    r.raise_for_status()
    data = r.json()
    print(data)
except requests.exceptions.HTTPError as e:
    print(user_id)
    print(e.response.status_code)
