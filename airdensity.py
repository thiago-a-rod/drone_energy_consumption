import pandas as pd
import datetime
import METAR_KAGC



def AirDensity(df_log):
    '''
    This function returns the air density for a particular flight
    :param df: [DataFrame] data frame with all the flights 'FlightSheet.csv'
    :param flight: [int] flight number
    :return: [float] air density in [kg/m^3]
    '''
    df = df_log.copy()
    df['date'] = df['date'] + ' '
    df['time_day'] = df['time_day'] + ':00.0'
    df['date'] = df['date'].astype(str)
    df['time_day'] = df['time_day'].astype(str)
    df['time_day'] = df[['date', 'time_day']].apply(lambda x: ''.join(x), axis=1)

    date_time_obj = datetime.datetime.strptime(df['time_day'].min(), '%Y-%m-%d %H:%M:%S.%f')
    rho = METAR_KAGC.calculate_density(date_time_obj)
    return rho


