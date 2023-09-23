import {
  createRouter,
  createWebHistory
} from 'vue-router'

import HomeView from '../views/HomeView.vue'
import SbsRunView from '../views/SbsRunView.vue'
import SbsNotFoundView from '../views/SbsNotFoundView.vue'
import SbsShowView from '../views/SbsShowView.vue'

const router = createRouter({
  history: createWebHistory(
    import.meta.env.BASE_URL),
  routes: [{
      path: '/',
      name: 'main',
      component: HomeView,
    },
    {
      path: "/sbs/run/:hash",
      name: "sbsrun",
      component: SbsRunView
    },
    {
      path: "/sbs/run",
      redirect: `/`
    },
    {
      path: "/sbs/nooooooooooooo",
      name: "sbsNotFound",
      component: SbsNotFoundView
    },
    {
      path: "/sbs/show/:hash",
      name: "sbsshow",
      component: SbsShowView
    },
    {
      path: "/sbs/show",
      redirect: `/`
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: `/`
    },
  ]
})

export default router