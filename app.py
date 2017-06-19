from flask import Flask, render_template, request, redirect
import requests
import json as simplejson
import pandas as pd
from bokeh.charts import TimeSeries, show, output_file
from bokeh.embed import components 

app = Flask(__name__) #root path

@app.route('/result', methods=['POST']) # home page
def result():
  ticker=request.form['dataset_code']
  r=requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?api_key=tBXpG5nLBevqCdXXFi1U')
  json_object=r.json()
  close_data, open_data, date_data=[],[],[]
  data=json_object['dataset']['data']
  for arr in data:
    date_data.append(arr[0])
    open_data.append(arr[1])
    close_data.append(arr[4])
  if request.form.getlist('Close'):
    d=pd.DataFrame(dict(Date=date_data, Price=close_data))
    pp1 = TimeSeries(d, x='Date',title="close price",ylabel='Stock Prices')
    script,div=components(pp1)
    return render_template('result.html', script=script, div=div)
  if request.form.getlist('Open'):
    d=pd.DataFrame(dict(Date=date_data, Price=open_data))
    pp2 = TimeSeries(d, x='Date',title="open price",ylabel='Stock Prices')
    script,div=components(pp2)
    return render_template('result.html', script=script, div=div)
  #return render_template('result.html', result=df)
  #return render_template('result.html', result=df)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507) # start this app
