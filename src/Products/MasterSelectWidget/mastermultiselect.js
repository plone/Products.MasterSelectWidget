(function($) {
    var cache = {}; // Cache AJAX results
    var guid = 0;   // Used to give each handler binding a unique name
    // Anonymizer so we can bind the same handler multiple times per eventtype
    function _anon(f) { return function() { f.apply(this, arguments); }; };

    function bindAndTrigger(field, data, function_to_bind) {
        $(field)
            .find('input:checkbox').bind('click.masterslavevalue' + ++guid,
                data, _anon(function_to_bind));
        //trigger the event once, then restore the checked box to its original value
        var activate = $(field).find('input:checkbox').first();
        activate.trigger('click.masterslavevalue' + guid);
        activate.is(':checked') ? activate.removeAttr('checked') : activate.attr('checked','checked');
    };

    function handleMasterFieldAction(event) {
        var field = jQuery(this.closest('div.field'));
        var fieldname = field.data('fieldname');
        var args = event.data;
        var slave = args.slaveid;
        var action = args.action;
        var values = args.getValues(field);
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

    function getMultiSelectedValuesJSON(field) {
        var values = field.find('input:checkbox');
        var listed_values = [];
        for (var i = 0; i < values.length; i++){
            listed_values.push('"' + jQuery(values[i]).attr('value') + '":' + values[i].checked);
        }
        var str_values = '{' + listed_values.join(',') + '}';
        return str_values;
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
    $.fn.bindMultiselectMasterSlaveVocabulary = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getMultiSelectedValuesJSON,
            doAction: updateSelect,
        };
        bindAndTrigger(this, data, handleMasterFieldAction);
    };

    // AJAX value handling
    function updateValue(field, data) {
        field = $('#archetypes-fieldname-' + field + ' #' + field);
        field.val(data).change();
        if (field.is('.kupu-editor-textarea')) // update kupu editor too
            field.siblings('iframe:first').contents().find('body').html(data);
    };
    $.fn.bindMultiselectMasterSlaveValue= function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getMultiSelectedValuesJSON,
            doAction: updateValue,
        };
        bindAndTrigger(this, data, handleMasterFieldAction);
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
    }
    $.fn.bindMultiselectMasterSlaveToggle = function(slaveid, action, url) {
        var data = {
            slaveid: slaveid,
            action: action,
            url: url,
            getValues: getMultiSelectedValuesJSON,
            doAction: toggleField,
        };
        bindAndTrigger(this, data, handleMasterFieldAction);
    };
})(jQuery);
