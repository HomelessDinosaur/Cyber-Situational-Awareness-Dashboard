import useSWR from "swr";
import { DataMode, NetworkTraffic } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useNetworkObservables = (mode: DataMode) => {
  const { data, error } = useSWR<NetworkTraffic[]>(
    `/api/network-traffic?mode=${mode}`,
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
