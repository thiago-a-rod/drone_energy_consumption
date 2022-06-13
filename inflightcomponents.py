"""
This module calculates the inflight components used in the energy model
"""
import numpy as np
import airdensity


def hoverInducedPower(df):
    gravity = 9.81
    R = 0.15
    A = 4 * np.pi * R ** 2
    payload = df.payload.min()
    m = payload / 1000 + 3.08 + 0.635  # This mass includes the mass of the aircraft and battery
    rho = airdensity.AirDensity(df)
    return ((m*gravity)**(3/2))/np.sqrt(2*rho*A) # commented to exclude A and g


def mass_airdensity(df):
    payload = df.payload.min()
    m = payload / 1000 + 3.08 + 0.635  # This mass includes the mass of the aircraft and battery
    rho = airdensity.AirDensity(df)
    return ((m) ** (3 / 2)) / np.sqrt(rho)



