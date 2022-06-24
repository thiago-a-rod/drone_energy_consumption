"""
This module performs the GHG emission analysis provided in the paper.
"""

import pandas as pd
import energy_distance
import numpy as np


class Battery:
    def __init__(self, type, specific_energy, ghg_kg, mass, capacity, energy_km):
        self.type = type
        self.s_e = specific_energy  # kWh/kg of battery
        self.ghg_kg = ghg_kg  # gCO2e/kg of battery (GREET)
        self.mass = mass  # kg # mass of battery
        self.capacity = capacity  # Wh energy capacity of the battery
        self.energy_km = energy_km  # MJ/km energy consumption per km

    def calculate_mass(self):
        self.mass = (self.capacity/1000) / self.s_e

    def cycles(self, base, *low_high):
        self.cycles = base
        self.ghg_cycle = self.ghg_kg * self.mass / self.cycles
        self.ghg_MJ = self.ghg_cycle/self.capacity*(1000/3.6)
        self.ghg_km = self.ghg_MJ * self.energy_km


        if len(low_high) != 0:
            self.cycles_low = low_high[0]
            self.cycles_high = low_high[1]
            self.ghg_cycle_low = self.ghg_kg * self.mass / self.cycles_high  # more cycles means lower case for ghg/cycle
            self.ghg_cycle_high = self.ghg_kg * self.mass / self.cycles_low  # more cycles means lower case for ghg/cycle
            self.ghg_MJ_low = self.ghg_cycle_low / self.capacity * (1000/3.6)
            self.ghg_MJ_high = self.ghg_cycle_high / self.capacity * (1000/3.6)
            self.ghg_km_low = self.ghg_MJ_low * self.energy_km
            self.ghg_km_high = self.ghg_MJ_high * self.energy_km


def drone_ghg_emissions(energy, distance, electric_losses):
    coeff = pd.read_csv('data/coefficients.csv', index_col=0)
    drone_energy_base = energy_distance.energy_two_way(2, coeff, payload=500, speed=12, altitude=100,
                                                       rho=1.2) * 0.0036 / 4
    bat_drone = Battery("Li-iron", None, 4562.04, 0.6, 129.96, drone_energy_base)
    bat_drone.cycles(300, 150, 1000)  # cycles (base, low, high) cases
    ghg_bat = bat_drone.ghg_km * distance
    ghg_bat_low = bat_drone.ghg_km_low * distance
    ghg_bat_high = bat_drone.ghg_km_high * distance

    up_electricity = 22  # gCO2e/MJ upstream emissions (GREET)
    ghg_upstream = up_electricity * energy/electric_losses

    ghg_grid = [111, 177, 250]  # gCO2e/MJ (low, base, high) Non-baseload American emissions 2020 (eGRID)

    ghg_fuel = ghg_grid[1] * energy/electric_losses
    ghg_fuel_low = ghg_grid[0] * energy/electric_losses
    ghg_fuel_high = ghg_grid[2] * energy/electric_losses

    ghg_low = ghg_bat_low + ghg_upstream + ghg_fuel_low
    ghg_high = ghg_bat_high + ghg_upstream + ghg_fuel_high
    ghg = ghg_bat + ghg_upstream + ghg_fuel
    return ghg, ghg_low, ghg_high


def main():
    coeff = pd.read_csv('data/coefficients.csv', index_col=0)
    vehicles = ['Medium duty diesel truck', 'Small diesel vans', 'Medium duty e-truck',
                'Small electric van', 'Electric cargo bicycle', 'Quad-copter drone']
    base_distance = 2 # km
    drone_energy_base = energy_distance.energy_two_way(base_distance, coeff, payload=500, speed=12, altitude=100,
                                                       rho=1.2)*0.0036/(2*base_distance)
    # print(drone_energy_base,2*base_distance*drone_energy_base/0.0036)
    ghg_electricity = 177  # gCO2e/MJ
    ghg_diesel = 69.35  # gCO2e/MJ

    up_electricity = 22  # gCO2e/MJ upstream emissions (GREET)
    up_diesel = 15.34  # gCO2e/MJ upstream emissions (GREET)
    VMT = 121206 # miles (GREET)

    battery_capacity = np.array([80, 46.1])  # battery capacity of the Medium duty e-truck, Small electric van
    bat_capacity = 27  # kWh battery capacity Li-ion (GREET)
    ghg_Li_ion = 1611723  # g/vehicle lifetime Li-ion battery GHG for conventional material (GREET)
    ghg_kwh_bat = ghg_Li_ion/bat_capacity  #g/kWh of battery capacity constructed
    bat_emissions = ghg_kwh_bat*battery_capacity
    bat_emissions_km = bat_emissions/(VMT*1.60934)
    #print(bat_emissions_km)

    # battery emissions for drone
    electric_losses = 0.88 * (1 - 6.5 / 100)
    bat_drone = Battery("Li-iron", None, 4562.04, 0.6, 129.96, drone_energy_base)
    bat_drone.cycles(300, 150, 1000)  # cycles (base, low, high) cases
    ghg_bat_drone = bat_drone.ghg_km

    # e-cargo bicycle
    bat_capacity_bike = 0.5  # kWh
    bat_emissions_bike = ghg_kwh_bat * bat_capacity_bike
    energy_consumption_bike = (0.083/3.6)/electric_losses  # kWh/km
    cycles = 500  # lifetime cycles
    km_travelled = cycles * bat_capacity_bike/energy_consumption_bike
    bat_emissions_km_bike = bat_emissions_bike/km_travelled

    e_consumption = [11, 4.9, 3.13/electric_losses, 1.36/electric_losses, energy_consumption_bike*3.6,
                     drone_energy_base/electric_losses]
    ghg_upstream = [up_diesel, up_diesel, up_electricity, up_electricity, up_electricity, up_electricity]
    ghg_battery = [0, 0, bat_emissions_km[0], bat_emissions_km[1], bat_emissions_km_bike, ghg_bat_drone]
    ghg_fuel = [ghg_diesel, ghg_diesel, ghg_electricity, ghg_electricity, ghg_electricity, ghg_electricity]
    vehicles = pd.DataFrame({"Vehicle": vehicles, "energy consumption [MJ/km]": e_consumption, 'ghg_fuel [g/MJ]':ghg_fuel,
                             "ghg fuel upstream [g/MJ]": ghg_upstream, "GHG_battery [g/km]": ghg_battery})
    vehicles.to_csv("data/vehicles.csv", index=False)
    print(vehicles)


if __name__=="__main__":
    main()

