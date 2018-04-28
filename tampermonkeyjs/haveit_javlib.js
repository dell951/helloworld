// ==UserScript==
// @name         HaveIT?-javlibrary
// @namespace    http://tampermonkey.net/
// @include      http://www.javlibrary.com/*
// @version      0.1
// @description  do I have it already?
// @author       You
// @require      http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.4.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_notification
// @grant        GM_setClipboard
// @grant        GM_getResourceURL
// ==/UserScript==

queryJid = function(q_jid){
    rtn = false;
    $.ajax({
        async: false,
        url: 'http://192.168.1.150:5555/' + q_jid,
        crossDomain: true,
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            rtn = data.details.found;
        },
        error: function(jqXHR, textStatus, errorThrown) {
              console.log(jqXHR.status);
        }
    });
    console.log('queryJid(' + q_jid + ') returning ' + rtn);
    return rtn;
};

$(document).ready(
    $(".id").each(function( index ) {
        haveit = queryJid($(this).text());
        if (haveit){
            $(this).css('background-color','#00b649').css('color','white');
        }
    })
);