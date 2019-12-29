# California Renewable Predictions with FB Prophet

Contents
-
California-Renewable-Predictions-with-FB-Prophet:
-ETL:
  -Jupyter notebook that sets up SQL DB, then scrapes renewable production data from CAISO and pulls energy demand data from EIA API, and loads into database
-Predictions and Analysis:
  -Jupyter notebook for analyzing renewable production data in California 
  -Jupyter notebook for analyzing total energy demand in California
  -Jupyter notebook using FB Prophet to predict renewable power production and write results to DB
  -Jupyter notebook for predicting energy demand
-SQL:
  - SQL files for refernce, all sql is also in ETL jupyter notebook  
-Flask-api-app
  -local app that returns data from built database 
  -home page html is in "templates" folder 


Contributors
-
-[Scott Clark](https://github.com/scottinsactown)
  - Contributed to ETL process and database set-up 
  - Created some of the visualizations in renewable production and energy demand analysis 

PROJECT STILL IN DEVELOPMENT
-
Future Plans:
- Continue to scrape/ request most current data and work on improving Renewable Prediction Accuracy
- Build Demand Prediction Model 
- Improve API (more routes, more pages, better home page, ...) 

