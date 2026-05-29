<template>
  <q-footer elevated class="bg-grey-8 text-white">
    <q-toolbar>
      <q-toolbar-title>
        <div class="text-subtitle2">© {{ currentYear }} Subscription Manager</div>
      </q-toolbar-title>
      
      <div class="q-gutter-sm">
        <q-btn flat round dense icon="help_outline" size="sm">
          <q-tooltip>Help & Support</q-tooltip>
        </q-btn>
        <q-btn flat round dense icon="policy" size="sm">
          <q-tooltip>Privacy Policy</q-tooltip>
        </q-btn>
        <q-btn flat round dense icon="code" size="sm">
          <q-tooltip>API Docs</q-tooltip>
        </q-btn>
      </div>
    </q-toolbar>
  </q-footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped></style>