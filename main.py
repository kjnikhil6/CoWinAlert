import pickle
import time
from selenium.webdriver.chrome.options import Options
from func import *
from selenium import webdriver



##############
SearchByPin = '''//*[@id="mat-tab-label-0-1"]/div'''
SearchText = '''//*[@id="mat-input-0"]'''
Search = '''//*[@id="mat-tab-content-0-1"]/div/div[1]/div/div/button'''

TextAvailable1='''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div[7]'''
TextAvailable00 = '''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div/p'''
TextAvailable01="/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div/p"
          
NotAvailable1 = 'No Vaccination center is available for booking.'
NotAvailable2="Currently there are no centers available for this day. Please check again in few hours."
############333             
def ComapareText(pincode, Content):
    with open('data.pkl', 'r+b') as f:
        myData = pickle.load(f)
        f.seek(0)
        Prev_Val = myData.get(pincode)
        if Prev_Val:  #pincode exist
            if Content == Prev_Val:
                print('same preval')
                return 0
            else:  #change detected
                myData[pincode] = Content
                print(myData)
                pickle.dump(myData, f)
                return 1
        else:  #make slot
            myData[pincode] = Content
            pickle.dump(myData, f)
            print('myData')
            return 0


################################


chrome_options = Options()
chrome_options.headless=True
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--remote-debugging-port=9222")
#chrome_options.add_argument("start-maximized")
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('/home/fl/Downloads/chromedriver',options=chrome_options)
browser.set_window_size(1200,600)
try:
  browser.set_page_load_timeout(60)
  browser.get('https://www.cowin.gov.in')
  Click(SearchByPin, browser)
except:
  browser.quit()
  print("page not get")

time.sleep(1)
print('starting')
for pincode in PINCODES.split(","):

  try:
    Type(SearchText, browser, value=pincode)
    Click(Search, browser)
    time.sleep(1)
    print('getting content')
    Content = ContentText(TextAvailable00,TextAvailable01,TextAvailable1, browser)
    print(Content)
    if Content==0:
    	continue   # error
    change = ComapareText(str(pincode), Content)
    print('changed',change)
    if change:
      if Content != NotAvailable1 and Content != NotAvailable2 :
        status = SMS()
                #SendMail()
        print(status)
        # else:#print no change
        #   #staus=SMS(msg="no cahnge mwone")
        #   print(staus)
  except Exception as e:
    browser.quit()
    print(e)
browser.quit()
with open('counter.pkl', 'rb') as f:
  count = pickle.load(f)
with open('counter.pkl', 'wb') as f:
  count += 1
  pickle.dump(count, f)
  print('run:',count)
if count%25 ==0:
  _= SendMail(msg='Program is Running')

# mydata={'678601':'No Vaccination center is available for booking.'}
# with open('data.pkl', 'wb') as f:
#   pickle.dump(mydata, f)
#count=0

# with open('counter.pkl', 'wb') as f:
#   pickle.dump(count, f)
