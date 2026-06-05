<template>
  <q-card
    :style="$q.screen.gt.sm ? 'width: 500px' : 'width: 95%'"
    class="q-pa-md q-ma-md shadow-2"
  >
    <q-card-section class="text-center">
      <div class="text-h5 q-mt-sm q-mb-xs">
        {{ service ? "Edit Service" : "Create New Service" }}
      </div>
      <div class="text-caption text-grey-7">
        {{
          service
            ? "Modify service details below"
            : "Fill out the fields to register a new application service"
        }}
      </div>
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" class="q-gutter-y-md q-ma-sm">
        <q-input
          filled
          v-model="form.name"
          label="Service Name *"
          type="text"
          lazy-rules
          :rules="[
            (val) =>
              (val && val.trim().length > 0) || 'Service name is required',
          ]"
        >
          <template v-slot:prepend>
            <q-icon name="apps" />
          </template>
        </q-input>

        <q-input
          filled
          v-model="form.logo_url"
          label="Logo URL *"
          type="url"
          placeholder="https://example.com/logo.png"
          lazy-rules
          :rules="[
            (val) => (val && val.trim().length > 0) || 'Logo URL is required',
            (val) => isValidUrl(val) || 'Please enter a valid URL',
          ]"
        >
          <template v-slot:prepend>
            <q-icon name="link" />
          </template>
        </q-input>

        <div
          v-if="isValidUrl(form.logo_url)"
          class="flex justify-center q-my-sm"
        >
          <q-avatar
            square
            size="80px"
            class="bg-grey-3 q-pa-xs rounded-borders shadow-1"
          >
            <img
              :src="form.logo_url"
              alt="Logo preview"
              @error="onImageError"
            />
          </q-avatar>
        </div>

        <q-input
          filled
          v-model="form.description"
          label="Description *"
          type="textarea"
          autogrow
          lazy-rules
          :rules="[
            (val) =>
              (val && val.trim().length > 0) || 'Description is required',
          ]"
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
            @click="goBack"
          />
          <q-btn
            :label="service ? 'Update Service' : 'Create Service'"
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
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Notify } from "quasar";
import { useServiceStore, type ServicePayload } from "../store/service";

// FIX: Assigned defineProps to a 'props' constant so it is accessible in the script block below
const props = defineProps({
  service: {
    type: Object as () => ServicePayload | null,
    default: null,
  },
});

const router = useRouter();
const serviceStore = useServiceStore();

const form = reactive<ServicePayload>({
  name: "",
  logo_url: "",
  description: "",
});

// Sync data if we are in Edit Mode
onMounted(async () => {
  // Now props.service will evaluate perfectly without throwing an error!
  console.log("ServiceForm mounted with service prop:", props.service);
  if (props.service) {
    Object.assign(form, props.service);
  } else {
    const routeId = router.currentRoute.value.params.id;
    if (routeId) {
      const serviceId = parseInt(routeId as string, 10);
      const existingService = await serviceStore.fetchServiceById(serviceId);
      if (existingService) {
        Object.assign(form, existingService);
      } else {
        Notify.create({
          type: "negative",
          message: "Service not found. Redirecting to dashboard.",
        });
        goBack();
      }
    }
  }
});

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

// Fallback if the logo url is broken
const onImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = "https://cdn.quasar.dev/logo-v2/svg/logo.svg";
};

// Navigation fallback
const goBack = (): void => {
  serviceStore.clearCurrentService();
  router.push("/dashboard");
};

// Dummy onSubmit handler to ensure compilation succeeds if missing from your copy
const onSubmit = () => {
  console.log("Form payload submitted:", form);
};
</script>