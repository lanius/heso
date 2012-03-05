# coding: utf-8
from wtforms import (
    Form, FormField, FieldList, HiddenField, TextField, TextAreaField,
    validators, ValidationError, widgets
)
from wtforms.validators import Required


class HesofileForm(Form):
    filename = TextField(u'filename', [validators.required()])
    document = TextAreaField(u'document', [validators.required()])
    removed = HiddenField(u'removed')


class HesoForm(Form):
    description = TextField(u'description', [validators.required()])
    files = FieldList(FormField(HesofileForm), min_entries=1)
