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
    vocabulary=SELECT + ".bind%(widget_type)sMasterSlaveVocabulary('%(name)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue');",
    value=SELECT + ".bind%(widget_type)sMasterSlaveValue('%(name)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue');",
    toggle=SELECT + ".bind%(widget_type)sMasterSlaveToggle('%(name)s', '%(action)s', "
    "%(hidden)s);",
    multi_toggle=SELECT + ".bind%(widget_type)sMasterSlaveToggle('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue-yolo');",
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
            hidden = '[]'
            if 'hide_values' in slave:
                values = slave['hide_values']
                if not isinstance(values, (tuple, list)):
                    values = [values]
                if field.type == 'boolean':
                    values = [boolean_value(v) for v in values]
                else:
                    values = [str(v) for v in values]
                hidden = json.dumps(values)
            slave['hidden'] = hidden

            toggle_type = field.multiValued and 'multi_toggle' or 'toggle'
            template = BINDERS.get(slave.get('action')) or BINDERS[toggle_type]
            yield template % slave

    def __call__(self, field):
        """render javascript"""
        return JQUERY_ONLOAD % '\n'.join(self.renderJS(field))


class MasterSelectJSONValue(BrowserView):
    """JSON vocabulary or value for the given slave field"""

    def getSlaves(self, fieldname):
        return getattr(self.context.Schema()[fieldname].widget, 'slave_fields', ())

    def getVocabulary(self, slave, kw):
        method_name = slave['vocab_method']
        vocabulary = self._call_custom_method(method_name, slave, kw)
        slave_name = slave.get('name')
        schema = self.context.Schema()
        field = schema[slave_name]

        actualValue = field.getAccessor(self.context)()
        if not isinstance(actualValue, list):
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

    def getValues(self, slave, kw):
        method_name = slave['vocab_method']
        vocabulary = self._call_custom_method(method_name, slave, kw)
        json_values = json.dumps(translate(vocabulary, context=self.request))
        return json_values

    def getToggleValue(self, slave, action, kw):
        method_name = slave['toggle_method']
        toggle = self._call_custom_method(method_name, slave, kw)
        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})
        return json_toggle

    def _call_custom_method(self, method_name, slave, kw):
        method = getattr(self.context, method_name, None)
        if not method and HAS_SCHEMAEXTENDER:
            extenders = [adapter for name, adapter in getAdapters((self.context,), ISchemaExtender)]
            for extender in extenders:
                method = getattr(extender, method_name, None)
                if method:
                    break

        result = method(**kw)
        return result

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')

        field = self.request['field']
        slaveid = self.request['slave']
        value = self.request['value']

        for slave in self.getSlaves(field):
            if slave['name'] != slaveid:
                continue

            action = slave.get('action')
            if action not in ['vocabulary', 'value', 'hide', 'disable']:
                raise ValueError('Invalid master-slave action')

            decoder = json.JSONDecoder()
            try:
                kw = decoder.decode(value)
            except ValueError:
                kw = {slave['control_param']: value}
            if type(kw) is not dict:
                kw = {slave['control_param']: kw}

            if action == 'vocabulary':
                return self.getVocabulary(slave, kw)
            elif action == 'value':
                return self.getValues(slave, kw)
            elif action in ['hide', 'show', 'enable', 'disable']:
                return self.getToggleValue(slave, action, kw)

        raise ValueError('No such master-slave combo')


class MasterSelectJSONValueYOLO(BrowserView):
    """JSON vocabulary or value for the given slave field"""

    def getSlaves(self, fieldname):
        return getattr(self.context.Schema()[fieldname].widget, 'slave_fields', ())

    def getVocabulary(self, slave, kw):
        method_name = slave['vocab_method']
        vocabulary = self._call_custom_method(method_name, slave, kw)
        slave_name = slave.get('name')
        schema = self.context.Schema()
        field = schema[slave_name]

        actualValue = field.getAccessor(self.context)()
        if not isinstance(actualValue, list):
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

    def getValues(self, slave, kw):
        method_name = slave['vocab_method']
        vocabulary = self._call_custom_method(method_name, slave, kw)
        json_values = json.dumps(translate(vocabulary, context=self.request))
        return json_values

    def getToggleValue(self, slave, action, kw):
        method_name = slave['toggle_method']
        toggle = self._call_custom_method(method_name, slave, kw)
        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})
        return json_toggle

    def _call_custom_method(self, method_name, slave, kw):
        method = getattr(self.context, method_name, None)
        if not method and HAS_SCHEMAEXTENDER:
            extenders = [adapter for name, adapter in getAdapters((self.context,), ISchemaExtender)]
            for extender in extenders:
                method = getattr(extender, method_name, None)
                if method:
                    break

        result = method(**kw)
        return result

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')

        field = self.request['field']
        slaveid = self.request['slave']
        value = self.request['value']
        action = self.request['action']

        for slave in self.getSlaves(field):
            if slave['name'] != slaveid or slave['action'] != action:
                continue

            action = slave.get('action')
            if action not in ['vocabulary', 'value', 'hide', 'disable', 'enable']:
                raise ValueError('Invalid master-slave action')

            decoder = json.JSONDecoder()
            try:
                kw = decoder.decode(value)
            except ValueError:
                kw = {slave['control_param']: value}
            if type(kw) is not dict:
                kw = {slave['control_param']: kw}

            return self.getToggleValue(slave, action, kw)

        raise ValueError('No such master-slave combo')
