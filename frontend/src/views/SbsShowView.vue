<template>
  <v-row>
    <v-col cols="12"><div class="text-h4">Информация об SBS</div></v-col>
    <v-col cols="12"
      ><p>Дата создания: {{ sbsInfo["create_ts"] }}</p>
      <p>Модель 1: {{ sbsInfo["model_1"] }}</p>
      <p>Модель 2: {{ sbsInfo["model_2"] }}</p>
    </v-col>
    <!-- <v-col cols="12">SBS статистика {{ sbsInfo }}</v-col> -->

    <v-col cols="12"><div class="text-h4">Результаты</div></v-col>
    <v-col>
      <div id="chart"></div>

      <!-- <div>{{ sbsStat.res }}</div> -->

      <!-- <ul>
        <li v-for="(item, i) in sbsStat.data" :key="i">
          {{ item }}
        </li>
      </ul> -->
    </v-col>
  </v-row>
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
              this.renderChart();
              this.setUpdateTimer();
            });
        });
    },
    setUpdateTimer() {
      setTimeout(() => {
        this.init();
      }, 5000);
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
          height: 350,
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
        // xaxis: {
        //   categories: [1],
        // },
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
          offsetX: 40,
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
