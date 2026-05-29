<template>
  <q-page class="q-pa-md">
    <div class="row q-col-gutter-md">
      <!-- Stats Cards -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-primary text-white">
          <q-card-section>
            <div class="text-h6">Total Subscriptions</div>
            <div class="text-h4">12</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-teal text-white">
          <q-card-section>
            <div class="text-h6">Monthly Spend</div>
            <div class="text-h4">$142.50</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-orange text-white">
          <q-card-section>
            <div class="text-h6">Upcoming Renewals</div>
            <div class="text-h4">3</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="bg-red text-white">
          <q-card-section>
            <div class="text-h6">Expired</div>
            <div class="text-h4">1</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Recent Subscriptions Table -->
      <div class="col-12">
        <q-table
          title="Active Subscriptions"
          :rows="rows"
          :columns="columns"
          row-key="name"
          flat
          bordered
        >
          <template v-slot:body-cell-status="props">
            <q-td :props="props">
              <q-chip
                :color="props.value === 'Active' ? 'green' : 'red'"
                text-color="white"
                dense
              >
                {{ props.value }}
              </q-chip>
            </q-td>
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn flat round color="grey" icon="edit" size="sm" />
              <q-btn flat round color="negative" icon="delete" size="sm" />
            </q-td>
          </template>
        </q-table>
      </div>
    </div>

    <!-- Floating Action Button -->
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="addNewSubscription">
        <q-tooltip>Add Subscription</q-tooltip>
      </q-btn>
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const columns = [
  { name: 'name', align: 'left', label: 'Service', field: 'name', sortable: true },
  { name: 'category', align: 'left', label: 'Category', field: 'category', sortable: true },
  { name: 'price', align: 'center', label: 'Price ($)', field: 'price', sortable: true },
  { name: 'nextBilling', align: 'left', label: 'Next Billing', field: 'nextBilling', sortable: true },
  { name: 'status', align: 'center', label: 'Status', field: 'status' },
  { name: 'actions', align: 'right', label: 'Actions', field: 'actions' }
]

const rows = ref([
  {
    name: 'Netflix',
    category: 'Entertainment',
    price: 15.99,
    nextBilling: '2023-11-15',
    status: 'Active'
  },
  {
    name: 'Spotify',
    category: 'Music',
    price: 9.99,
    nextBilling: '2023-11-20',
    status: 'Active'
  },
  {
    name: 'Adobe CC',
    category: 'Software',
    price: 52.99,
    nextBilling: '2023-11-01',
    status: 'Active'
  }
])

const addNewSubscription = () => {
  $q.notify({
    message: 'Add new subscription clicked',
    color: 'info'
  })
}
</script>