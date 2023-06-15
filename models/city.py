#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
# import sqlalchemy modules
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


<<<<<<< HEAD
class City(BaseModel, Base):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", cascade='all, delete', backref="cities")
=======
class City(BaseModel):
    """ The city class, contains state ID and name """
    state_id = ""
    name = ""
>>>>>>> fadd9a816bad09078ac0c136eb3a6789a136be7c
