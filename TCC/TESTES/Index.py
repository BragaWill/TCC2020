from pydriller import RepositoryMining
from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount
import csv

# Url of repository
name = 'azure-cosmos-java-getting-started'
url = '../Repos/' + name


class GeradorCSV(object):

    def limpa(self, text):
        aux = text
        aux2 = aux.replace('{', '')
        aux3 = aux2.replace('}', '')
        aux4 = aux3.replace('\'', '')
        aux5 = aux4.replace(':', '')
        aux6 = aux5.replace(',', '').strip()
        aux7 = aux6.split()
        return aux7


# Initial and final commits hash.
vet = []
for commit in RepositoryMining(url).traverse_commits():
    vet.append(commit.hash)
x = len(vet)
inicio = vet[0]
fim = vet[x - 1]

# ChangeSet
metric = ChangeSet(path_to_repo=url, from_commit=inicio, to_commit=fim)
maximum = metric.max()
average = metric.avg()

# CodeChurn
metric = CodeChurn(path_to_repo=url, from_commit=inicio, to_commit=fim)
files_count = metric.count()
files_max = metric.max()
files_avg = metric.avg()
ger = GeradorCSV()
total = ger.limpa('{}'.format(files_count))
num = total[1::2]
pal = total[::2]
maxi = ger.limpa('{}'.format(files_max))
num1 = maxi[1::2]
avg = ger.limpa('{}'.format(files_avg))
num2 = avg[1::2]

# ContributorsCount
metric = ContributorsCount(path_to_repo=url, from_commit=inicio, to_commit=fim)
count = metric.count()
minor = metric.count_minor()
ger = GeradorCSV()
cont = ger.limpa('{}'.format(count))  # Number of contributors per file
numCC = cont[1::2]
minor = ger.limpa('{}'.format(minor))  # Number of "minor" contributors per file
num1CC = minor[1::2]

# Lines Count
metric = LinesCount(path_to_repo=url, from_commit=inicio, to_commit=fim)
# Added
added_count = metric.count_added()
added_max = metric.max_added()
added_avg = metric.avg_added()
# Removed
removed_count = metric.count_removed()
removed_max = metric.max_removed()
removed_avg = metric.avg_removed()
ger = GeradorCSV()

addc = ger.limpa('{}'.format(added_count))
numLC = addc[1::2]
addm = ger.limpa('{}'.format(added_max))
num1LC = addm[1::2]
adda = ger.limpa('{}'.format(added_avg))
num2LC = adda[1::2]
remc = ger.limpa('{}'.format(removed_count))
num3LC = remc[1::2]
remm = ger.limpa('{}'.format(removed_max))
num4LC = remm[1::2]
rema = ger.limpa('{}'.format(removed_avg))
num5LC = rema[1::2]

# HunksCount
metric = HunksCount(path_to_repo=url, from_commit=inicio, to_commit=fim)
files = metric.count()
text = '{}'.format(files)  # Hunks Count files
ger = GeradorCSV()
auxHC = ger.limpa(text)
numHC = auxHC[1::2]

# ContributorsExperience
metric = ContributorsExperience(path_to_repo=url, from_commit=inicio, to_commit=fim)
files = metric.count()
text = '{}'.format(files)  # Contributors Experience files
ger = GeradorCSV()
auxCE = ger.limpa(text)
numCE = auxCE[1::2]

# CommitsCount
metric = CommitsCount(path_to_repo=url, from_commit=inicio, to_commit=fim)
files = metric.count()
text = '{}'.format(files)  # Commits Count files
ger = GeradorCSV()
auxCoC = ger.limpa(text)
numCoC = auxCoC[1::2]

# Make the document CSV with process metrics
with open('../CSVs/ProcessMetrics/metrics', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(
        ['filePath', 'filesCount', 'filesMax', 'filesAvg', 'maxChanges', 'avgChanges', 'countContributors',
         'minorContributors', 'countAdded', 'maxAdded', 'avgAdded', 'countRem', 'maxRem', 'avgRem', 'hunksCount',
         'contributorsExperience', 'commitsCount'])
    for i in range(len(num) and len(pal)):
        thewriter.writerow(
            ['{}'.format(pal[i]), '{}'.format(num[i]), '{}'.format(num1[i]), '{}'.format(num2[i]), '{}'.format(maximum),
             '{}'.format(average), '{}'.format(numCC[i]), '{}'.format(num1CC[i]), '{},'.format(numLC[i]),
             '{}'.format(num1LC[i]), '{}'.format(num2LC[i]), '{}'.format(num3LC[i]), '{}'.format(num4LC[i]),
             '{}'.format(num5LC[i]), '{}'.format(numHC[i]), '{}'.format(numCE[i]), '{}'.format(numCoC[i])])
