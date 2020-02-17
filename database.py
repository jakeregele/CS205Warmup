import sqlite3
import csv

def main():
    user_input = ''

    # initialize connection with database
    db = sqlite3.connect('spotify_data.db')

    # main program loop for user input
    while user_input.lower() not in ['q', 'quit']:

        # get input from command line
        user_input = input("")

        # check to make sure user has not quit
        if user_input.lower() not in ['q', 'quit']:
            user_input.split()
            query_string = parse(user_input)
            if (query_string != "-1"):
                query(query_string)


# load data from file
def load_data(db):
    # remove any existing tables from db
    drop_tables(db, "DROP TABLE top_songs;")
    drop_tables(db, "DROP TABLE top_artists;")

    # create db tables
    create_table(db, "CREATE TABLE top_artists(id INTEGER PRIMARY KEY, artist_name CHAR[32], genre CHAR[32], top_ranked CHAR[64]);")
    create_table(db, "CREATE TABLE top_songs(id INTEGER PRIMARY KEY, song_name CHAR[64], length INTEGER, ranking INTEGER, artist INTEGER, FOREIGN KEY (artist) REFERENCES top_artists(id));")

    # initialize db tables
    # populate each with csvs
    # load each csv into vector and populate tables with them
    top_songs = []
    top_artists = []

    with open('top50songs.csv') as csv_songs:
        for row in csv.reader(csv_songs):
            top_songs.append([row[1], row[2], row[3], row[4]])

    with open('artists.csv') as csv_artists:
        for row in csv.reader(csv_artists):
            top_artists.append([row[1], row[2], row[3]])


    for x in range(1, len(top_songs)):
        insert_statement = "INSERT INTO top_songs VALUES (" + str(x) + ",\"" + top_songs[x][0] + "\"," + top_songs[x][1] + "," + top_songs[x][2] + ",\"" + top_songs[x][3] + "\");"
        db.execute(insert_statement)

    for x in range(1, len(top_artists)):
        insert_statement = "INSERT INTO top_artists VALUES (" + str(x) + ",\"" + top_artists[x][0] + "\",\"" + top_artists[x][1] + "\",\"" + top_artists[x][2] + "\");"
        db.execute(insert_statement)

    db.commit()

    return 0
    # one of the commands should be load data, which will create the database and the schema and read
    # data from your csv files into the tables; if the database already exists, then the command will overwrite
    # the existing database


# create db table
def create_table(db, table):
    db.cursor()
    db.execute(table)
    db.commit()


# drop tables before recreating them for each iteration
def drop_tables(db, table):
    db.cursor()
    db.execute(table)
    db.commit()


# query database, load data if not already loaded
# list of commands
# command[0] = return variable
# command[1] = table
# OPT command[2] = item from table
def query(sql_list, db):
    song_list = {"length", "ranking"}
    artist_list = {"genre", "top_ranked"}

    if (sql_list[1] == "song" and sql_list[0] in song_list) or (sql_list[1] == "artist" and sql_list[0] in artist_list):
        # single query
        selectQ = "SELECT " + sql_list[0] + " FROM "
        selectQ += "top_songs WHERE song_name = " + "\"" + sql_list[2] + "\"" if sql_list[1] == "song" else "top_artists WHERE artist_name = " + "\"" + sql_list[2] + "\""

        val = select_helper(selectQ, db)
    else:
        # join query
        if sql_list[1] == "song":
            # query from songs to artists
            selectQ = "SELECT artist FROM top_songs WHERE song_name = " + "\"" + sql_list[2] + "\""
            artist_id = select_helper(selectQ, db)

            selectQ = "SELECT " + sql_list[0] + " FROM top_artists WHERE id = " + str(artist_id)
            val = select_helper(selectQ, db)
        else:
            # query from artists to songs
            selectQ = "SELECT top_ranked FROM top_artists WHERE artist_name = " + "\"" + sql_list[2] + "\""
            song_name = select_helper(selectQ, db)

            selectQ = "SELECT " + sql_list[0] + " FROM top_songs WHERE song_name = " + "\"" + str(song_name) + "\""
            val = select_helper(selectQ, db)

    return val

def select_helper(query, db):
    cur = db.cursor()
    cur.execute(query)
    val = cur.fetchone()[0]
    return val
main()