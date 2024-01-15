"""
Author: FellowBeginner
Blog: https://fellowbeginners.wordpress.com/

Automation Script: Create groups in partner organisations in CPQ instance
Application: Oracle CPQ
IDE: Python-Selenium

Prerequisite:
Account User: Admin access with ProxyLogin

Inputs:
Driver
cpqInstanceName = "SiteName"
username = "username"
password = "password"
groupsToCreate = [ [<groupName~string>, <groupVarName~string>, <addAllUsersToGroup~boolean> ] ] #2D Array of mixed datatype
exceptionListOfCompanies = [] #Array of strings
noOfPagesToSkip = -1
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a group
def createGroup(driver, companyName, groupName, groupVarName, addAllUsers = False):
    if (len(driver.find_elements(By.XPATH,"//td[text()='" + groupVarName + "']")) == 0):
        driver.find_element(By.XPATH,"//a[@id='add']").click()
        time.sleep(5)
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "group-name|input")))
        driver.find_element(By.ID,"group-name|input").send_keys(groupName)
        time.sleep(3)
        driver.find_element(By.ID,"variable-name|input").send_keys(groupVarName)
        time.sleep(3)
        if(addAllUsers): #Click >> arrow button to add all users to the group
            driver.find_element(By.ID,"all-users-right-btn_oj2|text").click()  # select all users
            time.sleep(3)
        driver.find_element(By.ID,"save-btn_oj0|text").click()
        time.sleep(5)
        print("Group "+groupName+" added for " + companyName)
    else:
        print("Group "+groupName+" already exists for " + companyName)

# MAIN: Create Groups in all the partners
def createPartnersGroups(driver, cpqInstanceName, groupsToCreate=[], exceptionListOfCompanies=[], noOfPagesToSkip=-1):
	#Basic URL variables
	url = "https://" + cpqInstanceName + ".bigmachines.com"
	proxylogout = url + "/logout.jsp?proxy_logout=true&amp;_bm_trail_refresh_=true"

	driver.get("https://" + cpqInstanceName + ".bigmachines.com/admin/company/list_external_companies.jsp")
	time.sleep(2)

	pagesCountStr = driver.find_element(By.XPATH,"//table[3]//td[@class='bottom-bar']").text
	pagesCount = int(pagesCountStr.split(": ")[1]) // 100

	# Extract all the partner orgs available in the page
	for i in range(pagesCount + 1):
		print("pageNo :", i)

		if(i<noOfPagesToSkip):
			continue
		elif(i==noOfPagesToSkip):
			for j in range(i + 1):
				ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.CONTROL).perform()
				driver.find_element(By.ID,"next_iter_link").click()
				time.sleep(5)

		count = 1
		list_of_companies = [[x.get_attribute('href'), x.text] for x in
							 driver.find_elements(By.XPATH,"//td[1]//a[@class='list-field']")]
		list_of_companiesProxy = [x.get_attribute('href') for x in
								  driver.find_elements(By.XPATH,"//td[8]//a[@class='list-field']")]

		for company, proxyLink in zip(list_of_companies, list_of_companiesProxy):
			companyID = company[0].replace(
				"https://" + cpqInstanceName + ".bigmachines.com/admin/company/edit_external_company.jsp?id=", "")
			companyName = company[1]
			print(count, companyName)

			# Check if the partners are present in exceptionList
			if companyID not in exceptionListOfCompanies:
				# List of Users: print(url+"/admin/users/list_users.jsp?company_id="+companyID)
				# ProxyLogin: print(proxyLink)
				driver.get(proxyLink)
				time.sleep(2)
				driver.get(url + "/admin/groups/list_groups.jsp?_bm_trail_refresh_=true")
				time.sleep(2)

				for groupDetail in groupsToCreate:
					if(len(groupDetail) == 3 and type(groupDetail[0]) == str
							and type(groupDetail[1]) == str
							and type(groupDetail[2]) == bool):
						createGroup(driver, companyName, groupDetail[0], groupDetail[1], groupDetail[2])
					else:
						print("The group details ",groupDetail," are incorrect. Please retry with the format [ [<groupName~string>, <groupVarName~string>, <addAllUsersToGroup~boolean> ] ]")

				driver.get(proxylogout)
				time.sleep(5)
			else:
				print("This company " + companyName + " is in exclusion list..")

			count = count + 1

		if (count > 100):
			for j in range(i + 1):
				ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.CONTROL).perform()
				driver.find_element(By.ID,"next_iter_link").click()
				time.sleep(5)