CREATE DATABASE lab_asset_db;
USE lab_asset_db;
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);
CREATE TABLE labs (
    lab_id INT AUTO_INCREMENT PRIMARY KEY,
    lab_name VARCHAR(100),
    location VARCHAR(100)
);
CREATE TABLE equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_name VARCHAR(100),
    category VARCHAR(100),
    total_quantity INT,
    available_quantity INT,
    lab_id INT,
    FOREIGN KEY (lab_id) REFERENCES labs(lab_id)
);
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    year INT,
    phone VARCHAR(15)
);
CREATE TABLE issue_records (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    equipment_id INT,
    issue_date DATE,
    return_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);

INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');
INSERT INTO labs (lab_name, location) VALUES
('Programming Lab', 'Block A'),
('Electronics Lab', 'Block B'),
('Mechanical Lab', 'Block C');
INSERT INTO equipment (equipment_name, category, total_quantity, available_quantity, lab_id) VALUES
('Desktop Computer', 'Computer', 30, 30, 1),
('Oscilloscope', 'Electronics', 15, 15, 2),
('3D Printer', 'Mechanical', 5, 5, 3);
INSERT INTO students (name, department, year, phone) VALUES
('Rahul', 'CSE', 2, '9876543210'),
('Anjali', 'ECE', 3, '9876501234');


INSERT INTO issue_records (student_id, equipment_id, issue_date, return_date, status)
VALUES
(1, 1, '2026-02-26', NULL, 'Issued'),
(2, 2, '2026-02-26', NULL, 'Issued');


INSERT INTO students (name, department, year, phone) VALUES
('Arjun Nair','CSE',1,'9123456781'),
('Meera Joseph','CSE',2,'9123456782'),
('Akhil Menon','ECE',1,'9123456783'),
('Divya Krishnan','ECE',3,'9123456784'),
('Rohit Sharma','ME',2,'9123456785'),
('Sneha Pillai','ME',4,'9123456786'),
('Vishnu Prasad','CSE',3,'9123456787'),
('Ananya Das','ECE',2,'9123456788'),
('Kiran Mathew','ME',1,'9123456789'),
('Lakshmi Nair','CSE',4,'9123456790'),
('Harsha Reddy','ECE',3,'9123456791'),
('Neha Verma','CSE',2,'9123456792'),
('Aditya Kumar','ME',3,'9123456793'),
('Priya Menon','ECE',1,'9123456794'),
('Farhan Ali','CSE',2,'9123456795');



INSERT INTO admin (username, password) VALUES
('lab_assistant', 'lab123'),
('inventory_manager', 'inv123'),
('hod_cse', 'hod123'),
('system_admin', 'sys123');



INSERT INTO labs (lab_name, location) VALUES
('Data Structures Lab', 'Block A'),
('Network Lab', 'Block A'),
('Computer Lab - IT', 'Block D'),
('Software Lab - IT', 'Block D'),
('Microprocessor Lab', 'Block B'),
('Electrical Machines Lab', 'Block E'),
('Power Systems Lab', 'Block E'),
('Thermal Engineering Lab', 'Block C'),
('CAD Lab - CE', 'Block F'),
('Structural Lab - CE', 'Block F'),
('Embedded Systems Lab', 'Block B'),
('Robotics Lab', 'Block G');


INSERT INTO students (name, department, year, phone) VALUES
('Ethan Clark','CSE',1,'9000000101'),
('Olivia Martin','IT',2,'9000000102'),
('Noah Wilson','ECE',3,'9000000103'),
('Ava Thompson','EEE',1,'9000000104'),
('Liam Anderson','ME',2,'9000000105'),
('Sophia Taylor','CE',4,'9000000106'),
('Mason Thomas','CSE',3,'9000000107'),
('Isabella Moore','IT',1,'9000000108'),
('Lucas Jackson','ECE',2,'9000000109'),
('Mia White','EEE',3,'9000000110'),
('James Harris','ME',4,'9000000111'),
('Charlotte Lewis','CE',2,'9000000112'),
('Benjamin Walker','CSE',1,'9000000113'),
('Amelia Hall','IT',3,'9000000114'),
('Elijah Allen','ECE',4,'9000000115'),
('Harper Young','EEE',2,'9000000116'),
('Daniel King','ME',1,'9000000117'),
('Evelyn Wright','CE',3,'9000000118'),
('Henry Scott','CSE',4,'9000000119'),
('Abigail Green','IT',2,'9000000120'),
('Alexander Baker','ECE',1,'9000000121'),
('Emily Adams','EEE',4,'9000000122'),
('Michael Nelson','ME',3,'9000000123'),
('Elizabeth Carter','CE',1,'9000000124'),
('Sebastian Mitchell','CSE',2,'9000000125'),
('Avery Perez','IT',4,'9000000126'),
('Jack Roberts','ECE',3,'9000000127'),
('Ella Turner','EEE',1,'9000000128'),
('Owen Phillips','ME',2,'9000000129'),
('Scarlett Campbell','CE',4,'9000000130'),
('Wyatt Parker','CSE',3,'9000000131'),
('Chloe Evans','IT',1,'9000000132'),
('Gabriel Edwards','ECE',2,'9000000133'); 



INSERT INTO equipment (equipment_name, category, total_quantity, available_quantity, lab_id) VALUES
('Server Machine','Computer',5,5,1),
('Router','Networking',20,20,3),
('Switch','Networking',25,25,3),
('Laser Printer','Computer',10,10,1),
('Projector','Electronics',8,8,2),
('Function Generator','Electronics',12,12,2),
('Multimeter','Electronics',30,30,2),
('Soldering Station','Electronics',20,20,6),
('Arduino Kit','Embedded',40,40,14),
('Raspberry Pi','Embedded',35,35,14),
('Stepper Motor','Mechanical',25,25,3),
('Hydraulic Trainer Kit','Mechanical',6,6,3),
('CNC Machine','Mechanical',4,4,10),
('Welding Machine','Mechanical',10,10,10),
('Surveying Instrument','Civil',15,15,12),
('Concrete Testing Machine','Civil',5,5,12),
('Total Station','Civil',7,7,12),
('Power Supply Unit','Electrical',20,20,8),
('Transformer Model','Electrical',10,10,8),
('Induction Motor Setup','Electrical',6,6,8),
('Thermal Conductivity Apparatus','Mechanical',5,5,9),
('Refrigeration Test Rig','Mechanical',4,4,9),
('Microprocessor Kit','Electronics',18,18,6),
('FPGA Board','Electronics',12,12,6),
('Robotics Arm','Robotics',3,3,15),
('Drone Kit','Robotics',6,6,15),
('VR Headset','Computer',10,10,4),
('Graphics Tablet','Computer',12,12,4),
('Firewall Device','Networking',8,8,5),
('Network Analyzer','Networking',5,5,5),
('Embedded Trainer Board','Embedded',10,10,14),
('Digital Storage Oscilloscope','Electronics',10,10,2),
('PLC Trainer Kit','Electrical',8,8,8),
('Solar Panel Setup','Electrical',6,6,8),
('Wind Turbine Model','Electrical',3,3,8),
('AutoCAD Workstation','Computer',20,20,11),
('Structural Testing Frame','Civil',4,4,13),
('Beam Testing Apparatus','Civil',6,6,13),
('Smart Board','Computer',5,5,1),
('UPS System','Computer',10,10,1),
('3D Scanner','Mechanical',3,3,10),
('Lathe Machine','Mechanical',5,5,10),
('Drill Machine','Mechanical',12,12,10),
('Microcontroller Kit','Embedded',20,20,14),
('Battery Testing Unit','Electrical',7,7,8),
('Signal Generator','Electronics',14,14,2),
('Digital Multimeter','Electronics',25,25,2);


INSERT INTO issue_records (student_id, equipment_id, issue_date, return_date, status) VALUES
(1, 3, '2026-01-02', '2026-01-06', 'Returned'),
(2, 5, '2026-01-03', NULL, 'Issued'),
(3, 2, '2026-01-04', '2026-01-09', 'Returned'),
(4, 6, '2026-01-05', NULL, 'Issued'),
(5, 1, '2026-01-06', '2026-01-11', 'Returned'),
(6, 4, '2026-01-07', NULL, 'Issued'),
(7, 7, '2026-01-08', '2026-01-13', 'Returned'),
(8, 9, '2026-01-09', NULL, 'Issued'),
(9, 8, '2026-01-10', '2026-01-15', 'Returned'),
(10, 10, '2026-01-11', NULL, 'Issued'),
(11, 12, '2026-01-12', '2026-01-17', 'Returned'),
(12, 11, '2026-01-13', NULL, 'Issued'),
(13, 13, '2026-01-14', '2026-01-19', 'Returned'),
(14, 15, '2026-01-15', NULL, 'Issued'),
(15, 14, '2026-01-16', '2026-01-21', 'Returned'),
(16, 16, '2026-01-17', NULL, 'Issued'),
(17, 18, '2026-01-18', '2026-01-23', 'Returned'),
(18, 17, '2026-01-19', NULL, 'Issued'),
(19, 19, '2026-01-20', '2026-01-25', 'Returned'),
(20, 20, '2026-01-21', NULL, 'Issued'),
(21, 21, '2026-01-22', '2026-01-27', 'Returned'),
(22, 22, '2026-01-23', NULL, 'Issued'),
(23, 23, '2026-01-24', '2026-01-29', 'Returned'),
(24, 24, '2026-01-25', NULL, 'Issued'),
(25, 25, '2026-01-26', '2026-01-31', 'Returned'),
(26, 26, '2026-01-27', NULL, 'Issued'),
(27, 27, '2026-01-28', '2026-02-02', 'Returned'),
(28, 28, '2026-01-29', NULL, 'Issued'),
(29, 29, '2026-01-30', '2026-02-04', 'Returned'),
(30, 30, '2026-01-31', NULL, 'Issued'),
(31, 31, '2026-02-01', '2026-02-06', 'Returned'),
(32, 32, '2026-02-02', NULL, 'Issued'),
(33, 33, '2026-02-03', '2026-02-08', 'Returned'),
(34, 34, '2026-02-04', NULL, 'Issued'),
(35, 35, '2026-02-05', '2026-02-10', 'Returned'),
(36, 36, '2026-02-06', NULL, 'Issued'),
(37, 37, '2026-02-07', '2026-02-12', 'Returned'),
(38, 38, '2026-02-08', NULL, 'Issued'),
(39, 39, '2026-02-09', '2026-02-14', 'Returned'),
(40, 40, '2026-02-10', NULL, 'Issued'),
(41, 41, '2026-02-11', '2026-02-16', 'Returned'),
(42, 42, '2026-02-12', NULL, 'Issued'),
(43, 43, '2026-02-13', '2026-02-18', 'Returned'),
(44, 44, '2026-02-14', NULL, 'Issued'),
(45, 45, '2026-02-15', '2026-02-20', 'Returned'),
(46, 46, '2026-02-16', NULL, 'Issued'),
(47, 47, '2026-02-17', '2026-02-22', 'Returned'),
(48, 48, '2026-02-18', NULL, 'Issued'),
(49, 49, '2026-02-19', '2026-02-24', 'Returned'),
(50, 50, '2026-02-20', NULL, 'Issued');



CREATE VIEW current_issued AS
SELECT s.name, e.equipment_name, i.issue_date
FROM issue_records i
JOIN students s ON i.student_id = s.student_id
JOIN equipment e ON i.equipment_id = e.equipment_id
WHERE i.status = 'Issued';

CREATE VIEW lab_usage AS
SELECT l.lab_name, e.equipment_name, COUNT(i.issue_id) AS times_borrowed
FROM issue_records i
JOIN equipment e ON i.equipment_id = e.equipment_id
JOIN labs l ON e.lab_id = l.lab_id
GROUP BY l.lab_id, e.equipment_id;

DELIMITER $$

CREATE TRIGGER decrease_available
AFTER INSERT ON issue_records
FOR EACH ROW
BEGIN
  -- Only decrease if the new record is 'Issued' and equipment is available
  IF NEW.status = 'Issued' AND 
     (SELECT available_quantity FROM equipment WHERE equipment_id = NEW.equipment_id) > 0 THEN
    UPDATE equipment
    SET available_quantity = available_quantity - 1
    WHERE equipment_id = NEW.equipment_id;
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER increase_available
AFTER UPDATE ON issue_records
FOR EACH ROW
BEGIN
  -- Only increase if status changed from 'Issued' to 'Returned'
  IF NEW.status = 'Returned' AND OLD.status = 'Issued' THEN
    UPDATE equipment
    SET available_quantity = available_quantity + 1
    WHERE equipment_id = NEW.equipment_id;
  END IF;
END$$

DELIMITER ;

ALTER TABLE issue_records
ADD CONSTRAINT chk_status
CHECK (status IN ('Issued','Returned'));

ALTER TABLE issue_records
ADD CONSTRAINT chk_return_date
CHECK (return_date IS NULL OR return_date >= issue_date);

ALTER TABLE equipment
ADD CONSTRAINT chk_available_quantity
CHECK (available_quantity >= 0);

use lab_asset_db;

UPDATE admin
SET password = 'addmin1234'
WHERE username = 'admin';

ALTER TABLE issue_records
ADD COLUMN fine INT DEFAULT 0;
    
ALTER TABLE equipment 
ADD COLUMN status VARCHAR(20) DEFAULT 'Available';


-- Step 1: Drop existing foreign keys
ALTER TABLE issue_records
DROP FOREIGN KEY issue_records_ibfk_1;

ALTER TABLE issue_records
DROP FOREIGN KEY issue_records_ibfk_2;

-- Step 2: Add them again with CASCADE
ALTER TABLE issue_records
ADD CONSTRAINT fk_student
FOREIGN KEY (student_id)
REFERENCES students(student_id)
ON DELETE CASCADE;

ALTER TABLE issue_records
ADD CONSTRAINT fk_equipment
FOREIGN KEY (equipment_id)
REFERENCES equipment(equipment_id)
ON DELETE CASCADE;

SHOW CREATE TABLE issue_records;

CREATE TABLE complaints (complaint_id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(100), equipment_id INT, complaint_type VARCHAR(50), message TEXT, status ENUM('Pending','Resolved') DEFAULT 'Pending', submitted_at DATETIME DEFAULT NOW());
CREATE TABLE student_users (id INT AUTO_INCREMENT PRIMARY KEY, student_id INT UNIQUE, username VARCHAR(50) UNIQUE, password VARCHAR(100));

ALTER TABLE complaints ADD COLUMN student_id INT, ADD FOREIGN KEY (student_id) REFERENCES students(student_id);

SET SQL_SAFE_UPDATES = 0;
DELETE FROM student_users;
SET SQL_SAFE_UPDATES = 1;

INSERT INTO student_users (student_id, username, password)
SELECT student_id,
       LOWER(REPLACE(name, ' ', '')),
       CONCAT(LOWER(REPLACE(name, ' ', '')), '456')
FROM students;
