import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import BaseButton from "./components/ui/BaseButton.vue";

const app = createApp(App);

app.use(router);

app.component("base-button", BaseButton);

app.mount("#app");
