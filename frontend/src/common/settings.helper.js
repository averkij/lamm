import {
    v4 as uuidv4
} from 'uuid';

export const SettingsHelper = {
    // getFontSizeLeft() {
    //     return localStorage.fontSizeLeft ? localStorage.fontSizeLeft : defaultClientSettings.fontSizeLeft;
    // },
    getUserId() {
        return localStorage.userId ? localStorage.userId : uuidv4();
    },
}

const defaultClientSettings = {}