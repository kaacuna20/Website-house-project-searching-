CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    photo VARCHAR(200),
    public_api_key VARCHAR(200) UNIQUE,
    public_api_key_expires DATETIME,
    secret_api_key VARCHAR(500) UNIQUE,
    secret_api_key_expires DATETIME,
    admin_api_key VARCHAR(500) UNIQUE,
    is_admin BOOL DEFAULT FALSE NOT NULL,
    is_active BOOL DEFAULT TRUE NOT NULL
);
CREATE INDEX idx_public_apikey ON users (public_api_key);
