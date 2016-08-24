# encoding: utf-8
# pylint: disable=missing-docstring
"""
Quest Server
============

This is an HTTP server for LOL Quests.
"""
import json
import os
from flask import Flask, render_template, abort, request
from flask import redirect


def create_app():
    _app = Flask(__name__)

    project_folder = os.path.dirname(__file__)
    with open(os.path.join(project_folder, "hashes_map.json")) as hashes_map_file:
        _app.config['QUEST_STAGE_RELATIONS'] = json.loads(hashes_map_file.read())
    return _app

app = create_app()  # pylint: disable=invalid-name


@app.route('/', methods=['GET', 'POST'])
def root():
    error = ""
    if request.method == 'POST':
        first_stage_hash = request.form.get('password')
        if first_stage_hash not in app.config['QUEST_STAGE_RELATIONS']:
            error = "Неправильный пароль"
        else:
            return redirect('/' + request.form.get('password', ''))
    return render_template('home.html', error=error)


@app.route('/<team_stage_hash>', methods=['GET', 'POST'])
def stage(team_stage_hash):
    if team_stage_hash not in app.config['QUEST_STAGE_RELATIONS']:
        abort(403)
    team_stage = app.config['QUEST_STAGE_RELATIONS'][team_stage_hash]
    template_kwargs = {
        'stage': team_stage['stage'],
    }
    if request.method == 'POST':
        if request.form.get('password') == team_stage['stage']['key']:
            return redirect('/' + team_stage['next_hash'])
        template_kwargs['error'] = "Неправильный пароль"
    return render_template(
        "quest_stages/%s" % team_stage['stage']['template_name'],
        **template_kwargs
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
