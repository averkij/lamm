<template>
  <v-row>
    <v-col cols="12">Главная страница</v-col>
    <!-- <v-row
        ></v-row
      >
      <div class="d-flex align-center mt-8">
        <div class="d-inline-block" style="flex: auto">
          <v-text-field
            v-model="query"
            :append-icon="'mdi-send'"
            @click:append="sendMessage"
            @keydown.enter.prevent="sendMessage"
            clearable
            label="Тема"
            type="input"
            variant="outlined"
          ></v-text-field>
        </div>
      </div>
      <v-row class="mt-6">
        <v-col class="text-center table-label">Сильные стороны</v-col>
        <v-col class="text-center table-label">Слабые стороны</v-col>
      </v-row>
      <v-row>
        <div class="left-title text-center table-label">Внутренняя среда</div>
        <v-col>
          <v-card flat class="pa-2 bg-green" title="Плюсы">
            <v-card
              v-for="item in data.s"
              variant="outlined"
              :key="item"
              class="ma-2 bg-white"
            >
              <v-card-item>
                <div>
                  <div class="text-body-1">
                    {{ item.title }}. {{ item.text }}
                  </div>
                </div>
              </v-card-item>
            </v-card>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat class="pa-2 bg-blue" title="Минусы">
            <v-card
              v-for="item in data.w"
              variant="outlined"
              :key="item"
              class="ma-2 bg-white"
            >
              <v-card-item>
                <div>
                  <div class="text-body-1">
                    {{ item.title }}. {{ item.text }}
                  </div>
                </div>
              </v-card-item>
            </v-card>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <div class="left-title text-center table-label">Внешняя среда</div>
        <v-col>
          <v-card flat class="pa-2 bg-yellow" title="Возможности">
            <v-card
              v-for="item in data.o"
              variant="outlined"
              :key="item"
              class="ma-2 bg-white"
            >
              <v-card-item>
                <div>
                  <div class="text-body-1">
                    {{ item.title }}. {{ item.text }}
                  </div>
                </div>
              </v-card-item>
            </v-card>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat class="pa-2 bg-red" title="Угрозы">
            <v-card
              v-for="item in data.t"
              variant="outlined"
              :key="item"
              class="ma-2 bg-white"
            >
              <v-card-item>
                <div>
                  <div class="text-body-1">
                    {{ item.title }}. {{ item.text }}
                  </div>
                </div>
              </v-card-item>
            </v-card>
          </v-card>
        </v-col>
      </v-row>
    </v-col> -->
  </v-row>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { DataProvider } from "@/common/data.provider";
import { mapGetters } from "vuex";

export default defineComponent({
  name: "HomeView",
  components: {
    DataProvider,
  },
  data() {
    return {
      answer: "...",
      query: "жизни кошки",
      data: {
        s: [
          {
            title: "",
            text: "",
          },
        ],
        w: [
          {
            title: "",
            text: "",
          },
        ],
        o: [
          {
            title: "",
            text: "",
          },
        ],
        t: [
          {
            title: "",
            text: "",
          },
        ],
      },
    };
  },
  methods: {
    sendMessage() {
      this.data = DataProvider.getSWOT(this.query);
    },
  },
  computed: {
    ...mapGetters([]),
  },
  watch: {},
  mounted() {
    this.data = DataProvider.getSWOT(this.query);
  },
});
</script>
