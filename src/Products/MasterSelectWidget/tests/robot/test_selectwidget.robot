*** settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

${masterfield_id_1}  masterField
${slavefield_id_1}  slaveField1
${slavefield_id_2}  slaveField2
${slavefield_id_3}  slaveField3

*** Test Cases ***

Test masterfield1 vocabulary change of slavefield1
    Go to  ${PLONE_URL}/msw_demo/edit
    ${masterfield_1_xpath}  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Page Should Contain  num: 2
    Page Should Contain  num: 3
    Page Should Contain  num: 4
    Select From List By Value  xpath=${masterfield_1_xpath}/select  5
    Page Should Not Contain  num: 2
    Page Should Not Contain  num: 3
    Page Should Not Contain  num: 4

Test masterfield1 visibility toggle of slavefield1
    ${masterfield_1_xpath}  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  6
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_1}

Test masterfield1 visibility toggle of slavefield2
    ${masterfield_1_xpath}  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  2
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  4
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_2}

Test masterfield1 activation toggle of slavefield3
    ${masterfield_1_xpath}  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Click Element  ${slavefield_id_3}
    Checkbox Should Not Be Selected  ${slavefield_id_3}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  2
    Click Element  ${slavefield_id_3}
    Checkbox Should Be Selected  ${slavefield_id_3}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  5
    Click Element  ${slavefield_id_3}
    Checkbox Should Be Selected  ${slavefield_id_3}

*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit

Get field XPath
    [Arguments]  ${field_id}
    [Return]  //div[@id="archetypes-fieldname-${field_id}"]

