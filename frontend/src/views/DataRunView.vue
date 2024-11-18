<template>
  <div v-if="taskTitle">
    <v-row class="mt-0 pt-0" v-if="source_file">
      <v-col cols="12" class="text-left">
        <span class="text-subtitle-1">Source: </span><span class="text-h6 ml-2 source-title">{{ source_file }}</span>            
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" class=""><div v-html="taskTitle"></div></v-col>
      </v-row
    >
    <!-- <v-row class="mt-8">
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
    </v-row> -->
    <v-row class="mt-12">
      <v-col cols="12 mt-8 hidden-sm-and-down" class="text-center">
        <v-btn
          class="btn-main"
          color="green"
          variant="tonal"
          @click="vote('good')"
          :disabled="isLoading"
          >База</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="red"
          variant="tonal"
          @click="vote('bad')"
          :disabled="isLoading"
          >Не база</v-btn
        ></v-col
      ><v-col cols="12 mt-2 hidden-md-and-up" class="text-center"
        ><v-btn
          color="green"
          class="btn-main"
          variant="tonal"
          @click="vote('good')"
          :disabled="isLoading"
          >База</v-btn
        ><v-btn
          class="ml-8 btn-main"
          color="red"
          variant="tonal"
          @click="vote('bad')"
          :disabled="isLoading"
          >Не база</v-btn
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
  name: "DataRunView",
  data() {
    return {
      taskId: "",
      taskTitle: "",
      taskLeft: "",
      taskRight: "",
      taskMeta: "{}",
      isLoading: false,
      swapAnswers: false,
      showCommentDialog: false,
      commentInProgress: false,
    };
  },
  methods: {
    getSbsInfo() {
      this.$store
        .dispatch(GET_SBS_INFO, {
          sbsId: this.$route.params.hash,
        })
        .then(() => {
          if (this.sbsInfo["state"] == 3) {
            console.log("SBS finished.");
            this.$router.push({
              path: `/sbs/finished`,
            });
          }
        })
        .catch(() => {
          console.log("Can not get task. SBS not found.");
          this.$router.push({
            path: `/sbs/nooooooooooooo`,
          });
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
          this.taskTitle = this.formatTaskTitle(this.sbsTasks[0][1]);
          this.taskMeta = JSON.parse(this.sbsTasks[0][6]);
          console.log("Task:", this.taskMeta);

          if (this.swapAnswers) {
            this.taskLeft = this.sbsTasks[0][4];
            this.taskRight = this.sbsTasks[0][3];
          } else {
            this.taskLeft = this.sbsTasks[0][3];
            this.taskRight = this.sbsTasks[0][4];
          }

          this.isLoading = false;
        })
        .catch(() => {
          console.log("Can not get task. SBS not found.");
        });
    },
    formatTaskTitle(text) {
      let res = `<span class='pre-wrap text-h5'>${text}</span>`;
      let firstU = text.indexOf("U:");
      let lastA = text.indexOf("A:");

      if (firstU > 0 && lastA > 0) {
        let prefix = text.substring(0, firstU + 2);
        let postfix = text.substring(lastA, text.length);
        let query = text.substring(firstU + 2, lastA);

        res = `<span class='pre-wrap'>${prefix}</span><span class='text-h5 pre-wrap'>${query}</span><span class='pre-wrap'>${postfix}</span>`;
      }

      return res;
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
    source_file() {
      if (!this.taskMeta || !this.taskMeta.source_file || this.taskMeta.source_file == null) {
        return "";
      }
      return this.taskMeta.source_file;
    },
  },
  mounted() {
    this.getSbsInfo();
    this.getNextTask();
  },
  components: { CommentDialog },
});
</script>
