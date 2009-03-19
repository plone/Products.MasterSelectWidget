from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import SelectionWidget
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


registerWidget(MasterSelectWidget,
               title='Master Select',
               description="Select field which uses javascript to control subordinate widgets.",
               used_for=('Products.Archetypes.public.StringField',
                         'Products.Archetypes.Field.LinesField')
               )
