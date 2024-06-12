from flask import Blueprint,render_template,redirect,url_for,session

profile_bp = Blueprint('profile',__name__,static_folder="static", template_folder="templates", url_prefix='/profile')

# to solve the problem of /profile/chatroom, this is handled by redirecting to /chatroom if the problem is faced
@profile_bp.route("/chatroom")
def chatroom():
    return redirect(url_for("chatroom"))

#to solve #/profile/profile problem
@profile_bp.route("/profile")
def profile():
    return redirect(url_for('profile.user_profile', username=session['username']))

@profile_bp.route('/<username>')
def user_profile(username):
    #can access the username from the url
    return render_template("profile.html" , username = username)