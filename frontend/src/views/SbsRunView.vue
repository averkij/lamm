<template>
  <div>
    <v-row class="mt-1">
      <v-col cols="12" class="text-center text-h5">{{ sbsTasks[0][1] }}</v-col>
      <v-col cols="12"
        ><v-alert
          type="info"
          border="left"
          colored-border
          color="black-lighten-6"
          class="mt-6"
          elevation="0"
        >
          Ответы моделей расположены в произвольном порядке.
        </v-alert>
      </v-col> </v-row
    ><v-row class="mt-8">
      <v-col cols="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">{{
          sbsTasks[0][3]
        }}</v-card></v-col
      >
      <v-col cols="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">
          {{ sbsTasks[0][4] }}
        </v-card></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="12 mt-8" class="text-center">
        <v-btn color="blue" variant="tonal" @click="vote('left')"
          >Левый лучше</v-btn
        ><v-btn class="ml-8" color="blue" variant="tonal" @click="vote('right')"
          >Правый лучше</v-btn
        ><v-btn class="ml-8" color="green" variant="tonal" @click="vote('good')"
          >Оба хорошие</v-btn
        ><v-btn class="ml-8" color="red" variant="tonal" @click="vote('bad')"
          >Оба плохие</v-btn
        ><v-btn class="ml-8" color="grey" variant="tonal" @click="vote('skip')"
          >Пропустить</v-btn
        >
      </v-col>
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
    vote(answer) {
      this.getNextTask();
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
