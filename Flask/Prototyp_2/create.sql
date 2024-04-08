CREATE TABLE article (
    id INT PRIMARY KEY AUTO_INCREMENT,
    article_name VARCHAR(50),
    article_description TINYTEXT,
    category VARCHAR(20),
    groupes VARCHAR(50),
    weight INT,
    picture VARCHAR(30)
);

create Table area (
	id int primary key AUTO_INCREMENT,
    name varchar(20),
    max_cont INT,
    allocated_cont INT
);

Create Table location (
	id int primary key AUTO_INCREMENT,
    area int,
    category varchar(20),
    occupation_status bool NOT NULL,
    size varchar(10),
    position JSON,
    foreign key (area) references area(id)
);

CREATE TABLE container (
	id INT primary key AUTO_INCREMENT,
    stocks JSON,
    barcode bigint unsigned,
    current_location INT NOT NULL,
    target_location INT,
    size varchar(10),
    foreign key (current_location) references location(id),
    foreign key (target_location) references location(id)
);

CREATE TABLE stock (
	id INT PRIMARY KEY AUTO_INCREMENT,
	container INT,
    article INT,
    quantity INT,
    foreign key (container) references container(id),
    foreign key (article) references article(id)
);


drop table stock;
drop table container;
drop table location;
drop table area;
drop table article;

