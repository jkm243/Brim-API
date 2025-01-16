
# API de Suppression de Fond d'Image (Background Remover)

Une API REST qui permet de supprimer automatiquement l'arrière-plan des images en utilisant le modèle d'intelligence artificielle RMBG-1.4.

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Déploiement](#-déploiement)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Tests](#-tests)
- [Dépannage](#-dépannage)

## ✨ Fonctionnalités

- Suppression automatique de l'arrière-plan des images
- Support des formats d'image courants (JPG, PNG)
- API REST simple à utiliser
- Traitement rapide avec support GPU (si disponible)

## 🚀 Installation

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd background-remover
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 💻 Déploiement

1. **Lancer l'API**
```bash
python BRIM/api_test.py
```
L'API sera accessible sur `http://localhost:5000`

2. **Variables d'environnement (optionnel)**
- `PORT` : Port du serveur (défaut: 5000)
- `HOST` : Hôte du serveur (défaut: 0.0.0.0)

## 🔌 Utilisation

### Endpoint API

**POST** `/api/segment`

#### Headers
```
Content-Type: application/json
```

#### Body
```json
{
    "image": "URL_DE_VOTRE_IMAGE"
}
```

#### Exemple de Réponse
```json
{
    "status": "success",
    "message": "Image traitée avec succès",
    "output_path": "/chemin/vers/image_sans_fond.png"
}
```

### Exemples d'Utilisation

#### Python
```python
import requests

url = "http://localhost:5000/api/segment"
data = {
    "image": "https://exemple.com/image.jpg"
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### PowerShell
```powershell
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "image" = "https://exemple.com/image.jpg"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/segment" -Method Post -Headers $headers -Body $body
```

## 📁 Structure du Projet

```
background-remover/
├── BRIM/
│   ├── api_test.py     # Serveur API principal
│   ├── test_api.py     # Tests de l'API
│   ├── test.py         # Tests standalone
│   └── app.py          # Application Flask
├── requirements.txt     # Dépendances
└── README.md           # Documentation
```

## 🧪 Tests

1. **Lancer les tests de l'API**
```bash
python BRIM/test_api.py
```

2. **Tester avec une image spécifique**
```bash
python BRIM/test.py
```

## 🔧 Dépannage

### Erreurs Courantes

1. **"torch" is not defined**
   - Solution: Vérifier l'installation de PyTorch
   ```bash
   pip install torch torchvision
   ```

2. **Erreur de CUDA**
   - Solution: Installer la version CPU de PyTorch si pas de GPU
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Port déjà utilisé**
   - Solution: Changer le port dans api_test.py ou arrêter le processus utilisant le port 5000

## ⚙️ Prérequis Techniques

- Python 3.8+
- RAM: 8GB minimum
- GPU: Recommandé pour de meilleures performances
- Espace disque: 2GB minimum
- Connexion Internet stable

## 📝 Notes

- Les images traitées sont temporairement stockées sur le serveur
- Le modèle utilise CUDA si disponible, sinon CPU
- Format de sortie: PNG avec canal alpha (transparence)

## 🤝 Support

Pour toute question ou problème :
1. Consulter la section Dépannage
2. Ouvrir une issue sur GitHub
3. Contacter l'équipe de support

## 📄 Licence

[Votre licence]
```
