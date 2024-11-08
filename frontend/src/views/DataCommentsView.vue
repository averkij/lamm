<template>
  <div>
    <!-- <v-row>
      <v-col cols="12"><div class="text-h4">Информация об SBS</div></v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col cols="12" sm="6">
        <v-card>
          <v-table>
            <tbody>
              <tr>
                <td>Модель 1</td>
                <td>{{ sbsInfo["model_1"] }}</td>
              </tr>
              <tr>
                <td>Средняя длина ответа</td>
                <td>{{ getExtra("avg_len_1") }}</td>
              </tr>
              <tr>
                <td>Количество уворотов</td>
                <td>{{ getExtra("sorry_1") }}</td>
              </tr>
            </tbody>
          </v-table></v-card
        >
      </v-col>
      <v-col cols="12" sm="6">
        <v-card>
          <v-table>
            <tbody>
              <tr>
                <td>Модель 2</td>
                <td>{{ sbsInfo["model_2"] }}</td>
              </tr>
              <tr>
                <td>Средняя длина ответа</td>
                <td>{{ getExtra("avg_len_2") }}</td>
              </tr>
              <tr>
                <td>Количество уворотов</td>
                <td>{{ getExtra("sorry_2") }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row> -->
    <!-- <v-col cols="12">SBS статистика {{ sbsInfo }}</v-col> -->

    <v-row v-if="showComments()">
      <v-col cols="12">
        <v-expansion-panels>
          <v-expansion-panel
            v-for="(item, i) in sbsComments"
            :key="i"
            :title="formatCommentTitle(item['comment'], i)"
          >
            <v-expansion-panel-text>
              <div>
                {{ item["prompt_1"] }}
              </div>
              <div>
                {{ item["model_1"] }}
              </div>
              <div>
                {{ item["model_2"] }}
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <!-- {{ sbsComments }} -->
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO } from "@/store/actions.type";
import { GET_SBS_COMMENTS } from "../store/actions.type";

export default defineComponent({
  name: "DataCommentsView",
  components: {},
  data() {
    return {
      chartRendered: false,
      chart: {},
      sbsRes: "",
    };
  },
  methods: {
    init() {
      this.$store
        .dispatch(GET_SBS_INFO, {
          sbsId: this.$route.params.hash,
        })
        .catch(() => {
          console.log("Can not get task. SBS not found.");
          this.$router.push({
            path: `/sbs/nooooooooooooo`,
          });
        });
      this.getSbsComments();
    },
    getSbsComments() {
      this.$store.dispatch(GET_SBS_COMMENTS, {
        sbsId: this.$route.params.hash,
      });
    },
    showComments() {
      if (this.sbsComments && this.sbsComments.length > 0) {
        return true;
      }
      return false;
    },
    formatCommentTitle(title, i) {
      if (!title || title == "") {
        return i + ".";
      }
      return `${i}. ${title}`;
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo", "sbsComments"]),
  },
  watch: {},
  mounted() {
    this.init();
  },
});
</script>
