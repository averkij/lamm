<template>
  <div>
    <v-row>
      <v-col cols="12"><div class="text-h4">Информация об SBS</div></v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col cols="6">
        <v-card>
          <v-table>
            <tbody>
              <tr>
                <td>Дата создания</td>
                <td>{{ sbsInfo["create_ts"] }}</td>
              </tr>
              <tr>
                <td>Модель 1</td>
                <td>{{ sbsInfo["model_1"] }}</td>
              </tr>
              <tr>
                <td>Модель 2</td>
                <td>{{ sbsInfo["model_2"] }}</td>
              </tr>
            </tbody>
          </v-table></v-card
        >
      </v-col></v-row
    >
    <!-- <v-col cols="12">SBS статистика {{ sbsInfo }}</v-col> -->

    <v-row class="mt-5">
      <v-col cols="12"><div class="text-h4">Результаты</div></v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col cols="6">
        <v-card>
          <v-table v-if="sbsStat.res">
            <tbody>
              <tr>
                <td>Первый лучше</td>
                <td>{{ sbsStat.res["1"] }}</td>
              </tr>
              <tr>
                <td>Второй лучше</td>
                <td>{{ sbsStat.res["2"] }}</td>
              </tr>
              <tr>
                <td>Оба хорошие</td>
                <td>{{ sbsStat.res["3"] }}</td>
              </tr>
              <tr>
                <td>Оба плохие</td>
                <td>{{ sbsStat.res["4"] }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <!-- <div>{{ sbsStat.res }}</div> -->

        <!-- <ul>
        <li v-for="(item, i) in sbsStat.data" :key="i">
          {{ item }}
        </li>
      </ul> -->
      </v-col>
      <v-col cols="6">
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
import ApexCharts from "apexcharts";

export default defineComponent({
  name: "SbsShowView",
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
        });
    },
    formatSbs() {
      let sbs = this.calculateSbs(this.sbsStat.res);

      this.sbsRes = `${sbs[0]} : ${sbs[1]}`;
    },
    calculateSbs(data) {
      let model1 = data["1"];
      let model2 = data["2"];
      let bothGood = data["3"];
      let bothBad = data["4"];

      let total = model1 + model2 + bothGood + bothBad;

      if (!total) {
        total = 1;
      }

      let res1 = ((model1 + bothGood / 2) / total) * 100;
      let res2 = ((model2 + bothGood / 2) / total) * 100;
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
    renderChart() {
      let series = [
        {
          name: this.sbsInfo["model_1"],
          data: [this.sbsStat.res["1"]],
        },
        {
          name: this.sbsInfo["model_2"],
          data: [this.sbsStat.res["2"]],
        },
        {
          name: "Обе хороши",
          data: [this.sbsStat.res["3"]],
        },
        {
          name: "Обе плохи",
          data: [this.sbsStat.res["4"]],
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
