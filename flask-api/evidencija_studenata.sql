-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 05, 2024 at 02:08 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `evidencija_studenata`
--

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `lozinka` varchar(500) NOT NULL,
  `rola` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `ime`, `prezime`, `email`, `lozinka`, `rola`) VALUES
(1, 'Petar', 'Petrović', 'test@test.com', 'scrypt:32768:8:1$LSrKOyFZ4KAEgCHl$3f69b9ab5666b99314526587e704891bd09cbafff4cd01c28484a00a8016a80b0958a2ed2314550dceabc577c189dbed64fec7063dcf0eab29639697b5dfd7d4', 'profesor'),
(10, 'Administrator', 'Administrator', 'test2@test.com', 'scrypt:32768:8:1$mmpQlc1kiiWXhURW$b069d8183f6ccaf801905826b3cade16526b65ccf66fe515290692198156b10eda1d69eae7d920cf67b8130098e786be5320cf8bc08a7f7b1f99180dc85b3413', 'administrator');

-- --------------------------------------------------------

--
-- Table structure for table `ocene`
--

CREATE TABLE `ocene` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `predmet_id` int(11) NOT NULL,
  `ocena` smallint(6) NOT NULL,
  `datum` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ocene`
--

INSERT INTO `ocene` (`id`, `student_id`, `predmet_id`, `ocena`, `datum`) VALUES
(33, 34, 14, 10, '2023-01-20'),
(34, 34, 13, 10, '2023-06-20'),
(35, 35, 14, 9, '2023-01-20');

-- --------------------------------------------------------

--
-- Table structure for table `predmeti`
--

CREATE TABLE `predmeti` (
  `id` int(11) NOT NULL,
  `sifra` varchar(30) NOT NULL,
  `naziv` varchar(50) NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `espb` int(11) NOT NULL,
  `obavezni_izborni` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `predmeti`
--

INSERT INTO `predmeti` (`id`, `sifra`, `naziv`, `godina_studija`, `espb`, `obavezni_izborni`) VALUES
(13, 'MAT2', 'Matematika 2', 1, 7, 'obavezni'),
(14, 'MAT1', 'Matematika 1', 1, 7, 'obavezni'),
(24, 'KSS1', 'Klijent server sistemi', 3, 8, 'obavezni'),
(25, 'VEB1', 'Veb programiranje', 3, 6, 'obavezni'),
(26, 'NET1', 'NET tehnologije', 3, 6, 'obavezni');

-- --------------------------------------------------------

--
-- Table structure for table `studenti`
--

CREATE TABLE `studenti` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) NOT NULL,
  `prezime` varchar(100) NOT NULL,
  `broj_indeksa` varchar(10) NOT NULL,
  `godina_studija` smallint(6) NOT NULL,
  `jmbg` varchar(20) NOT NULL,
  `datum_rodjenja` date NOT NULL,
  `espb` int(11) NOT NULL,
  `prosek_ocena` float(10,2) NOT NULL,
  `broj_telefona` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `ime_roditelja` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `studenti`
--

INSERT INTO `studenti` (`id`, `ime`, `prezime`, `broj_indeksa`, `godina_studija`, `jmbg`, `datum_rodjenja`, `espb`, `prosek_ocena`, `broj_telefona`, `email`, `ime_roditelja`) VALUES
(34, 'Marko', 'Marković', 'SRT 01/22', 3, '1212003735021', '2003-12-12', 14, 10.00, '06112345678', 'marko@marko.com', 'Željko'),
(35, 'Ivana', 'Ivanović', 'SRT 02/22', 3, '1111003735046', '2003-11-11', 7, 9.00, '06212345678', 'ivana@ivana.com', 'Dragan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ocene`
--
ALTER TABLE `ocene`
  ADD PRIMARY KEY (`id`),
  ADD KEY `foreign_predmeti` (`predmet_id`),
  ADD KEY `foreign_studenti` (`student_id`);

--
-- Indexes for table `predmeti`
--
ALTER TABLE `predmeti`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `studenti`
--
ALTER TABLE `studenti`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `ocene`
--
ALTER TABLE `ocene`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `predmeti`
--
ALTER TABLE `predmeti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `studenti`
--
ALTER TABLE `studenti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ocene`
--
ALTER TABLE `ocene`
  ADD CONSTRAINT `foreign_predmeti` FOREIGN KEY (`predmet_id`) REFERENCES `predmeti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `foreign_studenti` FOREIGN KEY (`student_id`) REFERENCES `studenti` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
