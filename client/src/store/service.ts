import { defineStore } from "pinia";
import httpClient from "../plugins/interceptor";
import type { AxiosError } from "axios";
import { useAuth } from "./auth";

// 1. Define interfaces for the Service Data based on your Django API response
export interface ServiceItem {
  id: number;
  name: string;
  logo_url: string;
  description: string;
}

export interface PaginatedServiceResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ServiceItem[];
}

// Interface for creating or updating a service (payload types)
export interface ServicePayload {
  name: string;
  logo_url: string;
  description: string;
}

interface ServiceState {
  services: ServiceItem[];
  pagination: {
    count: number;
    next: string | null;
    previous: string | null;
  };
  currentService: ServiceItem | null;
  loading: boolean;
  error: string | null;
}

export const useServiceStore = defineStore("services", {
  state: (): ServiceState => ({
    services: [],
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
    currentService: null,
    loading: false,
    error: null,
  }),

  getters: {
    allServices(): ServiceItem[] {
      return this.services;
    },
    isLoading(): boolean {
      return this.loading;
    },
    getServiceError(): string | null {
      return this.error;
    }
  },

  actions: {
    // READ (Fetch all / paginated services)
    async fetchServices(pageUrl: string = "services") {
      this.loading = true;
      this.error = null;
      try {
        // Keeps track of the base URL or paginated endpoints handed down by Django
        const response = await httpClient.get<PaginatedServiceResponse>(pageUrl);
        if (response.data) {
          this.services = response.data.results;
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

    // READ (Fetch a single service by ID)
    async fetchServiceById(id: number | string) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.get<ServiceItem>(`services/${id}/`);
        if (response.data) {
          this.currentService = response.data;
        }
      } catch (error) {
        this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // CREATE (Add a new service)
    async createService(serviceData: ServicePayload) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.post<ServiceItem>("services", serviceData);
        if (response.data) {
          // Add the newly created item to the local list state
          this.services.unshift(response.data);
          this.pagination.count++;
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // UPDATE (Modify an existing service)
    async updateService(id: number, serviceData: Partial<ServicePayload>) {
      this.loading = true;
      this.error = null;
      try {
        const response = await httpClient.put<ServiceItem>(`services/${id}/`, serviceData);
        if (response.data) {
          // Update the item in the local state array
          const index = this.services.findIndex((item) => item.id === id);
          if (index !== -1) {
            this.services[index] = response.data;
          }
          if (this.currentService?.id === id) {
            this.currentService = response.data;
          }
        }
        return response.data;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // DELETE (Remove a service)
    async deleteService(id: number) {
      this.loading = true;
      this.error = null;
      try {
        await httpClient.delete(`services/${id}/`);
        // Remove from local list state
        this.services = this.services.filter((item) => item.id !== id);
        this.pagination.count--;
      } catch (error) {
        return this.handleError(error);
      } finally {
        this.loading = false;
      }
    },

    // Centralized internal error handling mimicking your Auth structure
    handleError(error: any): string {
      const err = error as AxiosError<{ message?: string }>;
      let message = "An error occurred with services API!";
      if (err.response && err.response.data && err.response.data.message) {
        message = err.response.data.message;
      }
      this.error = message;
      console.error(message, error);
      return message;
    },

    // Clean local state if needed
    clearCurrentService() {
      this.currentService = null;
    }
  },
});