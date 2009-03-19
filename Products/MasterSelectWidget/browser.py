# -*- coding: utf-8 -*-
import simplejson as json
from zope.i18n import translate
from Products.Archetypes import DisplayList
from Products.Five import BrowserView

SELECT = "$('#archetypes-fieldname-%(master)s')"

BINDERS = dict(
    vocabulary=SELECT + ".bindMasterSlaveVocabulary('%(name)s', "
        "'%(absolute_url)s/@@masterselect-jsonvalue');",
    value=SELECT + ".bindMasterSlaveValue('%(name)s', "
        "'%(absolute_url)s/@@masterselect-jsonvalue');",
    toggle=SELECT + ".bindMasterSlaveToggle('%(name)s', '%(action)s', "
        "%(hidden)s);",
)

JQUERY_ONLOAD = '''\
(function($) { $(function() {
%s
});})(jQuery);
'''

def boolean_value(value):
    return value in (1, '1', 'true', 'True', True)

class SetupSlaves(BrowserView):
    """Generate Javascript to bind masters to slaves"""
    
    def renderJS(self, field):
        master = field.getName()
        slaves = getattr(field.widget, 'slave_fields', ())
        for s in slaves:
            slave = s.copy()
            slave['master'] = master
            slave['absolute_url'] = self.context.absolute_url()

            slave.setdefault('control_param','master_value')
            hidden = '[]'
            if 'hide_values' in slave:
                values = slave['hide_values']
                if not isinstance(values, (tuple,list)):
                    values = [values]
                if field.type == 'boolean':
                    values = [boolean_value(v) for v in values]
                else:
                    values = [str(v) for v in values]
                hidden = json.dumps(values)
            slave['hidden'] = hidden
            
            template = BINDERS.get(slave.get('action')) or BINDERS['toggle']
            yield template % slave
    
    def __call__(self, field):
        """render javascript"""            
        return JQUERY_ONLOAD % '\n'.join(self.renderJS(field))

class MasterSelectJSONValue(BrowserView):
    """JSON vocabulary or value for the given slave field"""
    
    def __call__(self):
        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8')
        
        field = self.request['field']
        slaveid = self.request['slave']
        value = self.request['value']
        
        slaves = getattr(self.context.Schema()[field].widget, 
            'slave_fields', ())
        for slave in slaves:
            if slave['name'] != slaveid:
                continue
            
            action = slave.get('action')
            if action not in ['vocabulary', 'value']:
                raise ValueError('Invalid master-slave action')
            
            kw = { slave['control_param']: value }
            result = getattr(self.context, slave['vocab_method'])(**kw)
            
            if action == 'value':
                return json.dumps(translate(result, value))
            
            if isinstance(result, (tuple, list)):
                result = DisplayList(zip(result, result))
            return json.dumps([
                dict(
                    value=item,
                    label=translate(result.getValue(item), self.request)
                ) for item in result
            ])
        
        raise ValueError('No such master-slave combo')
