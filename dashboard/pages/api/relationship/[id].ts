import type { NextApiRequest, NextApiResponse } from "next";
import Database from "../../../lib/database";
import { DataMode, Relationship } from "../../../lib/types";

export const getNetworkObservables = async (
  req: NextApiRequest,
  res: NextApiResponse
) => {
  const { id, mode } = req.query;
  if (req.method === "GET") {
    try {
      const db = await Database.getClient(mode as DataMode);

      const observable = await db
        .collection("relationship")
        .findOne<Relationship>({ source_ref: id });

      if (!observable) {
        return res
          .status(404)
          .send({ message: "source reference with id could not be found" });
      }

      const targetType = observable.target_ref.split("--")[0];
      const targetRef = await db
        .collection(targetType)
        .findOne({ id: observable.id });

      if (!targetRef) {
        return res
          .status(404)
          .send({ message: "target reference with id could not be found" });
      }

      return res.status(200).send(targetRef);
    } catch (err) {
      return res.status(500).send(err);
    }
  }
};

export default getNetworkObservables;
