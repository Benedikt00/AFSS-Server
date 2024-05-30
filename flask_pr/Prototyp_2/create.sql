CREATE TABLE article (
    id INT PRIMARY KEY AUTO_INCREMENT,
    article_name VARCHAR(50),
    article_description TINYTEXT,
    category VARCHAR(20),
    groupes JSON,
    weight INT,
    picture VARCHAR(100)
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

Create Table categories(
	title varchar(50) Primary Key,
    unit varchar(10),
    prefixes JSON
);

Create Table primary_groupes(
	title varchar(50) Primary Key
);

Create Table seondary_groupes(
	prim_title varchar(50),
    title varchar(50),
    foreign key (title) references primary_groupes(title),
    constraint PK_seondary_groupes Primary Key (prim_title, title)
    );

SELECT categories.title AS categories_title, categories.unit AS categories_unit, categories.perfixes AS categories_prefixes FROM categories;

INSERT INTO primary_groupes (title)
VALUES ('Maschinenbau');

INSERT INTO categories (title, unit, prefixes)
VALUES ('Höhe', 'm', '["c", "m", ""]');

Select * from stock;

drop table stock;
drop table container;
drop table location;
drop table area;
drop table article;
drop table categories;
