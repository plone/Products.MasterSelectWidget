var _registry = new Object();
var _all_keys = new Array();
var _master_elements = new Object();

function getInputElementToModify(form_name, element_id) {
    var cur_form = document.forms[form_name];
    if (typeof(cur_form)=="undefined") {
        alert("The form "+form_name+" could not be found in the document.");
        return;
    }
    var slave_field = cur_form[element_id];
    if (typeof(slave_field)=="undefined") {
        alert("Slave field "+element_id+" could not be found in the form "+form_name);
        return;
    }

    // with checkbox, we get the field *and* the hidden field
    if (typeof(slave_field.type) == "undefined")
        slave_field = slave_field[0];

    return slave_field;
}

function getValueForElement(selectInput) {
    var selectInputValue = '';
    if (selectInput.type == "checkbox") {
        selectInputValue = 'false';
        if (selectInput.checked)
            selectInputValue = 'true';
    } else {
        selectInputValue = selectInput.value;
    }
    return selectInputValue;
}

function modifySlaveField(responseText, cur_sel) {
    switch (cur_sel['action']) {
    case "vocabulary":
        modifyList(responseText, cur_sel);
        break;
    case "value":
        modifySlaveValue(responseText, cur_sel);
        break;
    default:
        // Should not get here
    }
}

function modifySlaveValue(responseText, cur_sel) {
    var cur_elem = getInputElementToModify(cur_sel["form"], cur_sel["slave"]);

    // check for kupu, if classname is kupu-editor-textarea then get it's sibling iframe
    if (cur_elem.className=='kupu-editor-textarea') {
        var iframe = cur_elem.parentNode.getElementsByTagName('iframe')[0];
        iframe.contentWindow.document.body.innerHTML = responseText;
    }
    
    cur_elem.value = responseText;
    // Handle select boxes in all browsers
    if (cur_elem.options)
        for (var i=0; i < cur_elem.options.length; i++)
            if (cur_elem.options[i].value == responseText)
                cur_elem.selectedIndex = i;
    // Pass a bogus event and the real element
    changeOnSelect('', cur_elem);
    if (cur_elem.onchange)
        cur_elem.onchange();
}

function modifyList(list_text, cur_sel) {
    var cur_elem = getInputElementToModify(cur_sel["form"], cur_sel["slave"]);
    var options_array = list_text.split('|');
    var options_length = options_array.length;
    var selected_array = new Array();
    for (var i=0; i < cur_elem.options.length; i++)
        if (cur_elem[i].selected)
            selected_array.push(cur_elem[i].value);
    options_array[0] = options_array[0].replace("<div>","").replace(/^\s*<div>\s*/, "");
    options_array[options_length-1] = options_array[options_length-1].replace(/\s*<\/div>\s*$/, "");
    cur_elem.options.length = 0;
    for (var j=0; j < options_length; j++) {
        var desc_name = options_array[j].split('^');
        var selected = false;
        for (var i=0; i < selected_array.length; i++)
            if (desc_name[1] == selected_array[i])
                selected = true;
        var newOpt = new Option(desc_name[0],desc_name[1], selected, selected);
        newOpt.selected = selected;
        newOpt.defaultSelected = selected;
        cur_elem.options[cur_elem.options.length] = newOpt;
    }
    // Pass a bogus event and the real element
    changeOnSelect('', cur_elem);
    if (cur_elem.onchange)
        cur_elem.onchange();
}

function getNewOptions(selectInput, cur_key) {
    var cur_sel = _registry[cur_key];
    var url = cur_sel["url"];
    var selectInputValue = getValueForElement(selectInput);
    if (cur_sel["last_val"] != selectInputValue) {
        cur_sel["last_val"] = selectInputValue;
        var result = cur_sel["_cache"][selectInputValue];
        if (typeof(result)!="undefined") {
            modifySlaveField(result, cur_sel);
            return;
        }
        var change_func = new Function("selectProcessRequestChange('"+cur_key+"','"+selectInputValue+"');");
        var selectRequest = cur_sel["_request"];
        // Abort any earlier requests on this same key
        if (selectRequest.readyState != 0)
            selectRequest.abort();
        selectRequest.onreadystatechange = change_func;
        selectRequest.open("GET", url + selectInputValue, true );
        selectRequest.send(null);
    }
}

function selectProcessRequestChange(cur_key, selectValue) {
    var cur_sel = _registry[cur_key];
    var selectRequest = cur_sel["_request"];
    if (selectRequest.readyState==4) {
        if (selectRequest.status==200) {
            if (typeof(cur_sel)!="undefined") {
                modifySlaveField(selectRequest.responseText, cur_sel);
                cur_sel["_cache"][selectValue] = selectRequest.responseText;
            }
        } else {
            alert("Problem retrieving XML data from url "+cur_sel["url"]+selectValue)
        }
    }
}

function changeOnSelect(ev, master_element) {
    if (! master_element) {
        if (ev.target)
            var master_element = ev.target;
        else if (ev.srcElement)
            var master_element = ev.srcElement;
        else
            var master_element = this;
    }
    var selectInput = master_element;
    var selectInputValue = getValueForElement(master_element);
    var form_name = master_element.form.name;
    var master_key = form_name+'|'+selectInput.id;
    var key_list = _master_elements[master_key];
    if (typeof(key_list)!="undefined") {
        for (var i=0; i < key_list.length; i++) {
            var cur_key = key_list[i];
            var cur_sel = _registry[cur_key];
            if (typeof(cur_sel)!="undefined") {
                var element_id = cur_sel["slave"];
                switch (cur_sel["action"]) {
                    case "vocabulary":
                    case "value":
                        var cur_elem = getInputElementToModify(form_name, element_id);
                        // Change slave vocabulary
                        getNewOptions(selectInput, cur_key);
                        break;
                    default:
                        var should_hide = inArray(cur_sel["values"], selectInputValue)
                        // We need to look at the whole field because some widgets are quite complex
                        var field_elem = document.getElementById('archetypes-fieldname-'+element_id);
                        if (cur_sel["action"] == "disable")
                            disableField(field_elem, should_hide);
                        else if (cur_sel["action"] == "enable")
                            disableField(field_elem, !should_hide);
                        else if (cur_sel["action"] == "hide")
                            hideField(field_elem, should_hide);
                        else if (cur_sel["action"] == "show")
                            hideField(field_elem, !should_hide);
                }
            }
        }
    }
}

function disableField(field_elem, should_hide) {
    // Special handling for complex widgets
    if (typeof(field_elem.disabled)!="undefined") field_elem.disabled=should_hide;
    // Walk the tree to get disablable elements
    if (field_elem.childNodes)
        for (var i=0; i < field_elem.childNodes.length; i++) {
            var child = field_elem.childNodes[i];
            if (typeof(child.disabled)!="undefined" || child.childNodes) disableField(child, should_hide);
        }
}

function hideField(field_elem, should_hide) {
    // Special handling for complex widgets
    if (should_hide) {
        var vis = "hidden";
        var disp = "none";
    } else {
        var vis = "visible";
        // This may mess with existing css
        var disp = "";
    }

    if (field_elem.style) {
        field_elem.style.visibility = vis;
        field_elem.style.display = disp;
        // Walk the tree to get INPUT element which are explicitly visible
        if (field_elem.childNodes)
            for (var i=0; i < field_elem.childNodes.length; i++) {
                var child = field_elem.childNodes[i];
                if (child.nodeName == "INPUT" || child.childNodes)
                    hideField(child, should_hide);
            }
    }
}

function inArray(list, value) {
    for (var i=0; i < list.length; i++)
        if (list[i] == value)
            return true;
    return false;
}

function registerDynamicSelect(form_name, master_id, slave_id, action, vocab_method, param, base_url) {
    var url;
    switch (action) {
    case "value":
        url = 'getXMLSlaveValue?method='+vocab_method+'&param='+param+'&value=';
        break;
    case "vocabulary":
        url = 'getXMLSelectVocab?method='+vocab_method+'&param='+param+'&value=';
        break;
    default:
        // Should not happen
        alert("registerDynamicSelect: invalid action " + action);
    }
    if (base_url)
        url = base_url + '/' + url;
    var select_desc = new Object();
    var key = form_name+'|'+master_id+'|'+slave_id+'|vocabulary'
    var master_key = form_name+'|'+master_id;
    select_desc["form"] = form_name;
    select_desc["master"] = master_id;
    select_desc["slave"] = slave_id;
    select_desc["action"] = action;
    select_desc["url"] = url;
    select_desc["last_val"] = "";
    select_desc["_cache"] = new Object();
    select_desc["_request"] = new XMLHttpRequest();
    _registry[key] = select_desc;
    var all_children = _master_elements[form_name+'|'+master_id];
    if (typeof(all_children)=="undefined")
        all_children = new Array();
    all_children.push(key);
    _master_elements[master_key] = all_children;
    _all_keys.push(master_key);
}

function registerHideOnSelect(form_name, master_id, slave_id, hide_action, hide_values) {
    var select_desc = new Object();
    var key = form_name+'|'+master_id+'|'+slave_id+'|'+hide_action;
    var master_key = form_name+'|'+master_id;
    select_desc["form"] = form_name;
    select_desc["master"] = master_id;
    select_desc["slave"] = slave_id;
    select_desc["action"] = hide_action;
    select_desc["values"] = hide_values;
    _registry[key] = select_desc;
    var all_children = _master_elements[form_name+'|'+master_id];
    if (typeof(all_children)=="undefined")
        all_children = new Array();
    all_children.push(key);
    _master_elements[master_key] = all_children;
    _all_keys.push(master_key);
}

function dynamicSelectInit() {
    for (var i=0; i < _all_keys.length; i++) {
        var key_list = _master_elements[_all_keys[i]];
        // Just get the first one for a given master
        var cur_sel = _registry[key_list[0]];
        var master = getInputElementToModify(cur_sel["form"],cur_sel["master"]);
        var e = 'change'; 
        if (master.type == 'checkbox') 
            e = 'click'; 
        if (master.addEventListener)
            master.addEventListener(e, changeOnSelect, false);
        else if (master.attachEvent)
            master.attachEvent('on'+e, changeOnSelect);
            changeOnSelect('', master);
    }
}

if (window.addEventListener)
    window.addEventListener("load", dynamicSelectInit, false);
else if (window.attachEvent)
    window.attachEvent("onload", dynamicSelectInit);
