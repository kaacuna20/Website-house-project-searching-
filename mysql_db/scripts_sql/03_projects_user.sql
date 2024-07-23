CREATE TABLE IF NOT EXISTS project_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    project_id INT,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    UNIQUE(user_id, project_id)
);