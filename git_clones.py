#! /usr/bin/python3.7
# rootVIII
# Download/clone all of a user's public repositories
# Pass a the Github user's username with the -u option
# Usage: python git_clones.py -u <github username>
# Example: python git_clones.py -u rootVIII
#
from argparse import ArgumentParser
from sys import exit
from re import findall
from urllib.request import urlopen
from subprocess import call, PIPE


class GitClones:
    def __init__(self, user):
        self.url = "https://github.com/%s?tab=repositories" % user
        self.git_clone = "git clone https://github.com/%s/%s.git"
        self.user = user
        self.repos = []
        self.page = ''

    def get_repositories(self):
        try:
            r = urlopen(self.url)
        except Exception:
            print("Unable to make request to %s's Github page" % self.user)
            exit(1)
        else:
            self.page = r.read().decode('utf-8')
        pattern = r"repository_nwo:%s/(.*)," % self.user
        for line in findall(pattern, self.page):
            yield line.split(',')[0]

    def get_names(self):
        self.repos = [r for r in self.get_repositories()]
        return set(self.repos)

    def download(self, git_repos):
        for git in git_repos:
            cmd = self.git_clone % (self.user, git)
            try:
                call(cmd.split(), stdout=PIPE)
            except Exception as e:
                print(e)
                print('unable to download:%s\n ' % git)


if __name__ == "__main__":
    message = 'Usage: python git_clones.py -u <github username>'
    h = 'Github Username'
    parser = ArgumentParser(description=message)
    parser.add_argument('-u', '--user', required=True, help=h)
    d = parser.parse_args()
    clones = GitClones(d.user)
    repositories = clones.get_names()
    clones.download(repositories)