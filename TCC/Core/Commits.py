from pydriller import RepositoryMining
from git import Repo
import os.path
import csv

aux = open('../List-Of-Samples/awssamples.txt', 'r')
list_repos = aux.readlines()


def gerarCsv(urlweb, repo):
    path = '../CSVs/Commits/' + repo
    if path == '../CSVs/Commits/':
        exit()
    if os.path.isfile(path):
        print(path + ".csv")
    elif not os.path.isfile(path):
        print(path + ".csv")
        with open('../CSVs/Commits/' + repo, 'w', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(
                ['hash', 'author_date', 'author_timezone', 'committer_date', 'committer_timezone',
                 'in_main_branch', 'merge', 'project_name', 'dmm_unit_size', 'dmm_unit_complexity',
                 'dmm_unit_interfacing', 'old_path', 'new_path', 'filename', 'change_type', 'added',
                 'removed', 'nloc', 'complexity', 'token_count'])
            for commit in RepositoryMining(urlweb, only_modifications_with_file_types=['.java']).traverse_commits():
                for m in commit.modifications:
                    thewriter.writerow(
                        ["{}".format(commit.hash),
                         "{}".format(commit.author_date),
                         "{}".format(commit.author_timezone),
                         "{}".format(commit.committer_date),
                         "{}".format(commit.committer_timezone),
                         "{}".format(commit.in_main_branch),
                         "{}".format(commit.merge),
                         "{}".format(commit.project_name),
                         "{}".format(commit.dmm_unit_size),
                         "{}".format(commit.dmm_unit_complexity),
                         "{}".format(commit.dmm_unit_interfacing),
                         "{}".format(m.old_path),
                         "{}".format(m.new_path),
                         "{}".format(m.filename),
                         "{}".format(m.change_type),
                         "{}".format(m.added),
                         "{}".format(m.removed),
                         "{}".format(m.nloc),
                         "{}".format(m.complexity),
                         "{}".format(m.token_count)])


for repo in list_repos:
    repo = repo.rstrip('\n')
    path = '../Repositories/' + repo
    urlweb = 'https://github.com/' + repo + '.git'
    if not os.path.exists(path):
        print("cloning..." + path)
        Repo.clone_from(urlweb, path)
        gerarCsv(urlweb, repo)
    else:
        gerarCsv(urlweb, repo)

aux.close()
