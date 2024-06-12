from flask import Blueprint,render_template,redirect,url_for,session

chatroom_bp = Blueprint('chatroom',__name__,static_folder="static", template_folder="templates", url_prefix='/chatroom')


#to solve chatroom/chatroom problem
@chatroom_bp.route("/chatroom")
def chatroom():
    return redirect(url_for("chatroom"))
#to solve #/chatroom/profile problem
@chatroom_bp.route("/profile")
def profile():
    return redirect(url_for('profile.user_profile', username=session['username']))

@chatroom_bp.route('/<room>')
def chat_room(room):
    return render_template("chatroom.html", room = room)