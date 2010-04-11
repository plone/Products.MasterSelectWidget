"""Demonstrates the use of MasterSelectWidget."""

from Products.Archetypes.public import *
from AccessControl import ClassSecurityInfo
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget

# Define slave parameters for masterField
slave_fields = (
    # Controls the vocab of slaveField1
    {'name': 'slaveField1',
     'action': 'vocabulary',
     'vocab_method': 'getSlaveVocab',
     'control_param': 'master',
    },
    # Controls the visibility of slaveField1 also
    {'name': 'slaveField1',
     'action': 'hide',
     'hide_values': ('6',),
    },
    # Controls the visibility of slaveField2
    {'name': 'slaveField2',
     'action': 'hide',
     'hide_values': ('2','4'),
    },
    # Disables slaveField3
    {'name': 'slaveField3',
     'action': 'disable',
     'hide_values': ('1','5'),
    },
)

# Define slave parameters for masterField2
slave_fields2 = (
    # Controls the vocab of slaveMasterField
    {'name': 'slaveMasterField',
     'action': 'vocabulary',
     'vocab_method': 'getSlaveVocab2',
     'control_param': 'master',
    },
    # Controls the value of slaveValueField
    {'name': 'slaveValueField',
     'action': 'value',
     'vocab_method': 'getSlaveValue',
     'control_param': 'master',
    },
)

# Define slave parameters for slaveMasterField
slave_master_fields = (
    # Controls the visibility of slaveField4
    {'name': 'slaveField4',
     'action': 'hide',
     'hide_values': ('c','g'),
    },
)

# define slave parameters for masterField3
slave_fields3 = (
    # Controls the visibility of slaveField5
    {'name': 'slaveField5',
     'action': 'show',
     'hide_values': ('other',),
    },
    # Enable slaveValueField
    {'name': 'slaveValueField',
     'action': 'enable',
     'hide_values': ('one',),
    },
)

schema = BaseSchema + Schema((

    IntegerField(
        name='masterField',
        searchable=1,
        default='',
        vocabulary=['1','2','3','4','5','6'],
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
        vocabulary=['1','2','3','4','5','6'],
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
        vocabulary=['10','20','30','40','50'],
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
        vocabulary=['a','b','c','d','e','f'],
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
        vocabulary=['1','2','3','4','5','6'],
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
        vocabulary=['one','two','three','other'],
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
            description='This field controls the visibility of slaveField6, '
                'which will only become visible when this checkbox is checked.'
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
))

class MasterSelectDemo(BaseContent):
    """Demo from MasterSelectWidget."""
    schema = schema
    content_icon = "document_icon.gif"
    security = ClassSecurityInfo()

    _at_rename_after_creation = True # rename object according to the title

    security.declarePublic('getSlaveVocab')
    def getSlaveVocab(self, master):
        """Vocab method that returns a vocabulary consisting of the numbers
        between the input number and 10.

        The displayed value has "num: " prepended.
        """
        results = range(int(master)+1, 10)
        results = [(str(a), "num: "+str(a)) for a in results]
        return DisplayList(results)

    security.declarePublic('getSlaveVocab2')
    def getSlaveVocab2(self, master):
        """Vocab method that returns a vocabulary consisting of the five
        letters after the selected letter.

        The displayed value will be capitalized, the stored value lowercase.
        """
        numeric = ord(master)
        results = range(numeric+1, numeric+6)
        results = [(chr(a), chr(a).upper()) for a in results]
        return DisplayList(results)

    security.declarePublic('getSlaveVocab2')
    def getSlaveValue(self, master):
        """Value method that returns ROT13 transformed input."""
        numeric = ord(master)
        result = chr(numeric+13)
        return result


registerType(MasterSelectDemo, 'MasterSelectWidget')
