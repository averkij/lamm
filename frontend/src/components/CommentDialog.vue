<template>
  <v-dialog max-width="500px">
    <v-card>
      <div style="height: 400px">
        <v-card class="d-flex flex-column" style="height: 100%">
          <v-card-title class="justify-center pt-5 text-h6 px-6">
            Сделать заметку
          </v-card-title>

          <v-card-actions class="px-6 mt-3 pb-0"
            ><v-radio-group v-model="eventId">
              <v-radio label="Плохой промпт" value="commentBadPrompt"></v-radio>
              <v-radio label="Другое" value="commentOther"></v-radio>
            </v-radio-group>
          </v-card-actions>

          <v-textarea
            class="px-6 mt-0"
            variant="outlined"
            label="Комментарий"
            v-model="commentText"
          ></v-textarea>

          <v-spacer></v-spacer>
          <v-card-actions>
            <v-btn
              color="info"
              class="px-4"
              :disabled="inProgress"
              @click="close"
            >
              Отмена
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="info"
              class="px-4"
              :disabled="inProgress"
              @click="comment"
              >Отправить</v-btn
            >
          </v-card-actions>
        </v-card>
      </div>
    </v-card>
  </v-dialog>
</template>
  
  <script>
export default {
  name: "CommentDialog",
  props: {
    value: Boolean,
    inProgress: Boolean,
  },
  data() {
    return { commentText: "", eventId: "commentBadPrompt" };
  },
  methods: {
    comment() {
      this.$emit("comment", this.commentText, this.eventId);
    },
    close() {
      this.$emit("close");
    },
  },
  computed: {},
  mounted() {},
};
</script>
  