-- ===========================================
-- SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS
-- Spaceflights - PostgreSQL
-- ===========================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS spaceflights;

-- Usar la base de datos
\c spaceflights;

-- Crear esquema para datos de spaceflights
CREATE SCHEMA IF NOT EXISTS spaceflights;

-- Tabla para empresas
CREATE TABLE IF NOT EXISTS spaceflights.companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    founded_year INTEGER,
    country VARCHAR(100),
    parent_company VARCHAR(255),
    company_rating VARCHAR(10),
    iata_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para shuttles
CREATE TABLE IF NOT EXISTS spaceflights.shuttles (
    id SERIAL PRIMARY KEY,
    shuttle_name VARCHAR(255) NOT NULL,
    company_id INTEGER REFERENCES spaceflights.companies(id),
    shuttle_type VARCHAR(100),
    engine_type VARCHAR(100),
    engine_vendor VARCHAR(100),
    engines INTEGER,
    passenger_capacity INTEGER,
    cancellation_policy VARCHAR(100),
    crew INTEGER,
    d_check_complete BOOLEAN DEFAULT FALSE,
    moon_clearance_complete BOOLEAN DEFAULT FALSE,
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para reviews
CREATE TABLE IF NOT EXISTS spaceflights.reviews (
    id SERIAL PRIMARY KEY,
    shuttle_id INTEGER REFERENCES spaceflights.shuttles(id),
    review_score INTEGER CHECK (review_score >= 1 AND review_score <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para datos procesados
CREATE TABLE IF NOT EXISTS spaceflights.processed_data (
    id SERIAL PRIMARY KEY,
    data_type VARCHAR(100) NOT NULL,
    data_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para modelos entrenados
CREATE TABLE IF NOT EXISTS spaceflights.models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_type VARCHAR(100),
    model_version VARCHAR(50),
    model_metrics JSONB,
    model_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para logs de ejecución
CREATE TABLE IF NOT EXISTS spaceflights.execution_logs (
    id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(255) NOT NULL,
    execution_id VARCHAR(100),
    status VARCHAR(50),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_companies_name ON spaceflights.companies(name);
CREATE INDEX IF NOT EXISTS idx_shuttles_company_id ON spaceflights.shuttles(company_id);
CREATE INDEX IF NOT EXISTS idx_reviews_shuttle_id ON spaceflights.reviews(shuttle_id);
CREATE INDEX IF NOT EXISTS idx_execution_logs_pipeline ON spaceflights.execution_logs(pipeline_name);
CREATE INDEX IF NOT EXISTS idx_execution_logs_status ON spaceflights.execution_logs(status);

-- Insertar datos de ejemplo
INSERT INTO spaceflights.companies (name, founded_year, country, parent_company, company_rating, iata_approved) VALUES
('SpaceX', 2002, 'USA', NULL, '95%', TRUE),
('Boeing', 1916, 'USA', NULL, '80%', TRUE),
('Blue Origin', 2000, 'USA', 'Amazon', '70%', FALSE),
('Virgin Galactic', 2004, 'USA', 'Virgin Group', '65%', FALSE)
ON CONFLICT DO NOTHING;

INSERT INTO spaceflights.shuttles (shuttle_name, company_id, shuttle_type, engine_type, engine_vendor, engines, passenger_capacity, cancellation_policy, crew, d_check_complete, moon_clearance_complete, price) VALUES
('Falcon 9', 1, 'Reusable', 'Merlin', 'SpaceX', 9, 7, 'Flexible', 2, TRUE, TRUE, 100000.00),
('New Shepard', 3, 'Suborbital', 'BE-3', 'Blue Origin', 1, 6, 'Strict', 0, FALSE, FALSE, 80000.00),
('SpaceShipTwo', 4, 'Suborbital', 'RocketMotorTwo', 'Virgin Galactic', 1, 6, 'Moderate', 2, TRUE, FALSE, 200000.00),
('Soyuz', 2, 'Capsule', 'RD-107', 'Energia', 4, 3, 'Strict', 3, TRUE, TRUE, 150000.00)
ON CONFLICT DO NOTHING;

-- Crear usuario específico para la aplicación
CREATE USER IF NOT EXISTS spaceflights_user WITH PASSWORD 'spaceflights_pass';
GRANT ALL PRIVILEGES ON DATABASE spaceflights TO spaceflights_user;
GRANT ALL PRIVILEGES ON SCHEMA spaceflights TO spaceflights_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA spaceflights TO spaceflights_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA spaceflights TO spaceflights_user;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos Spaceflights inicializada correctamente';
    RAISE NOTICE 'Esquema: spaceflights';
    RAISE NOTICE 'Usuario: spaceflights_user';
    RAISE NOTICE 'Puerto: 5433 (para evitar conflicto con PostgreSQL del sistema)';
END $$;