-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 10, 2018 at 05:24 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.32-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wowdb_login`
--

-- --------------------------------------------------------

--
-- Table structure for table `Account`
--

CREATE TABLE `Account` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `salt` varbinary(100) NOT NULL,
  `verifier` varchar(100) NOT NULL,
  `ip` varchar(16) DEFAULT NULL,
  `timezone` varchar(4) DEFAULT NULL,
  `os` varchar(16) DEFAULT NULL,
  `platform` varchar(16) DEFAULT NULL,
  `locale` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Account`
--

INSERT INTO `Account` (`id`, `name`, `salt`, `verifier`, `ip`, `timezone`, `os`, `platform`, `locale`) VALUES
(1, 'TEST', 0xf4309a962edd5283293cf06556cc7e7fe2dbf232aeaf7cb3438d05e9d7a0e0d7, '46648186518343394880333132289518892739570503731571972133503643613572235148956', '127.0.0.1', '120', 'Win', 'x86', 'enGB'),
(2, 'TEST2', 0xae1b05e0bd8c35e789622ab2e27f5e5c95000d74382fa3c245794a95ef0cb86b, '41673165534760024451124393493679504063007404292161252621717782436042874409863', '127.0.0.1', '120', 'Win', 'x86', 'enGB');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Account`
--
ALTER TABLE `Account`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Account`
--
ALTER TABLE `Account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;