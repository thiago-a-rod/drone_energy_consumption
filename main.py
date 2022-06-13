import pre_processing
import regime
import energy_summary
import energy_model
import power_speed
import energy_distance
import ghg_emission
import ghg_subregions
import vehicle_comparison
import ARE


def main():
    print("Preprocessing the data.")
    pre_processing.main()
    print('Generating flight-regime figures.')
    regime.main()
    print('Creating energy summary.')
    energy_summary.main()
    print('Calculating coefficients.')
    energy_model.main()
    print('Generating power-speed figure.')
    power_speed.main()
    print("Generating energy-distance figure.")
    energy_distance.main()
    print('Calculating GHG emissions.')
    ghg_emission.main()
    print('Assessing GHG emissions for subregions.')
    ghg_subregions.main()
    print('Comparing different vehicles.')
    vehicle_comparison.main()
    print('Calculating absolute relative errors')
    ARE.main()
    print('Status: Completed')


if __name__=="__main__":
    main()

