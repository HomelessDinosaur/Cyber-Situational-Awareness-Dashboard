import { FC } from "react";
import { InputNode, ResponsiveNetwork } from "@nivo/network";
import { useNetworkData } from "../../lib/hooks/useNetworkData";
import Tooltip from "../shared/Tooltip";
import { DataMode } from "../../lib/types";

const isLocal = (n: { id: string }) => n.id.startsWith("192.168");

const nodeSize = (n: { id: string }) => (isLocal(n) ? 24 : 15);

interface Props {
  mode?: DataMode;
}

const NetworkGraph: FC<Props> = ({ mode = "realtime" }) => {
  const { data, isLoading } = useNetworkData(mode);

  return (
    <>
      <div className="flex justify-between items-center">
        <p className="text-xl pb-4">Devices on Network</p>
        <Tooltip content="This visualisation represents the devices and sub-networks present within a network. The connections between them are also indicated." />
      </div>
      {!isLoading && data.nodes && (
        <ResponsiveNetwork
          data={data}
          margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
          linkDistance={100}
          centeringStrength={1}
          repulsivity={50}
          nodeSize={(n) => nodeSize(n)}
          activeNodeSize={(n) => 1.5 * nodeSize(n)}
          nodeColor={(n: InputNode) => (isLocal(n) ? "#86dacc" : "#f69889")}
          nodeBorderWidth={1}
          nodeBorderColor={{
            from: "color",
            modifiers: [["darker", 0.8]],
          }}
          linkBlendMode="multiply"
          motionConfig="gentle"
        />
      )}
    </>
  );
};

export default NetworkGraph;
