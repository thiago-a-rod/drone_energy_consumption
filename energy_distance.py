"""
This module creates Figure 2
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import ghg_emission as ghg


def energy_two_way(distance, coeff, payload=500, speed=12, altitude=100, rho=1.2):
    m = 3.08 + 0.635
    x_unload = ((m) ** (3 / 2)) / np.sqrt(rho)
    x_load = (((m + payload / 1000) ) ** (3 / 2)) / np.sqrt(rho)

    b1_tk = coeff.loc['takeoff', 'b1']
    b0_tk = coeff.loc['takeoff', 'b0']
    b1_cr = coeff.loc['cruise', 'b1']
    b0_cr = coeff.loc['cruise', 'b0']
    b1_ld = coeff.loc['landing', 'b1']
    b0_ld = coeff.loc['landing', 'b0']

    d = distance * 1000
    V = speed
    t = d/V
    takeoff_speed = 2.5
    landing_speed = 2.0
    Energy_tk1 = (x_load * b1_tk + b0_tk) * (altitude/takeoff_speed) / 3600 # Wh
    Energy_cr1 = (x_load * b1_cr + b0_cr) * t / 3600
    Energy_ld1 = (x_load * b1_ld + b0_ld) * (altitude/landing_speed) / 3600 # Wh
    Energy_tk2 = (x_unload * b1_tk + b0_tk) * (altitude/takeoff_speed) / 3600
    Energy_cr2 = (x_unload * b1_cr + b0_cr) * t / 3600
    Energy_ld2 = (x_unload * b1_ld + b0_ld) * (altitude/landing_speed) / 3600

    Total_Energy = Energy_tk1 + Energy_cr1 + Energy_ld1 + Energy_tk2 + Energy_cr2 + Energy_ld2
    return Total_Energy


def figure2():
    plt.rcParams.update({'figure.autolayout': True})
    plt.rcParams["font.family"] = "Helvetica"
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})

    coeff = pd.read_csv('data/coefficients.csv', index_col=0)

    distance = np.arange(0, 8.5, 0.01)
    e_500 = [energy_two_way(d, coeff, payload=500, speed=12) for d in distance]
    e_0 = [energy_two_way(d, coeff, payload=0, speed=12) for d in distance]
    e_500_4 = [energy_two_way(d, coeff, payload=500, speed=4) for d in distance]
    e_0_4 = [energy_two_way(d, coeff, payload=0, speed=4) for d in distance]

    df_dist = pd.DataFrame(
        {"d": distance, "e_500": e_500, "e_0": e_0, "e_500_4": e_500_4,
         "e_0_4": e_0_4})
    df_dist[df_dist > 129.96] = None
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,6))

    ax1.plot(df_dist.d, df_dist.e_500_4, color='red')
    ax1.plot(df_dist.d, df_dist.e_500, color='blue')

    ax1.plot(df_dist.d, df_dist.e_0, color='blue')
    ax1.plot(df_dist.d, df_dist.e_0_4, color='red')
    ax1.set_ylim(0, 145)
    xlim_max = 5
    ax1.set_xlim(0, xlim_max)
    label_format = "{:.1f}"
    ticks_loc = ax1.get_xticks().tolist()
    ax1.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax1.set_xticklabels([label_format.format(x) for x in ticks_loc], fontsize=16)
    ticks_loc = ax1.get_yticks().tolist()
    ax1.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax1.set_yticklabels([label_format.format(x) for x in ticks_loc], fontsize=16)

    ax1.axhline(129.96, xmin=0, xmax=xlim_max, color='gray', linestyle=(0, (3, 5, 1, 5)), alpha=0.5)

    sns.despine(top=True, right=True)
    ax1.set_xlabel('Delivery Distance [km]\n(a)', fontsize=18)
    ax1.set_ylabel('Total Energy Consumption \ntwo-way delivery [Wh/package]', fontsize=18)
    ax1.text(2.0, 131, 'LiPo Battery Capacity', color="black", fontsize=14)
    ax1.text(2.7, 95, '500 g', rotation=28, fontsize=12, color="gray")
    ax1.text(3.5, 95, 'No payload', rotation=22, fontsize=12, color="gray")
    ax1.text(0.8, 95, '500 g', rotation=60, fontsize=12, color="gray")
    ax1.text(1.2, 95, 'No payload', rotation=54., fontsize=12, color="gray")
    ax1.legend(['4 m/s', "12 m/s"], title='Cruise speed', fontsize=14, frameon=False).get_title().set_fontsize(14)
    ax1.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)

    distance = np.arange(0, 8.5, 0.01)
    e_500 = [energy_two_way(d, coeff, payload=500, speed=12) for d in distance]
    df_dist = pd.DataFrame({"d": distance, "e_500": e_500})

    print(df_dist.e_500.max())
    df_dist = df_dist[df_dist.e_500 < 129.96].copy()
    df_dist['e_500'] = df_dist.e_500*0.0036  # Converting Wh to MJ

    ghg_base, ghg_low, ghg_high = [], [], []

    electric_losses = 0.88 * (1 - 6.5 / 100)
    for i in range(len(df_dist)):
        a, b, c = ghg.drone_ghg_emissions(df_dist.loc[i, 'e_500'], df_dist.loc[i, 'd'], electric_losses)
        ghg_base.append(a)
        ghg_low.append(b)
        ghg_high.append(c)

    df_dist['ghg'] = ghg_base
    df_dist['ghg_low'] = ghg_low
    df_dist['ghg_high'] = ghg_high

    ax2.plot(df_dist.d, df_dist.ghg, color='blue')
    ax2.fill_between(df_dist.d, df_dist.ghg_low, df_dist.ghg_high, color='gray', alpha=0.5)
    # ax2.scatter(2, df_dist.loc[df_dist.d==2,'ghg'], c='black', s=30)
    # ax2.vlines(2, df_dist.loc[df_dist.d==2,'ghg_low'],df_dist.loc[df_dist.d==2,'ghg_high'], colors='red', linestyles='--')
    # ax2.text(2-0.05, df_dist.loc[df_dist.d==2,'ghg_high'] + 3.8, 'base case', size=14, rotation=90)
    xlim_max = 4.3
    ax2.set_xlim(0, xlim_max)

    #ax2.set_xticklabels(ax2.get_xticks(), fontsize=16)
    #ax2.set_yticklabels(ax2.get_xticks(), fontsize=16)

    ticks_loc = ax2.get_xticks().tolist()
    ax2.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax2.set_xticklabels([label_format.format(x) for x in ticks_loc], fontsize=16)
    ticks_loc = ax2.get_yticks().tolist()
    ax2.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax2.set_yticklabels([label_format.format(x) for x in ticks_loc], fontsize=16)

    sns.despine(top=True, right=True)
    ax2.set_xlabel('Delivery Distance [km]\n(b)', fontsize=18)
    ax2.set_ylabel('$CO_{2}e$ emissions \ntwo-way delivery [g/package]', fontsize=18)
    plt.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    plt.savefig("results/figure2.pdf")
    plt.show()



def main():
    figure2()


if __name__=="__main__":
    main()