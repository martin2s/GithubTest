# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from math import *
import pyodbc
import pandas as pd
from random import *


def updateStats(stats):
    with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=LAPTOP-SO3DD4CM\SQLEXPRESS;'
                        'Database=AlterLife;'
                        'Trusted_Connection=yes;') as conn:
        newstats = stats
        for i in range(len(newstats)):
            cursor = conn.cursor()
            cursor.execute('update playerstats set StatValue = ? where statid = ?', newstats[i], i+1)
            conn.commit()


def intro():
    print('What did your Mother and Father decide to name you?')
    introName = input()
    return introName


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def yes_or_no_condition():
    answer = str.lower(input())
    while answer != 'yes' and answer != 'no':
        print('Simply say Yes or No')
        answer = str.lower(input())
    return answer


def random_stats():
    print('Would you like to answer some questions about yourself to determine your base stats or'
          ' start life at random ?')
    random_or_not = str.lower(input())
    while random_or_not != 'yes' and random_or_not != 'no':
        print('Simply say Yes or No')
        random_or_not = str.lower(input())
    return random_or_not


def create_stats(random_or_not):
    if random_or_not == 'no':  # User did not want to answer questions, therefore random
        intelligence = randint(1, 100)
        health = randint(1, 100)
        wealth = randint(1, 100)
        looks = randint(1, 100)
        karma = randint(1, 100)
        happiness = randint(1, 100)
        stats = [karma, health, happiness, looks, wealth, intelligence]
        updateStats(stats)

        return stats
    else:  # base stats start at 50
        intelligence = 50
        health = 50
        wealth = 50
        looks = 50
        karma = 50
        happiness = 50

        stats = [karma, health, happiness, looks, wealth, intelligence]
        with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=LAPTOP-SO3DD4CM\SQLEXPRESS;'
                            'Database=AlterLife;'
                            'Trusted_Connection=yes;') as conn:
            sqlquery = pd.read_sql_query('select QuestionID, Question, StatAffected1, Answer1, Answer2, StatDifference1, '
                                         'StatDifference2, Stage from Questions', conn)

            df = pd.DataFrame(sqlquery, columns=['QuestionID', 'Question', 'StatAffected1', 'Answer1', 'Answer2',
                                                 'StatDifference1', 'StatDifference2', 'Stage'])

        for index, row in df.iterrows():
            stage_check = df['Stage'].values[index]
            if stage_check == 0:
                print(row['Question'])
                answer = yes_or_no_condition()
                playerstat = df['StatAffected1'].values[index] - 1  # there is a minus 1 as index starts from 1 instead of 0
                StatValue = stats[playerstat]
                if answer == df['Answer1'].values[index]:
                    StatValue = StatValue + df['StatDifference1'].values[index]
                    stats[playerstat] = int(StatValue)
                if answer == df['Answer2'].values[index]:
                    StatValue = StatValue + df['StatDifference2'].values[index]
                    stats[playerstat] = int(StatValue)
        updateStats(stats)
        return stats


def print_stats():
    with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=LAPTOP-SO3DD4CM\SQLEXPRESS;'
                        'Database=AlterLife;'
                        'Trusted_Connection=yes;') as conn:

        sqlquery = pd.read_sql_query('select statID, StatDescription, StatValue from PlayerStats', conn)
        df = pd.DataFrame(sqlquery, columns=['statID', 'StatDescription', 'StatValue'])

        for index, row in df.iterrows():
            print('Your', row['StatDescription'], 'is', row['StatValue'])


def get_question():
    with pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=LAPTOP-SO3DD4CM\SQLEXPRESS;'
                        'Database=AlterLife;'
                        'Trusted_Connection=yes;') as conn:

        sqlquery = pd.read_sql_query('select TOP 1 Question, StatAffected1, Answer1, Answer2,'
                                     ' StatDifference1, StatDifference2, Stage, QuestionAsked from Questions'
                                     ' where QuestionAsked = 0', conn)
        df = pd.DataFrame(sqlquery, columns=['Question', 'StatAffected1', 'Answer1', 'Answer2',
                                             'StatDifference1', 'StatDifference2', 'Stage', 'QuestionAsked'])

        return df


# Initial greeting and get the name from user
name = intro()
# say hello to user
print_hi(name)
# determines whether user wants random stats
random_or_not = random_stats()
# creates base stats for user based on whether random or not
stats = create_stats(random_or_not)




# Baby Stage
print('Welcome to the big world!\nYou have just been born and despite not knowing the choices you make could change '
      'the rest of your life')


print_stats()
get_question()
print('my name jeff')
print('my name a test')
# def ask_question(question):




