from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.String(400), primary_key=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    father_id = db.Column(db.String(400), db.ForeignKey ('person.id'), nullable= True)
    mother_id = db.Column(db.String(400), db.ForeignKey ('person.id'), nullable = True)

    def __repr__(self):
        return '<Person %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "rol":self.rol,
            "age":self.age,
            "father_id":self.father_id,
            "mother_id":self.mother_id
                
            # do not serialize the password, its a security breach
        }

    def get_persons():
        persons = Person.query.order_by(Person.age.desc())
        persons = list(map(lambda person: person.serialize(), persons))
        return persons

    def get_person_id(id):
        Me = Person.query.get(id)
        Father = Person.query.filter_by(id=Me.father_id).first()
        if Father is None:
            Father = []
        Mother = Person.query.filter_by(id=Me.mother_id).first()
        if Mother is None:
            Mother = []
        Child = Person.query.filter( (Person.father_id == id) | (Person.mother_id == id) ).first()
        if Child is None:
            Child = []
        family = {
            "father": Person.serialize(Father),
            "mother": Person.serialize(Mother),
            "me": Person.serialize(Me),
            "child": Person.serialize(Child)
            
        }
        
   
    def create_person(name, last_name, rol, age, father_id, mother_id):
        person = Person(name=name, last_name=last_name, rol=rol, age=age, father_id=father_id, mother_id=mother_id)
        db.session.add(person)
        db.session.commit()