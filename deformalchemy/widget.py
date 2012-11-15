# Copyright (C) 2012 the DeformAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is released under the MIT License
# http://www.opensource.org/licenses/mit-license.php

from deform.widget import SelectWidget
from deform_bootstrap.widget import (ChosenMultipleWidget,
                                     ChosenSingleWidget)
from pyramid.path import DottedNameResolver


class SQLAlchemyWidget(object):

    def __init__(self, class_, label, value, order_by=None, *filters):
        self.class_ = class_
        self.label = label
        self.value = value
        self.filters = filters
        self.order_by = order_by

    def populate(self, session, *filters):

        class_ = self.class_
        if isinstance(class_, basestring):
            # FIXME: replace DottedNameResolver
            # to remove pyramid from setup requires.
            class_ = DottedNameResolver().resolve(class_)

        query = session.query(getattr(class_, self.value),
                              getattr(class_, self.label))
        if not self.order_by is None:
            order_by = getattr(class_, self.order_by)

        else:
            order_by = None

        if not filters:
            filters = self.filters

        query = query.filter(*filters).order_by(order_by).distinct()
        self.values = [('', '')] + [(unicode(t[0]), unicode(t[1])) for t in query.all()]


class SQLAlchemySelectWidget(SQLAlchemyWidget, SelectWidget):
    
    def __init__(self, class_, label, value, order_by=None, *filters, **kw):
        SQLAlchemyWidget.__init__(self, class_, label, value, order_by, *filters)
        SelectWidget.__init__(self, **kw)


class SQLAlchemyChosenSingleWidget(SQLAlchemyWidget, ChosenSingleWidget):
    
    def __init__(self, class_, label, value, order_by=None, *filters, **kw):
        SQLAlchemyWidget.__init__(self, class_, label, value, order_by, *filters)
        ChosenSingleWidget.__init__(self, **kw)


class SQLAlchemyChosenMultipleWidget(SQLAlchemyWidget, ChosenMultipleWidget):
    
    def __init__(self, class_, label, value, order_by=None, *filters, **kw):
        SQLAlchemyWidget.__init__(self, class_, label, value, order_by, *filters)
        ChosenMultipleWidget.__init__(self, **kw)
