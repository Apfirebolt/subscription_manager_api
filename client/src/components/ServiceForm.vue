<template>
  <q-card
      :style="$q.screen.gt.sm ? 'width: 500px' : 'width: 95%'"
      class="q-pa-md shadow-2"
    >
      <q-card-section class="text-center">
        <!-- Dynamic title based on mode -->
        <div class="text-h5 q-mt-sm q-mb-xs">
          {{ isEditMode ? "Edit Service" : "Create New Service" }}
        </div>
        <div class="text-caption text-grey-7">
          {{ isEditMode ? "Modify service details below" : "Fill out the fields to register a new application service" }}
        </div>
      </q-card-section>

      <q-card-section>
        <!-- Quasar form utilizing global loading state from store -->
        <q-form @submit="onSubmit" class="q-gutter-y-md">
          
          <!-- Service Name -->
          <q-input
            filled
            v-model="form.name"
            label="Service Name *"
            type="text"
            lazy-rules
            :rules="[(val) => (val && val.trim().length > 0) || 'Service name is required']"
          >
            <template v-slot:prepend>
              <q-icon name="apps" />
            </template>
          </q-input>

          <!-- Logo URL -->
          <q-input
            filled
            v-model="form.logo_url"
            label="Logo URL *"
            type="url"
            placeholder="https://example.com/logo.png"
            lazy-rules
            :rules="[
              (val) => (val && val.trim().length > 0) || 'Logo URL is required',
              (val) => isValidUrl(val) || 'Please enter a valid URL'
            ]"
          >
            <template v-slot:prepend>
              <q-icon name="link" />
            </template>
          </q-input>

          <!-- Image Preview Block (shows up only if URL looks valid) -->
          <div v-if="isValidUrl(form.logo_url)" class="flex justify-center q-my-sm">
            <q-avatar square size="80px" class="bg-grey-3 q-pa-xs rounded-borders shadow-1">
              <img :src="form.logo_url" alt="Logo preview" @error="onImageError" />
            </q-avatar>
          </div>

          <!-- Description -->
          <q-input
            filled
            v-model="form.description"
            label="Description *"
            type="textarea"
            autogrow
            lazy-rules
            :rules="[(val) => (val && val.trim().length > 0) || 'Description is required']"
          >
            <template v-slot:prepend>
              <q-icon name="description" />
            </template>
          </q-input>

          <!-- Action Buttons -->
          <div class="row justify-end q-gutter-x-sm q-pt-md">
            <q-btn
              label="Cancel"
              type="button"
              color="grey-7"
              flat
              v-close-popup
              @click="goBack"
            />
            <q-btn
              :label="isEditMode ? 'Update Service' : 'Create Service'"
              type="submit"
              color="primary"
              :loading="serviceStore.isLoading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Notify } from "quasar";
import { useServiceStore, type ServicePayload } from "../store/service";

const route = useRoute();
const router = useRouter();
const serviceStore = useServiceStore();

// Track if we are editing an item by checking URL params (e.g., /services/:id/edit)
const serviceId = computed(() => {
  const id = route.params.id;
  return id ? Number(id) : null;
});
const isEditMode = computed(() => serviceId.value !== null);

// Strongly typed form payload matching our Pinia store interface
const form = reactive<ServicePayload>({
  name: "",
  logo_url: "",
  description: "",
});

// Sync data if we are in Edit Mode
onMounted(async () => {
  if (isEditMode.value && serviceId.value) {
    await serviceStore.fetchServiceById(serviceId.value);
    
    // If the item exists in the store after fetching, populate the form
    if (serviceStore.currentService) {
      form.name = serviceStore.currentService.name;
      form.logo_url = serviceStore.currentService.logo_url;
      form.description = serviceStore.currentService.description;
    } else {
      Notify.create({
        type: "negative",
        message: "Failed to load service data. Returning to dashboard...",
      });
      goBack();
    }
  }
});

// Form Submission
const onSubmit = async (): Promise<void> => {
  try {
    if (isEditMode.value && serviceId.value) {
      // Handle Update
      await serviceStore.updateService(serviceId.value, form);
      if (!serviceStore.getServiceError) {
        Notify.create({ type: "positive", message: "Service updated successfully!" });
      }
    } else {
      // Handle Create
      await serviceStore.createService(form);
      if (!serviceStore.getServiceError) {
        Notify.create({ type: "positive", message: "Service created successfully!" });
      }
    }
  } catch (error) {
    console.error("Form submission error:", error);
  }
};

// Simple URL validation helper
const isValidUrl = (urlString: string): boolean => {
  if (!urlString) return false;
  try {
    new URL(urlString);
    return true;
  } catch (_) {
    return false;
  }
};

// Fallback if the logo url is broken or blocks hotlinking
const onImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = "https://cdn.quasar.dev/logo-v2/svg/logo.svg"; // Fallback placeholder
};

// Navigation fallback
const goBack = (): void => {
  serviceStore.clearCurrentService(); // Clean state
  router.push("/dashboard");
};
</script>