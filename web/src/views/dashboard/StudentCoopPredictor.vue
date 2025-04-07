<template>
    <div>
        <h3>Co-op Prediction</h3>
        <el-progress :percentage="coop.coopPrediction" status="success" />
        <p><strong>Chance:</strong> {{ coop.coopPrediction }}%</p>
        <p><strong>Advice:</strong> {{ coop.careerAdvice }}</p>
    </div>
</template>
  
  <script>
  import { defineComponent, ref, onMounted } from 'vue';
  import localStore from "@/utils/store.js";
  import api from "@/utils/api.js";
  import _ from 'lodash';
  
  export default {
    data() {
      return {
        coop: {
          coopPrediction: 0,
          careerAdvice: ''
        },
      }
    },
    computed: {
  
    },
    async created() {
      this.user_id = this.$route.params.id || this.get_login_user_id();
      await this.get_user_info();
      await this.calculate_coop_prediction();
    },
    mounted() {
  
    },
    methods: {
      get_login_user_id() {
        return JSON.parse(localStore.get("user"))["user_id"];
      },
      async get_user_info() {
        this.user_info = await api.get(`/api/users/info/${this.user_id}`);
      },
      async calculate_coop_prediction() {
        const allPredictions = await api.get(`/api/performance_predictions`);
        const sorted = _.orderBy(allPredictions, 'predicted_average', 'desc');
        const studentPrediction = sorted.find(p => p.student_id === this.user_id);
        if (!studentPrediction || studentPrediction.predicted_average < 80) {
          this.coop = {
            coopPrediction: 0,
            careerAdvice: "Work on improving your average to qualify for co-op."
          };
          return;
        }
        const rank = sorted.findIndex(p => p.student_id === this.user_id) + 1;
        if (rank <= 10) {
          this.coop = {
            coopPrediction: 100,
            careerAdvice: "Great job! You're in the top 10 for co-op eligibility."
          };
        } else {
          const scale = Math.max(100 - (rank - 10) * 2, 30);
          this.coop = {
            coopPrediction: scale,
            careerAdvice: "You're eligible, but improve your rank to get selected."
          };
        }
        console.log(this.coop)
      }
    }
  };
  </script>