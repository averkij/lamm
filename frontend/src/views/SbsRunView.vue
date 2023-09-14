<template>
  <div>
    <v-row class="mt-1">
      <v-col cols="12" class="text-center text-h5"
        >{{ taskId }}. {{ taskTitle }}</v-col
      >
      <v-col cols="12"
        ><v-alert
          type="info"
          border="left"
          colored-border
          color="black-lighten-6"
          class="mt-6"
          elevation="0"
        >
          Ответы моделей расположены в случайном порядке.
        </v-alert>
      </v-col> </v-row
    ><v-row class="mt-8">
      <v-col cols="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">{{
          taskLeft
        }}</v-card></v-col
      >
      <v-col cols="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">
          {{ taskRight }}
        </v-card></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="12 mt-8" class="text-center">
        <v-btn
          color="blue"
          variant="tonal"
          @click="vote('left')"
          :disabled="isLoading"
          >Левый лучше</v-btn
        ><v-btn
          class="ml-8"
          color="green"
          variant="tonal"
          @click="vote('good')"
          :disabled="isLoading"
          >Оба хорошие</v-btn
        ><v-btn
          class="ml-8"
          color="red"
          variant="tonal"
          @click="vote('bad')"
          :disabled="isLoading"
          >Оба плохие</v-btn
        ><v-btn
          class="ml-8"
          color="blue"
          variant="tonal"
          @click="vote('right')"
          :disabled="isLoading"
          >Правый лучше</v-btn
        >
      </v-col>
      <v-col cols="12 mt-2" class="text-center"
        ><v-btn
          class="ml-8"
          color="grey"
          variant="tonal"
          @click="vote('skip')"
          :disabled="isLoading"
          >Пропустить</v-btn
        ></v-col
      >
    </v-row>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO, GET_TASK, RESOLVE_TASK } from "@/store/actions.type";

export default defineComponent({
  name: "SbsRunView",
  components: {},
  data() {
    return {
      taskId: "",
      taskTitle: "",
      taskLeft: "",
      taskRight: "",
      isLoading: false,
    };
  },
  methods: {
    getSbsInfo() {
      this.$store.dispatch(GET_SBS_INFO, {
        sbsId: this.$route.params.hash,
      });
    },
    getNextTask() {
      this.isLoading = true;
      this.$store
        .dispatch(GET_TASK, {
          sbsId: this.$route.params.hash,
          userId: this.userId,
        })
        .then(() => {
          this.taskId = this.sbsTasks[0][0];
          this.taskTitle = this.sbsTasks[0][1];
          this.taskLeft = this.sbsTasks[0][3];
          this.taskRight = this.sbsTasks[0][4];
          this.isLoading = false;
        });
    },
    vote(answer) {
      this.$store
        .dispatch(RESOLVE_TASK, {
          sbsId: this.$route.params.hash,
          userId: this.userId,
          taskId: this.taskId,
          answer: answer,
        })
        .then(() => {
          this.getNextTask();
          this.getSbsInfo();
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
