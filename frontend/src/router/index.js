import {
  createRouter,
  createWebHistory
} from 'vue-router'

import HomeView from '../views/HomeView.vue'
import SbsRunView from '../views/SbsRunView.vue'
import SbsNotFoundView from '../views/SbsNotFoundView.vue'
import SbsShowView from '../views/SbsShowView.vue'
import SbsCommentsView from '../views/SbsCommentsView.vue'
import SbsFinishedView from '../views/SbsFinishedView.vue'

import DataRunView from '../views/DataRunView.vue'
import DataShowView from '../views/DataShowView.vue'
import DataCommentsView from '../views/DataCommentsView.vue'

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
      path: "/sbs/finished",
      name: "sbsFinished",
      component: SbsFinishedView
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
      path: "/sbs/comments/:hash",
      name: "sbscomments",
      component: SbsCommentsView
    },
    {
      path: "/data/check/:hash",
      name: "datarun",
      component: DataRunView
    },
    {
      path: "/data/check",
      redirect: `/`
    },
    {
      path: "/data/show/:hash",
      name: "datashow",
      component: DataShowView
    },
    {
      path: "/data/show",
      redirect: `/`
    },
    {
      path: "/data/comments/:hash",
      name: "datacomments",
      component: DataCommentsView
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: `/`
    },
  ]
})

export default router