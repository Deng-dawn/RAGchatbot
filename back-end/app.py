from uuid import uuid4
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from datetime import timedelta

import chatAgent
import exts
import os

app = Flask(__name__)
CORS(app)  # allow cross domain request

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = exts.SESSION_TYPE
app.config['SESSION_FILE_DIR'] = exts.SESSION_PATH
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=exts.SESSION_DURA)  # available in 20 minutes

sess = Session()
sess.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/chatbot', methods=['POST'])
def chatbot():
    # todo: add a preset question cotton for better querying result
    session_id = session.get('session_id')
    if session_id is None:
        session_id = str(uuid4())
        session['session_id'] = session_id

    if 'chat_history' not in session:
        session['chat_history'] = []
        print("NEW Session begins:")

    data = request.json
    chat_info = {"user_query": data['query'], "chat_history": session['chat_history']}

    ai_response, new_chat_history = chatAgent.run_chat_bot_agent(chat_info)

    response_content = exts.CHATBOT_ERROR if not ai_response else ai_response
    session['chat_history'] = new_chat_history

    return jsonify({'role': 'assistant', 'content': response_content})


if __name__ == '__main__':
    app.run()
