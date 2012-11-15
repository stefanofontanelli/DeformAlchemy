# Copyright (C) 2012 the DeformAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is released under the MIT License
# http://www.opensource.org/licenses/mit-license.php

from deformalchemy import SQLAlchemyForm
from .models import (Account,
                     Base,
                     Person,
                     Address)
import logging
import sys

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    # In Python < 2.7 use unittest2.
    import unittest2 as unittest

else:
    import unittest


log = logging.getLogger(__name__)


class TestsSQLAlchemyForm(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_account_form(self):
        form = SQLAlchemyForm(Account)
        bootstrap_form = SQLAlchemyForm(Account,
                                        bootstrap_form_style='form-vertical')

    def test_person_form(self):
        form = SQLAlchemyForm(Person)
        bootstrap_form = SQLAlchemyForm(Person,
                                        bootstrap_form_style='form-vertical')

    def test_address_form(self):
        form = SQLAlchemyForm(Address)
        bootstrap_form = SQLAlchemyForm(Address,
                                        bootstrap_form_style='form-vertical')

    def test_widget_populate(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.orm import scoped_session
        engine = create_engine('sqlite:///')
        Base.metadata.bind = engine
        Base.metadata.create_all()
        session = scoped_session(sessionmaker(bind=engine))()
        form = SQLAlchemyForm(Address,
                              bootstrap_form_style='form-vertical')
        widget = form['person'].widget
        widget.populate(session)

