from flask.ext.script import Manager

from tazo import app

manager = Manager(app)

@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()
