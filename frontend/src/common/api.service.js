import axios from "axios";

import {
    API_URL
} from "@/common/config";


const ApiService = {
    init() {
        console.log("API_URL", API_URL)

        axios.defaults.baseURL = API_URL;
    },
    query(resource, params) {
        return axios.get(resource, params).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    get(resource, slug = "") {
        return axios.get(`${resource}/${slug}`).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    download(resource, slug = "") {
        return axios.get(`${resource}/${slug}`, {
            responseType: 'blob'
        }).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    post(resource, slug, params, isBinary) {
        let config = {}
        if (isBinary) {
            config = {
                responseType: 'blob'
            }
        }
        return axios.post(
            `${resource}/${slug}`,
            params,
            config
        ).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    update(resource, slug, params) {
        return axios.put(`${resource}/${slug}`, params);
    },
    put(resource, params) {
        return axios.put(`${resource}`, params);
    },
    delete(resource) {
        return axios.delete(resource).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    }
};

export default ApiService;

export const SbsService = {
    getSbsInfo(params) {
        return ApiService.get("sbs",
            `info/${params.sbsId}`);
    },
    getSbsTask(params) {

        console.log('API', params)

        return ApiService.get("sbs",
            `task/get/${params.sbsId}/${params.userId}`);
    },
};