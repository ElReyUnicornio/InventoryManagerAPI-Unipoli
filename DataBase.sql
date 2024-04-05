Drop database if exists `inventory`;
create database `inventory`;
use `inventory`;

create table categories (
  `id` int(11) not null auto_increment,
  `name` varchar(255) not null,
  primary key (`id`)
) engine=InnoDB default charset=utf8;

create table `products` (
  `id` int(11) not null auto_increment,
  `name` varchar(255) not null,
  `description` varchar(255) not null,
  `category` int(11) not null,
  `stock` int(11) not null,
  primary key (`id`),
  foreign key (`category`) references `categories` (`id`)
) engine=InnoDB default charset=utf8;

create table `users` (
  `name` varchar(255) not null,
  `enrollment` varchar(10) not null,
  `password` varchar(255) not null,
  `role` ENUM('Admin', 'Student') not null,
  `carreer` varchar(255),
  `quarter` int(11),
  `position` varchar(255),
  primary key (`enrollment`)
) engine=InnoDB default charset=utf8;

create table `logs` (
  `id` int(11) not null auto_increment,
  `date` datetime not null,
  `description` varchar(255) not null,
  `user` varchar(10) not null,
  primary key (`id`),
  foreign key (`user`) references `users` (`enrollment`)
) engine=InnoDB default charset=utf8;

-- categories default data
insert into `categories` (`name`) values ('Periféricos');
insert into `categories` (`name`) values ('Hardware');
insert into `categories` (`name`) values ('Software');
insert into `categories` (`name`) values ('Dispositivos');

-- users default data
insert into `users` (`name`, `enrollment`, `password`, `role`, `carreer`, `quarter`, `position`) values ('Alejandro', '2303150187', '$2b$12$iMaHOVSOAS7oBSOMJ.BV0O3ny1o8ZdlbMErTvYwgIC36objgQiu9W', 'Admin', '', 0, 'Admin');

-- products default data
insert into `products` (`name`, `description`, `category`, `stock`) values ('Mouse', 'Mouse inalámbrico', 1, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('Teclado', 'Teclado inalámbrico', 1, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('Monitor', 'Monitor 24 pulgadas', 1, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('CPU', 'CPU i7 8va generación', 2, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('RAM', 'RAM 8GB DDR4', 2, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('Windows', 'Windows 10', 3, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('Linux', 'Ubuntu 18.04', 3, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('MacOS', 'MacOS Mojave', 3, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('USB', 'USB 3.0 16GB', 4, 10);
insert into `products` (`name`, `description`, `category`, `stock`) values ('Disco duro', 'Disco duro 1TB', 4, 10);