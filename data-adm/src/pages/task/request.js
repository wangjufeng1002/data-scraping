import axios from "axios"

export const requestList = (params) => {

    return axios.get('/api/data/scraping/queryJobTask',{params})
}
export const requestDetail = (params) => {

    return axios.get('/api/data/scraping/queryJobTaskDetail',{params})
}

export const download=(params)=>{
    return axios({
        url:'/api/data/scraping/exportJobTaskResult',
        method:'GET',
        responseType: 'blob',
        params,
    })
}