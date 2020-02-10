// ==UserScript==
// @name         HaveIT?
// @namespace    http://tampermonkey.net/
// @include      http://888kf.xyz/*
// @include      http://javtorrent.re/*
// @include      https://www.sehuatang.org/*
// @include      https://www.777x.com/*
// @include      http://thz4.net/*
// @include      http://www.ssl.yx51.net/bbs/*
// @include      http://www.javlibrary.com/*
// @include      https://www.xianrenfuli.com/*
// @include      http://cngougoubt.co/sou/*
// @include      http://thzvv.net/*
// @include      https://www.sehuatanghd.com/*
// @include      https://www.777x.com/*
// @include      http://*/pw/*
// @include      https://shtsds1.me/*
// @include      http://*lufi99.info/*
// @include      http://1024.qdldd.biz/*
// @include      https://btos.pw/search/*
// @include      http://*2.*.*/*
// @include      https://www.javbus.com/*
// @include      https://av-help.memo.wiki/*
// @include      https://www.busdmm.cc*
// @include      http://*/2048/*
// @include      http*://www.busdmm.cc/*
// @include      http*://www.dmmbus.co/*
// @include      http*://*javbus.com/*
// @include      https://www.busdmm.cc/*
// @include      http*://*t66y.com/*
// @include      http://iwertygv.co/*
// @include      http://mo6699.net/*
// @include      http://www.zhaileba.info/*
// @include      http://cntorrentkitty.com/*
// @include      http://www.ceo-7158.com/*
// @include      https://www.sehuatang.org/*
// @include      file:///Users/azu/Desktop/a.html
// @version      0.7
// @description  do I have it already?
// @author       You
// @require      http://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.4.min.js
// @require      https://cdn.jsdelivr.net/npm/mark.js@8.11.1/dist/jquery.mark.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_notification
// @grant        GM_setClipboard
// @grant        GM_getResourceURL
// ==/UserScript==

var queryJidList = function(jsondata){
    var rtn = new Object();
    var startTime = new Date();
    var servertarget = "http://192.168.1.150:5555/find";
    if (location.protocol === "https:")
        servertarget = "https://192.168.1.150:5556/find";
    $.ajax({
        async: false,
        url: servertarget,
        crossDomain: true,
        type: 'POST',
        dataType: 'json',
        data: jsondata,
        success: function(data, textStatus, jqXHR) {
            rtn = data;
            var endTime = new Date();
            var timeDiff = endTime - startTime; //in ms
                // strip the ms
            timeDiff /= 1000;

            var seconds = Math.round(timeDiff);
            console.log("queryJidList took " + seconds + " seconds");
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("exception : " + jqXHR.status);
        }
    });
    return rtn;
};

var queryJid = function(q_jid){
    var rtn = false;
    var startTime = new Date();
    var servertarget = "http://192.168.1.150:5555/jid=";
    if (location.protocol === "https:")
        servertarget = "https://192.168.1.150:5556/jid=";
    $.ajax({
        async: false,
        url: servertarget + q_jid,
        crossDomain: true,
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            rtn = data.details;
            var endTime = new Date();
            var timeDiff = endTime - startTime; //in ms
                // strip the ms
            timeDiff /= 1000;

            var seconds = Math.round(timeDiff);
            console.log("queryJid took " + seconds + " seconds");
        },
        error: function(jqXHR, textStatus, errorThrown) {
              console.log(jqXHR.status);
        }
    });
    console.log('queryJid(' + q_jid + ') returning ' + rtn);
    return rtn;
};

var iterateMyFav = function(fulltext){
    var ignoreList = new Array("mp4","avi","mkv","rmvb","m4v","fc2","xp1024","link12345","new2018","cr2","cr1","sex2","fbf6","ck8","bbe2","ff0000","ffd800",
                              "ff6","4ef40","31bcd5","dfebf3","ee3148","dioguitar23");
//    $("<style>").prop("type", "text/css").html("mark {background-color: #00b649; color: white;}").appendTo("head");
//    $("<style>").prop("type", "text/css").html("markczimu {background-color: yellow; color: red;}").appendTo("head");
    $("<style>")
        .prop("type", "text/css")
        .html("\
              .markfound {\
                  background-color: #40BF55;\
                  color: white;\
		          font-weight: bold;\
               }\
              .markHfound {\
                  background-color: #40BF55;\
                  color: yellow;\
		          font-weight: bold;\
               }\
              .markczimu {\
                  background-color: #0F7884;\
                  color: white;\
		         font-weight: bold;\
               }\
              .markczimubackup {\
                  background-color: #0F7884;\
                  color: #6bff75;\
		         font-weight: bold;\
               }\
              .markHczimu {\
                background-color: #0F7884;\
                color: yellow;\
                font-weight: bold;\
               }\
            ")
    .appendTo("head");
    //console.log(fulltext);
    const regex = /(\d*)+([a-zA-Z]{2,})-?(\d+)+/gm;
    let m;
    var qids = new Array();
    var search_json = {}
    while ((m = regex.exec(fulltext)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }

        // The result can be accessed through the `m`-variable.
        m.forEach((match, groupIndex) => {
            if (groupIndex == 0 && ignoreList.indexOf(match.toLowerCase()) == -1){
                qids.push(match);
            }
        });
    }

    search_json['ids_list'] = qids;
    var all_list = queryJidList(JSON.stringify(search_json));

    while ((m = regex.exec(fulltext)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        }

        // The result can be accessed through the `m`-variable.
        m.forEach((match, groupIndex) => {
            if (groupIndex == 0 && ignoreList.indexOf(match.toLowerCase()) == -1){
                detail = all_list.details_list[match];
                console.log(detail)
                if (detail.found){
                    if (detail.czimu){
                        if (detail.resolution[0] >= 1080)
                            $("body").mark(match,{"className": "markHczimu"});
                        else {
                            if (detail.hbackup)
                                $("body").mark(match,{"className": "markczimu"});
                            else
                                $("body").mark(match,{"className": "markczimubackup"});
                        }
                    }else{
                        if (detail.resolution[0] >= 1080)
                            $("body").mark(match,{"className": "markHfound"});
                        else
                            $("body").mark(match,{"className": "markfound"});
                    }
                }
            }
        });
    }
};

$(document).ready(
    iterateMyFav(document.body.innerText)
);
