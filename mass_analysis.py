"""
This script is not available on GITHUB
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def energy_two_way(distance, coeff, m, payload, speed=12, altitude=100, rho=1.2):
    x_unload = ((m) ** (3 / 2)) / np.sqrt(rho)
    x_load = ((m + payload) ** (3 / 2)) / np.sqrt(rho)

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


def main():
    plt.rcParams.update({'figure.autolayout': True})
    coeff = pd.read_csv("data/coefficients.csv", index_col=0)
    v = pd.read_csv("results/table3.csv")

    print(v)
    mass = np.arange(0, 25.5, 0.005)
    distance = 4
    payload = 0.5
    e_05 = [energy_two_way(distance, coeff, m, payload, speed=12, altitude=100, rho=1.2)*0.0036 for m in mass]
    e_1 = [energy_two_way(distance, coeff, m, 2*payload, speed=12, altitude=100, rho=1.2) * 0.0036 for m in mass]
    e_2 = [energy_two_way(distance, coeff, m, 4*payload, speed=12, altitude=100, rho=1.2) * 0.0036 for m in mass]
    e_5 = [energy_two_way(distance, coeff, m, 10*payload, speed=12, altitude=100, rho=1.2) * 0.0036 for m in mass]
    e_10 = [energy_two_way(distance, coeff, m, 20*payload, speed=12, altitude=100, rho=1.2) * 0.0036 for m in mass]
    fig = plt.figure(figsize=(10, 6))
    plt.grid(which="Major", alpha=0.2)

    plt.plot(mass, e_05, label='500 g', color='#ABD7EC')
    plt.plot(mass, e_1, label='1 kg', color='#59C1E8')
    plt.plot(mass, e_2, label='2 kg', color='#3585DA')
    plt.plot(mass, e_5, label='5 kg', color='#1061B0')
    plt.plot(mass, e_10, label='10 kg', color='#003C72')
    sns.despine(top=True, right=True)
    plt.xlabel("Drone mass [kg]\n(aircraft + battery) ", fontsize=14)  # includes the aircraft, battery and payload. Assumes a payload weighting 10% of the total mass.
    plt.ylabel("Energy consumption [MJ/package]", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(0, 25)
    plt.ylim(0,5.5)
    data = pd.DataFrame({"mass":mass, "energy":e_05})
    color = ['orange', 'black', 'red', 'brown', 'gray', 'blue']
    for i in range(len(v['Vehicle Class'])):
        y = v.loc[i, 'Energy consumption [MJ/package]']
        data['y'] = np.fabs(data.energy - y)
        x_max = data.loc[data.y == data.y.min(), 'mass'].copy()
        plt.hlines(y, 0, x_max, linestyles='--', colors='black', alpha=0.3)
        # plt.vlines(x_max, 0, y, linestyles='--', colors=color[i], alpha=0.5)
        # plt.scatter(x_max, y, marker="o", c=color[i], label=v.loc[i, 'Vehicle Class'])
        plt.text(x_max + 0.8, y - 0.08, v.loc[i, 'Vehicle Class'])
    plt.legend(title="Payload mass", bbox_to_anchor=(1.15, 0.45), frameon=False)


    print()






    plt.show()



if __name__=='__main__':
    main()

