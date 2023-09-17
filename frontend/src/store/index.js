import {
    createStore
} from 'vuex'

import {
    v4 as uuidv4
} from 'uuid';

import {
    SbsService
} from "@/common/api.service";

import {
    SET_USER_ID,
    SET_USER_NAME,
    SET_SBS_INFO,
    SET_SBS_STAT,
    SET_TASK,
    SET_TRY_ID
} from "./mutations.type"

import {
    GET_SBS_INFO,
    GET_SBS_STAT,
    GET_TASK,
    RESOLVE_TASK,
} from "./actions.type"

import {
    SettingsHelper
} from "@/common/settings.helper";

const initialState = {
    userId: SettingsHelper.getUserId(),
    tryId: "",
    userName: "Sergei",
    sbsInfo: {},
    sbsTasks: [
        ["", "", "", "", ""]
    ],
    sbsStat: []
}

export default createStore({
    state: {
        ...initialState
    },
    actions: {
        async [GET_SBS_INFO](context, params) {
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
        async [GET_SBS_STAT](context, params) {
            const {
                data
            } = await SbsService.getSbsStat({
                "sbsId": params.sbsId
            });
            context.commit(SET_SBS_STAT, {
                data: data
            });

            return data;
        },
        async [GET_TASK](context, params) {
            let tryId = uuidv4().substring(0, 12).replace("-", "");
            const {
                data
            } = await SbsService.getSbsTask({
                "sbsId": params.sbsId,
                "userId": params.userId,
                "tryId": tryId
            });
            context.commit(SET_TASK, {
                data: data
            });
            context.commit(SET_TRY_ID, {
                tryId: tryId
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
                "tryId": params.tryId,
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
        [SET_SBS_STAT](state, params) {
            state.sbsStat = params.data;
        },
        [SET_TASK](state, params) {
            state.sbsTasks = params.data["items"];
        },
        [SET_TRY_ID](state, params) {
            console.log("tryId:", params.tryId)

            state.tryId = params.tryId;
        }
    },
    getters: {
        userId(state) {
            return state.userId;
        },
        tryId(state) {
            return state.tryId;
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
        sbsStat(state) {
            return state.sbsStat;
        },
    }
})