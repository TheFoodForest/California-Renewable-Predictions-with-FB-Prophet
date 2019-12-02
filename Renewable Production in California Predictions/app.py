from flask import Flask, jsonify 
import pandas as pd
from sqlalchemy import create_engine
from config import username, password

app = Flask(__name__)

engine = create_engine('postgresql://{}:{}@localhost:5432/California_Renewables'.format(username, password))

conn = engine.connect()
##sql = 'select a."ds", a.yhat as "Predicted Value", b."RENEW TOTAL" as "True Production", (a.yhat - b."RENEW TOTAL") as "Error"From "RenewablePredictions" aleft join "RenewableProduction" bon a."ds" = b."TIMESTAMP"order by a."ds"'
#responce_data = pd.read_sql(sql=sql,con=conn)



@app.route('/')
def home():
    return ('Welcome to my Renewable Predictions API! <br/>'
    'Available Routes: <br/>'
    'localhost:5000/contact <br/>'
    'localhost:5000/renewable_prod<br/>'
    'localhost:5000/api/renewable_prod/date/YYYY-mm-dd/unit:<br/>'
    '  EX:localhost:5000/api/renewable_prod/date/YYYY-mm-dd/MWh <br/>'
    '**Units: "MWh","GWh"'
    'localhost:500/api/date/range/ : <br/>'
    '**localhost:5000/api/date/range/YYYY-mm-dd(START DATE)/YYYY-mm-dd(END DATE)/unit '
    )

@app.route('/contact')
def contact():
    name = 'Graham Penrose'
    email = 'grahamelpenrose@gmail.com'
    return 'Please contact {} at {} with any questions/ comments'.format(name, email)

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
    responce_dict['summary'] = {'Total True Production':total_prod, 'Total Predicted Production':total_pred, 'Percent Error':p_err}
    return jsonify(responce_dict)



if __name__ == '__main__':
    app.run(debug=True)

