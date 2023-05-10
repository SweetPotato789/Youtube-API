from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)



# My table Model
class User_accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    username = db.Column(db.String(100),unique = True, nullable=False)
    google_account = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(500), nullable=False)

    def __init__(self, username, google_account, password):         
        self.username = username                 
        self.google_account = google_account          
        self.password = password

# marshallow (ma) is used for the serialization
class User_AccountSchema(ma.Schema):
    class Meta:
        fields = ("username", "google_account", "password")



# Object
User_Account = User_AccountSchema()
User_Accounts_schema = User_AccountSchema(many=True)

def create_tables():
    db.create_all()

if __name__ == '__main__':
    create_tables()

# adds creates user account
@app.route('/user_accounts', methods=['POST'])
def add_user_account():
    # Check if the requst body contains all required keys
    if not all(key in request.json for key in ['username', 'google_account', 'password']):
        abort(400, 'Missing required keys in Json payload')

    # Retrieve the data from the request body
    username = request.json['username']
    google_account = request.json['google_account']
    password = request.json['password']


    # Create a new user account object and add it to the database
    my_useraccounts = User_accounts(username, google_account, password)
    db.session.add(my_useraccounts)
    db.session.commit()

    # Serialize and return the new user account object
    return jsonify(User_Account.dump(my_useraccounts)), 201

# shows user accounts
@app.route('/show_useraccounts', methods = ['GET'])
def get_user_account():
    user_accounts = User_accounts.query.all()
    result = User_Accounts_schema.dump(user_accounts)
    return jsonify(result)

# deletes user account
@app.route('/user_accounts/<int:id>', methods=['DELETE'])
def delete_user_account(id):
    user_account = User_accounts.query.get(id)
    if user_account:
        db.session.delete(user_account)
        db.session.commit()
        return jsonify({'message': 'User account has been deleted successfully'})
    else:
        abort(404, 'Video not found')

app.run(debug=True)
