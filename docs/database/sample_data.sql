-- Insertion de données d'exemple

-- Véhicules
INSERT INTO vehicles (make, model, year, vin, license_plate) VALUES
('Volvo', 'VNL 860', 2020, '4V4NC9EH6LN123456', 'ABC123'),
('Freightliner', 'Cascadia', 2019, '3AKJHHDR9KSLA4567', 'XYZ789'),
('Peterbilt', '579', 2021, '1XPWD40X1MD654321', 'DEF456');

-- Mécaniciens
INSERT INTO mechanics (first_name, last_name, email, phone, specialization, certification_level) VALUES
('Jean', 'Dupont', 'jean.dupont@mechanic.com', '+33123456789', ARRAY['Moteur', 'Transmission'], 'Expert'),
('Marie', 'Martin', 'marie.martin@mechanic.com', '+33987654321', ARRAY['Électrique', 'Diagnostic'], 'Senior'),
('Pierre', 'Bernard', 'pierre.bernard@mechanic.com', '+33567891234', ARRAY['Freins', 'Suspension'], 'Intermédiaire');

-- Pièces
INSERT INTO parts (name, part_number, description, manufacturer, category, compatible_vehicles, price_range) VALUES
('Filtre à huile', 'VOL123456', 'Filtre à huile haute performance', 'Volvo', 'Filtration',
 '{"models": ["VNL 860", "VNL 780"]}', '{"min": 25.99, "max": 45.99}'),
('Plaquettes de frein', 'FRL789012', 'Plaquettes de frein longue durée', 'Freightliner', 'Freinage',
 '{"models": ["Cascadia", "Century"]}', '{"min": 89.99, "max": 129.99}'),
('Alternateur', 'PET345678', 'Alternateur 160A', 'Peterbilt', 'Électrique',
 '{"models": ["579", "389"]}', '{"min": 299.99, "max": 499.99}');

-- Bons de travail
INSERT INTO work_orders (vehicle_id, mechanic_id, status, description, diagnosis, estimated_hours, estimated_cost)
SELECT 
    v.id,
    m.id,
    'En cours',
    'Maintenance préventive complète',
    'Inspection systématique requise',
    4.5,
    450.00
FROM vehicles v, mechanics m
WHERE v.make = 'Volvo' AND m.first_name = 'Jean'
LIMIT 1;

-- Historique de maintenance
INSERT INTO maintenance_history (vehicle_id, work_order_id, service_type, description, mileage, service_date, next_service_date)
SELECT 
    v.id,
    w.id,
    'Maintenance préventive',
    'Changement huile et filtres',
    150000,
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '6 months'
FROM vehicles v, work_orders w
WHERE v.make = 'Volvo' AND w.status = 'En cours'
LIMIT 1;

-- Diagnostics
INSERT INTO diagnostics (work_order_id, symptoms, diagnostic_codes, ai_analysis, recommended_actions, confidence_score)
SELECT 
    id,
    ARRAY['Bruit anormal au freinage', 'Vibrations'],
    ARRAY['P0128', 'C1234'],
    'Usure probable des plaquettes de frein, vérification du système de freinage recommandée',
    ARRAY['Remplacement des plaquettes', 'Inspection des disques'],
    0.89
FROM work_orders
WHERE status = 'En cours'
LIMIT 1;

-- Fournisseurs
INSERT INTO suppliers (name, contact_info, address, parts_catalog, rating) VALUES
('Pièces Pro Plus', 
 '{"email": "contact@piecesproplus.com", "phone": "+33123456789"}',
 '{"street": "123 Rue de la Mécanique", "city": "Lyon", "postal_code": "69000", "country": "France"}',
 '{"specialties": ["Volvo", "Freightliner"], "inventory_size": 5000}',
 4.8);
