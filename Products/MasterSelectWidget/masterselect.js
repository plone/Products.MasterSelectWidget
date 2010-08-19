(function($) {
    var cache = {}; // Cache AJAX results
    var guid = 0;   // Used to give each handler binding a unique name
    // Anonymizer so we can bind the same handler multiple times per eventtype
    function _anon(f) { return function() { f.apply(this, arguments); }; };

    function justValue(el, master, multivalued) {
        master = typeof(master) != 'undefined' ? master : null;
        multivalued = typeof(multivalued) != 'undefined' ? multivalued : false;
        var $el = $(el);
        if ($el.is('select')) {
            return $el.val()
        } else if ($el.is('input:radio')) {
            return $el.val()
        } else if ($el.is('input:checkbox')) {
            if (master != null && multivalued) {
                // return all checked values of the field with name set in 'master'
                var result = new Array();
                $el.closest('[id='+master+']').find('[name^='+master+']').each(function() {
                    if($(this).attr('checked')) {
                        result.push($(this).val());
                    }
                });
                return result;
            } else {
                return $el.attr('checked');
            }
        } 
    }
    function typeAndValue(el) {
        // Returns type of widget and it's value
        var result = new Object();
        var $items = $(el).find('select');
        if ($items.length == 1) {
            result.type = 'select';
            result.value = $($items[0]).val();
        } else {
            $items = $(el).find('input:checkbox');
            if ($items.length == 1) {
                result.type = 'checkbox';
                result.value = $($items[0]).attr('checked');
            } else if ($items.length > 1) {
                result.type = 'multicheckbox';
                result.value = new Array();
                $items.each(function() {
                    if (this.checked) {
                        result.value.push($(this).val())
                    }
                });
            } else {
                $items = $(el).find('input:radio');
                if ($items.length > 0) {
                    result.type = 'radio';
                    result.value = null;
                    $items.each(function() {
                        if (this.checked) {
                            result.value = $(this).val();
                            return false;
                        }
                    });
                }
            }
        }
        return result;
    }
    function cleanedName(name) {
        // clean input name from zope type selectors (eg name:list) 
        return name.split(':',1)[0];
    }
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
        var value = justValue(this);
        var slave = event.data.slaveid;
        var name = cleanedName(this.name);
        var cachekey = [name, slave, value].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url, 
                { field: name, slave: slave, value: value },
                function(data) {
                    cache[cachekey] = data;
                    updateSelect(slave, data);
                });
            else updateSelect(slave, cache[cachekey]);        
    };
    $.fn.bindMasterSlaveVocabulary = function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        var val = typeAndValue(this);
        if (val.type == 'select') {
            var $items = $(this).find('select');
            $items.bind('change.masterslavevocabulary' + ++guid, data,
                    _anon(handleMasterVocabularyChange))
                    .trigger('change.masterslavevocabulary' + guid);
        }
        if (val.type == 'checkbox') {
            var $items = $(this).find('input:checkbox');
            $items.bind('click.masterslavevocabulary' + ++guid,
                data, _anon(handleMasterVocabularyChange))
                .trigger('click.masterslavevocabulary' + guid);
        }
        if (val.type == 'multicheckbox') {
            var $items = $(this).find('input:checkbox');
            // data.multivalued = true;
            alert('Not implemented');
        }
        if (val.type == 'radio') {
            var $items = $(this).find('input:radio');
            var $bound = $items.bind('click.masterslavevocabulary' + ++guid,
                data, _anon(handleMasterVocabularyChange));
        }
    };
    
    // AJAX value handling
    function updateValue(field, data) {
        field = $('#archetypes-fieldname-' + field + ' #' + field);
        field.val(data).change();
        if (field.is('.kupu-editor-textarea')) // update kupu editor too
            field.siblings('iframe:first').contents().find('body').html(data);
    }
    function handleMasterValueChange(event) {
        var value = justValue(this);
        var slave = event.data.slaveid;
        var name = cleanedName(this.name);
        var cachekey = [name, slave, value].join(':');
        if (cache[cachekey] == undefined)
            $.getJSON(event.data.url, 
                { field: name, slave: slave, value: value },
                function(data) {
                    cache[cachekey] = data;
                    updateValue(slave, data);
                });
            else updateValue(slave, cache[cachekey]);
    };
    $.fn.bindMasterSlaveValue = function(slaveid, url) {
        var data = { slaveid: slaveid, url: url };
        var val = typeAndValue(this);
        if (val.type == 'select') {
            var $items = $(this).find('select');
            $items.bind('change.masterslavevalue' + ++guid, data,
                    _anon(handleMasterValueChange))
                    .trigger('change.masterslavevalue' + guid);
        }
        if (val.type == 'checkbox') {
            var $items = $(this).find('input:checkbox');
            $items.bind('click.masterslavevalue' + ++guid,
                data, _anon(handleMasterValueChange))
                .trigger('click.masterslavevalue' + guid);
        }
        if (val.type == 'multicheckbox') {
            var $items = $(this).find('input:checkbox');
            // data.multivalued = true;
            alert('Not implemented');
        }
        if (val.type == 'radio') {
            var $items = $(this).find('input:radio');
            var $bound = $items.bind('click.masterslavevalue' + ++guid,
                data, _anon(handleMasterValueChange));
        }
    };
    
    // Field status/visibility toggles
    function handleMasterToggle(event) {
        var action = event.data.action;
        var slave = $('#archetypes-fieldname-' + event.data.slaveid);
        var val = justValue(this, event.data.master, event.data.multivalued);
        if (!jq.isArray(val)) {
            val = $.inArray(val, event.data.values) > -1;
        } else {
            var result = false;
            $.each(val, function(idx, name) {
                if ($.inArray(name, event.data.values) > -1){
                    result = true;
                    return false
                }
            });
            val = result;
        }
        if ($.inArray(action, ['hide', 'disable']) > -1) {
            val = !val;
            action = action == 'hide' ? 'show' : 'enable';
        }
        if (action == 'show')
            slave.each(function() { $(this)[ val ? "show" : "hide" ](); });
        else
            slave.find(':input').attr('disabled', val ? '' : 'disabled');
    }
    $.fn.bindMasterSlaveToggle = function(slaveid, action, values, master) {
        var data = { slaveid: slaveid, 
                     action: action, 
                     values: values, 
                     multivalued: false, 
                     master: master };
        var val = typeAndValue(this);
        if (val.type == 'select') {
            var $items = $(this).find('select');
            $items.bind('change.masterslavetoggle' + ++guid, data,
                    _anon(handleMasterToggle))
                    .trigger('change.masterslavetoggle' + guid);
        }
        if (val.type == 'checkbox') {
            var $items = $(this).find('input:checkbox');
            $items.bind('click.masterslavetoggle' + ++guid,
                data, _anon(handleMasterToggle))
                .trigger('click.masterslavetoggle' + guid);
            // set the original value
            $items.attr('checked', val.value);
        }
        if (val.type == 'multicheckbox') {
            var $items = $(this).find('input:checkbox');
            data.multivalued = true;
            var $bound = $items.bind('click.masterslavetoggle' + ++guid,
                data, _anon(handleMasterToggle))
                .trigger('click.masterslavetoggle' + guid);
            $bound.each(function() {
                $item = $(this);
                $item.attr('checked', $.inArray($item.val(), val.value) == -1 ? null : 'checked')
            })
        }
        if (val.type == 'radio') {
            var $items = $(this).find('input:radio');
            var $bound = $items.bind('click.masterslavetoggle' + ++guid,
                data, _anon(handleMasterToggle));
            if (val.value != null) {
                // click at default value
                $bound.each(function() {
                    if ($(this).val() == val.value) {
                        $(this).trigger('click');
                        return false;
                    }
                })
            }
        }
    };
})(jQuery);
