import os
import datetime
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
import pandas as pd,re

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# initialize database migration management
migrate = Migrate(app, db)

def getJsonList():
    from models import Mapping
    db.create_all()
    geoCords=Mapping.query.all()
    #json_output = json.dumps(geoCords)
    return geoCords

@app.route('/')
def home_page():
    jdata=getJsonList()
    return render_template('index.html',maps=jdata,total_locations=len(jdata))

@app.route('/populate')
def populate_table():
    df = pd.read_csv('finalExtracted.csv')
    df = df[df['predicted_class1']=='Informative']
    print(df.columns)
    from models import Request,Mapping
    for index, row in df.iterrows():
        if row['predicted_class2']=='Caution and advice':
            if pd.isna(row['predicted_where_caution_x'])==False:
                s=row['predicted_where_caution_x']
                locations=s.split(', ')
                for place in locations:
                    if len(place)>1:
                        place=re.sub(r"[^a-zA-Z0-9]",' ', place)
                        place=re.sub(' +',' ',place)
                        mapping=Mapping(place)
                        db.session.add(mapping)
                        db.session.commit()
        if row['predicted_class2']=='Casualities and damage':
            if pd.isna(row['predicted_where_casuality'])==False:

                s=row['predicted_where_casuality']
                print(s)
                locations=s.split(', ')
                for place in locations:
                    if len(place)>1:
                        place=re.sub(r"[^a-zA-Z0-9]",' ', place)
                        place=re.sub(' +',' ',place)
                        mapping=Mapping(place)
                        db.session.add(mapping)
                        db.session.commit()  
        if row['predicted_class2']=='Donations of money, goods or services':
            if pd.isna(row['predicted_where_donation'])==False and row['intention']=='Invites/asks people to donate/provide/give/do something':
                s=row['predicted_where_donation']
                locations=s.split(', ')
                for place in locations:
                    if len(place)>1:
                        place=re.sub(r"[^a-zA-Z0-9]",' ', place)
                        place=re.sub(' +',' ',place)
                        mapping=Mapping(place)
                        db.session.add(mapping)
                        db.session.commit() 

    return "Populate data"

@app.route('/request')
def resources_required():
	return render_template('request.html')

@app.route('/processRequest', methods=['POST'])
def processRequest():
    from models import Request,Mapping
    db.create_all()
    name = request.form.get('request_name')
    contact = request.form.get('request_contact')
    location = request.form.get('request_location')
    resource = request.form.get('request_resource')
    additional = request.form.get('request_additional')
    timestamp=datetime.datetime.now()
    user_request = Request(name,contact,resource,additional,location,timestamp)
    db.session.add(user_request)
    mapping=Mapping(location,resource)
    db.session.add(mapping)
    db.session.commit()
    return redirect('/')

@app.route('/confidence',methods=['POST'])
def confidence():
    location_id = request.form.get('validate_location')
    print(location_id)
    from models import Mapping
    location_row = Mapping.query.filter_by(id=location_id).first()
    location_row.confidence = location_row.confidence+1
    db.session.commit()
    return redirect('/validate')


@app.route('/validate')
def validateData():
    all_locations = getJsonList()
    return render_template('validate.html',all_locations=all_locations)

def getCords(location):
    from bingmaps.apiservices import LocationByAddress
    key='Apv2l9wgX2-JuwgKuHx6Y8_1BM-LOksxxRa-6kGfdGWzNx4ZHEyuSyffdo1bOR0P'
    data = {'locality': location,'country':'USA','key': key}
    loc_by_address = LocationByAddress(data)
    return (loc_by_address.get_coordinates)

@app.route('/refreshMap')
def refreshMap():
    from models import Mapping
    geoCords=Mapping.query.all()
    for row in geoCords:
        if row.latitude==None:
            print("here")
            print(row.location)
            cords=getCords(row.location)
            print(cords)
            if(len(cords)==0):
                print("nahi mila") 
            else:
                row.latitude=cords[0].latitude
                row.longitude=cords[0].longitude
            db.session.commit()
    return redirect('/')

@app.route('/admin')
def admin():
    return render_template('admin.html')
