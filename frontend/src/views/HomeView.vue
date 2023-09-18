<template>
  <v-row>
    <!-- <v-col cols="12" class="text-h5">Главная страница</v-col> -->
    <v-col>
      <div>
        <v-img
          class="mt-10"
          :height="660"
          src="https://habrastorage.org/webt/wk/ow/_g/wkow_gley98vpszdizm1fx5gnde.png"
        ></v-img>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { defineComponent } from "vue";

import { mapGetters } from "vuex";

export default defineComponent({
  name: "HomeView",
  components: {},
  data() {
    return {
      data: {},
    };
  },
  methods: {},
  computed: {
    ...mapGetters([]),
  },
  watch: {},
  mounted() {},
});
</script>
