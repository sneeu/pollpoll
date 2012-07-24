import logging

from flask.ext.wtf import FieldList, Form, HiddenField, TextField, validators


logger = logging.getLogger(__name__)


class PollForm(Form):
    question = TextField('Question', [validators.Required()])
    choices = FieldList(
        TextField('Choice', [validators.required()]), min_entries=2)


class VoteForm(Form):
    choice = HiddenField('Choice')
