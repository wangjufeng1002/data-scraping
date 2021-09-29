import axios from "axios"

export const requestList=(params)=>{
    return axios.get('/api/data/scraping/queryAccountInfo',{params})
}
export const editAccount=()=>{

}