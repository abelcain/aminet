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


WITH RECURSIVE PathCTE AS (
    -- Base case: Start with root paths (where Parent is NULL)
    SELECT
        B.ID,
        B.Child AS volumeID,
        B.Parent AS parentVolumeID,
        A.name AS volumeName,
        CAST(A.name AS CHAR(255)) AS path
    FROM
        B
    JOIN
        A ON B.Child = A.ID
    WHERE
        B.Parent IS NULL

    UNION ALL

    -- Recursive case: Append children to paths
    SELECT
        B.ID,
        B.Child AS volumeID,
        B.Parent AS parentVolumeID,
        A.name AS volumeName,
        CONCAT(cte.path, '\\', A.name) AS path
    FROM
        B
    JOIN
        A ON B.Child = A.ID
    JOIN
        PathCTE cte ON B.Parent = cte.volumeID
)
SELECT
    ROW_NUMBER() OVER (ORDER BY path) AS path_id,
    path
FROM
    (SELECT DISTINCT path FROM PathCTE) AS distinct_paths
    
ORDER BY
    path;


WITH RECURSIVE PathCTE AS (
    -- Base case: Start with root paths (where Parent is NULL)
    SELECT
        B.ID,
        B.Child AS volumeID,
        B.Parent AS parentVolumeID,
        A.name AS volumeName,
        CAST(A.name AS CHAR(255)) AS path
    FROM
        B
    JOIN
        A ON B.Child = A.ID
    WHERE
        B.Parent IS NULL

    UNION ALL

    -- Recursive case: Append children to paths
    SELECT
        B.ID,
        B.Child AS volumeID,
        B.Parent AS parentVolumeID,
        A.name AS volumeName,
        CONCAT(cte.path, '\\', A.name) AS path
    FROM
        B
    JOIN
        A ON B.Child = A.ID
    JOIN
        PathCTE cte ON B.Parent = cte.volumeID
)
-- First, generate the row numbers
SELECT *
FROM (
    SELECT
        ROW_NUMBER() OVER (ORDER BY path) AS path_id,
        path
    FROM
        (SELECT DISTINCT path FROM PathCTE) AS distinct_paths
) AS numbered_paths
-- Then, filter by the path_id
WHERE
    path_id = 5;  -- Replace with the desired path_id

```
