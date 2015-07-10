# -*- coding: utf-8 -*-
try:
    import json
except:
    import simplejson as json

from zope.i18n import translate
from zope.component import getAdapters
from Products.Archetypes import DisplayList
from Products.Five import BrowserView

try:
    from archetypes.schemaextender.interfaces import ISchemaExtender
    HAS_SCHEMAEXTENDER = True
except:
    HAS_SCHEMAEXTENDER = False


SELECT = "$('#archetypes-fieldname-%(master)s')"

BINDERS = dict(
    vocabulary=SELECT + ".bind%(widget_type)sMasterSlaveVocabulary('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue');",
    value=SELECT + ".bind%(widget_type)sMasterSlaveValue('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue');",
    toggle=SELECT + ".bind%(widget_type)sMasterSlaveToggle('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue');",
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
            slave['widget_type'] = field.multiValued and 'Multiselect' or ''

            slave.setdefault('control_param', 'master_value')

            template = BINDERS.get(slave.get('action')) or BINDERS['toggle']
            yield template % slave

    def __call__(self, field):
        """render javascript"""
        return JQUERY_ONLOAD % '\n'.join(self.renderJS(field))


class MasterSelectJSONValue(BrowserView):
    """JSON vocabulary or value for the given slave field"""

    def _call_action_method(self, method_name, slave, args):
        method = getattr(self.context, method_name, None)
        if not method and HAS_SCHEMAEXTENDER:
            extenders = [adapter for name, adapter in getAdapters((self.context,), ISchemaExtender)]
            for extender in extenders:
                method = getattr(extender, method_name, None)
                if method:
                    break

        result = method(**args)
        return result

    def getSlaves(self, fieldname):
        return getattr(self.context.Schema()[fieldname].widget, 'slave_fields', ())

    def getVocabulary(self, slave, kw):
        method_name = slave['vocab_method']
        vocabulary = self._call_action_method(method_name, slave, kw)
        slave_name = slave.get('name')
        schema = self.context.Schema()
        field = schema[slave_name]

        actualValue = field.getAccessor(self.context)()
        if not isinstance(actualValue, (list, tuple)):
            actualValue = [actualValue]
        vocabulary = DisplayList(zip(vocabulary, vocabulary))

        json_voc = json.dumps([
            dict(
                value=item,
                label=translate(vocabulary.getValue(item), context=self.request),
                selected=(item in actualValue) and 'selected' or '',
            ) for item in vocabulary
        ])
        return json_voc

    def getValues(self, slave, args):
        method_name = slave['vocab_method']
        vocabulary = self._call_action_method(method_name, slave, args)
        json_values = json.dumps(translate(vocabulary, context=self.request))
        return json_values

    def getToggleValue(self, slave, action, args):
        method_name = slave.get('toggle_method', None)
        if method_name:
            toggle = self._call_action_method(method_name, slave, args)
        else:
            hide_values = slave.get('hide_values')
            if not isinstance(hide_values, [list, tuple]):
                hide_values = (boolean_value(hide_values),)
            toggle = args in hide_values

        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})
        return json_toggle

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')

        field = self.request['field']
        slaveid = self.request['slave']
        value = self.request['value']
        action = self.request['action']

        for slave in self.getSlaves(field):
            if slave['name'] != slaveid or slave['action'] != action:
                continue

            if action not in ['vocabulary', 'value', 'hide', 'show', 'enable', 'disable']:
                raise ValueError('Invalid master-slave action')

            args_name = slave.get('control_param', None)
            decoder = json.JSONDecoder()
            try:
                kwargs = decoder.decode(value)
            except ValueError:
                kwargs = None
            if type(kwargs) is not dict:
                kwargs = args_name and {args_name: value} or value

            if action == 'vocabulary':
                return self.getVocabulary(slave, kwargs)
            elif action == 'value':
                return self.getValues(slave, kwargs)
            elif action in ['hide', 'show', 'enable', 'disable']:
                return self.getToggleValue(slave, action, kwargs)

        raise ValueError('No such master-slave combo')
