-- Création des tables principales

-- Table des véhicules
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    make VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    vin VARCHAR UNIQUE,
    license_plate VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des mécaniciens
CREATE TABLE mechanics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    phone VARCHAR,
    specialization VARCHAR[],
    certification_level VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des pièces
CREATE TABLE parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    part_number VARCHAR UNIQUE NOT NULL,
    description TEXT,
    manufacturer VARCHAR,
    category VARCHAR,
    compatible_vehicles JSONB,
    price_range JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des bons de travail
CREATE TABLE work_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID REFERENCES vehicles(id),
    mechanic_id UUID REFERENCES mechanics(id),
    status VARCHAR NOT NULL,
    description TEXT,
    diagnosis TEXT,
    estimated_hours DECIMAL,
    estimated_cost DECIMAL,
    actual_hours DECIMAL,
    actual_cost DECIMAL,
    parts_used JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Table historique de maintenance
CREATE TABLE maintenance_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID REFERENCES vehicles(id),
    work_order_id UUID REFERENCES work_orders(id),
    service_type VARCHAR NOT NULL,
    description TEXT,
    mileage INTEGER,
    service_date DATE NOT NULL,
    next_service_date DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des diagnostics
CREATE TABLE diagnostics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    work_order_id UUID REFERENCES work_orders(id),
    symptoms TEXT[],
    diagnostic_codes TEXT[],
    ai_analysis TEXT,
    recommended_actions TEXT[],
    confidence_score DECIMAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des fournisseurs
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    contact_info JSONB,
    address JSONB,
    parts_catalog JSONB,
    rating DECIMAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Création des index
CREATE INDEX idx_vehicles_vin ON vehicles(vin);
CREATE INDEX idx_work_orders_vehicle_id ON work_orders(vehicle_id);
CREATE INDEX idx_work_orders_mechanic_id ON work_orders(mechanic_id);
CREATE INDEX idx_maintenance_history_vehicle_id ON maintenance_history(vehicle_id);
CREATE INDEX idx_diagnostics_work_order_id ON diagnostics(work_order_id);

-- Création des triggers pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_vehicles_updated_at
    BEFORE UPDATE ON vehicles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_mechanics_updated_at
    BEFORE UPDATE ON mechanics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_parts_updated_at
    BEFORE UPDATE ON parts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_work_orders_updated_at
    BEFORE UPDATE ON work_orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_maintenance_history_updated_at
    BEFORE UPDATE ON maintenance_history
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnostics_updated_at
    BEFORE UPDATE ON diagnostics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_suppliers_updated_at
    BEFORE UPDATE ON suppliers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
