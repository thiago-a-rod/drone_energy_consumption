"""
This module performs the linear regression used in the main energy model.
"""

import pandas as pd
import numpy as np
import LinearRegression as lr
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter


def calculate_coefficients(summary, sample):
    summary.payload = summary.payload.astype(int)
    summary_sample = summary[summary.flight.isin(sample.flight)].copy()
    coeff = lr.linear_regression(summary_sample, 'mass_rho')
    b1_error, b0_error = bootstrap_standard_error(summary, sample)
    coeff['b1_error'] = b1_error
    coeff['b0_error'] = b0_error
    coeff.to_csv('data/coefficients.csv')
    coeff.to_csv('results/table1.csv')
    print(coeff)



def bootstrap_standard_error(summary, sample):
    tk_b1 = []
    tk_b0 = []
    cr_b1 = []
    cr_b0 = []
    ld_b1 = []
    ld_b0 = []
    n = 1000
    for i in range(n):
        print("iteration: %d" % (i), end='\r')
        subsample = np.random.choice(sample.flight, size=120, replace=True)
        summary.payload = summary.payload.astype(int)
        summary_sample = summary[summary.flight.isin(subsample)].copy()

        coeff = lr.linear_regression(summary_sample, "mass_rho")
        tk_b1.append(coeff.loc['takeoff', 'b1'])
        tk_b0.append(coeff.loc['takeoff', 'b0'])
        cr_b1.append(coeff.loc['cruise', 'b1'])
        cr_b0.append(coeff.loc['cruise', 'b0'])
        ld_b1.append(coeff.loc['landing', 'b1'])
        ld_b0.append(coeff.loc['landing', 'b0'])

    b1_error = [np.std(tk_b1), np.std(cr_b1), np.std(ld_b1)]
    b0_error = [np.std(tk_b0), np.std(cr_b0), np.std(ld_b0)]

    return b1_error, b0_error

def rl(regime,df,coeff):
    return [coeff.loc[regime,'b1']*df.Pi_hover.min() + coeff.loc[regime,'b0'],
            coeff.loc[regime,'b1']*df.Pi_hover.max() + coeff.loc[regime,'b0']]

def figure7(summary, sample):
    plt.rcParams.update({'figure.autolayout': True})
    plt.rcParams["font.family"] = "Helvetica"
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    plt.rcParams['legend.title_fontsize'] = 'large'
    summary.payload = summary.payload.astype(int)
    summary_sample = summary[summary.flight.isin(sample.flight)].copy()
    coeff = lr.linear_regression(summary_sample, 'Pi_hover')

    df = summary.copy()
    fig, ax = plt.subplots()
    ax.scatter(x=df['Pi_hover'], y=df['Power_takeoff'], label='Takeoff', alpha=0.5, color='blue')
    ax.scatter(x=df['Pi_hover'], y=df['Power_cruise'], label='Cruise', alpha=0.5, color='red')
    ax.scatter(x=df['Pi_hover'], y=df['Power_landing'], label='Landing', alpha=0.5, color='orange')
    interval = [260, 330]
    ax.plot(interval, rl('takeoff', df, coeff), linestyle='--', color='black', alpha=0.7)
    ax.plot(interval, rl('cruise', df, coeff), linestyle='--', color='black', alpha=0.7)
    ax.plot(interval, rl('landing', df, coeff), linestyle='--', color='black', alpha=0.7)

    plt.legend(title='Flight regime', frameon=False, loc="lower center", fontsize='large', ncol=3)
    plt.ylim(0, 750)
    # plt.xlim(interval)
    # plt.xlabel(r"$\dfrac{mass^{1.5}}{\sqrt{\rho}}$ [$kg \cdot m^{1.5}$]", fontsize=20)
    plt.xlabel(r"Induced Power [W]", fontsize=20)
    plt.ylabel("Average Power [W]", fontsize=20)
    plt.xticks(fontsize=16)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plt.yticks(fontsize=16)
    sns.despine(top=True, right=True)
    plt.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    plt.savefig('results/figure7.pdf')
    plt.show()


def main():
    summary = pd.read_csv('data/energy_summary.csv')
    sample = pd.read_csv('data/sample.csv')  # List of the 120 randomly selected flights used in the paper
    calculate_coefficients(summary, sample)
    figure7(summary, sample)



if __name__=="__main__":
    main()
