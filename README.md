# aminet

```sql
CREATE TABLE A (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Insert data into table A
INSERT INTO A (id, name) VALUES 
(1, NULL),
(2, 'Amiga Workbench'),
(3, 'Commodore'),
(4, 'Escom'),
(5, 'Alt Release'),
(6, 'Alt Release 2'),
(7, 'HDD Installer'),
(8, 'A4000T');

-- Drop existing table B if it exists
DROP TABLE IF EXISTS B;

-- Create table B with foreign keys referencing A
CREATE TABLE B (
    ID INTEGER PRIMARY KEY,
    Parent INTEGER,
    Child INTEGER,
    FOREIGN KEY (Parent) REFERENCES A(ID),
    FOREIGN KEY (Child) REFERENCES A(ID)
);

-- Insert relationships into table B
INSERT INTO B (ID, Parent, Child) VALUES 
(1, NULL, 2),       -- Amiga Workbench
(2, NULL, 3),       -- Commodore
(3, NULL, 4),       -- Escom
(4, 2, 5),          -- Amiga Workbench -> Alt Release
(5, 2, 6),          -- Amiga Workbench -> Alt Release 2
(6, 2, 8),          -- Amiga Workbench -> A4000T
(7, 2, 7),          -- Amiga Workbench -> HDD Installer
(8, 3, 8),          -- Commodore -> A4000T
(9, 3, 5),          -- Commodore -> Alt Release
(10, 4, 8),         -- Escom -> A4000T
(11, 4, 5),         -- Escom -> Alt Release
(12, 5, 8),         -- Alt Release -> A4000T (For all)
(13, 9, 8),         -- Commodore\Alt Release -> A4000T
(14, 11, 8);        -- Escom\Alt Release -> A4000T



SELECT * FROM B;


WITH RECURSIVE CTE AS (
    -- Base case: select root paths from B and A
    SELECT 
        B.ID,
        B.Child AS ChildID,
        A.Name AS Path
    FROM 
        B
    JOIN 
        A ON B.Child = A.ID
    WHERE 
        B.Parent IS NULL

    UNION ALL

    -- Recursive case: build paths
    SELECT
        B.ID,
        B.Child AS ChildID,
        CONCAT(CTE.Path, '\\', A.Name) AS Path
    FROM 
        B
    JOIN 
        CTE ON B.Parent = CTE.ChildID
    JOIN 
        A ON B.Child = A.ID
)
SELECT Path FROM CTE;
```
