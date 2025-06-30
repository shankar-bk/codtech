from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Tracks users per room
rooms_users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    rooms_users.setdefault(room, set()).add(username)
    send(f"{username} joined the room.", to=room)
    emit('user_list', list(rooms_users[room]), to=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    rooms_users.get(room, set()).discard(username)
    send(f"{username} left the room.", to=room)
    emit('user_list', list(rooms_users[room]), to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = f"{data['username']}: {data['message']}"
    send(message, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
