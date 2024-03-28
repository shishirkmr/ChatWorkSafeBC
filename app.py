from flask import Flask, render_template, request, jsonify
from question_anaswering import QuestionAnsweringSystem
from chatbot import RagChatApplication

app = Flask(__name__)


@app.route('/')
def chat_home():
    return render_template('chat-index.html')

@app.route('/qna')
def qna_home():
    return render_template('qna-index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Here you can process the user_message or send it to a model for response
    qa = RagChatApplication(user_query=user_message)
    bot_response = qa.generate()
    return jsonify({'message': bot_response})

@app.route('/ask', methods=['POST'])
def qna():
    user_message = request.json['message']
    # Here you can process the user_message or send it to a model for response
    qa = QuestionAnsweringSystem(user_query=user_message)
    bot_response = qa.generate()
    return jsonify({'message': bot_response})


if __name__ == '__main__':
    app.run()
