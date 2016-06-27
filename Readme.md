This is a web interface to contribute test-lists to the citizen-lab test-lists
repository.

It works by exposing a web interface that automatically creates pull requests
on github with the added URLs.

## Deploying

Install the depedencies with (tested on ubuntu trusty with universe):

```
apt-get update
apt-get install -y git redis-server python-setuptools python-dev python-pip build-essential
pip install -r requirements.txt
```

Make sure that git is configured properly. That is you are able to push to the
origin repository via ssh and that the `--global user.*` options are set 
properly like so:

```
git config --global user.name "OONI Bot"
git config --global user.email "ooni-bot@openobservatory.org"
```

Populate the instance directory with the appropriate files:

```
mkdir /tmp/instance/
git clone git@github.com:ooni-bot/test-lists.git /tmp/instance/test-lists
cd /tmp/instance/test-lists
git remote add hellais https://github.com/hellais/test-lists.git
git remote add citizenlab https://github.com/citizenlab/test-lists.git
echo 'GITHUB_USERNAME = "ooni-bot"' >> /tmp/instance/production.cfg
echo 'GITHUB_PASSWORD = "changeme"' >> /tmp/instance/production.cfg
```

Then to run you first need to start the celery worker with:

```
celery -A tazo.tasks worker -Q git -c 1
```

Then you can start the web interface with:

```
python manage run
```

It will bind on port 5000.
