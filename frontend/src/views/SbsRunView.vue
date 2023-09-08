<template>
  <div>
    <v-row>
      <v-col cols="12">{{ sbsTasks[0][1] }}</v-col> </v-row
    ><v-row>
      <v-col cols="6">{{ sbsTasks[0][3] }}</v-col>
      <v-col cols="6">{{ sbsTasks[0][4] }}</v-col>
    </v-row>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO, GET_TASK } from "@/store/actions.type";

export default defineComponent({
  name: "SbsRunView",
  components: {},
  data() {
    return {};
  },
  methods: {
    getSbsInfo() {
      this.$store.dispatch(GET_SBS_INFO, {
        sbsId: this.$route.params.hash,
      });
    },
    getNextTask() {
      this.$store.dispatch(GET_TASK, {
        sbsId: this.$route.params.hash,
        userId: this.userId,
      });
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo", "sbsTasks"]),
  },
  mounted() {
    this.getSbsInfo();
    this.getNextTask();
  },
});
</script>
