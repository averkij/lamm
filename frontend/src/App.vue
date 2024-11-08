
<style>
@import "./assets/main.css";
@import url("https://fonts.googleapis.com/css2?family=Audiowide&display=swap");
</style>

<template>
  <div>
    <v-app>
      <!-- Top app bar -->
      <v-toolbar :color="showSbsInfo ? 'deep-purple' : 'deep-purple'" flat>
        <!-- <v-app-bar-nav-icon
          ><v-icon>mdi-alien-outline</v-icon></v-app-bar-nav-icon
        > -->
        <v-spacer></v-spacer>

        <div>
          <div v-if="!showSbsInfo" class="font-title">⚡️ GIGAMETR</div>
          <div v-if="showSbsInfo">
            ⚡️
            <span class="font-weight-medium hidden-sm-and-down">
              {{ sbsInfo["model_1"] }}</span
            >
            <span class="hidden-sm-and-down"> против </span>
            <!-- <span class="hidden-md-and-up"> | </span> -->
            <span class="font-weight-medium hidden-sm-and-down">{{
              sbsInfo["model_2"]
            }}</span>
            <span class="hidden-sm-and-down">:</span>
            <span class="hidden-sm-and-down"> выполнено </span>
            <span class="font-weight-medium">{{
              sbsInfo["solved_tasks"]
            }}</span>
            из
            <span class="font-weight-medium">{{ sbsInfo["total_tasks"] }}</span>
            <span class="hidden-sm-and-down"> заданий</span>
          </div>
        </div>
        <v-spacer></v-spacer>

        <v-btn v-if="showSbsInfo" icon>
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
      } else if (this.$route.name == "datarun") {
        this.$router.push({
          path: `/data/show/${this.$route.params.hash}`,
        });
      } else if (this.$route.name == "sbsshow") {
        this.$router.push({
          path: `/sbs/run/${this.$route.params.hash}`,
        });
      } else if (this.$route.name == "datashow") {
        this.$router.push({
          path: `/data/check/${this.$route.params.hash}`,
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
  mounted() {},
};
</script>
  