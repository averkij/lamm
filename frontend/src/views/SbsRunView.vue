<template>
  <div>
    <v-row class="mt-1">
      <v-col cols="12" class="text-center text-h5">{{ taskTitle }}</v-col>
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
      <v-col cols="12" sm="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">
          {{ taskLeft }}
        </v-card></v-col
      >
      <v-col cols="12" sm="6"
        ><v-card elevation="1" class="pa-5 bg-yellow-lighten-5 pre-wrap">
          {{ taskRight }}
        </v-card></v-col
      >
    </v-row>
    <v-row>
      <v-col cols="12 mt-8 hidden-sm-and-down" class="text-center">
        <v-btn
          color="blue"
          class="btn-main"
          variant="tonal"
          @click="vote('left')"
          :disabled="isLoading"
          >Левый лучше</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="green"
          variant="tonal"
          @click="vote('good')"
          :disabled="isLoading"
          >Оба хорошие</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="red"
          variant="tonal"
          @click="vote('bad')"
          :disabled="isLoading"
          >Оба плохие</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="blue"
          variant="tonal"
          @click="vote('right')"
          :disabled="isLoading"
          >Правый лучше</v-btn
        > </v-col
      ><v-col cols="12 mt-8 hidden-md-and-up" class="text-center">
        <v-btn
          color="blue btn-main"
          variant="tonal"
          @click="vote('left')"
          :disabled="isLoading"
          ><span class="hidden-xs">Левый лучше</span
          ><span class="hidden-sm-and-up">Верхний лучше</span></v-btn
        ><v-btn
          class="ml-8"
          color="blue btn-main"
          variant="tonal"
          @click="vote('right')"
          :disabled="isLoading"
          ><span class="hidden-xs">Правый лучше</span
          ><span class="hidden-sm-and-up">Нижний лучше</span></v-btn
        > </v-col
      ><v-col cols="12 mt-2 hidden-md-and-up" class="text-center"
        ><v-btn
          color="green"
          class="btn-main"
          variant="tonal"
          @click="vote('good')"
          :disabled="isLoading"
          >Оба хорошие</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="red"
          variant="tonal"
          @click="vote('bad')"
          :disabled="isLoading"
          >Оба плохие</v-btn
        >
      </v-col>
      <v-col cols="12 mt-2" class="text-center"
        ><v-btn
          class="btn-main"
          color="grey"
          variant="tonal"
          @click="vote('skip')"
          :disabled="isLoading"
          >Пропустить</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="grey"
          variant="tonal"
          @click="
            // $refs.commentDialog.init();
            showCommentDialog = true
          "
          :disabled="isLoading"
          >Пометить</v-btn
        >
        <CommentDialog
          ref="commentDialog"
          v-model="showCommentDialog"
          :inProgress="commentInProgress"
          @comment="sendComment"
          @close="showCommentDialog = false"
        />
        <!-- :totalBatches="selectedProcessingTotalBatches" -->
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO, GET_TASK, RESOLVE_TASK } from "@/store/actions.type";
import CommentDialog from "@/components/CommentDialog.vue";

export default defineComponent({
  name: "SbsRunView",
  data() {
    return {
      taskId: "",
      taskTitle: "",
      taskLeft: "",
      taskRight: "",
      isLoading: false,
      swapAnswers: false,
      showCommentDialog: false,
      commentInProgress: false,
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
      this.doRandomSwap();
      this.$store
        .dispatch(GET_TASK, {
          sbsId: this.$route.params.hash,
          userId: this.userId,
        })
        .then(() => {
          this.taskId = this.sbsTasks[0][0];
          this.taskTitle = this.sbsTasks[0][1];

          if (this.swapAnswers) {
            this.taskLeft = this.sbsTasks[0][4];
            this.taskRight = this.sbsTasks[0][3];
          } else {
            this.taskLeft = this.sbsTasks[0][3];
            this.taskRight = this.sbsTasks[0][4];
          }

          this.isLoading = false;
        });
    },
    sendComment(comment, event) {
      this.commentInProgress = true;
      console.log("Comment:", comment, "Event:", event);

      this.$store
        .dispatch(RESOLVE_TASK, {
          sbsId: this.$route.params.hash,
          userId: this.userId,
          taskId: this.taskId,
          tryId: this.tryId,
          comment: comment,
          answer: event,
        })
        .then(() => {
          this.commentInProgress = false;
          this.showCommentDialog = false;
        });
    },
    vote(answer) {
      //change answer if swapped
      if (this.swapAnswers) {
        if (answer == "left") {
          answer = "right";
        } else if (answer == "right") {
          answer = "left";
        }
      }

      this.$store
        .dispatch(RESOLVE_TASK, {
          sbsId: this.$route.params.hash,
          userId: this.userId,
          taskId: this.taskId,
          tryId: this.tryId,
          answer: answer,
        })
        .then(() => {
          this.getNextTask();
          this.getSbsInfo();
        });
    },
    doRandomSwap() {
      let r = Math.round(Math.random());
      if (r == 1) {
        this.swapAnswers = true;
        console.log("[swap answers]");
      } else {
        this.swapAnswers = false;
      }
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo", "sbsTasks", "tryId"]),
  },
  mounted() {
    this.getSbsInfo();
    this.getNextTask();
  },
  components: { CommentDialog },
});
</script>
