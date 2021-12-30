import axios from 'axios';
import router from "@/router/index"


const service = axios.create({
    baseUrl: '',
    timeout: 600000
})


// 请求拦截，请求前置处理
service.interceptors.request.use(
    config => {
        let token = localStorage.getItem('token')
        if (token) {
            config.headers['x-token'] = token
        }
        return config
    },
    error => {
        this.$message.error('发送请求失败')
        return Promise.reject();
    }
)


service.interceptors.response.use(
    response => {
        if (response.data['message'] === '登录超时，请重新登录' ) {
            router.push({path: `/login?redirect=${router.history.current.fullPath}`});
        }
        return response.data
    }
)

export default service;