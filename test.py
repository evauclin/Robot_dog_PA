import requests


def test_app():
    # URL de l'API
    url = "http://0.0.0.0:80/upload"
    url_vm = "http://52.212.87.244:80/upload"

    file_path = "Capture d'écran 25 avril 2024.jpg"
    files = {"image": open(file_path, "rb")}
    headers = {"accept": "application/json"}
    response = requests.post(url_vm, files=files, headers=headers)
    assert response.status_code == 200
