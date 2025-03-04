<template>
  <div class="professor-container">
    <el-card class="professor-card">
      <h2>Professor Dashboard</h2>
      
      <el-descriptions title="Professor Information" :column="2" border>
        <el-descriptions-item label="Name">{{ professor.name }}</el-descriptions-item>
        <el-descriptions-item label="Course">{{ professor.course }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ professor.email }}</el-descriptions-item>
      </el-descriptions>

      <h3>Manage Student Grades</h3>
      <el-table :data="students" style="width: 100%" border>
        <el-table-column prop="name" label="Student Name" width="200"></el-table-column>
        <el-table-column prop="email" label="Email" width="250"></el-table-column>
        <el-table-column prop="grade" label="Grade" width="100">
          <template #default="scope">
            <el-input v-model="scope.row.grade" size="small" />
          </template>
        </el-table-column>
        <el-table-column prop="feedback" label="Feedback" width="300">
          <template #default="scope">
            <el-input v-model="scope.row.feedback" placeholder="Provide feedback" />
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="updateGrade(scope.row)">Save</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'ProfessorDashboard',
  setup() {
    const professor = ref({
      name: 'Dr. Jane Smith',
      course: 'Computer Science',
      email: 'janesmith@example.com'
    });

    const students = ref([
      { name: 'John Doe', email: 'johndoe@example.com', grade: 'B+', feedback: '' },
      { name: 'Alice Johnson', email: 'alicejohnson@example.com', grade: 'A', feedback: '' },
      { name: 'Michael Brown', email: 'michaelbrown@example.com', grade: 'B-', feedback: '' }
    ]);

    const updateGrade = (student) => {
      console.log('Updated Student:', student);
      ElMessage.success(`Updated grade for ${student.name}`);
    };

    return { professor, students, updateGrade };
  }
});
</script>

<style scoped>
.professor-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.professor-card {
  width: 80%;
  padding: 20px;
}
</style>
