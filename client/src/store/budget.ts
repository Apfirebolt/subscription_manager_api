import { defineStore } from "pinia";
import httpClient from "../plugins/interceptor";
import type { AxiosError } from "axios";

// 1. Define core interfaces mirroring your Django Budget model
export interface BudgetItem {
  id: number;
  user: number; // User ID association reference
  amount: number;
  duration: "MONTHLY" | "QUARTERLY" | "SEMI_ANNUAL" | "YEARLY";
  description: string;
  created_at: string;
  updated_at: string;
}

// Payload schema for dispatching creation and update actions
export interface BudgetPayload {
  amount: number;
  duration: string;
  description: string;
}

interface BudgetState {
  budget: BudgetItem | null; // Single budget tracking point
  loading: boolean;
  error: string | null;
}

export const useBudgetStore = defineStore("budget", {
  state: (): BudgetState => ({
    budget: null,
    loading: false,
    error: null,
  }),

  getters: {
    currentBudget(): BudgetItem | null {
      return this.budget;
    },
    isLoading(): boolean {
      return this.loading;
    },
    getBudgetError(): string | null {
      return this.error;
    }
  },

  actions: {
    // READ (Fetch the user's single budget record)
    async fetchBudget() {
      this.loading = true;
      this.error = null;
      try {
        // Points to your single-resource profile budget retrieval view
        const response = await httpClient.get<BudgetItem>("budgets");
        if (response.data) {
          this.budget = response.data;
        }
      } catch (error) {
        // If your backend cleanly throws a 404 when no budget exists yet,
        // we swallow it quietly so the UI can confidently render the Empty State.
        const err = error as AxiosError;
        if (err.response?.status === 404) {
          this.budget = null;
        } else {
          this.handleError(error);
        }
      } finally {
        this.loading = false;
      }
    },

    // CREATE (Establish an initial budget boundary allocation)
    async createBudget(budgetData: BudgetPayload) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.post<BudgetItem>("budgets", budgetData);
        if (response.data) {
          this.budget = response.data;
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // UPDATE (Modify limits or duration cycles dynamically)
    async updateBudget(id: number, budgetData: Partial<BudgetPayload>) {
      this.loading = true;
      this.error = null;
      try {
        // Hit the detail route updates endpoint pattern: budget/:id/
        const response = await httpClient.put<BudgetItem>(`budget/${id}/`, budgetData);
        if (response.data) {
          this.budget = response.data;
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // DELETE (Remove the spending profile restriction limits entirely)
    async deleteBudget(id: number) {
      this.loading = true;
      this.error = null;
      try {
        await httpClient.delete(`budget/${id}/`);
        // Reset the single object tracker state back to null
        this.budget = null;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // Centralized core interceptor layout error tracking parser
    handleError(error: any): string {
      const err = error as AxiosError<{ message?: string }>;
      let message = "An error occurred with the budgets engine pipeline!";
      if (err.response && err.response.data && err.response.data.message) {
        message = err.response.data.message;
      }
      this.error = message;
      console.error(message, error);
      return message;
    },

    // Resets store state values locally during a user logout sequence
    clearBudgetStore() {
      this.budget = null;
      this.error = null;
    }
  },
});