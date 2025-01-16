import requests
#import json

# URL de l'API
url = "http://localhost:5000/api/segment"

# Données à envoyer
data = {
    "image": "https://cdn1.ozone.ru/s3/multimedia-h/6721119629.jpg"
}

# Envoi de la requête
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)

# Affichage du résultat
print("Status Code:", response.status_code)
print("Réponse:", response.json()) 