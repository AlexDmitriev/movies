import requests, codecs, json, sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

f = codecs.open('data/top50.txt', 'r', 'UTF-8')

for line in f:
    name = line.rstrip('\n')
    resp = requests.get('http://www.omdbapi.com/?t=%s' % name)

    if resp.status_code != 200:
        print "API error"
    else:
        movie = json.loads(resp.text)

        if "imdbID" in movie.keys():
            movie_genres = []
            movie_actors = []

            c.execute("SELECT * FROM movie WHERE imdbID = '%s'" % movie['imdbID'])
            db_movie = c.fetchone()

            if db_movie is None:

                c.execute('INSERT INTO movie (imdbID, title, year, plot, director) values ("%s", "%s", "%s", "%s", "%s")'
                    % (movie['imdbID'], movie['Title'], movie['Year'], movie['Plot'], movie['Director']))
                conn.commit()
                movie_id = c.lastrowid

                if "Genre" in movie.keys():
                    genres = movie['Genre'].split(",")
                    for genre in genres:
                        c.execute('SELECT * FROM genre WHERE name = "%s"' % genre.strip())
                        db_genre = c.fetchone()
                        if db_genre:
                            movie_genres.append((movie_id, db_genre[0]))
                        else:
                            c.execute('INSERT INTO genre (name) VALUES("%s")' % genre.strip())
                            conn.commit()
                            movie_genres.append((movie_id, c.lastrowid))

                    for g in movie_genres:
                        c.execute('insert into movie_genre_through values (?,?)', g)
                        conn.commit()


                if "Actors" in movie.keys():
                    actors = movie['Actors'].split(",")
                    for actor in actors:
                        c.execute('SELECT * FROM actor WHERE name = "%s"' % actor.strip())
                        db_actor = c.fetchone()
                        if db_actor:
                            movie_actors.append((movie_id, db_actor[0]))
                        else:
                            c.execute('INSERT INTO actor (name) VALUES("%s")' % actor.strip())
                            conn.commit()
                            movie_actors.append((movie_id, c.lastrowid))

                    for a in movie_actors:
                        c.execute('insert into movie_actor_through values (?,?)', a)
                        conn.commit()


        else:
            print "Movie %s not found" % name

conn.close()
