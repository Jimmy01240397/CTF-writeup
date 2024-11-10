#!/usr/bin/env python3

# import mysql.connector

def connect():
    def cnx():
        # placeholder for emulating a connection
        print("Connected to database")
        pass

    def cursor():
        # placeholder for emulating a cursor
        print("Cursor created")
        pass

    # cnx = mysql.connector.connect(
    #     host = "localhost",
    #     user = "fulu",
    #     password = "fulu",
    #     database = "fulu"
    # )
    # cursor = cnx.cursor()

    return (cnx, cursor)
