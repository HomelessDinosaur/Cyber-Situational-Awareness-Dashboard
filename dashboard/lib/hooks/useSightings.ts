import useSWR from "swr";
import { DataMode, Sighting } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useSightings = (mode: DataMode) => {
  const { data, error } = useSWR<Sighting[]>(
    `/api/sighting?mode=${mode}`,
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
