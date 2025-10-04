CREATE DATABASE `milki4` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `debug_toolbar_historyentry` (
  `request_id` char(32) NOT NULL,
  `data` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `factory_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `logo_url` longtext,
  `company_status` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_company_customer_id_591e5290_fk_factory_customer_id` (`customer_id`),
  CONSTRAINT `factory_company_customer_id_591e5290_fk_factory_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `membership` varchar(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `factory_customer_user_id_5533cd43_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_factory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `location_name` longtext,
  `city` varchar(100) DEFAULT NULL,
  `admin_region` varchar(100) DEFAULT NULL,
  `latitude_point` varchar(100) DEFAULT NULL,
  `longitude_point` varchar(100) DEFAULT NULL,
  `is_operational` tinyint(1) NOT NULL,
  `production_capacity` int DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `company_id` bigint NOT NULL,
  `inputer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_factory_company_id_ac6e705a_fk_factory_company_id` (`company_id`),
  KEY `factory_factory_inputer_id_e4ed8530_fk_factory_customer_id` (`inputer_id`),
  CONSTRAINT `factory_factory_company_id_ac6e705a_fk_factory_company_id` FOREIGN KEY (`company_id`) REFERENCES `factory_company` (`id`),
  CONSTRAINT `factory_factory_inputer_id_e4ed8530_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(50) NOT NULL,
  `invoice_type` varchar(10) NOT NULL,
  `issue_date` datetime(6) NOT NULL,
  `due_date` datetime(6) DEFAULT NULL,
  `total_amount` decimal(14,2) DEFAULT NULL,
  `tax_amount` decimal(12,2) DEFAULT NULL,
  `discount_amount` decimal(12,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  `purchase_order_id` bigint DEFAULT NULL,
  `sales_order_id` bigint DEFAULT NULL,
  `supplier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `factory_invoice_purchase_order_id_b3c419bc_fk_factory_p` (`purchase_order_id`),
  KEY `factory_invoice_sales_order_id_1685e9dd_fk_factory_salesorder_id` (`sales_order_id`),
  KEY `factory_invoice_supplier_id_cfab2ba3_fk_factory_supplier_id` (`supplier_id`),
  KEY `factory_invoice_customer_id_2ec43a4d_fk_factory_customer_id` (`customer_id`),
  CONSTRAINT `factory_invoice_customer_id_2ec43a4d_fk_factory_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_invoice_purchase_order_id_b3c419bc_fk_factory_p` FOREIGN KEY (`purchase_order_id`) REFERENCES `factory_purchaseorder` (`id`),
  CONSTRAINT `factory_invoice_sales_order_id_1685e9dd_fk_factory_salesorder_id` FOREIGN KEY (`sales_order_id`) REFERENCES `factory_salesorder` (`id`),
  CONSTRAINT `factory_invoice_supplier_id_cfab2ba3_fk_factory_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `factory_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_invoiceitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `quantity` int NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `total_price` decimal(14,2) NOT NULL,
  `invoice_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_invoiceitem_invoice_id_a46dc682_fk_factory_invoice_id` (`invoice_id`),
  KEY `factory_invoiceitem_product_id_dd017e18_fk_factory_product_id` (`product_id`),
  CONSTRAINT `factory_invoiceitem_invoice_id_a46dc682_fk_factory_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `factory_invoice` (`id`),
  CONSTRAINT `factory_invoiceitem_product_id_dd017e18_fk_factory_product_id` FOREIGN KEY (`product_id`) REFERENCES `factory_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_date` datetime(6) NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  `reference_number` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `invoice_id` bigint NOT NULL,
  `payer_id` bigint DEFAULT NULL,
  `method_id` bigint NOT NULL,
  `supplier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_payment_invoice_id_8bd4f474_fk_factory_invoice_id` (`invoice_id`),
  KEY `factory_payment_payer_id_a1770aee_fk_factory_customer_id` (`payer_id`),
  KEY `factory_payment_method_id_70e8acd9_fk_factory_paymentmethod_id` (`method_id`),
  KEY `factory_payment_supplier_id_caf3ef10_fk_factory_supplier_id` (`supplier_id`),
  CONSTRAINT `factory_payment_invoice_id_8bd4f474_fk_factory_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `factory_invoice` (`id`),
  CONSTRAINT `factory_payment_method_id_70e8acd9_fk_factory_paymentmethod_id` FOREIGN KEY (`method_id`) REFERENCES `factory_paymentmethod` (`id`),
  CONSTRAINT `factory_payment_payer_id_a1770aee_fk_factory_customer_id` FOREIGN KEY (`payer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_payment_supplier_id_caf3ef10_fk_factory_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `factory_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_paymentmethod` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `method_name` varchar(50) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `method_name` (`method_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `unit_of_measure` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `authorizer_id` bigint DEFAULT NULL,
  `category_id` bigint NOT NULL,
  `company_id` bigint NOT NULL,
  `inputer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `factory_product_authorizer_id_c8cd5c8d_fk_factory_customer_id` (`authorizer_id`),
  KEY `factory_product_category_id_56a77f2a_fk_factory_category_id` (`category_id`),
  KEY `factory_product_company_id_2be2f52c_fk_factory_company_id` (`company_id`),
  KEY `factory_product_inputer_id_03bf1d3e_fk_factory_customer_id` (`inputer_id`),
  CONSTRAINT `factory_product_authorizer_id_c8cd5c8d_fk_factory_customer_id` FOREIGN KEY (`authorizer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_product_category_id_56a77f2a_fk_factory_category_id` FOREIGN KEY (`category_id`) REFERENCES `factory_category` (`id`),
  CONSTRAINT `factory_product_company_id_2be2f52c_fk_factory_company_id` FOREIGN KEY (`company_id`) REFERENCES `factory_company` (`id`),
  CONSTRAINT `factory_product_inputer_id_03bf1d3e_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_purchaseorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `placed_at` datetime(6) NOT NULL,
  `order_status` varchar(30) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorized_at` datetime(6) DEFAULT NULL,
  `authorizer_id` bigint NOT NULL,
  `inputer_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_purchaseorde_supplier_id_1adfa5af_fk_factory_s` (`supplier_id`),
  KEY `factory_purchaseorde_authorizer_id_6df04cc4_fk_factory_c` (`authorizer_id`),
  KEY `factory_purchaseorder_inputer_id_4c428dc8_fk_factory_customer_id` (`inputer_id`),
  CONSTRAINT `factory_purchaseorde_authorizer_id_6df04cc4_fk_factory_c` FOREIGN KEY (`authorizer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_purchaseorde_supplier_id_1adfa5af_fk_factory_s` FOREIGN KEY (`supplier_id`) REFERENCES `factory_supplier` (`id`),
  CONSTRAINT `factory_purchaseorder_inputer_id_4c428dc8_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_purchaseorderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_date` datetime(6) DEFAULT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `factory_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `purchase_order_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL,
  `warehouse_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_purchaseorde_factory_id_5bdd2c1b_fk_factory_f` (`factory_id`),
  KEY `factory_purchaseorde_product_id_a1bbb5a1_fk_factory_p` (`product_id`),
  KEY `factory_purchaseorde_purchase_order_id_3f6ef3fb_fk_factory_p` (`purchase_order_id`),
  KEY `factory_purchaseorde_supplier_id_f0a1775c_fk_factory_s` (`supplier_id`),
  KEY `factory_purchaseorde_warehouse_id_f8aed653_fk_factory_w` (`warehouse_id`),
  CONSTRAINT `factory_purchaseorde_factory_id_5bdd2c1b_fk_factory_f` FOREIGN KEY (`factory_id`) REFERENCES `factory_factory` (`id`),
  CONSTRAINT `factory_purchaseorde_product_id_a1bbb5a1_fk_factory_p` FOREIGN KEY (`product_id`) REFERENCES `factory_product` (`id`),
  CONSTRAINT `factory_purchaseorde_purchase_order_id_3f6ef3fb_fk_factory_p` FOREIGN KEY (`purchase_order_id`) REFERENCES `factory_purchaseorder` (`id`),
  CONSTRAINT `factory_purchaseorde_supplier_id_f0a1775c_fk_factory_s` FOREIGN KEY (`supplier_id`) REFERENCES `factory_supplier` (`id`),
  CONSTRAINT `factory_purchaseorde_warehouse_id_f8aed653_fk_factory_w` FOREIGN KEY (`warehouse_id`) REFERENCES `factory_warehouse` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_salesorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `placed_at` datetime(6) NOT NULL,
  `order_status` varchar(30) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `authorizer_id` bigint DEFAULT NULL,
  `inputer_id` bigint DEFAULT NULL,
  `to_customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_salesorder_authorizer_id_9a95c6b7_fk_factory_customer_id` (`authorizer_id`),
  KEY `factory_salesorder_inputer_id_43345748_fk_factory_customer_id` (`inputer_id`),
  KEY `factory_salesorder_to_customer_id_8fbd00e2_fk_factory_c` (`to_customer_id`),
  CONSTRAINT `factory_salesorder_authorizer_id_9a95c6b7_fk_factory_customer_id` FOREIGN KEY (`authorizer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_salesorder_inputer_id_43345748_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_salesorder_to_customer_id_8fbd00e2_fk_factory_c` FOREIGN KEY (`to_customer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_salesorderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `total_price` decimal(14,2) NOT NULL,
  `factory_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `sales_order_id` bigint NOT NULL,
  `warehouse_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_salesorderitem_factory_id_c0700654_fk_factory_factory_id` (`factory_id`),
  KEY `factory_salesorderitem_product_id_e31bf83f_fk_factory_product_id` (`product_id`),
  KEY `factory_salesorderit_sales_order_id_5d7d3ad2_fk_factory_s` (`sales_order_id`),
  KEY `factory_salesorderit_warehouse_id_bce5f913_fk_factory_w` (`warehouse_id`),
  CONSTRAINT `factory_salesorderit_sales_order_id_5d7d3ad2_fk_factory_s` FOREIGN KEY (`sales_order_id`) REFERENCES `factory_salesorder` (`id`),
  CONSTRAINT `factory_salesorderit_warehouse_id_bce5f913_fk_factory_w` FOREIGN KEY (`warehouse_id`) REFERENCES `factory_warehouse` (`id`),
  CONSTRAINT `factory_salesorderitem_factory_id_c0700654_fk_factory_factory_id` FOREIGN KEY (`factory_id`) REFERENCES `factory_factory` (`id`),
  CONSTRAINT `factory_salesorderitem_product_id_e31bf83f_fk_factory_product_id` FOREIGN KEY (`product_id`) REFERENCES `factory_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_stock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unit_price` decimal(12,2) DEFAULT NULL,
  `quantity` int NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `authorizer_id` bigint NOT NULL,
  `inputer_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `warehouse_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `factory_stock_warehouse_id_product_id_8fcd8cd9_uniq` (`warehouse_id`,`product_id`),
  KEY `factory_stock_authorizer_id_54ab55d6_fk_factory_customer_id` (`authorizer_id`),
  KEY `factory_stock_inputer_id_354764b1_fk_factory_customer_id` (`inputer_id`),
  KEY `factory_stock_product_id_90e6508a_fk_factory_product_id` (`product_id`),
  CONSTRAINT `factory_stock_authorizer_id_54ab55d6_fk_factory_customer_id` FOREIGN KEY (`authorizer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_stock_inputer_id_354764b1_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_stock_product_id_90e6508a_fk_factory_product_id` FOREIGN KEY (`product_id`) REFERENCES `factory_product` (`id`),
  CONSTRAINT `factory_stock_warehouse_id_bd66f3f1_fk_factory_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `factory_warehouse` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_stockmovementlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mdate` datetime(6) NOT NULL,
  `unit_price` decimal(12,2) DEFAULT NULL,
  `quantity` int unsigned NOT NULL,
  `movement_type` varchar(10) NOT NULL,
  `remarks` longtext,
  `status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `logged_at` datetime(6) NOT NULL,
  `authorizer_id` bigint DEFAULT NULL,
  `destination_factory_id` bigint NOT NULL,
  `inputer_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  `source_factory_id` bigint NOT NULL,
  `destination_warehouse_id` bigint NOT NULL,
  `source_warehouse_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_stockmovemen_authorizer_id_9738e05a_fk_factory_c` (`authorizer_id`),
  KEY `factory_stockmovemen_destination_factory__03ba3e12_fk_factory_f` (`destination_factory_id`),
  KEY `factory_stockmovemen_inputer_id_73c3efbc_fk_factory_c` (`inputer_id`),
  KEY `factory_stockmovemen_product_id_73a71235_fk_factory_p` (`product_id`),
  KEY `factory_stockmovemen_source_factory_id_cc5ffa03_fk_factory_f` (`source_factory_id`),
  KEY `factory_stockmovemen_destination_warehous_cc1cbcd7_fk_factory_w` (`destination_warehouse_id`),
  KEY `factory_stockmovemen_source_warehouse_id_06a56f0c_fk_factory_w` (`source_warehouse_id`),
  CONSTRAINT `factory_stockmovemen_authorizer_id_9738e05a_fk_factory_c` FOREIGN KEY (`authorizer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_stockmovemen_destination_factory__03ba3e12_fk_factory_f` FOREIGN KEY (`destination_factory_id`) REFERENCES `factory_factory` (`id`),
  CONSTRAINT `factory_stockmovemen_destination_warehous_cc1cbcd7_fk_factory_w` FOREIGN KEY (`destination_warehouse_id`) REFERENCES `factory_warehouse` (`id`),
  CONSTRAINT `factory_stockmovemen_inputer_id_73c3efbc_fk_factory_c` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_stockmovemen_product_id_73a71235_fk_factory_p` FOREIGN KEY (`product_id`) REFERENCES `factory_product` (`id`),
  CONSTRAINT `factory_stockmovemen_source_factory_id_cc5ffa03_fk_factory_f` FOREIGN KEY (`source_factory_id`) REFERENCES `factory_factory` (`id`),
  CONSTRAINT `factory_stockmovemen_source_warehouse_id_06a56f0c_fk_factory_w` FOREIGN KEY (`source_warehouse_id`) REFERENCES `factory_warehouse` (`id`),
  CONSTRAINT `factory_stockmovementlog_quantity_48ca6e96_check` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_supplier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(100) NOT NULL,
  `supplier_contact_person` varchar(100) DEFAULT NULL,
  `supplier_phone` varchar(20) DEFAULT NULL,
  `supplier_email` varchar(100) DEFAULT NULL,
  `supplier_address` longtext,
  `supplier_status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `company_id` bigint NOT NULL,
  `inputer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_supplier_company_id_7d35863a_fk_factory_company_id` (`company_id`),
  KEY `factory_supplier_inputer_id_6bb805ee_fk_factory_customer_id` (`inputer_id`),
  CONSTRAINT `factory_supplier_company_id_7d35863a_fk_factory_company_id` FOREIGN KEY (`company_id`) REFERENCES `factory_company` (`id`),
  CONSTRAINT `factory_supplier_inputer_id_6bb805ee_fk_factory_customer_id` FOREIGN KEY (`inputer_id`) REFERENCES `factory_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `factory_warehouse` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `capacity` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `is_authorized` tinyint(1) NOT NULL,
  `authorization_time` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `authorized_by_id` bigint DEFAULT NULL,
  `factory_id` bigint NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `factory_warehouse_authorized_by_id_650dcc5e_fk_factory_c` (`authorized_by_id`),
  KEY `factory_warehouse_factory_id_d28bf688_fk_factory_factory_id` (`factory_id`),
  CONSTRAINT `factory_warehouse_authorized_by_id_650dcc5e_fk_factory_c` FOREIGN KEY (`authorized_by_id`) REFERENCES `factory_customer` (`id`),
  CONSTRAINT `factory_warehouse_factory_id_d28bf688_fk_factory_factory_id` FOREIGN KEY (`factory_id`) REFERENCES `factory_factory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


