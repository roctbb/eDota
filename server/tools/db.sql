create table players
(
    id    serial
        constraint players_pk
            primary key,
    name  varchar(255),
    key   varchar(20),
    state varchar(50) default 'waiting'::character varying,
    code  text
);