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
    getSbsStat(params) {
        return ApiService.get("sbs",
            `stat/${params.sbsId}`);
    },
    getSbsTask(params) {
        return ApiService.get("sbs",
            `task/get/${params.sbsId}/${params.userId}/${params.tryId}`);
    },
    resolveSbsTask(params) {
        let form = new FormData();

        let eventId = 5 //skip
        switch (params.answer) {
            case 'left':
                eventId = 1;
                console.log('First model is better');
                break;
            case 'right':
                eventId = 2;
                console.log('Second model is better');
                break;
            case 'good':
                eventId = 3;
                console.log('Both models are good');
                break;
            case 'bad':
                eventId = 4;
                console.log('Both models are bad');
                break;
            default:
                console.log('Task is skipped');
        }

        form.append("sbs_guid", params.sbsId);
        form.append("user_guid", params.userId);
        form.append("task_id", params.taskId);
        form.append("try_id", params.tryId);
        form.append("event_id", eventId);

        return ApiService.post("sbs",
            `task/resolve`, form);
    },
};