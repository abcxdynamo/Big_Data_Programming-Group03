import axios from 'axios';
import {ElMessage} from 'element-plus';
import localStore from './store';
import _ from 'lodash';

// Creating an Axios Instance
const api = axios.create({
    baseURL: 'http://localhost:5001',
    timeout: 10000,
    withCredentials: true

});

// request interceptors
api.interceptors.request.use(
    (config) => {
        const token = localStore.get('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// response interceptors
api.interceptors.response.use(
    (response) => {
        const resp_data = response.data;
        const {success, code, data} = resp_data;
        if (success) {
            return data || {};
        } else {
            ElMessage.error(code + ", " + data && data["err_msg"] || "ERROR");
            return Promise.reject(data);
        }
    },
    (error) => {
        if (!_.includes(["ERR_CANCELED"], error.code)) {
            console.log(error);
            let message = 'Request failed, please try again later';
            ElMessage.error(message);
        }
        return Promise.reject(error);
    }
);

export default api;
