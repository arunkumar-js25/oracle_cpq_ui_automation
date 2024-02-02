# Oracle CPQ UI Automation
Selenium based automation bot to do routine and time consuming tasks on Oracle CPQ Cloud application.

## Pre-requisites
* Chrome Browser should be installed
* Supports Python >= 3.9
* CPQ account should have admin access with proxy login option


### Installation
```
pip install py-oracle-cpq-ui-automation
```
### Usage
Just type `import oracle_cpq_ui_automation` in the module you want to use Oracle CPQ UI Automation.

### Example
```
import oracle_cpq_ui_automation

#Initialise the automation class with SiteName, username, password
main = oracle_cpq_ui_automation("<cpqInstanceName>","<userName>","<password>") 

#It will autolaunch the Chromedriver browser

#Login into the CPQ Site
main.login()
```

## Automation Functions
### 1) Partner Orgs: Create Groups
Navigate to Partner Orgs page and check if the given groups exists in the partner org, else it will create the group

#### Inputs:
1. groupsToCreate = [ [<groupName | string>, <groupVarName | string>, <addAllUsersToGroup | boolean> ] ] 
2. exceptionListOfCompanies = [<partnerOrg-VariableName>] 
3. noOfPagesToSkip = -1

#### Code:
```
main.createGroupsinPartnerOrg(
    [["<groupName>","<groupVar",True]], #groupsToCreate #2D Array of mixed datatype
    [], #exceptionListOfCompanies = [] #Array of strings
    -1 #noOfPagesToSkip = -1
)
```
### 2) Extract and Save BML Libraries as Text files.
Navigates to Util library page and save all the util libraries as text file 

#### Inputs:
1. skipLibraries = 0 #Skip no.of.libraries to save

#### Code:
```
main.extractBmlLibrary(skipLibraries=0)
```

#### Output:
The output folder will be created and files will be saved locally in the below path
```
D:\
   > <cpqInstanceName
      > BML Library
          > library1.txt
            library2.txt
```

### Bot Features
* Automation Bot will automatically download the compatible chrome driver version based on your installed browser.
* Automations are UI-based so users can monitor, if any unexpected behaviour occurs then can close the automation to avoid problems.

### Authors & Contributors
* Arun Kumar (arunkumar.js25@gmail.com)