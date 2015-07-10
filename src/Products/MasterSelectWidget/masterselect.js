(function($) {
    var cache = {}; // Cache AJAX results
    var guid = 0;   // Used to give each handler binding a unique name
    // Anonymizer so we can bind the same handler multiple times per eventtype
    function _anon(f) { return function() { f.apply(this, arguments); }; };

    function bindHandler(field, data, function_to_bind) {
        guid++;
        $(field)
            .find('input:checkbox').bind('click.masterslave' + guid,
                data, _anon(function_to_bind)).end()
            .find('select').bind('change.masterslave' + guid,
                data, _anon(function_to_bind));
    };

    function triggerMultiselect(field) {
        var activate = $(field).find('input:checkbox').first();
        activate.trigger('click.masterslave' + guid).find('input:checkbox');
        activate.is(':checked') ? activate.removeAttr('checked') : activate.attr('checked','checked');
    };

    function triggerSelect(field) {
        $(field)
            .find('input:checkbox').trigger('click.masterslave' + guid).end()
            .find('select').trigger('change.masterslave' + guid);
    };

    function handleMasterFieldAction(event) {
        var fieldname = jQuery(this.closest('div.field')).data('fieldname');
        var args = event.data;
        var slave = args.slaveid;
        var action = args.action;
        var values = args.getValues(this);
        var cachekey = [fieldname, slave, action, values].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url,
                { field: fieldname, slave: slave, action: action, value: values},
                function(data) {
                    cache[cachekey] = data;
                    args.doAction(slave, data);
                });
            else args.doAction(slave, cache[cachekey]);
    };

    function getJSONofMultiSelectValues(field) {
        var field = jQuery(field.closest('div.field'));
        var values = field.find('input:checkbox');
        var listed_values = [];
        for (var i = 0; i < values.length; i++){
            listed_values.push('"' + jQuery(values[i]).attr('value') + '":' + values[i].checked);
        }
        var str_values = '{' + listed_values.join(',') + '}';
        return str_values;
    };

    function getJSONofSingleSelectValue(field) {
        var value = $.nodeName(field, 'input') ? '' + field.checked : $(field).val();
        return value
    };

    // AJAX vocabulary handling
    function updateSelect(field, data) {
        var values = {}; // Remember current selections; reselect afterwards
        $('#archetypes-fieldname-' + field).find('select')
            .each(function() { values[this] = $(this).val() })
            .empty().html( // Replace all options with new ones
                $.map(data, function(entry) {
                    return '<option value="' + entry.value + '" '+ entry.selected +' >' +
                        entry.label + '</option>';
                }).join('')
                ).each(function(){if (!(this.selectedIndex))
                                     $(this).val(values[this])}
                                     ).change();
    };

    // AJAX value handling
    function updateValue(field, data) {
        field = $('#archetypes-fieldname-' + field + ' #' + field);
        field.val(data).change();
        if (field.is('.kupu-editor-textarea')) // update kupu editor too
            field.siblings('iframe:first').contents().find('body').html(data);
    };

    // Field status/visibility toggles
    function toggleField(field, data) {
        var field = $('#archetypes-fieldname-' + field);
        var toggle = data.toggle;
        var action = data.action;
        if (action == 'show')
            field.each(function() { $(this)[ toggle ? "show" : "hide" ]('fast'); });
        if (action == 'enable'){
            if (toggle)
                field.find(':input').removeAttr('disabled');
            else
                field.find(':input').attr('disabled', 'disabled');
        }
    };
    $.fn.bindMultiselectMasterSlaveVocabulary = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getJSONofMultiSelectValues,
            doAction: updateSelect,
        };
        bindHandler(this, data, handleMasterFieldAction)
        triggerMultiselect(this);
    };
    $.fn.bindMasterSlaveVocabulary = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getJSONofSingleSelectValue,
            doAction: updateSelect,
        };
        bindHandler(this, data, handleMasterFieldAction);
        triggerSelect(this);
    };
    $.fn.bindMultiselectMasterSlaveValue= function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getJSONofMultiSelectValues,
            doAction: updateValue,
        };
        bindHandler(this, data, handleMasterFieldAction)
        triggerMultiselect(this);
    };
    $.fn.bindMasterSlaveValue = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getJSONofSingleSelectValue,
            doAction: updateValue,
        };
        bindHandler(this, data, handleMasterFieldAction)
        triggerSelect(this);
    };
    $.fn.bindMultiselectMasterSlaveToggle = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getJSONofMultiSelectValues,
            doAction: toggleField,
        };
        bindHandler(this, data, handleMasterFieldAction)
        triggerMultiselect(this);
    };

    // Field status/visibility toggles
    function handleMasterToggle(event) {
        var action = event.data.action;
        var slave = $('#archetypes-fieldname-' + event.data.slaveid);
        var val = $.nodeName(this, 'input') ? this.checked : $(this).val();
        val = $.inArray(val, event.data.values) > -1;
        if ($.inArray(action, ['hide', 'disable']) > -1) {
            val = !val;
            action = action == 'hide' ? 'show' : 'enable';
        }
        if (action == 'show')
            slave.each(function() { $(this)[ val ? "show" : "hide" ]('fast'); });
        if (action == 'enable'){
            if (val)
                slave.find(':input').removeAttr('disabled');
            else
                slave.find(':input').attr('disabled', 'disabled');
        }
    }
    $.fn.bindMasterSlaveToggle = function(slaveid, action, values) {
        var data = { slaveid: slaveid, action: action, values: values };
        var checkbox = $(this).find('input:checkbox')
        if (!checkbox) {
            return;
        }
        var checked = checkbox.prop('checked');
        $(this)
            .find('select').bind('change.masterslavetoggle' + ++guid, data,
                _anon(handleMasterToggle))
                .trigger('change.masterslavetoggle' + guid).end()
            .find('input:checkbox').bind('click.masterslavetoggle' + ++guid,
                data, _anon(handleMasterToggle))
                .trigger('click.masterslavetoggle' + guid);
        // Maintain the value even though we fired a click event which
        // may have changed it
        checkbox.attr('checked', checked);
    };
})(jQuery);
