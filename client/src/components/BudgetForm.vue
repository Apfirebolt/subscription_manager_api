<template>
  <q-card
    :style="$q.screen.gt.sm ? 'width: 500px' : 'width: 95%'"
    class="q-pa-md shadow-2 flat no-border-radius-on-dialog"
  >
    <q-card-section class="text-center q-pb-none">
      <div class="text-h5 q-mt-sm q-mb-xs">
        {{ budget ? "Modify Budget Settings" : "Configure Target Budget" }}
      </div>
      <div class="text-caption text-grey-7">
        {{
          budget
            ? "Adjust your financial limits and distribution tier below"
            : "Establish a spending ceiling to regulate subscription allocations"
        }}
      </div>
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" class="q-gutter-y-md q-ma-sm">
        
        <q-input
          filled
          v-model.number="form.amount"
          label="Budget Limit Amount *"
          type="number"
          step="0.01"
          prefix="$"
          lazy-rules
          :rules="[
            (val) => val !== null && val !== '' || 'Amount is required',
            (val) => val > 0 || 'Budget limit must be greater than 0',
          ]"
        >
          <template v-slot:prepend>
            <q-icon name="attach_money" />
          </template>
        </q-input>

        <q-select
          filled
          v-model="form.duration"
          label="Billing Cycle Duration *"
          :options="durationOptions"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Please select a tracking cycle duration']"
        >
          <template v-slot:prepend>
            <q-icon name="date_range" />
          </template>
        </q-select>

        <q-input
          filled
          v-model="form.description"
          label="Notes / Description"
          type="textarea"
          placeholder="e.g., General allocation pool for family streaming accounts and SaaS keys."
          autogrow
        >
          <template v-slot:prepend>
            <q-icon name="description" />
          </template>
        </q-input>

        <div class="row justify-end q-gutter-x-sm q-pt-md">
          <q-btn
            label="Cancel"
            type="button"
            color="grey-7"
            flat
            v-close-popup
            @click="handleCancel"
          />
          <q-btn
            :label="budget ? 'Update Budget' : 'Establish Budget'"
            type="submit"
            color="primary"
            :loading="budgetStore.isLoading"
          />
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useBudgetStore } from "../store/budget";

// Define TypeScript interfaces matching our Backend model setup
interface BudgetPayload {
  id?: number;
  amount: number | string;
  duration: string;
  description: string;
}

const props = defineProps({
  budget: {
    type: Object as () => BudgetPayload | null,
    default: null,
  },
});

const emit = defineEmits(["close"]);
const router = useRouter();
const budgetStore = useBudgetStore();

// Form reactive payload tracking
const form = reactive<BudgetPayload>({
  amount: "",
  duration: "MONTHLY", // Matches default backend choice
  description: "",
});

// Dropdown options matching the Django TextChoices model enum exactly
const durationOptions = [
  { label: "Monthly", value: "MONTHLY" },
  { label: "Quarterly", value: "QUARTERLY" },
  { label: "Semi-Annual", value: "SEMI_ANNUAL" },
  { label: "Yearly", value: "YEARLY" },
];

onMounted(() => {
  // Check if an existing budget was passed for update context mutations
  if (props.budget) {
    Object.assign(form, props.budget);
  }
});

const onSubmit = async () => {
  try {
    if (props.budget?.id) {
      // Execute UPDATE workflow against /api/budget/:id/
      await budgetStore.updateBudget(props.budget.id, { ...form });
    } else {
      // Execute CREATE workflow against base /api/budget/
      await budgetStore.createBudget({ ...form });
    }
    
    // Close the dialogue popup window instantly upon success resolver
    emit("close");
  } catch (error) {
    console.error("Failed to commit budget adjustments:", error);
  }
};

const handleCancel = (): void => {
  emit("close");
};
</script>

<style scoped>
/* Removes unnecessary margins when injected straight inside a dialog envelope wrapper */
.no-border-radius-on-dialog {
  margin: 0 !important;
  box-shadow: none !important;
}
</style>