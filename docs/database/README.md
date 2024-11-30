# Documentation Base de Données

## Schéma de la Base de Données

La base de données utilise PostgreSQL avec les extensions suivantes :
- uuid-ossp (pour la génération d'UUID)
- jsonb (pour les données JSON)

## Tables Principales

### vehicles
Stocke les informations sur les véhicules
- id (UUID, PK)
- make (VARCHAR)
- model (VARCHAR)
- year (INTEGER)
- vin (VARCHAR, UNIQUE)
- license_plate (VARCHAR)

### mechanics
Informations sur les mécaniciens
- id (UUID, PK)
- first_name (VARCHAR)
- last_name (VARCHAR)
- email (VARCHAR, UNIQUE)
- specialization (VARCHAR[])
- certification_level (VARCHAR)

### parts
Catalogue des pièces
- id (UUID, PK)
- name (VARCHAR)
- part_number (VARCHAR, UNIQUE)
- manufacturer (VARCHAR)
- category (VARCHAR)
- compatible_vehicles (JSONB)
- price_range (JSONB)

### work_orders
Bons de travail
- id (UUID, PK)
- vehicle_id (UUID, FK)
- mechanic_id (UUID, FK)
- status (VARCHAR)
- description (TEXT)
- diagnosis (TEXT)
- estimated_hours (DECIMAL)
- estimated_cost (DECIMAL)

### maintenance_history
Historique des maintenances
- id (UUID, PK)
- vehicle_id (UUID, FK)
- work_order_id (UUID, FK)
- service_type (VARCHAR)
- mileage (INTEGER)
- service_date (DATE)
- next_service_date (DATE)

### diagnostics
Diagnostics et analyses
- id (UUID, PK)
- work_order_id (UUID, FK)
- symptoms (TEXT[])
- diagnostic_codes (TEXT[])
- ai_analysis (TEXT)
- recommended_actions (TEXT[])
- confidence_score (DECIMAL)

### suppliers
Informations sur les fournisseurs
- id (UUID, PK)
- name (VARCHAR)
- contact_info (JSONB)
- address (JSONB)
- parts_catalog (JSONB)
- rating (DECIMAL)

## Scripts SQL

1. [init.sql](init.sql)
   - Création des tables
   - Index
   - Triggers
   - Contraintes

2. [sample_data.sql](sample_data.sql)
   - Données d'exemple
   - Cas d'utilisation

## Maintenance

### Sauvegardes
Les sauvegardes sont automatisées quotidiennement via Supabase.

### Migrations
Utilisez les outils de migration Supabase pour les mises à jour de schéma.

### Performance
Des index sont créés sur les colonnes fréquemment utilisées :
- vehicles(vin)
- work_orders(vehicle_id, mechanic_id)
- maintenance_history(vehicle_id)
- diagnostics(work_order_id)

## Sécurité

- Authentification via Supabase Auth
- Chiffrement des données sensibles
- Politiques RLS (Row Level Security)
- Audit logs activés
