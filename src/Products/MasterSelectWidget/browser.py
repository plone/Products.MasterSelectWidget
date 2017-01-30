# -*- coding: utf-8 -*-
try:
    import json
except:
    import simplejson as json

from Products.MasterSelectWidget.config import AVAILABLE_ACTIONS
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
    "'%(absolute_url)s/@@masterselect-jsonvalue-vocabulary');",
    value=SELECT + ".bind%(widget_type)sMasterSlaveValue('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue-values');",
    toggle=SELECT + ".bind%(widget_type)sMasterSlaveToggle('%(name)s', '%(action)s', "
    "'%(absolute_url)s/@@masterselect-jsonvalue-toggle');",
)

JQUERY_ONLOAD = '''\
(function($) { $(function() {
%s
});})(jQuery);
'''


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


class JSONValuesForAction(BrowserView):
    """base class for views called to compute JSON values of an action"""

    def __init__(self, context, request):
        super(JSONValuesForAction, self).__init__(context, request)
        self.field = self.request['field']
        self.slaveid = self.request['slave']
        self.value = self.request['value']
        self.action = self.request['action']

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')

        action = self.action
        value = self.value

        if action not in AVAILABLE_ACTIONS:
            raise ValueError('Invalid master-slave action')

        for slave in self.getSlaves(self.field):
            if slave['name'] != self.slaveid or slave['action'] != action:
                continue
            args = self.extractArguments(slave, value)

            return self.computeJSONValues(slave, args)
        raise ValueError('No such master-slave combo')

    def getSlaves(self, fieldname):
        return getattr(self.context.Schema()[fieldname].widget, 'slave_fields', ())

    def extractArguments(self, slave, value):
        decoder = json.JSONDecoder()
        try:
            args = decoder.decode(value)
        except ValueError:
            args = value
        if type(args) is not list:
            args = [args]
        return args

    def computeJSONValues(self, slave, args):
        """ to override """

    def _call_action_method(self, method_name, slave, args):
        method = getattr(self.context, method_name, None)
        if not method and HAS_SCHEMAEXTENDER:
            extenders = [adapter for name, adapter in getAdapters((self.context,), ISchemaExtender)]
            for extender in extenders:
                method = getattr(extender, method_name, None)
                if method:
                    break

        result = method(*args)
        return result


class JSONValuesForVocabularyChange(JSONValuesForAction):
    """view computing JSON values for 'vocabulary' action"""

    def computeJSONValues(self, slave, args):
        method_name = slave['vocab_method']
        vocabulary = self._call_action_method(method_name, slave, args)
        slave_name = slave.get('name')
        schema = self.context.Schema()
        field = schema[slave_name]

        actualValue = field.getAccessor(self.context)()
        if not isinstance(actualValue, (list, tuple)):
            actualValue = [actualValue]
        vocabulary = DisplayList(zip(vocabulary.keys(), vocabulary.values()))

        json_voc = json.dumps([
            dict(
                value=item,
                label=translate(vocabulary.getValue(item), context=self.request),
                selected=(item in actualValue) and 'selected' or '',
            ) for item in vocabulary
        ])
        return json_voc


class JSONValuesForValueUpdate(JSONValuesForAction):
    """view computing JSON values for 'value' action"""

    def computeJSONValues(self, slave, args):
        method_name = slave['vocab_method']
        vocabulary = self._call_action_method(method_name, slave, args)
        json_values = json.dumps(translate(vocabulary, context=self.request))

        return json_values


class JSONValuesForToggle(JSONValuesForAction):
    """view computing JSON values for 'visibility/availability toggle' action"""

    def computeJSONValues(self, slave, args):
        method_name = slave.get('toggle_method', None)
        if method_name:
            toggle = self._call_action_method(method_name, slave, args)
        else:
            hide_values = slave.get('hide_values')
            if not isinstance(hide_values, (list, tuple)):
                hide_values = (hide_values,)
            values = []
            for val in hide_values:
                if not isinstance(val, str):
                    val = str(bool(val))
                values.append(val)
            toggle = str(args[0]) in values

        action = self.action
        if action in ['disable', 'hide']:
            toggle = not toggle
            action = action == 'disable' and 'enable' or 'show'
        json_toggle = json.dumps({'toggle': toggle, 'action': action})

        return json_toggle
