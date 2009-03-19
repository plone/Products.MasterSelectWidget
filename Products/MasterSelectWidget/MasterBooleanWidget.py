from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.Registry import registerWidget


class MasterBooleanWidget(BooleanWidget):
    security = ClassSecurityInfo()

    _properties = BooleanWidget._properties.copy()
    _properties.update({
        'macro': 'masterboolean',
        'format': 'select',
        'helper_js': ('++resource++masterselect.js',),
        'slave_fields': (), # Fields controlled by this field, if control_type
                            # is vocabulary only the first entry is used
        })


registerWidget(MasterBooleanWidget,
               title='Master Boolean',
               description="Boolean field which uses javascript to control subordinate widgets.",
               used_for=('Products.Archetypes.public.BooleanField',)
               )
