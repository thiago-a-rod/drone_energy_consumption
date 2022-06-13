"""
This module creates an energy summary of the flights.
"""

import pandas as pd
import scipy.integrate
import inflightcomponents as inflight


def avg_power_summary(df):
    takeOff = df[df.regime == "takeoff"]
    cruise = df[df.regime == "cruise"]
    landing = df[df.regime == "landing"]
    time_cruise = cruise['time'].max() - cruise['time'].min()
    time_takeoff = takeOff['time'].max() - takeOff['time'].min()
    time_landing = landing['time'].max() - landing['time'].min()
    time_whole = landing['time'].max() - takeOff['time'].min()

    e_measured_cruise = scipy.integrate.simps(cruise['power'], x=cruise["time"], even="avg")
    e_measured_takeoff = scipy.integrate.simps(takeOff['power'], x=takeOff["time"], even="avg")
    e_measured_landing = scipy.integrate.simps(landing['power'], x=landing["time"], even="avg")
    e_measured_whole = e_measured_takeoff + e_measured_cruise + e_measured_landing
    return e_measured_takeoff, e_measured_cruise, e_measured_landing, e_measured_whole,\
           time_takeoff, time_cruise, time_landing, time_whole


def create_energy_summary(data):
    '''
    :param data: data frame with all flights
    :return: creates a csv with an energy summary
    '''

    energy_summary = pd.DataFrame()
    flights = list(set(data['flight']))
    i = 1
    for flight in flights:
        print('flight: %d progress = %d%%'%(flight, i*100/len(flights)) , end='\r')
        df = data[data['flight'] == flight].copy()
        payload = df.payload.min()
        speed = df.speed.min()
        altitude = df.altitude.min()
        mass_rho = inflight.mass_airdensity(df)
        Pi_hover = inflight.hoverInducedPower(df)
        e_tk, e_cr, e_ld, e_wl, t_tk, t_cr, t_ld, t_wl = avg_power_summary(df)
        energy_flight = pd.DataFrame({'flight': [flight], 'payload': [payload], "altitude": [altitude],
                                      'speed': [speed], 'Energy_takeoff': e_tk, 'Energy_cruise': e_cr,
                                      'Energy_landing': e_ld, 'Energy_total': e_wl, 'time_takeoff': t_tk,
                                      'time_cruise':  t_cr, 'time_landing': t_ld, 'time_total': t_wl,
                                      'Power_takeoff': e_tk / t_tk, 'Power_cruise': e_cr / t_cr,
                                      'Power_landing': e_ld / t_ld, "avg_power": e_wl / t_wl,
                                      "mass_rho": mass_rho, "Pi_hover": Pi_hover})
        energy_summary = pd.concat([energy_summary,energy_flight], ignore_index=True)
        i += 1
    energy_summary.to_csv('data/energy_summary.csv', index=False)
    print("Energy Summary Created as energy_summary.csv")

def main():
    data = pd.read_csv("data/flights_processed.csv")
    data['power'] = data['battery_current']*data['battery_voltage']
    create_energy_summary(data)


if __name__ == '__main__':
    main()