<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="header">
      <h1>Student Dashboard</h1>
    </div>

    <!-- Grades Section -->
    <div class="card">
      <h2>Academic Performance</h2>
      <div v-if="grades.length > 0">
        <table class="grades-table">
          <thead>
            <tr>
              <th>Course</th>
              <th>Grade</th>
              <th>Term</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="grade in grades" :key="grade.course">
              <td>{{ grade.course }}</td>
              <td :class="getGradeClass(grade.score)">{{ grade.score }}</td>
              <td>{{ grade.term }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No grades available</p>
    </div>

    <!-- Co-op Prediction -->
    <div class="card">
      <h2>Co-op Eligibility</h2>
      <div v-if="coopPrediction">
        <div class="prediction-status" :class="coopPrediction.eligible ? 'eligible' : 'not-eligible'">
          {{ coopPrediction.eligible ? 'Eligible' : 'Not Eligible' }}
        </div>
        <p>Success Probability: {{ (coopPrediction.probability * 100).toFixed(1) }}%</p>
      </div>
      <p v-else>Loading prediction...</p>
    </div>

    <!-- Career Prediction -->
    <div class="card">
      <h2>Career Recommendation</h2>
      <div v-if="careerPrediction">
        <h3>{{ careerPrediction.career }}</h3>
        <div class="confidence-meter">
          <div class="meter-bar" :style="{ width: careerPrediction.confidence * 100 + '%' }"></div>
        </div>
        <p>{{ (careerPrediction.confidence * 100).toFixed(1) }}% Confidence</p>
      </div>
      <p v-else>Generating recommendations...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      grades: [],
      coopPrediction: null,
      careerPrediction: null
    }
  },
  methods: {
    getGradeClass(score) {
      return score >= 80 ? 'grade-a' : score >= 60 ? 'grade-b' : 'grade-c';
    },
    async fetchData() {
      try {
        // Fetch grades
        const gradesRes = await axios.get('/api/student/grades');
        this.grades = gradesRes.data;

        // Fetch co-op prediction
        const coopRes = await axios.get('/api/student/coop-prediction');
        this.coopPrediction = coopRes.data;

        // Fetch career prediction
        const careerRes = await axios.get('/api/student/career-prediction');
        this.careerPrediction = careerRes.data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  },
  mounted() {
    this.fetchData();
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}

.card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.grades-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.grades-table th, .grades-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.grade-a { color: #4CAF50; }
.grade-b { color: #FFC107; }
.grade-c { color: #F44336; }

.prediction-status {
  font-size: 1.2rem;
  margin: 1rem 0;
}

.eligible { color: #4CAF50; }
.not-eligible { color: #F44336; }

.confidence-meter {
  height: 10px;
  background: #eee;
  border-radius: 5px;
  margin: 1rem 0;
}

.meter-bar {
  height: 100%;
  background: #2196F3;
  border-radius: 5px;
  transition: width 0.5s ease;
}
</style>