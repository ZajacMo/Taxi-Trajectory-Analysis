import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import TlbsMap from "tlbs-map-vue";
import axios from "axios";

Vue.config.productionTip = false;
Vue.use(ElementUI).use(TlbsMap);
Vue.prototype.$http = axios;
new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
