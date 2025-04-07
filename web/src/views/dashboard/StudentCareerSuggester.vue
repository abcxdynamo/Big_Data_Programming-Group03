<template>
  <div class="career-container">
    <h3>Recommended Course</h3>
    <el-alert v-if="career" type="success" :closable="false" show-icon class="alert">
      <template #title>You are best suited for a career as a <strong>{{ career }}</strong>.</template>
    </el-alert>
    <p class="summary" v-if="career">This recommendation is based on patterns observed in successful graduates from your program. Consider focusing your efforts on building skills aligned with this career path.</p>
    <el-alert
      v-if="career && tips[career]"
      :title="`Pro Tip: ${tips[career]}`"
      type="info"
      show-icon
      class="pro-tip"
    />
  </div>
</template>

<script>
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";

export default {
  data() {
    return {
      user_id: null,
      career: '',
      tips: {
        "Data Scientist": "Strengthen your machine learning, Python, and statistics skills.",
        "Data Analyst": "Master SQL, Excel, and BI tools like Power BI or Tableau.",
        "Software Engineer": "Build strong foundations in algorithms and system design.",
        "Database Administrator": "Focus on SQL performance tuning and backup strategies.",
        "Cloud Engineer": "Get certified in platforms like AWS, Azure, or GCP.",
        "Others": "Explore various domains, and talk to an academic or career advisor for personalized paths."
      }
    };
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.fetch_prediction();
  },
  methods: {
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async fetch_prediction() {
      try {
        const response = await api.get(`/api/performance_predictions`);
        const prediction = response.find(p => p.student_id === this.user_id);
        if (prediction && prediction.predicted_career) {
          this.career = prediction.predicted_career;
        } else {
          this.career = "Others";
        }
      } catch (error) {
        console.error("Failed to fetch career prediction", error);
        this.career = "Others";
      }
    }
  }
};
</script>

<style scoped>
.career-container {
  padding: 20px;
  max-width: 800px;
  margin: auto;
}

.summary {
  font-size: 12px;
  font-weight: bold;
  font-style: italic;
  color: #555;
  margin: 16px 0;
  text-align: center;
}

</style>

