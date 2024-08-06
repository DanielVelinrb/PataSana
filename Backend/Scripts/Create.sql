-- Crear la base de datos
CREATE DATABASE railway;

-- Conectar a la base de datos
\c mi_veterinaria;

-- Crear la tabla Usuario
CREATE TABLE Usuario (
    ID TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    Rol TEXT NOT NULL
);

-- Crear la tabla Mascota
CREATE TABLE Mascota (
    ID TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Raza TEXT NOT NULL,
    Especie TEXT NOT NULL,
    Edad INTEGER NOT NULL,
    Observaciones TEXT,
    ID_Dueno TEXT NOT NULL
);

-- Crear la tabla Producto
CREATE TABLE Producto (
    ID TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Precio INTEGER NOT NULL,
    Descripcion TEXT,
    Cantidad INTEGER NOT NULL
);

-- Crear la tabla Visitas
CREATE TABLE Visitas (
    ID TEXT PRIMARY KEY,
    Fecha DATE NOT NULL,
    duenio TEXT NOT NULL,
    Observaciones TEXT,
    NombreMascota TEXT NOT NULL,
    MotivoVisita TEXT NOT NULL,
);


-- Crear la tabla Visitas_Productos
CREATE TABLE Visitas_Productos (
    IDVisitas TEXT NOT NULL,
    IDProducto TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Cantidad INTEGER NOT NULL,
    Total INTEGER NOT NULL,
    PRIMARY KEY (IDVisitas, IDProducto),
    FOREIGN KEY (IDVisitas) REFERENCES Visitas(ID),
    FOREIGN KEY (IDProducto) REFERENCES Producto(ID)
);
