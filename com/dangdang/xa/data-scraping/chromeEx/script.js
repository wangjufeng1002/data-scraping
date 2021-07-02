
setTimeout(async () => {

    const user = await getUser()
    const userjson = JSON.parse(user)
    console.log(userjson)
    cleanCookie()
    isLogin(userjson)
    login(userjson)
    //1分钟之后再次执行
    setTimeout(() => {
        window.location.href = 'https://www.baidu.com'
    }, 30000)
}, 2000)


const cleanCookie = () => {
    let baidu = document.getElementsByClassName("bg s_btn_wr")
    if (baidu.length > 0) {
        console.log("百度页面,准备清除缓存")
        chrome.runtime.sendMessage('clean', (response) => {
            console.log('清除成功')
            window.location.href = 'https://login.taobao.com/'
        })

    }

}
//判断是否已经登录,登录之后发送10次cookie
const isLogin = (userjson) => {
    let logo = document.getElementById("mallLogo")
    let index = 0
    console.log(logo)
    if (logo != null) {
        console.log("登录成功,发送cookies")
        let timer = setInterval(() => {
            console.log(index)
            getCookie(userjson)
            index++
            if (index > 10) {
                clearInterval(timer)
            }
        }, 1000);
    }
}

const getCookie = (user) => {
    chrome.runtime.sendMessage('cookies', function (response) {
        console.log("cookie", response)

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "http://localhost:10001/updateHeaders", true)
        xhr.setRequestHeader('content-type', 'application/json');
        var data = { "account": user.account, "cookie": response }
        xhr.send(JSON.stringify(data))

    })
}
const getUser = () => {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "http://localhost:10001/getInvalidHeader", true)
        xhr.send()
        xhr.onload = (e) => {
            resolve(e.target.response)
        }
    })
}
const login = (user) => {
    //登录之后跳转
    let menu = document.getElementsByClassName("mt-menu-item")
    if (menu.length > 0) {
        window.location.href = 'https://chaoshi.detail.tmall.com/item.htm?id=620005546339'
    }
    //登录
    let username = document.getElementsByName("fm-login-id")
    console.log(username.length)
    if (username.length > 0) {

        username[0].value = user.account
        let passwd = document.getElementsByName("fm-login-password")
        passwd[0].value = user.password
        let loginbutton = document.getElementsByClassName("fm-submit")
        loginbutton[0].click()
        console.log(username[0])

    }

}
