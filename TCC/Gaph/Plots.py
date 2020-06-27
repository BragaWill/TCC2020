import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

# import statistics

metrica_1 = []
metrica_2 = []

framework1 = pd.read_csv("../CSVs/ProcessMetrics/AWS/active-directory-android-native-oidcandroidlib-v2.csv")
framework2 = pd.read_csv("../CSVs/ProcessMetrics/AZURE/aci-java-create-container-groups.csv")

t1 = framework1.lines_added_avg
t2 = framework2.lines_added_avg

metrica_1 = t1.values
metrica_2 = t2.values

metrica_1 = np.array(metrica_1, dtype=float)
metrica_2 = np.array(metrica_2, dtype=float)


def drawViolinPlot(axis, xlabel, xticks, xticklabels, ylabel, bandwidth, title):
    axis.set_xlabel(xlabel)
    axis.set_xticks(xticks)
    axis.set_xticklabels(xticklabels)

    axis.set_ylabel(ylabel)

    axis.violinplot(sequences, showmeans=True, showmedians=True, bw_method=bandwidth)
    axis.set_title(title)


sequences = (metrica_1, metrica_2)

figure, axis = plot.subplots(1)
plot.subplots_adjust(hspace=0.4)

bandwidth = None
drawViolinPlot(axis,
               "Samples",
               np.arange(len(sequences) + 1),
               ('', 'AWS', 'Azure'),
               "AVG Lines Count", bandwidth,
               "Violin Plot")

plot.text(1, me)
plot.yscale('log')
plot.savefig('grafico.png')
