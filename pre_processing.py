"""
This module process the data avaliable at https://doi.org/10.1184/R1/12683453.v1
"""

import pandas as pd
import regime


def main():
    try:
        data = pd.read_csv('data/flights.csv', low_memory=False)
        data = data[((data.route == 'R1') | (data.route == 'R2') | (data.route == 'R3') | (data.route == 'R4') |
                     (data.route == 'R5')) & (data.payload < 750)]
        flights = list(set(data.flight))
        data_processed = pd.DataFrame()
        for flight in flights:
            df = data[data.flight == flight].copy()
            takeOff, landing, cruise, wholeflight = regime.find_regime(df)
            for r in [takeOff, cruise, landing]:
                data_processed = pd.concat([data_processed, r], ignore_index=True)
        data_processed.to_csv("data/flights_processed.csv", index=False)
    except FileNotFoundError:
        print('''
        --------------------------------------------
        Error: File 'flights.csv' not found.
        Please download the file 'flights.csv' from:
        https://doi.org/10.1184/R1/12683453.v1
        --------------------------------------------''')



if __name__ == '__main__':
    main()
