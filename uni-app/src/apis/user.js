import request from '@/utils/request'

function Func(method, data = null, params = null) {
    return request({url: '/api/user', method: method, data: data, params: params});
}
// 登录
export function login(data) {
    return request({url: '/auth/login', method: 'post', data})
}

// 退出登录