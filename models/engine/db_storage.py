#!/usr/bin/python3
"""File to Implement the DB storage"""
import os

from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User

from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session


classes = {
        "User": User, "State": State, "City": City,
        "Amenity": Amenity, "Place": Place, "Review": Review
        }


class DBStorage():
    """Implementing the class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializing the instance"""

        user = os.getenv('HBNB_MYSQL_USER')
        pw = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pw, host, db),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            # drop all tables if testing

            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all objects depending of the class name"""

        if not self.__session:
            self.reload()

        objects = {}

        if type(cls) is str:
            cls = classes[cls]

        if cls in classes.values():

            for obj in self.__session.query(cls).all():
                objects[obj.__class__.__name__ + '.' + obj.id] = obj

        else:
            for c in classes.values():
                for obj in self.__session.query(c):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj

        return objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all table in DB and start a Session"""

        Base.metadata.create_all(bind=self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """close the db session"""
        self.__session.close()
