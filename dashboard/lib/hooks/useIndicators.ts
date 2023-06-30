import useSWR from "swr";
import { DataMode, Indicator } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useIndicators = (mode: DataMode) => {
  const { data, error } = useSWR<Indicator[]>(
    `/api/indicator?mode=${mode}`,
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
