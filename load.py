import requests, codecs, json, sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

# resp = requests.get('https://todolist.example.com/tasks/')
# if resp.status_code != 200:
#     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))


f = codecs.open('data/top50.txt', 'r', 'UTF-8')
for line in f:
    name = line.rstrip('\n')
    print "Loading %s movie" % name
    resp = requests.get('http://www.omdbapi.com/?t=%s' % name)
    if resp.status_code != 200:
        raise ApiError('GET {}'.format(resp.status_code))
    else:
        movie = json.loads(resp.text)
        if "Genre" in movie.keys():
            genres = movie['Genre'].split(",")
            for genre in genres:
                c.execute("SELECT COUNT(*) FROM genres WHERE name = '%s'" % genre.strip())
                (exitst,)=c.fetchone()
                if exitst < 1:
                    c.execute("INSERT INTO genres (name) VALUES('%s')" % genre.strip())
                    conn.commit()

        print "\n"


# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))


conn.close()
