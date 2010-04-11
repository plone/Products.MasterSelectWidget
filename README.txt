Overview
========

This is an Archetypes widget which controls the vocabulary or display
of other fields on an edit page. It needs to be given information about
which fields to control and how to control them.

To install it just extract into your products directory, restart zope,
and install it with the QuickInstaller.

Usage
=====

To use it just create a field like::

    StringField(
        name='master_field',
        default='',
        vocabulary=DisplayList(
            (('week', 'Week'),
              ('wedding','Wedding'),
              ('winona','Winona'),
              ('winter', 'Winter'),
              ('weather','Weather'),
              ('cow', 'Cow'),
            ),
        ),
        widget=MasterSelectWidget(
            label='Test Widget',
            description='Test this',
            slave_fields=(
                {'name': 'slave_field_name',
                  'action': 'vocabulary',
                  'vocab_method': 'mySlaveVocabularyMethod',
                  'control_param': 'my_method_parameter',
                },
            ),
        ),
    ),

You can use any field type compatible with a normal SelectWidget. And
you may use any of the normal SelectWidget parameters (except 'format',
which must be set to 'select'). It will appear and behave like a normal
SelectWidget, but changes in this widget will affect the widgets described
in the slave_fields parameter.


Parameters
==========

All the magic happens in the slave_fields parameter which should be a
sequence of mappings. Each mapping is a description of a field controlled
by this master field:

name
  The name of the field to control on when the selection changes. The
  controlled field/widget may be of any type unless the 'vocabulary' or
  'value' action is used. When the action is 'vocabulary', the field must
  use either a MultiSelectionWidget, a SelectionWidget, or a
  MasterSelectWidget any of which must have the 'format' parameter set
  to 'select' (this is the default only for MasterSelectWidget). For
  'value', the widget must be simple enough to change the current value
  using element.value or elem.selectedIndex (StringWidget, SelectionWidget,
  AutoCompleteWidget, maybe others).

action
  The type of action to perform on the slave field.  This can be
  'vocabulary', which alters the vocabulary of the slave field using an
  XMLHttpRequest call; 'hide' or 'show' which sets the slave field's
  visibility style attribute; 'enable' or 'disable' which marks the
  target widget as enabled or disabled; or 'value' which alters the
  value of another simple widget (StringWidget) on selection change
  using an XMLHttpRequest call. To use the 'vocabulary' action, the
  slave field must meet the widget requirements stated above. To use
  the 'enable'/'disable' actions, the field must use a HTML widget
  that can be enabled/disabled.

vocab_method
  The name of a method to call to retrieve the dynamic vocabulary for
  the slave field, or the value for the slave field when 'value' is used.
  For 'vocabulary', this must return a DisplayList. For 'value, it must
  return a string or msg_id.  The method must accept a parameter which
  will be used to pass the new value selected in the master widget. The
  name of this parameter defaults to 'master_value', but any name may be
  used as long as it is specified using the control_param element. Used
  only with 'action':'vocabulary' or 'action':'value'.

control_param
  As described above, this is the name of the paramter used when
  calling the vocab_method. Used only with 'action':'vocabulary'
  or 'action':'value'.

hide_values
  A sequence of values which when selected in the master widget cause
  the slave field/widget to be hidden, shown or disabled. The method
  used is determined by the 'action' element. Used only with
  'action':'hide', 'action':'enable', 'action':'disable' or
  'action':'show'.

A single MasterSelectWidget may control any number of slave fields, new
fields are controlled by adding new mappings to the slave_fields list/tuple.
A field which is the target of a MasterSelectWidget action may itself use
a MasterSelectWidget to control other fields.

The MasterSelectDemo type includes a number of master and slave widgets in
different configurations.

To enable the demo type go to portal_setup, hit the `Import` tab, select the
`MasterSelectWidget demo` profile and click the `Import all steps` button at the bottom.

Enjoy!


Credits
=======

Author
  Alec Mitchell: apm13@columbia.edu

Contributor
  Dorneles Tremea: deo@plonesolutions.com
