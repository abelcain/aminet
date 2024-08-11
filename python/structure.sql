CREATE TABLE DirectoryStructure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('directory', 'file') NOT NULL,
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES DirectoryStructure(id)
);

-- Insert the root directory
INSERT INTO DirectoryStructure (name, type, parent_id) 
    VALUES 
        ('Utilities', 'directory', NULL);

-- Insert the 'MultiView.info' file
INSERT INTO DirectoryStructure (name, type, parent_id) V
ALUES ('MultiView.info', 'file', (SELECT id FROM DirectoryStructure WHERE name = 'Utilities'));

-- Insert the 'MultiView' directory
INSERT INTO DirectoryStructure (name, type, parent_id) 
VALUES ('MultiView', 'directory', (SELECT id FROM DirectoryStructure WHERE name = 'Utilities'));

-- Insert the 'MultiView/MultiView.info' file
INSERT INTO DirectoryStructure (name, type, parent_id) VALUES ('MultiView.info', 'file', (SELECT id FROM DirectoryStructure WHERE name = 'MultiView' AND parent_id = (SELECT id FROM DirectoryStructure WHERE name = 'Utilities')));
