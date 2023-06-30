import type { NextApiRequest, NextApiResponse } from "next";
import Database from "../../../lib/database";
import { DataMode } from "../../../lib/types";

export const getNetworkObservables = async (
  req: NextApiRequest,
  res: NextApiResponse
) => {
  const { type, mode } = req.query;
  if (req.method === "GET") {
    try {
      const db = await Database.getClient(mode as DataMode);

      const observables = await db
        .collection(type as string)
        .find()
        .toArray();

      return res.status(200).send(observables);
    } catch (err) {
      return res.status(500).send(err);
    }
  }
};

export default getNetworkObservables;
