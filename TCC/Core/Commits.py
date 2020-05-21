from pydriller import RepositoryMining
from git import Repo
import os.path
import csv

aux = open('../List-Of-Samples/azuresamples.txt', 'r')
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
                ['commit_hash', 'filename', 'old_path', 'new_path', 'change_type', 'added', 'removed', 'nloc',
                 'complexity',
                 'token_count',
                 'commiter_date', 'dmm_unit_size', 'dmm_unit_complexity', 'dmm_unit_interfacing'])
            for commit in RepositoryMining(urlweb).traverse_commits():
                for m in commit.modifications:
                    thewriter.writerow(
                        ["{}".format(commit.hash), "{}".format(m.filename), "{}".format(m.old_path), "{}".format(m.new_path),
                         "{}".format(m.change_type.name), "{}".format(m.nloc), "{}".format(m.added), "{}".format(m.removed),
                         "{}".format(m.token_count), "{}".format(m.complexity), "{}".format(commit.committer_date),
                         "{}".format(commit.dmm_unit_size), "{}".format(commit.dmm_unit_complexity),
                         "{}".format(commit.dmm_unit_interfacing)])


for repo in list_repos:
    repo = repo.rstrip('\n')
    path = '../Repositories/' + repo
    urlweb = 'https://github.com/' + repo + '.git'
    if not os.path.exists(path):
        print("cloning..."+path)
        Repo.clone_from(urlweb, path)
        gerarCsv(urlweb, repo)
    else:
        gerarCsv(urlweb, repo)


aux.close()

"""
print("commit_hash, filename, old_path, new_path, change_type, added, removed, nloc, complexity, token_count, "
      "commiter_date, dmm_unit_size, dmm_unit_complexity,dmm_unit_interfacing")
for commit in RepositoryMining(urlweb).traverse_commits():
    for m in commit.modifications:
        # and n in commit.traverse_commits():
        print(
            "{},".format(commit.hash),
            "{},".format(m.filename),
            "{},".format(m.old_path),
            "{},".format(m.new_path),
            "{},".format(m.change_type.name),
            "{},".format(m.nloc),
            "{},".format(m.added),
            "{},".format(m.removed),
            "{},".format(m.token_count),
            "{},".format(m.complexity),
            "{},".format(commit.committer_date),
            "{},".format(commit.dmm_unit_size),
            "{},".format(commit.dmm_unit_complexity),
            "{}".format(commit.dmm_unit_interfacing)
        )
"""
