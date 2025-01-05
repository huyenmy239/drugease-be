-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: drugease
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'pbkdf2_sha256$870000$7yE07kniUJHkWFZvpLHtju$WJU0Nw6Z7TfLErtSbrNrRhNcZnYKHjohzFtB4hPtYnE=','mie',1,'doctor',1);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `account_groups`
--

LOCK TABLES `account_groups` WRITE;
/*!40000 ALTER TABLE `account_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `account_user_permissions`
--

LOCK TABLES `account_user_permissions` WRITE;
/*!40000 ALTER TABLE `account_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add employee',8,'add_employee'),(30,'Can change employee',8,'change_employee'),(31,'Can delete employee',8,'delete_employee'),(32,'Can view employee',8,'view_employee'),(33,'Can add account',9,'add_account'),(34,'Can change account',9,'change_account'),(35,'Can delete account',9,'delete_account'),(36,'Can view account',9,'view_account'),(37,'Can add warehouse',10,'add_warehouse'),(38,'Can change warehouse',10,'change_warehouse'),(39,'Can delete warehouse',10,'delete_warehouse'),(40,'Can view warehouse',10,'view_warehouse'),(41,'Can add export receipt',11,'add_exportreceipt'),(42,'Can change export receipt',11,'change_exportreceipt'),(43,'Can delete export receipt',11,'delete_exportreceipt'),(44,'Can view export receipt',11,'view_exportreceipt'),(45,'Can add import receipt',12,'add_importreceipt'),(46,'Can change import receipt',12,'change_importreceipt'),(47,'Can delete import receipt',12,'delete_importreceipt'),(48,'Can view import receipt',12,'view_importreceipt'),(49,'Can add medicine',13,'add_medicine'),(50,'Can change medicine',13,'change_medicine'),(51,'Can delete medicine',13,'delete_medicine'),(52,'Can view medicine',13,'view_medicine'),(53,'Can add import receipt detail',14,'add_importreceiptdetail'),(54,'Can change import receipt detail',14,'change_importreceiptdetail'),(55,'Can delete import receipt detail',14,'delete_importreceiptdetail'),(56,'Can view import receipt detail',14,'view_importreceiptdetail'),(57,'Can add export receipt detail',15,'add_exportreceiptdetail'),(58,'Can change export receipt detail',15,'change_exportreceiptdetail'),(59,'Can delete export receipt detail',15,'delete_exportreceiptdetail'),(60,'Can view export receipt detail',15,'view_exportreceiptdetail'),(61,'Can add prescription detail',16,'add_prescriptiondetail'),(62,'Can change prescription detail',16,'change_prescriptiondetail'),(63,'Can delete prescription detail',16,'delete_prescriptiondetail'),(64,'Can view prescription detail',16,'view_prescriptiondetail'),(65,'Can add patient',17,'add_patient'),(66,'Can change patient',17,'change_patient'),(67,'Can delete patient',17,'delete_patient'),(68,'Can view patient',17,'view_patient'),(69,'Can add prescription',18,'add_prescription'),(70,'Can change prescription',18,'change_prescription'),(71,'Can delete prescription',18,'delete_prescription'),(72,'Can view prescription',18,'view_prescription');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('2272c3d10b528f5cbe982a1372cbfd9cc76ea79f','2024-12-12 09:06:41.853942',1);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','account'),(8,'accounts','employee'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(17,'prescriptions','patient'),(18,'prescriptions','prescription'),(16,'prescriptions','prescriptiondetail'),(5,'sessions','session'),(11,'warehouse','exportreceipt'),(15,'warehouse','exportreceiptdetail'),(12,'warehouse','importreceipt'),(14,'warehouse','importreceiptdetail'),(13,'warehouse','medicine'),(10,'warehouse','warehouse');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-12-12 05:03:31.943048'),(2,'contenttypes','0002_remove_content_type_name','2024-12-12 05:03:32.026002'),(3,'auth','0001_initial','2024-12-12 05:03:32.234394'),(4,'auth','0002_alter_permission_name_max_length','2024-12-12 05:03:32.284589'),(5,'auth','0003_alter_user_email_max_length','2024-12-12 05:03:32.289219'),(6,'auth','0004_alter_user_username_opts','2024-12-12 05:03:32.293691'),(7,'auth','0005_alter_user_last_login_null','2024-12-12 05:03:32.299308'),(8,'auth','0006_require_contenttypes_0002','2024-12-12 05:03:32.301410'),(9,'auth','0007_alter_validators_add_error_messages','2024-12-12 05:03:32.306351'),(10,'auth','0008_alter_user_username_max_length','2024-12-12 05:03:32.313695'),(11,'auth','0009_alter_user_last_name_max_length','2024-12-12 05:03:32.319143'),(12,'auth','0010_alter_group_name_max_length','2024-12-12 05:03:32.332308'),(13,'auth','0011_update_proxy_permissions','2024-12-12 05:03:32.337763'),(14,'auth','0012_alter_user_first_name_max_length','2024-12-12 05:03:32.342554'),(15,'accounts','0001_initial','2024-12-12 05:03:32.653157'),(16,'admin','0001_initial','2024-12-12 05:03:32.766969'),(17,'admin','0002_logentry_remove_auto_add','2024-12-12 05:03:32.773343'),(18,'admin','0003_logentry_add_action_flag_choices','2024-12-12 05:03:32.781529'),(19,'authtoken','0001_initial','2024-12-12 05:03:32.876915'),(20,'authtoken','0002_auto_20160226_1747','2024-12-12 05:03:32.897940'),(21,'authtoken','0003_tokenproxy','2024-12-12 05:03:32.901180'),(22,'authtoken','0004_alter_tokenproxy_options','2024-12-12 05:03:32.905581'),(23,'prescriptions','0001_initial','2024-12-12 05:03:33.107939'),(24,'warehouse','0001_initial','2024-12-12 05:03:33.713405'),(25,'prescriptions','0002_initial','2024-12-12 05:03:33.834896'),(26,'sessions','0001_initial','2024-12-12 05:03:33.862200'),(27,'prescriptions','0003_patient_insurance_alter_prescription_instruction','2024-12-13 21:29:05.185796'),(28,'prescriptions','0004_patient_nguoi_giam_ho','2024-12-14 04:15:43.636746'),(29,'accounts','0002_employee_is_active','2025-01-03 16:20:22.343195'),(30,'warehouse','0002_remove_medicine_employee_exportreceipt_is_approved_and_more','2025-01-03 16:20:22.648766'),(31,'warehouse','0003_alter_exportreceipt_total_amount_and_more','2025-01-03 20:02:00.826588'),(32,'accounts','0003_alter_employee_image','2025-01-05 05:58:05.980431'),(33,'prescriptions','0005_remove_patient_nguoi_giam_ho','2025-01-05 05:58:06.120496'),(34,'warehouse','0004_alter_exportreceipt_export_date_and_more','2025-01-05 05:58:06.506405');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Nguyễn Thị Huyền My','2003-10-18',0,'087303003841','0363032802','Quận 9','hihi@gmail.com','hihi.png',1),(2,'Nguyễn Thị Thanh Huyến','2003-06-04',0,'056654687878','0642335846','Quận 12','thuyen@gmail.com','hi.png',1);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `export_receipt`
--

LOCK TABLES `export_receipt` WRITE;
/*!40000 ALTER TABLE `export_receipt` DISABLE KEYS */;
INSERT INTO `export_receipt` VALUES (1,120000,'2024-12-12 00:00:00.000000',1,52,1,0);
/*!40000 ALTER TABLE `export_receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `export_receipt_detail`
--

LOCK TABLES `export_receipt_detail` WRITE;
/*!40000 ALTER TABLE `export_receipt_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `export_receipt_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `import_receipt`
--

LOCK TABLES `import_receipt` WRITE;
/*!40000 ALTER TABLE `import_receipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `import_receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `import_receipt_detail`
--

LOCK TABLES `import_receipt_detail` WRITE;
/*!40000 ALTER TABLE `import_receipt_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `import_receipt_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `medicine`
--

LOCK TABLES `medicine` WRITE;
/*!40000 ALTER TABLE `medicine` DISABLE KEYS */;
INSERT INTO `medicine` VALUES (1,'Panadol','Viên',12000,'Liều lượng mạnh',2000),(2,'Extra','Viên',12000,'Mạnh',1200),(3,'Paracetamol','Viên',23000,'Vừa phải',22300);
/*!40000 ALTER TABLE `medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (3,'Tran Quang Hieu','1985-08-22',1,'987654321098','00000000','456 Nguyen Trai, Hanoi','hieuhieu212@exam.com','2024-12-12 10:15:00.000000',1,0.6),(4,'Pham Minh Tuan','1992-03-30',1,'345678901234','0923456789','789 Hai Ba Trung, Da Nang','phamtuan@example.com','2024-12-12 11:30:00.000000',1,0),(6,'Vu Thi Mai','1995-06-10',0,'135792468024','0945678901','654 Tan Binh, Ho Chi Minh','vuthimai@example.com','2024-12-12 14:00:00.000000',1,0),(8,'Doan Minh Duy','1994-09-25',1,'111223344556','0967890123','333 Mai Thi Luu, Da Nang','doanduy@example.com','2024-12-12 16:30:00.000000',1,0),(9,'Phan Minh Chien','1989-12-14',1,'112233445577','0978901234','555 An Duong Vuong, Hue','phanchien@example.com','2024-12-12 17:45:00.000000',1,0),(10,'Nguyen Mai Thanh','1993-07-02',0,'223344556688','0989012345','222 Thanh Hoa, Ho Chi Minh','nguyenmaithanh@example.com','2024-12-12 18:00:00.000000',1,0),(13,'Nguyễn Thị Huyền My','2024-11-28',0,'087303003841','0363032802','Quận 9','test@gmail.com','2024-12-13 03:44:58.967627',1,0),(14,'Tô Phan Kiều Thương','2024-12-18',1,'4423424343','22222222112','562','phanthuong2468@gmail.com','2024-12-13 12:11:46.946224',2,0),(21,'Huyền hay hỏi','1967-12-16',0,'09876543213','098765678','Quận 9','','2024-12-13 19:27:51.437962',1,0),(22,'Hello','2024-12-14',1,'12345678910','067482911','23 nguyễn văn','ththie@gmail.com','2024-12-14 00:46:10.950923',1,0.5),(23,'Helli','2024-12-14',1,'1121111221','012431111','23 nguyễn','Thrh@gmail.com','2024-12-14 00:47:13.435065',1,0),(24,'Tô Phan Kiều Thương','2024-12-14',0,'012365214526','0858950556','quận 2','moaib2222a@gmail.com','2024-12-14 03:15:57.448405',1,0.5),(25,'Trần Hiếu','2024-12-14',1,'012546325412','0215426321','quận 8','phanthuong0200468@gmail.com','2024-12-14 03:20:47.661723',1,1),(26,'Trần Hiếu','2024-12-14',0,'012546325532','0215426666','quận 8','phanth333uong0200468@gmail.com','2024-12-14 03:24:30.707176',1,2),(27,'Trần Hiếu An','2024-12-14',0,'012546325666','0215426523','quận 8','ng0200468@gmail.com','2024-12-14 03:25:01.298047',1,0),(28,'hello','2024-12-14',1,'123456789','0978452154','62 Nguye','Hello@gmail.com','2024-12-14 04:16:33.895617',1,0.5),(29,'chao cac ban','2024-12-14',1,'5478129632','0764708309','26 Ngun','ththieu@gmail.com','2024-12-14 04:28:19.051717',1,0.5),(30,'webservice','2024-12-14',1,'123456654','097451245','ngueen','hello12121@gmail.com','2024-12-14 04:40:32.299925',1,0.5);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES (6,'Viêm mũi','2024-12-24 00:00:00.000000','Uống 1 lần',2,3),(52,'Cảm cúm','2024-12-13 21:08:14.329613','Uống ngày 2 lần',1,3),(54,'Cảm','2024-12-13 21:14:37.943041','Uống ngày 2 lần',1,8),(57,'Sốt, ho sổ mũi','2024-12-13 21:56:59.485141','Uống ngày 2 lần',1,9);
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `prescription_detail`
--

LOCK TABLES `prescription_detail` WRITE;
/*!40000 ALTER TABLE `prescription_detail` DISABLE KEYS */;
INSERT INTO `prescription_detail` VALUES (23,1,'jbjb',1,52),(31,5,'jbjb',1,54),(32,1,'Ngày 2 viên',1,57);
/*!40000 ALTER TABLE `prescription_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
INSERT INTO `warehouse` VALUES (1,'Long Châu','Quận 9',1);
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-05 13:03:23
