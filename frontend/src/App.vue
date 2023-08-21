
<style>
@import "./assets/main.css";
</style>

<template>
  <v-app>
    <!-- Left drawer menu -->
    <!-- <v-navigation-drawer app v-model="drawer" temporary>
      <v-list nav dense>
        <div class="text-button pa-1">Contents</div>
        <v-list-item-group
          v-model="group"
          active-class="blue--text text--accent-4"
        >
          <v-list-item
            v-for="(n, i) in [...Array(PARTS_AMOUNT).keys()]"
            :key="i"
            link
            @click="changePart(n + 1)"
            class="ma-0 pa-0 pl-3"
          >
            {{ contents[langCodeFrom][n] }}
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer> -->

    <!-- Top app bar -->
    <v-card flat>
      <!-- <v-toolbar class="my-toolbar" extended flat>
        <v-row>
          <v-col cols="12" class="text-center"> asd </v-col>
        </v-row>
      </v-toolbar> -->
    </v-card>

    <v-main>
      <v-container class="pb-15 pt-8">
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { LANGUAGES, DEFAULT_FROM, DEFAULT_TO } from "@/common/language.helper";
import {
  DEFAULT_PART,
  PARTS_AMOUNT,
  FONT_SIZE_NORMAL,
  FONT_SIZE_SMALL,
  FONT_SIZE_LARGE,
} from "@/common/helper";
import {
  SET_FONT_SIZE_LEFT,
  SET_FONT_SIZE_RIGHT,
  SET_LAYOUT_MODE,
  SET_COLOR_PROMPT,
  SET_SHOW_TEXT_LEFT,
  SET_SHOW_TEXT_RIGHT,
} from "@/store/mutations.type";
import { mapGetters } from "vuex";
import { LanguageHelper } from "./common/language.helper";

const assets = import.meta.glob(`./assets/info/**`, {
  as: "raw",
});

export default {
  name: "App",
  data: () => ({
    LANGUAGES,
    PARTS_AMOUNT,
    FONT_SIZE_NORMAL,
    FONT_SIZE_SMALL,
    FONT_SIZE_LARGE,
    drawer: false,
    contents: LanguageHelper.initContents(),
  }),
  mounted() {},
  methods: {
    getContents() {
      let path = `./assets/info/contents.json`;
      console.log(assets);
      if (assets[path]) {
        assets[path]().then((resp_json) => {
          this.contents = JSON.parse(resp_json);
        });
      }
    },
    getFlagImgPath(code) {
      return new URL(`./assets/flags/flag-${code}-h.svg`, import.meta.url).href;
    },
    changePart(n) {
      this.$router.push({
        path: `/${n}/${this.langCodeFrom}/${this.langCodeTo}`,
      });
    },
    changeLangFrom(code) {
      this.$router.push({
        path: `/${this.currPart}/${code}/${this.langCodeTo}`,
      });
    },
    changeLangTo(code) {
      this.$router.push({
        path: `/${this.currPart}/${this.langCodeFrom}/${code}`,
      });
    },
    goToGithub() {
      window.open("https://github.com/averkij/a-studio", "_blank");
    },
    setFontSizeLeft(mode) {
      if (this.fontSizeLeft == mode) {
        localStorage.fontSizeLeft = FONT_SIZE_NORMAL;
        this.$store.commit(SET_FONT_SIZE_LEFT, {
          fontSizeLeft: FONT_SIZE_NORMAL,
        });
      } else {
        localStorage.fontSizeLeft = mode;
        this.$store.commit(SET_FONT_SIZE_LEFT, {
          fontSizeLeft: mode,
        });
      }
    },
    setFontSizeRight(mode) {
      if (this.fontSizeRight == mode) {
        localStorage.fontSizeRight = FONT_SIZE_NORMAL;
        this.$store.commit(SET_FONT_SIZE_RIGHT, {
          fontSizeLeft: FONT_SIZE_NORMAL,
        });
      } else {
        localStorage.fontSizeRight = mode;
        this.$store.commit(SET_FONT_SIZE_RIGHT, {
          fontSizeRight: mode,
        });
      }
    },
    changeLayoutMode() {
      let layoutMode = this.layoutMode;
      layoutMode = (layoutMode + 1) % 3;
      localStorage.layoutMode = layoutMode;
      this.$store.commit(SET_LAYOUT_MODE, {
        layoutMode: layoutMode,
      });
    },
    changeColorPrompt() {
      let colorPrompt = this.colorPrompt;
      colorPrompt = (colorPrompt + 1) % 4;
      localStorage.colorPrompt = colorPrompt;
      this.$store.commit(SET_COLOR_PROMPT, {
        colorPrompt: colorPrompt,
      });
    },
    toggleLeftText() {
      let showTextLeft = Number(this.showTextLeft);
      showTextLeft = ((showTextLeft + 1) % 2).toString();
      localStorage.showTextLeft = showTextLeft;
      this.$store.commit(SET_SHOW_TEXT_LEFT, {
        showTextLeft: showTextLeft,
      });
    },
    toggleRightText() {
      let showTextRight = Number(this.showTextRight);
      showTextRight = ((showTextRight + 1) % 2).toString();
      localStorage.showTextRight = showTextRight;
      this.$store.commit(SET_SHOW_TEXT_RIGHT, {
        showTextRight: showTextRight,
      });
    },
  },
  computed: {
    ...mapGetters([
      "fontSizeLeft",
      "fontSizeRight",
      "layoutMode",
      "colorPrompt",
      "showTextLeft",
      "showTextRight",
    ]),
    langCodeFrom() {
      let langCode = this.$route.params.from;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_FROM;
    },
    langCodeTo() {
      let langCode = this.$route.params.to;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_TO;
    },
    currPart() {
      let part_id = this.$route.params.part;
      if (part_id < 1 || part_id > PARTS_AMOUNT) {
        return DEFAULT_PART;
      }
      return part_id;
    },
    iconFontDecreaseLeftIsActive() {
      return this.fontSizeLeft == "1";
    },
    iconFontIncreaseLeftIsActive() {
      return this.fontSizeLeft == "2";
    },
    iconFontDecreaseRightIsActive() {
      return this.fontSizeRight == "1";
    },
    iconFontIncreaseRightIsActive() {
      return this.fontSizeRight == "2";
    },
  },
  mounted() {
    this.getContents();
  },
};
</script>
  