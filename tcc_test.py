#!/usr/bin/env python

##============================================================================== 
# file:                 tcc_test.py
# date:                 Tue Mar  6 18:48:04 PST 2018
# author(s):            Thalita Coleman  <thalitaneu@gmail.com>
# abstract:             Navigate to TCC website, click on selected links, 
#			and return http status codes. 
#------------------------------------------------------------------------------ 
# requirements: python 2.7 
#	 notes: set chromedriverPath variable before executing	
#------------------------------------------------------------------------------ 
##============================================================================== 


# Import required libraries
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json




# General Script Configuration
chromedriverPath= '/path/to/chromedriver'
logPath='/tmp/chromeDriver.log'
DEBUG= True


# Enable browser logging
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL' }
browser = webdriver.Chrome(executable_path=chromedriverPath, service_args=["--verbose", "--log-path=" + logPath], desired_capabilities=d)


# Navigate to main site
browser.get('http://www.taxcreditco.com')


# Make browser wait until the tab that contains services is present
services = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Services')))


# Click the "Sections" menu option
services.click()


# Make browser wait until div that contains "Discover our Services" is present
sectionDiv = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-7')))


# Locate Div with Section links, retrieve URLS for first 4 links.
sectionLinks = sectionDiv.find_elements_by_tag_name('a')



# Display links for debugging purposes only
if DEBUG == True:
	counter= 1
	for link in sectionLinks:
		l = link.get_attribute('href')
		print 'link ' + str(counter) + ': ' + str(l)

		counter += 1
	print "\n\n" 



# Place URLs to be visited in a list
sectionUrls= []
for link in sectionLinks:
	l = link.get_attribute('href')
	sectionUrls.append(l)



# Access each link and report the HTTP status code
counter = 1
for url in sectionUrls:

	# navigate to the url
	print "\n\n\nGetting URL " + str(counter) + "..."
	browser.get(url)

	# access the performance log to get HTTP status code
	performance_log = browser.get_log('performance')

	# for each log in performance log
	for logEntry in performance_log:


		messageContainer= logEntry.get('message')      #returns unicode
		messageContainer= json.loads(messageContainer) #converts to dictionary
		

		if messageContainer.get('message').get('method') == "Network.responseReceived":
			loggedUrl= str(messageContainer.get('message').get('params').get('response').get('url'))

			if loggedUrl == url:
				loggedMethod= str(messageContainer.get('message').get('method'))
				loggedStatus= str(messageContainer.get('message').get('params').get('response').get('status'))

				# display info
				print "=============================================="
				print "URL " + str(counter)
				print "URL: " + loggedUrl
				print "Status: " + loggedStatus
				print "=============================================="

	counter += 1

print "\n\nDone, sleeping for 15"
time.sleep(15)
browser.quit()
