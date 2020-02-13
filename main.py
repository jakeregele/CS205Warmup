import sqlite3
import csv


def main():
    user_input = ''

    # initialize connection with database
    db = sqlite3.connect('spotify_data.db')

    drop_tables(db, "DROP TABLE top_songs;")
    drop_tables(db, "DROP TABLE top_artists;")

    # create db tables
    create_table(db, "CREATE TABLE top_artists(id INTEGER PRIMARY KEY, artist_name CHAR[32], genre CHAR[32], top_ranked_song CHAR[32]);")
    create_table(db, "CREATE TABLE top_songs(id INTEGER PRIMARY KEY, song_name CHAR[64], song_length INTEGER, ranking INTEGER, artist INTEGER, FOREIGN KEY (artist) REFERENCES top_artists(id));")

    load_data(db)

    # main program loop for user input
    while user_input.lower() not in ['q', 'quit']:

        # get input from command line
        user_input = input("")

        # check to make sure user has not quit
        if user_input.lower() not in ['q', 'quit']:
            user_input.split()
            query_string = parse(user_input)
            query(query_string)


# load data from file
def load_data(db):

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
def query(sqlString):
    return 0


# translate commands from user into SQL query
def parse(userList):
    query_string = ''

    return query_string


main()