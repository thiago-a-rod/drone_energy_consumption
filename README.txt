This README.txt file was generated on 2022-06-13 by Thiago A. Rodrigues
+------------+---------+
------------+---------+
------------+---------+
------------+---------+
------------+---------+
------------+---------+
------------+---------+
------------+---------+
13. ARE.py

This project contains the following CSV files:
01. model_2error.csv
02. sample.csv
03. predictions_cruise.csv
04. predictions_landing.csv
05. predictions_takeOff.csv

External dependencies (should be uploaded to folder 'data' before running): 
01. 'flights.csv': https://doi.org/10.1184/R1/12683453.v1
02. 'CO₂ equivalent non-baseload output emission rate (lb_MWh), by eGRID subregion, 2020.csv': https://www.epa.gov/egrid/data-explorer 
03. 'eGRID2020_subregions.shp': https://www.epa.gov/egrid/egrid-mapping-files

Execute the script "main.py" to run the analysis.
XGBoost functions are available at helpers.r and modeling_byregime.r



Scripts, dependencies, and outputs: 
-------+-----------------------+----------------------------------------+-----------------------+
| Order | Script                | Dependencies                           | Outcome               |
+-------+-----------------------+----------------------------------------+-----------------------+
| 1     | pre_processing.py     | regime.py                              | flights_processed.csv |
|       |                       | flights.csv                            |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 2     | regime.py             | flights.csv                            | Figure S1             |
|       |                       |                                        | Figure S2             |
|       |                       |                                        | Figure S3             |
|       |                       |                                        | Figure S4             |
+-------+-----------------------+----------------------------------------+-----------------------+
| 3     | energy_summary.py     | inflightcomponents.py                  | energy_summary.csv    |
|       |                       | airdensity.py                          |                       |
|       |                       | METAR_KAGC.py                          |                       |
|       |                       | flights_processed.csv                  |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 4     | energy_model.py       | LinearRegression.py                    | Table 1               |
|       |                       | sample.csv                             | Figure 8              |
|       |                       |                                        | coefficients.csv      |     
+-------+-----------------------+----------------------------------------+-----------------------+
| 5     | power_speed.py        | energy_summary.csv                     | Figure 1              |
+-------+-----------------------+----------------------------------------+-----------------------+
| 6     | energy_distance.py    | ghg_emissions.py                       | Figure 2              |
|       |                       | coefficients.csv                       |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 7     | ghg_emissions.py      | coefficients.csv                       | vehicles.csv          |
+-------+-----------------------+----------------------------------------+-----------------------+
| 8     | ghg_subregions.py     | eGRID2020_subregions.cpg               | Table 2               |
|       |                       | eGRID2020_subregions.dbf               | Table 3               |
|       |                       | eGRID2020_subregions.prj               | Table S2              |
|       |                       | eGRID2020_subregions.sbn               | Table S3              |
|       |                       | eGRID2020_subregions.sbx               | Table S4              |
|       |                       | eGRID2020_subregions.shp               | Figure 3              |
|       |                       | eGRID2020_subregions.shx               | Figure 6              |
|       |                       | "CO2 equivalent non-baseload output    |                       |
|       |                       |      emission rate (lb_MWh), by eGRID  |                       |
|       |                       |      subregion, 2020.csv"              |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 9     | vehicle_comparison.py | table3.csv                             | Figure 4              |
|       |                       |                                        | Figure 5              |
|       |                       |                                        | Figure S5             |
+-------+-----------------------+----------------------------------------+-----------------------+
| 10    | ARE.py                | model_2error.csv                       | Figure S11            |
|       |                       | sample.csv                             |                       |
|       |                       | coefficients.csv                       |                       |
|       |                       | energy_summary.csv                     |                       |
+-------+-----------------------+----------------------------------------+-----------------------+