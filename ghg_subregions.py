import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from pprint import pprint
import energy_distance
import numpy as np


class Vehicle:
    def __init__(self, name, e_consumption, ghg_upstream, stop_km, pack_stop, pack_km_low, pack_km_high):
        self.name = name
        self.consumption = e_consumption
        self.upstream = ghg_upstream * e_consumption
        self.stop_km = stop_km
        self.pack_stop = pack_stop
        self.pack_km = pack_stop * stop_km
        self.energy_pack = e_consumption / self.pack_km
        self.pack_km_low = pack_km_low
        self.pack_km_high = pack_km_high
        self.energy_pack_upper = e_consumption / pack_km_low  # upper limit
        self.energy_pack_lower = e_consumption / pack_km_high  # lower limit

    def set_electric_emissions(self, egrid_df):
        self.fuel_emissions = {}
        for i in range(len(egrid_df)):
            self.fuel_emissions[egrid_df.loc[i, 'Region']] = egrid_df.loc[i, 'g/MJ'] * self.consumption

    def set_diesel_emissions(self, egrid_df, diesel_ghg):
        self.fuel_emissions = {}
        for i in range(len(egrid_df)):
            self.fuel_emissions[egrid_df.loc[i, 'Region']] = diesel_ghg * self.consumption

    def set_battery_emissions(self, battery_emission):
        self.battery = battery_emission

    def compute_ghg_total(self):
        self.total_ghg = {}
        for i in range(len(self.fuel_emissions)):
            region = list(self.fuel_emissions.keys())[i]
            self.total_ghg[region] = self.fuel_emissions[region] + self.upstream + self.battery

    def compute_ghg_pack(self):
        self.ghg_pack = {}
        self.fuel_pack = {}
        self.upstream_pack = self.upstream / self.pack_km
        self.battery_pack = self.battery / self.pack_km

        for i in range(len(self.fuel_emissions)):
            region = list(self.fuel_emissions.keys())[i]
            self.fuel_pack[region] = self.fuel_emissions[region] / self.pack_km
            self.ghg_pack[region] = self.total_ghg[region] / self.pack_km

    def compute_pack_to_drone(self, energy_pack_drone, ghg_pack_drone):
        self.energy_pack_to_drone = self.consumption / energy_pack_drone
        self.ghg_pack_to_drone = {}
        for i in range(len(self.fuel_emissions)):
            region = list(self.fuel_emissions.keys())[i]
            self.ghg_pack_to_drone[region] = self.total_ghg[region] / ghg_pack_drone[region]

    def compute_energy_drone_equivalent(self, package_km_drone):
        self.energy_drone_equivalent = self.energy_pack * package_km_drone


def table3(v, vehicles):
    name = []
    consumption = []
    fuel_emission = []
    upstream = []
    battery = []
    energy_pack = []
    ghg_package = []

    for i in range(len(vehicles)):
        name.append(v[i].name)
        consumption.append(v[i].consumption)
        upstream.append(v[i].upstream)
        energy_pack.append(v[i].energy_pack)
        battery.append(v[i].battery)
        fuel_emission.append(v[i].fuel_emissions['US'])
        ghg_package.append(v[i].ghg_pack['US'])

    df = pd.DataFrame({"Vehicle Class": name, 'Energy Consumption [MJ/km]': consumption,
                       'Fuel GHG emissions [g/km]':fuel_emission, 'Upstream GHG emissions [g/km]': upstream,
                       'Battery GHG emissions [g/km]': battery, "Energy consumption [MJ/package]": energy_pack, 'GHG emission [g/package]': ghg_package})

    df.to_csv("results/table3.csv", index=False)
    print(df)


def supplemental_tables(v, vehicles):
    total_ghg_df = pd.DataFrame({"subregion": v[0].total_ghg.keys()})
    ghg_pack_df = pd.DataFrame({"subregion": v[0].total_ghg.keys()})
    parameters = pd.DataFrame({"Vehicle Class": vehicles.Vehicle})
    delivery_intensity = []

    for i in range(2, len(vehicles)):
        total_ghg_df[v[i].name] = v[i].total_ghg.values()
        ghg_pack_df[v[i].name] = v[i].ghg_pack.values()
    for i in range(len(vehicles)):
        delivery_intensity.append((v[i].pack_km_low, v[i].pack_km, v[i].pack_km_high))

    parameters["Delivery intensity [packages/km] (lower, base, upper)"] = delivery_intensity

    total_ghg_df.sort_values(by=['subregion'], inplace=True)
    ghg_pack_df.sort_values(by=['subregion'], inplace=True)

    parameters.to_csv('results/tableS2.csv', index=False)
    total_ghg_df.to_csv('results/tableS3.csv', index=False)
    ghg_pack_df.to_csv("results/tableS4.csv", index=False)

def table2(v):
    v_class = [v[i].name for i in range(6)]
    mecrd = [v[i].energy_drone_equivalent for i in
             range(6)]  # minimum energy consumption required for the drone ([MJ/km])
    ddr = [v[i].energy_pack_to_drone for i in range(6)]
    ddr_multiplier = [v[i].energy_pack_to_drone / v[i].pack_km for i in range(6)]

    table2 = pd.DataFrame(
        {"Vehicle": v_class, "Delivery density required to match drone energy consumption [package/km]": ddr,
         "(multiplier from base case)": ddr_multiplier,
         "Minimum energy consumption required for the drone [MJ/km]": mecrd})
    table2.to_csv("results/table2.csv", index=False)
    print(table2)


def maps(subregions, egrid, v):
    regions = egrid.Region.copy()
    ghg_packs_to_drone = pd.DataFrame({"region": regions})
    for i in range(len(v)):
        ghg_packs_to_drone[v[i].name] = v[i].ghg_pack_to_drone.values()
    ghg_packs_to_drone['drone_emissions'] = v[5].ghg_pack.values()
    ghg_packs_to_drone['drone_emissions_km'] = v[5].total_ghg.values()

    subregions.rename(columns={"ZipSubregi": "region"}, inplace=True)
    df = pd.merge(subregions, ghg_packs_to_drone, on='region', how='outer')
    df_main = df.copy()
    df_main.drop([0, 1, 6, 7, 26], inplace=True)

    fig, ax = plt.subplots(1, figsize=(10, 6))
    v_compare = 'drone_emissions_km'
    vmin = df[v_compare].min()
    vmax = df[v_compare].max()
    palet = "viridis_r"
    df_main.plot(column=v_compare, cmap=palet, linewidth=0.8, ax=ax, edgecolor='0',
                 norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm = plt.cm.ScalarMappable(cmap=palet, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []  # empty array for the data range
    cbar = fig.colorbar(sm)  # add the colorbar to the figure
    cbar.ax.set_ylabel("gCO₂e/km", fontsize=16)

    plt.tick_params(axis='both', which='both', bottom=False, left=False,
                    labelbottom=False, labelleft=False)
    sns.despine(top=True, right=True, bottom=True, left=True)
    fig.savefig('results/figure3.pdf', dpi=300)

    fig, ax = plt.subplots(1, figsize=(10, 6))
    v_compare = 'Medium duty diesel truck'
    vmin = df[v_compare].min()
    vmax = df[v_compare].max()
    palet = "cividis_r"
    df_main.plot(column=v_compare, cmap=palet, linewidth=0.8, ax=ax, edgecolor='0',
                 norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm = plt.cm.ScalarMappable(cmap=palet, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []  # empty array for the data range
    cbar = fig.colorbar(sm)  # add the colorbar to the figure
    cbar.ax.set_ylabel("Packages per km", fontsize=16)
    # ax.set_xlabel('Longitude (deg)')
    # ax.set_ylabel('Latitude (deg)')
    plt.tick_params(axis='both', which='both', bottom=False, left=False,
                    labelbottom=False, labelleft=False)
    # ax.set_title("", fontsize=16)
    sns.despine(top=True, right=True, bottom=True, left=True)
    fig.savefig('results/figure6.pdf')
    plt.show()


def attribute_units():
    unit_dict = {'name': 'str', 'consumption': 'MJ/km', 'upstream': "gCO2e/km",
                 'stop_km': "stop/km", 'pack_stop': 'package/stop', 'pack_km': 'package/km',
                 'pack_km_low': 'package/km', 'pack_km_high': 'package/km',
                 'energy_pack': 'MJ/package', 'energy_pack_upper': 'MJ/package', 'energy_pack_lower': 'MJ/package',
                 'fuel_emissions': 'gCO2e/km', 'battery': 'gCO2e/km', 'total_ghg': "gCO2e/km",
                 'upstream_pack': 'gCO2e/package',
                 'battery_pack': 'gCO2e/package', 'fuel_pack': 'gCO2e/package', 'ghg_pack': 'gCO2e/package',
                 "energy_pack_to_drone": 'package/km', "ghg_pack_to_drone": 'package/km',
                 "energy_drone_equivalent": "MJ/km"}
    for key in unit_dict.keys():
        print(key, ":", unit_dict[key])


def main():
    try:
        file_name = 'CO₂ equivalent non-baseload output emission rate (lb_MWh), by eGRID subregion, 2020.csv'
        egrid = pd.read_csv('data/'+file_name)
    except FileNotFoundError:
        print('''
                --------------------------------------------
                Error: File 'CO₂ equivalent non-baseload output emission rate (lb_MWh), by eGRID subregion, 2020.csv' not found.
                Please download the file 'CO₂ equivalent non-baseload output emission rate (lb_MWh), by eGRID subregion, 2020.csv' from:
                https://www.epa.gov/egrid/data-explorer
                --------------------------------------------''')
    try:
        subregions = gpd.read_file("data/eGRID2020_subregions.shp")
    except FileNotFoundError:
        print('''
                --------------------------------------------
                Error: File 'eGRID2020_subregions.shp' not found.
                Please download the file 'eGRID2020_subregions.shp' from:
                https://www.epa.gov/egrid/egrid-mapping-files
                --------------------------------------------''')

    vehicles = pd.read_csv("data/vehicles.csv")

    egrid['g/MJ'] = egrid[' CO2 equivalent non-baseload output emission rate (lb/MWh) by eGRID subregion 2020']*453.592/3600

    stop_km = np.array([0.7, 1.74, 0.7, 1.74, 1, 0.25])  # fleet DNA
    battery = vehicles['GHG_battery [g/km]']
    diesel_ghg = vehicles.loc[0, 'ghg_fuel [g/MJ]']
    pack_stop = np.array([3, 2, 3, 2, 1, 1])
    pack_km_low = np.array([1.5, 1.5, 1.5, 1.5, 0.25, 0.125])
    pack_km_high = np.array([5, 5, 5, 5, 3, 0.5])

    vclass = vehicles.Vehicle

    v = []
    for i in range(len(vclass)):
        v.append(Vehicle(vclass[i], vehicles.loc[i, 'energy consumption [MJ/km]'],
                         vehicles.loc[i, 'ghg fuel upstream [g/MJ]'], stop_km[i], pack_stop[i],
                         pack_km_low[i], pack_km_high[i]))
        v[i].set_battery_emissions(battery[i])
        if i < 2:
            v[i].set_diesel_emissions(egrid, diesel_ghg)
        else:
            v[i].set_electric_emissions(egrid)
        v[i].compute_ghg_total()
        v[i].compute_ghg_pack()
    for i in range(len(vclass)):
        v[i].compute_pack_to_drone(v[5].energy_pack, v[5].ghg_pack)
        v[i].compute_energy_drone_equivalent(v[5].pack_km)



    table3(v, vehicles)
    supplemental_tables(v, vehicles)
    table2(v)
    maps(subregions,egrid,v)

if __name__=="__main__":
    main()
