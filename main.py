import sqlite3

def main():
    user_input = ''
    while user_input.lower() != 'q':
        user_input = input("")
        user_input.split()
        query_string = parse(user_input)
        query(query_string)





def load_data(fileName):
    #one of the commands should be load data, which will create the database and the schema and read
    #data from your csv files into the tables; if the database already exists, then the command will overwrite
    #the existing database

def query(sqlString):

def parse(userList):
    query_string = ''

    return query_string