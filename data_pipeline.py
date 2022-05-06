#Updates once a day
#Reminder: Need to have this pipeline running in docker in the future

#Written by Adam Asimolowo

import json
from newsapi.const import SOURCES_URL
from pymysql.connections import MysqlPacket
from requests import NullHandler
from requests.api import get
from main import mysql
import pandas as pd
from newsapi import NewsApiClient
import pymysql
from user import User

# Init
newsapi = NewsApiClient(api_key='cc25f61892174ebf82454d80258ad77e')

sum = 0
def getEverything(keyword):
    sum = 0 

    all_articles = newsapi.get_everything(q=keyword,
                                      from_param='2021-12-01',
                                      to='2021-12-07',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
    return all_articles

#PSUEDECODE

#STEP 1: split the keywords given by a user and add them into a list
#STEP 2: afterwards, loop through that list and use the getEverything function for each of those keywords
#getEverything("bitcoin")
#STEP 3: loop through all the users currently within the database and get their keywords; once u get their keywords, save those keywords in the newsfeed table
#STEP 4: query through all users in the users table list and retrieve their keywords

query1 = "SELECT keywords FROM users"

keywords = []

def getKeyWords(db):

    connection = db.connect() 
    if connection:

        print("connection made")
        cursor = connection.cursor(pymysql.cursors.DictCursor) #the cursor is utilized for querying sql databases
        if cursor:
            print("cursor variable found")
            query = "SELECT keywords FROM users"
            cursor.execute(query)
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
            connection.commit()   
    elif not connection:
        print("ERROR: connection not made...")

    return keywords
#ok1 = json.dumps(getEverything("tom"), indent = 4)
#print(ok1)
print("\n\n\n\n")

keywords_users = getKeyWords(mysql)
print("BROPLEASEGIVEMETHEWAY")
print(keywords_users)
articles = []

def executeKeyWords():

    keywords_title = []
    keywords_authors = []
    keywords_urls = []
    keywords_date_time = []
    keywords_image_urls = []
    keywords_category = []
    cat = "keywords"

    sum = 0  
    for i in keywords_users:
        print(len(i))
        for j in i:
            print("\nLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASSSSSSSSSSSSSSSS")
            print(j)
            all_articles = getEverything(j)
            #articles.append(getEverything(j))
            #print(all_articles)
            for item, value in all_articles.items():
                #print(item, value)
                if item == "articles":
                        #print(value)
                    for i in value:
                        #print(i)
                        sum = sum + 1
                        print(sum)
                        if sum >= 10:
                            sum = 0
                            break
                        else:

                            keywords_title.append(i['title'])
                            keywords_authors.append(i['author'])
                            keywords_urls.append(i['url'])
                            keywords_date_time.append(i['publishedAt'])
                            keywords_image_urls.append(i['urlToImage'])
                            keywords_category.append(j)

                            print(i['title'])
                            print(i['url'])
                            print(i['publishedAt'])
                            print(i['title'])
            
    return keywords_authors, keywords_urls, keywords_date_time, keywords_title, keywords_image_urls, keywords_category
    
            
def getTopHeadLines(cat):
    top_headlines = newsapi.get_top_headlines(#q='bitcoin',
                                            category=cat,
                                            language='en',
                                            country='us')
    return top_headlines


# REMINDER:
# IN THIS SECTION, WE WANT TO USE get_all_search FOR THE KEYWORDS
# THE DATAPIPELINE NEEDS TO READ WHAT THE USERs KEYWORDS ARE AND THEN FILTER THE 
# ARTICLES BASED ON THOSE SPECIFIC KEYWORDS


kk = getTopHeadLines("business")
print(kk) 

def getHeadlineProperties(var, cat):

    title = []
    authors = []
    urls = []
    date_time = []
    category = []
    image_urls = []
    sum = 0

    for item, value in var.items():
        #print(item, value)
        #print(str(item), str(value) + "\n")
        if item == "articles":
            #print(value)
            for i in value:
                sum = sum + 1
                print(sum)
                if sum >= 10:
                    break
                else:
                    #utilize an list to append all the values within the JSON file into a list
                    authors.append(i['author'])
                    urls.append(i['url']) 
                    date_time.append(i['publishedAt'])
                    title.append(i['title'])
                    image_urls.append(i['urlToImage'])
                    category.append(cat)
                    #if i == "source":
                    #   print('source found')

    return authors, urls, date_time, title, image_urls, category


properties_business = getHeadlineProperties(getTopHeadLines('business'), 'business')
properties_technology = getHeadlineProperties(getTopHeadLines('technology'), 'technology')
properties_general = getHeadlineProperties(getTopHeadLines('general'), 'general')
properties_health = getHeadlineProperties(getTopHeadLines('health'), 'health')
properties_science = getHeadlineProperties(getTopHeadLines('science'), 'science')
properties_sports = getHeadlineProperties(getTopHeadLines('sports'), 'sports')
properties_entertainment = getHeadlineProperties(getTopHeadLines('entertainment'), 'entertainment')
properties_keywords = executeKeyWords()


def getLengthArticles(var):

    for item, value in var.items():
        if item == "totalResults":
            print(value)
            return value
        

#create COLUMNS FOR EACH PROPERTY; EXAMPLE: DATAFRAMES
def convertPropertiesToDF(properties_cat):
    
    i = 0
    data = {'authors': properties_cat[i] , 'urls': properties_cat[i+1] , 'date_time': properties_cat[i+2] , 'title': properties_cat[i+3] , 'image_urls': properties_cat[i+4], 'category': properties_cat[i+5]}
    
    if data:
        dataFrame = pd.DataFrame(data)
        print("\n")
        print(dataFrame)
        
        return dataFrame
    
    else:
        print("data not found")
    
    #print(dataFrame['authors'])
    #print(dataFrame['urls'])

dataFrame_general = convertPropertiesToDF(properties_general)

#print(dataFrame)
print("\n\n\n")


article_preference_dictionary = {
    
    #1 = business
    #2 = technology
    #3 = general
    #4 = sports
    #5 = health
    #6 = science
    #7 = entertainment

    1 : convertPropertiesToDF(properties_business),
    2 : convertPropertiesToDF(properties_technology),
    3 : convertPropertiesToDF(properties_general),
    4 : convertPropertiesToDF(properties_sports),
    5 : convertPropertiesToDF(properties_health),
    6 : convertPropertiesToDF(properties_science),
    7 : convertPropertiesToDF(properties_entertainment),
    8 : convertPropertiesToDF(properties_keywords)


}

print(article_preference_dictionary[1])
#get the length of the dictionary 
print(len(article_preference_dictionary))

print("TESTING THIS OUT.....................")

#put lines 112-116 into the integration aspect of the code

#for k,v in article_preference_dictionary[4].iterrows():
 #   print(v['title'])
  #  print(v['date_time'])
   # print(v['category'])


print("\n\n")



#def insert_newsfeed_data(db, apikey, repeat_time, title, url, date_time, category, keyword, favorite)

def insert_newsfeed_data(db):

    #FETCH DATA FROM NEWSFEED
    #establishing a connection to the database

    connection = db.connect() 

    if connection:
        print("connection made")
        cursor = connection.cursor(pymysql.cursors.DictCursor) #the cursor is utilized for querying sql databases
        if cursor:
            print("cursor variable found")

            #psuedocode, only clear the table for columns that do not have their pipeline id located in the favorites pipeline id
            query1 ="SET FOREIGN_KEY_CHECKS = 0;"
            cursor.execute(query1)
            
            query3 = "TRUNCATE TABLE `newsfeed`;"
            cursor.execute(query3)

            query4 = "SET FOREIGN_KEY_CHECKS = 1;"
            cursor.execute(query4)

            for i in range(1, (len(article_preference_dictionary)+1)):
                for k, v in article_preference_dictionary[i].iterrows():

                    #print("\n")
                    #print(v['title'])
                    #print(v['date_time'])
                    #print(v['category'])
                    #print(v['urls'])
                    
                    query2 = "INSERT INTO newsfeed VALUES (NULL, %s, %s, %s, %s, %s, %s)"

                    if query2:
    
                        cursor.execute(query2, (v['authors'], v['title'], v['urls'], v['date_time'], v['image_urls'], v['category'],))
                        print("imported into database")

                    connection.commit()

    elif not connection:
        print("ERROR: connection not made...")


insert_newsfeed_data(mysql)


