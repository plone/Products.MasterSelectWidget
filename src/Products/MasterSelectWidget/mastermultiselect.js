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

    function getSelectedValuesJSON(field) {
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
    function handleMasterVocabularyChange(event) {
        var field = jQuery(this.closest('div.field'));
        var fieldname = field.data('fieldname');
        var values = getSelectedValuesJSON(field);
        var slave = event.data.slaveid;
        var cachekey = [fieldname, slave, values].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url,
                { field: fieldname, slave: slave, value: values },
                function(data) {
                    cache[cachekey] = data;
                    updateSelect(slave, data);
                });
            else updateSelect(slave, cache[cachekey]);
    };
    $.fn.bindMultiselectMasterSlaveVocabulary = function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        bindAndTrigger(this, data, handleMasterVocabularyChange);
    };

    // AJAX value handling
    function updateValue(field, data) {
        field = $('#archetypes-fieldname-' + field + ' #' + field);
        field.val(data).change();
        if (field.is('.kupu-editor-textarea')) // update kupu editor too
            field.siblings('iframe:first').contents().find('body').html(data);
    }
    function handleMasterValueChange(event) {
        var field = jQuery(this.closest('div.field'));
        var fieldname = field.data('fieldname');
        var values = getSelectedValuesJSON(field);
        var slave = event.data.slaveid;
        var cachekey = [fieldname, slave, values].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url,
                { field: fieldname, slave: slave, value: values},
                function(data) {
                    cache[cachekey] = data;
                    updateValue(slave, data);
                });
            else updateValue(slave, cache[cachekey]);
    };
    $.fn.bindMultiselectMasterSlaveValue= function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        bindAndTrigger(this, data, handleMasterValueChange);
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
    $.fn.bindMultiselectMasterSlaveToggle = function(slaveid, action, values) {
        var data = { slaveid: slaveid, action: action, values: values };
        bindAndTrigger(this, data, handleMasterToggle);
    };
})(jQuery);
