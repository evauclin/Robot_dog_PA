import requests

# URL de l'API
url = 'http://127.0.0.1:8000/upload'
url_vm = 'http://34.245.54.151:80/upload'

# Chemin vers l'image que vous souhaitez envoyer
file_path = 'app/ReferenceImages/test.jpg'

# Création du payload pour l'envoi de l'image
files = {'image': open(file_path, 'rb')}

# En-têtes de la requête
headers = {'accept': 'application/json'}

# Envoi de la requête POST avec le payload et les en-têtes spécifiés
response = requests.post(url_vm, files=files, headers=headers)

# Affichage de la réponse
print(response.text)
