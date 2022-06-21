"""
This module creates figures 4 and 5.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'figure.autolayout': True, 'font.size': 14, })
plt.rcParams["font.family"] = "Helvetica"
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
import ghg_emission


def figure4(df):
    df1 = df.sort_values(by=['energy'], ascending=True).copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    color_others = "#9F9F9F"
    ax1.barh(df1['Vehicle Class'], df1.energy,
             color=["blue", color_others, color_others, color_others, color_others, color_others],
             xerr=np.array([df1.e_low, df1.e_high]), capsize=5)
    ax1.set_xticks(ax1.get_xticks(), fontsize=26)
    ax1.set_yticks(ax1.get_yticks(), fontsize=28)
    sns.despine(top=True, right=True)
    ax1.set_xlabel('Energy Consumption [MJ/km]\n(a)', fontsize=28)
    ax1.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    df1 = df.sort_values(by=['e_pack'], ascending=True).copy()

    ax2.barh(df1['Vehicle Class'], df1.e_pack,
             color=[color_others, "blue", color_others, color_others, color_others, color_others],
             xerr=np.array([df1.e_pack_high, df1.e_pack_low]), capsize=5)
    ax2.set_xticks(ax2.get_xticks(), fontsize=26)
    ax2.set_yticks(ax2.get_yticks(), fontsize=28)
    sns.despine(top=True, right=True)
    ax2.set_xlabel('Energy consumption [MJ/Package]\n(b)', fontsize=28)
    ax2.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    plt.savefig("results/figure4.pdf")


def figure5(df):
    df1 = df.sort_values(by=['ghg_km_fuel'], ascending=True).copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    ax1.barh(df1['Vehicle Class'], df1.ghg_km_upstream, color='gray', label='Upstream fuel')
    ax1.barh(df1['Vehicle Class'], df1.ghg_km_battery, color='orange', left=df1.ghg_km_upstream, label='Battery lifecycle')
    ax1.barh(df1['Vehicle Class'], df1.ghg_km_fuel, color='lightblue', left=df1.ghg_km_battery + df1.ghg_km_upstream,
             label='Fuel consumption', xerr=np.array([df1.ghg_error_low, df1.ghg_error_low]), capsize=5)
    ax1.legend(title='Emission source', frameon=False)

    ax1.set_xticks(ax1.get_xticks(), fontsize=26)
    ax1.set_yticks(ax1.get_yticks(), fontsize=28)
    sns.despine(top=True, right=True)
    ax1.set_xlabel('CO₂e emissions [g/km]\n(a)', fontsize=28)
    ax1.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)

    df1 = df.sort_values(by=['ghg_base_pack'], ascending=True).copy()


    ax2.barh(df1['Vehicle Class'], df1.ghg_upstream_pack, color='gray', label='Upstream fuel')
    ax2.barh(df1['Vehicle Class'], df1.ghg_battery_pack, color='orange', left=df1.ghg_upstream_pack, label='Battery lifecycle')
    ax2.barh(df1['Vehicle Class'], df1.ghg_fuel_pack, color='lightblue', left=df1.ghg_battery_pack + df1.ghg_upstream_pack,
             label='Fuel consumption', xerr=np.array([df1.ghg_error_low_pack, df1.ghg_error_high_pack]), capsize=5)
    ax2.legend(title='Emission source', frameon=False)

    ax2.set_xticks(ax2.get_xticks(),fontsize=26)
    ax2.set_yticks(ax2.get_yticks(), fontsize=28)
    sns.despine(top=True, right=True)
    ax2.set_xlabel('CO₂e emissions [g/package]\n(b)', fontsize=28)
    ax2.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    plt.savefig("results/figure5.pdf")
    plt.show()

def figureS1(df):
    df1 = df.sort_values(by=['tonkm'], ascending=True).copy()

    plt.figure(figsize=(14, 8))
    color_others = "#9F9F9F"

    plt.figure(figsize=(14, 6))

    plt.barh(df1['Vehicle Class'], df1.tonkm,
             color=[color_others, color_others, color_others, color_others, color_others, "blue"],
             xerr=np.array([0.2 * df1.tonkm, 0.2 * df1.tonkm]), capsize=5)

    plt.xticks(fontsize=26)
    plt.yticks(fontsize=28)
    sns.despine(top=True, right=True)
    plt.grid(which='major', axis='both', color='gray', linewidth=1.0, alpha=0.1)
    plt.xlabel('Energy consumption [MJ/ton-km]', fontsize=28)
    plt.savefig("results/figureS1.pdf")
    plt.show()


def main():
    df = pd.read_csv("results/table3.csv")
    print(df)

    df["energy"] = df['Energy Consumption [MJ/km]'].copy()
    df['e_high'] = df.energy * 0.2   # 40% energy consumption variation due tue driving styles
    df['e_low'] = df.energy * 0.2
    df.loc[5, ["e_high", "e_low"]] = 0

    stop_km = np.array([0.7, 1.74, 0.7, 1.74, 1, 0.25])
    pack_stop = np.array([3, 2, 3, 2, 1, 1])
    pack_km = pack_stop * stop_km
    pack_km_low = np.array([1.5, 1.5, 1.5, 1.5, 0.25, 0.125])
    pack_km_high = np.array([5, 5, 5, 5, 3, 0.5])

    df['e_pack'] = df.energy / pack_km
    df['e_pack_low'] = np.fabs(df.energy / pack_km_low - df.e_pack)
    df['e_pack_high'] = np.fabs(df.energy / pack_km_high - df.e_pack)

    ghg_fuel_low = np.array([69.5, 69.5, 111, 111, 111, 111])
    ghg_fuel_high = np.array([69.5, 69.5, 250, 250, 250, 250])

    df['ghg_km_fuel'] = df['Fuel GHG emissions [g/km]'].copy()
    df['ghg_km_upstream'] = df['Upstream GHG emissions [g/km]'].copy()
    df['ghg_km_battery'] = df['Battery GHG emissions [g/km]'].copy()
    electric_losses = 0.88 * (1 - 6.5 / 100)
    bat_drone = ghg_emission.Battery("Li-iron", None, 4562.04, 0.6, 129.96, df.loc[5,"energy"])
    bat_drone.cycles(300, 150, 1000)  # cycles (base, low, high) cases

    df['ghg_km_battery_high'] = np.array([0, 0, 24.5, 14.1, 1.3, bat_drone.ghg_km_high])
    df['ghg_km_battery_low'] = np.array([0, 0, 24.5, 14.1, 1.3, bat_drone.ghg_km_low])

    df["ghg_km_fuel_low"] = df.energy * ghg_fuel_low * (0.8)
    df["ghg_km_fuel_high"] = df.energy * ghg_fuel_high * (1.2)

    df['ghg_base'] = df.ghg_km_fuel + df.ghg_km_upstream + df.ghg_km_battery
    df['ghg_high'] = df.ghg_km_fuel_high + df.ghg_km_upstream + df.ghg_km_battery_high
    df['ghg_low'] = df.ghg_km_fuel_low + df.ghg_km_upstream + df.ghg_km_battery_low

    df['ghg_error_high'] = df.ghg_high - df.ghg_base
    df['ghg_error_low'] = df.ghg_base - df.ghg_low

    df['ghg_fuel_pack'] = df.ghg_km_fuel / pack_km
    df['ghg_upstream_pack'] = df.ghg_km_upstream / pack_km
    df['ghg_battery_pack'] = df.ghg_km_battery / pack_km

    df['ghg_fuel_pack_low'] = df.ghg_km_fuel / pack_km_low
    df['ghg_upstream_pack_low'] = df.ghg_km_upstream / pack_km_low
    df['ghg_battery_pack_low'] = df.ghg_km_battery / pack_km_low

    df['ghg_fuel_pack_high'] = df.ghg_km_fuel / pack_km_high
    df['ghg_upstream_pack_high'] = df.ghg_km_upstream / pack_km_high
    df['ghg_battery_pack_high'] = df.ghg_km_battery / pack_km_high

    df['ghg_base_pack'] = df.ghg_fuel_pack + df.ghg_upstream_pack + df.ghg_battery_pack
    df['ghg_high_pack'] = df.ghg_fuel_pack_high + df.ghg_upstream_pack_high + df.ghg_battery_pack_high
    df['ghg_low_pack'] = df.ghg_fuel_pack_low + df.ghg_upstream_pack_low + df.ghg_battery_pack_low

    df['ghg_error_high_pack'] = df.ghg_high_pack - df.ghg_base_pack
    df['ghg_error_low_pack'] = df.ghg_base_pack - df.ghg_low_pack

    df['max_payload'] = [4400, 4400, 2500, 2500, 95, 0.5]
    df['tonkm'] = (df['Energy Consumption [MJ/km]'] / df.max_payload) * 1000

    figure4(df)
    figure5(df)
    figureS1(df)


if __name__ == "__main__":
    main()
