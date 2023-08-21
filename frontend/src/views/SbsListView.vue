<template>
  <v-row>
    <v-col cols="12">SBS список</v-col>
  </v-row>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";

export default defineComponent({
  name: "SbsListView",
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
