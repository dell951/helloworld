// ==UserScript==
// @name         javtorrent ad
// @namespace    http://tampermonkey.net/
// @include      http://1be.biz/*
// @include      http://1dl.biz/*
// @version      0.1
// @description  try to take over the world!
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

$(document).ready(function () {
    setTimeout(function () {
         document.querySelector('a.j-link').click();
    }, 1000);
 });
 