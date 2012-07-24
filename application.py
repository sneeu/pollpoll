from flask import Flask, redirect, render_template, request, url_for

from data import Poll, Choice
from forms import PollForm, VoteForm


app = Flask(__name__)
app.debug = True
app.secret_key = 'e=(oo3Uwaaz-<j\'2~BHQQd}VO)*9P;[k|Okd2#!J^4y7#g[?3*\wfd0z|y'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/polls/new', methods=['GET', 'POST'])
def poll_create():
    form = PollForm(request.form)
    app.logger.debug(form)

    if form.validate_on_submit():
        poll = Poll.create(form.question.data)
        for choice in form.choices:
            Choice.create(poll.key, choice.data)
        return redirect(url_for('poll_detail', poll_key=poll.key))

    return render_template('poll_create.html', form=form)


@app.route('/polls/<poll_key>', methods=['GET', 'POST'])
def poll_detail(poll_key):
    poll = Poll.load(poll_key)

    if request.method == 'POST':
        choice = poll.choice_by_name(request.form.get('choice'))
        if choice:
            choice.register_vote()
            return redirect(url_for('poll_detail', poll_key=poll.key))

    choices = [
        (choice, VoteForm(choice=choice.name), ) for choice in poll.choices]
    return render_template('poll_detail.html', poll=poll, choices=choices)


if __name__ == '__main__':
    app.run()
