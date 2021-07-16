import os
##function0-choose function
def choose():
    fnum = input('Please enter the function you want to access(Exit -- "quit"): (1-stock price/2-airnow) ')
    if fnum=="1":
        stocks()
    elif fnum=="2":
        main()
    elif fnum=="quit":
        os._exit(0)    
    else: 
        print("You have entered the wrong number!")
##function1-stockprice

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def stocks(): 
 stockcode = input('Please enter the stockname(US)(Reselect the function --"return"// Exit -- "quit"): ')
 if stockcode=="return": 
     choose()
 elif stockcode=="quit":
     os._exit(0)
 else:
  try:
   url="https://www.futunn.com/stock/"+stockcode+"-US"
   page=urlopen(url)
   soup = BeautifulSoup(page,"lxml")
   list1=str(soup.find_all(class_='stock-price'))
   list2=re.findall(r">(.+?)<", list1)
   print("The stock code is "+stockcode+", and the price is "+list2[0]+" $.")
   stocks()
  except:
   print('Please enter valid zipcode')
   stocks()
##function2-airnow
def main():
    zipcode = input('Please enter the zipcode(Reselect the function --"return"// Exit -- "quit"): ')
    if zipcode=="return": 
     choose()
    elif zipcode=="quit":
     os._exit(0)
    else:
     date=input('Please enter the date: YYYY-MM-DD(Reselect the function --"return"// Exit -- "quit"): ')
     if date=="return": 
      choose()
     elif date=="quit":
      os._exit(0)
     else:
      try:
       BaseURL="https://www.airnowapi.org/aq/forecast/zipCode/"
       URLPost = {'format': 'application/json',
               'zipCode':zipcode,
               'date': date,
               'distance': '5',
               'API_KEY': '3FF488E8-B96E-4370-8F70-XXXXXXXX'
                    }              
                    
    
       UseRequest(BaseURL, URLPost) 
      except:
          print("You entered the wrong zip code (or date)!")
          main()
def UseRequest(BaseURL, URLPost):
    #Uses request library
    import requests
    import pandas as pd
    response=requests.get(BaseURL, URLPost)
    jsontxt = response.json()
    data = {'City':[],
            'Date':[],
            'AQIType':[],
            'AQIValue':[]}#creat an empty dataframe
    data=pd.DataFrame(data)
    for list in jsontxt:
            AQIType = list['ParameterName']
            City=list['ReportingArea']
            AQIValue=list['AQI']
            Date=list['DateForecast']
            data = data.append({'City':City,
                                'Date':Date,
                                'AQIType':AQIType,
                                'AQIValue':AQIValue},ignore_index=True)#add a new row into dataframe
            print("For Location ", City, " the AQI for ", AQIType, "is ", AQIValue," on ",Date ,".\n")#print readable output in console
    print(data)
    data.to_csv("Part2_OUTFILE.txt", sep=',',mode="a",index=None)#save to txt
    print("The output has been saved to Part2_OUTFILE.txt.")  
    main()
choose()
 
