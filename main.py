
from flask import Flask

from selenium.webdriver.chrome.options import Options

from func import *
import pickle
from selenium import webdriver
#from selenium.common.exceptions import TimeoutException

import time




SearchByPin='''//*[@id="mat-tab-label-0-1"]/div'''
SearchText='''//*[@id="mat-input-0"]'''
Search='''//*[@id="mat-tab-content-0-1"]/div/div[1]/div/div/button'''

#TextAvailable2='''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]'''
#TextAvailable1='''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div'''
TextAvailable0='''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div/p'''
NotAvailable='No Vaccination center is available for booking.'


def ComapareText(pincode,Content):
  with open('data.pkl','r+b') as f:
    myData=pickle.load(f)
    Prev_Val=myData.get(pincode)
    if Prev_Val:#pincode exist
      if Content == Prev_Val:
        print('NOchange')
        return 0
      else:#change detected
        myData[pincode]=Content
        pickle.dump(myData, f)
        return 1
    else:#make slot 
      myData[pincode]=Content
      pickle.dump(myData, f)
      return 0
################################

chrome_options = Options()
chrome_options.headless=True
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)


app = Flask('app')

@app.route('/')
def hello_world():
  browser.get('https://www.cowin.gov.in')
  Click(SearchByPin,browser)
  time.sleep(1)
  for pincode in PINCODES.split(","):

    print(pincode)
    
    Type(SearchText,browser,value=pincode)
    print(2)
    Click(Search,browser)
    time.sleep(1)
    print(3)
    Content=ContentText(TextAvailable0,browser)
    print(Content)
    change=ComapareText(pincode,Content)
    print(change)
    if change:
      if Content!=NotAvailable:
        status=SMS()
        #SendMail()
        print(status)                                 
    # else:#print no change
    #   #staus=SMS(msg="no cahnge mwone")
    #   print(staus)
  browser.quit()
  with open('counter.pkl','rb') as f:
    count=pickle.load(f)
  print(count)
  with open('counter.pkl', 'wb') as f:
    count+=1
    pickle.dump(count, f)

    return str(count)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

# mydata={'678601':'No Vaccination center is available for booking.'}
# with open('data.pkl', 'wb') as f:
#   pickle.dump(mydata, f)
#count=0

# with open('counter.pkl', 'wb') as f:
#   pickle.dump(count, f)