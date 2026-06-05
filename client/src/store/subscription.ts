import { defineStore } from "pinia";
import httpClient from "../plugins/interceptor";
import type { AxiosError } from "axios";

// 1. Interfaces mirroring your Django Subscription model responses
export interface SubscriptionItem {
  id: number;
  user: number;
  service: number; // Foreign key ID of the associated service
  plan_name: string | null;
  status: "ACTIVE" | "PAUSED" | "CANCELED" | "EXPIRED";
  cost: number;
  billing_cycle: "MONTHLY" | "YEARLY";
  next_billing_date: string; // YYYY-MM-DD from backend
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedSubscriptionResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: SubscriptionItem[];
}

// Interface for creating or updating a subscription (payload types)
export interface SubscriptionPayload {
  service: number;
  plan_name?: string;
  status?: string;
  cost: number;
  billing_cycle: string;
  next_billing_date: string; // Expects YYYY-MM-DD
  notes?: string;
}

interface SubscriptionState {
  subscriptions: SubscriptionItem[];
  pagination: {
    count: number;
    next: string | null;
    previous: string | null;
  };
  currentSubscription: SubscriptionItem | null;
  loading: boolean;
  error: string | null;
}

export const useSubscriptionStore = defineStore("subscriptions", {
  state: (): SubscriptionState => ({
    subscriptions: [],
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
    currentSubscription: null,
    loading: false,
    error: null,
  }),

  getters: {
    allSubscriptions(): SubscriptionItem[] {
      return this.subscriptions;
    },
    isLoading(): boolean {
      return this.loading;
    },
    getSubscriptionError(): string | null {
      return this.error;
    }
  },

  actions: {
    // READ (Fetch all / paginated subscriptions for the logged-in user)
    async fetchSubscriptions(pageUrl: string = "subscriptions") {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.get<PaginatedSubscriptionResponse>(pageUrl);
        if (response.data) {
          this.subscriptions = response.data.results;
          this.pagination = {
            count: response.data.count,
            next: response.data.next,
            previous: response.data.previous,
          };
        }
      } catch (error) {
        this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // Centralized internal error handling mimicking your Auth structure
    handleError(error: any): string {
      const err = error as AxiosError<{ message?: string }>;
      let message = "An error occurred with subscriptions API!";
      if (err.response && err.response.data && err.response.data.message) {
        message = err.response.data.message;
      }
      this.error = message;
      console.error(message, error);
      return message;
    },

    // READ (Fetch a single subscription's full details by ID)
    async fetchSubscriptionById(id: number | string) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.get<SubscriptionItem>(`subscriptions/${id}/`);
        if (response.data) {
          this.currentSubscription = response.data;
        }
        return response.data;
      } catch (error) {
        this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // CREATE (Add a new subscription tracker record)
    async createSubscription(subscriptionData: SubscriptionPayload) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.post<SubscriptionItem>("subscriptions", subscriptionData);
        if (response.data) {
          // Push new active subscription tracking node straight to the front of the list
          this.subscriptions.unshift(response.data);
          this.pagination.count++;
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // UPDATE (Modify plans, cycles, or pricing fields)
    async updateSubscription(id: number, subscriptionData: Partial<SubscriptionPayload>) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.put<SubscriptionItem>(`subscriptions/${id}/`, subscriptionData);
        if (response.data) {
          // Synchronize local UI state mapping instantly without forcing an aggressive refetch
          const index = this.subscriptions.findIndex((item) => item.id === id);
          if (index !== -1) {
            this.subscriptions[index] = response.data;
          }
          if (this.currentSubscription?.id === id) {
            this.currentSubscription = response.data;
          }
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // DELETE (Stop tracking a subscription)
    async deleteSubscription(id: number) {
      this.loading = true;
      this.error = null;
      try {
        await httpClient.delete(`subscriptions/${id}/`);
        // Remove item matching the target ID from memory
        this.subscriptions = this.subscriptions.filter((item) => item.id !== id);
        this.pagination.count--;
      } catch (error) {
        this.handleError(error);
      } finally {
        this.loading = false;
      }
    },  
},
});