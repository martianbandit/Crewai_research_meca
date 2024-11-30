from typing import List, Optional, Dict
import os
from datetime import datetime
from PIL import Image
import io
import base64
from pathlib import Path
import cv2
import numpy as np
from supabase import create_client, Client

class ImageManager:
    """Gestionnaire pour le traitement et le stockage des images"""

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.image_bucket = "vehicle-images"
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        self.max_size = 10 * 1024 * 1024  # 10MB
        self.thumbnail_size = (800, 600)

    async def save_vehicle_image(self, 
                               vehicle_id: str, 
                               image_data: bytes, 
                               category: str,
                               description: str = None) -> Dict:
        """Sauvegarde une image de véhicule"""
        try:
            # Validation et prétraitement
            image = Image.open(io.BytesIO(image_data))
            
            # Création du thumbnail
            image.thumbnail(self.thumbnail_size)
            
            # Génération du nom de fichier
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{vehicle_id}_{category}_{timestamp}.jpg"
            
            # Conversion en JPEG et compression
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=85, optimize=True)
            compressed_data = buffer.getvalue()
            
            # Upload vers Supabase Storage
            file_path = f"{vehicle_id}/{category}/{filename}"
            self.supabase.storage.from_(self.image_bucket).upload(
                file_path,
                compressed_data
            )
            
            # Enregistrement des métadonnées
            metadata = {
                "vehicle_id": vehicle_id,
                "category": category,
                "description": description,
                "filename": filename,
                "file_path": file_path,
                "size": len(compressed_data),
                "created_at": datetime.now().isoformat()
            }
            
            self.supabase.table("vehicle_images").insert(metadata).execute()
            
            return metadata
            
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde de l'image: {str(e)}")

    async def get_vehicle_images(self, 
                               vehicle_id: str, 
                               category: Optional[str] = None) -> List[Dict]:
        """Récupère les images d'un véhicule"""
        try:
            query = self.supabase.table("vehicle_images").select("*").eq("vehicle_id", vehicle_id)
            
            if category:
                query = query.eq("category", category)
                
            response = query.execute()
            return response.data
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des images: {str(e)}")

    async def analyze_damage(self, image_data: bytes) -> Dict:
        """Analyse les dommages sur une image"""
        try:
            # Conversion en format OpenCV
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Prétraitement
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Détection des contours
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyse des anomalies
            damages = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filtrer les petits contours
                    x, y, w, h = cv2.boundingRect(contour)
                    damages.append({
                        "position": {"x": x, "y": y},
                        "size": {"width": w, "height": h},
                        "area": area,
                        "severity": "high" if area > 1000 else "medium" if area > 500 else "low"
                    })
            
            return {
                "damages_detected": len(damages),
                "damage_areas": damages,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse de l'image: {str(e)}")

    async def extract_text_from_image(self, image_data: bytes) -> str:
        """Extrait le texte d'une image (par exemple, pour les plaques d'immatriculation)"""
        try:
            # Utilisation de Tesseract OCR
            import pytesseract
            
            # Conversion de l'image
            image = Image.open(io.BytesIO(image_data))
            
            # Prétraitement pour améliorer l'OCR
            image = image.convert('L')  # Conversion en niveaux de gris
            
            # Extraction du texte
            text = pytesseract.image_to_string(image)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")

    def create_image_grid(self, image_paths: List[str], grid_size: tuple = (2, 2)) -> bytes:
        """Crée une grille d'images pour la visualisation"""
        try:
            rows, cols = grid_size
            cell_size = (800 // cols, 600 // rows)
            
            # Création de l'image finale
            final_image = Image.new('RGB', (800, 600))
            
            for idx, path in enumerate(image_paths[:rows * cols]):
                row = idx // cols
                col = idx % cols
                
                # Chargement et redimensionnement de l'image
                img_data = self.supabase.storage.from_(self.image_bucket).download(path)
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail(cell_size)
                
                # Placement dans la grille
                x = col * cell_size[0]
                y = row * cell_size[1]
                final_image.paste(img, (x, y))
            
            # Conversion en bytes
            buffer = io.BytesIO()
            final_image.save(buffer, format="JPEG")
            return buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création de la grille d'images: {str(e)}")

    def generate_report_with_images(self, 
                                  work_order_id: str, 
                                  images: List[Dict],
                                  template: str = "default") -> bytes:
        """Génère un rapport PDF avec les images"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            
            # En-tête du rapport
            c.drawString(100, 750, f"Rapport d'Inspection - Bon de travail #{work_order_id}")
            c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
            
            y_position = 700
            for img_data in images:
                # Ajout de l'image
                img_path = img_data["file_path"]
                img_bytes = self.supabase.storage.from_(self.image_bucket).download(img_path)
                img = Image.open(io.BytesIO(img_bytes))
                
                # Redimensionnement pour le PDF
                img.thumbnail((400, 300))
                img_path_temp = f"temp_{img_data['filename']}"
                img.save(img_path_temp)
                
                c.drawImage(img_path_temp, 100, y_position - 300)
                c.drawString(100, y_position - 320, f"Catégorie: {img_data['category']}")
                c.drawString(100, y_position - 340, f"Description: {img_data['description']}")
                
                os.remove(img_path_temp)
                y_position -= 400
                
                if y_position < 100:
                    c.showPage()
                    y_position = 700
            
            c.save()
            return buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport: {str(e)}")
