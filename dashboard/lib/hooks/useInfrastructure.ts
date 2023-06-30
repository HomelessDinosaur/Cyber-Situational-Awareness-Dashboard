import useSWR from "swr";
import { DataMode, Infrastructure } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useInfrastructure = (mode: DataMode) => {
  const { data, error } = useSWR<Infrastructure[]>(
    `/api/infrastructure?mode=${mode}`,
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
