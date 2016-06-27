import os
import csv
from datetime import datetime

from github import Github
from .git import Git
from .config import category_codes, country_codes, TEST_LISTS_REPO
from .app import create_celery

from celery import current_app

celery = create_celery()

def append_url_to_csv(country_code, url, category_code, source, notes):
    # url,category_code,category_description,date_added,source,notes
    target_file = os.path.join(
        TEST_LISTS_REPO,
        "lists",
        "{0}.csv".format(country_code)
    )
    header = None
    if not os.path.exists(target_file):
        header = ["url", "category_code", "category_description", "date_added",
                  "source", "notes"]
    with open(target_file, 'a') as f:
        csv_writer = csv.writer(f, dialect='excel')
        if header is not None:
            csv_writer.writerow(header)
        csv_writer.writerow([
            url,
            category_code,
            category_codes[category_code][0],
            datetime.now().strftime("%Y-%m-%d"),
            source,
            notes
        ])


@celery.task
def submit_urls(urls, contributor):
    celery_app = current_app._get_current_object()

    assert celery_app.conf.GITHUB_USERNAME is not None
    assert celery_app.conf.GITHUB_PASSWORD is not None

    github = Github(celery_app.conf.GITHUB_USERNAME,
                    celery_app.conf.GITHUB_PASSWORD)
    git = Git(TEST_LISTS_REPO)
    git.pull(["-u", celery_app.conf.TARGET_REPO.split("/")[0], "master"])
    branch_name = ("user-contribution/{0}".format(
        datetime.now().strftime("%Y%m%dT%H%M%S")
    ))
    git.checkout(["-b", branch_name])
    try:
        country_names = set()
        for url in urls:
            country_code = url['country'].upper()
            if (country_code not in country_codes.keys() and
                    country_code != "GLOBAL"):
                raise Exception("Invalid country code '{0}'".format(country_code))
            if country_code == "GLOBAL":
                country_names.add("Global")
            else:
                country_names.add(country_codes[country_code])
            append_url_to_csv(
                country_code=url['country'].lower(),
                url=url['url'],
                category_code=url['category'],
                source=contributor,
                notes=url['notes']
            )
        for untracked_file in git.list_untracked():
            git.add([untracked_file])
        commit_title = "Add user contributed URLs for countries {0}".format(
            ' '.join(list(country_names))
        )
        commit_msg = "This Pull Request was automatically generated from the web"
        git.add(["."])
        git.commit([
            "-m",
            commit_title
        ])
        git.push(["-u", "origin", branch_name])
        repo = github.get_repo(celery_app.conf.TARGET_REPO)
        head = "{0}:{1}".format(celery_app.conf.GITHUB_USERNAME, branch_name)
        print "Repo %s" % celery_app.conf.TARGET_REPO
        print "Head %s" % head
        repo.create_pull(commit_title, commit_msg,
                         head=head,
                         base="master")
    finally:
        git.checkout(["master"])
