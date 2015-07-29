from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.Registry import registerWidget


class MasterMultiSelectWidget(MultiSelectionWidget):
    security = ClassSecurityInfo()

    _properties = MultiSelectionWidget._properties.copy()
    _properties.update({
        'macro': 'mastermultiselection',
        'helper_js': ('++resource++masterselect.js',),
        'slave_fields': (),  # Fields controlled by this field, if control_type
                             # is vocabulary only the first entry is used
    })


registerWidget(MasterMultiSelectWidget,
               title='Master MultiSelect',
               description="MultiSelect field which uses javascript to control subordinate widgets.",
               used_for=('Products.Archetypes.Field.LinesField')
               )
