import { defineStore } from "pinia";
import Cookie from "js-cookie";
import router from "../routes";
import httpClient from "../plugins/interceptor";
import type { AxiosError } from "axios";

interface AuthData {
  token: string;
  user?: any;
  [key: string]: any;
}

interface AuthState {
  authData: AuthData | null;
  loading: boolean;
}

export const useAuth = defineStore("auth", {
  state: (): AuthState => ({
    authData: Cookie.get("user") ? JSON.parse(Cookie.get("user")!) : null,
    loading: false,
  }),

  getters: {
    getAuthData(): AuthData | null {
      return this.authData;
    },
    isLoading(): boolean {
      return this.loading;
    },
  },

  actions: {
    async loginAction(loginData: any) {
      try {
        const response = await httpClient.post("login", loginData);
        if (response.data) {
          this.authData = response.data;
          // set the data in cookie
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          router.push("/dashboard");
        }
      } catch (error) {
        const err = error as AxiosError<{ message?: string }>;
        let message = "An error occurred!";
        if (err.response && err.response.data && err.response.data.message) {
          message = err.response.data.message;
        }
        return error;
      }
    },

    async registerAction(registerData: any) {
      try {
        const response = await httpClient.post("register", registerData);
        if (response.data && response.status === 201) {
          this.authData = response.data;
          Cookie.set("user", JSON.stringify(response.data), { expires: 30 });
          router.push("/dashboard");
        }
      } catch (error) {
        const err = error as AxiosError<{ message?: string }>;
        let message = "An error occurred!";
        if (err.response && err.response.data && err.response.data.message) {
          message = err.response.data.message;
        }
        console.log(error);
        return error;
      }
    },

    async getProfileData() {
      try {
        // get the token from the cookie
        const cookieData = Cookie.get("user");
        if (!cookieData) return;
        
        const authData: AuthData = JSON.parse(cookieData);
        const headers = {
          Authorization: `Bearer ${authData.token}`,
        };
        const response = await httpClient.get("profile", { headers: headers as any });
        console.log(response.data);
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    logout() {
      this.authData = null;
      Cookie.remove("user");
      router.push("/login");
    },

    resetAuth() {
      this.authData = null;
    },
  },
});
