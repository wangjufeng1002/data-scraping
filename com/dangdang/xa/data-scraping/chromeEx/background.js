
async function getCookie() {

    try {
        const cookies = await chrome.cookies.getAll({});
        console.log("cookies:", cookies)

        let cookiesString = ''
        var cookiesMap = new Map()
        for (let i = 0; i < cookies.length; i++) {
            if (cookies[i].domain === '.taobao.com' || cookies[i].domain === '.tmall.com' || cookies[i].domain === 'mdskip.taobao.com') {
                cookiesMap.set(cookies[i].name, cookies[i].value)
            }
        }
        cookiesMap.forEach((value, key) => {
            cookiesString += key + "=" + value + ";"
        })


        return cookiesString;
    } catch (error) {
        return `Unexpected error: ${error.message}`;
    }


}


chrome.runtime.onMessage.addListener(  (request,sender,sendResponse)=>{

    console.log(request)
    if(request==='cookies'){
        getCookie().then((e)=>{
            sendResponse(e)
          });
        return true;
    }
    else{
        clean()
    }
  
 

})

const clean=()=>{

    var millisecondsPerWeek = 1000 * 60 * 60 * 24 * 10;
	var ago = (new Date()).getTime() - millisecondsPerWeek;
    var data= {
        "appcache": true,
        "cache": true,
        "cacheStorage": true,
        "cookies": true,
        "downloads": true,
        "fileSystems": true,
        "formData": true,
        "history": true,
        "indexedDB": true,
        "localStorage": true,
        "passwords": true,
        "serviceWorkers": true,
        "webSQL": true
    }
	chrome.browsingData.remove({ "since": ago }, data , function () {
        console.log("清楚缓存成功")
	});

}