from pydriller import RepositoryMining
from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount
import csv
import os.path

# aux = open('../List-Of-Samples/azuresamples.txt', 'r')
aux = open('../List-Of-Samples/awssamples.txt', 'r')
list_repos = aux.readlines()


# Path of repository
# name = 'azure-cosmos-java-sql-api-todo-app'
# path = '../Repos/' + name


def getHash(path, num):  # if num = 0 return init and if num != 0 return end.
    vet = []
    for commit in RepositoryMining(path).traverse_commits():
        vet.append(commit.hash)
    x = len(vet)
    if num == 0:
        return vet[0]
    return vet[x - 1]


def limpa(text, num):
    aux1 = text
    aux2 = aux1.replace('{', '')
    aux3 = aux2.replace('}', '')
    aux4 = aux3.replace('\'', '')
    aux5 = aux4.replace(':', '')
    aux6 = aux5.replace(',', '').strip()
    aux7 = aux6.split()
    if num == 0:
        return aux7[::2]
    return aux7[1::2]


def geraCSV(url, repository, initial, final):
    path = '../CSVs/ProcessMetrics/' + repository
    if path == '../CSVs/ProcessMetrics/':
        exit()
    if not os.path.isfile(path):
        print(path + ".csv")
        with open('../CSVs/ProcessMetrics/' + repository, 'w', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(
                ['filePath', 'maxChangeSet', 'avgChangeSet', 'totalCodeChurn', 'maxCodeChurn', 'avgCodeChurn',
                 'commitCount', 'hunksCount','lines_added_count', 'lines_added_avg',
                 'lines_added_max', 'lines_removed_count',
                 'lines_removed_avg', 'lines_removed_max']
            )
            # ChangeSet
            metric = ChangeSet(path_to_repo=url, from_commit=initial, to_commit=final)
            maximum = metric.max()
            average = metric.avg()

            # CodeChurn
            metric = CodeChurn(path_to_repo=url, from_commit=initial, to_commit=final)
            files_count = metric.count()
            files_max = metric.max()
            files_avg = metric.avg()

            diretory = limpa("{}".format(files_count), 0)  # names of archives

            files_count = limpa("{}".format(files_count), 1)
            files_max = limpa("{}".format(files_max), 1)
            files_avg = limpa("{}".format(files_avg), 1)

            # CommitsCount
            metric = CommitsCount(path_to_repo=url, from_commit=initial, to_commit=final)
            commitCount = metric.count()
            commitCount = limpa("{}".format(commitCount), 1)

            # ContributorsCount
            metric = ContributorsCount(path_to_repo=url, from_commit=initial, to_commit=final)
            count = metric.count()
            minor = metric.count_minor()
            count = limpa("{}".format(count), 1)
            minor = limpa("{}".format(minor), 1)

            # ContributorsExperience
            metric = ContributorsExperience(path_to_repo=url, from_commit=initial, to_commit=final)
            exp = metric.count()
            exp = limpa("{}".format(exp), 1)

            # HunksCount
            metric = HunksCount(path_to_repo=url, from_commit=initial, to_commit=final)
            hunks = metric.count()
            hunks = limpa("{}".format(hunks), 1)

            # LinesCount
            metric = LinesCount(path_to_repo=url, from_commit=initial, to_commit=final)
            # Line Added
            added_count = metric.count_added()
            added_max = metric.max_added()
            added_avg = metric.avg_added()

            added_count = limpa("{}".format(added_count), 1)
            added_max = limpa("{}".format(added_max), 1)
            added_avg = limpa("{}".format(added_avg), 1)

            # Line Removed
            removed_count = metric.count_removed()
            removed_max = metric.max_removed()
            removed_avg = metric.avg_removed()

            removed_count = limpa("{}".format(removed_count), 1)
            removed_max = limpa("{}".format(removed_max), 1)
            removed_avg = limpa("{}".format(removed_avg), 1)

            n = len(diretory)
            """
            print(len(diretory), "max:{}".format(maximum), "avg:{}".format(average), len(files_count), len(files_max),
                  len(files_avg), len(commitCount), len(count), len(minor), len(exp),
                  len(hunks), len(added_count), len(added_avg), len(added_max),
                  len(removed_count), len(removed_avg), len(removed_max))
            """
            for i in range(len(diretory)):
                thewriter.writerow(
                    [diretory[i], maximum, average, files_count[i], files_max[i],
                     files_avg[i], commitCount[i], hunks[i], added_count[i],
                     added_avg[i], added_max[i], removed_count[i], removed_avg[i], removed_max[i]]
                )


for repo in list_repos:
    repo = repo.rstrip('\n')
    urlweb = 'https://github.com/' + repo + '.git'
    print("Analyzing: " + urlweb)
    init = (getHash(urlweb, 0))
    end = (getHash(urlweb, 1))
    if not os.path.isfile('../CSVs/ProcessMetrics/' + repo):
        geraCSV(urlweb, repo, init, end)

aux.close()
