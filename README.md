# California Renewable Predictions with FB Prophet
Data
-
California ISO Reports - [http://www.caiso.com/market/Pages/ReportsBulletins/DailyRenewablesWatch.aspx](http://www.caiso.com/market/Pages/ReportsBulletins/DailyRenewablesWatch.aspx)

US Energy Information Administration (EIA) API - [https://www.eia.gov/opendata/register.php](https://www.eia.gov/opendata/register.php)

Everything here only runs locally, project built out of interest in topic and for practice with data analytics. The reports use raw data and are not intended to be used as the basis for operational or financial decisions.

Contents
-
### California-Renewable-Predictions-with-FB-Prophet:
#### ETL:
- Jupyter notebook that:
  - Builds structure for local PostgreSQL database
  - Gets California energy prodction data from daily renewable reports on CAISO website 
  - Gets historic California energy demand data from EIA API
  - Builds dataframes with the data and writes to database
#### Predictions and Analysis:
  - Jupyter notebook for analyzing flow of energy through California  
  - Jupyter notebook using FB Prophet to predict renewable power production and write results to DB
  - Jupyter notebook for predicting energy demand
#### SQL:
  - SQL files for refernce, all sql is also in ETL jupyter notebook  
#### Flask-api-app
  - APP ONLY LOCAL, NOT REDISTRUBUTING DATA 
  - local app that returns data from built database 
  - home page html is in "templates" folder 


Contributors
-
- [Scott Clark](https://github.com/scottinsactown)
  - Contributed to ETL process and database set-up 
  - Created some of the visualizations in renewable production and energy demand analysis 

Project Still in Development 
-
Future Plans:
- Continue to work on improving Renewable Prediction Accuracy
- Build Demand Prediction Model 
- Improve API (more routes, more pages, better home page, ...) 

