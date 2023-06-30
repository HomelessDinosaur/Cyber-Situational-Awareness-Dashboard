import useSWR from "swr";
import { DataMode, Ipv4Address } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useIpv4Addresses = (mode: DataMode) => {
  const { data, error } = useSWR<Ipv4Address[]>(
    `/api/ipv4-addr?mode=${mode}`,
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
