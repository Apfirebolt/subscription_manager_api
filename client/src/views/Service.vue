<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Hello, {{ authData?.userData?.username || 'User' }}!</div>

    <div class="text-body1 q-mb-md">
      Welcome to your service dashboard. Here you can manage all your subscriptions in one place. Use the button below to add a new service and start tracking your expenses.
    </div>

    <div class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-4" v-for="service in services" :key="service.id">
            <q-card class="my-card">
            <q-card-section>
                <div class="text-h6">{{ service.name }}</div>
                <div class="text-subtitle2 text-grey-7">{{ service.description }}</div>
                <!-- Display logo_url -->
                <div v-if="service.logo_url" class="q-mt-sm">
                <q-img :src="service.logo_url" :alt="service.name + ' logo'" class="service-logo" />
                </div>
            </q-card-section>
            <q-card-actions align="right">
                <q-btn flat color="primary" label="Edit" @click="editService(service)" />
                <q-btn flat color="negative" label="Delete" @click="deleteService(service.id)" />
            </q-card-actions>
            </q-card>
        </div>
    </div>

    <q-dialog v-model="isServiceFormOpen" persistent>
      <q-card style="min-width: 350px; max-width: 500px; width: 100%;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Track New Subscription</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup @click="closeServiceForm" />
        </q-card-section>

        <q-card-section class="q-pt-md">
          <ServiceForm @close="closeServiceForm" />
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="openServiceForm">
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
const isServiceFormOpen = ref(false)
const serviceStore = useServiceStore()
console.log('Auth Data in Dashboard:', authData)

// Dummy placeholder methods for layout compilation stability
const editService = (service: any) => {
  console.log('Edit service', service)
}
const deleteService = (id: number) => {
  console.log('Delete service id', id)
}

// services
const services = computed(() => serviceStore.services) 

const openServiceForm = () => {
  isServiceFormOpen.value = true
}

// Fixed minor case syntax spacing typo from initial script copy
const closeServiceForm = () => {
  isServiceFormOpen.value = false
}

onMounted(() => {
  serviceStore.fetchServices()
})
</script>