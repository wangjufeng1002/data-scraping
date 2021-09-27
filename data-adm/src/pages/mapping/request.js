import axios from "axios"

export const requestList = (params) => {

    return axios.get('http://localhost:8080/api/data/scraping/queryProductMap',{params})
}
export const submitMapping=(data)=>{
   //todo  
   return axios.post('/api/data/scraping/modifyProductMap',{...data})
}