// ==UserScript==
// @name         HaveIT?
// @namespace    http://tampermonkey.net/
// @include      http://javtorrent.re/*
// @include      http://javlibrary.com/*
// @version      0.1
// @description  do I have it already!
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

iterateJtext = function(jtext){
    var rtn = false;
    const regex = /^\[(.*)\]/g;
    const str = jtext;
    let m;

    while ((m = regex.exec(str)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }

        // The result can be accessed through the `m`-variable.
        m.forEach((match, groupIndex) => {
            if (groupIndex > 0 ){
                console.log("query Jid : " + match);
                rtn = queryJid(match);
                //rtn = true;
            }
        });
    }
    return rtn;
};

queryJid = function(q_jid){
    rtn = false;
    $.ajax({
        url: 'http://127.0.0.1:5000/' + q_jid,
        crossDomain: true,
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            rtn = true;
            console.log(data.details.jid + ', ' + data.details.path + ', ' + data.details.size );
        },
        error: function(jqXHR, textStatus, errorThrown) {
              console.log(jqXHR.status);
//            console('An error occurred... Look at the console (F12 or Ctrl+Shift+I, Console tab) for more information!');
//            $('#result').html('<p>status code: '+jqXHR.status+'</p><p>errorThrown: ' + errorThrown + '</p><p>jqXHR.responseText:</p><div>'+jqXHR.responseText + '</div>');
//            console.log('jqXHR:');
//            console.log(jqXHR);
//            console.log('textStatus:');
//            console.log(textStatus);
//            console.log('errorThrown:');
//            console.log(errorThrown);
        }
    });
    return rtn;
};

// parameter is an array of Javascript objects
$(document).ready(
    $(".base-t").each(function( index ) {
        haveit = iterateJtext($(this).text());
        if (haveit){
            $(this).css('color','green');
            //console.log( index + ": " + $( this ).text() );
        }
    })
);

