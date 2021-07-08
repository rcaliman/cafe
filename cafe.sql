-- MariaDB dump 10.19  Distrib 10.5.10-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cafe
-- ------------------------------------------------------
-- Server version	10.5.10-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cafe`
--

DROP TABLE IF EXISTS `cafe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cafe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` tinytext NOT NULL,
  `quantidade_comprada` float NOT NULL,
  `data_compra` date NOT NULL,
  `origem` tinytext NOT NULL,
  `estoque` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cafe`
--

LOCK TABLES `cafe` WRITE;
/*!40000 ALTER TABLE `cafe` DISABLE KEYS */;
INSERT INTO `cafe` VALUES (6,'Cascão',2000,'2020-06-01','Manhuaçu (Fauze)',1),(16,'Café Lemita, 85 pontos, Mercado Livre, 970 m, Frutas Vermelhas e Mel',6000,'2021-04-24','Paraguaçu, Sul de Minas Gerais',1),(17,'Robusta Amazonico, 84 Pontos, Poliana Perrut de Lima',3000,'2021-06-11','Novo Horizonte do Oeste, RO',1);
/*!40000 ALTER TABLE `cafe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `torra`
--

DROP TABLE IF EXISTS `torra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `torra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cafe` int(11) NOT NULL,
  `temp_inicial` float DEFAULT NULL,
  `temp_final` float DEFAULT NULL,
  `temp_piso` float DEFAULT NULL,
  `temp_minutos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`temp_minutos`)),
  `fluxo_ar` float DEFAULT NULL,
  `velocidade_tambor` float DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `data_torra` date DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `torra_id_cafe_cafe_id` (`id_cafe`),
  CONSTRAINT `torra_id_cafe_cafe_id` FOREIGN KEY (`id_cafe`) REFERENCES `cafe` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `torra`
--

LOCK TABLES `torra` WRITE;
/*!40000 ALTER TABLE `torra` DISABLE KEYS */;
INSERT INTO `torra` VALUES (55,16,190,208,106,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"108\"], \"tempgrid2\": [\"113\"], \"tempgrid3\": [\"125\"], \"tempgrid4\": [\"131\"], \"tempgrid5\": [\"134\"], \"tempgrid6\": [\"138\"], \"tempgrid7\": [\"141\"], \"tempgrid8\": [\"144\"], \"tempgrid9\": [\"146\"], \"tempgrid10\": [\"149\"], \"tempgrid11\": [\"152\"], \"tempgrid12\": [\"158\"], \"tempgrid13\": [\"162\"], \"tempgrid14\": [\"163\"], \"tempgrid15\": [\"167\"], \"tempgrid16\": [\"171\"], \"tempgrid17\": [\"174\"], \"tempgrid18\": [\"175\"], \"tempgrid19\": [\"178\"], \"tempgrid20\": [\"179\"], \"tempgrid21\": [\"181\"], \"tempgrid22\": [\"187\"], \"tempgrid23\": [\"194\"], \"tempgrid24\": [\"200\"], \"tempgrid25\": [\"208\"]}',80,40,400,'2021-07-07',NULL),(56,16,190,204,107,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"107\"], \"tempgrid2\": [\"118\"], \"tempgrid3\": [\"128\"], \"tempgrid4\": [\"139\"], \"tempgrid5\": [\"147\"], \"tempgrid6\": [\"155\"], \"tempgrid7\": [\"162\"], \"tempgrid8\": [\"170\"], \"tempgrid9\": [\"179\"], \"tempgrid10\": [\"187\"], \"tempgrid11\": [\"194\"], \"tempgrid12\": [\"197\"], \"tempgrid13\": [\"197\"], \"tempgrid14\": [\"199\"], \"tempgrid15\": [\"202\"], \"tempgrid16\": [\"204\"], \"tempgrid17\": [\"203\"], \"tempgrid18\": [\"204\"], \"tempgrid19\": [\"204\"]}',60,40,400,'2021-07-07',NULL),(57,6,190,198,96,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"118\"], \"tempgrid2\": [\"96\"], \"tempgrid3\": [\"106\"], \"tempgrid4\": [\"115\"], \"tempgrid5\": [\"127\"], \"tempgrid6\": [\"137\"], \"tempgrid7\": [\"145\"], \"tempgrid8\": [\"151\"], \"tempgrid9\": [\"156\"], \"tempgrid10\": [\"160\"], \"tempgrid11\": [\"162\"], \"tempgrid12\": [\"165\"], \"tempgrid13\": [\"168\"], \"tempgrid14\": [\"172\"], \"tempgrid15\": [\"176\"], \"tempgrid16\": [\"179\"], \"tempgrid17\": [\"185\"], \"tempgrid18\": [\"187\"], \"tempgrid19\": [\"191\"], \"tempgrid20\": [\"195\"], \"tempgrid21\": [\"197\"], \"tempgrid22\": [\"198\"]}',80,40,400,'2021-06-23',NULL),(58,6,190,204,160,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"164\"], \"tempgrid2\": [\"160\"], \"tempgrid3\": [\"166\"], \"tempgrid4\": [\"167\"], \"tempgrid5\": [\"167\"], \"tempgrid6\": [\"168\"], \"tempgrid7\": [\"170\"], \"tempgrid8\": [\"172\"], \"tempgrid9\": [\"175\"], \"tempgrid10\": [\"176\"], \"tempgrid11\": [\"177\"], \"tempgrid12\": [\"177\"], \"tempgrid13\": [\"177\"], \"tempgrid14\": [\"178\"], \"tempgrid15\": [\"178\"], \"tempgrid16\": [\"179\"], \"tempgrid17\": [\"179\"], \"tempgrid18\": [\"180\"], \"tempgrid19\": [\"181\"], \"tempgrid20\": [\"182\"], \"tempgrid21\": [\"183\"], \"tempgrid22\": [\"184\"], \"tempgrid23\": [\"185\"], \"tempgrid24\": [\"192\"], \"tempgrid25\": [\"198\"], \"tempgrid26\": [\"204\"]}',80,40,250,'2021-07-07',NULL),(59,16,190,207,102,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"102\"], \"tempgrid2\": [\"103\"], \"tempgrid3\": [\"107\"], \"tempgrid4\": [\"118\"], \"tempgrid5\": [\"130\"], \"tempgrid6\": [\"140\"], \"tempgrid7\": [\"144\"], \"tempgrid8\": [\"147\"], \"tempgrid9\": [\"150\"], \"tempgrid10\": [\"152\"], \"tempgrid11\": [\"154\"], \"tempgrid12\": [\"157\"], \"tempgrid13\": [\"159\"], \"tempgrid14\": [\"162\"], \"tempgrid15\": [\"167\"], \"tempgrid16\": [\"170\"], \"tempgrid17\": [\"171\"], \"tempgrid18\": [\"171\"], \"tempgrid19\": [\"173\"], \"tempgrid20\": [\"176\"], \"tempgrid21\": [\"180\"], \"tempgrid22\": [\"187\"], \"tempgrid23\": [\"195\"], \"tempgrid24\": [\"204\"], \"tempgrid25\": [\"207\"]}',80,40,400,'2021-07-07',NULL),(60,16,190,219,104,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"106\"], \"tempgrid2\": [\"108\"], \"tempgrid3\": [\"119\"], \"tempgrid4\": [\"129\"], \"tempgrid5\": [\"137\"], \"tempgrid6\": [\"143\"], \"tempgrid7\": [\"145\"], \"tempgrid8\": [\"146\"], \"tempgrid9\": [\"146\"], \"tempgrid10\": [\"149\"], \"tempgrid11\": [\"154\"], \"tempgrid12\": [\"159\"], \"tempgrid13\": [\"165\"], \"tempgrid14\": [\"168\"], \"tempgrid15\": [\"170\"], \"tempgrid16\": [\"171\"], \"tempgrid17\": [\"174\"], \"tempgrid18\": [\"177\"], \"tempgrid19\": [\"179\"], \"tempgrid20\": [\"180\"], \"tempgrid21\": [\"183\"], \"tempgrid22\": [\"189\"], \"tempgrid23\": [\"196\"], \"tempgrid24\": [\"203\"], \"tempgrid25\": [\"207\"], \"tempgrid26\": [\"215\"], \"tempgrid27\": [\"219\"]}',80,40,400,'2021-05-22',NULL),(61,17,190,213,116,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"120\"], \"tempgrid2\": [\"119\"], \"tempgrid3\": [\"129\"], \"tempgrid4\": [\"135\"], \"tempgrid5\": [\"140\"], \"tempgrid6\": [\"148\"], \"tempgrid7\": [\"154\"], \"tempgrid8\": [\"161\"], \"tempgrid9\": [\"167\"], \"tempgrid10\": [\"174\"], \"tempgrid11\": [\"179\"], \"tempgrid12\": [\"185\"], \"tempgrid13\": [\"190\"], \"tempgrid14\": [\"193\"], \"tempgrid15\": [\"199\"], \"tempgrid16\": [\"203\"], \"tempgrid17\": [\"207\"], \"tempgrid18\": [\"208\"], \"tempgrid19\": [\"208\"], \"tempgrid20\": [\"209\"], \"tempgrid21\": [\"209\"], \"tempgrid22\": [\"209\"], \"tempgrid23\": [\"211\"], \"tempgrid24\": [\"212\"], \"tempgrid25\": [\"213\"]}',80,40,400,'2021-06-16',NULL),(62,6,190,213,147,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"158\"], \"tempgrid2\": [\"147\"], \"tempgrid3\": [\"147\"], \"tempgrid4\": [\"150\"], \"tempgrid5\": [\"154\"], \"tempgrid6\": [\"158\"], \"tempgrid7\": [\"162\"], \"tempgrid8\": [\"165\"], \"tempgrid9\": [\"168\"], \"tempgrid10\": [\"173\"], \"tempgrid11\": [\"178\"], \"tempgrid12\": [\"184\"], \"tempgrid13\": [\"189\"], \"tempgrid14\": [\"189\"], \"tempgrid15\": [\"189\"], \"tempgrid16\": [\"188\"], \"tempgrid17\": [\"188\"], \"tempgrid18\": [\"188\"], \"tempgrid19\": [\"189\"], \"tempgrid20\": [\"190\"], \"tempgrid21\": [\"191\"], \"tempgrid22\": [\"192\"], \"tempgrid23\": [\"193\"], \"tempgrid24\": [\"194\"], \"tempgrid25\": [\"198\"], \"tempgrid26\": [\"202\"], \"tempgrid27\": [\"206\"], \"tempgrid28\": [\"209\"], \"tempgrid29\": [\"213\"]}',80,40,250,'2021-05-26','segunda torra'),(63,16,190,203,111,'{\"tempgrid0\": [\"190\"], \"tempgrid1\": [\"113\"], \"tempgrid2\": [\"122\"], \"tempgrid3\": [\"128\"], \"tempgrid4\": [\"132\"], \"tempgrid5\": [\"136\"], \"tempgrid6\": [\"139\"], \"tempgrid7\": [\"143\"], \"tempgrid8\": [\"146\"], \"tempgrid9\": [\"149\"], \"tempgrid10\": [\"151\"], \"tempgrid11\": [\"155\"], \"tempgrid12\": [\"158\"], \"tempgrid13\": [\"160\"], \"tempgrid14\": [\"163\"], \"tempgrid15\": [\"166\"], \"tempgrid16\": [\"168\"], \"tempgrid17\": [\"171\"], \"tempgrid18\": [\"173\"], \"tempgrid19\": [\"180\"], \"tempgrid20\": [\"185\"], \"tempgrid21\": [\"190\"], \"tempgrid22\": [\"195\"], \"tempgrid23\": [\"199\"], \"tempgrid24\": [\"203\"]}',80,40,400,'2021-07-07',NULL);
/*!40000 ALTER TABLE `torra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `senha` varchar(100) DEFAULT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

----LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
---- INSERT INTO `usuarios` VALUES (2,'usuario','senha','nome completo','email');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
----UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-07 23:29:21
