drop table if exists genre;
create table genre (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists movie;
create table movie (
  id integer primary key autoincrement,
  imdbID text not null unique,
  title text not null,
  year text not null,
  plot text,
  director text
);

drop table if exists actor;
create table actor (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists movie_genre_through;
CREATE TABLE movie_genre_through (
    movie_id integer,
    genre_id integer,
    foreign key(movie_id) references movie(id) on delete cascade,
    foreign key(genre_id) references genre(id) on delete cascade
);

drop table if exists movie_actor_through;
CREATE TABLE movie_actor_through (
    movie_id integer,
    actor_id integer,
    foreign key(movie_id) references movie(id) on delete cascade,
    foreign key(actor_id) references actor(id) on delete cascade
);
