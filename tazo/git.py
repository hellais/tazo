import subprocess

class Git(object):
    def __init__(self, repo_directory):
        self.repo_directory = repo_directory

    def run(self, args):
        command = ['git'] + args
        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=self.repo_directory)
        stdout, _ = proc.communicate()
        return stdout

    def checkout(self, args=[]):
        return self.run(["checkout"] + args)

    def commit(self, args=[]):
        return self.run(["commit"] + args)

    def add(self, args=[]):
        return self.run(["add"] + args)

    def push(self, args=[]):
        return self.run(["push"] + args)

    def pull(self, args=[]):
        return self.run(["pull"] + args)

    def list_untracked(self):
        stdout = self.run(["status", "-u", "-z"])
        untracked = map(lambda x: x.replace("?? ", ""),
                        stdout.split("\0")[:-1])
        print untracked
        return untracked

    def status(self, args=[]):
        return self.run(["status"])
