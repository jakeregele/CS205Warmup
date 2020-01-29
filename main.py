import sqlite3


def main():
    user_input = ''

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
def load_data(fileName):
    return 0
    # one of the commands should be load data, which will create the database and the schema and read
    # data from your csv files into the tables; if the database already exists, then the command will overwrite
    # the existing database


# query database, load data if not already loaded
def query(sqlString):
    return 0


# translate commands from user into SQL query
def parse(userList):
    query_string = ''

    return query_string
