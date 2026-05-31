<template>
  <q-layout view="lHh Lpr lFf">
    <HeaderComponent @toggle-drawer="leftDrawerOpen = !leftDrawerOpen" />

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-1"
    >
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        <q-item clickable to="/">
          <q-item-section avatar><q-icon name="dashboard" /></q-item-section>
          <q-item-section><q-item-label>Dashboard</q-item-label></q-item-section>
        </q-item>
        <q-item clickable to="/services">
          <q-item-section avatar><q-icon name="apps" /></q-item-section>
          <q-item-section><q-item-label>Services</q-item-label></q-item-section>
        </q-item>
        <q-item clickable to="/budget">
          <q-item-section avatar><q-icon name="attach_money" /></q-item-section>
          <q-item-section><q-item-label>Budget</q-item-label></q-item-section>
        </q-item>
        <q-item clickable to="/subscriptions">
          <q-item-section avatar><q-icon name="subscriptions" /></q-item-section>
          <q-item-section><q-item-label>Subscriptions</q-item-label></q-item-section>
        </q-item>
        <q-item clickable to="/profile">
          <q-item-section avatar><q-icon name="person" /></q-item-section>
          <q-item-section><q-item-label>Profile</q-item-label></q-item-section>
        </q-item>
        <q-item clickable to="/logout">
          <q-item-section avatar><q-icon name="logout" /></q-item-section>
          <q-item-section><q-item-label>Logout</q-item-label></q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <FooterComponent />
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import HeaderComponent from './components/HeaderComponent.vue'
import FooterComponent from './components/FooterComponent.vue'

const leftDrawerOpen = ref(false)
</script>