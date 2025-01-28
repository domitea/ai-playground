<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>AI Orchestrator</v-card-title>
      <v-switch v-model="darkMode" label="Tmavý režim"></v-switch>
      <v-text-field v-model="query" label="Zadejte dotaz..." outlined></v-text-field>
      <v-btn color="primary" @click="askAI" :disabled="loading">Odeslat</v-btn>
      <v-progress-linear v-if="loading" indeterminate></v-progress-linear>
      <v-divider class="my-4"></v-divider>

      <v-card v-if="response" class="pa-4">
        <v-card-title>Odpověď:</v-card-title>
        <v-card-text>{{ response }}</v-card-text>
      </v-card>

      <v-list v-if="history.length">
        <v-list-subheader>Historie dotazů</v-list-subheader>
        <v-list-item v-for="(item, index) in history" :key="index">
          <v-list-item-title>{{ item.query }}</v-list-item-title>
          <v-list-item-subtitle>{{ item.response }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import { ref, onMounted, watchEffect } from "vue";

export default {
  setup() {
    const query = ref("");
    const response = ref("");
    const history = ref([]);
    const loading = ref(false);
    const darkMode = ref(false);
    let ws = null;

    const askAI = () => {
      if (!query.value) return;
      loading.value = true;
      response.value = "";
      ws.send(JSON.stringify({ query: query.value }));
    };

    onMounted(() => {
      ws = new WebSocket("ws://localhost:8080/ws");

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        response.value += data.response + " ";
        if (!data.cached) {
          history.value.unshift({ query: query.value, response: response.value });
        }
        loading.value = false;
      };

      ws.onopen = () => console.log("WebSocket připojen!");
      ws.onerror = (error) => console.error("WebSocket error:", error);
      ws.onclose = () => console.log("WebSocket odpojen.");
    });

    return { query, response, history, loading, darkMode, askAI };
  },
};
</script>
