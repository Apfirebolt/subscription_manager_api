<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Hello, {{ authData?.userData?.username || 'User' }}!</div>

    Welcome to your service dashboard. Here you can manage all your subscriptions in one place. Use the button below to add a new service and start tracking your expenses.

    <ServiceForm />
    <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-4" v-for="service in services" :key="service.id">
            <q-card class="my-card">
            <q-card-section>
                <div class="text-h6">{{ service.name }}</div>
                <div class="text-subtitle2 text-grey-7">{{ service.category }}</div>
                <div class="text-body1 q-mt-sm">Next Billing Date: {{ new Date(service.next_billing_date).toLocaleDateString() }}</div>
                <div class="text-body1">Price: ${{ service.price }}</div>
            </q-card-section>
            <q-card-actions align="right">
                <q-btn flat color="primary" label="Edit" @click="editService(service)" />
                <q-btn flat color="negative" label="Delete" @click="deleteService(service.id)" />
            </q-card-actions>
            </q-card>
        </div>
    </div>

    <!-- Floating Action Button -->
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="addNewService">
        <q-tooltip>Add Service</q-tooltip>
      </q-btn>
    </q-page-sticky>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import ServiceForm from '../components/ServiceForm.vue'
import { useAuth } from '../store/auth'
import { useServiceStore } from '../store/service'

const $q = useQuasar()
const authStore = useAuth()
const authData = authStore.authData
const serviceStore = useServiceStore()
console.log('Auth Data in Dashboard:', authData)

// services
const services = computed(() => serviceStore.services) 

const addNewSubscription = () => {
  $q.notify({
    message: 'Add new subscription clicked',
    color: 'info'
  })
}

onMounted(() => {
  serviceStore.fetchServices()
})
</script>