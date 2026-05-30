<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card
      :style="$q.screen.gt.sm ? 'width: 400px' : 'width: 90%'"
      class="q-pa-md shadow-2"
    >
      <q-card-section class="text-center">
        <div class="text-h5 q-mt-sm q-mb-xs">Login</div>
        <div class="text-caption text-grey-7">
          Please enter your credentials
        </div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input
            filled
            v-model="form.email"
            label="Email"
            type="email"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Email is required']"
          >
            <template v-slot:prepend>
              <q-icon name="email" />
            </template>
          </q-input>

          <q-input
            filled
            v-model="form.password"
            label="Password"
            :type="showPassword ? 'text' : 'password'"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Password is required',
            ]"
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
              <q-icon
                :name="showPassword ? 'visibility' : 'visibility_off'"
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </template>
          </q-input>

          <div>
            <q-btn
              label="Login"
              type="submit"
              color="primary"
              class="full-width"
              :loading="loading"
            />
          </div>
        </q-form>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <q-btn
          flat
          no-caps
          label="Forgot password?"
          color="primary"
          size="sm"
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { Notify } from "quasar";
import { useAuth } from "../store/auth";

const authStore = useAuth();
const loading = ref(false);
const showPassword = ref(false);

const form = reactive({
  email: "",
  password: "",
});

const onSubmit = () => {
  loading.value = true;
  // Simulate API call
  setTimeout(async () => {
    try {
      await authStore.loginAction(form);
    } catch (error) {
      console.error("Login failed:", error);
    } finally {
      loading.value = false;
    }
  }, 1000);
};

onMounted(() => {
  // If user is already logged in, redirect to dashboard
  console.log("Checking auth data on mount:", authStore.authData);
  if (authStore.authData){
    // show toast message
    Notify.create({
      type: "positive",
      message: "You are already logged in! Redirecting to dashboard...",
    });
  }
});
</script>
