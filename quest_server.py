import json
import os
from flask import Flask, render_template, abort, request
from flask import redirect

app = Flask(__name__)

project_folder = os.path.dirname(__file__)

hashes_map_file = open(os.path.join(project_folder, "hashes_map.json"))
hashes_map = json.loads(hashes_map_file.read())

@app.route('/', methods=['GET', 'POST'])
def root():
    error = ""
    if request.method == 'POST':
        first_stage_hash = request.form.get('password')
        if not first_stage_hash in hashes_map:
            error = "Неправильный пароль"
        else:
            return redirect('/' + request.form.get('password', ''))
    return render_template('home.html', error=error)


@app.route('/<id_hash>', methods=['GET', 'POST'])
def main(id_hash):
    template_kwargs = {}
    if request.method == 'GET':
        try:
            stage = hashes_map[id_hash]['stage']
            template_kwargs['stage'] = stage
        except KeyError:
            abort(403)
    else:
        if id_hash in hashes_map and hashes_map[id_hash]['stage']['key'] == request.form.get('password'):
            return redirect('/' + hashes_map[id_hash]['next_hash'])
        template_kwargs['stage'] = hashes_map[id_hash]['stage']
        template_kwargs['error'] = "Неправильный пароль"
    return render_template("quest_stage.html", **template_kwargs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
