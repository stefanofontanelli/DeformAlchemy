# Copyright (C) 2012 the DeformAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is released under the MIT License
# http://www.opensource.org/licenses/mit-license.php

from .widget import (SQLAlchemySelectWidget,
                     SQLAlchemyChosenSingleWidget,
                     SQLAlchemyChosenMultipleWidget)
from colanderalchemy import SQLAlchemySchemaNode
from deform import Form
from deform.widget import (CheckboxWidget,
                           DateInputWidget,
                           DateTimeInputWidget,
                           RadioChoiceWidget,
                           TextAreaWidget,
                           TextInputWidget)
from deform_bootstrap.widget import DateTimeInputWidget as DateTimeWidget
from inspect import isfunction
from sqlalchemy import (Boolean,
                        Date,
                        DateTime,
                        Enum,
                        Float,
                        inspect,
                        Integer,
                        String,
                        Text,
                        Time)


class SQLAlchemyForm(Form):

    def __init__(self, class_, includes=None, excludes=None, overrides=None, **kw):
        self.class_ = class_
        self.bootstrap = 'bootstrap_form_style' in kw
        schema = SQLAlchemySchemaNode(class_,
                                      includes=includes,
                                      excludes=excludes,
                                      overrides=overrides)
        self.inspector = inspect(class_)
        for prop in self.inspector.attrs:

            name = prop.key
            if name not in schema or not schema[name].widget is None:
                continue

            try:
                getattr(self.inspector.column_attrs, name)
                factory = 'get_widget_from_column'

            except AttributeError:
                getattr(self.inspector.relationships, name)
                factory = 'get_widget_from_relationship'

            schema[name].widget = getattr(self, factory)(prop)

        Form.__init__(self, schema, **kw)

    def get_widget_from_column(self, prop):

        name = prop.key
        column = prop.columns[0]
        foreign_keys = column.foreign_keys
        column_type = getattr(column.type, 'impl', column.type)
        if foreign_keys:
            # Use FKs to retrieve referenced class
            # and use it to create a select box.
            table = list(foreign_keys)[0].column.table
            for name, class_ in self.class_._decl_class_registry.items():

                if name == '_sa_module_registry' or \
                   class_.__table__ != table:
                    continue

                widget = self.get_select_widget_from_class(class_, False)
                break

        elif isinstance(column_type, Boolean):
            widget = CheckboxWidget()

        elif isinstance(column_type, Date):
            widget = DateInputWidget()

        elif isinstance(column_type, DateTime):
            if self.bootstrap:
                widget = DateTimeWidget()
            else:
                widget = DateTimeInputWidget()

        elif isinstance(column_type, Enum):
            values = [(value, value) for value in column.type.enums]
            widget = RadioChoiceWidget(values=values)

        elif isinstance(column_type, Text):
            widget = TextAreaWidget()

        else:
            widget = TextInputWidget()

        return widget

    def get_widget_from_relationship(self, prop):

        if isfunction(prop.argument):
            class_ = prop.argument()

        else:
            class_ = prop.argument

        return self.get_select_widget_from_class(class_, prop.uselist)

    def get_select_widget_from_class(self, class_, multiple):

        inspector = inspect(class_)
        primary_keys = inspector.primary_key
        if len(primary_keys) > 1:
            msg = 'Multiple primary keys are not supported'
            raise NotImplementedError(msg)

        key = primary_keys[0].key
        if self.bootstrap and multiple:
            widget = SQLAlchemyChosenMultipleWidget(class_,
                                                    label=key,
                                                    value=key)

        elif self.bootstrap:
            widget = SQLAlchemyChosenSingleWidget(class_,
                                                  label=key,
                                                  value=key)

        else:
            widget = SQLAlchemySelectWidget(class_,
                                            label=key,
                                            value=key,
                                            multiple=multiple)

        return widget

    def populate_widgets(self, session):

        for node in self.schema:
            try:
                node.widget.populate(session)

            except AttributeError:
                continue
