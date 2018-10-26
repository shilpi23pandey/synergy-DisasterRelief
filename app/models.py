from app import db


class Guest(db.Model):
    """Simple database model to track event attendees."""

    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

class Request(db.Model):
    """Simple database model to track event attendees."""

    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    contact = db.Column(db.String(12))
    resourceType = db.Column(db.String(20))
    details = db.Column(db.String(500))
    location=db.Column(db.String(80))
    timestamp=db.Column(db.DateTime)
    

    def __init__(self, name=None, contact=None, resourceType=None,details=None,location=None,timestamp=None):
        self.name = name
        self.contact = contact
        self.resourceType = resourceType
        self.details = details
        self.location = location
        self.timestamp = timestamp
        
class Caution(db.Model):

    __tablename__='caution'
    id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String(80))
    time = db.Column(db.DateTime)
    type_of_caution=db.Column(db.String(80))
    
    def __init__(self, name=None, location=None,time=None,type_of_caution=None):
        self.name = name
        self.location = location
        self.time = time
        self.type_of_caution=type_of_caution


class Casuality(db.Model):

    __tablename__='casuality'
    id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String(80))
    time = db.Column(db.DateTime)
    infra_or_people=db.Column(db.String(80))
    
    def __init__(self, name=None, location=None,time=None,infra_or_people=None):
        self.name = name
        self.location = location
        self.time = time
        self.infra_or_people=infra_or_people

class Donation(db.Model):
    
    __tablename__='donation'
    id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String(80))
    time = db.Column(db.DateTime)
    intention=db.Column(db.String(20))
    type_of_resource=db.Column(db.String(40))
    
    def __init__(self, name=None, location=None,time=None,intention=None,type_of_resource=None):
        self.name = name
        self.location = location
        self.time = time
        self.intention=intention
        self.type_of_resource=type_of_resource


class Mapping(db.Model):
    
    __tablename__='mapping'
    id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String(80))
    typeM = db.Column(db.String(40))
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    confidence=db.Column(db.Float)

    def __init__(self, location=None,typeM=None,latitude=None,longitude=None,confidence=0):
        self.location = location
        self.typeM = typeM
        self.latitude=latitude
        self.longitude=longitude
        self.confidence=confidence