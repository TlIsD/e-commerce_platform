import axios from "axios";

const http = axios.create({
    baseURL: "http://api.platform.cn:8000",
    withCredentials: false,
})

// 请求拦截器
http.interceptors.request.use((config)=>{
    console.log("http请求之前");
    return config;
}, (error)=>{
    console.log("http请求错误");
    return Promise.reject(error);
});

// 响应拦截器
http.interceptors.response.use((response)=>{
    console.log("服务端响应成功之后，执行then之前");
    return response;
}, (error)=>{
    console.log("服务端响应错误内容......");
    return Promise.reject(error);
});

export default http;