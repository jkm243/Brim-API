"""
API de segmentation d'images pour la suppression de fond

Cette API permet de supprimer automatiquement l'arrière-plan d'une image en utilisant
le modèle RMBG-1.4 de BriaAI.

Endpoint:
    POST /api/segment

Format de la requête:
    Content-Type: application/json
    Body: {
        "image": "url_de_l_image"  # URL de l'image à traiter
    }

Réponse:
    Format: JSON
    Succès (200):
        {
            "success": true,
            "image": "base64_de_l_image_sans_fond" 
        }
    Erreur (400):
        {
            "error": "Message d'erreur"
        }

Exemple d'utilisation:
    curl -X POST http://localhost:5000/api/segment \\
         -H "Content-Type: application/json" \\
         -d '{"image": "https://cdn1.ozone.ru/s3/multimedia-h/6721119629.jpg"}'
"""

from transformers import AutoModelForImageSegmentation
from torchvision.transforms.functional import normalize
import numpy as np
import torch
import torch.nn.functional as F
from skimage import io
from PIL import Image
import os
from flask import Flask, request, jsonify
import requests
from io import BytesIO

app = Flask(__name__)

# Charger le modèle une seule fois au démarrage
model = AutoModelForImageSegmentation.from_pretrained("briaai/RMBG-1.4",trust_remote_code=True)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

def preprocess_image(im: np.ndarray, model_input_size: list) -> torch.Tensor:
    if len(im.shape) < 3:
        im = im[:, :, np.newaxis]
    im_tensor = torch.tensor(im, dtype=torch.float32).permute(2,0,1)
    im_tensor = F.interpolate(torch.unsqueeze(im_tensor,0), size=model_input_size, mode='bilinear')
    image = torch.divide(im_tensor,255.0)
    image = normalize(image,[0.5,0.5,0.5],[1.0,1.0,1.0])
    return image

def postprocess_image(result: torch.Tensor, im_size: list)-> np.ndarray:
    result = torch.squeeze(F.interpolate(result, size=im_size, mode='bilinear') ,0)
    ma = torch.max(result)
    mi = torch.min(result)
    result = (result-mi)/(ma-mi)
    im_array = (result*255).permute(1,2,0).cpu().data.numpy().astype(np.uint8)
    im_array = np.squeeze(im_array)
    return im_array

@app.route('/api/segment', methods=['POST'])
def segment_image():
    try:
        # Récupérer l'URL de l'image depuis la requête JSON
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'URL de l\'image non fournie'}), 400
            
        image_url = data['image']
        
        # Télécharger l'image depuis l'URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Convertir l'image en array numpy
        orig_im = np.array(img)
        orig_im_size = orig_im.shape[0:2]
        
        # Prétraitement
        model_input_size = [1024, 1024]
        image = preprocess_image(orig_im, model_input_size).to(device)
        
        # Inférence
        result = model(image)
        
        # Post-traitement
        result_image = postprocess_image(result[0][0], orig_im_size)
        
        # Créer l'image sans fond
        pil_mask_im = Image.fromarray(result_image)
        no_bg_image = img.copy()
        no_bg_image.putalpha(pil_mask_im)
        
        # Sauvegarder temporairement et retourner le chemin
        output_path = f"temp_{np.random.randint(1000,9999)}.png"
        no_bg_image.save(output_path)
        
        return jsonify({
            'status': 'success',
            'message': 'Image traitée avec succès',
            'output_path': os.path.abspath(output_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
