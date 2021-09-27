module.exports = {
    devServer: {
      host: 'localhost',
      port: 8080,
      proxy: {
        '/get': {
          target: 'http://localhost:3000',// 要跨域的域名
          changeOrigin: true, // 是否开启跨域
        },
        '/api': {
          target: 'http://192.168.47.230:10004',// 要跨域的域名
          changeOrigin: true, // 是否开启跨域
          pathRewrite: {   //重写路径
            //'^/api': '/api'   // 这种接口配置出来     http://XX.XX.XX.XX:8083/api/login
            '^/api': '/' //这种接口配置出来     http://XX.XX.XX.XX:8083/login
        }
      }
    }
  }
}