# RealTime-Market-Price-Monitoring
The code attached has the following, 

1. OPTIONS data recording

2. Real time Stock Monitoring using Google Finance(part1) and Yahoo Finance markets (part1)

Also using the fractional root-mean-square volatility we can fairly estimate that if the volatality is high, the stock prices will probably go down, giving the market brokers, 
the market entry point and market movers can capitalize on that in the initial 15 minutes given the stocks have high market cap. 
Also I have attached screenshot for POSTMAN Web Services API Tool to test the Google Finance API to get the "EL" values in after market/pre market to get the after market or pre market price.

I have run "In market" Data for the following stocks, YHOO, MTCH, TSLA, GOOG, AMZN, ADBE, AAPL, QCOM, CTXS, ZNGA.

For after hours Data, following stocks were used which were giving the "EL" Value as also can be seen in the POSTMAN RESTful API Service Tool returning raw JSON data with the headers.  
MSFT,CSCO,TSLA,GOOG,AMZN,ADBE,AAPL,QCOM,CTXS,MMM 
Also to calculate the volatality, we have used a multi dimensional list to iterate through each stocks prices to calculate the standard deviation and mean using the numpy library.

The code can be tweaked to be used across markets in major exchanges across the world. Output files shared are one for after hours and in market hours. Similarly Pre Market hours can be calculate.

At any point, you just need to do Ctrl +C to exit the code if running from the terminal/cmd (Anaconda).
