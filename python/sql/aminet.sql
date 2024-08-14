USE aminet;

-- Step 1: Create the `types` table
CREATE TABLE `types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
);

-- Step 2: Insert the data into `types`
INSERT INTO `types` (`type`) VALUES
('volume'),
('dir'),
('file'),
('info');

-- Step 3: Create the `directorystructure` table with the foreign key constraint
CREATE TABLE `directorystructure` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `parentID` INT NULL,
  `name` VARCHAR(45) NOT NULL,
  `type` INT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_directorystructure_type`
    FOREIGN KEY (`type`)
    REFERENCES `types`(`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);