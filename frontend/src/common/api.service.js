import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {
    API_URL
} from "@/common/config";
import {
    ErrorHelper
} from "@/store/items.module"

const ApiService = {
    init() {
        Vue.use(VueAxios, axios);
        Vue.axios.defaults.baseURL = API_URL;
    },
    query(resource, params) {
        return Vue.axios.get(resource, params).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    get(resource, slug = "") {
        return Vue.axios.get(`${resource}/${slug}`).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    download(resource, slug = "") {
        return Vue.axios.get(`${resource}/${slug}`, {
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
        return Vue.axios.post(
            `${resource}/${slug}`,
            params,
            config
        ).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    },
    update(resource, slug, params) {
        return Vue.axios.put(`${resource}/${slug}`, params);
    },
    put(resource, params) {
        return Vue.axios.put(`${resource}`, params);
    },
    delete(resource) {
        return Vue.axios.delete(resource).catch(error => {
            throw new Error(`ApiService ${error}`);
        });
    }
};

export default ApiService;

export const SbsService = {
    getSbsInfo(params) {
        return ApiService.get("sbs",
            `$info/${params.sbsId}`);
    },
};