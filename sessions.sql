-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Jul 23, 2025 at 05:14 AM
-- Server version: 5.7.39
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Factor`
--

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `session_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `session_title` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `format` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`session_id`, `username`, `session_title`, `created_at`, `format`) VALUES
(1, 'innovative challenger', 'Should everyone turn vegan?', '2025-07-19 18:47:12', 'bp'),
(2, 'innovative challenger', 'Should everyone turn vegan?', '2025-07-19 18:48:42', 'bp'),
(3, 'innovative challenger', 'abc', '2025-07-19 20:04:18', 'ap'),
(4, 'innovative challenger', 'abc', '2025-07-20 04:19:28', 'ap'),
(5, 'innovative challenger', 'abc', '2025-07-20 04:19:51', 'ap'),
(6, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 04:24:21', 'bp'),
(7, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:10:48', 'bp'),
(8, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:20:47', 'bp'),
(9, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:21:48', 'bp'),
(10, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:23:14', 'bp'),
(11, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:24:53', 'bp'),
(12, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:39:58', 'bp'),
(13, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:48:00', 'bp'),
(14, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 06:52:27', 'bp'),
(15, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 07:05:59', 'bp'),
(16, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 07:15:16', 'bp'),
(17, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 07:47:15', 'bp'),
(18, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 07:50:13', 'bp'),
(19, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 07:55:16', 'bp'),
(20, 'tester', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 10:08:17', 'bp'),
(21, 'realjupiter05', 'Should the legal voting age be lowered to 16 in all countries?', '2025-07-20 10:45:21', 'bp'),
(22, 'real', 'Should all universities offer free tuition, funded by the government?', '2025-07-20 13:55:24', 'bp'),
(23, 'real', 'Man vs Machine', '2025-07-20 14:28:03', 'bp'),
(24, 'real', 'Are Developed Nations to be held accountable for Climate Change?', '2025-07-20 15:19:50', 'bp'),
(25, 'real', 'Are Developed Nations to be held accountable for Climate Change?', '2025-07-20 17:26:14', 'ap'),
(26, 'real', 'Are Developed Nations to be held accountable for Climate Change?', '2025-07-20 17:31:04', 'bp'),
(27, 'real', ' Should homework be abolished in primary schools?', '2025-07-21 08:43:14', 'bp'),
(28, 'real', 'Should taxes be dropped to 0?', '2025-07-21 11:03:25', 'bp'),
(29, 'real', 'Ban the Use of AI in Political Campaigning.', '2025-07-22 08:14:13', 'bp'),
(30, 'real', 'Should schools implement mandatory uniforms for students?', '2025-07-22 15:21:39', 'bp'),
(31, 'real', 'Should schools implement mandatory uniforms for students?', '2025-07-22 15:25:28', 'bp'),
(32, 'real', 'Should Social Media be censored?', '2025-07-22 16:18:42', 'bp'),
(33, 'prajwal', 'Should taxes be dropped to 0?', '2025-07-22 18:46:50', 'bp'),
(34, 'prajwal', 'Are Developed Nations to be held accountable for Climate Change?', '2025-07-22 19:59:59', 'bp');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
