#!/usr/bin/python3
"""
new storage class DBStorage
"""
import models
from sqlalchemy import (create_engine)
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    class DBStorage
    will create engnie
    will create a new session
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        initializes the object DBStorage
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')
            ), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        method returns a dictionary
        """

        our_objects = {}
        our_classes = [value for key, value in models.classes.items()]

        if cls is None:
            for obj in self.__session.query(User, State, City, Amenity,
                                            Place, Review).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                our_objects[key] = obj
        else:
            for obj in self.__session.query(eval(cls)).all():
                key = "{}.{}".format(eval(cls).__name__, obj.id)
                our_objects[key] = obj
        return our_objects

    def new(self, obj):
        """
        Adds a new object to the database
        """
        self.__session.add(obj)

    def save(self):
        """
        saves the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes the current object
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables in the db & current session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)

        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        removes / closes the session
        """
        self.__session.close()