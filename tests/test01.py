from oracle_cpq_ui_automation import oracle_cpq_ui_automation

main = oracle_cpq_ui_automation("testnovgp","karun","Birlasoft@6")
main.launchChrome()
main.login()
main.createGroupsinPartnerOrg([["Partner User","partnerUser",True]],[],-1)