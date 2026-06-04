<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Hello, {{ authData?.userData?.username || 'User' }}!</div>

    <div v-if="subscriptionStore.isLoading || serviceStore.isLoading" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="40px" />
    </div>

    <div v-else class="row q-col-gutter-md">
      <div v-if="subscriptions.length === 0" class="col-12 text-center text-grey q-my-xl">
        <q-icon name="layers_clear" size="48px" class="q-mb-sm" />
        <div class="text-h6">No subscriptions tracked yet.</div>
        <div class="text-body2">Click the plus icon down right to get started.</div>
      </div>

      <div v-else v-for="subscription in subscriptions" :key="subscription.id" class="col-12 col-md-6 col-lg-4">
        <q-card class="my-card">
          <q-card-section>
            <div class="text-h6">{{ subscription.service_name }}</div>
            <div class="text-subtitle2 text-grey-7">{{ subscription.subscription_type }}</div>
          </q-card-section>

          <q-card-section>
            <div><strong>Next Billing Date:</strong> {{ subscription.next_billing_date }}</div>
            <div class="q-mt-xs"><strong>Amount:</strong> ${{ subscription.amount }}</div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Edit" color="primary" @click="editSubscription(subscription)" />
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="isSubscriptionFormOpen" persistent>
      <q-card style="min-width: 350px; max-width: 500px; width: 100%;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">New Subscription</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup @click="closeSubscriptionForm" />
        </q-card-section>

        <q-card-section class="q-pa-none">
          <SubscriptionForm @close="closeSubscriptionForm" :subscription="selectedSubscription" />
        </q-card-section>
      </q-card>
    </q-dialog>
    
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="openSubscriptionForm">
        <q-tooltip anchor="center left" self="center right">Track New Subscription</q-tooltip>
      </q-btn>
    </q-page-sticky>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useQuasar } from 'quasar'
import SubscriptionForm from '../components/SubscriptionForm.vue'
import { useAuth } from '../store/auth'
import { useServiceStore } from '../store/service'
import { useSubscriptionStore } from '../store/subscription'

const $q = useQuasar()
const authStore = useAuth()
const serviceStore = useServiceStore()
const subscriptionStore = useSubscriptionStore()

// FIX 4: Ensured reactive references are correctly unwrapped or extracted cleanly depending on store design
const authData = computed(() => authStore.authData)
const isSubscriptionFormOpen = ref(false)
const selectedSubscription = ref<any | null>(null)
const subscriptions = computed(() => subscriptionStore.allSubscriptions || [])

onMounted(() => {
  serviceStore.fetchServices()
  subscriptionStore.fetchSubscriptions()
})

const openSubscriptionForm = () => {
  selectedSubscription.value = null
  isSubscriptionFormOpen.value = true
}

const closeSubscriptionForm = () => {
  isSubscriptionFormOpen.value = false
  selectedSubscription.value = null
}

const editSubscription = (row: any) => {
  // FIX 5: Creating deep clone so form mutations don't alter dashboard cards pre-save
  selectedSubscription.value = JSON.parse(JSON.stringify(row))
  isSubscriptionFormOpen.value = true
}
</script>

<style scoped>
.my-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.my-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
</style>