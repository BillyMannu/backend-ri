import this
from traceback import print_tb
from unicodedata import name
from idlelib.multicall import r
import mysql.connector
import json
import sys as json
# from json import jsonEncoder
from flask import request, make_response

# connect to database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    database="penzi"
)
print('MySQL Database connection successful')
print(mydb)


# json
class Penzi:
    def penzi(self, number, message):

        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM users  WHERE number=' + number)
        myresult = mycursor.fetchall()

        if len(myresult) > 0:
            print("client  is already in the system")
            return "<h1> youre already in the system</h1>"
            # return make_response({
            #     "message": "you are already in the system"
            # }, 200)
        else:
            json = request.json
            message = json['message']
            number = json['number']

            sql = "INSERT INTO messages (number, message) VALUES (%s, %s)"
            val = (number, message)
            mycursor.execute(sql, val)
            mydb.commit()

            print(mycursor.rowcount, "record inserted.")

            print("client is now registered")
            message2 = "welcome to our dating service with 600 potential partners! To register SMS " \
                       "start#name#age#sex#provnce#town "
            sql2 = "INSERT INTO messages (message,number) VALUES (%s,%s)"
            val2 = (message2, number)
            mycursor.execute(sql2, val2)
            mydb.commit()
            # return make_response({
            #     "message":"welcome to our dating service with 600 potential partners! To register SMS " \
            #            "start#name#age#sex#provnce#town "
            # })
            return "<h1> returning html </h1>"


class Start:
    def start(self, number, message):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT number FROM users WHERE number=" + number)
        myresult = mycursor.fetchall()

        if len(myresult) > 0:
            print("is already in the system")
            return make_response({
                "message": "you had already sent the bio "
            })
        else:
            json = request.json
            message = json["message"]
            number = json["number"]

            mycursor = mydb.cursor()

            sql = "INSERT INTO users (number) VALUES( %s)"
            val = number
            thistuple = (val,)
            mycursor.execute(sql, thistuple)
            mydb.commit()
            sql1 = "UPDATE users SET name = (%s),sex = (%s),dateOfBirth = (%s),province = (%s),town = (%s) WHERE number =" + number
            x = message.split("#")
            x.pop(0)
            mycursor.execute(sql1, x)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
            print("client has added his bio")

            message2 = "Thank you.SMS details#level of education# profession#marital status#religion#tribe to 5001 E.G " \
                       "details#diploma#accountant# single#christian#mijikenda "
            sql2 = "INSERT INTO messages(number, message) VALUES (%s,%s)"
            val2 = number, message2
            mycursor.execute(sql2, val2)
            mydb.commit()
            return make_response({
                "message": "Thank you.SMS details#level of education# profession#marital status#religion#tribe to 5001 E.G details#diploma#accountant# single#christian#mijikenda "
            })


class Details:
    def details(self, number, message):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT levelOfEducation  FROM users WHERE number=" + number)
        myresult = mycursor.fetchall()

        # if len(myresult) > 0:
        #     print("client details already in the system")
        #     return make_response({
        #         "message": "you had already sent these details "
        #     })
        # else:
        mycursor = mydb.cursor()
        sql = "UPDATE  users SET levelOfEducation = (%s) , profession = (%s) ,religion = (%s), tribe = (%s)  WHERE number = " + number

        x = message.split("#")
        x.pop(0)
        mycursor.execute(sql, x)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

        message2 = "This is the last stage of registration SMS a brief description of yourself to search for a MPENZI, SMS match to 5001 starting with the word MYSELF E.G MYSELF Chocolate, lovely, sexy etc."
        sql2 = "INSERT INTO messages (number,message) VALUES(%s,%s)"
        val2 = number, message2
        mycursor.execute(sql2, val2)
        mydb.commit()

        return make_response({
            "message": "This is the last stage of registration SMS a brief description of yourself to search for a MPENZI, SMS match to 5001 starting with the word MYSELF E.G MYSELF Chocolate, lovely, sexy etc."
        })


class Myself:
    def myself(self, number, message):
        mycursor = mydb.cursor()

        # myresult = mycursor.fetchall()

        # if len(myresult) > 0:
        #     print("is already in the system")
        #     return make_response({
        #         "message": "you had already sent their description"
        #     })
        # else:
        json = request.json
        message = json["message"]
        number = json["number"]
        myself = message.split(' ', 1)[1]

        mycursor = mydb.cursor()

        sql1 = "UPDATE users SET myself = (%s) WHERE number =" + number
        val = myself
        thistuple = (val,)
        mycursor.execute(sql1, thistuple)
        mydb.commit()

        print("client has added his description")

        message2 = "You are now registered! Enjoy yourself To search for a MPENZI SMS Match #age #town to 5001 E.G Match#23-25#Nairobi"
        sql2 = "INSERT INTO messages(number, message) VALUES (%s,%s)"
        val2 = number, message2
        mycursor.execute(sql2, val2)
        print(mycursor.rowcount, "record inserted.")
        mydb.commit()

        return make_response({
            "message": "You are now registered! Enjoy yourself To search for a MPENZI SMS Match #age #town to 5001 E.G Match#23-25#Nairobi"
        })


class Match:
    def match(self, number, message):
        json = request.json
        message = json["message"]
        number = json["number"]

        x = message.split("#")
        age = x.pop(1)

        town = x.pop(1)

        range = age.split("-")

        lowerboundary = range.pop(0)
        upperboundary = range.pop(0)

        mycursor = mydb.cursor()
        sql = "SELECT  DISTINCT name,YEAR(CURDATE()) - YEAR(dateOfBirth) AS age,number FROM users WHERE town = (%s) HAVING age BETWEEN " + lowerboundary + " AND " + upperboundary + " ORDER BY rand() LIMIT 3 "

        val = town
        thistuple = (val,)

        mycursor.execute(sql, thistuple)
        myresult = mycursor.fetchall()
        print(myresult)

        return make_response({
            "message": "we have 30 ladies who match your choice! We will send you details of 3 of them shortly. To get more details about a lady, SMS her number EG 0722123456 to 5001",
            "message1": myresult
        })


class Next:
    def next(self, message):
        json = request.json
        message = json["message"]

        mycursor = mydb.cursor()
        sql = "SELECT  DISTINCT name,YEAR(CURDATE()) - YEAR(dateOfBirth) AS age,number FROM users WHERE town = (%s) HAVING age BETWEEN " + lowerboundary + " AND " + upperboundary


class Choice:
    def choice(self, message, number):
        json = request.json
        message = json["message"]
        number = json["number"]

        # x = message.split()[1]  

        # thistuple = (x,)
        thistuple = (message,)

        mycursor = mydb.cursor()

        # Lina aged 29 Coast province, Lamu town Graduate accountant,  Christian, kikuyu,. Send DESCRIBE 07221223456 to get more details about Lina
        # sql = "SELECT DISTINCT name,YEAR(CURDATE()) - YEAR(dateOfBirth) AS age,province,town,levelOfEducation,religion,tribe FROM users WHERE number = (%s)" 
        # val = thistuple

        # mycursor.execute(sql,val)
        # myresult= mycursor.fetchall()
        # print (myresult)

        sql_name = "SELECT name FROM users where number = (%s)"
        val = thistuple
        mycursor.execute(sql_name, val)
        name_result = mycursor.fetchall()

        sql_province = "SELECT province FROM users where number = (%s)"
        val = thistuple
        mycursor.execute(sql_province, val)
        province_result = mycursor.fetchall()

        sql_town = "SELECT town FROM users where number = (%s)"
        val = thistuple
        mycursor.execute(sql_town, val)
        town_result = mycursor.fetchall()

        sql_age = "SELECT YEAR(CURDATE()) - YEAR(dateOfBirth) AS age FROM users where number = (%s)"
        val = thistuple
        mycursor.execute(sql_age, val)
        age_result = mycursor.fetchall()

        sql = "SELECT DISTINCT levelOfEducation,religion,tribe FROM users WHERE number = (%s)"
        val = thistuple
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

        # Lina aged 29 Coast province, Lamu town Graduate accountant,  Christian, kikuyu,. Send DESCRIBE 07221223456 to get more details about Lina
        sms = name_result + "aged" + age_result + "province" + town_result + "town" + myresult
        print(sms)

        return make_response({
            "message": sms
        })


class Chosen:
    def chosen(self, number, message):
        json = request.json
        number = json["number"]
        message = json["message"]

        thistuple = (number,)
        mycursor = mydb.cursor()

        # HI Lina A guy called Andrew is interested in u and requested ur details Aged 25 based in Nairobi. Do you want to know more about her? Send yes to 5001
        # name, age, town
        sql = "SELECT  DISTINCT name,YEAR(CURDATE()) - YEAR(dateOfBirth) AS age,number,town FROM users WHERE number= (%s)"
        val = thistuple
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.commit()
        print(myresult)
        return make_response({
            "message1": myresult
        })


class Description:
    def description(self, message, number):
        json = request.json
        number = json["number"]
        message = json["message"]

        x = message.split(' ', 1)[1]

        thistuple = (x,)
        mycursor = mydb.cursor()

        sql = "SELECT DISTINCT myself FROM users WHERE number=(%s) "
        val = thistuple

        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        mydb.commit()

        print(myresult)
        return make_response({
            "message": myresult
        })


class Accept:
    def accept(self, number, message):
        json = request.json
        message = json['message']
        number = json['number']

        # mydb.cursor()
        # sql = 


class Activate:
    def activate():
        return make_response({
            "message": "You are now registered! Enjoy yourself To search for a MPENZI SMS Match #age #town to 5001 E.G Match#23-25#Nairobi"
        })


class Deactivate:
    def deactivate(self, number):
        json = request.json
        number = json['number']

        mycursor = mydb.cursor()
        sql = "DELETE FROM users WHERE  number =" + number
        val = number
        myresult = mycursor.execute(sql, val)
        print(myresult)
        mydb.commit()
        return make_response({
            "message": "Hi  Andrew! You are due for de-activation from our dating service on Tuesday the 25th To re-activate send ACTIVATE to 5001"
        })
