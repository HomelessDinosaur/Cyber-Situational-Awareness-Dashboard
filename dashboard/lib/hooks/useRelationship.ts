import useSWR from "swr";
import { DataMode, StixObject } from "../types";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export const useRelatipnship = (object: StixObject, mode: DataMode) => {
  const { data, error } = useSWR<StixObject[]>(
    `/api/relationship/${object.id}?mode=${mode}`,
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
