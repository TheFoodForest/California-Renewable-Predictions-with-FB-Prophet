# California Renewable Predictions with FB Prophet

Overview:
  - Sourced California Renewable Production data from Kaggle
  - Exploratory analysis of production data in jupyter notebook 
  - FB Prophet time series modeling near the end of analysis notebook for predicting total renewable production per hour
  - Built PostgreSQL database with sourced data and wrote predictions into database
  - Python file using Flask to create localhost api that returns Predicted and True values for total renewable produciton based off input date in json format
 
Project still in development...
 
 
Future Plans:
  - Get CAISO API access to recreate data pulled from kaggle but extend the end of the dates of data available to most current data available from CAISO
    - Current data ends partially into 2018
  - Source Cali power demand data per hour to predict future demand and analize predicted success of meeting 33% renewable production by 2020
  
  
