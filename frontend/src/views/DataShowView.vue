<template>
  <div>
    <v-row>
      <v-col cols="12"><div class="text-h4">Оценка данных</div></v-col>
    </v-row>

    <v-row>
      <v-col>
        <div>
          <v-img class="mt-10" :height="260" :src="getQrImg()"></v-img>
        </div>
      </v-col>
    </v-row>
    
    <v-row class="mt-2">
      <v-col cols="12" sm="6">
        <v-badge
          v-if="sbsInfo['state'] == 0"
          color="info"
          content="В работе"
          inline
        ></v-badge>
        <v-badge v-else color="success" content="Завершено" inline></v-badge>
      </v-col>
    </v-row>

    <v-row class="mt-5">
      <v-col cols="12"><div class="text-h4">Результаты</div></v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col cols="12" sm="6">
        <v-card>
          <v-table v-if="sbsStat.res">
            <tbody>
              <tr>
                <td>Норм</td>
                <td>{{ sbsStat.res["3"] }}</td>
              </tr>
              <tr>
                <td>Фигня</td>
                <td>{{ sbsStat.res["4"] }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6">
        <v-card class="pa-5 fill-height d-flex align-center justify-center">
          <div class="text-h5">
            {{ this.sbsRes }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12"><div class="mt-4" id="chart"></div></v-col>
    </v-row>
  </div>
</template>

<script>
import { defineComponent } from "vue";

// Components
import { mapGetters } from "vuex";
import { GET_SBS_INFO, GET_SBS_STAT } from "@/store/actions.type";
import { API_URL } from "@/common/config";
import ApexCharts from "apexcharts";

export default defineComponent({
  name: "DataShowView",
  components: {},
  data() {
    return {
      chartRendered: false,
      chart: {},
      sbsRes: "",
      API_URL,
    };
  },
  methods: {
    init() {
      this.$store
        .dispatch(GET_SBS_INFO, {
          sbsId: this.$route.params.hash,
        })
        .then(() => {
          this.$store
            .dispatch(GET_SBS_STAT, {
              sbsId: this.$route.params.hash,
            })
            .then(() => {
              this.formatSbs();
              this.renderChart();
              this.setUpdateTimer();
            });
        })
        .catch(() => {
          console.log("Can not get task. SBS not found.");
          this.$router.push({
            path: `/sbs/nooooooooooooo`,
          });
        });
    },
    getExtra(key) {
      if (
        !this.sbsInfo ||
        !this.sbsInfo["extra_data"] ||
        !(key in this.sbsInfo["extra_data"])
      ) {
        return "";
      }
      return this.sbsInfo["extra_data"][key];
    },
    formatSbs() {
      let sbs = this.calculateSbs(this.sbsStat.res);

      this.sbsRes = `${sbs[0]} : ${sbs[1]}`;
    },
    calculateSbs(data) {
      let bothGood = data["3"];
      let bothBad = data["4"];

      let total = bothGood + bothBad;

      if (!total) {
        total = 1;
      }

      let res1 = (bothGood / total) * 100;
      let res2 = (bothBad / total) * 100;
      return [res1.toFixed(2), res2.toFixed(2)];
    },
    setUpdateTimer() {
      setTimeout(() => {
        this.init();
      }, 10000);
    },
    getSbsInfo() {
      this.$store.dispatch(GET_SBS_INFO, {
        sbsId: this.$route.params.hash,
      });
    },
    getSbsStat() {
      this.$store.dispatch(GET_SBS_STAT, {
        sbsId: this.$route.params.hash,
      });
    },
    getQrImg() {
      console.log(`${API_URL}static/img/${this.$route.params.hash}.png`)
      return `${API_URL}static/img/${this.$route.params.hash}.png`;
    },
    renderChart() {
      let series = [
        {
          name: "Норм",
          data: [this.sbsStat.res["3"]],
          color: "#3ae396"
        },
        {
          name: "Фигня",
          data: [this.sbsStat.res["4"]],
          color: "#f54f12"
        },
      ];
      var options = {
        chart: {
          type: "bar",
          stacked: true,
          stackType: "100%",
          height: 200,
        },
        series: series,
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        title: {
          text: this.sbsInfo["comment"],
        },
        xaxis: {
          categories: [1],
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return val;
            },
          },
        },
        fill: {
          opacity: 1,
        },
        legend: {
          position: "top",
          horizontalAlign: "left",
          offsetX: 20,
        },
      };

      if (!this.chartRendered) {
        this.chart = new ApexCharts(document.querySelector("#chart"), options);
        this.chart.render();
        this.chartRendered = true;
      } else {
        this.chart.updateSeries(series);
      }
    },
  },
  computed: {
    ...mapGetters(["userId", "userName", "sbsInfo", "sbsStat"]),
  },
  watch: {},
  mounted() {
    this.init();
  },
});
</script>
