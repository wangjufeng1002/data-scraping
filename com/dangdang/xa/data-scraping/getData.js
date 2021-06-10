// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://winshare.tmall.com/*
// @icon         https://www.google.com/s2/favicons?domain=userscript.zone
// @grant        GM_setValue
// @grant        none
// @require      https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/6.18.2/babel.js
// @require      https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/6.16.0/polyfill.js
// ==/UserScript==

(function() {
    //油猴脚本 自动爬取数据
    'use strict';
    var urls=[
        'https://winshare.tmall.com/category-491558491.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558491&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558501.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558501&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558488.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558488&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558500.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558500&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558506.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558506&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558486.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558486&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558504.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558504&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558503.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558503&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558507.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558507&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558485.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558485&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558490.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558490&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558505.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558505&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558492.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558492&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558495.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558495&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558496.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558496&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558487.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558487&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558489.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558489&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558497.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558497&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729360.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729360&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729359.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729359&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729374.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729374&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729372.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729372&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729371.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729371&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729361.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729361&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729366.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729366&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729365.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729365&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729370.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729370&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729375.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729375&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729368.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729368&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729363.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729363&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698229.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698229&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698226.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698226&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698234.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698234&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698221.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698221&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698222.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698222&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698233.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698233&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698231.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698231&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698225.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698225&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698223.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698223&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698224.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698224&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698215.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698215&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698232.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698232&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384473200.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384473200&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585610.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585610&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585596.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585596&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585597.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585597&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585604.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585604&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585614.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585614&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585613.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585613&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585606.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585606&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585609.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585609&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849738635.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849738635&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491717852.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491717852&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491550351.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491550351&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491562031.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491562031&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474752.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474752&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491647586.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491647586&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491698214.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491698214&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491595423.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491595423&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474751.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474751&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849729358.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849729358&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491650530.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491650530&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849768723.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849768723&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491681820.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491681820&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491558483.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491558483&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849760062.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849760062&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491585594.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491585594&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491687656.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491687656&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491666441.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491666441&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491552450.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491552450&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474753.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474753&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491655539.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491655539&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849332800.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849332800&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491689872.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491689872&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491659877.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491659877&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491553986.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491553986&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491644529.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491644529&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849745608.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849745608&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849764123.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849764123&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491677010.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491677010&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491702467.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491702467&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849741392.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849741392&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491663462.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491663462&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491593674.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491593674&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849765778.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849765778&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491652691.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491652691&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491569878.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491569878&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-850412544.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=850412544&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474750.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474750&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849683450.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849683450&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491717852.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491717852&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849746127.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849746127&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-849769293.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=849769293&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384473200.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384473200&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491694268.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491694268&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491721726.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491721726&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-491658052.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=491658052&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474745.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474745&pageNo=1&tsearch=y#anchor',
        'https://winshare.tmall.com/category-384474749.htm?spm=a1z10.3-b-s.w4011-23389038992.272.39ff7652dDgWAz&catId=384474749&pageNo=1&tsearch=y#anchor',
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
            var category=$(".J_TCrumbDropHd")[0]?.innerText
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

            var name=category+page+"_"+guid()+".txt"
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