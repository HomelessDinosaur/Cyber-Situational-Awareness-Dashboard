import useSWR from "swr";
import { DataMode } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useNetworkData = (mode: DataMode) => {
  const { data, error } = useSWR(
    `/api/infrastructure-traffic/network?mode=${mode}`,
    fetcher
  );

  // render data
  const isLoading = !data && !error;

  return {
    data,
    isLoading,
    error,
  };
};
