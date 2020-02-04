import sqlite3
import csv


def main():
    user_input = ''

    # initialize connection with database
    db = sqlite3.connect('spotify_data')
    # create db tables
    create_table(db, "Create Table 1 String Here")
    create_table(db, "Create Table 2 String Here")

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
    for row in csv.reader("top50songs.csv"):
        top_songs.append(row)

    for row in csv.reader("artists.csv"):
        top_artists.append(row)

    for x in range(1, len(top_songs) + 1):
        insert_statement = "INSERT INTO top_songs VALUES " + (x, top_songs[x][0], top_songs[x - 1][1], top_songs[x - 1][2], top_songs[x - 1][3]) + ";"
        db.execute(insert_statement)

    for x in range(1, len(top_artists) + 1):
        insert_statement = "INSERT INTO top_artists VALUES " + (x, top_songs[x][0], top_artists[x - 1][1], top_artists[x - 1][2], top_artists[x - 1][3]) + ";"
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

# query database, load data if not already loaded
def query(sqlString):
    return 0


# translate commands from user into SQL query
def parse(userList):
    query_string = ''

    return query_string
