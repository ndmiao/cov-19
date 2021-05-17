import Vue from 'vue'
import Router from 'vue-router'
import Global from '@/components/Global'
import China from '@/components/China'
import News from '@/components/News'
import Load from '@/components/Load'
import AutoDisplay from '@/components/AutoDisplay'
import Admin from '@/components/Admin'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Global',

      component: Global
    },
    {
      path: '/China',
      name: 'China',

      component: China
    },
    {
      path: '/News',
      name: 'News',

      component: News
    },
    {
      path: '/AutoDisplay',
      name: 'AutoDisplay',

      component: AutoDisplay
    },
    {
      path: '/Load',
      name: 'Load',

      component: Load
    },
    {
      path: '/Admin',
      name: 'Admin',

      component: Admin
    }
  ]
})





 




