from pydriller import RepositoryMining
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.hunks_count import HunksCount
import csv

class GeradorCSV(object):

    def limpa(self, texto):
        aux = texto
        aux2 = aux.replace('{', '')
        aux3 = aux2.replace('}', '')
        aux4 = aux3.replace('\'', '')
        aux5 = aux4.replace(':', '')
        aux6 = aux5.replace(',', '').strip()
        aux7 = aux6.split()

        return aux7


def gera_csv(texto, metrica):
    saida = metrica
    ger = GeradorCSV()
    aux = ger.limpa(texto)
    numeros = aux[1::2]
    palavras = aux[::2]
    dir = '../CSVs/teste'
    with open(dir + saida, 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['filePath', 'total'])
        for i in range(len(numeros) and len(palavras)):
            thewriter.writerow(['{}'.format(palavras[i]), '{}'.format(numeros[i])])

# Url do repositorio a ser analisado e arquivo de saida .csv
name = 'azure-cosmos-java-getting-started'
url = '../Repos/' + name

# Obter hash dos commits inicial e final.
vet = []
for commit in RepositoryMining(url).traverse_commits():
    vet.append(commit.hash)
x = len(vet)
inicio = vet[0]
# print(inicio)
fim = vet[x - 1]
# print(fim)
'''
#Traverse commits
for commit in RepositoryMining(url).traverse_commits():
    print(
        'The commit {} has been modified by {}, '
        'committed by {} in date {}'.format(
            commit.hash,
            commit.author.name,
            commit.committer.name,
            commit.committer_date
        )
    )
'''

# CommitsCount
metric = CommitsCount(path_to_repo=url, from_commit=inicio, to_commit=fim)
files = metric.count()
text = '{}'.format(files)  # Commits Count files
ger = GeradorCSV()
auxCoC = ger.limpa(text)
palCoC = auxCoC[::2]
numCoC = auxCoC[1::2]
with open('../CSVs/ProcessMetrics/teste', 'w', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['filePath', 'commitsCount'])
    for i in range(len(numCoC) and len(palCoC)):
        thewriter.writerow(['{}'.format(palCoC[i]), '{}'.format(numCoC[i])])
