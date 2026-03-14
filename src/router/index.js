import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Projects from "../views/Projects.vue";

const routes = [
  { path: "/", name: "", component: Home },
  { path: "/projects", name: "Projects", component: Projects },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
