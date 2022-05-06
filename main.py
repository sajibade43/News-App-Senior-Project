from flask import session, render_template, redirect, g, url_for
from flaskext.mysql import MySQL
from user import registerUser, signIn, userProfile, forgotPassword, resetPassword, editProfile, changePassword, \
    getHomePage
from newsfeed import retrieveNewsFeed
from follow import retrieveUsers, followUser, unfollowUser, userFollowingList, userFollowersList, numOfFollowers,\
    verifyIfUserFollow
from favorites import favoriteArticle, unfavoriteArticle, verifyIfFavoriteExist, getFavorites
from __init__ import app

mysql = MySQL(app)


@app.route('/')
def index():
    if g.user:
        return getHomePage(g.user, mysql)
    return render_template("login-form.html")


@app.route('/login-form.html')
def login_form():
    return render_template("login-form.html")


@app.route('/signup-form.html')
def signup_form():
    return render_template("signup-form.html")


@app.route('/homepage.html')
def homepage():
    if g.user:
        print(" \n\nAWFAFWAFAFWAFDWAFWAFWA \n\n\n\n LAWFAWFA" + str(g.user))
        return getHomePage(g.user, mysql)
        # return render_template("homepage.html")
    return redirect(url_for('index'))


@app.route('/settings.html')
def settings():
    if g.user:
        return render_template("settings.html")
    else:
        print("lol")
        render_template("login-form.html")


@app.route('/edit_password.html')
def edit_password():
    if g.user:
        return render_template("edit_password.html")
    else:
        return render_template("login-form.html")


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/password_reset.html')
def resetpage():
    return render_template("password_reset.html")


@app.route('/users.html')
def usersPage():
    return render_template("users.html")


@app.route("/register", methods=['POST'])
def register():
    return registerUser(mysql)


@app.route("/login", methods=['POST'])
def login():
    return signIn(mysql)


@app.route("/profile/<username>", methods=['GET'])
def user(username):
    if g.user:
        g.user = username
        return userProfile(g.user, mysql)
    return redirect(url_for('index'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    return forgotPassword(mysql)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    return resetPassword(token, mysql)


@app.route('/profile/<username>', methods=['POST'])
def edit_profile(username):
    if g.user:
        g.user = username
        return editProfile(g.user, mysql)
    return redirect(url_for('index'))


@app.route('/password_change', methods=['POST'])
def password_change():
    if g.user:
        return changePassword(g.user, mysql)
    return redirect(url_for('index'))


@app.route("/newsfeed/<username>", methods=['GET'])
def get_newsfeed(username):
    if g.user:
        g.user = username
        return retrieveNewsFeed(username, mysql)
    return redirect(url_for('index'))


@app.route("/users", methods=['GET'])
def get_users():
    return retrieveUsers(mysql)


@app.route("/profile/<userID>/follow/<userID2>", methods=['POST'])
def follow_user(userID, userID2):
    return followUser(userID, userID2, mysql)


@app.route("/profile/<userID>/unfollow/<userID2>", methods=['DELETE'])
def unfollow_user(userID, userID2):
    return unfollowUser(userID, userID2, mysql)


@app.route("/profile/<userID>/following", methods=['GET'])
def get_followingList(userID):
    return userFollowingList(userID, mysql)


@app.route("/profile/<userID>/followers", methods=['GET'])
def get_followersList(userID):
    return userFollowersList(userID, mysql)


@app.route("/profile/<userID>/follows/<userID2>", methods=['GET'])
def verifyIfUserFollows(userID, userID2):
    return verifyIfUserFollow(userID, userID2, mysql)


@app.route("/<userID>/favorite/<articleID>", methods=["POST"])
def favorite_article(userID, articleID):
    return favoriteArticle(userID, articleID, mysql)


@app.route("/<userID>/unfavorite/<articleID>", methods=["DELETE"])
def unfavorite_article(userID, articleID):
    return unfavoriteArticle(userID, articleID, mysql)


@app.route("/<userID>/favorites/<articleID>", methods=["GET"])
def verify_favorite(userID, articleID):
    return verifyIfFavoriteExist(userID, articleID, mysql)


@app.route("/<userID>/favorites", methods=["GET"])
def get_favorites(userID):
    return getFavorites(userID, mysql)



@app.route("/<userID>/numOfFollowers", methods=["GET"])
def get_numOfFollowers(userID):
    return numOfFollowers(userID, mysql)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
