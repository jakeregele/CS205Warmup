# Starting point for when I realized argparse was just not going to work the way I wanted
# This is were all the methods in database began and then became fully realized over there
# This code should not be ran as it's not totally complete


# # Create a group for the user choice (mutually exclusive so only one can be true
# group = musicParse.add_mutually_exclusive_group()
# group.add_argument('-loadData', action="store_true", help="Starting command to load database")
# group.add_argument('-genre', action="store_true", help="Enter song name to find out it's genre")
# group.add_argument('-ranking', action="store_true", help="Enter artist name to find out their top song rank")
# group.add_argument('-lengthSong', action="store_true", help="Enter song name to find the length of their top song")
# group.add_argument('-lengthArtist', action="store_true", help="Enter artist to find the length of that song")


def checkInput(user_strings, loaded, db):
    # Split user input into a list so we can extract query and command
    user_input = user_strings.split()

    # Get the index of the command
    numCommand = len(user_input) - 1

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
        if user_input[numCommand].lower in ['-h', '-help']:
            sendHelp()
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

        elif user_input[numCommand] == '-genre':
            loaded = genre(user_query, loaded, db)

        elif user_input[numCommand] == '-ranking':
            loaded = ranking(user_query, loaded, db)

        elif user_input[numCommand] == '-lengthSong':
            loaded = lengthSong(user_query, loaded, db)

        elif user_input[numCommand] == '-lengthArtist':
            loaded = lengthArtist(user_query, loaded, db)

        elif user_input[numCommand] == '-artistSong':
            loaded = artistSong(user_query, loaded, db)

        elif user_input[numCommand] == '-songArtist':
            loaded = songArtist(user_query, loaded, db)


        else:
            noCorrect(user_input, loaded)
    else:
        noCorrect(user_input, loaded)

    return loaded


# If-elif-else statements for each member in the mut. excl. group
def loadData(loaded, db):
    # load database using function
    db = sqlite3.connect('spotify_data.db')
    load_data(db)
    print("Database loaded!")
    loaded = True
    return loaded


def genre(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    # Output what the user inputted
    print("Song Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['genre', 'artist', user_query]
    temp = query(db, userChoice)
    if temp != "":
        print("The Genre is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def artistSong(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    # Output what the user inputted
    print("Song Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['song_name', 'artist', user_query]
    temp = query(db, userChoice)
    if temp != "":
        print("The artist's top song is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def songArtist(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    # Output what the user inputted
    print("Song Name: ", user_query)
    # Create a list to send to DB
    userChoice = ['artist_name', 'song', user_query]
    temp = query(db, userChoice)
    if temp != "":
        print("The Genre is:", temp)
    else:
        print(user_query, " was not found. Query invalid. Try again.")

    return loaded


def ranking(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Artist Name: ", arg_str)
    userChoice = ['ranking', 'artist', arg_str]
    temp = query(db, userChoice)
    if temp != "":
        print("The ranking is:", temp)
    else:
        print(arg_str, " was not found. Query invalid. Try again.")

    return loaded


def lengthSong(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Song Name: ", arg_str)
    userChoice = ['length', 'top_song', arg_str]
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
        print(arg_str, " was not found. Try again")

    return loaded


def lengthArtist(user_query, loaded, db):
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Artist Name: ", arg_str)
    userChoice = ['length', 'artist', arg_str]
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
        print(arg_str, " was not found. Try again")

    return loaded


def sendHelp():
    print("help stuff")


def noCorrect(user_input, loaded):
    print(user_input, "is not valid")
    if not loaded:
        print("Make sure to load the database with -loadData first")
    elif loaded:
        print("Choose only one of the optional arguments after typing the correct value. Enter -h for more help")

    return loaded

