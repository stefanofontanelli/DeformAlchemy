# Copyright (C) 2012 the DeformAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is released under the MIT License
# http://www.opensource.org/licenses/mit-license.php

from sqlalchemy import (Boolean,
                        Column,
                        Date,
                        DateTime,
                        Enum,
                        Float,
                        ForeignKey,
                        Integer,
                        Numeric,
                        Time,
                        Unicode,
                        UnicodeText)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()


class Account(Base):

    __tablename__ = 'accounts'

    email = Column(Unicode(64), primary_key=True)
    enabled = Column(Boolean, default=True)
    created = Column(DateTime, nullable=True, default=datetime.datetime.now)
    timeout = Column(Time, nullable=False)
    note = Column(UnicodeText)
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person')


class Person(Base):

    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    surname = Column(Unicode(32), nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    birthday = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    addresses = relationship('Address')


class Address(Base):

    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street = Column(Unicode(64), nullable=False)
    city = Column(Unicode(32), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Numeric, nullable=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship(Person)
