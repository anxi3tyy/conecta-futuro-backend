CREATE TABLE usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(100) NOT NULL,
  contraseña VARCHAR(255) NOT NULL,
  tipo_usuario VARCHAR(20) NOT NULL,
  telefono VARCHAR(20),
  direccion VARCHAR(150),
  comuna VARCHAR(100),
  fecha_registro DATETIME
);


CREATE TABLE beneficiarios (
  id_beneficiario INT PRIMARY KEY,
  id_rsh VARCHAR(20),
  tramo_rsh VARCHAR(20), 
  nivel_digital VARCHAR(20), 
  observaciones TEXT,
  FOREIGN KEY (id_beneficiario) REFERENCES usuarios(id_usuario)
);


CREATE TABLE voluntarios (
  id_voluntario INT PRIMARY KEY,
  especialidad VARCHAR(100),
  disponibilidad VARCHAR(50),
  FOREIGN KEY (id_voluntario) REFERENCES usuarios(id_usuario)
);


CREATE TABLE donaciones (
  id_donacion INT AUTO_INCREMENT PRIMARY KEY,
  id_donante INT NOT NULL,
  tipo_donacion VARCHAR(20) NOT NULL, 
  descripcion TEXT,
  fecha_donacion DATETIME,
  FOREIGN KEY (id_donante) REFERENCES usuarios(id_usuario)
);


CREATE TABLE equipos (
  id_equipo INT AUTO_INCREMENT PRIMARY KEY,
  tipo_equipo VARCHAR(50) NOT NULL,
  estado VARCHAR(20) NOT NULL, 
  id_donacion INT,
  fecha_ingreso DATETIME,
  FOREIGN KEY (id_donacion) REFERENCES donaciones(id_donacion)
);


CREATE TABLE entregas (
  id_entrega INT AUTO_INCREMENT PRIMARY KEY,
  id_equipo INT,
  id_beneficiario INT,
  id_voluntario INT,
  fecha_entrega DATETIME,
  observaciones TEXT,
  FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
  FOREIGN KEY (id_beneficiario) REFERENCES beneficiarios(id_beneficiario),
  FOREIGN KEY (id_voluntario) REFERENCES voluntarios(id_voluntario)
);


CREATE TABLE cursos (
  id_curso INT AUTO_INCREMENT PRIMARY KEY,
  nombre_curso VARCHAR(100) NOT NULL,
  descripcion TEXT,
  duracion INT,
  modalidad VARCHAR(20) NOT NULL
);


CREATE TABLE inscripciones (
  id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
  id_beneficiario INT,
  id_curso INT,
  fecha_inscripcion DATETIME,
  estado VARCHAR(20),
  FOREIGN KEY (id_beneficiario) REFERENCES beneficiarios(id_beneficiario),
  FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);


CREATE TABLE soporte (
  id_ticket INT AUTO_INCREMENT PRIMARY KEY,
  id_beneficiario INT,
  id_voluntario INT,
  descripcion TEXT NOT NULL,
  estado VARCHAR(20) NOT NULL, 
  fecha_creacion DATETIME,
  FOREIGN KEY (id_beneficiario) REFERENCES beneficiarios(id_beneficiario),
  FOREIGN KEY (id_voluntario) REFERENCES voluntarios(id_voluntario)
);
