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
${masterboolean_id}  masterBoolean
${mastermultiselect_id}  masterMultiSelect

*** Test Cases ***

Test masterfield1 change vocabulary of slavefield1
    Select From List By Value  ${masterfield_1_id}  1
    ${vocabulary} =  Get List Items  ${slavefield_1_id}
    ${expected_voc} =  Create List  num: 2  num: 3  num: 4  num: 5  num: 6  num: 7  num: 8  num: 9
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Select From List By Value  ${masterfield_1_id}  5
    ${vocabulary} =  Get List Items  ${slavefield_1_id}
    ${expected_voc} =  Create List  num: 6  num: 7  num: 8  num: 9
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}

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
    ${expected_voc} =  Create List  G  H  I  J  K
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Select From List By Value  ${masterfield_2_id}  a
    ${vocabulary} =  Get List Items  ${slaveMasterfield_id}
    ${expected_voc} =  Create List  B  C  D  E  F
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}

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
    ${expected_voc} =  Create List  42
    Select Checkbox  ${mastermultiselect_id}_2
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected_voc} =  Create List  20
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Select Checkbox  ${mastermultiselect_id}_4
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected_voc} =  Create List  20  23  29  31  37  40
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Select Checkbox  ${mastermultiselect_id}_3
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected_voc} =  Create List  20  23  29  30  31  37  40
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}
    Unselect Checkbox  ${mastermultiselect_id}_2
    ${vocabulary} =  Get List Items  ${slavefield_7_id}
    ${expected_voc} =  Create List  30  31  37  40
    Lists Should Be Equal  ${vocabulary}  ${expected_voc}

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

