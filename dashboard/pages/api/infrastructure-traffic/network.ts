import type { NextApiRequest, NextApiResponse } from "next";
import Database from "../../../lib/database";
import {
  DataMode,
  Infrastructure,
  Ipv4Address,
  NetworkTraffic,
  Relationship,
} from "../../../lib/types";

export const getNetworkObservables = async (
  req: NextApiRequest,
  res: NextApiResponse
) => {
  const { mode } = req.query;
  if (req.method === "GET") {
    try {
      const db = await Database.getClient(mode as DataMode);

      const infrastructure = await db
        .collection<Infrastructure>("infrastructure")
        .find()
        .toArray();

      const ipRefs = await db
        .collection("relationship")
        .find({ $or: infrastructure.map((i) => ({ source_ref: i.id })) })
        .toArray();

      const ips = await db
        .collection("ipv4-addr")
        .find<Ipv4Address>({ $or: ipRefs.map((i) => ({ id: i.target_ref })) })
        .toArray();

      const internet = await db
        .collection("ipv4-addr")
        .find<Ipv4Address>({ $nor: ips.map((i) => ({ id: i.id })) })
        .toArray();

      const links = await db
        .collection("network-traffic")
        .find<NetworkTraffic>({})
        .toArray();

      res.send({
        nodes: [
          ...ips.map((i) => ({ id: i.value, color: "red", size: 24 })),
          ...internet.map((i) => ({ id: i.value, color: "blue", size: 15 })),
        ],
        links: links
          .map((link) => ({
            source: [...ips, ...internet].find((i) => i.id === link.src_ref)
              ?.value,
            target: [...ips, ...internet].find((i) => i.id === link.dst_ref)
              ?.value,
          }))
          .filter((l) => l.source && l.target)
          .filter(
            (l, idx, arr) =>
              idx ===
              arr.findIndex(
                (t) => t.source === l.source && t.target === l.target
              )
          ),
      });
    } catch (err) {
      return res.status(500).send(err);
    }
  }
};

export default getNetworkObservables;
