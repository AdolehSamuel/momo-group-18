CREATE TABLE `Transactions` (
  `transaction_id` INT,AUTO_INTREMENCT,
  `receiver_id` VARCHAR(20),
  `sender_id` string,
  `amount` Decimal,
  `currency` String,
  `Transactiondate` datetime,
  PRIMARY KEY (`transaction_id`)
);

CREATE TABLE `Users` (
  `user_id` INT ,
  `phone number` VARCHAR,
  `name` VARCHAR,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `Transaction_categories` (
  `category_id` INT,
  `category_name` VARCHAR,
  `description` Text,
  PRIMARY KEY (`category_id`)
);

CREATE TABLE `System_logs` (
  `log_id` INT,
  `message` Text,
  `log_type` Enum,
  `timestamp` Datetime,
  PRIMARY KEY (`log_id`),
  FOREIGN KEY (`message`)
      REFERENCES `Transaction_categories`(`description`)
);

