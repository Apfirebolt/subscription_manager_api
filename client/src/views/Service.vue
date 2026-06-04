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
            <div v-if="service.logo_url" class="q-mt-sm">
              <q-img :src="service.logo_url" :alt="service.name + ' logo'" class="service-logo" />
            </div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat color="primary" label="Edit" @click="editService(service)" />
            <q-btn flat color="negative" label="Delete" @click="confirmDeleteService(service)" />
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="isServiceFormOpen" persistent>
      <q-card style="min-width: 350px; max-width: 500px; width: 100%;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Track New Service</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup @click="closeServiceForm" />
        </q-card-section>

        <q-card-section class="q-pa-none">
          <ServiceForm @close="closeServiceForm" :service="selectedService" @createService="closeServiceForm" />
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="isConfirmOpen" persistent>
      <ConfirmDialog
        title="Delete Service?"
        :message="`Are you sure you want to permanently remove ${serviceToDelete?.name || 'this service'}?`"
        ok-label="Delete"
        ok-color="negative"
        icon="delete_forever"
        icon-color="negative"
        :loading="serviceStore.isLoading"
        @confirm="handleDeleteService"
        @cancel="closeConfirmDialog"
      />
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
import ConfirmDialog from '../components/ConfirmModal.vue'
import { useAuth } from '../store/auth'
import { useServiceStore } from '../store/service'

const $q = useQuasar()
const authStore = useAuth()
const authData = authStore.authData
const serviceStore = useServiceStore()

// Service Form State
const isServiceFormOpen = ref(false)
const selectedService = ref(null)

// Confirmation Dialog State
const isConfirmOpen = ref(false)
const serviceToDelete = ref<any | null>(null)

// Services
const services = computed(() => serviceStore.services) 

const editService = (service: any) => {
  selectedService.value = service
  isServiceFormOpen.value = true
}

// Step 1: Open confirmation dialog and save service payload context
const confirmDeleteService = (service: any) => {
  serviceToDelete.value = service
  isConfirmOpen.value = true
}

// Step 2: Run store action when user hits 'OK'
const handleDeleteService = async () => {
  if (serviceToDelete.value) {
    try {
      await serviceStore.deleteService(serviceToDelete.value.id)
      // Close the modal only after successful deletion
      closeConfirmDialog()
    } catch (error) {
      console.error("Failed to delete service:", error)
    }
  }
}

const closeConfirmDialog = () => {
  isConfirmOpen.value = false
  serviceToDelete.value = null
}

const openServiceForm = () => {
  selectedService.value = null  
  isServiceFormOpen.value = true
}

const closeServiceForm = () => {
  isServiceFormOpen.value = false
}

const createService = (payload) => {
  closeServiceForm()
  useServiceStore.createService(payload)
  $q.notify({ type: 'positive', message: 'Service created successfully!' })
}

onMounted(() => {
  serviceStore.fetchServices()
})
</script>