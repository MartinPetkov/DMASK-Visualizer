drop table if exists Student cascade;
drop table if exists Course cascade;
drop table if exists Offering cascade;
drop table if exists Took cascade;

create table Student(
        sid integer,
        firstName varchar(128),
        email varchar(128),
        cgpa real
);

create table Course(
        dept varchar(128),
        cNum integer,
        name varchar(128)
);

create table Offering(
        oid integer,
        dept varchar(128),
        cNum integer,
        instructor varchar(128)
);

create table Took(
        sid integer,
        oid integer,
        grade integer
);
