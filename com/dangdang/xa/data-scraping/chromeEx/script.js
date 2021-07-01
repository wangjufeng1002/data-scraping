
setTimeout(()=>{


    cleanCookie()
    isLogin()
    login()
    //1分钟之后再次执行
    setTimeout(()=>{
        window.location.href='https://www.baidu.com'
    },60000)
},2000)


const cleanCookie=()=>{
    let baidu=document.getElementsByClassName("bg s_btn_wr")
    if(baidu.length>0){
        console.log("百度页面,准备清除缓存")
        chrome.runtime.sendMessage('clean',(response)=>{
            console.log('清除成功')
            window.location.href='https://login.taobao.com/'
        })
    
    }

}
//判断是否已经登录,登录之后发送10次cookie
const isLogin=()=>{
    let logo= document.getElementById("mallLogo")
    let index =0
    console.log(logo)
    if(logo!=null){
        console.log("登录成功,发送cookies")
       let timer= setInterval(() => {
           console.log(index)
            getCookie()
            index++
            if(index>10){
                clearInterval(timer)
            }
        }, 2000);
    }
}

const getCookie=()=>{
    chrome.runtime.sendMessage('cookies', function(response){
        console.log("cookie",response)

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "http://localhost:10001/updateHeaders", true)
        xhr.setRequestHeader('content-type', 'application/json');
        var data = { "account": "123", "cookie": response }
        xhr.send(JSON.stringify(data))

    })
}
const login =()=>{
    //登录之后跳转
    let menu= document.getElementsByClassName("mt-menu-item")
    if(menu.length>0){
        window.location.href='https://chaoshi.detail.tmall.com/item.htm?id=620005546339'
    }
    //登录
    let username=document.getElementsByName("fm-login-id")
    console.log(username.length)
    if(username.length>0){
        username[0].value='zxc90028'
        let passwd=document.getElementsByName("fm-login-password")
        passwd[0].value='aini131470777'
        let loginbutton=document.getElementsByClassName("fm-submit")
        loginbutton[0].click()
        console.log(username[0])

    }

}
