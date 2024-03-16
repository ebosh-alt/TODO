create table tasks(
    id      integer primary key,
    user_id integer,
    title varchar(255),
    description varchar(1024)
);
