import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './routes' // Import the router configuration
import App from './App.vue'

// Import Quasar core and icon styles
import { Quasar } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(Quasar, {
  plugins: {},
})

app.mount('#app')