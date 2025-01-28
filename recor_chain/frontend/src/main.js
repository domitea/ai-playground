import { createApp } from "vue";
import App from "./App.vue";
import { createVuetify } from "vuetify";
import "vuetify/styles";
import VueNativeSock from "vue-native-websocket-vue3";

const vuetify = createVuetify();
const app = createApp(App);

app.use(vuetify);
app.use(VueNativeSock, "ws://localhost:8080/ws", {
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
});

app.mount("#app");
