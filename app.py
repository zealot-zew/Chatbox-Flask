from flask import Flask, render_template, redirect, request,session,flash, Blueprint,url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_session import Session

import random
from string import ascii_uppercase

from Profile_bp import profile_bp
from Chatroom_bp import chatroom_bp

app = Flask(__name__)

#configure app
app.config["SECRET_KEY"] == "hkdslgborilbvilrufhnlkeriolhdfn" #random key
socketio = SocketIO(app)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configuring blueprints
app.register_blueprint(profile_bp, url_prefix="/profile")
app.register_blueprint(chatroom_bp,url_prefix="/chatroom")


#helpers functions

rooms = {}
def generate_unique_code(length):
    while True:
        code = ''
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    return code


#creating routes

#home page route
@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")  #home page basically have nothing
    else:
        session.clear()
        flash("Succesfully logged out")
        return render_template("home.html") 
    

#chatroom route
@app.route("/chatroom", methods = ["GET","POST"])
def chatroom():
    if request.method == "GET":
        '''youtube_url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
        return redirect(youtube_url)'''
        if 'username' not in session or not session["username"]:
            flash("Create a profile first")
            return redirect(url_for('profile')) #redirect to profile using url_for
        else:
            return render_template("chatroom.html") #happens via GET to chatroom
        
    if request.method == "POST":
            room = request.form.get("code")
            action = request.form.get("action")
            if action == "join":
                if not room:
                    flash("Room Code is necessary!")
                    return render_template("chatroom.html")
                elif room not in rooms:
                    flash("Invalid Room Code!")
                    return render_template("chatroom.html")
                session["room"] = room
                return redirect(url_for('chatroom.chat_room', room = session['room']))
            elif action == "create":
                room = generate_unique_code(4)
                session["room"] = room
                rooms[room] = {'members' : 0, 'messages' : []}     #the room dict initilasation (boiler code)
                return redirect(url_for('chatroom.chat_room', room = session['room'],messages=rooms[room]['messages']))

    #{room:{members:0,messgage:[]}}
            
#profile route
@app.route("/profile", methods = ["POST","GET"])
def profile():
    if ('username' not in session or not session["username"]):
        if request.method == "GET":
            return render_template("profile.html")
    
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Username is required!")
            return render_template("profile.html")
        else:
            current_user = request.form.get("username")
            session["username"] = current_user
            return redirect(url_for('chatroom'))
        
    if request.method == "GET" and session["username"]:
        current_user = session["username"]
        return redirect(url_for('profile.user_profile', username=current_user))

#setting up socket connecting
@socketio.on("connect")
def handle_connect(auth):
    room = session["room"]
    name = session["username"]
    
    if name == None:
        return redirect(url_for(profile))
    
    if room not in rooms:
        leave_room(room)
        return 

    join_room(room)
    send({"name": name, "message": "A wild card appeared in the room"}, to=room)
    rooms[room]['members'] += 1
    print(f"{name} has joined the room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session['room']
    name = session['username']

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
            print(f"room {room} is deleted")

    send({"name":name, "message":"has exited the group"},to=room)
    print(f"{name} has exited the room {room}")

@socketio.on('send_message')
def handle_send_message(data):
    room = session.get('room')
    name = session.get('username') 
    message = data.get('message')
    if room and name and message:
        send({"name": name, "message": message}, to=room)
        


if __name__ == "__main__":
    socketio.run(app,debug=True)