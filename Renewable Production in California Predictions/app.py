from flask import Flask, jsonify 
import pandas as pd
from sqlalchemy import create_engine
from config import username, password
import numpy as np 

app = Flask(__name__, static_folder=r"C:\Users\graha\Desktop\Data Science Practice\California-Renewable-Predictions-with-FB-Prophet\Renewable Production in California Predictions\static")

engine = create_engine('postgresql://{}:{}@localhost:5432/California_Renewables'.format(username, password))

conn = engine.connect()
##sql = 'select a."ds", a.yhat as "Predicted Value", b."RENEW TOTAL" as "True Production", (a.yhat - b."RENEW TOTAL") as "Error"From "RenewablePredictions" aleft join "RenewableProduction" bon a."ds" = b."TIMESTAMP"order by a."ds"'
#responce_data = pd.read_sql(sql=sql,con=conn)



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
/*
        ol.center_text li
    {
    text-align: left;
    margin-left: 45%;
        } 

        ul.center_text li
    {
    text-align: left;
    
        } 
*/
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
        <ul class='center_list>
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
            on a."ds" = b."TIMESTAMP" where to_char(a."ds", 'YYYY-mm-dd') = '{}'\
            order by a."ds"'''.format(date_str)
    responce_data = pd.read_sql(sql=sql,con=conn)
    if unit == 'MWh':
        div = 1
    elif unit == 'GWh':
        div = 1000
    
    for index, row in responce_data.iterrows():
        pred = row[1]//div
        true = row[2]//div
        responce_dict['production']['{}'.format(row[0])] = {'Predicted Production':pred,'True Production':true}

    total_prod = round(responce_data['True Production'].sum()/div,2)
    total_pred = round(responce_data['Predicted Value'].sum()/div,2)
    err = total_pred - total_prod
    p_err = round((err/total_prod)*100,2)
    responce_data['PE'] = np.absolute(responce_data['True Production'] - responce_data['Predicted Value'])/responce_data['True Production']
    mape = round((np.sum(responce_data['PE'])/len(responce_data))*100,2)
    responce_dict['summary'] = {'Total True Production':total_prod, 'Total Predicted Production':total_pred, 'Percent Error':p_err,'Mean Absolute Percent Error':mape}
    return jsonify(responce_dict)



if __name__ == '__main__':
    app.run(debug=True)

