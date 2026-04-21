-- Database Dump for AssetTracker Pro
-- Designed for 1000+ employees and a dedicated HR department

CREATE DATABASE IF NOT EXISTS asset_tracker_db;
USE asset_tracker_db;

-- --------------------------------------------------------
-- Table Structure for `employees`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_code` varchar(50) NOT NULL UNIQUE,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL UNIQUE,
  `phone_number` varchar(20) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `role` enum('Admin', 'HR', 'Employee') DEFAULT 'Employee',
  `is_active` boolean DEFAULT true,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table Structure for `assets`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_tag` varchar(50) NOT NULL UNIQUE,
  `name` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `serial_number` varchar(150) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_cost` decimal(10,2) DEFAULT NULL,
  `status` enum('Available', 'Assigned', 'In Maintenance', 'Lost', 'Retired') DEFAULT 'Available',
  `notes` text DEFAULT NULL,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table Structure for `asset_assignments`
-- Notes: No strict Foreign Key constraints per requirements.
-- `asset_id` references `assets.id`
-- `employee_id` references `employees.id`
-- `assigned_by_id` references `employees.id` (The HR/Admin who made the assignment)
-- --------------------------------------------------------
DROP TABLE IF EXISTS `asset_assignments`;
CREATE TABLE `asset_assignments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `assigned_by_id` int(11) NOT NULL,
  `assignment_date` date NOT NULL,
  `expected_return_date` date DEFAULT NULL,
  `actual_return_date` date DEFAULT NULL,
  `assignment_notes` text DEFAULT NULL,
  `return_notes` text DEFAULT NULL,
  `status` enum('Active', 'Returned') DEFAULT 'Active',
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table Structure for `audit_logs`
-- Tracks all major actions in the system for accountability
-- `performed_by_id` references `employees.id`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `performed_by_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `target_table` varchar(100) NOT NULL,
  `target_record_id` int(11) NOT NULL,
  `details` text DEFAULT NULL,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Dumping Dummy Data for `employees`
-- --------------------------------------------------------
INSERT INTO `employees` (`employee_code`, `first_name`, `last_name`, `email`, `department`, `role`) VALUES
('EMP001', 'Alice', 'Smith', 'alice.smith@company.com', 'HR', 'Admin'),
('EMP002', 'Bob', 'Johnson', 'bob.johnson@company.com', 'Engineering', 'Employee'),
('EMP003', 'Charlie', 'Davis', 'charlie.davis@company.com', 'Sales', 'Employee'),
('EMP004', 'Diana', 'Prince', 'diana.prince@company.com', 'Marketing', 'Employee'),
('EMP005', 'Evan', 'Wright', 'evan.wright@company.com', 'Engineering', 'Employee');

-- --------------------------------------------------------
-- Dumping Dummy Data for `assets`
-- --------------------------------------------------------
INSERT INTO `assets` (`asset_tag`, `name`, `category`, `serial_number`, `purchase_date`, `status`) VALUES
('AST-LP-001', 'MacBook Pro 16"', 'Laptop', 'C02XD123456', '2025-01-15', 'Assigned'),
('AST-LP-002', 'Dell XPS 15', 'Laptop', 'DXPS98765', '2025-02-20', 'Assigned'),
('AST-PH-001', 'iPhone 15 Pro', 'Phone', 'IPH15P5555', '2025-03-01', 'Available'),
('AST-SW-001', 'Adobe Creative Cloud', 'Software License', 'ADOBE-CC-999', '2025-01-10', 'Assigned'),
('AST-MN-001', 'Dell UltraSharp 27"', 'Monitor', 'DUM27-1111', '2024-11-05', 'In Maintenance');

-- --------------------------------------------------------
-- Dumping Dummy Data for `asset_assignments`
-- --------------------------------------------------------
INSERT INTO `asset_assignments` (`asset_id`, `employee_id`, `assigned_by_id`, `assignment_date`, `status`) VALUES
(1, 2, 1, '2025-01-20', 'Active'), -- Bob Johnson assigned MacBook Pro by Alice Smith
(2, 3, 1, '2025-02-25', 'Active'), -- Charlie Davis assigned Dell XPS by Alice Smith
(4, 4, 1, '2025-01-12', 'Active'); -- Diana Prince assigned Adobe CC by Alice Smith

-- --------------------------------------------------------
-- Dumping Dummy Data for `audit_logs`
-- --------------------------------------------------------
INSERT INTO `audit_logs` (`performed_by_id`, `action`, `target_table`, `target_record_id`, `details`) VALUES
(1, 'CREATE', 'employees', 2, 'Added new employee Bob Johnson'),
(1, 'CREATE', 'assets', 1, 'Added new asset MacBook Pro 16"'),
(1, 'ASSIGN', 'asset_assignments', 1, 'Assigned asset AST-LP-001 to employee EMP002');
