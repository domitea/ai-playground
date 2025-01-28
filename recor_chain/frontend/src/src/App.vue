<template>
  <v-app>
    <v-container>
      <v-card class="pa-4">
        <v-card-title>AI Orchestrator</v-card-title>
        <v-text-field v-model="query" label="Zadejte dotaz..." outlined></v-text-field>
        <v-btn color="primary" @click="askAI">Odeslat</v-btn>
        <v-divider class="my-4"></v-divider>
        <v-card v-if="response" class="pa-4">
          <v-card-title>Odpověď:</v-card-title>
          <v-card-text>{{ response }}</v-card-text>
        </v-card>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data() {
    return { query: "", response: "", ws: new WebSocket("ws://localhost:8080/ws") };
  },
  methods: {
    askAI() { this.response = ""; this.ws.send(this.query); },
  },
  mounted() {
    this.ws.onmessage = (event) => { this.response += JSON.parse(event.data).response + " "; };
  }
};
</script>