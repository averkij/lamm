import {
    createStore
} from 'vuex'

import {
    SbsService
} from "@/common/api.service";

import {
    SET_USER_ID,
    SET_USER_NAME,
    SET_SBS_INFO
} from "./mutations.type"

import {
    GET_SBS_INFO,
    GET_TASK,
} from "./actions.type"

import {
    SettingsHelper
} from "@/common/settings.helper";

const initialState = {
    userId: SettingsHelper.getUserId(),
    userName: "Sergei",
    sbsInfo: {}
}

export default createStore({
    state: {
        ...initialState
    },
    actions: {
        async [GET_SBS_INFO](context, params) {
            const {
                data
            } = await SbsService.getSbsInfo(params);
            context.commit(SET_SBS_INFO, {
                data: data
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
    }
})