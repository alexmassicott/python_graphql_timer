from uuid import uuid4


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Department, Employee, Role
    
    # Create the fixtures
    engineering = Department(id=str(uuid4()), name='Engineering')
    engineering.save()
    hr = Department(id=str(uuid4()), name='Human Resources')
    hr.save()

    manager = Role(id=str(uuid4()), name='manager')
    manager.save()

    engineer = Role(id=str(uuid4()), name='engineer')
    engineer.save()

    peter = Employee(id=str(uuid4()), name='Peter', department=engineering, role=engineer)
    peter.save()

    roy = Employee(id=str(uuid4()), name='Roy', department=engineering, role=engineer)
    roy.save()

    tracy = Employee(id=str(uuid4()), name='Tracy', department=hr, role=manager)
    tracy.save()
