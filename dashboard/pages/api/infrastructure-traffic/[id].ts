import type { NextApiRequest, NextApiResponse } from "next";
import Database from "../../../lib/database";
import {
  DataMode,
  Ipv4Address,
  NetworkTraffic,
  Relationship,
} from "../../../lib/types";

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

      const targetRef = await db
        .collection("ipv4-addr")
        .findOne({ id: observable.target_ref });

      if (!targetRef) {
        return res
          .status(404)
          .send({ message: "target reference with id could not be found" });
      }

      const traffic = await db
        .collection<NetworkTraffic>("network-traffic")
        .find({ src_ref: targetRef.id })
        .toArray();

      return res.status(200).send({
        ip: targetRef.value,
        traffic: traffic,
      });
    } catch (err) {
      return res.status(500).send(err);
    }
  }
};

export default getNetworkObservables;
