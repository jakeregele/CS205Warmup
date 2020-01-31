import sqlite3


# TABLE NAME: top50songs ATTRIBUTE NAMES: Track.Name, Length., Ranking, Artist.Name
# TABLE NAME: artists ATTRIBUTE NAMES: artist, genre, top ranked song
def main():
    user_input = ''

    # main program loop for user input
    while user_input.lower() not in ['q', 'quit']:

        # get input from command line
        user_input = input("")

        # check to make sure user has not quit
        if user_input.lower() == 'help':
            print("help")

        elif user_input.lower() not in ['q', 'quit']:
            user_input.split()
            query_string = parse(user_input)
            query(query_string)

    return 0


# load data from file
def load_data(file_name):

    # initialize db tables

    # populate each with csvs
    # create RDB connection
    # overwrite current DB tables in memory

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
def query(sql_string):
    return 0


# translate commands from user into SQL query
def parse(user_list):
    query_string = ''
    i = len(user_list)

    return query_string

main()
