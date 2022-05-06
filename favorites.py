import pymysql
from flask import jsonify
from user import User


def favoriteArticle(current_user, articleID, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "INSERT INTO favorites(userId, pipelineID, favorite_author, favorite_title, favorite_url, favorite_dateandtime, " \
            "favorite_imageurl, favorite_category) SELECT u.user_id, n.pipeline_id, n.author, n.title, n.url, n.dateandtime, n.imageurl, n.category FROM newsfeed n, users u " \
            "where n.pipeline_id = %s and u.user_id = %s;"
    cursor.execute(query, (articleID, current_user,))
    connection.commit()
    response = "Successfully favorited article!"
    return jsonify({'message': response}), 200


def unfavoriteArticle(current_user, articleID, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM favorites f where f.userId = %s and f.pipelineID = %s;"
    cursor.execute(query, (current_user, articleID,))
    connection.commit()
    response = "Successfully un-favorited article!"
    return jsonify({'message': response}), 200


def verifyIfFavoriteExist(current_user, articleID, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM favorites f where f.userId = %s and f.pipelineID = %s;"
    cursor.execute(query, (current_user, articleID,))
    doesFavoriteExist = cursor.fetchall()
    if len(doesFavoriteExist) > 0:
        message = "Yes, the user does favorite the article"
        connection.close()
        return jsonify({'response': message}), 200
    else:
        message = "No, the user doesn't favorite that article"
        connection.close()
        return jsonify({'response': message}), 200


def getFavorites(current_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT u.username, f.favorite_author, f.favorite_title, f.favorite_url, f.favorite_dateandtime, f.favorite_imageurl, f.favorite_category " \
            "from favorites f LEFT JOIN users u ON f.userID = u.user_id WHERE f.userID = %s or f.userID IN (SELECT f.UserFollow FROM " \
            "follow f WHERE f.User = %s) ORDER BY favorite_dateandtime DESC;"
    cursor.execute(query, (current_user,current_user,))
    favorites = cursor.fetchall()
    connection.close()
    return jsonify(results=favorites), 200
