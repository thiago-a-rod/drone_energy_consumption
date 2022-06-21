This README.txt file was generated on 2022-06-13 by Thiago A. RodriguesAuthor Contact Information    Name: Thiago A. Rodrigues    Institution: Carnegie Mellon University    Address: 5000 Forbes Avenue, Pittsburgh, Pennsylvania, USA, 1521    Email: tarodrig@andrew.cmu.edu-------------------GENERAL INFORMATION-------------------Project Title: Drone flight data reveal energy and greenhouse gas emissions savings for very small package delivery.Project Description: This project provides the scripts used for data processing, data analysis, development of the energy model, comparison of vehicles, and visualizations described in the paper of the same title. ---------------------DATA & FILE OVERVIEW---------------------The versions of the main packages used are:
+------------+---------+| Package    | Version |+------------+---------+| pandas     | 1.4.2   |+------------+---------+| matplotlib | 3.5.2   |+------------+---------+| scipy      | 1.8.1   |+------------+---------+| seaborn    | 0.11.2  |+------------+---------+| metar      | 1.9.0   |+------------+---------+| geopandas  | 0.10.2  |+------------+---------+This project contains the following scripts: 01. airdensity.py02. energy_distance.py03. energy_model.py04. energy_summary.py05. ghg_emissions.py06. ghg_subregions.py07. inflightcomponents.py08. LinearRegresision.py09. METAR_KAGC.py10. power_speed.py11. pre_processing.py12. regime.py13. vehicle_comparison.py
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
03. 'eGRID2020_subregions.shp' and 'eGRID2020_subregions.shx': https://www.epa.gov/egrid/egrid-mapping-files

Execute the script "main.py" to run the analysis.
XGBoost functions are available at helpers.r and modeling_byregime.r


Scripts, dependencies, and outputs: +-------+-----------------------+----------------------------------------+-----------------------+
| Order | Script                | Dependencies                           | Outcome               |
+-------+-----------------------+----------------------------------------+-----------------------+
| 1     | pre_processing.py     | regime.py                              | flights_processed.csv |
|       |                       | flights.csv                            |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 2     | regime.py             | flights.csv                            | Figure S3             |
|       |                       |                                        | Figure S4             |
|       |                       |                                        | Figure S5             |
|       |                       |                                        | Figure S6             |
+-------+-----------------------+----------------------------------------+-----------------------+
| 3     | energy_summary.py     | inflightcomponents.py                  | energy_summary.csv    |
|       |                       | airdensity.py                          |                       |
|       |                       | METAR_KAGC.py                          |                       |
|       |                       | flights_processed.csv                  |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 4     | energy_model.py       | LinearRegression.py                    | Table 1               |
|       |                       | sample.csv                             | Figure 7              |
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
|       |                       | eGRID2020_subregions.shx               | Figure S2             |
|       |                       | "CO2 equivalent non-baseload output    |                       |
|       |                       |      emission rate (lb_MWh), by eGRID  |                       |
|       |                       |      subregion, 2020.csv"              |                       |
+-------+-----------------------+----------------------------------------+-----------------------+
| 9     | vehicle_comparison.py | table3.csv                             | Figure 4              |
|       |                       |                                        | Figure 5              |
|       |                       |                                        | Figure S1             |
+-------+-----------------------+----------------------------------------+-----------------------+
| 10    | ARE.py                | model_2error.csv                       | Figure S12            |
|       |                       | sample.csv                             |                       |
|       |                       | coefficients.csv                       |                       |
|       |                       | energy_summary.csv                     |                       |
+-------+-----------------------+----------------------------------------+-----------------------+