"""Demonstrates the use of MasterSelectWidget."""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import ReferenceWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

# Define slave parameters for masterField
slave_fields = (
    # Controls the vocab of slaveField1
    {
        'name': 'slaveField1',
        'action': 'vocabulary',
        'vocab_method': 'getSlaveVocab',
        'control_param': 'master',
    },
    # Controls the visibility of slaveField1 also
    {
        'name': 'slaveField1',
        'action': 'hide',
        'hide_values': ('6',),
    },
    # Controls the visibility of slaveField2
    {
        'name': 'slaveField2',
        'action': 'hide',
        'hide_values': ('2', '4'),
    },
    # Disables slaveField3
    {
        'name': 'slaveField3',
        'action': 'disable',
        'hide_values': ('1', '5'),
    },
)

# Define slave parameters for masterField2
slave_fields2 = (
    # Controls the vocab of slaveMasterField
    {
        'name': 'slaveMasterField',
        'action': 'vocabulary',
        'vocab_method': 'getSlaveVocab2',
        'control_param': 'master',
    },
    # Controls the value of slaveValueField
    {
        'name': 'slaveValueField',
        'action': 'value',
        'vocab_method': 'getSlaveValue',
        'control_param': 'master',
    },
)

# Define slave parameters for slaveMasterField
slave_master_fields = (
    # Controls the visibility of slaveField4
    {
        'name': 'slaveField4',
        'action': 'hide',
        'hide_values': ('c', 'g'),
    },
)

# define slave parameters for masterField3
slave_fields3 = (
    # Controls the visibility of slaveField5
    {
        'name': 'slaveField5',
        'action': 'show',
        'hide_values': ('other',),
    },
    # Enable slaveValueField
    {
        'name': 'slaveValueField',
        'action': 'enable',
        'hide_values': ('one',),
    },
)

# define slave parameters for masterMultiSelect
multiselect_slave_fields = (
    # Controls the vocabulary of slaveField7
    {
        'name': 'slaveField7',
        'action': 'vocabulary',
        'vocab_method': 'getSlaveVocab7',
        'control_param': 'values',
    },
    # Controls the visibility of slaveField7
    {
        'name': 'slaveField7',
        'action': 'hide',
        'toggle_method': 'hideSlaveVocab7',
        'control_param': 'values',
    },
)

# define slave parameters for masterMultiSelect2
multiselect_slave_fields2 = (
    # Controls the value of slaveValueField2
    {
        'name': 'slaveValueField2',
        'action': 'value',
        'vocab_method': 'getSlaveValue2',
        'control_param': 'values',
    },
    # Enable slaveValueField2
    {
        'name': 'slaveValueField2',
        'action': 'enable',
        'toggle_method': 'enableSlaveValue2',
        'control_param': 'values',
    },
)

schema = BaseSchema + Schema((

    IntegerField(
        name='masterField',
        searchable=1,
        default='',
        vocabulary=['1', '2', '3', '4', '5', '6'],
        widget=MasterSelectWidget(
            slave_fields=slave_fields,
            description="This field controls the vocabulary of slaveField1,"
                        "the available values in slaveField1 will be equal "
                        "to the numbers between the selected number and 10. "
                        "When the value 2 or 4 is selected, slaveField2 will "
                        "be hidden. When the value 1 or 5 is selected, "
                        "slaveField3 will be disabled. When value 6 is "
                        "selected, slaveField one will be hidden.",
        ),
    ),

    LinesField(
        name='slaveField1',
        searchable=1,
        default='',
        vocabulary=['1', '2', '3', '4', '5', '6'],
        widget=MultiSelectionWidget(
            format='select',
            description="This field's vocabulary is controlled by the value "
                        "selected in masterField. The values available here "
                        "will be the numbers between the number selected in "
                        "masterField and 10. The field will be hidden when 6 "
                        "is selected in the masterField.",
        ),
    ),

    IntegerField(
        name='slaveField2',
        searchable=1,
        default='',
        vocabulary=['10', '20', '30', '40', '50'],
        widget=SelectionWidget(
            format='select',
            description="This field's visiblity is controlled by the value "
                        "selected in masterField. It will become invisible "
                        "when the values 2 or 4 are selected.",
        ),
    ),

    BooleanField(
        name='slaveField3',
        searchable=1,
        default='',
        widget=BooleanWidget(
            format='select',
            description="This field's availability is controlled by the value "
                        "selected in masterField. It will be deactivated when "
                        "the values 1 or 5 are selected.",
        ),
    ),

    StringField(
        name='masterField2',
        searchable=1,
        default='',
        vocabulary=['a', 'b', 'c', 'd', 'e', 'f'],
        widget=MasterSelectWidget(
            slave_fields=slave_fields2,
            description="This field controls the vocabulary of slaveMasterField, "
                        "the available values in slaveMasterField will be the "
                        "5 letters after the selected letter. It also controls "
                        "the current value of the field SlaveValueField, which "
                        "contains the ROT13 transformed value of the selection.",
        ),
    ),

    StringField(
        name='slaveMasterField',
        searchable=1,
        default='',
        vocabulary=['1', '2', '3', '4', '5', '6'],
        widget=MasterSelectWidget(
            slave_fields=slave_master_fields,
            description="This field's vocabulary is controlled by the value "
                        "selected in masterField2. The values available here "
                        "will be the 5 letters after the selected letter. "
                        "This field also controls the visibility of slaveField4. "
                        "If the values c or g are selected slaveField4 will "
                        "be hidden.",
        ),
    ),

    ReferenceField(
        name='slaveField4',
        searchable=1,
        default='',
        relationship="bad_news",
        widget=ReferenceWidget(
            description="This field's visiblity is controlled by the value "
                        "selected in slaveMasterField. It will become invisible "
                        "when the values c or g are selected.",
        ),
    ),

    StringField(
        name='slaveValueField',
        searchable=1,
        default='',
        widget=StringWidget(
            description="This field's value is controlled by the value "
                        "selected in MasterField2. It will display the ROT13 "
                        "transformation of the value selected. The field's "
                        "availability is controlled by the value selected in "
                        "masterField3. It only will be activated when the"
                        "values 'one' is selected.",
        ),
    ),

    StringField(
        name='masterField3',
        searchable=1,
        default='',
        vocabulary=['one', 'two', 'three', 'other'],
        widget=MasterSelectWidget(
            slave_fields=slave_fields3,
            description="This field controls the visibility of slaveField5. "
                        "It will become visible only when the value 'other' "
                        "is selected. It also controls the availability of"
                        "slaveValueField. It will be enabled when the value "
                        "'one' is selected.",
        ),
    ),

    StringField(
        name='slaveField5',
        searchable=1,
        widget=StringWidget(
            description="This field's visiblity is controlled by the value "
                        "selected in masterField3. It will become visible "
                        "only when the value 'other' is selected.",
        ),
    ),

    BooleanField(
        name='masterBoolean',
        widget=MasterBooleanWidget(
            slave_fields=(
                dict(name='slaveField6', action='show', hide_values=1),),
            description="This field controls the visibility of slaveField6, "
                        "which will only become visible when this checkbox is checked."
        ),
    ),

    StringField(
        name='slaveField6',
        widget=StringWidget(
            description="This field's visiblity is controlled by the value "
                        "selected in masterBoolean. It will become visible "
                        "only when that checkbox is checked.",
        ),
    ),

    LinesField(
        name='masterMultiSelect',
        multiValued=1,
        vocabulary=['10', '20', '30', '40', '50'],
        widget=MasterMultiSelectWidget(
            slave_fields=multiselect_slave_fields,
            format='checkbox',
            description="This field controls the vocabulary of slaveField7. "
                        "The available values in slaveField7 will be equal "
                        "to the selected numbers and all the prime numbers "
                        "between the lowest and higher selection."
        ),
    ),

    LinesField(
        name='slaveField7',
        searchable=1,
        default='',
        vocabulary=[],
        widget=SelectionWidget(
            format='select',
            description="This field's vocabulary is controlled by the values "
                        "selected in masterMultiSelect. The values available here "
                        "will be the selected numbers and all the prime numbers "
                        "between them or 42 when no values are selected."
        ),
    ),

    LinesField(
        name='masterMultiSelect2',
        multiValued=1,
        vocabulary=['you', 'are', 'random', 'words', 'is', 'better', 'than', 'world'],
        widget=MasterMultiSelectWidget(
            slave_fields=multiselect_slave_fields2,
            format='select',
            description="This field controls the value of slaveValueField2, it "
                        "will be a string join of all selected values. It also "
                        "controls availability of slaveValueField2. It will be "
                        "deactivated when both words 'you' and 'are' are selected."
        ),
    ),

    StringField(
        name='slaveValueField2',
        searchable=1,
        default='default',
        widget=StringWidget(
            description="This field's value is controlled by the values selected "
                        "in masterMultiSelect2. It will display a join of all "
                        "selected values. This field will be activated when both "
                        "words 'you' and 'are' are selected."
        ),
    ),
))


class MasterSelectDemo(BaseContent):
    """Demo from MasterSelectWidget."""
    schema = schema
    content_icon = "document_icon.gif"
    security = ClassSecurityInfo()

    _at_rename_after_creation = True  # rename object according to the title

    security.declarePublic('getSlaveVocab')

    def getSlaveVocab(self, master):
        """Vocab method that returns a vocabulary consisting of the numbers
        between the input number and 10.

        The displayed value has "num: " prepended.
        """
        results = range(int(master) + 1, 10)
        results = [(str(a), "num: " + str(a)) for a in results]
        return DisplayList(results)

    security.declarePublic('getSlaveVocab2')

    def getSlaveVocab2(self, master):
        """Vocabulary method that returns a vocabulary consisting of the five
        letters after the selected letter.

        The displayed value will be capitalized, the stored value lowercase.
        """
        numeric = ord(master)
        results = range(numeric + 1, numeric + 6)
        results = [(chr(a), chr(a).upper()) for a in results]
        return DisplayList(results)

    security.declarePublic('getSlaveValue')

    def getSlaveValue(self, master):
        """Value method that returns ROT13 transformed input."""
        numeric = ord(master)
        result = chr(numeric + 13)
        return result

    security.declarePublic('getSlaveVocab7')

    def getSlaveVocab7(self, *values):
        """Vocabulary method that returns values + prime numbers between values."""
        def isPrime(n):
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True

        selection = sorted([int(v['val']) for v in values if v['selected']])
        selection = selection or [42]
        results = []
        for i in range(selection[0], selection[-1] + 1):
            if i in selection or isPrime(i):
                results.append((str(i), str(i)))
        return DisplayList(results)

    security.declarePublic('hideSlaveVocab7')

    def hideSlaveVocab7(self, *values):
        """Hide method returning true if 4 or more values are checked in masterfield"""
        selection = [v['val'] for v in values if v['selected']]
        return len(selection) >= 4

    security.declarePublic('getSlaveValue2')

    def getSlaveValue2(self, *values):
        """Value method that returns the sum of selected values."""
        selection = [v['val'] for v in values if v['selected']]
        result = ' '.join(selection)
        return result

    security.declarePublic('enableSlaveValue2')

    def enableSlaveValue2(self, *values):
        """Enable method that returns true if both 'you' and 'are' are selected."""
        selection = [v['val'] for v in values if v['selected']]
        enable = 'you' in selection and 'are' in selection
        return enable


registerType(MasterSelectDemo, 'MasterSelectWidget')
