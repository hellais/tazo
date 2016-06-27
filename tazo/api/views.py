import os
import re

from flask import Blueprint, jsonify
from flask import request

from ..testlists import csv_to_dict

api = Blueprint('api', __name__, url_prefix='/api')

@api.record
def record_params(setup_state):
    app = setup_state.app
    api.test_lists_dir = app.config.get('TEST_LISTS_REPO')

@api.route('/country/<country_code>', methods=["GET"])
def list_country_list(country_code):
    country_code = country_code.lower()
    if not re.match("^[a-z]{2}$", country_code):
        return jsonify({'error': 'Invalid country code'}), 400
    test_list = os.path.join(api.test_lists_dir,
                             "lists",
                             "{}.csv".format(country_code))
    if not os.path.exists(test_list):
        return jsonify({'error': 'Could not find test list for '
                                 'country {}'.format(country_code)}), 404

    filter_by = {}
    for key in ('category_code', 'source'):
        filter_by[key] = request.args.get(key)
    items = csv_to_dict(test_list, filter_by=filter_by)
    return jsonify(items=items), 200

