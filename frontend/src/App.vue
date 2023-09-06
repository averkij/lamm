
<style>
@import "./assets/main.css";
</style>

<template>
  <v-app>
    <!-- Top app bar -->
    <v-card flat>
      <v-toolbar class="my-toolbar" flat>
        <v-row>
          <v-col cols="12" class="text-center">
            {{ userName }} ({{ userId }})
          </v-col>
        </v-row>
      </v-toolbar>
    </v-card>

    <v-main>
      <v-container class="pb-15 pt-8">
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
// import { SET_LAYOUT_MODE } from "@/store/mutations.type";
import { mapGetters } from "vuex";
// import { SettingsHelper } from "./common/settings.helper";

export default {
  name: "App",
  data: () => ({}),
  mounted() {},
  methods: {
    init() {},
    // changePart(n) {
    //   this.$router.push({
    //     path: `/${n}/${this.langCodeFrom}/${this.langCodeTo}`,
    //   });
    // },
    // changeLayoutMode() {
    //   let layoutMode = this.layoutMode;
    //   layoutMode = (layoutMode + 1) % 3;
    //   localStorage.layoutMode = layoutMode;
    //   this.$store.commit(SET_LAYOUT_MODE, {
    //     layoutMode: layoutMode,
    //   });
    // },
  },
  computed: {
    ...mapGetters(["userId", "userName"]),
    // langCodeFrom() {
    //   let langCode = this.$route.params.from;
    //   if (this.LANGUAGES[langCode]) {
    //     return langCode;
    //   }
    //   return DEFAULT_FROM;
    // },
  },
  mounted() {
    // this.init();
  },
};
</script>
  