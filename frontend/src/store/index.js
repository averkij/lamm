import {
    createStore
} from 'vuex'

import {
    SbsService
} from "@/common/api.service";

import {
    SET_USER_ID,
    SET_USER_NAME,
    SET_SBS_INFO,
    SET_TASK
} from "./mutations.type"

import {
    GET_SBS_INFO,
    GET_TASK,
    RESOLVE_TASK,
} from "./actions.type"

import {
    SettingsHelper
} from "@/common/settings.helper";

const initialState = {
    userId: SettingsHelper.getUserId(),
    userName: "Sergei",
    sbsInfo: {},
    sbsTasks: [
        ["", "", "", "", ""]
    ]
}

export default createStore({
    state: {
        ...initialState
    },
    actions: {
        async [GET_SBS_INFO](context, params) {

            console.log("GET_SBS_INFO params", params)

            const {
                data
            } = await SbsService.getSbsInfo({
                "sbsId": params.sbsId
            });
            context.commit(SET_SBS_INFO, {
                data: data
            });
            return data;
        },
        async [GET_TASK](context, params) {
            const {
                data
            } = await SbsService.getSbsTask({
                "sbsId": params.sbsId,
                "userId": params.userId
            });
            context.commit(SET_TASK, {
                data: data
            });
            return data;
        },
        async [RESOLVE_TASK](context, params) {
            const {
                data
            } = await SbsService.resolveSbsTask({
                "sbsId": params.sbsId,
                "userId": params.userId,
                "taskId": params.taskId,
                "answer": params.answer
            });
            return data;
        },
    },
    mutations: {
        [SET_USER_ID](state, params) {
            state.userId = params.userId;
        },
        [SET_USER_NAME](state, params) {
            state.userId = params.userName;
        },
        [SET_SBS_INFO](state, params) {
            state.sbsInfo = params.data;
        },
        [SET_TASK](state, params) {
            state.sbsTasks = params.data["items"];
        }
    },
    getters: {
        userId(state) {
            return state.userId;
        },
        userName(state) {
            return state.userName;
        },
        sbsInfo(state) {
            return state.sbsInfo;
        },
        sbsTasks(state) {
            return state.sbsTasks;
        },
    }
})