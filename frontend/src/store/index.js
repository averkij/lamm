import {
    createStore
} from 'vuex'

import {
    SET_USER_ID,
    SET_USER_NAME,
} from "./mutations.type"

import {
    SettingsHelper
} from "@/common/settings.helper";

const initialState = {
    userId: SettingsHelper.getUserId(),
    userName: "Sergei",
}

export default createStore({
    state: {
        ...initialState
    },
    mutations: {
        [SET_USER_ID](state, params) {
            state.userId = params.userId;
        },
        [SET_USER_NAME](state, params) {
            state.userId = params.userName;
        },
    },
    getters: {
        userId(state) {
            return state.userId;
        },
        userName(state) {
            return state.userName;
        },
    }
})