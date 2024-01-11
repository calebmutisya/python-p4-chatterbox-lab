from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages= Message.query.all()
        return jsonify([message.to_dict() for message in messages])
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(**data)
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()),201
            
    
@app.route('/messages/<int:id>', methods =['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message= Message.query.get(id)
    if request.method == 'GET':
        if message:
            return jsonify(message.to_dict())
        else:
            return jsonify({'error': 'Message not found'}), 404
    elif request.method == 'PATCH':
        data= request.get_json()
        if message:
            message.body= data['body']
            db.session.commit()
            return jsonify(message.to_dict())
        else:
            return jsonify({'error': 'Message not found'}), 404
    elif request.method == 'DELETE':
        if message:
            db.session.delete(message)
            db.session.commit()
            return jsonify({'message': 'Message deleted succesfully'})
        else:
            return jsonify({'error': 'Message not found'}), 404


if __name__ == '__main__':
    app.run(port=5555)
