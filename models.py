from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# many-to-many relationships
person_behaviors = db.Table('person_behaviors',
                            db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
                            db.Column('behavior_id', db.Integer, db.ForeignKey('behavior.id'), primary_key=True)
                            )


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(500), nullable=True)

    # many-to-many relationship with behaviors
    behaviors = db.relationship('Behavior', secondary=person_behaviors, backref='people')

    def to_dict(self):
        """convert person to dictionary with behaviors grouped by type"""
        approved = [b.description for b in self.behaviors if b.behavior_type == 'approved']
        hide = [b.description for b in self.behaviors if b.behavior_type == 'hide']

        return {
            'id': self.id,
            'name': self.name,
            'photoUrl': self.photo_url,
            'behaviors': {
                'approved': approved,
                'hide': hide
            }
        }


class Behavior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    behavior_type = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'type': self.behavior_type
        }