/*
* Author   : JasonHung
* Date     : 20220717
* Update   : 20230717
* Function : otsuka check card reader
*/

/*
 * database otsuka_invoice_history
 */ 
create database otsuka_card_reader DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_card_reader;

/* 
 * success_record
 */
create table success_record(
no int not null primary key AUTO_INCREMENT,
c_date datetime null,
r_date date null,
r_time time null,
content varchar(100) null,
cpu varchar(10) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* 
 * fail_record
 */
create table fail_record(
no int not null primary key AUTO_INCREMENT,
c_date datetime null,
r_date date null,
r_time time null,
content varchar(100) null,
cpu varchar(10) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

