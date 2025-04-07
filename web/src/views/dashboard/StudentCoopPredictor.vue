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
      await this.fetch_grades();
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
      async fetch_grades() {
        try {
                const all_grades = await api.get(`/api/grades/list`);
                this.grades = all_grades.filter(g => g.student_id === this.user_id);
            } catch (error) {
                console.error("Error fetching grades:", error);
            }
      },            
      async calculate_coop_prediction() {
        if (this.grades.length === 0) {
                this.coop = {
                    coopPrediction: 0,
                    careerAdvice: "No academic record available for co-op assessment"
                };
                return;
        }
        const currentLevel = _.maxBy(this.grades, 'term_id')?.program_level;
        if (!currentLevel || currentLevel > 1) {
                this.coop = {
                    coopPrediction: 0,
                    careerAdvice: "Co-op eligibility is only available for Level 1 students"
                };
                return;
        }
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