#from oracle_cpq_ui_automation import oracle_cpq_ui_automation

import oracle_cpq_ui_automation

main = oracle_cpq_ui_automation("<cpqInstanceName>","<userName>","<password>")
main.launchChrome()
main.login()
main.createGroupsinPartnerOrg(
    [["<groupName>","<groupVar",True]], #groupsToCreate = [ [<groupName~string>, <groupVarName~string>, <addAllUsersToGroup~boolean> ] ] #2D Array of mixed datatype
    [], #exceptionListOfCompanies = [] #Array of strings
    -1 #noOfPagesToSkip = -1
)