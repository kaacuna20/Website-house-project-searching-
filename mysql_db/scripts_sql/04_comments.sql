CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    comment TEXT(500) NOT NULL,
    user_id INT,
    project_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
);