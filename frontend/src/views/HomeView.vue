<template>
  <v-row>
    <!-- <v-col cols="12" class="text-h5">Главная страница</v-col> -->
    <v-col>
      <div>
        <v-img class="mt-10" :height="660" :src="getImg()"></v-img>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { defineComponent } from "vue";
import { API_URL } from "@/common/config";
import { mapGetters } from "vuex";

export default defineComponent({
  name: "HomeView",
  components: {},
  data() {
    return {
      API_URL,
    };
  },
  methods: {
    getImg() {
      return `${API_URL}static/img/home_2.jpeg`;
    },
  },
  computed: {
    ...mapGetters([]),
  },
  watch: {},
  mounted() {},
});
</script>
