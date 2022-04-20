import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import null


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/lets_drive'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class RidersInformation(db.Model):
    id = db.Column(db.Integer())
    name = db.Column(db.String(100))
    birthday = db.Column(db.Text())
    blood_group = db.Column(db.Text())
    fathers_name = db.Column(db.Text())
    issue_date = db.Column(db.Text())
    validity = db.Column(db.Text())
    license_no = db.Column(db.Integer(),  primary_key= True)
    issuing_authority = db.Column(db.Text())
    image = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now())


    def __init__(self, name, birthday, blood_group, fathers_name, issue_date, validity, license_no, issuing_authority, image):
        self.name = name
        self.birthday = birthday
        self.blood_group = blood_group
        self.fathers_name = fathers_name
        self.issue_date = issue_date
        self.validity = validity
        self.license_no = license_no
        self.issuing_authority = issuing_authority
        self.image = image


class RidersInformationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'birthday', 'blood_group', 'fathers_name', 'issue_date', 'validity', 'license_no', 'issuing_authority', 'image')


rider_information_schema = RidersInformationSchema()
riders_information_schema = RidersInformationSchema(many = True)


@app.route('/get', methods = ['GET'])
def get_riderDetails():
    all_rider_details = RidersInformation.query.all()
    results = riders_information_schema.dumps(all_rider_details)
    return jsonify(results)


@app.route('/get/<license_no>/', methods=['GET'])
def post_riderDetails(license_no):
    riders = RidersInformation.query.get(license_no)
    return rider_information_schema.jsonify(riders)

@app.route('/add', methods = ['POST'])
def add_riderDetails():
    name = request.json['name']
    birthday = request.json['birthday']
    blood_group = request.json['blood_group']
    fathers_name = request.json['fathers_name']
    issue_date = request.json['issue_date']
    validity = request.json['validity']
    license_no = request.json['license_no']
    issuing_authority = request.json['issuing_authority']
    image = request.json['image']

    riders = RidersInformation(name, birthday, blood_group, fathers_name, issue_date, validity, license_no, issuing_authority, image)
    db.session.add(riders)
    db.session.commit()
    return rider_information_schema.jsonify(riders)


@app.route('/update/<license_no>/', methods=['PUT'])
def update_riderDetails(license_no):
    riders = RidersInformation.query.get(license_no)

    name = request.json['name']
    birthday = request.json['birthday']
    blood_group = request.json['blood_group']
    fathers_name = request.json['fathers_name']
    issue_date = request.json['issue_date']
    validity = request.json['validity']
    issuing_authority = request.json['issuing_authority']
    image = request.json['image']

    riders.name = name
    riders.birthday = birthday
    riders.blood_ = blood_group
    riders.fathers_name = fathers_name
    riders.issue_date = issue_date
    riders.validity = validity
    riders.issuing_authority = issuing_authority
    riders.image = image

    db.session.commit()
    return rider_information_schema.jsonify(riders)


@app.route('/delete/<license_no>/', methods=['DELETE'])
def riderDetails_delete(license_no):
    rider = RidersInformation.query.get(license_no)
    db.session.delete(rider)
    db.session.commit()

    return rider_information_schema.jsonify(rider)



if __name__ == '__main__':
    app.run(host = '192.168.31.160', port =5000, debug=True)