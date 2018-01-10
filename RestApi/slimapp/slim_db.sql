-- phpMyAdmin SQL Dump
-- version 4.7.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 09, 2018 at 05:51 PM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `slim_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `barcode`
--

CREATE TABLE `barcode` (
  `code` varchar(80) NOT NULL DEFAULT '',
  `status` enum('ready','registred') NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `barcode`
--

INSERT INTO `barcode` (`code`, `status`) VALUES
('EAGPRC', 'registred'),
('EAGPRA', 'registred'),
('EAGPRB', 'ready');

-- --------------------------------------------------------

--
-- Table structure for table `join_user_barcode`
--

CREATE TABLE `join_user_barcode` (
  `user` int(11) NOT NULL,
  `barcode` varchar(80) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `join_user_barcode`
--

INSERT INTO `join_user_barcode` (`user`, `barcode`, `date`) VALUES
(1, 'EAGPRC', '2018-01-08 16:11:53'),
(1, 'EAGPRA', '2018-01-09 17:48:43'),
(1, 'EAGPRA', '2018-01-09 17:49:34');

-- --------------------------------------------------------

--
-- Table structure for table `join_user_product`
--

CREATE TABLE `join_user_product` (
  `user` int(11) NOT NULL,
  `product` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prodcut`
--

CREATE TABLE `prodcut` (
  `id` int(11) NOT NULL,
  `label` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `prodcut`
--

INSERT INTO `prodcut` (`id`, `label`) VALUES
(1, 'nutrizione personalizzata'),
(2, 'predisposizione malattie'),
(7, 'just fill up');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(40) NOT NULL,
  `salt` varchar(50) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `city` varchar(80) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `note` text,
  `mobile` varchar(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `password`, `salt`, `name`, `last_name`, `address`, `city`, `zip_code`, `note`, `mobile`) VALUES
(36, 'rustam@gmail.com', '4f4eeb964e4474fd78cc8eace30c170cd079e4d9', '543333555202901', 'Rustam', 'Atakishiyev', 'ViaRuggeroLeoncovallo', 'Rome', '00199', 'goodluck', '3312058398'),
(3, 'dottcolombo@yahoo.it', 'fa1f908d510c8821950958a8e827a70289fcfa02', '123321', 'Elena Maria', 'Colombo', '', '', '', '', NULL),
(47, 'rustam.atakisiev@gmail.com', '64ec21471774563153f94745b30a0fbc49d005a2', '280557571224948', 'Rustam', 'Atakishiyev', 'Via Ruggero Leoncovallo', 'Rome', '00199', 'goodluck', '3312058398');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barcode`
--
ALTER TABLE `barcode`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `join_user_barcode`
--
ALTER TABLE `join_user_barcode`
  ADD KEY `user` (`user`),
  ADD KEY `barcode` (`barcode`);

--
-- Indexes for table `join_user_product`
--
ALTER TABLE `join_user_product`
  ADD KEY `user` (`user`),
  ADD KEY `product` (`product`);

--
-- Indexes for table `prodcut`
--
ALTER TABLE `prodcut`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `prodcut`
--
ALTER TABLE `prodcut`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
