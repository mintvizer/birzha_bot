create table if not exists birzha
(
    id                     serial not null
        constraint birzha_pk
            primary key,
    ticker                 varchar(30),
    owner           varchar(100),
    relationship           varchar(150),
    date                   varchar(40),
    cost                  double precision,
    shares                    integer,
    value             integer,
    shares_total           integer,
    status                 varchar(10)

);

alter table birzha
    owner to postgres;
