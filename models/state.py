#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref="state",
                              cascade="all, delete-orphan")

    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""

        super().__init__(*args, **kwargs)

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """get the cities for states"""
            from models import storage

            dict_cities = storage.all(City).values()
            cities = []

            for obj in dict_cities:
                if obj.state_id == self.id:
                    cities.append(obj)

            return cities
