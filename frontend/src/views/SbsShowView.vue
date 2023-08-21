<template>
  <v-row>
    <v-col cols="12">SBS статистика</v-col>
  </v-row>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";

export default defineComponent({
  name: "SbsShowView",
  components: {},
  data() {
    return {};
  },
  methods: {},
  computed: {
    ...mapGetters([]),
  },
  watch: {},
  mounted() {},
});
</script>
