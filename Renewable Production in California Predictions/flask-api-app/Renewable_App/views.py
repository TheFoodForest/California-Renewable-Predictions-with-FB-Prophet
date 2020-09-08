"""
Flask views for rendering templates 

"""
## Flask file creating the routes for the rendering and getting data from db

from flask import jsonify, render_template, url_for
from Renewable_App import app
from Renewable_App import conection
import pandas as pd
import numpy as np 


 
Con = conection.Connection('local')
engine = Con.init_connection_engine()


conn = engine.connect()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/api')
def api():
    return render_template('api.html')




@app.route('/api/renewable_prod/date/<date_str>',defaults={'unit':'MWh'})
@app.route('/api/renewable_prod/date/<date_str>/<unit>')
def get_date_data(date_str,unit):
    sql = '''SELECT * FROM "Comparison".percentproductionrenewable r
             WHERE to_char(r."Date", 'YYYY-MM-DD') = '{}' '''.format(date_str)
    data = pd.read_sql(sql=sql,con=conn)
    if str(unit).upper() in ['GWH','GW','G']:
        data['Renewable Production'] = data['Renewable Production'] / 1000
        data['Total Production'] = data['Total Production'] / 1000
    data['Hour'] = data['Date'].dt.hour
    data.drop(columns=['Date'], inplace=True)
    data = data[['Hour', 'Renewable Production','Total Production','Percent Production Renew']]
    responce = data.to_dict(orient='list')
    return jsonify(responce)


@app.route('/api/renewable_prod/date/range/<start_date>/<end_date>',defaults={'unit':'MWh'})
@app.route('/api/renewable_prod/date/range/<start_date>/<end_date>/<unit>')
def get_range_data(start_date, end_date, unit):
    responce = {}
    dates = np.array(pd.date_range(start='{}'.format(start_date),end='{}'.format(end_date)).date)
    for date in dates:
        datee = str(date)
        sql = '''SELECT * FROM "Comparison".percentproductionrenewable r
                WHERE to_char(r."Date", 'YYYY-MM-DD') = '{}' '''.format(datee)
        try:
            data = pd.read_sql(sql=sql,con=conn)
            if str(unit).upper() in ['GWH','GW','G']:
                data['Renewable Production'] = data['Renewable Production'] / 1000
                data['Total Production'] = data['Total Production'] / 1000
            data['Hour'] = data['Date'].dt.hour
            data.drop(columns=['Date'], inplace=True)
            data = data[['Hour', 'Renewable Production','Total Production','Percent Production Renew']]
            responce['{}'.format(datee)] = data.to_dict(orient='list')
        except:
            responce['{}'.format(datee)] = ["No production data for this date"]
    return jsonify(responce)


@app.route('/api/renewable_demand/date/<date_str>',defaults={'unit':'MWh'})
@app.route('/api/renewable_demand/date/<date_str>/<unit>')
def get_date_data_demand(date_str,unit):
    sql = '''SELECT * FROM "Comparison".percentdemandrenewable r
             WHERE to_char(r."Date", 'YYYY-MM-DD') = '{}' '''.format(date_str)
    data = pd.read_sql(sql=sql,con=conn)
    if str(unit).upper() in ['GWH','GW','G']:
        data['Renewable Production'] = data['Renewable Production'] / 1000
        data['Total Demand'] = data['Total Production'] / 1000
    data['Hour'] = data['Date'].dt.hour
    data.drop(columns=['Date'], inplace=True)
    data = data[['Hour', 'Renewable Production','Total Demand','Percent Demand Renew']]
    responce = data.to_dict(orient='list')
    return jsonify(responce)


@app.route('/api/renewable_demand/date/range/<start_date>/<end_date>',defaults={'unit':'MWh'})
@app.route('/api/renewable_demand/date/range/<start_date>/<end_date>/<unit>')
def get_range_data_demand(start_date, end_date, unit):
    responce = {}
    dates = np.array(pd.date_range(start='{}'.format(start_date),end='{}'.format(end_date)).date)
    for date in dates:
        datee = str(date)
        sql = '''SELECT * FROM "Comparison".percentdemandrenewable r
                WHERE to_char(r."Date", 'YYYY-MM-DD') = '{}' '''.format(datee)
        try:
            data = pd.read_sql(sql=sql,con=conn)
            if str(unit).upper() in ['GWH','GW','G']:
                data['Renewable Production'] = data['Renewable Production'] / 1000
                data['Total Demand'] = data['Total Demand'] / 1000
            data['Hour'] = data['Date'].dt.hour
            data.drop(columns=['Date'], inplace=True)
            data = data[['Hour', 'Renewable Production','Total Demand','Percent Demand Renew']]
            responce['{}'.format(datee)] = data.to_dict(orient='list')
        except:
            responce['{}'.format(datee)] = ["No production data for this date"]
    return jsonify(responce)