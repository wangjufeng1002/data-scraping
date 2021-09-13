// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://bokuts.tmall.com/*
// @icon         https://www.google.com/s2/favicons?domain=userscript.zone
// @grant        GM_setValue
// @grant        none
// @require      https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.18.2/babel.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/6.16.0/polyfill.js
// ==/UserScript==

(function() {
    'use strict';
    var urls=[
        "https://bokuts.tmall.com/search.htm?tsearch=y&search=y&orderType=newOn_desc&viewType=grid&keyword=&lowPrice=26.0&highPrice=26.1"
    ]



    //init()
    start()
    console.log(localStorage)

    function init(){
        localStorage.setItem("index",0)
        localStorage.setItem("isLocationed",false)
    }
    function start(){

        var caIndex=localStorage.getItem("index")
        if(caIndex==null){
            localStorage.setItem("index",0)
        }
        caIndex=localStorage.getItem("index")
        var url=urls[caIndex]
        var isLocationed =localStorage.getItem("isLocationed")
        console.log(isLocationed)
        if(isLocationed===null ||isLocationed==='false'){
            console.log("in")
            console.log(caIndex)
            console.log(url)
            localStorage.setItem("isLocationed",true)
            if(caIndex==urls.length){
                localStorage.setItem("index",0)
                localStorage.setItem("isLocationed",false)

                return
            }
            location.href=url
        }
        setTimeout(()=>{
            var children=$(".J_TItems").children()
            var page=$(".ui-page-s-len")[0].innerHTML
            var index=page.split('/')
            if(index[0]>=25){
                localStorage.setItem("index",parseInt(caIndex)+1)
                localStorage.setItem("isLocationed",false)
                location.href=url
                return
            }
            var text;
            for(var  i=0;i<children.length;i++ ){
                text+=children[i].innerHTML
            }

            var name=page+"_"+guid()+".txt"
            download(name,text)
            if(index[0]===index[1]){
                console.log("111")
                localStorage.setItem("index",parseInt(caIndex)+1)
                localStorage.setItem("isLocationed",false)
                location.href=urls[parseInt(caIndex)+1]
            }
            $(".ui-page-s-next")[0].click()


        },2000)
    }
    function fake_click(obj) {
        var ev = document.createEvent("MouseEvents");
        ev.initMouseEvent(
            "click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null
        );
        obj.dispatchEvent(ev);
    }

    function download(name, data) {
        var urlObject = window.URL || window.webkitURL || window;

        var downloadData = new Blob([data]);

        var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a")
        save_link.href = urlObject.createObjectURL(downloadData);
        save_link.download = name;
        fake_click(save_link);
    }
    function guid() {
        return 'xxxx-4xxx-yxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    // Your code here...
})();