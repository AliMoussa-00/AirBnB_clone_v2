#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import os

from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
            )


class Place(BaseModel, Base):
    """ A place to stay """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "places"

        city_id = Column(String(60),
                         ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60),
                         ForeignKey('users.id'),
                         nullable=False)

        name = Column(String(128), nullable=False)
        description = Column(String(128), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")

        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """attribute that returns list of Review instances"""
            reviews = models.storage.all("Review").values()
            list_review = []

            for review in reviews:
                if review.place_id == self.id:
                    list_review.append(review)

            return list_review

        @property
        def amenities(self):
            """attribute that returns list of Amenty instances"""
            amenities = models.storage.all("Amenity").values()
            list_amenities = []

            for ame in amenities:

                if ame.id in self.amenity_ids:
                    list_amenities.append(ame)

            return list_amenities

        @amenities.setter
        def amenities(self, value):
            """add 'Amenity.id' to 'amenitiy_id' """
            if type(value).__name__ == "Amenity":
                self.amenity_ids.append(value.id)
