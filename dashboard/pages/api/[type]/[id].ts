import type { NextApiRequest, NextApiResponse } from "next";
import Database from "../../../lib/database";
import { DataMode } from "../../../lib/types";

export const getNetworkObservables = async (
  req: NextApiRequest,
  res: NextApiResponse
) => {
  const { type, id, mode } = req.query;
  if (req.method === "GET") {
    try {
      const db = await Database.getClient(mode as DataMode);

      const observable = await db.collection(type as string).findOne({ id });

      return res.status(200).send(observable);
    } catch (err) {
      return res.status(500).send(err);
    }
  }
};

export default getNetworkObservables;
