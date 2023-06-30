import useSWR from "swr";
import { DataMode, Location } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useLocations = (mode: DataMode) => {
  const { data, error } = useSWR<Location[]>(
    `/api/location?mode=${mode}`,
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
