drop table if exists genres;
create table genres (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists movies;
create table movies (
  id integer primary key autoincrement,
  imdbID text not null unique,
  title text not null,
  year text not null,
  plot text,
  director text
);

drop table if exists actors;
create table actors (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists movies_genres;
CREATE TABLE movies_genres (
    movie_id integer,
    genre_id integer,
    foreign key(movie_id) references movies(id) on delete cascade,
    foreign key(genre_id) references genres(id) on delete cascade
);

drop table if exists movies_actors;
CREATE TABLE movies_actors (
    movie_id integer,
    actors_id integer,
    foreign key(movie_id) references movies(id) on delete cascade,
    foreign key(actors_id) references actors(id) on delete cascade
);
