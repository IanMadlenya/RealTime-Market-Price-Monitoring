##***** beginning of python code *****
import urllib2 # works fine with Python 2.7.9 (not 3.4.+)
import json
import time
import os, re, csv
import datetime
import numpy

# Pre Market and Post Market work fairly similar as per the deprecated
# Google Finance API. The variable elt and el are available only during
# after market hours and pre market hours.
# But instances where the stock doesn't have any pre market or post market 
# Activity, I have made a exception where it will just take the last traded
# time i.e last day or current day's 4pm trade price depending on the 
# current timestamp.
# eg. on 23rd November - WMT didn't have a after hours trade and hence elt
# was not found.
# I also tested this on the Postman Webservice API Calls attached is the screenshot
# Also this code can be used for stock exchanges all over the world.
# Although Google Finance Data is Real Time in comparison to Yahoo's 15 min
# Lag, working with a Deprecated API and concrete documentation, expanding to
# other exchanges could require some tweaking depending on the times when the
# trading hours and after/pre trading hours in that country/exchange

def fetchPreMarket(symbol, exchange):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s:%s" % (exchange, symbol)
    u = urllib2.urlopen(url)
    content = u.read()
    data = json.loads(content[3:])
    info = data[0]
    # If the company is not traded in after or pre market
    # Hence use Try except to avoid run time errors
    # If After/Pre Market Trade Exists
    try:
        t = str(info["elt"]) # time stamp
        l = float(info["l"]) # close price 
        p = float(info["el"]) # stock price in pre-market 
        return (t,l,p)
    # If NO Pre/After Market Trade
    except:
        t = str(info["lt"])
        l = float(info["l"]) # close price (previous trading day)
        p = float(info["l"]) # stock price in pre-market (after-hours)
        return (t,l,p)

# Fetch Market Data during Trading hours - 9.30 am to 4.30 pm
# THE HTTP 1.1 request sent to the Google Finance API with the q (query)
# Parameter returns back a JSON object which can be loaded using the json
# Model and fetch the last traded Time and Price.
# The Format is checked using POST MAN Tool for testing Web Services
# with HTTP Status 200 OK, with NO-CACHE , NO-STORE , MUST-REVALIDATE,
# PROXY-REVALIDATE conditions signifying, that we cannot store it in the user
# Cache and that for every new HTTP request, you'll get back a refreshed new response.

def fetchMarket(symbol, exchange):
    link = "http://finance.google.com/finance/info?client=ig&q="
    url = link+"%s:%s" % (exchange, symbol)
    u = urllib2.urlopen(url)
    content = u.read()
    data = json.loads(content[3:])
    info = data[0]
    t = str(info["ltt"]) # time stamp
    p = float(info["l"]) # close price (previous trading day)
    return (t,p)


# Main Function
# Logic Loop for running which function where
# Depending on Time of the day
# Setting your Time Zone to New York 

if __name__ == "__main__":
 # display time corresponding to your location
    print(time.ctime())

    #Used Stocks during Market Time 9.30PM - 4.00PM
    # YHOO MTCH TSLA GOOG AMZN ADBE AAPL QCOM CTXS ZNGA

    #Used During After Hours 4.00 -4.30pm
    # MICROSOFT, CISCO, TESLA, GOOGLE, AMAZON, APPLE, ADOBE, QUALCOMM, CITRIX, 3M Stocks Chosen
    
    symbol_list = ['MSFT','CSCO','TSLA','GOOG','AMZN','ADBE','AAPL','QCOM','CTXS','MMM']
    
    # Set local time zone to NYC
    os.environ['TZ']='America/New_York'
    t=time.localtime() # string
    
    p0 = 0

    # Initialize Colums for Writing to CSV
    column_names = ['time_stamp']
    for symbol in symbol_list:
        column_names.append(symbol)

    # Open File for Writing
    f = open('part2.csv','a') 
    print ','.join(column_names)
    f.write(','.join(column_names)+'\n')
    f.flush()

    #Data Row for Prices
    data_row = []

    #Load volatility
    volatility = []

    #Actual volatility
    ackvolatility = []

    #SuperList MultiDimensional List
    superlist =[]

    #Stockwise volatility Calulation
    stockVol =[]

    # Multi Dimension List

    #Keep Running until for every 60 seconds
    while True:
        t=time.localtime()

        #Set to a Dummy to get the Listed Current Time
        #If it is between 9-9.30, 9.30-4pm, 4-4.30pm and beyond

        if( t.tm_hour ==9):
            if (t.tm_min) <30:
                data_row.append(str(fetchpreMarket('MSFT','NASDAQ')[0]))
            else:
                data_row.append(str(fetchMarket('MSFT','NASDAQ')[0]))
        
        if (t.tm_hour>9 and t.tm_hour<16):  
            data_row.append(str(fetchMarket('MSFT','NASDAQ')[0]))

        if (t.tm_hour==16):
            if (t.tm_min < 31):
                data_row.append(str(fetchpreMarket('MSFT','NASDAQ')[0]))
            else:
                pass
           
        #Calculate the Price and Volatility 
        for stock in symbol_list:
            t=time.localtime()
            # Before Trading Hours Before 9 am.
            if (t.tm_hour<9):
                print("STOCK Exchange is Not ACTIVE Now")
            # Pre Market Hours - 9.00 am t0 9.30 am
            elif (t.tm_hour==9):
                if (t.tm_min < 30):
                    t, l, p = fetchPreMarket(stock,"NASDAQ")
                    if(p!=p0):
                        p0 = p
                        print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,(p/l-1)*100.))
               
                        #Append to volatility
                        volatility.append(p);

                        #Append Time Stamp and Price 
                        data_row.append(str(p))
                
                else:
                    # Time from 9.30 am - 9.59 am
                    t, p = fetchMarket(stock,"NASDAQ")
                    if(p!=p0):
                        p0 = p
                        print("%s\t%.2f" % (t, p))
                         
                        #Append Price 
                        data_row.append(str(p))
 
            # Normal Market Hours 9.30 am to 4pm
            elif (t.tm_hour>9 and t.tm_hour<16):
                t, p = fetchMarket(stock,"NASDAQ")
                if(p!=p0):
                    p0 = p
                    print("%s\t%.2f" % (t, p))

                    #Append Price 
                    data_row.append(str(p))

            # After Hours Market Data from 4.00 pm - 4.30 pm
            elif (t.tm_hour==16):
                if (t.tm_min < 30):
                    t, l, p = fetchPreMarket(stock,"NASDAQ")
                    
                    print("%s\t%.2f\t%.2f\t%+.2f\t%+.2f%%" % (t, l, p, p-l,(p/l-1)*100.))
                    
                    #Append Price 
                    data_row.append(str(p))
                    
                # If the Time is after 4.30 -5.00 PM    
                else:
                    print("STOCK Exchange is Not ACTIVE Now")
            # If the Time is after 5.00 PM
            elif (t.tm_hour>16):
                print("STOCK Exchange is Not ACTIVE Now")
        
        superlist.append(volatility);

        #Write to the File
        f.write(','.join(data_row)+'\n')

        #Clear the Data_Row
        data_row = []

        #Calculate Volatality
        t=time.localtime()
        if (t.tm_hour==9 and t.tm_min == 30):
            #Write it to the File
            for j in range(len(symbol_list)):
                for i, value in enumerate(superlist):
                    stockVol.append(superlist[i][j])

                #Calculate the Fractional Rootmean Square Volatility
                std = numpy.std(stockVol, axis =0)
                mean = numpy.mean(stockVol, axis=0)
                ackvolatility.append(std/mean)

            print "volatility is", ackvolatility
            #Print volatility
            f.write(str(ackvolatility) + '\n')
            ackvolatility = []

        #Sleep for 1 minute , Check every minute
        time.sleep(60)
    #Close the File
    f.close()
    
