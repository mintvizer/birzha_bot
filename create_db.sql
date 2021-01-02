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
    transaction         varchar(30),
    shares_total           integer,
    status                 varchar(10)

);
create table if not exists ticket_sale
(
	id serial
		constraint ticket_sale_pk
			primary key,
	ticket varchar(50)
);
