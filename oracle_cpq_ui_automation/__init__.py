"""
Author: FellowBeginner, arunkumar-js25
Blog: https://fellowbeginners.wordpress.com/

Automation Script: Create groups in partner organisations in CPQ instance
Application: Oracle CPQ
IDE: Python-Selenium

Prerequisite:
Account User: Admin access with ProxyLogin
"""
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

''' Custom Modules '''
from oracle_cpq_ui_automation.partner_orgs import createPartnersGroups
from oracle_cpq_ui_automation.bmllib import BmlLibrary

class oracle_cpq_ui_automation:
    def __init__(self,cpqInstanceName, username, password):
        self.cpqInstanceName = cpqInstanceName
        self.username = username
        self.password = password
        self._cpq_instance_url = "https://" + cpqInstanceName + ".bigmachines.com/"
        self.baseFolder = "D:\\"+cpqInstanceName

        #Calling Chromedriver launch
        self.launchChrome()
        self.wait = WebDriverWait(self.driver, 10)

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
        try:
            self.driver.get(self._cpq_instance_url)
            self.wait.until(EC.visibility_of_element_located((By.ID,'login-form')))
        except:
            print("Error: Unable to navigate with Login URL")

        time.sleep(3)
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "psword").send_keys(self.password)
        self.driver.find_element(By.ID, "log_in").click()
        time.sleep(5)

        if (len(self.driver.find_elements(By.ID,"login-form")) > 0):
            print("Error: Login Failed")

    def logout(self):
        self.driver.get(self._cpq_instance_url+"logout.jsp?_bm_trail_refresh_=true")

    def navigateTo_admin(self):
        self.driver.get(self._cpq_instance_url+"admin/index.jsp?_bm_trail_refresh_=true")

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

    def extractBmlLibrary(self,skipLibraries=0):
        '''Inputs:
               driver = launchChrome()
               cpqInstanceName = ""
               saveLocation = self.baseFolder+"/BML Library/
        '''
        bmlLib = BmlLibrary(self.driver, self.cpqInstanceName, self.baseFolder+"/BML Library/")
        bmlLib.extract_bmllib(skipLibraries) #Parameters: skipLibraries=0

if __name__=="__main__":
    #main = oracle_cpq_ui_automation(cpqInstanceName="<companySiteName>",username="<username>",password="<password>")
    #main.login()

    ''' 1# Partner Orgs
    main.createGroupsinPartnerOrg(groupsToCreate=[["Partner User","partnerUser",True]],
                                  exceptionListOfCompanies=[],
                                  noOfPagesToSkip=-1)
    '''

    ''' 2# Save the BML Libraries as txt file 
    main.extractBmlLibrary(skipLibraries=0)
    '''