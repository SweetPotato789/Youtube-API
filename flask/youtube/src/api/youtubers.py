from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)




# My table Model
class Youtuber(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500), nullable = False)
    bio = db.Column(db.String(5000))

    def __init__(self, name, bio):         
        self.name = name
        self.bio = bio
                         

# marshallow (ma) is used for the serialization
class YoutuberSchema(ma.Schema):
    class Meta:
        fields = ("name", "bio")



# Object
youtuber_schema = YoutuberSchema()
youtubers_schema = YoutuberSchema(many=True)

def create_tables():
    db.create_all()

if __name__ == '__main__':
    create_tables()

# shows youtubers
@app.route('/youtubers', methods=['GET'])
def get_youtubers():
    youtubers = Youtuber.query.all()
    result = youtubers_schema.dump(youtubers)
    return jsonify(result)


# adds in new or current youtubers
@app.route('/show_youtubers', methods=['POST'])
def add_youtuber():
    # Check if the request body contains all required keys
    if not all(key in request.json for key in ['name', 'bio']):
        abort(400, 'Missing required keys in JSON payload')

    # Retrieve the data from the request body
    name = request.json['name']
    bio = request.json['bio']

    # Create a new Youtuber object and add it to the database
    youtuber = Youtuber(name=name, bio=bio)
    db.session.add(youtuber)
    db.session.commit()

    # Serialize and return the newly added youtuber
    result = youtuber_schema.dump(youtuber)
    return jsonify(result)


app.run(debug=True)