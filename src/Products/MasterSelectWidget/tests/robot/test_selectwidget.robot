*** settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Collections


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

${masterfield_id_1}  masterField
${masterfield_id_2}  masterField2
${masterfield_id_3}  masterField3
${slavefield_id_1}  slaveField1
${slavefield_id_2}  slaveField2
${slavefield_id_3}  slaveField3
${slavefield_id_4}  slaveField4
${slavefield_id_5}  slaveField5
${slavefield_id_6}  slaveField6
${slaveMasterfield_id}  slaveMasterField
${slaveValuefield_id}  slaveValueField
${masterboolean_id}  masterBoolean

*** Test Cases ***

Test masterfield1 change vocabulary of slavefield1
    ${masterfield_1_xpath} =  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Page Should Contain  num: 2
    Page Should Contain  num: 3
    Page Should Contain  num: 4
    Select From List By Value  xpath=${masterfield_1_xpath}/select  5
    Page Should Not Contain  num: 2
    Page Should Not Contain  num: 3
    Page Should Not Contain  num: 4

Test masterfield1 toggle visibility of slavefield1
    ${masterfield_1_xpath} =  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  6
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_1}

Test masterfield1 toggle visibility of slavefield2
    ${masterfield_1_xpath} =  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  2
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_2}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  4
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_2}

Test masterfield1 toggle activation of slavefield3
    ${masterfield_1_xpath} =  Get field XPath  ${masterfield_id_1}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  1
    Element Should Be Disabled  id=${slavefield_id_3}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  2
    Element Should Be Enabled  id=${slavefield_id_3}
    Select From List By Value  xpath=${masterfield_1_xpath}/select  5
    Element Should Be Disabled  id=${slavefield_id_3}

Test masterfield2 change vocabulary of slaveMasterField
    ${masterfield_2_xpath} =  Get field XPath  ${masterfield_id_2}
    Select From List By Value  xpath=${masterfield_2_xpath}/select  f
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected_voc} =  Create List  G  H  I  J  K
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Select From List By Value  xpath=${masterfield_2_xpath}/select  a
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected_voc} =  Create List  B  C  D  E  F
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}

Test masterfield2 change value of slaveValueField
    ${masterfield_2_xpath} =  Get field XPath  ${masterfield_id_2}
    Select From List By Value  xpath=${masterfield_2_xpath}/select  d
    Textfield Value Should Be  ${slaveValuefield_id}  q
    Select From List By Value  xpath=${masterfield_2_xpath}/select  a
    Textfield Value Should Be  ${slaveValuefield_id}  n

Test slaveMasterField toggle visibility of slavefield4
    ${slaveMasterfield_xpath} =  Get field XPath  ${slaveMasterfield_id}
    Select From List By Value  xpath=${slaveMasterfield_xpath}/select  b
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_id_4}
    Select From List By Value  xpath=${slaveMasterfield_xpath}/select  c
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_id_4}

Test masterfield3 toggle activation of slaveValueField
    ${masterfield_3_xpath} =  Get field XPath  ${masterfield_id_3}
    Select From List By Value  xpath=${masterfield_3_xpath}/select  other
    Element Should Be Disabled  id=${slaveValuefield_id}
    Select From List By Value  xpath=${masterfield_3_xpath}/select  one
    Element Should Be Enabled  id=${slaveValuefield_id}

Test masterfield3 toggle visibility of slavefield5
    ${masterfield_3_xpath} =  Get field XPath  ${masterfield_id_3}
    Select From List By Value  xpath=${masterfield_3_xpath}/select  other
    Element Should Be Visible  id=${slavefield_id_5}
    Select From List By Value  xpath=${masterfield_3_xpath}/select  one
    Element Should Not Be Visible  id=${slavefield_id_5}

Test masterboolean toggle visibility of slavefield6
    Element Should Not Be Visible  id=${slavefield_id_6}
    Select Checkbox  ${masterboolean_id}
    Element Should Be Visible  id=${slavefield_id_6}
    Unselect Checkbox  ${masterboolean_id}
    Element Should Not Be Visible  id=${slavefield_id_6}

*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin
    Go to  ${PLONE_URL}/msw_demo/edit

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit

Get field XPath
    [Arguments]  ${field_id}
    [Return]  //div[@id="archetypes-fieldname-${field_id}"]

