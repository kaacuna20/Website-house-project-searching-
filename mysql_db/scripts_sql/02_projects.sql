CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100) NOT NULL UNIQUE, 
    logo VARCHAR(250) NOT NULL,
    location VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    contact VARCHAR(50) NOT NULL,
    area FLOAT NOT NULL,
    price INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    img_url VARCHAR(300) NOT NULL,
    description TEXT(400) NOT NULL,
    url_website VARCHAR(250) NOT NULL,
    slug VARCHAR(250) NOT NULL UNIQUE,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    CHECK (area >= 0 AND price >= 0)
    );
CREATE INDEX idx_slug ON projects (slug);