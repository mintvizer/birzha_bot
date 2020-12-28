create table if not exists birzha
(
    id                     serial not null
        constraint birzha_pk
            primary key,
    ticker                 varchar(30),
    company_name           varchar(100),
    insider_name           varchar(150),
    price                  double precision,
    date                   varchar(40),
    insider_trading_shares integer,
    marcet_cap             varchar(50),
    status                 varchar(10),
    insider_position           varchar(150)

);

alter table birzha
    owner to postgres;
