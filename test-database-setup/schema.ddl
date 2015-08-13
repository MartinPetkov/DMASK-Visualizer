drop schema if exists sophiadmask cascade;
create schema sophiadmask;
set search_path to sophiadmask;

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
