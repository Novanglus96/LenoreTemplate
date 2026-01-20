// useBackendReady.js
import { ref, onMounted } from "vue";
import axios from "axios";
import { useApiKey } from "./useApiKey";

const apiKey = useApiKey();

const backendReady = ref(false);

const apiClient = axios.create({
  baseURL: "/api/v1",
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
  },
});

export function useBackendReady() {
  onMounted(async () => {
    while (!backendReady.value) {
      try {
        const res = await apiClient.get("/options/health/");

        if (res.status === 200) {
          backendReady.value = true;
        }
      } catch (err) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log(err);
      }
    }
  });

  return { backendReady };
}
