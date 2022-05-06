import pymysql
from flask import jsonify
from user import User

def getKeyWords(username, db):
    user = User.getUser(db, username, "username")
    keywords = []
    connection = db.connect() 
    if connection:
        print("connection made")
        cursor = connection.cursor(pymysql.cursors.DictCursor) #the cursor is utilized for querying sql databases
        if cursor:
            print("cursor variable found")
            query = "SELECT keywords from users u WHERE u.user_id = %s"
            cursor.execute(query, (user.id,))
            rows = cursor.fetchall()
            users_length = len(rows)
            print(rows)

            for i in range(users_length):
                for index, value in rows[i].items():
                    if value != None:
                        try:
                            keywords_split = value.split( )
                            print(keywords_split)
                            keywords.append(keywords_split)
                        except:
                            print("user only had one keyword in the newsfeed table")
                    else:
                        print("User has no keywords.. therefore we will not add it to the keyword article search to save resources")
            print(keywords)
            print(rows)

    return keywords
    

def retrieveNewsFeed(username, db):
    user = User.getUser(db, username, "username")
    preferences = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    keywords = getKeyWords(username, db)
    UserPreference = []

    for preference in preferences:
        if User.getUser(db, 1, preference):
            connection = db.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT nf.pipeline_id, nf.author, nf.title, nf.url, nf.dateandtime, nf.imageurl, nf.category from newsfeed nf, users u WHERE nf.category = %s and u." + preference + " = 1 and u.user_id = %s"
            print(query)
            print(user.id)
            cursor.execute(query, (preference,user.id,))
            rows = cursor.fetchall()
            print(rows)
            UserPreference.append(rows)
            connection.close()
        elif User.getUser(db, 0, preference):
            pass

    if keywords:
        for keyword in keywords:
            for word in keyword: #we want to search for the category with the key term each iteration
                connection = db.connect() #for user_id = 86, we'll make three connections
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                query2 = "SELECT nf.pipeline_id, nf.author, nf.title, nf.url, nf.dateandtime, nf.imageurl, nf.category from newsfeed nf, users u WHERE nf.category = %s and u.user_id = %s"
                cursor.execute(query2, (word, user.id,))
                rows2 = cursor.fetchall()
                UserPreference.append(rows2)

    return jsonify(results=UserPreference)
