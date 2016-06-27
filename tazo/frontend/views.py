import re
import os

from flask import Blueprint
from flask import render_template
from .forms import NewURLForm, CategorizeURLSForm, URLForm
from ..config import category_codes, country_codes
from ..testlists import csv_to_dict

frontend = Blueprint('frontend', __name__)

@frontend.record
def record_params(setup_state):
    app = setup_state.app
    frontend.test_lists_dir = app.config.get('TEST_LISTS_REPO')
    frontend.target_repo = app.config.get('TARGET_REPO')

@frontend.route('/', methods=["GET"])
def select_country():
    return render_template('frontend/home.html',
                           countries=country_codes.items())

@frontend.route('/country/<country_code>', methods=["GET", "POST"])
def show_country(country_code):
    country_code = country_code.lower()
    if not re.match("^[a-z]{2}$", country_code) and \
            not country_code == "global":
        return render_template('frontend/error.html',
                               message="invalid country code")

    new_urls = NewURLForm()
    if new_urls.validate_on_submit():
        # XXX verify if the added URLs are already part of the test list of
        # the country in question.
        categorize_urls = CategorizeURLSForm()
        categorize_urls.contributor = new_urls.contributor.data
        categorize_urls.country.data = country_code
        for url in new_urls.urls.data.split("\n"):
            if url.strip() == "":
                continue
            elif url.startswith("#"):
                continue
            url_form = URLForm()
            url_form.url = url
            url_form.notes = ""
            categorize_urls.urls.append_entry(url_form)
        return render_template('frontend/categorize.html',
                               form=categorize_urls)

    test_list = os.path.join(frontend.test_lists_dir,
                             "lists",
                             "{0}.csv".format(country_code))
    items = {}
    if os.path.exists(test_list):
        items = csv_to_dict(test_list)

    return render_template('frontend/show_country.html',
                           existing_urls=items,
                           form=new_urls,
                           country_code=country_code)

@frontend.route('/add', methods=["POST"])
def add():
    from ..tasks import submit_urls

    categorize_urls = CategorizeURLSForm()
    new_urls = []
    for nu in categorize_urls.urls.data:
        nu["country"] = categorize_urls.country.data
        new_urls.append(nu)
    submit_urls.apply_async((new_urls, categorize_urls.contributor.data),
                            queue="git")
    return render_template('frontend/added.html',
                           new_urls=new_urls,
                           target_repo=frontend.target_repo)

