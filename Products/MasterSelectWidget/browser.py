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
    
    def getSlaves(self, field):
        for slave in getattr(field.widget, 'slave_fields', ()):
            yield slave.copy()
        
    def renderJS(self, field):
        master = field.getName()
        for slave in self.getSlaves(field):
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
    
    def getSlaves(self, fieldname):
        return getattr(self.context.Schema()[fieldname].widget, 
            'slave_fields', ())
    
    def getVocabulary(self, slave, value):
        kw = { slave['control_param']: value }
        result = getattr(self.context, slave['vocab_method'])(**kw)
        return result
    
    def __call__(self):
        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8')
        
        field = self.request['field']
        slaveid = self.request['slave']
        value = self.request['value']
        
        for slave in self.getSlaves(field):
            if slave['name'] != slaveid:
                continue
            
            action = slave.get('action')
            if action not in ['vocabulary', 'value']:
                raise ValueError('Invalid master-slave action')
            
            result = self.getVocabulary(slave, value)
            
            if action == 'value':
                return json.dumps(translate(result, self.request))
            
            if isinstance(result, (tuple, list)):
                result = DisplayList(zip(result, result))
            actualValue = self.context.Schema()[slave.get('name')].get(self.context)
            if  not isinstance(actualValue,list):
                actualValue = [actualValue,]
            return json.dumps([
                dict(
                    value=item,
                    label=translate(result.getValue(item), self.request),
                    selected=(item in actualValue) and 'selected' or '',
                ) for item in result
            ])       

        raise ValueError('No such master-slave combo')
