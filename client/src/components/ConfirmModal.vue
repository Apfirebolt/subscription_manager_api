<template>
  <q-card
    :style="$q.screen.gt.sm ? 'width: 450px' : 'width: 95%'"
    class="q-pa-md q-ma-md shadow-2"
  >
    <q-card-section class="text-center">
      <q-avatar 
        :icon="icon" 
        :color="iconColor + '-1'" 
        :text-color="iconColor" 
        size="56px" 
        class="q-mb-sm"
      />
      <div class="text-h5 q-mt-sm q-mb-xs">
        {{ title }}
      </div>
      <div class="text-body2 text-grey-7 q-mt-sm">
        {{ message }}
      </div>
    </q-card-section>

    <q-card-section v-if="$slots.default">
      <slot></slot>
    </q-card-section>

    <q-card-actions align="right" class="q-gutter-x-sm q-pt-md">
      <q-btn
        :label="cancelLabel"
        type="button"
        color="grey-7"
        flat
        v-close-popup
        @click="onCancel"
      />
      <q-btn
        :label="okLabel"
        type="button"
        :color="okColor"
        :loading="loading"
        @click="onConfirm"
      />
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, withDefaults } from 'vue';

// Define explicit props with types and default fallbacks
interface Props {
  title?: string;
  message?: string;
  okLabel?: string;
  cancelLabel?: string;
  okColor?: string;
  icon?: string;
  iconColor?: string;
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Confirm Action",
  message: "Are you sure you want to proceed with this action?",
  okLabel: "OK",
  cancelLabel: "Cancel",
  okColor: "primary",
  icon: "help_outline",
  iconColor: "primary",
  loading: false,
});

// Define Emits for parent communication
const emit = defineEmits<{
  (e: "confirm"): void;
  (e: "cancel"): void;
}>();

const onConfirm = () => {
  emit("confirm");
};

const onCancel = () => {
  emit("cancel");
};
</script>