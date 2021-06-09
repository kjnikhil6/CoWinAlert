import os
import os
import pickle
import requests
import smtplib, ssl
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   

from dotenv import load_dotenv
project_folder = os.path.expanduser('/home/fl/CoWinAlert')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


#PINCODES=os.getenv('PINCODEs')
PINCODES=os.environ.get('pincodes')
EMAIL_ID = os.environ.get('EMAIL_ID')
EMAIL_PASS=os.environ.get('EMAIL_PASS')
RECEIVER_MAIL=os.environ.get('RECEIVR_mailid_1')
RECEIVER_NOS=os.environ.get('RECEIVR_NOS')#add more by seperating with comma
FAST2SMS_AUTH=os.environ.get('FAST2SMS_AUTH')
###############
SearchByPin = '''//*[@id="mat-tab-label-0-1"]/div'''
SearchText = '''//*[@id="mat-input-0"]'''
Search = '''//*[@id="mat-tab-content-0-1"]/div/div[1]/div/div/button'''
location='./div/div/div[1]/div/h5'
slots='./div/div/div[2]/ul/li'

TextAvailable1='''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div[7]/div/div/div/div'''

TextAvailable00 = '''/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div/p'''
TextAvailable01="/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div[4]/div/p"    
NotAvailable1 = 'No Vaccination center is available for booking.'
NotAvailable2="Currently there are no centers available for this day. Please check again in few hours."



#####################


def SendMail(msg="Sitil keri nokk kutta"):
    port = 587#465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = EMAIL_ID  # Enter your address
    receiver_email = RECEIVER_MAIL  # Enter receiver address
    password = EMAIL_PASS
    message = f"Subject: Alert\n\n{msg}"

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print('Mail SEnt')
            return 'Mail Send Successfully'
    except Exception as e:
        print(e)
        return(str(e))



def SMS(msg="Sitil keri nokk kutta"):
        url = "https://www.fast2sms.com/dev/bulk"
        my_data = {
     # Your default Sender ID
    'sender_id': 'FSTSMS', 
    
     # Put your message here!
    'message': msg, 
    
    'language': 'english',
    'route': 'p',
    
    # You can send sms to multiple numbers
    # separated by comma.
    'numbers': RECEIVER_NOS 
}
        headers = {
        'authorization': FAST2SMS_AUTH,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST",
                            url,
                            data = my_data,
                            headers = headers)
        returned_msg = json.loads(response.text)
        return returned_msg['message'][0]


####################################



def Click(Xpath,browser):
    element_present = EC.presence_of_element_located((By.XPATH, Xpath))
    WebDriverWait(browser, 40).until(element_present)
    browser.find_element_by_xpath(Xpath).click()
def Type(Xpath,browser,value=""):
    element_present = EC.presence_of_element_located((By.XPATH, Xpath))
    WebDriverWait(browser, 20).until(element_present)
    browser.find_element_by_xpath(Xpath).send_keys(value)
def ContentText(Xpath0,Xpath1,Xpath3,browser):
    try:
    	
    	
    	try:
    		#element_present = EC.presence_of_element_located((By.XPATH,Xpath0))
    		#WebDriverWait(browser, 10).until(element_present)#No Vaccination center is available for booking.
    		content= browser.find_element_by_xpath(Xpath0).get_attribute('textContent')
    		print(content)
    		return 0
    	except:
    		#element_present = EC.presence_of_element_located((By.XPATH,Xpath1))
    		#WebDriverWait(browser,4).until(element_present)#Currently there are no centers available for this day.........
    		content= browser.find_element_by_xpath(Xpath1).get_attribute('textContent')
    		print(content)
    		return 0
        	

    except:
    	print("gotnew")
    	try:
    		element_present = EC.presence_of_element_located((By.XPATH,Xpath3))
    		WebDriverWait(browser, 20).until(element_present)
    		content= browser.find_elements_by_xpath(Xpath3)#.get_attribute('textContent')
    		print(content)
    		print("lv2")
    		return content
    	except:
    		print("error123")
    		return 0

def check_MailSent(pincode,LOC_NAME,DATE,VaccNAME,AgeGroup,D1,D2):
	with open('data.pkl', 'rb') as f:
		prevData = pickle.load(f)
	try:
		_=prevData[pincode][LOC_NAME][DATE][VaccNAME][AgeGroup]
		#if sts == 1:
			#Save(pincode,LOC_NAME,DATE,VaccNAME,AgeGroup,D1,D2,mailSTS=O)#change sts
		return True
	except:
		Save(pincode,LOC_NAME,DATE,VaccNAME,AgeGroup,D1,D2)
		return False
		
def check_BOOKED(slot):
    d1d2=  './div/a'
    try:
        sts=slot.find_element_by_xpath(d1d2)
        if sts.get_attribute('textContent') == 'Booked':
        	return True
    except NoSuchElementException:
        return False

def Save(pincode,locName,date,VaccNAME,AgeGrp,D1,D2):
	with open('data.pkl', 'rb') as f:
		myData=pickle.load(f)
	with open('data.pkl', 'wb') as f:
		myData[pincode]=myData.get(pincode,{})
		myData[pincode][LOC_NAME]=myData[pincode].get(LOC_NAME,{})
		myData[pincode][LOC_NAME][DATE]=myData[pincode][LOC_NAME].get(DATE,{})
		myData[pincode][LOC_NAME][DATE][VaccNAME]=myData[pincode][LOC_NAME][DATE].get(VaccNAME,{})
		myData[pincode][LOC_NAME][DATE][VaccNAME][AgeGroup]=myData[pincode][LOC_NAME][DATE][VaccNAME].get(AgeGroup,[D1,D2])
		#mailSTS=1 =>sendSend
		pickle.dump(myData,f)
	return myData
import requests
import smtplib, ssl
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
project_folder = os.path.expanduser('/home/fl/CoWinAlert')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


PINCODES=os.getenv('PINCODEs')

EMAIL_ID = os.getenv('EMAIL_ID')
EMAIL_PASS=os.getenv('EMAIL_PASS')
RECEIVER_MAIL=os.getenv('RECEIVR_mailid_1')
RECEIVER_NOS=os.getenv('RECEIVR_NOS')#add more by seperating with comma
FAST2SMS_AUTH=os.getenv('FAST2SMS_AUTH')

def SendMail(msg="Time to book for Vaccine"):
    port = 587#465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = EMAIL_ID  # Enter your address
    receiver_email = RECEIVER_MAIL  # Enter receiver address
    password = EMAIL_PASS
    message = f"Subject: Alert\n\n{msg}"

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print('Mail SEnt')
            return 'Mail Send Successfully'
    except Exception as e:
        print(e)
        return(str(e))



def SMS(msg="Time to book for Vaccine"):
        url = "https://www.fast2sms.com/dev/bulk"
        my_data = {
     # Your default Sender ID
    'sender_id': 'FSTSMS', 
    
     # Put your message here!
    'message': msg, 
    
    'language': 'english',
    'route': 'p',
    
    # You can send sms to multiple numbers
    # separated by comma.
    'numbers': RECEIVER_NOS 
}
        headers = {
        'authorization': FAST2SMS_AUTH,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST",
                            url,
                            data = my_data,
                            headers = headers)
        returned_msg = json.loads(response.text)
        return returned_msg['message'][0]


####################################







def Click(Xpath,browser):
    element_present = EC.presence_of_element_located((By.XPATH, Xpath))
    WebDriverWait(browser, 40).until(element_present)
    browser.find_element_by_xpath(Xpath).click()
def Type(Xpath,browser,value=""):
    element_present = EC.presence_of_element_located((By.XPATH, Xpath))
    WebDriverWait(browser, 20).until(element_present)
    browser.find_element_by_xpath(Xpath).send_keys(value)
def ContentText(Xpath0,Xpath1,Xpath3,browser):
    try:
    	
    	
    	try:
    		element_present = EC.presence_of_element_located((By.XPATH,Xpath0))
    		WebDriverWait(browser, 20).until(element_present)
    		content= browser.find_element_by_xpath(Xpath0).get_attribute('textContent')
    		print(content)
    		print("lv1")
    		return content
    	except:
    		element_present = EC.presence_of_element_located((By.XPATH,Xpath1))
    		WebDriverWait(browser, 20).until(element_present)
    		content= browser.find_element_by_xpath(Xpath1).get_attribute('textContent')
    		print(content)
    		print("lv2")
    		return content
        	

    except:
    	print("gotnew")
    	try:
    		element_present = EC.presence_of_element_located((By.XPATH,Xpath3))
    		WebDriverWait(browser, 20).until(element_present)
    		content= browser.find_element_by_xpath(Xpath3).get_attribute('textContent')
    		print(content)
    		print("lv2")
    		return content
    	except:
    		print("error123")
    		return 0

