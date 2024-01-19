import os
import time
import re
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BmlLibrary:
    def __init__(self,driver,cpqInstanceName,saveLocation=""):
        self.driver = driver
        self.cpqInstanceName = cpqInstanceName
        self._cpq_instance_url = "https://" + cpqInstanceName + ".bigmachines.com/"
        self.wait = WebDriverWait(self.driver, 10)
        self.saveLocation = saveLocation
        self.bmllibs = []

        #Calling BML page
        self.navigateTo_bmllib()

    def navigateTo_bmllib(self):
        self.driver.get(self._cpq_instance_url+"admin/bmllib/list_functions.jsp")

    #bmllibrary
    def extract_bmllib(self,skip=0):
        list_of_bmllibs = [x.get_attribute('href') for x in self.driver.find_elements(By.XPATH,"//form[@name='bmForm']/table[2]/tbody/tr/td[2]/a")]
        list_of_bmllibs.pop(0) #removing header tr data

        #Progressbar
        progress = tqdm(range(0, len(list_of_bmllibs)))
        progress.set_description("Exporting BML Libraries ")
        for p,bmllib in zip(progress,list_of_bmllibs):
            if(p < skip):
                continue

            self.driver.get(bmllib)
            self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
            #time.sleep(5)

            # BML LIB CLASS
            bmllib_ins = BMLLIB()
            bmllib_ins.instance = self.cpqInstanceName
            bmllib_ins.url = bmllib
            bmllib_ins.name = self.driver.find_element(By.ID,'name').get_attribute('value')
            bmllib_ins.variableName = self.driver.find_element(By.ID,'variableName').get_attribute('value')
            bmllib_ins.description = self.driver.find_element(By.NAME,'description').get_attribute('value')
            bmllib_ins.returnType = self.driver.find_element(By.NAME,'returnType').get_attribute('value')

            #Parameters
            params = [[ele1.text,ele2.text]
                          for ele1,ele2
                          in
                          zip(
                              self.driver.find_elements(By.XPATH,".//div[@class='x-grid3-cell-inner x-grid3-col-paramName']"),
                              self.driver.find_elements(By.XPATH,".//div[@class='x-grid3-cell-inner x-grid3-col-paramType']")
                          )]
            bmllib_ins.params = params

            #ATTRIBUTES
            attrs = [ele.text for ele in self.driver.find_elements(By.XPATH,".//div[@class='x-grid3-cell-inner x-grid3-col-attr']")]
            bmllib_ins.attributes = attrs

            #LIBRARYFUNCTIONS
            self.driver.find_element(By.XPATH,"//div[@id='libraryFnEdCodeTools']/div/div/ul/li[4]").click()
            libFuncs = [ele.text for ele in
                     self.driver.find_elements(By.XPATH,".//div[@class='x-grid3-cell-inner x-grid3-col-libFunction']")]
            bmllib_ins.libraryfunctions = libFuncs

            #CODE
            self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME,"iframe"))
            bmllib_ins.code = self.driver.find_element(By.ID,'textarea').get_attribute('value')
            self.driver.switch_to.default_content()

            #BACK - not needed as we are using link to open bml
            #self.driver.find_element(By.XPATH,"//button[@type='button'][text()='Back']").click()

            self.bmllibs.append(bmllib_ins)
            bmllib_ins.save(self.saveLocation)
        print("%s bml util libraries exported successfully.."%(len(self.bmllibs)))
class BMLLIB:
    #Util BML Library Function Editor: Properties & Parameters
    def __init__(self):
        self.url = ""
        self.instance = ""
        self.name = ""
        self.variableName = ""
        self.description = ""
        self.returnType = ""
        self.params = []
        self.attributes = []
        self.libraryfunctions = []
        self.code = ""

    def display(self):
        print(self.name + " - " + self.variableName)

    def save(self, save_loc = ""):
        if(save_loc == ""):
            save_loc = "./bin/" + self.instance + "/BML Library/"

        if(not os.path.exists(save_loc)):
            # Create a new directory because it does not exist
            os.makedirs(save_loc)

        # open text file
        file_name = self.name + " - " + self.variableName
        file_name = re.sub(r'[^\w\-_\. ]', '', file_name)
        text_file = open(save_loc + file_name + ".txt", "w")
        # write string to file
        content = """
Name         : %s
VariableName : %s
Description  : %s
Url : %s

==========
Parameter: 
==========
Parameter Name                                          Parameter Type
%s

===========
Attributes: 
===========
%s

==================
Library Functions:
==================
%s

=========
BML Code:
=========
%s

"""%(self.name,
       self.variableName,
       self.description,
       self.url,
       '\n'.join([ x[0].ljust(40) + x[1].rjust(30) for x in self.params]),
       '\n'.join(self.attributes),
       '\n'.join(self.libraryfunctions),
       self.code)

        #try:
        text_file.write(content)
        #except:
        #    print("UnicodeEncodeError: 'charmap' codec can't encode character")

        # close file
        text_file.close()
