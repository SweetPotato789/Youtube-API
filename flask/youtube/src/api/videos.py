from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)



# My table Model with b-tree (index)
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), index=True, unique=False)
    description = db.Column(db.String(200))
    author = db.Column(db.String(50))

    def __init__(self, title, description, author):         
        self.title = title                 
        self.description = description          
        self.author = author

# marshallow (ma) is used for the serialization
class VideoSchema(ma.Schema):
    class Meta:
        fields = ("title", "author", "description")


# Object
video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)

# Create the database tables and index
db.create_all()
db.session.commit()


@app.route('/video', methods=['POST'])
def add_video():
    # Check if the requst body contains all required keys
    if not all(key in request.json for key in ['title', 'description', 'author']):
        abort(400, 'Missing required keys in Json payload')

    # Retrieve the data from the request body
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']


    # Create a new Video object and add it to the database
    my_videos = Video(title, description, author)
    db.session.add(my_videos)
    db.session.commit()

    # Serialize and return the new video object
    return video_schema.jsonify(my_videos), 201

@app.route('/video', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    result = videos_schema.dump(videos)
    return jsonify(result)


@app.route('/video/<int:id>', methods=['DELETE'])
def delete_video(id):
    video = Video.query.get(id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return jsonify({'message': 'Video has been deleted successfully'})
    else:
        abort(404, 'Video not found')
        

app.run(debug=True)
