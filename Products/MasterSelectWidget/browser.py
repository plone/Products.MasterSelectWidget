# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

registerDynamicSelect = '''
registerDynamicSelect('edit_form',
                      '%(master)s',
                      '%(name)s',
                      '%(action)s',
                      '%(vocab_method)s',
                      '%(control_param)s',
                      '%(absolute_url)s');
'''

registerHideOnSelect = '''
registerHideOnSelect('edit_form',
                     '%(master)s',
                     '%(name)s',
                     '%(action)s',
                     %(hidden)s);
'''

def boolean_value(value):
    if value in (1, '1', 'true', 'True', True):
        return 'true'
    return 'false'


class SetupSlaves(BrowserView):
    """javascript stuff for slaves fields
    """

    def __call__(self, field):
        """render javascript
        """
        js = []
        master = field.getName()
        slaves = getattr(field.widget, 'slave_fields', ())
        for s in slaves:
            slave = s.copy()
            slave['master'] = master
            slave['absolute_url'] = self.context.absolute_url()
            action = slave.get('action', None)
            if action in ['vocabulary', 'value']:
                slave.setdefault('control_param','master_value')
                js.append(registerDynamicSelect % slave)

            else:
                hide_values = slave.get('hide_values', None)

                if hide_values is None:
                    hide_values = []
                elif type(hide_values) not in (tuple,list):
                    hide_values = [hide_values]

                if field.type == 'boolean':
                    hide_values = [boolean_value(v) for v in hide_values]

                hidden = "new Array('%s')" % "','".join(hide_values)
                slave['hidden'] = hidden
                js.append(registerHideOnSelect % slave)

        return ''.join(js)

