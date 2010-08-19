from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import SelectionWidget, MultiSelectionWidget
from Products.Archetypes.Registry import registerWidget


class MasterSelectWidget(SelectionWidget):
    security = ClassSecurityInfo()

    _properties = SelectionWidget._properties.copy()
    _properties.update({
        'macro': 'masterselection',
        'format': 'select',
        'helper_js': ('++resource++masterselect.js',),
        'slave_fields': (), # Fields controlled by this field, if control_type
                            # is vocabulary only the first entry is used
        })

class MasterMultiSelectWidget(MultiSelectionWidget):
    security = ClassSecurityInfo()

    _properties = MultiSelectionWidget._properties.copy()
    _properties.update({
        'macro': 'mastermultiselection',
        'format': 'checkbox',
        'helper_js': ('++resource++masterselect.js',),
        'slave_fields': (), # Fields controlled by this field, if control_type
                            # is vocabulary only the first entry is used
        })


registerWidget(MasterSelectWidget,
               title='Master Select',
               description="Select field which uses javascript to control subordinate widgets.",
               used_for=('Products.Archetypes.public.StringField',
                         'Products.Archetypes.Field.LinesField')
               )
registerWidget(MasterMultiSelectWidget,
               title='Master Multi Select',
               description="Select field which uses javascript to control subordinate widgets.",
               used_for=('Products.Archetypes.Field.LinesField')
               )
