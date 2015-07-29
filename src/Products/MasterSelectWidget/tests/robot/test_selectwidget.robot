*** settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  Collections


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

${masterfield_1_id}  masterField
${masterfield_2_id}  masterField2
${masterfield_3_id}  masterField3
${slavefield_1_id}  slaveField1
${slavefield_2_id}  slaveField2
${slavefield_3_id}  slaveField3
${slavefield_4_id}  slaveField4
${slavefield_5_id}  slaveField5
${slavefield_6_id}  slaveField6
${slavefield_7_id}  slaveField7
${slaveMasterfield_id}  slaveMasterField
${slaveValuefield_id}  slaveValueField
${slaveValuefield_2_id}  slaveValueField2
${masterboolean_id}  masterBoolean
${mastermultiselect_id}  masterMultiSelect
${mastermultiselect2__id}  masterMultiSelect2

*** Test Cases ***

Test masterFields are triggered at form init
    ${vocabulary} =  Get List Items  ${slavefield_1_id}
    ${expected} =  Create List  2  3  4  5  6  7  8  9
    Lists Should Be Equal  ${vocabulary}  ${expected}
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_6_id}
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected} =  Create List  b  c  d  e  f
    Lists Should Be Equal  ${vocabulary}  ${expected}


Test masterfield1 change vocabulary of slavefield1
    Select From List By Value  ${masterfield_1_id}  1
    ${vocabulary} =  Get List Items  ${slavefield_1_id}
    ${expected} =  Create List  2  3  4  5  6  7  8  9
    Lists Should Be Equal  ${vocabulary}  ${expected}
    Select From List By Value  ${masterfield_1_id}  5
    ${vocabulary} =  Get List Items  ${slavefield_1_id}
    ${expected} =  Create List  6  7  8  9
    Lists Should Be Equal  ${vocabulary}  ${expected}

Test masterfield1 toggle visibility of slavefield1
    Select From List By Value  ${masterfield_1_id}  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_1_id}
    Select From List By Value  ${masterfield_1_id}  6
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_1_id}

Test masterfield1 toggle visibility of slavefield2
    Select From List By Value  ${masterfield_1_id}  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_2_id}
    Select From List By Value  ${masterfield_1_id}  2
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_2_id}
    Select From List By Value  ${masterfield_1_id}  1
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_2_id}
    Select From List By Value  ${masterfield_1_id}  4
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_2_id}

Test masterfield1 toggle activation of slavefield3
    Select From List By Value  ${masterfield_1_id}  1
    Element Should Be Disabled  id=${slavefield_3_id}
    Select From List By Value  ${masterfield_1_id}  2
    Element Should Be Enabled  id=${slavefield_3_id}
    Select From List By Value  ${masterfield_1_id}  5
    Element Should Be Disabled  id=${slavefield_3_id}

Test masterfield2 change vocabulary of slaveMasterField
    Select From List By Value  ${masterfield_2_id}  f
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected} =  Create List  g  h  i  j  k
    Lists Should Be Equal  ${vocabulary}  ${expected}
    Select From List By Value  ${masterfield_2_id}  a
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected} =  Create List  b  c  d  e  f
    Lists Should Be Equal  ${vocabulary}  ${expected}

Test masterfield2 change value of slaveValueField
    Select From List By Value  ${masterfield_2_id}  d
    Textfield Value Should Be  ${slaveValuefield_id}  q
    Select From List By Value  ${masterfield_2_id}  a
    Textfield Value Should Be  ${slaveValuefield_id}  n

Test slaveMasterField toggle visibility of slavefield4
    Select From List By Value  ${slaveMasterfield_id}  b
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_4_id}
    Select From List By Value  ${slaveMasterfield_id}  c
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_4_id}

Test masterfield3 toggle activation of slaveValueField
    Select From List By Value  ${masterfield_3_id}  other
    Element Should Be Disabled  id=${slaveValuefield_id}
    Select From List By Value  ${masterfield_3_id}  one
    Element Should Be Enabled  id=${slaveValuefield_id}

Test masterfield3 toggle visibility of slavefield5
    Select From List By Value  ${masterfield_3_id}  other
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_5_id}
    Select From List By Value  ${masterfield_3_id}  one
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_5_id}

Test masterboolean toggle visibility of slavefield6
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_6_id}
    Select Checkbox  ${masterboolean_id}
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_6_id}
    Unselect Checkbox  ${masterboolean_id}
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_6_id}

Test mastermultiselect change vocabulary of slavefield7
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected} =  Create List  42
    Select Checkbox  ${mastermultiselect_id}_2
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected} =  Create List  20
    Lists Should Be Equal  ${vocabulary}  ${expected}
    Select Checkbox  ${mastermultiselect_id}_4
    Select Checkbox  ${mastermultiselect_id}_3
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected} =  Create List  20  23  29  30  31  37  40
    Lists Should Be Equal  ${vocabulary}  ${expected}
    Unselect Checkbox  ${mastermultiselect_id}_3
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected} =  Create List  20  23  29  31  37  40
    Lists Should Be Equal  ${vocabulary}  ${expected}

Test mastermultiselect toggle visibility of slavefield7
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_7_id}
    Select Checkbox  ${mastermultiselect_id}_1
    Select Checkbox  ${mastermultiselect_id}_2
    Select Checkbox  ${mastermultiselect_id}_3
    Select Checkbox  ${mastermultiselect_id}_4
    Element Should Not Be Visible  id=archetypes-fieldname-${slavefield_7_id}
    Unselect Checkbox  ${mastermultiselect_id}_2
    Element Should Be Visible  id=archetypes-fieldname-${slavefield_7_id}

Test mastermultiselect2 change value of slaveValueField2
    Select From List By Value  ${mastermultiselect_2_id}  words  better  world
    Textfield Value Should Be  ${slaveValuefield_2_id}  words better world

Test mastermultiselect2 toggle activation of slaveValueField2
    Element Should Be Disabled  id=${slaveValuefield_2_id}
    Select From List By Value  ${mastermultiselect_2_id}  you  are  random
    Element Should Be Enabled  id=${slaveValuefield_2_id}
    Unselect From List By Value  ${mastermultiselect_2_id}  you
    Element Should Be disabled  id=${slaveValuefield_2_id}

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

