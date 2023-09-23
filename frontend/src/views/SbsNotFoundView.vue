<template>
  <v-row>
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
  name: "SbsNotFoundView",
  components: {},
  data() {
    return {
      API_URL,
    };
  },
  methods: {
    getImg() {
      return `${API_URL}static/img/sbs_not_found.jpeg`;
    },
  },
  computed: {
    ...mapGetters([]),
  },
  watch: {},
  mounted() {},
});
</script>
