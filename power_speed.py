"""
This module Creates Figure 1
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    plt.rcParams.update({'figure.autolayout': True, 'font.size': 14, })
    plt.rcParams["font.family"] = "Helvetica"
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

    df = pd.read_csv("data/energy_summary.csv")
    sns.boxplot(x='speed', y='Power_cruise', data=df, color="magenta")
    plt.grid(which="major",alpha=0.2)
    plt.ylabel("Average power \nduring cruise [Wh]", fontsize=14)
    plt.xlabel("Speed [m/s]", fontsize=14)
    plt.ylim(0,650)
    sns.despine(top=True, right=True)
    plt.savefig('results/figure1.pdf', dpi=500)
    plt.show()


if __name__=="__main__":
    main()
