from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# My Income Model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    affiliate_link = db.Column(db.String(5000))
    subscriptions = db.Column(db.Integer)
    ads = db.Column(db.Integer)

    def __init__(self, affiliate_link, subscriptions, ads):         
        self.affiliate_link = affiliate_link                
        self.subscriptions = subscriptions       
        self.ads = ads


# marshallow (ma) is used for the serialization
class IncomeSchema(ma.Schema):
    class Meta:
        fields = ("affiliate_link", "subscriptions", "ads")



# Object
income_schema = IncomeSchema()
profit_schema = IncomeSchema(many=True)

def create_tables():
    db.create_all()

if __name__ == '__main__':
    create_tables()

@app.route('/incomes', methods=['GET'])
def get_incomes():
    incomes = Income.query.all()
    return profit_schema.jsonify(incomes)

@app.route('/show_income', methods=['POST'])
def add_income():
    # Check if the request body contains all required keys
    required_keys = {'affiliate_link', 'subscriptions', 'ads'}
    if not all(key in request.json for key in ['affiliate_link', 'subscriptions', 'ads']):
        abort(400, 'Missing required keys in Json payload')

    # Retrieve the data from the request body
    affiliate_link = request.json['affiliate_link']
    subscriptions = request.json['subscriptions']
    ads = request.json['ads']

    # Add the income source to the database
    new_income = Income(affiliate_link=affiliate_link, subscriptions=subscriptions, ads=ads)
    db.session.add(new_income)
    db.session.commit()

    return income_schema.jsonify(new_income)

app.run(debug=True)
