from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Owner, Animal, Vet, AnimalVetVisit
from datetime import datetime
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# App configuration (Database URI and disable modification tracking)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') # Update the URI if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Routes

# 1. Root endpoint
@app.route('/')
def index():
    return "Welcome to petify!"


# 2. Create a full record (POST)
@app.route('/create_full_record', methods=['POST'])
def create_full_record():
    data = request.get_json()

    required_fields = ['owner_name', 'owner_address', 'owner_phone', 'owner_email', 
                       'animal_name', 'animal_species', 'animal_age', 'animal_image', 
                       'vet_name', 'vet_specialty', 'vet_phone', 'vet_email', 'visit_date', 'notes']
    
    if not all(key in data for key in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Owner: Check if exists or create a new one
        owner = Owner.query.filter_by(email=data['owner_email']).first()
        if not owner:
            owner = Owner(name=data['owner_name'], address=data['owner_address'], 
                          phone_number=data['owner_phone'], email=data['owner_email'])
            db.session.add(owner)
            db.session.commit()

        # Vet: Check if exists or create a new one
        vet = Vet.query.filter_by(email=data['vet_email']).first()
        if not vet:
            vet = Vet(name=data['vet_name'], specialty=data['vet_specialty'], 
                      phone_number=data['vet_phone'], email=data['vet_email'])
            db.session.add(vet)
            db.session.commit()

        # Animal: Check if exists or update
        animal = Animal.query.filter_by(name=data['animal_name'], owner_id=owner.owner_id).first()
        if not animal:
            animal = Animal(name=data['animal_name'], species=data['animal_species'], 
                            age=int(data['animal_age']), animal_image=data['animal_image'], owner_id=owner.owner_id)
            db.session.add(animal)
            db.session.commit()
        else:
            # If animal exists, update the animal (image, age, etc.)
            animal.name = data['animal_name']
            animal.species = data['animal_species']
            animal.age = int(data['animal_age'])
            animal.animal_image = data['animal_image']
            db.session.commit()

        # Create a new visit for the animal and vet
        visit_date = datetime.strptime(data['visit_date'], '%Y-%m-%d').date()
        visit = AnimalVetVisit(animal_id=animal.animal_id, vet_id=vet.vet_id, visit_date=visit_date, notes=data['notes'])
        db.session.add(visit)
        db.session.commit()

        return jsonify({
            "visit_id": visit.visit_id,
            "owner_name": owner.name,
            "owner_address": owner.address,
            "owner_phone": owner.phone_number,
            "owner_email": owner.email,
            "animal_name": animal.name,
            "animal_species": animal.species,
            "animal_age": animal.age,
            "animal_image": animal.animal_image,
            "vet_name": vet.name,
            "vet_specialty": vet.specialty,
            "vet_phone": vet.phone_number,
            "vet_email": vet.email,
            "visit_date": visit.visit_date.strftime('%Y-%m-%d'),
            "notes": visit.notes
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error, possibly a duplicate entry"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400




# 3. Get all records (GET)
@app.route('/all_records', methods=['GET'])
def get_all_records():
    visits = AnimalVetVisit.query.all()
    result = []

    for visit in visits:
        result.append({
            "visit_id": visit.visit_id,  # Include visit_id in the response
            "owner_name": visit.animal.owner.name,
            "owner_address": visit.animal.owner.address,
            "owner_phone": visit.animal.owner.phone_number,
            "owner_email": visit.animal.owner.email,
            "animal_name": visit.animal.name,
            "animal_species": visit.animal.species,
            "animal_age": visit.animal.age,
            "animal_image": visit.animal.animal_image,
            "vet_name": visit.vet.name,
            "vet_specialty": visit.vet.specialty,
            "vet_phone": visit.vet.phone_number,
            "vet_email": visit.vet.email,
            "visit_date": visit.visit_date.strftime('%Y-%m-%d'),
            "notes": visit.notes
        })

    return jsonify(result), 200


# 4. Update a full record (PUT)
@app.route('/update_full_record/<int:visit_id>', methods=['PUT'])
def update_full_record(visit_id):
    data = request.get_json()

    visit = AnimalVetVisit.query.get(visit_id)
    if not visit:
        return jsonify({"error": "Visit not found"}), 404

    try:
        # Update Visit information
        visit.visit_date = datetime.strptime(data['visit_date'], '%Y-%m-%d').date()
        visit.notes = data['notes']
        db.session.commit()

        # Update associated Animal information
        animal = visit.animal
        animal.name = data['animal_name']
        animal.species = data['animal_species']
        animal.age = data['animal_age']
        animal.animal_image = data['animal_image']
        db.session.commit()

        # Update associated Vet information
        vet = visit.vet
        vet.name = data['vet_name']
        vet.specialty = data['vet_specialty']
        vet.phone_number = data['vet_phone']
        db.session.commit()

        # Update associated Owner information
        owner = animal.owner
        owner.name = data['owner_name']
        owner.address = data['owner_address']
        owner.phone_number = data['owner_phone']
        owner.email = data['owner_email']
        db.session.commit()

        return jsonify({
            "visit_id": visit.visit_id,
            "owner_name": owner.name,
            "owner_address": owner.address,
            "owner_phone": owner.phone_number,
            "owner_email": owner.email,
            "animal_name": animal.name,
            "animal_species": animal.species,
            "animal_age": animal.age,
            "animal_image": animal.animal_image,
            "vet_name": vet.name,
            "vet_specialty": vet.specialty,
            "vet_phone": vet.phone_number,
            "vet_email": vet.email,
            "visit_date": visit.visit_date.strftime('%Y-%m-%d'),
            "notes": visit.notes
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# 5. Delete a full record (DELETE)
#models.py it has the table
@app.route('/delete_full_record/<int:visit_id>', methods=['DELETE'])
def delete_full_record(visit_id):
    # Find the AnimalVetVisit by visit_id
    visit = AnimalVetVisit.query.get(visit_id)
    if not visit:
        print(f"Visit with ID {visit_id} not found.")
        return jsonify({"error": "Visit not found"}), 404

    try:
        print(f"Found visit: {visit.visit_id}")

        # Access animal and owner before deleting the visit
        animal = visit.animal
        owner = animal.owner

        print(f"Found animal: {animal.animal_id} for visit {visit_id}")
        print(f"Found owner: {owner.owner_id} for animal {animal.animal_id}")

        # Delete the visit
        db.session.delete(visit)
        db.session.commit()
        print(f"Visit {visit_id} deleted successfully.")

        # Check if the associated animal still has any remaining visits
        if not animal.visits:  # No other visits exist for this animal
            print(f"Animal {animal.animal_id} has no other visits. Deleting the animal.")
            # Delete the animal if no visits remain
            db.session.delete(animal)
            db.session.commit()
            print(f"Animal {animal.animal_id} deleted successfully.")

            # Check if the associated owner has any other animals
            if not owner.animals:  # No other animals exist for this owner
                print(f"Owner {owner.owner_id} has no other animals. Deleting the owner.")
                # Delete the owner if no animals remain
                db.session.delete(owner)
                db.session.commit()
                print(f"Owner {owner.owner_id} deleted successfully.")

        return jsonify({"message": "Record deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400






# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False)