CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    photo VARCHAR(200),
    api_key VARCHAR(200) UNIQUE,
    api_key_expires DATETIME,
    token_secret VARCHAR(200) UNIQUE,
    token_secret_expires DATETIME,
    is_admin BOOL DEFAULT FALSE NOT NULL
);

