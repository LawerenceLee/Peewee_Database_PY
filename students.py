#students.py
from peewee import *

db = SqliteDatabase('students.db')  


class Student(Model):
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)
    
    class Meta:
        database = db

# students.py continued

students = [
    {'username': 'charlieTucker',
    'points': 9},
    {'username': 'Mwallace',
    'points': 30234},
    {'username': 'FantasticSam',
    'points': 26323},
    {'username': 'JuliePeaches',
    'points': 64890}
]

def add_students():
    for pupil in students:
        try:
            Student.create(username=pupil['username'],
                      points=pupil['points'])
        except IntegrityError:
            pupil_record = Student.get(username=pupil['username'])
            pupil_record.points = pupil['points']
            pupil_record.save()
            
def top_student():
    student = Student.select().order_by(Student.points.desc()).get()
    return student
        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Student], safe=True)
    add_students()
    print('Our top student right now is: {0.username}.'.format(top_student()))