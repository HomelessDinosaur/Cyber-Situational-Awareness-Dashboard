import { FC, useEffect, useState } from "react";
import { ResponsiveChoropleth } from "@nivo/geo";
import { useLocations } from "../../lib/hooks/useLocations";
import countries from "../../lib/world_countries.json";
import Tooltip from "../shared/Tooltip";
import { DataMode } from "../../lib/types";

interface Props {
  mode?: DataMode;
}

const GeoMap: FC<Props> = ({ mode = "realtime" }) => {
  const { data, isLoading } = useLocations(mode);

  const locationData =
    data && data.length > 0
      ? Object.entries(
          data
            .map((d) => d.country)
            .reduce((prev, curr) => {
              prev[curr] = prev[curr] ? prev[curr] + 1 : 1;
              return prev;
            }, {} as Record<string, number>)
        ).map(([k, v]) => ({ id: k, value: v }))
      : [];

  return (
    <>
      <div className="flex justify-between items-center">
        <p className="text-xl pb-4">IP Connections by Country</p>
        <Tooltip content="This visualisation indicates the location of IP connections on the network by country." />
      </div>
      {!isLoading && data && (
        <ResponsiveChoropleth
          data={locationData}
          features={countries.features}
          margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
          colors="nivo"
          domain={[0, 1000000]}
          unknownColor="#666666"
          label="properties.name"
          valueFormat=".2s"
          projectionTranslation={[0.5, 0.5]}
          projectionRotation={[0, 0, 0]}
          enableGraticule={true}
          graticuleLineColor="#dddddd"
          borderWidth={0.5}
          borderColor="#152538"
          legends={[
            {
              anchor: "bottom-left",
              direction: "column",
              justify: true,
              translateX: 20,
              translateY: -100,
              itemsSpacing: 0,
              itemWidth: 94,
              itemHeight: 18,
              itemDirection: "left-to-right",
              itemTextColor: "#444444",
              itemOpacity: 0.85,
              symbolSize: 18,
              effects: [
                {
                  on: "hover",
                  style: {
                    itemTextColor: "#000000",
                    itemOpacity: 1,
                  },
                },
              ],
            },
          ]}
        />
      )}
    </>
  );
};

export default GeoMap;
