from django.shortcuts import render
from django.db import connection
from collections import namedtuple

# https://www.geeksforgeeks.org/namedtuple-in-python/
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Data', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_query(str):
    '''Execute SQL query and return its result as a list'''
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(str)
        result = namedtuplefetchall(cursor)
    except Exception as e:
        print(e)
        
        result = [e]
    finally:
        cursor.close()
        return result

