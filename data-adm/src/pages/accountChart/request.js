import axios from "axios"

export const requestData=(params)=>{
    return axios.get("/api/data/scraping/queryAggregation",{params})
}

export const getTotalData=(params)=>{
    return axios.get('/api/data/scraping/queryTotalSummery',{params})
}
export const getAccountData=(params)=>{
    return axios.get('/api/data/scraping/queryStaticDimension',{params})
}