import _ from 'lodash'
import localStore from '../utils/store'
import {createRouter, createWebHistory} from 'vue-router'
import Index from '../views/Index.vue'
import Login from '../views/Login.vue'
import Student from '../views/dashboard/Student.vue'
import Professor from '../views/dashboard/Professor.vue'
import Admin from '../views/dashboard/Admin.vue'
import Forbidden from '../views/error/Forbidden.vue'
import PageNotFound from '../views/error/PageNotFound.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/login', component: Login},
        {path: '/', component: Index, meta: {requiresAuth: true, roles: ['STUDENT', 'PROFESSOR', 'ADMIN']}},
        {path: '/student', component: Student, meta: {requiresAuth: true, roles: ['STUDENT']}},
        {path: '/professor', component: Professor, meta: {requiresAuth: true, roles: ['PROFESSOR']}},
        {path: '/admin', component: Admin, meta: {requiresAuth: true, roles: ['ADMIN']}},
        {path: '/403', component: Forbidden},
        {path: '/:pathMatch(.*)*', component: PageNotFound}
    ]
})

// Route Guard
router.beforeEach((to, from, next) => {
    let user = {}
    try {
        user = JSON.parse(localStore.get('user') || '{}')
    } catch (e) {
        print(e)
    }
    if (to.meta.requiresAuth && !user.token) {
        next('/login')
    } else if (to.meta.roles && !_.includes(to.meta.roles, user['role_name'])) {
        next('/403')
    } else {
        next()
    }
});

// router.afterEach((to, from, next) => {
//     console.log(from);
//     console.log(to);
//     console.log(next);
//     console.log("---");
//     if (next) {
//         next();
//     }
// });


export default router;
