import pickle
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pytz
from datetime import datetime as dt, timedelta

IST=pytz.timezone('Asia/Kolkata')
##############
          

from func import *		



################################




def scheduleAlert():
	chrome_options = Options()
	#chrome_options.headless=True
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--remote-debugging-port=9222")
	#chrome_options.add_argument("start-maximized")
	chrome_options.add_argument('--disable-dev-shm-usage')
	browser = webdriver.Chrome(options=chrome_options)
	browser.set_window_size(1200,600)
	try:
		browser.set_page_load_timeout(60)
		browser.get('https://www.cowin.gov.in')
		Click(SearchByPin, browser)
	except:
		browser.quit()
		print("page not loading")
	time.sleep(1)
	print('starting')
	try:
		for pincode in PINCODES.split(","):
			Type(SearchText, browser, value=pincode)
			Click(Search, browser)
			time.sleep(10)
			print('getting content')
			CONTENTS= ContentText(TextAvailable00,TextAvailable01,TextAvailable1, browser)
			if not  CONTENTS:
				continue #no slots available msg
			for content in CONTENTS:#loc,dates_slot
		
				LOC_NAME   = content.find_element_by_xpath(location).get_attribute('textContent').upper()
				DATE_SLOTS = content.find_elements_by_xpath(slots)#li
		
				for dateC,date_SLOT in enumerate(DATE_SLOTS):
		
					VacAge_TYPES=date_SLOT.find_elements_by_xpath('./div')
					if 'NA' in date_SLOT.get_attribute('textContent'):
						print('NA')
						continue
					DATE       = (dt.now(IST)+timedelta(days=dateC)).strftime('%d %b')
					for VacAge_TYPE in VacAge_TYPES:#diff vaccine fiff age group
						BOOKED=check_BOOKED(VacAge_TYPE)
						if not BOOKED:
							D1       = VacAge_TYPE.find_element_by_xpath('./div/div[1]/span[1]').get_attribute('textContent').split(' ')[1]
							D2       = VacAge_TYPE.find_element_by_xpath('./div/div[1]/span[2]').get_attribute('textContent').split(' ')[1]
							VaccNAME = VacAge_TYPE.find_element_by_xpath('./div/div[2]').get_attribute('textContent').upper()
							AgeGroup = VacAge_TYPE.find_element_by_xpath('./div/div[3]').get_attribute('textContent').upper()
							
							mailSend=check_MailSent(pincode,LOC_NAME,DATE,VaccNAME,AgeGroup,D1,D2)
							if not mailSend:
								SendMail(msg=f"PIN:{pincode}\n{LOC_NAME}\n{DATE}\n{VaccNAME}:{AgeGroup} D1:{D1} D2:{D2}")
	except:
		browser.quit()
	browser.quit()
while True:
	scheduleAlert()
	time.sleep(10)
	with open('data.pkl', 'rb') as f:
		myData=pickle.load(f)
		print(myData)
