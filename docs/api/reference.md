# API Reference - Assistant Mécanique Pro

## Vue d'Ensemble

L'API Assistant Mécanique Pro suit les principes REST et utilise JSON pour les requêtes et réponses.

Base URL : `https://api.assistant-mecanique.com/v1`

## Authentification

```bash
curl -X POST https://api.assistant-mecanique.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
```

Réponse :
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## Endpoints

### Véhicules

#### GET /vehicles
Liste tous les véhicules

```bash
curl https://api.assistant-mecanique.com/v1/vehicles \
  -H "Authorization: Bearer eyJ..."
```

Réponse :
```json
{
  "vehicles": [
    {
      "id": "uuid",
      "make": "Volvo",
      "model": "VNL 860",
      "year": 2020,
      "vin": "4V4NC9EH6LN123456"
    }
  ]
}
```

#### POST /vehicles
Ajoute un nouveau véhicule

```bash
curl -X POST https://api.assistant-mecanique.com/v1/vehicles \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Freightliner",
    "model": "Cascadia",
    "year": 2019,
    "vin": "3AKJHHDR9KSLA4567"
  }'
```

### Bons de Travail

#### GET /work-orders
Liste les bons de travail

Paramètres :
- `status` : Filtrer par statut
- `vehicle_id` : Filtrer par véhicule
- `mechanic_id` : Filtrer par mécanicien

```bash
curl https://api.assistant-mecanique.com/v1/work-orders?status=en_cours \
  -H "Authorization: Bearer eyJ..."
```

#### POST /work-orders
Crée un nouveau bon de travail

```bash
curl -X POST https://api.assistant-mecanique.com/v1/work-orders \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "uuid",
    "description": "Maintenance préventive",
    "estimated_hours": 4.5
  }'
```

### Diagnostic AI

#### POST /diagnostic
Analyse des symptômes

```bash
curl -X POST https://api.assistant-mecanique.com/v1/diagnostic \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "uuid",
    "symptoms": ["bruit_moteur", "vibrations"],
    "context": {
      "mileage": 150000,
      "last_service": "2023-01-15"
    }
  }'
```

### Pièces

#### GET /parts/search
Recherche de pièces

Paramètres :
- `q` : Terme de recherche
- `make` : Marque du véhicule
- `model` : Modèle
- `year` : Année
- `category` : Catégorie de pièce

```bash
curl https://api.assistant-mecanique.com/v1/parts/search?q=filtre%20huile&make=Volvo \
  -H "Authorization: Bearer eyJ..."
```

## Webhooks

### POST /webhooks/parts-availability
Notification de disponibilité des pièces

```json
{
  "part_id": "uuid",
  "status": "available",
  "supplier": "Pièces Pro Plus",
  "price": 299.99,
  "quantity": 5
}
```

## Erreurs

| Code | Description |
|------|-------------|
| 400  | Requête invalide |
| 401  | Non authentifié |
| 403  | Non autorisé |
| 404  | Ressource non trouvée |
| 429  | Trop de requêtes |
| 500  | Erreur serveur |

Exemple d'erreur :
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Le VIN spécifié n'est pas valide",
    "details": {
      "field": "vin",
      "value": "123"
    }
  }
}
```

## Limites

- Rate limit : 1000 requêtes/heure
- Taille max requête : 10MB
- Timeout : 30 secondes

## Versions

| Version | Statut | EOL |
|---------|--------|-----|
| v1      | Stable | - |
| v0      | Deprecated | 2024-12-31 |

## SDK

Des SDK sont disponibles pour :
- Python
- JavaScript
- PHP
- Java

Exemple Python :
```python
from assistant_mecanique import Client

client = Client("votre-api-key")
vehicles = client.vehicles.list()
```

## Support

- Email : api-support@assistant-mecanique.com
- Documentation : https://docs.assistant-mecanique.com
- Status : https://status.assistant-mecanique.com
