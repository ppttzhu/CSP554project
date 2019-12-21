import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import BootstrapVue from "bootstrap-vue";

import "../node_modules/bootstrap/dist/css/bootstrap.min.css";

Vue.config.productionTip = false;

axios.defaults.baseURL = "http://localhost:9200/";

// globals
Vue.prototype.$http = axios;
Vue.prototype.$axios = axios;

Vue.use(BootstrapVue);

new Vue({
  render: h => h(App)
}).$mount("#app");
