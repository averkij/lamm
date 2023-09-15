<template>
  <v-row>
    <v-col cols="12">SBS статистика</v-col>
  </v-row>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO } from "@/store/actions.type";

export default defineComponent({
  name: "SbsShowView",
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
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo"]),
  },
  watch: {},
  mounted() {
    this.getSbsInfo();
  },
});
</script>
