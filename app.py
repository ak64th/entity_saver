import datetime
import logging
from flask import Flask, request, jsonify
from flask_peewee.db import Database
from flask_peewee.utils import get_dictionary_from_model
from config import Configuration
from peewee import *

app = Flask(__name__)
app.config.from_object(Configuration)

db = Database(app)


class Entry(db.Model):
    form = TextField()
    form_name = TextField()
    entry = TextField()
    saved_at = DateTimeField(default=datetime.datetime.now)


Entry.create_table(fail_silently=True)


@app.route('/api/entity/', methods=['POST'])
def index():
    data = request.get_json(force=True)
    app.logger.debug(data)
    entry = Entry.create(form=data['form'], form_name=data['form_name'], entry=data['entry'])
    return jsonify(get_dictionary_from_model(entry))

if __name__ == '__main__':
    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host='0.0.0.0', port=4000)