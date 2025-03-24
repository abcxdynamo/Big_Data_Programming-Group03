<template>
    <div class="dashboard">
      <!-- Left Pane: Student Profile & Menu -->
      <div class="left-pane">
        <div class="profile">
          <img src="dummy-profile.png" alt="Profile Picture" class="profile-pic" />
          <h3>{{ student.name }}</h3>
          <p>ID: {{ student.id }}</p>
          <p>Email: {{ student.email }}</p>
        </div>
        <nav class="menu">
          <button v-for="item in menuItems" :key="item.name" @click="activeSection = item.component">
            {{ item.name }}
          </button>
        </nav>
      </div>
  
      <!-- Right Pane: Dynamic Content -->
      <div class="right-pane">
        <component :is="activeSection"></component>
      </div>
  
      <!-- Fixed Buttons: Home & Logout -->
      <button class="fixed-btn home-btn" @click="activeSection = 'PerformanceAnalysis'">Home</button>
      <button class="fixed-btn logout-btn" @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import PerformanceAnalysis from '../PerformanceAnalysis.vue';
  import Grades from '../Grades.vue';
  import Attendance from '../Attendance.vue';
  import CoopPredictor from '../CoopPredictor.vue';
  import CareerRecommendation from '../CareerRecommendation.vue';
  
  export default {
    components: {
      PerformanceAnalysis, Grades, Attendance, CoopPredictor, CareerRecommendation
    },
    data() {
      return {
        student: {
          name: 'John Doe',
          id: 'S1234567',
          email: 'johndoe@example.com'
        },
        menuItems: [
          { name: 'Grades', component: 'Grades' },
          { name: 'Attendance', component: 'Attendance' },
          { name: 'Co-op Predictor', component: 'CoopPredictor' },
          { name: 'Career Recommendation', component: 'CareerRecommendation' }
        ],
        activeSection: 'PerformanceAnalysis'
      };
    },
    methods: {
      logout() {
        console.log('Logging out...');
      }
    }
  };
  </script>
  
  <style scoped>
  .dashboard {
    display: flex;
    height: 100vh;
  }
  .left-pane {
    width: 250px;
    background: #2c3e50;
    color: white;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .profile-pic {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 10px;
  }
  .menu button {
    width: 100%;
    padding: 10px;
    margin: 5px 0;
    background: #34495e;
    color: white;
    border: none;
    cursor: pointer;
  }
  .menu button:hover {
    background: #1abc9c;
  }
  .right-pane {
    flex-grow: 1;
    padding: 20px;
  }
  .fixed-btn {
    position: fixed;
    bottom: 20px;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
  }
  .home-btn {
    left: 20px;
    background: #3498db;
    color: white;
  }
  .logout-btn {
    right: 20px;
    background: #e74c3c;
    color: white;
  }
  </style>