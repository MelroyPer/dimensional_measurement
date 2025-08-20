var getXmlValue = function (str, key) {
    return str.substring(
        str.lastIndexOf('<' + key + '>') + ('<' + key + '>').length,
        str.lastIndexOf('</' + key + '>')
    );
}

function removeSpaces(string) {
    return string.split(' ').join('');
}

function showProgress() {
    $("#divPageLoading").attr("style", "display:flex;align-items:center;justify-content:center;vertical-align: middle;color:#fff;");
}

function hideProgress() {
    $('#divPageLoading').hide();
}

function ProgressBarModal(showHide) {
    if (showHide === 'show') {
        $('#mod-progress').modal('show');
        if (arguments.length >= 2) {
            $('#progressBarParagraph').text(arguments[1]);
        } else {
            $('#progressBarParagraph').text('Failed...');
        }
    }
    else if (showHide === 'start') {
        $('#mod-progress').modal('show');
        $('#progressBarParagraph').text('Loading, Please wait...');
    }
    else {
    }
}

function sortByKeyDesc(array, key) {
    return array.sort(function (a, b) {
        var x = a[key]; var y = b[key];
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
}
function sortByKeyAsc(array, key) {
    return array.sort(function (a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}


/* Validation. */
function PositiveAndNegativeNumberOnly() {
    var AsciiValue = event.keyCode
    if ((AsciiValue >= 48 && AsciiValue <= 57) || (AsciiValue == 8 || AsciiValue == 127) || (AsciiValue == 45))
        event.returnValue = false;
    else
        event.returnValue = true;
}

function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode == 36 && charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}
function fncKeyLength(num) {
    var key;
    if (window.event) {
        key = window.event.keyCode; //IE
        IsCtrl = window.event.ctrlKey;
    }
    else {
        key = e.which; //firefox
        IsCtrl = e.ctrlKey;
    }
    if (IsCtrl && (key == 118 || key == 86)) {

        var ctlid = document.getElementById(num.id);
        var ctlvalue = ctlid.value;
        ctlid.value = Math.round(ctlvalue);
    }
}


function DrawCaptcha() {
    var a = Math.ceil(Math.random() * 9) + '';
    var b = Math.ceil(Math.random() * 9) + '';
    var c = Math.ceil(Math.random() * 9) + '';
    var d = Math.ceil(Math.random() * 9) + '';
    var e = Math.ceil(Math.random() * 9) + '';
    var f = Math.ceil(Math.random() * 9) + '';
    var g = Math.ceil(Math.random() * 9) + '';
    var h = Math.ceil(Math.random() * 9) + '';
    var i = Math.ceil(Math.random() * 9) + '';
    var j = Math.ceil(Math.random() * 9) + '';
    var code = "0";
    var cptLength = '4';
    if (cptLength == '1') {
        code = a;
    }
    else if (cptLength == '2') {
        code = a + ' ' + b;
    }
    else if (cptLength == '3') {
        code = a + ' ' + b + ' ' + c;
    }
    else if (cptLength == '4') {
        code = a + ' ' + b + ' ' + c + ' ' + d;

    }
    else if (cptLength == '5') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e;
    }
    else if (cptLength == '6') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f;
    }
    else if (cptLength == '7') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f + ' ' + g;
    }
    else if (cptLength == '8') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f + ' ' + g + ' ' + h;
    }
    else if (cptLength == '9') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f + ' ' + g + ' ' + h + ' ' + i;
    }
    else if (cptLength == '10') {
        code = a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f + ' ' + g + ' ' + h + ' ' + i + ' ' + j;
    }
    else { code = a + ' ' + b + ' ' + c; } //default}

    document.getElementById("txtCaptcha").value = code;
}


/* Autocomplete funcation */
var Constant = {
    contenttype: 'application/json; charset=utf-8'
};
var CommonUtility = {};

CommonUtility.RequestAjax = function (type, url, data, sucess, cache, complete, error, datatype) {
    sucess === undefined || sucess === null ? function (response) { alert(response) } : sucess;
    error === undefined || error === null ? function (xhr) {
        alert("error");
        if (xhr.status == 401) {
            window.location.href = '/Login/Index';
        }
    } : error;
    datatype === undefined || datatype === null ? "html" : datatype;
    var beforeSend = function beforeSend() {
        $("#ajaxLoader").show();
        $("#ajaxLoaderImage").show();
    };
    var failure = function failure() { alert("Error"); };
    var complete = function complete() {
        $("#ajaxLoader").hide();
        $("#ajaxLoaderImage").hide();
    };

    return $.ajax({
        url: url,
        data: data,
        cache: cache === null || cache === undefined || cache === '' ? false : cache,
        datatype: datatype,
        type: type,
        contenttype: datatype === "html" ? Constant.contenttype : "application/json",
        success: sucess,
        error: error,
        failure: failure,
        beforeSend: beforeSend,
        complete: complete
    })
}
CommonUtility.DeleteAjax = function (url, data, sucess) {
    if (!confirm('Do you really want to delete this?')) {
        return true;
    }
    sucess === undefined || sucess === null ? function (response) {
        alert(response)
    } : sucess;
    jQuery.ajax({
        url: url,
        type: 'DELETE',
        data: data,
        success: sucess,
        error: function (xhr) {
            alert("Error");
        }
    });
}
CommonUtility.CustomAutoComplete = function (request, response, Url, type, dataslicecount) {
    var Search = {};
    if (type != '' || type != null) {
        if ($.isArray(type)) {
            Search = CommonUtility.formedJSON2Object(type[0]);
        }
        else {
            Search['Type'] = type;
        }
    }
    Search['Name'] = request.term;
    Search['Prefix'] = request.term;

    $.ajax({
        url: Url,
        data: "{ 'Prefix': '" + request.term + "'}",
        dataType: "json",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            if (!data.d.length) {
                var result = [
                    {
                        label: 'No Results Found',
                        value: response.term
                    }
                ];
                response(result);
            } else {
                if (dataslicecount > 0) { data.d = data.d.slice(0, dataslicecount); }
                response($.map(data.d, function (item) {
                    return {
                        label: item,//item.split('-')[0],
                        val: item//item.split('-')[1]
                    }
                }))
            }
        },
        error: function (response) {
            console.log(response.responseText);
        },
        failure: function (response) {
            console.log(response.responseText);
        }
    });
}

CommonUtility.formedJSON2Object = function (tar) {
    var obj = {};
    tar = tar.replace(/^\{|\}$/g, '').split(',');
    for (var i = 0, cur, pair; cur = tar[i]; i++) {
        pair = cur.split(':');
        obj[pair[0]] = /^\d*$/.test(pair[1]) ? +pair[1] : pair[1];
    }
    return obj;
}

CommonUtility.CustomFullAutoComplete = function (sourcectrl, destctrl, url, flag = '', destctrlDataType = '00000000-0000-0000-0000-000000000000', checkselecteditem = true, dataslicecount = 0, isrequiredid = false) {
    $(sourcectrl.selector).autocomplete({
        source: function (request, response) {
            if (destctrl != null || destctrl != '') { $(destctrl.selector).val(destctrlDataType); }
            if (request.term.trim() !== "") {
                CommonUtility.CustomAutoComplete(request, response, url, flag, dataslicecount);
            }
        },
        select: function (e, i) {
            if (i.item.label === "No Results Found") {
                e.preventDefault();
                if (destctrl != null || destctrl != '') { $(destctrl.selector).val(destctrlDataType); }
            } else {
                if (destctrl != null || destctrl != '') { $(destctrl.selector).val(isrequiredid == true ? i.item.id : i.item.val); }
            }
        },
        close: function (e) {
            if (destctrl != null || destctrl != '') {
                if ($(destctrl.selector).val() === destctrlDataType && checkselecteditem == true) {
                    e.target.value = '';
                }
            }
        },
        minLength: 0
    });
}

//String Validation
$(function () {
    const regex_OnlyAlphabets = /^[a-zA-Z0-9.\-+±_/ ]+$/;
    const regex_OnlyAlphaNumeric = /^[a-zA-Z0-9]+$/;
    const regex_OnlyNumbers = /^-?\d*[.]?\d*$/;
    const regex_OnlyAmount = /^-?\d*[.]?\d*$/;
    
    $(".OnlyAlphabets").on("keypress", function (e) {
        var keyCode = e.keyCode || e.which;
        var isValid = regex_OnlyAlphabets.test(String.fromCharCode(keyCode));
        if (!isValid) {
            e.preventDefault();
        }
    });
    $(".OnlyAlphabets").on("paste", function (e) {
        var pastedData = e.originalEvent.clipboardData.getData('text/plain');
        if (pastedData) {
            if (!regex_OnlyAlphabets.test(pastedData)) {
                e.preventDefault();
                ErroralertJS('Only alphabets are allowed.');
            }
        }
    });
    $(".OnlyAlphaNumeric").on("keypress", function (e) {
        var keyCode = e.keyCode || e.which;
        var isValid = regex_OnlyAlphaNumeric.test(String.fromCharCode(keyCode));
        if (!isValid) {
            e.preventDefault();
        }
    });
    $(".OnlyAlphaNumeric").on("paste", function (e) {
        var pastedData = e.originalEvent.clipboardData.getData('text/plain');
        if (pastedData) {
            if (!regex_OnlyAlphaNumeric.test(pastedData)) {
                e.preventDefault();
                ErroralertJS('Only alphanumeric are allowed.');
            }
        }
    });
    $(".OnlyNumbers").on("keypress", function (e) {
        var keyCode = e.keyCode || e.which;
        var isValid = regex_OnlyNumbers.test(String.fromCharCode(keyCode));
        if (!isValid) {
            e.preventDefault();
        }
    });
    $(".OnlyNumbers").on("paste", function (e) {
        var pastedData = e.originalEvent.clipboardData.getData('text/plain');
        if (pastedData) {
            if (!regex_OnlyNumbers.test(pastedData)) {
                e.preventDefault();
                ErroralertJS('Only digits are allowed.');
            }
        }
    });
    $(".Amount").on("keypress", function (e) {
        var keyCode = e.keyCode || e.which;
        var inputChar = String.fromCharCode(keyCode);
        var currentValue = $(this).val();

        if (inputChar === '-' && currentValue === '') {
            return;
        }
         
        var isValid = regex_OnlyAmount.test(currentValue + inputChar);
        if (!isValid) {
            e.preventDefault();
        }
    });
    $(".Amount").on("paste", function (e) {
        var pastedData = e.originalEvent.clipboardData.getData('text/plain');
        if (pastedData) {
            if (!regex_OnlyAmount.test(pastedData)) {
                e.preventDefault();
                ErroralertJS('Only digits are allowed.');
            }
        }
    });
    $('.WordCapsStarteLetter').keyup(function () {
        var input = $(this);
        input.val(input.val().replace(/\b\w+/g, function (word) {
            return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
        }));
    });
});