"""
Author: FellowBeginner, arunkumar-js25
Blog: https://fellowbeginners.wordpress.com/

Automation Script: Create groups in partner organisations in CPQ instance
Application: Oracle CPQ
IDE: Python-Selenium

Prerequisite:
Account User: Admin access with ProxyLogin
"""
from oracle_cpq_ui_automation.partner_orgs import createPartnersGroups
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class oracle_cpq_ui_automation:
    def __init__(self,cpqInstanceName, username, password):
        self.cpqInstanceName = cpqInstanceName
        self.username = username
        self.password = password

    def launchChrome(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=opt)
        #driver = webdriver.Chrome(chromedriverPath)
        driver.implicitly_wait(1)
        driver.maximize_window()
        self.driver = driver
        time.sleep(5)

    def login(self):
        self.driver.get("https://" + self.cpqInstanceName + ".bigmachines.com/")
        time.sleep(3)
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "psword").send_keys(self.password)
        self.driver.find_element(By.ID, "log_in").click()
        time.sleep(5)

    def createGroupsinPartnerOrg(self, groupsToCreate=[], exceptionListOfCompanies=[], noOfPagesToSkip=-1):
        '''Inputs:
        driver = launchChrome()
        cpqInstanceName = ""
        username = ""
        password = ""
        groupsToCreate = [["Partner User","partnerUser",True],["Partner User","partnerUser"],["Partner User","partnerUser","t"]]
        exceptionListOfCompanies = []  # Array of strings
        noOfPagesToSkip =-1
        '''
        createPartnersGroups(self.driver, self.cpqInstanceName, groupsToCreate, exceptionListOfCompanies, noOfPagesToSkip)

#if __name__=="__main__":
    #main = oracle_cpq_ui_automation("<companySiteName>","<username>","<password>")
    #main.launchChrome()
    #main.login()
    #main.createGroupsinPartnerOrg([["Partner User","partnerUser",True]],[],-1)