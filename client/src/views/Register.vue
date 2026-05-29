<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card :style="$q.screen.gt.sm ? 'width: 400px' : 'width: 90%'" class="q-pa-md shadow-2">
      <q-card-section class="text-center">
        <div class="text-h5 q-mt-sm q-mb-xs">Register</div>
        <div class="text-caption text-grey-7">Create your account</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <q-input
            filled
            v-model="form.name"
            label="Full Name"
            lazy-rules
            :rules="[val => val && val.length > 0 || 'Name is required']"
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            filled
            v-model="form.email"
            label="Email"
            type="email"
            lazy-rules
            :rules="[val => val && val.length > 0 || 'Email is required']"
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
            :rules="[val => val && val.length > 0 || 'Password is required']"
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

          <q-input
            filled
            v-model="form.confirmPassword"
            label="Confirm Password"
            :type="showPassword ? 'text' : 'password'"
            lazy-rules
            :rules="[
              val => val && val.length > 0 || 'Please confirm your password',
              val => val === form.password || 'Passwords do not match'
            ]"
          >
            <template v-slot:prepend>
              <q-icon name="lock_reset" />
            </template>
          </q-input>

          <div>
            <q-btn
              label="Register"
              type="submit"
              color="primary"
              class="full-width"
              :loading="loading"
            />
          </div>
        </q-form>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <q-btn flat no-caps label="Already have an account? Login" color="primary" size="sm" to="/login" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const loading = ref(false)
const showPassword = ref(false)

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const onSubmit = () => {
  loading.value = true
  // Simulate API call
  setTimeout(() => {
    loading.value = false
    $q.notify({
      color: 'green-4',
      message: 'Account created successfully'
    })
  }, 1500)
}
</script>