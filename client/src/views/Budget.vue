<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Hello, {{ authData?.userData?.username || 'User' }}!</div>

    <div class="text-body1 q-mb-md">
      Welcome to your financial command center. Monitor your spending limits and track your subscription allocations across specific periods.
    </div>

    <div v-if="budgetStore.isLoading" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="40px" />
    </div>

    <div v-else class="row q-col-gutter-md">
      <div v-if="currentBudget" class="col-12 col-md-6 col-lg-4">
        <q-card class="my-card border-accent shadow-2">
          <q-card-section class="bg-primary text-white q-pa-md">
            <div class="row items-center justify-between">
              <div>
                <div class="text-overline text-grey-4">Active Subscription Budget</div>
                <div class="text-h3 text-weight-bold">${{ currentBudget.amount }}</div>
              </div>
              <q-icon name="account_balance_wallet" size="44px" class="opacity-80" />
            </div>
          </q-card-section>

          <q-card-section class="q-pa-md">
            <div class="row items-center q-mb-sm">
              <q-badge color="secondary" class="q-py-xs q-px-sm text-subtitle2 text-uppercase">
                {{ currentBudget.duration }} Tracker
              </q-badge>
            </div>
            
            <div v-if="currentBudget.description" class="text-body1 text-grey-9 q-mt-sm">
              {{ currentBudget.description }}
            </div>
            <div v-else class="text-body2 text-grey-5 italic q-mt-sm">
              No additional description added for this allocation tier.
            </div>
          </q-card-section>

          <q-separator inset />

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat color="primary" icon="edit" label="Modify Limit" @click="editBudget(currentBudget)" />
            <q-btn flat color="negative" icon="delete" label="Remove" @click="deleteBudget(currentBudget.id)" />
          </q-card-actions>
        </q-card>
      </div>

      <div v-else class="col-12 col-md-6 col-lg-4">
        <q-card class="my-card text-center q-pa-lg shadow-1 bg-grey-1" style="border: 2px dashed #ccc;">
          <q-card-section>
            <q-icon name="monetization_on" size="64px" color="grey-5" />
            <div class="text-h6 text-grey-8 q-mt-md">No Budget Configured</div>
            <div class="text-body2 text-grey-6 q-mt-sm">
              You haven't established a spending ceiling yet. Setting up a threshold helps keep track of your recurring subscriptions.
            </div>
          </q-card-section>
          <q-card-actions class="justify-center">
            <q-btn color="primary" icon="add" label="Set Up Budget" @click="openBudgetForm" />
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="isBudgetFormOpen" persistent>
      <q-card style="min-width: 350px; max-width: 500px; width: 100%;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ selectedBudget ? "Update Budget Settings" : "Configure Target Budget" }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup @click="closeBudgetForm" />
        </q-card-section>

        <q-card-section class="q-pa-none">
          <BudgetForm @close="closeBudgetForm" :budget="selectedBudget" />
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-page-sticky v-if="!currentBudget && !budgetStore.isLoading" position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="openBudgetForm">
        <q-tooltip anchor="center left" self="center right">Create Budget</q-tooltip>
      </q-btn>
    </q-page-sticky>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import BudgetForm from '../components/BudgetForm.vue' // Ensure this component is renamed/updated
import { useAuth } from '../store/auth'
import { useBudgetStore } from '../store/budget' // Pinia store tracking single user budget

const authStore = useAuth()
const authData = authStore.authData
const isBudgetFormOpen = ref(false)
const selectedBudget = ref(null)
const budgetStore = useBudgetStore()

// Access the reactive single budget structure via store computed properties
const currentBudget = computed(() => budgetStore.budget) 

const editBudget = (budget: any) => {
  selectedBudget.value = budget
  isBudgetFormOpen.value = true
}

const deleteBudget = (id: number) => {
  budgetStore.deleteBudget(id)
}

const openBudgetForm = () => {
  selectedBudget.value = null  
  isBudgetFormOpen.value = true
}

const closeBudgetForm = () => {
  isBudgetFormOpen.value = false
}

onMounted(() => {
  budgetStore.fetchBudget()
})
</script>

<style scoped>
.opacity-80 {
  opacity: 0.8;
}
</style>