import argparse

# Create the parser
musicParse = argparse.ArgumentParser(description='Music Database')

# Create a group for the user choice (mutually exclusive so only one can be true
group = musicParse.add_mutually_exclusive_group()
group.add_argument('-loadData', action="store_true", help="Starting command to load database")
group.add_argument('-genre', action="store_true", help="Enter song name to find out it's genre")
group.add_argument('-ranking', action="store_true", help="Enter artist name to find out their top song rank")
group.add_argument('-lengthSong', action="store_true", help="Enter song name to find the length of their top song")
group.add_argument('-lengthArtist', action="store_true", help="Enter artist to find the length of that song")

# Add one argument to the parser that will hold either song or artist
musicParse.add_argument('string', nargs='+', help="Song Name or Artist (correctly spelled and capitalized)")
args = musicParse.parse_args()

loaded = False

# If-elif-else statements for each member in the mut. excl. group
if args.loadData:
    # Add the user input to a string variable
    arg_str = ' '.join(args.string)

    # load database using function
    # load_data(db)
    print("Database loaded!")
    loaded = True

elif args.genre:
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        # load_data(db)
        print("Database loaded!")
        loaded = True

    # Add the user input to a string variable
    arg_str = ' '.join(args.string)
    # Output what the user inputted
    print("Song Name: ", arg_str)
    # Create a list to send to DB
    userChoice = ['genre', 'song', arg_str]
    # TODO: Send list to database

    # Testing to make sure list was correct
    # print("Genre: ", userChoice)

elif args.ranking:
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        # load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Artist Name: ", arg_str)
    userChoice = ['ranking', 'artist', arg_str]
    # TODO: Send list to database

    # Testing to make sure list was correct
    # print("Ranking: ", userChoice)

elif args.lengthSong:
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        # load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Song Name: ", arg_str)
    userChoice = ['length', 'top_song', arg_str]
    # TODO: Send list to database

    # Testing to make sure list was correct
    # print("Length: ", userChoice)

elif args.lengthArtist:
    if not loaded:
        print("Database has to be loaded...")
        # load database using function
        # load_data(db)
        print("Database loaded!")
        loaded = True

    arg_str = ' '.join(args.string)
    print("Artist Name: ", arg_str)
    userChoice = ['length', 'song', arg_str]
    # TODO: Send list to database

    # Testing to make sure list was correct
    # print("Length: ", userChoice)

else:
    print(args)
    if not loaded:
        print("Make sure to load the database with *any string* -loadData first")
    if loaded:
        print("Choose only one of the optional arguments after typing the correct value")
