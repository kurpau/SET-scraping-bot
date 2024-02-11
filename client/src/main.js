import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import BaseButton from "./components/ui/BaseButton.vue";
import BaseCard from "./components/ui/BaseCard.vue";
import BaseSpinner from "./components/ui/BaseSpinner.vue";

const app = createApp(App);

app.use(router);

app.component("base-button", BaseButton);
app.component("base-card", BaseCard);
app.component("base-spinner", BaseSpinner);

app.mount("#app");
