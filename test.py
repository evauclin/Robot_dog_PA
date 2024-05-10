import requests


def test_app():
    # URL de l'API
    url = "http://0.0.0.0:80/upload"
    url_vm = "http://18.201.12.192:80/upload"

    file_path = "Capture d'écran 25 avril 2024.jpg"
    files = {"image": open(file_path, "rb")}
    headers = {"accept": "application/json"}
    response = requests.post(url, files=files, headers=headers)
    assert response.status_code == 200


url = "http://0.0.0.0:80/upload"
url_vm = "http://18.201.12.192:80/upload"

file_path = "Capture d'écran 25 avril 2024.jpg"
files = {"image": open(file_path, "rb")}
headers = {"accept": "application/json"}
print("Sending request to the API")
response = requests.post(url_vm, files=files, headers=headers)
print("Response received")
name = response.json()["name"]
distance = response.json()["distance"]
message = response.json()["message"]
print(name, distance, message)
