from flask import Flask, jsonify 
import pandas as pd
from sqlalchemy import create_engine
from config import username, password
import numpy as np 

app = Flask(__name__, static_folder=r"C:\Users\graha\Desktop\Data Science Practice\California-Renewable-Predictions-with-FB-Prophet\Renewable Production in California Predictions\static")

engine = create_engine('postgresql://{}:{}@localhost:5432/California_Renewables'.format(username, password))

conn = engine.connect()

@app.route('/')
def home():
    return ('''
    <style>
        h1 {
    background-color: #c41e0c;
    color: #ffffff;
    font-family: arial, sans-serif;
    font-size: 30px;
    font-weight: bold;
    margin-top: 5px;
    margin-bottom: 5px;
    text-align:center;
    }

        .center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
        }

        h3{
    background-color: #c41e0c;
    color: #ffffff;
    font-family: arial, sans-serif;
    font-size: 20px;
    font-weight: bold;
    margin-top: 5px;
    margin-bottom: 5px;
    text-align:center;
        }

        li{
    font-family: arial, sans-serif;
    font-size: 15px;
    margin-top: 5px;
    margin-bottom: 5px;  
        }

    
        .center_text{
    text-align: center;
    list-style-position: inside;
        }

        ol.center_text li
    {
    text-align: left;
    margin-left: 30%;
        } 

        ul.center_text li
    {
    text-align: left;
    
        } 

    </style>
    <html>
    <head>
        <title>Renewable Predictions API</title>
    </head>
    <body>
    <h1>Welcome to my Renewable Predictions API!</h1> 
    <img src="static/image.png" alt="Solar Production in 2017" height="250" width="700" class="center"/>
    <br/>
    <h3>Available Routes:</h3> 
    <ol class="center_text">
        <li>localhost:5000/contact</li>
        <li>localhost:5000/renewable_prod</li>
        <li>localhost:5000/api/renewable_prod/date/YYYY-mm-dd/unit</li>
        <ul class="center_text">
            <li>Returns Hourly Production on provided date</li>
            <li>"unit" parameter is optional, default is "MWh" can pass "GWh"</li>
        </ul>
        <li>localhost:5000/api/renewable_prod/date/range/YYYY-mm-dd(START DATE)/YYYY-mm-dd(END DATE)/unit</li>
        <ul class="center_text">
            <li>Returns Hourly Production between two dates provided</li>
            <li>"unit" parameter is optional with same options as above</li>
        </ul>
    </ol>
    </body>
    </html>'''
    )

@app.route('/contact')
def contact():
    name = 'Graham Penrose'
    email = 'grahamelpenrose@gmail.com'
    return 'Please contact {} at {} with any questions/ comments'.format(name, email)

@app.route('/api/renewable_prod/date/<date_str>',defaults={'unit':'MWh'})
@app.route('/api/renewable_prod/date/<date_str>/<unit>')
def get_date_data(date_str,unit):
    responce_dict = {'production':{},
                     'summary':{}}
    sql = '''select a."ds", a.yhat as "Predicted Value", b."RENEW TOTAL" as "True Production", \
            (a.yhat - b."RENEW TOTAL") as "Error" From "RenewablePredictions" a left join "RenewableProduction" b \
            on a."ds" = b."TIMESTAMP" where to_char(a."ds", 'YYYY-mm-dd') = '{}' \
            order by a."ds"'''.format(date_str)
    responce_data = pd.read_sql(sql=sql,con=conn)
    responce_data['ds'] = pd.to_datetime(responce_data['ds'])
    responce_data['month'] = responce_data['ds'].dt.month
    responce_data['day'] = responce_data['ds'].dt.day
    responce_data['year'] = responce_data['ds'].dt.year
    responce_data['hour'] = responce_data['ds'].dt.hour
    responce_data['PE'] = np.absolute(responce_data['True Production'] - responce_data['Predicted Value'])/responce_data['True Production']
    responce_data = responce_data[['ds','year','month','day','hour','Predicted Value','True Production','Error','PE']]
    if unit == 'MWh':
        div = 1
    elif unit == 'GWh':
        div = 1000
    
    for index, row in responce_data.iterrows():
        pred = row[5]//div
        true = row[6]//div
        responce_dict['production']['{}'.format(row[0])] = {'Predicted Production':pred,'True Production':true}

    total_prod = round(responce_data['True Production'].sum()/div,2)
    total_pred = round(responce_data['Predicted Value'].sum()/div,2)
    err = total_pred - total_prod
    p_err = round((err/total_prod)*100,2)
    mape = round((np.sum(responce_data['PE'])/len(responce_data))*100,2)
    responce_dict['summary'] = {'Total True Production':total_prod, 'Total Predicted Production':total_pred, 'Percent Error':p_err,'Mean Absolute Percent Error':mape}
    return jsonify(responce_dict)

#Trying to figure out how to format the responce for the date range in a format that wold be easy to 
#work with.  Not sure of the best format for now
#Following format only returns the last hour of last day in range of dates
#totals seem to work properly 
@app.route('/api/renewable_prod/date/range/<start_date>/<end_date>',defaults={'unit':'MWh'})
@app.route('/api/renewable_prod/date/range/<start_date>/<end_date>/<unit>')
def get_range_data(start_date, end_date, unit):
    responce_dict = {'production':{'year':{'month':{'day':{'hour':{}}}}},
                     'summary':{}}
    sql = '''select a."ds", a.yhat as "Predicted Value", b."RENEW TOTAL" as "True Production", \
            (a.yhat - b."RENEW TOTAL") as "Error" From "RenewablePredictions" a left join "RenewableProduction" b \
            on a."ds" = b."TIMESTAMP" where to_char(a."ds", 'YYYY-mm-dd') >= '{}' and to_char(a."ds", 'YYYY-mm-dd') <= '{}'\
            order by a."ds"'''.format(start_date,end_date)
    responce_data = pd.read_sql(sql=sql,con=conn)
    responce_data['ds'] = pd.to_datetime(responce_data['ds'])
    responce_data['month'] = responce_data['ds'].dt.month
    responce_data['day'] = responce_data['ds'].dt.day
    responce_data['year'] = responce_data['ds'].dt.year
    responce_data['hour'] = responce_data['ds'].dt.hour
    responce_data['PE'] = np.absolute(responce_data['True Production'] - responce_data['Predicted Value'])/responce_data['True Production']
    responce_data = responce_data[['ds','year','month','day','hour','Predicted Value','True Production','Error','PE']]
    
    if unit == 'MWh':
        div = 1
    elif unit == 'GWh':
        div = 1000
    
    for index, row in responce_data.iterrows():
        pred = row[5]//div
        true = row[6]//div
        responce_dict['production'] = \
            {'{}'.format(row[1]) : {'{}'.format(row[2]) : {'{}'.format(row[3]) : {'{}'.format(row[4]) : {'Predicted Production':pred,
            'True Production':true}}}}}


    total_prod = round(responce_data['True Production'].sum()/div,2)
    total_pred = round(responce_data['Predicted Value'].sum()/div,2)
    err = total_pred - total_prod
    p_err = round((err/total_prod)*100,2)
    #responce_data['PE'] = np.absolute(responce_data['True Production'] - responce_data['Predicted Value'])/responce_data['True Production']
    mape = round((np.sum(responce_data['PE'])/len(responce_data))*100,2)
    responce_dict['summary'] = {'Total True Production':total_prod, 'Total Predicted Production':total_pred, 'Percent Error':p_err,'Mean Absolute Percent Error':mape}
    return jsonify(responce_dict)




if __name__ == '__main__':
    app.run(debug=True)

