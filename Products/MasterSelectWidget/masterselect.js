(function($) {
    var cache = {}; // Cache AJAX results
    var guid = 0;   // Used to give each handler binding a unique name
    // Anonymizer so we can bind the same handler multiple times per eventtype
    function _anon(f) { return function() { f.apply(this, arguments); }; };
    
    // AJAX vocabulary handling
    function updateSelect(field, data) {
        var values = {}; // Remember current selections; reselect afterwards
        $('#archetypes-fieldname-' + field).find('select')
            .each(function() { values[this] = $(this).val() })
            .empty().html( // Replace all options with new onesguid
                $.map(data, function(entry) {
                    return '<option value="' + entry.value + '">' + 
                        entry.label + '</option>';
                }).join('')
            ).each(function() { $(this).val(values[this]); }).change();
    };
    function handleMasterVocabularyChange(event) {
        var value = $.nodeName(this, 'input') ? 
            '' + this.checked : $(this).val();
        var slave = event.data.slaveid;
        var cachekey = [this.id, slave, value].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url, 
                { field: this.id, slave: slave, value: value },
                function(data) {
                    cache[cachekey] = data;
                    updateSelect(slave, data);
                });
            else updateSelect(slave, cache[cachekey]);        
    };
    $.fn.bindMasterSlaveVocabulary = function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        $(this)
            .find('select').bind('change.masterslavevocabulary' + ++guid,
                data, _anon(handleMasterVocabularyChange))
                .trigger('change.masterslavevocabulary' + guid).end()
            .find('input:checkbox').bind(
                'click.masterslavevocabulary' + ++guid, data, 
                _anon(handleMasterVocabularyChange))
                .trigger('click.masterslavevocabulary' + guid);
    };
    
    // AJAX value handling
    function handleMasterValueChange(event) {
        var value = $.nodeName(this, 'input') ? 
            '' + this.checked : $(this).val();
        var slave = event.data.slaveid;
        var cachekey = [this.id, slave, value].join(':');
        var target = $('#archetypes-fieldname-' + slave + ' #' + slave);
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url, 
                { field: this.id, slave: slave, value: value },
                function(data) {
                    cache[cachekey] = data;
                    target.val(data).change();
                    if (target.is('.kupu-editor-textarea'))
                        target.siblings('iframe:first').contents().find('body')
                            .html(data);
                });
            else {
                target.val(cache[cachekey]).change();
                if (target.is('.kupu-editor-textarea'))
                    target.siblings('iframe:first').contents().find('body')
                        .html(cache[cachekey]);
            }
    };
    $.fn.bindMasterSlaveValue = function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        $(this)
            .find('select').bind('change.masterslavevalue' + ++guid, data,
                _anon(handleMasterValueChange))
                .trigger('change.masterslavevalue' + guid).end()
            .find('input:checkbox').bind('click.masterslavevalue' + ++guid,
                data, _anon(handleMasterValueChange))
                .trigger('click.masterslavevalue' + guid);
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
            slave.each(function() { $(this)[ val ? "show" : "hide" ](); });
        else
            slave.find(':input').attr('disabled', val ? '' : 'disabled');
    }
    $.fn.bindMasterSlaveToggle = function(slaveid, action, values) {
        var data = { slaveid: slaveid, action: action, values: values };
        $(this)
            .find('select').bind('change.masterslavetoggle' + ++guid, data,
                _anon(handleMasterToggle))
                .trigger('change.masterslavetoggle' + guid).end()
            .find('input:checkbox').bind('click.masterslavetoggle' + ++guid,
                data, _anon(handleMasterToggle))
                .trigger('click.masterslavetoggle' + guid);
    };
})(jQuery);
