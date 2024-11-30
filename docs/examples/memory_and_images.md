# Exemples d'Utilisation - Mémoire et Images

## Gestion de la Mémoire

### Initialisation
```python
from app.memory.memo_manager import MemoManager
from app.database.supabase_manager import SupabaseManager

# Initialisation
memo_manager = MemoManager()
```

### Utilisation avec les Bons de Travail
```python
# Récupération d'un bon de travail (mise en cache automatique)
work_order = await memo_manager.get_work_order("wo_123")

# Récupération de tous les bons d'un véhicule
vehicle_orders = await memo_manager.get_work_orders_by_vehicle("vehicle_456")

# Invalidation du cache après modification
memo_manager.invalidate_work_order_cache("wo_123")
```

### Gestion des Pièces
```python
# Récupération des pièces compatibles
parts = await memo_manager.get_parts_by_vehicle("vehicle_456")

# Récupération d'une pièce spécifique
part = await memo_manager.get_part("part_789")

# Invalidation du cache des pièces
memo_manager.invalidate_part_cache("part_789")
```

## Gestion des Images

### Initialisation
```python
from app.utils.image_manager import ImageManager
from supabase import create_client

# Configuration Supabase
supabase = create_client(
    supabase_url="VOTRE_URL",
    supabase_key="VOTRE_CLE"
)

# Initialisation
image_manager = ImageManager(supabase)
```

### Sauvegarde d'Images
```python
# Lecture d'une image
with open("photo_dommage.jpg", "rb") as f:
    image_data = f.read()

# Sauvegarde avec métadonnées
metadata = await image_manager.save_vehicle_image(
    vehicle_id="vehicle_456",
    image_data=image_data,
    category="damage_inspection",
    description="Dommage pare-choc avant droit"
)
```

### Analyse de Dommages
```python
# Analyse automatique des dommages
damage_analysis = await image_manager.analyze_damage(image_data)

print(f"Nombre de zones endommagées : {damage_analysis['damages_detected']}")
for damage in damage_analysis['damage_areas']:
    print(f"Dommage détecté : {damage['severity']}")
```

### Extraction de Texte
```python
# Lecture d'une image de plaque
with open("plaque.jpg", "rb") as f:
    plate_image = f.read()

# Extraction du numéro
plate_number = await image_manager.extract_text_from_image(plate_image)
print(f"Plaque détectée : {plate_number}")
```

### Génération de Rapports
```python
# Récupération des images d'un véhicule
images = await image_manager.get_vehicle_images(
    vehicle_id="vehicle_456",
    category="inspection"
)

# Création d'une grille d'images
grid = image_manager.create_image_grid(
    image_paths=[img["file_path"] for img in images],
    grid_size=(2, 2)
)

# Génération d'un rapport PDF
pdf_data = image_manager.generate_report_with_images(
    work_order_id="wo_123",
    images=images
)

# Sauvegarde du rapport
with open("rapport_inspection.pdf", "wb") as f:
    f.write(pdf_data)
```

## Cas d'Utilisation Complet

### Inspection avec Photos
```python
async def process_inspection(vehicle_id: str, mechanic_id: str):
    # Création du bon de travail
    work_order = {
        "vehicle_id": vehicle_id,
        "mechanic_id": mechanic_id,
        "type": "inspection",
        "status": "en_cours"
    }
    
    # Sauvegarde avec mise en cache
    saved_order = await memo_manager.get_work_order(work_order["id"])
    
    # Traitement des photos
    inspection_photos = []
    for photo in photos:
        # Sauvegarde de la photo
        metadata = await image_manager.save_vehicle_image(
            vehicle_id=vehicle_id,
            image_data=photo["data"],
            category=photo["category"],
            description=photo["description"]
        )
        
        # Analyse des dommages si nécessaire
        if photo["category"] == "damage":
            analysis = await image_manager.analyze_damage(photo["data"])
            metadata["damage_analysis"] = analysis
        
        inspection_photos.append(metadata)
    
    # Génération du rapport
    report = image_manager.generate_report_with_images(
        work_order_id=work_order["id"],
        images=inspection_photos
    )
    
    return {
        "work_order": saved_order,
        "photos": inspection_photos,
        "report": report
    }
```

## Bonnes Pratiques

1. **Gestion de la Mémoire**
   - Utilisez des durées de cache appropriées
   - Invalidez le cache lors des modifications
   - Surveillez l'utilisation de la mémoire

2. **Traitement d'Images**
   - Compressez les images avant stockage
   - Utilisez des thumbnails pour l'affichage
   - Gérez les formats supportés

3. **Stockage**
   - Organisez les images par catégorie
   - Sauvegardez les métadonnées
   - Implémentez une politique de rétention

4. **Sécurité**
   - Validez les types de fichiers
   - Limitez la taille des uploads
   - Gérez les permissions d'accès
