#models.py it has the table
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owner'
    
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    animals = db.relationship('Animal', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<Owner {self.name}>'

    # Adding serialization
    serialize_only = ('owner_id', 'name', 'address', 'phone_number', 'email')

class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animal'
    
    animal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50))
    animal_image = db.Column(db.Text)  # Use Text for storing long URLs
    age = db.Column(db.Integer)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)
    
    visits = db.relationship('AnimalVetVisit', backref='animal', lazy=True)

    def __repr__(self):
        return f'<Animal {self.name} ({self.species})>'

    # Adding serialization
    serialize_only = ('animal_id', 'name', 'species', 'animal_image', 'age', 'owner_id')

    # Validate the 'name' field to ensure it is not empty
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Animal name cannot be empty")
        return value

class Vet(db.Model, SerializerMixin):
    __tablename__ = 'vet'
    
    vet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    visits = db.relationship('AnimalVetVisit', backref='vet', lazy=True)

    def __repr__(self):
        return f'<Vet {self.name}>'

    # Adding serialization
    serialize_only = ('vet_id', 'name', 'specialty', 'phone_number', 'email')

    # Validate the 'email' field to ensure it follows the correct format
    @validates('email')
    def validate_email(self, key, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        return value

class AnimalVetVisit(db.Model, SerializerMixin):
    __tablename__ = 'animal_vet_visit'
    
    visit_id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.vet_id', ondelete='CASCADE'), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Visit {self.visit_id} on {self.visit_date} for {self.animal.name}>'

    serialize_only = ('visit_id', 'animal_id', 'vet_id', 'visit_date', 'notes')

    @validates('visit_date')
    def validate_visit_date(self, key, value):
        from datetime import date
        if value > date.today():
            raise ValueError("Visit date cannot be in the future")
        return value