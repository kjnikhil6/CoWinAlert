import os
import requests
import smtplib, ssl
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


PINCODES=os.environ['PINCODEs']
EMAIL_ID = os.environ['EMAIL_ID']
EMAIL_PASS=os.environ['EMAIL_PASS']
RECEIVER_MAIL=os.environ['RECEIVR_mailid_1']
RECEIVER_NOS=os.environ['RECEIVR_NOS']#add more by seperating with comma
FAST2SMS_AUTH=os.environ['FAST2SMS_AUTH']

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
def ContentText(Xpath0,browser):
    try:
        element_present = EC.presence_of_element_located((By.XPATH,Xpath0))
        WebDriverWait(browser, 20).until(element_present)
        content= browser.find_element_by_xpath(Xpath0).get_attribute('textContent')
        print(content)
        print(len(content))
        return content

    except:
        return 1

