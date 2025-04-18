<template>
  <div>
    <div v-if="taskText">
      <v-row class="mt-0 pt-0" v-if="source_file">
        <v-col cols="12" class="text-left">
          <span class="text-subtitle-1">Источник: </span
          ><span class="text-h6 ml-2 source-title">{{ source_file }}</span>
        </v-col>
      </v-row>

      <div class="switch-controls">
        <v-switch
          v-model="renderMarkdown"
          color="primary"
          label="Markdown"
          hide-details
          density="compact"
          :disabled="showDiff"
        ></v-switch>
        <!-- <v-switch
          v-if="taskMeta.spell_check_success"
          v-model="showDiff"
          color="primary"
          label="Показать разницу"
          hide-details
          density="compact"
          class="mt-2"
          :disabled="renderMarkdown || showCorrected"
        ></v-switch> -->
        <!-- <v-switch
          v-if="taskMeta.spell_check_success"
          v-model="showCorrected"
          color="primary"
          label="Исправленный текст"
          hide-details
          density="compact"
          class="mt-2"
          :disabled="showDiff"
        ></v-switch> -->
      </div>

      <!-- <v-row v-if="taskMeta.spell_check_success" class="mt-4 mb-2">
        <v-col cols="12">
          <v-chip
            color="blue"
            size="small"
            class="mr-2"
          >
            <v-icon start size="small">mdi-spellcheck</v-icon>
            Spell check passed
          </v-chip>
          <v-chip
            v-if="taskMeta.spell_check_chunks_processed > 1"
            color="grey"
            size="small"
          >
            {{ taskMeta.spell_check_chunks_processed }} chunks processed
          </v-chip>
        </v-col>
      </v-row> -->

      <v-row v-if="showSpellCheck && taskMeta.spell_check_success" class="mt-1">
        <v-col cols="12">
          <v-chip
            color="blue"
            size="small"
            class="mr-2"
          >
            <v-icon start size="small">mdi-spellcheck</v-icon>
            Spell check passed
          </v-chip>
          <v-chip
            v-if="taskMeta.spell_check_chunks_processed > 1"
            color="grey"
            size="small"
          >
            {{ taskMeta.spell_check_chunks_processed }} chunks processed
          </v-chip>
        </v-col>
      </v-row>

      <!-- <div>{{ this.taskMeta.corrected }}</div>
      <div>{{ this.taskMeta.html_diff }}</div> -->

      <v-row class="mt-4">
        <!-- condition class text-h5 -->
        <v-col
          cols="12"
          class="text-h5"
          :class="{ 'markdown-content': renderMarkdown, 'pre-wrap': !renderMarkdown }"
          ><div v-html="displayText"></div
        ></v-col>
      </v-row>

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
        <v-col cols="12 mt-4" class="text-center"
          ><v-btn
            class="btn-main btn-white"
            color="white"
            variant="flat"
            @click="vote('skip')"
            :disabled="isLoading"
            >⏩ Пропустить</v-btn
          ><v-btn
            class="ml-8 btn-main btn-white"
            color="white"
            variant="flat"
            @click="
              // $refs.commentDialog.init();
              showCommentDialog = true
            "
            :disabled="isLoading"
            >🖊️ Пометить</v-btn
          >
          <!-- <v-btn
            class="ml-8 btn-main btn-white"
            color="white"
            variant="flat"
            @click="spellCheck"
            :disabled="isLoading || spellCheckInProgress || taskMeta.spell_check_success"
          >         
            <v-progress-circular
              v-if="spellCheckInProgress"
              indeterminate
              size="20"
              width="2"
              color="white"
              class="mr-2"
            ></v-progress-circular>
            ✅ Проверить
          </v-btn> -->
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
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
    >
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO, GET_TASK, RELOAD_TASK, RESOLVE_TASK } from "@/store/actions.type";
import CommentDialog from "@/components/CommentDialog.vue";
import { marked } from "marked";
import { SbsService } from "@/common/api.service";

export default defineComponent({
  name: "DataRunView",
  data() {
    return {
      taskId: "",
      taskText: "",
      taskLeft: "",
      taskRight: "",
      taskMeta: "{}",
      isLoading: false,
      swapAnswers: false,
      showCommentDialog: false,
      commentInProgress: false,
      renderMarkdown: false,
      spellCheckInProgress: false,
      showSpellCheck: false,
      showDiff: false,
      showCorrected: false,
      snackbar: false,
      snackbarText: '',
      snackbarColor: '',
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
          this.taskText = this.formatTaskText(this.sbsTasks[0][1]);
          this.taskMeta = JSON.parse(this.sbsTasks[0][6]);
          this.taskMeta.corrected = this.sbsTasks[0][8];
          this.taskMeta.html_diff = this.sbsTasks[0][9];
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
    formatTaskText(text) {
      // let res = `<span class='pre-wrap text-h5'>${text}</span>`;
      // let firstU = text.indexOf("U:");
      // let lastA = text.indexOf("A:");

      // if (firstU > 0 && lastA > 0) {
      //   let prefix = text.substring(0, firstU + 2);
      //   let postfix = text.substring(lastA, text.length);
      //   let query = text.substring(firstU + 2, lastA);

      //   res = `<span class='pre-wrap'>${prefix}</span><span class='text-h5 pre-wrap'>${query}</span><span class='pre-wrap'>${postfix}</span>`;
      // }

      // return res;
      return text;
    },
    renderAsMarkdown(text) {
      // Extract the HTML content from the formatting structure
      // let content = text;

      // // Simple regex to extract text from HTML spans
      // const htmlRegex = /<span[^>]*>(.*?)<\/span>/g;
      // let matches = [];
      // let match;
      // while ((match = htmlRegex.exec(text)) !== null) {
      //   matches.push(match[1]);
      // }

      // if (matches.length > 0) {
      //   // Join all extracted content
      //   content = matches.join('');
      // }

      // Render the content as markdown
      return marked(text);
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
    spellCheck() {      
      this.spellCheckInProgress = true;
      
      SbsService.spellCheck({
        sbsId: this.$route.params.hash,
        taskId: this.taskId
      })
      .then(() => {
        this.$store
          .dispatch(RELOAD_TASK, {
            sbsId: this.$route.params.hash,
            taskId: this.taskId,
            userId: this.userId,
          })
          .then(() => {
            this.taskText = this.formatTaskText(this.sbsTasks[0][1]);
            this.taskMeta = JSON.parse(this.sbsTasks[0][6]);
            this.taskMeta.corrected = this.sbsTasks[0][8];
            this.taskMeta.html_diff = this.sbsTasks[0][9];
            this.spellCheckInProgress = false;
            
            if (this.taskMeta.spell_check_success) {
              // this.renderMarkdown = false;
              // this.showSpellCheck = true;
              this.snackbarText = 'Spell check completed successfully';
              this.snackbarColor = 'success';
              this.snackbar = true;
            } else {
              this.snackbarText = 'Spell check failed';
              this.snackbarColor = 'error';
              this.snackbar = true;
            }
          });
      })
      .catch(error => {
        console.error('Error during spell check:', error);
        this.spellCheckInProgress = false;
        this.snackbarText = 'Error performing spell check';
        this.snackbarColor = 'error';
        this.snackbar = true;
      });
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo", "sbsTasks", "tryId"]),
    source_file() {
      if (
        !this.taskMeta ||
        !this.taskMeta.source_file ||
        this.taskMeta.source_file == null
      ) {
        return "";
      }
      return this.taskMeta.source_file;
    },
    displayText() {
      if (this.showCorrected && this.taskMeta.corrected && this.taskMeta.spell_check_success) {
        if (this.renderMarkdown) {
          return this.renderAsMarkdown(this.taskMeta.corrected);
        }
        return this.taskMeta.corrected;
      }
      if (this.showDiff && this.taskMeta.html_diff && this.taskMeta.spell_check_success) {
        return this.taskMeta.html_diff;
      }
      if (this.renderMarkdown) {
        return this.renderAsMarkdown(this.taskText);
      }
      if (this.showSpellCheck && this.taskMeta.spell_check_html_diff && this.taskMeta.spell_check_success) {
        return this.taskMeta.spell_check_html_diff;
      }
      return this.taskText;
    },
  },
  mounted() {
    this.getSbsInfo();
    this.getNextTask();
  },
  watch: {
    showDiff(newVal) {
      if (newVal) {
        this.renderMarkdown = false;
        this.showCorrected = false;
      }
    },
    showCorrected(newVal) {
      if (newVal) {
        this.showDiff = false;
      }
    },
    renderMarkdown(newVal) {
      if (newVal && this.showDiff) {
        this.showDiff = false;
      }
    }
  },
  components: { CommentDialog },
});
</script>

<style scoped>
.markdown-content :deep(p) {
  text-indent: 0px !important;
}

.markdown-content :deep(ol) {
  padding-left: 20px;
  margin-bottom: 1em;
}

.markdown-content :deep(ul) {
  list-style-type: disc;
  padding-left: 20px;
  margin-bottom: 1em;
}

.markdown-content :deep(p) {
  line-height: 1.6;
}

.markdown-content :deep(h3) {

  margin-bottom: 1em;
}

div {
  line-height: 1.5;
}

.markdown-content :deep(p:not(:last-child)) {
  margin-bottom: 0.6em;
}

.btn-white:disabled {
  color: #ccc !important;
}

.switch-controls {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 100;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>