"""
This module calculate the error for the main energy model and compares it with other models.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.integrate


def calculate_are_ML():
    cruise = pd.read_csv("data/predictions_cruise.csv", low_memory=False)
    landing = pd.read_csv("data/predictions_landing.csv", low_memory=False)
    takeoff = pd.read_csv("data/predictions_takeOff.csv", low_memory=False)
    data = pd.read_csv("data/flights_processed.csv", low_memory=False)
    data['p'] = data.battery_current*data.battery_voltage
    sample = pd.read_csv("data/sample.csv")
    df_cruise = data[~(data.flight.isin(list(sample.flight)))&(data.regime=='cruise')]
    df_cruise.reset_index()

    df_landing = data[~(data.flight.isin(list(sample.flight))) & (data.regime == 'landing')]
    df_landing.reset_index()

    df_takeoff = data[~(data.flight.isin(list(sample.flight))) & (data.regime == 'takeoff')]
    df_takeoff.reset_index()

    flights = list(set(df_cruise.flight))
    E, E_hat = [], []

    for flight in flights:
        data_cr = df_cruise [df_cruise .flight == flight].copy()
        cr = cruise[cruise.flights == flight].copy()
        e_cr = scipy.integrate.simps(data_cr.p, x=data_cr["time"], even="avg")
        e_hat_cr = scipy.integrate.simps(cr.predictions, x=data_cr["time"], even="avg")

        data_ld = df_landing[df_landing.flight == flight].copy()
        ld = landing[landing.flights == flight].copy()
        e_ld = scipy.integrate.simps(data_ld.p, x=data_ld["time"], even="avg")
        e_hat_ld = scipy.integrate.simps(ld.predictions, x=data_ld["time"], even="avg")

        data_tk = df_takeoff[df_takeoff.flight == flight].copy()
        tk = takeoff[takeoff.flights == flight].copy()
        e_tk = scipy.integrate.simps(data_tk.p, x=data_tk["time"], even="avg")
        e_hat_tk = scipy.integrate.simps(tk.predictions, x=data_tk["time"], even="avg")

        E.append(e_cr+e_ld+e_tk)
        E_hat.append(e_hat_cr+e_hat_ld+e_hat_tk)

    ARE_ML = np.fabs(np.array(E) - np.array(E_hat))/np.array(E)
    return ARE_ML

def main():
    plt.rcParams.update({'figure.autolayout': True})
    plt.rcParams["font.family"] = "Helvetica"
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})

    coeff = pd.read_csv("data/coefficients.csv")
    sample = pd.read_csv("data/sample.csv")
    summary = pd.read_csv("data/energy_summary.csv")
    df = summary[~summary.flight.isin(sample.flight)]
    df.reset_index(inplace=True)
    model_2_error = pd.read_csv("data/model_2error.csv")
    ARE_model2 = np.fabs(model_2_error.model2)
    ARE_ML = calculate_are_ML()

    x = df.mass_rho
    b1_tk = coeff.loc[0, 'b1']
    b1_cr = coeff.loc[1, 'b1']
    b1_ld = coeff.loc[2, 'b1']
    b0_tk = coeff.loc[0, 'b0']
    b0_cr = coeff.loc[1, 'b0']
    b0_ld = coeff.loc[2, 'b0']

    e = df.Energy_total
    e_hat = (b1_tk*x + b0_tk)*df.time_takeoff + (b1_cr*x + b0_cr)*df.time_cruise + (b1_ld*x + b0_ld)*df.time_landing
    e_hat = np.array(e_hat)
    model1_error = np.fabs(e - e_hat)/(e)

    ARE = pd.DataFrame({"Model 1": model1_error, "Model 2": ARE_model2, "XGBoost": ARE_ML})

    plt.grid(which="major", alpha=0.2)
    sns.boxplot(data=ARE)
    sns.despine(top=True, right=True)
    plt.ylabel("Absolute relative error", fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig("results/figureS11.pdf")
    plt.show()


if __name__=="__main__":
    main()