from flask import (Flask,render_template,
                    redirect,url_for, make_response,
                    request)
from flaskext.mysql import MySQL
import json
import collections
import requests
from yahoo_finance import Share
from datetime import datetime, timedelta

app = Flask(__name__)
start = datetime.now()
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'portfolio'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def get_cookie_data():
    try:
        data = json.loads(request.cookies.get('stockData'))
    except TypeError:
        data = {}
    return data

def get_date(dateFormat="%Y-%m-%d", addDays=0):

    timeNow = datetime.now()
    if (addDays!=0):
        anotherTime = timeNow - timedelta(days=addDays)
    else:
        anotherTime = timeNow

    return anotherTime.strftime(dateFormat)


@app.route('/')
def index():
    data = get_cookie_data()
    return render_template("index.html", saves=data)
    
def ethical():
    #0. Ethical Investing
    start_date = datetime.now()   
    end_date = start.strftime("%Y-%m-%d")
    print end_date
    addDays = 7 #days
    output_format = '%Y-%m-%d'
    start_date = get_date(output_format, addDays)
    print start_date
    

    conn = mysql.connect()
    cursor = conn.cursor()
    query_string = "SELECT ticker from EthicalStrategy" 
    cursor.execute(query_string)

    #1.have a list of stocks with risk
    stockstoPull = cursor.fetchall()
    print stockstoPull

    for stocksymbol in stockstoPull:
    # Retrieve finance data from yahoo api
        print stocksymbol[0]
        yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+stocksymbol[0]+'%22)&format=json&env=http://datatables.org/alltables.env'
          
        response = requests.get(yahoo_url)
        query = json.loads(response.text.decode("utf8"))['query']
       
        # Finance data
        stockdata = query['results']['quote']
            
        add_stockdata = ("insert into StockInfo (Symbol, BookValue, DivShare, DivYield, EarningsShare, LastTradePrice, PERatio, PEGRatio, CompName) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_values = (stockdata['Symbol'], stockdata['BookValue'], stockdata['DividendShare'], stockdata['DividendYield'], stockdata['EarningsShare'], stockdata['LastTradePriceOnly'], stockdata['PERatio'], stockdata['PEGRatio'], stockdata['Name'])

        cursor.execute(add_stockdata, data_values)
        conn.commit()
        json.loads(response.text.decode("utf8"))['query'] = None
   
    cursor2 = conn.cursor()
    q = "SELECT Symbol, CompName, LastTradePrice,PEGRatio, PERatio from portfolio.StockInfo WHERE 0.8 < PEGRatio and PEGRatio<= 1.5"
    
    rows=""
    cursor2.execute(q)
    rows = cursor2.fetchall()
    print "Ethical Investing strategy suggests the following stocks:\n"
    print rows
    

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['symbol'] = row[0]
        d['ticker'] = row[1]
        d['stockprice'] = row[2]
        stock = Share(row[0])
        closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]

        if(float(row[4])>50):
            d['per']=20
        elif float(row[4])<25 and float(row[4])>0:
            d['per']=45
        else:
            d['per']=35
        
        d['time'] = closes
        #d['per'] = 33
        objects_list.append(d)
        print d['per']
        
    j = json.dumps(objects_list)
    return j

def valuein():
    cnx = mysql.connect()
    cursor1 = cnx.cursor()

    start_date = datetime.now()   
    end_date = start.strftime("%Y-%m-%d")
    print end_date
    addDays = 7 #days
    output_format = '%Y-%m-%d'
    start_date = get_date(output_format, addDays)
    print start_date
    stockstoPull = ['ADBE', 'BANC', 'MSFT', 'TM', 'NCT', 'GOOGL', 'GM', 'AMZN', 'AAPL']

    for stocksymbol in stockstoPull:
        # Retrieve finance data from yahoo api
        yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+stocksymbol+'%22)&format=json&env=http://datatables.org/alltables.env'
        response = requests.get(yahoo_url)
        query = json.loads(response.text.decode("utf8"))['query']
           
        # Finance data
        stockdata = query['results']['quote']
            
        add_stockdata = ("insert into StockInfo (Symbol, BookValue, DivShare, DivYield, EarningsShare, LastTradePrice, PERatio, PEGRatio, CompName) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_values = (stockdata['Symbol'], stockdata['BookValue'], stockdata['DividendShare'], stockdata['DividendYield'], stockdata['EarningsShare'], stockdata['LastTradePriceOnly'], stockdata['PERatio'], stockdata['PEGRatio'], stockdata['Name'])

        cursor1.execute(add_stockdata, data_values)
        cnx.commit()
        json.loads(response.text.decode("utf8"))['query'] = None

    print "\nStock information of 10 companies added to database successfully!\n"
            
    cursor2 = cnx.cursor()
    cursor2.execute("select Symbol, CompName,LastTradePrice,PEGRatio,PERatio from StockInfo WHERE LastTradePrice < BookValue*1.5 and EarningsShare > DivShare*2 and DivYield > 3 and 0 < PEGRatio < 1.1")
    cnx.commit()
    rows = cursor2.fetchall()

    print "Value Investing strategy suggests the following stocks:\n"
    for row in rows:
         print row[1]+" ("+row[0]+")"

    cursor3 = cnx.cursor()
    cursor3.execute("DELETE from StockInfo")
    cnx.commit()
    cursor1.close()
    cursor2.close()
    cursor3.close()
    cnx.close() 
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['symbol'] = row[0]
        d['ticker'] = row[1]
        d['stockprice'] = row[2]
        stock = Share(row[0])
        closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]
        d['time'] = closes
        if(float(row[4])<4):
            d['per']=50
        elif float(row[4])<6 and float(row[4])>4:
            d['per']=30
        else:
            d['per']=20
        
        objects_list.append(d)
        
    j = json.dumps(objects_list)
    return j    

def growth():
    objects_list = []
    start_date = datetime.now()   
    end_date = start.strftime("%Y-%m-%d")
    print end_date
    addDays = 7 #days
    output_format = '%Y-%m-%d'
    start_date = get_date(output_format, addDays)
    print start_date

    stockstoPull = ['ADBE', 'BANC', 'MSFT', 'TM', 'HCI', 'NCT', 'GOOGL', 'GM', 'AMZN', 'AAPL']

    for stocksymbol in stockstoPull:
        # Retrieve finance data from yahoo api
        yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+stocksymbol+'%22)&format=json&env=http://datatables.org/alltables.env'
        response = requests.get(yahoo_url)
        query = json.loads(response.text.decode("utf8"))['query']
           
        # Finance data
        stockdata = query['results']['quote']
    
        multiple = float(stockdata['EPSEstimateNextYear']) / float(stockdata['EPSEstimateCurrentYear'])

        growth = ( (multiple ** .5) - 1 ) * 100
    
        if (growth > 10):
            print growth
            print stockdata['Name']
            d = collections.OrderedDict()
            d['symbol'] = stockdata['Symbol']
            d['ticker'] = stockdata['Name']
            d['stockprice'] = stockdata['LastTradePriceOnly']
            stock = Share(stockdata['Symbol'])
            closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]
            d['time'] = closes
            d['per'] = 33.33
            objects_list.append(d)
    j = json.dumps(objects_list)
    return j

def indexing():
    objects_list = []
    start_date = datetime.now()   
    end_date = start.strftime("%Y-%m-%d")
    print end_date
    addDays = 7 #days
    output_format = '%Y-%m-%d'
    start_date = get_date(output_format, addDays)
    print start_date    

    # 1.Fetch US Stock ETFs
    conn = mysql.connect()
    cursor = conn.cursor()
    # Take the use entered amount
    amount = 1000000
    if (amount >= 100000):
        query_string = "SELECT ticker_id,ticker_name FROM IndexStrategy WHERE type = '{type}'".format(type=1)  
        cursor.execute(query_string)
    else:
        query_string = "SELECT ticker_id,ticker_name FROM IndexStrategy WHERE type = '{type}'".format(type=2)  
        cursor.execute(query_string)
    rows = cursor.fetchall()
    #print rows    
    max_profit = 0;
    max_profit_ticker = ""    
    for row in rows:
        # Retrieve finance data from yahoo api
        print (str(row[0])) + row[1] + "\n\n"
        if(row[0] > max_profit):
            max_profit = row[0]
            max_profit_ticker = row[1]
    # Fetch the current data from Yahoo finance
    yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+max_profit_ticker+'%22)&format=json&env=http://datatables.org/alltables.env'
    stock = Share(max_profit_ticker)
    closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]     
    response = requests.get(yahoo_url)
    query = json.loads(response.text.decode("utf8"))['query']
    stockdata = query['results']['quote']
    print stockdata
    # Create a JSON Object to send in the response object    
    d = collections.OrderedDict()
    d['symbol'] = stockdata['Symbol']
    d['ticker'] = stockdata['Name']
    d['stockprice'] = stockdata['LastTradePriceOnly']
    d['time'] = closes
    d['per'] = 34
    objects_list.append(d) 
    
    # 2.Fetch International Stock ETFs
    if (amount >= 100000):
        query_string = "SELECT ticker_id,ticker_name FROM IndexStrategy WHERE type = '{type}'".format(type=3)  
        cursor.execute(query_string)
    else:
        query_string = "SELECT ticker_id,ticker_name FROM IndexStrategy WHERE type = '{type}'".format(type=4)  
        cursor.execute(query_string)
    rows = cursor.fetchall()
    #print rows    
    max_profit = 0;
    max_profit_ticker = ""    
    for row in rows:
        # Retrieve finance data from yahoo api
        print (str(row[0])) + row[1] + "\n\n"
        if(row[0] > max_profit):
            max_profit = row[0]
            max_profit_ticker = row[1]
    # Fetch the current data from Yahoo finance
    yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+max_profit_ticker+'%22)&format=json&env=http://datatables.org/alltables.env'
    stock = Share(max_profit_ticker)
    closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]  
    response = requests.get(yahoo_url)
    query = json.loads(response.text.decode("utf8"))['query']
    stockdata = query['results']['quote']

    # Create a JSON Object to send in the response object    
    d = collections.OrderedDict()
    d['symbol'] = stockdata['Symbol']
    d['ticker'] = stockdata['Name']
    d['stockprice'] = stockdata['LastTradePriceOnly']
    d['time'] = closes
    d['per'] = 34
    objects_list.append(d)      
    
    # 3.Fecth international bonds
    query_string = "SELECT ticker_id,ticker_name FROM IndexStrategy WHERE type = '{type}'".format(type=5)  
    cursor.execute(query_string)
    rows = cursor.fetchall()
    #print rows    
    max_profit = 0;
    max_profit_ticker = ""    
    for row in rows:
        # Retrieve finance data from yahoo api
        print (str(row[0])) + row[1] + "\n\n"
        if(row[0] > max_profit):
            max_profit = row[0]
            max_profit_ticker = row[1]
    # Fetch the current data from Yahoo finance
    yahoo_url =  'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(%22'+max_profit_ticker+'%22)&format=json&env=http://datatables.org/alltables.env'
    stock = Share(max_profit_ticker)
    closes = [c['Close'] for c in stock.get_historical(start_date, end_date)]  
    response = requests.get(yahoo_url)
    query = json.loads(response.text.decode("utf8"))['query']
    stockdata = query['results']['quote']

    # Create a JSON Object to send in the response object    
    d = collections.OrderedDict()
    d['symbol'] = stockdata['Symbol']
    d['ticker'] = stockdata['Name']
    d['stockprice'] = stockdata['LastTradePriceOnly']
    d['time'] = closes
    d['per'] = 34
    objects_list.append(d)     
    
    j = json.dumps(objects_list)    
    return j


    
@app.route('/fetchInfo', methods=["POST"])
def fetchInfo():
    print (request.form)
    amount=int(request.form['amount'])
    print amount

    strategy = request.form['strategy']
    print strategy
    
    if strategy=='ethical':
        j = ethical()
    elif strategy=='index':
        j = indexing()
    elif strategy=='valuein':
        j=valuein()
    elif strategy=='growth':
        j=growth()
    else:
        print "No strategy"
    
    conn = mysql.connect()
    cursor3 = conn.cursor()
    cursor3.execute("DELETE from StockInfo")
    conn.commit()
    cursor3.close()
    conn.close()

    response = make_response()

    #response.set_cookie('stockData', calculatedData)
    return render_template("result.html", saves=j)

app.run(debug=True, port=8000, host='0.0.0.0')

