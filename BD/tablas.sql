-- =============================================
-- SCRIPT COMPLETO DE BASE DE DATOS - CRM APP
-- =============================================

-- Crear base de datos
DROP DATABASE IF EXISTS usuarios_db;
CREATE DATABASE usuarios_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE usuarios_db;

-- =============================================
-- TABLA: usuarios
-- =============================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    edad INT NOT NULL CHECK (edad BETWEEN 1 AND 120),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices para optimización
    INDEX idx_nombre (nombre),
    INDEX idx_apellido (apellido),
    INDEX idx_edad (edad),
    INDEX idx_fecha_creacion (fecha_creacion)
) ENGINE=InnoDB;

-- =============================================
-- TABLA: correos
-- =============================================
CREATE TABLE correos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo ENUM('gmail', 'outlook', 'hotmail', 'yahoo', 'empresa', 'custom1', 'custom2', 'custom3') NOT NULL,
    correo VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Llave foránea con eliminación en cascada
    FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) 
        ON DELETE CASCADE,
    
    -- Índices para optimización
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_tipo (tipo),
    INDEX idx_correo (correo),
    INDEX idx_usuario_tipo (usuario_id, tipo),
    INDEX idx_fecha_creacion (fecha_creacion),
    
    -- Restricción única para evitar duplicados
    UNIQUE KEY unique_correo_usuario (usuario_id, tipo)
) ENGINE=InnoDB;
