create schema ltm_;

use ltm_;

create table account (
	id int primary key auto_increment,
    username varchar(100),
    password varchar(100)
);

insert into account (username, password) values
('admin', '1234'),
('user', 'pass');
