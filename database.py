import sqlite3
import csv


def main():
    db = sqlite3.connect('spotify_data.db')
    # Initialize the loaded to false since database hasn't been loaded yet
    loaded = False
    # Initialize user input to empty string
    user_words = ""

    # Output a nice welcome message
    print("Welcome to the Top 50 Spotify Database")
    print("To start enter query with a command or '-help' for more info")

    # main program loop for user input
    while user_words.lower() not in ['-q', '-quit']:
        # get input from command line
        user_words = input("")
        # send input to method to decide what the user is asking for
        loaded = checkInput(user_words, loaded, db)
        print(" ")


# load data from file
def load_data(db):
    # remove any existing tables from db
    drop_tables(db, "DROP TABLE IF EXISTS top_songs;")
    drop_tables(db, "DROP TABLE IF EXISTS top_artists;")

    # create db tables
    create_table(db,
                 "CREATE TABLE top_artists(id INTEGER PRIMARY KEY, artist_name CHAR[32], genre CHAR[32], top_ranked CHAR[64]);")
    create_table(db,
                 "CREATE TABLE top_songs(id INTEGER PRIMARY KEY, song_name CHAR[64], length INTEGER, ranking INTEGER, artist INTEGER, FOREIGN KEY (artist) REFERENCES top_artists(id));")

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
        insert_statement = "INSERT INTO top_songs VALUES (" + str(x) + ",\"" + top_songs[x][0] + "\"," + top_songs[x][
            1] + "," + top_songs[x][2] + ",\"" + top_songs[x][3] + "\");"
        db.execute(insert_statement)

    for x in range(1, len(top_artists)):
        insert_statement = "INSERT INTO top_artists VALUES (" + str(x) + ",\"" + top_artists[x][0] + "\",\"" + \
                           top_artists[x][1] + "\",\"" + top_artists[x][2] + "\");"
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
def query(db, sql_list):
    song_list = {"length", "ranking"}
    artist_list = {"genre", "top_ranked"}

    if (sql_list[1] == "song" and sql_list[0] in song_list) or (sql_list[1] == "artist" and sql_list[0] in artist_list):
        # single query
        selectQ = "SELECT " + sql_list[0] + " FROM "
        selectQ += "top_songs WHERE song_name = " + "\"" + sql_list[2] + "\"" if sql_list[
                                                                                     1] == "song" else "top_artists WHERE artist_name = " + "\"" + \
                                                                                                       sql_list[
                                                                                                           2] + "\""

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

    row = cur.fetchone()
    if row:
        val = row[0]
    else:
        val = ""

    return val


def checkInput(user_strings, loaded, db):
    # Split user input into a list so we can extract query and command
    user_input = user_strings.split()

    # Get the index of the command
    numCommand = len(user_input) - 1
    user_command = str(user_input[numCommand])

    # Initialize a counter and query string
    counter = 0
    user_query = ''

    # While loop to create string of user query without command
    while counter < numCommand:
        user_query += str(user_input[counter])
        # Add a space after each word until last word
        if counter + 1 != numCommand:
            user_query += " "
        counter += 1

    # If the index of the command is at 0 or negative, user has inputted only help or no query at all
    if numCommand <= 0:
        if user_command == "-loadData":
            loaded = loadData(loaded, db)
            return loaded
        elif user_command == '-h':
            sendHelp()
        elif user_command == '-help':
            sendHelp()
        elif user_command == '-quit':
            print("Goodbye.")
        elif user_command == "-q":
            print("Goodbye.")
        else:
            noCorrect(user_input, loaded)

    # If the index of the command is at 1 or larger, then we may have a correct query with command
    # If/elifs to pair command with correct function
    if numCommand >= 1:

        # Although help is also listed above, if user inputs query and help then help should be displayed
        if user_input[numCommand].lower in ['-h', '-help']:
            sendHelp()

        elif user_input[numCommand] == '-loadData':
            loaded = loadData(loaded, db)

        elif user_input[numCommand] == '-genreArtist':
            loaded = genreArtist(user_query, loaded, db)

        elif user_input[numCommand] == '-genreSong':
            loaded = genreSong(user_query, loaded, db)

        elif user_input[numCommand] == '-rankingArtist':
            loaded = rankingArtist(user_query, loaded, db)

        elif user_input[numCommand] == '-rankingSong':
            loaded = rankingSong(user_query, loaded, db)

        elif user_input[numCommand] == '-lengthSong':
            loaded = lengthSong(user_query, loaded, db)

        elif user_input[numCommand] == '-lengthArtist':
            loaded = lengthArtist(user_query, loaded, db)

        elif user_input[numCommand] == '-song':
            loaded = song(user_query, loaded, db)

        elif user_input[numCommand] == '-artist':
            loaded = artist(user_query, loaded, db)

        else:
            noCorrect(user_input, loaded)

    return loaded


def loadData(loaded, db):
    # load database using function
    db = sqlite3.connect('spotify_data.db')
    load_data(db)
    print("Database loaded!")
    loaded = True
    return loaded


def genreArtist(user_query, loaded, db):
    # If database hasn't been loaded then load database and change loaded to true
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    # Output what the user inputted
    print("Artist: ", user_query)
    # Create a list to send to DB
    userChoice = ['genre', 'artist', user_query]
    temp = query(db, userChoice)
    # If query function returns empty string, the user input was not found
    if temp != "":
        print("The Genre is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded

def genreSong(user_query, loaded, db):
    # If database hasn't been loaded then load database and change loaded to true
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    # Output what the user inputted
    print("Song Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['genre', 'song', user_query]
    temp = query(db, userChoice)
    # If query function returns empty string, the user input was not found
    if temp != "":
        print("The Genre is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def rankingArtist(user_query, loaded, db):
    # If database hasn't been loaded then load database and change loaded to true
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Artist Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['ranking', 'artist', user_query]
    temp = query(db, userChoice)
    # If query function returns empty string, the user input was not found
    if temp != "":
        print("The ranking is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def rankingSong(user_query, loaded, db):
    #Function works exactly the same as rankingArtist except the list being sent to DB has changed
    if not loaded:
        print("Database has to be loaded...")
        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Song name: ", user_query)
    userChoice = ['ranking', 'song', user_query]
    temp = query(db, userChoice)
    if temp != "":
        print("The ranking is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def song(user_query, loaded, db):
    # If database hasn't been loaded then load database and change loaded to true
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Artist Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['song_name', 'artist', user_query]
    temp = query(db, userChoice)
    # If query function returns empty string, the user input was not found
    if temp != "":
        print("Top Song:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def artist(user_query, loaded, db):
    # Function works exactly the same as song except the list being sent to DB has changed
    if not loaded:
        print("Database has to be loaded...")

        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Song Name: ", user_query)
    userChoice = ['artist_name', 'song', user_query]
    temp = query(db, userChoice)
    if temp != "":
        print("The artist is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def lengthSong(user_query, loaded, db):
    # If database hasn't been loaded then load database and change loaded to true
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Song Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['length', 'song', user_query]
    temp = query(db, userChoice)

    # If query function returns empty string, the user input was not found
    if temp != "":
        # Get the minute by dividing seconds
        minute = int(temp) // 60
        # Get the remaining seconds by subtracting the minutes from song length
        seconds = int(temp) - (minute * 60)
        # Depending on how many remaining seconds the output changes
        # If seconds is less than 10 the system has to output a 0 for readability
        if seconds < 10:
            length = str(minute)
            length += ":0"
            length += str(seconds)
            print("The length is:", length)
        else:
            length = str(minute)
            length += ":"
            length += str(seconds)
            print("The length is:", length)
    else:
        print(user_query, " was not found. Try again")

    return loaded


def lengthArtist(user_query, loaded, db):
    # Function works exactly the same as lengthSong except the list being sent to DB has changed
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    print("Artist Name: ", user_query)
    userChoice = ['length', 'artist', user_query]
    temp = query(db, userChoice)
    if temp != "":
        minute = int(temp) // 60
        seconds = int(temp) - (minute * 60)
        if seconds < 10:
            length = str(minute)
            length += ":0"
            length += str(seconds)
            print("The length is:", length)
        else:
            length = str(minute)
            length += ":"
            length += str(seconds)
            print("The length is:", length)
    else:
        print(user_query, " was not found. Try again")

    return loaded


def sendHelp():
    # Output help text to console
    print(" First type a song or artist with correct spelling & capitalization")
    print("   Then choose one of the following commands")
    print("         example query 'Ariana Grande -rankingArtist' ")
    print(" ")
    print("    Command      :      Information")
    print('   -loadData     : Starting command to load database')
    print("     -song       : Enter artist to find their top song")
    print(" -rankingArtist  : Enter artist to find out their top song ranking")
    print("  -genreArtist   : Enter artist to find out it's genre")
    print("  -lengthArtist  : Enter artist to find the length of their top song")
    print("     -artist     : Enter song to find the artist's name")
    print("   -genreSong    : Enter song to find out it's genre")
    print("  -rankingSong   : Enter song to find out that song's ranking")
    print("   -lengthSong   : Enter song to find the length of that song")
    print("      -quit      : To end program run")


def noCorrect(user_input, loaded):
    # Output the user's input so they know what they entered
    print(user_input, "is not valid")

    # Check to see if the database has been loaded and output helpful text
    if not loaded:
        print("Make sure to load the database with -loadData first")
    elif loaded:
        print("Choose only one of the optional arguments after typing the correct value. Enter -h for more help")

    return loaded


main()
