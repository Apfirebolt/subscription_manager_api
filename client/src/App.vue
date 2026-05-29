<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>
          Subscription Manager
        </q-toolbar-title>
        <q-btn flat round dense icon="account_circle" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-md">
        <div class="text-h4 q-mb-md">Welcome back!</div>
        
        <q-card class="my-card bg-secondary text-white" style="max-width: 350px">
          <q-card-section>
            <div class="text-h6">Monthly Subscription Budget</div>
            <div class="text-subtitle2">Limit Tracker</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            Your current spending ring and analytics will show up here.
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>