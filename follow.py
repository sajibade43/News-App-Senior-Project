import pymysql
from flask import jsonify


def retrieveUsers(db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT username, first_name, last_name from users"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return jsonify({'data': data}), 200


def followUser(current_user, other_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "INSERT INTO follow VALUES (NULL, %s, %s)"
    cursor.execute(query, (current_user, other_user,))
    connection.commit()
    response = "Successfully followed user!"
    return jsonify({'message': response}), 200


def unfollowUser(current_user, other_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM follow where User = %s and UserFollow = %s"
    cursor.execute(query, (current_user, other_user,))
    connection.commit()
    response = "Successfully unfollowed user!"
    return jsonify({'message': response}), 200


def userFollowingList(current_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT u.first_name, u.last_name, u.username from users u WHERE u.user_id IN (SELECT f.UserFollow FROM follow f WHERE f.User = %s);"
    cursor.execute(query, (current_user))
    followingList = cursor.fetchall()
    connection.close()
    return jsonify({'following': followingList}), 200


def userFollowersList(current_user: object, db: object) -> object:
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT u.first_name, u.last_name, u.username from users u WHERE u.user_id IN (SELECT f.User FROM follow f WHERE f.UserFollow = %s);"
    cursor.execute(query, (current_user))
    followersList = cursor.fetchall()
    connection.close()
    return jsonify({'followers': followersList}), 200


def numOfFollowers(current_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT COUNT(u.username) from users u WHERE u.user_id IN (SELECT f.User FROM follow f WHERE f.UserFollow = %s);"
    cursor.execute(query, (current_user))
    num = cursor.fetchone()
    connection.close()
    return jsonify(amount=num), 200


def verifyIfUserFollow(current_user, other_user, db):
    connection = db.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM follow WHERE User = %s and UserFollow = %s"
    cursor.execute(query, (current_user, other_user,))
    doesUserFollow = cursor.fetchall()
    if len(doesUserFollow) > 0:
        message = "Yes, the user does follow this particular user"
        connection.close()
        return jsonify({'response': message}), 200
    else:
        message = "No, the user does not follow this particular user"
        connection.close()
        return jsonify({'response': message}), 200
