import logging

from flask.ext.wtf import FieldList, Form, HiddenField, HTMLString, \
    TextField, html_params, validators


logger = logging.getLogger(__name__)


class ListWidget(object):
    def __init__(self, html_tag='ul', prefix_label=True):
        assert html_tag in ('ol', 'ul')
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<li>%s %s</li>' % (subfield.label, subfield()))
            else:
                html.append('<li>%s %s</li>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class PollForm(Form):
    question = TextField('Question', [validators.Required()])
    choices = FieldList(
        TextField('Choice'),
        min_entries=2, widget=ListWidget())


class VoteForm(Form):
    choice = HiddenField('Choice')
