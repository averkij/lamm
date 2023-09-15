
<style>
@import "./assets/main.css";
</style>

<template>
  <div>
    <v-app>
      <!-- Top app bar -->
      <v-toolbar class="my-toolbar" flat>
        <!-- <v-app-bar-nav-icon
          ><v-icon>mdi-alien-outline</v-icon></v-app-bar-nav-icon
        > -->

        <v-spacer></v-spacer>

        <div>
          <div v-if="showSbsInfo">
            <span class="font-weight-medium">{{ sbsInfo["model_1"] }}</span>
            против
            <span class="font-weight-medium">{{ sbsInfo["model_2"] }}</span
            >: выполнено
            <span class="font-weight-medium">{{
              sbsInfo["solved_tasks"]
            }}</span>
            из
            <span class="font-weight-medium">{{ sbsInfo["total_tasks"] }}</span>
            заданий
          </div>
        </div>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon @click="switchView">mdi-swap-horizontal</v-icon>
        </v-btn>
      </v-toolbar>

      <v-main>
        <v-container class="pb-15 pt-8">
          <router-view></router-view>
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
// import { SettingsHelper } from "./common/settings.helper";
// import { GET_SBS_INFO, GET_TASK } from "@/store/actions.type";

export default {
  name: "App",
  data: () => ({}),
  mounted() {},
  methods: {
    switchView() {
      if (this.$route.name == "sbsrun") {
        this.$router.push({
          path: `/sbs/show/${this.$route.params.hash}`,
        });
      } else if (this.$route.name == "sbsshow") {
        this.$router.push({
          path: `/sbs/run/${this.$route.params.hash}`,
        });
      }
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo"]),
    showSbsInfo() {
      if (this.sbsInfo && this.sbsInfo.model_1) {
        return true;
      }
      return false;
    },
  },
  mounted() {
    // this.getSbsInfo();
  },
};
</script>
  