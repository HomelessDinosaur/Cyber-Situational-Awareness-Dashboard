import { ResponsiveLine, Serie } from "@nivo/line";
import { FC, useEffect, useState } from "react";
import { useInfrastructure } from "../../lib/hooks/useInfrastructure";
import { DataMode, Infrastructure, NetworkTraffic } from "../../lib/types";
import Tooltip from "../shared/Tooltip";

const getLineData = async (
  infrastructure: Infrastructure,
  mode: DataMode
): Promise<Serie> => {
  const { ip, traffic } = (await (
    await fetch(`/api/infrastructure-traffic/${infrastructure.id}?mode=${mode}`)
  ).json()) as { ip: string; traffic: NetworkTraffic[] };

  if (!traffic) {
    return {
      id: ip,
      data: [],
    };
  }

  const sortByTime = traffic
    .map((time) => new Date(time.start))
    .sort((a, b) => a.getTime() - b.getTime());

  const data = [];

  for (let x = 1; x < 24; x++) {
    data.push({
      x,
      y: sortByTime.filter((ip) => ip.getHours() === x).length,
    });
  }

  return {
    id: ip,
    data,
  };
};

const convertToLineData = async (
  infrastructure: Infrastructure[],
  mode: DataMode
): Promise<Serie[]> => {
  if (infrastructure && infrastructure.length > 0) {
    return Promise.all(
      infrastructure.map(async (ip) => await getLineData(ip, mode))
    );
  }
  return [];
};

interface Props {
  mode?: DataMode;
}

const TimeGraph: FC<Props> = ({ mode = "realtime" }) => {
  const { data: infrastructure, isLoading: infraLoading } =
    useInfrastructure(mode);
  const [lineData, setLineData] = useState<Serie[]>([]);

  useEffect(() => {
    const getLineData = async () => {
      if (!infraLoading && infrastructure) {
        const lineData = await convertToLineData(infrastructure, mode);
        setLineData(
          lineData
            .slice(0, [...new Set(lineData.map((v) => v.id))].length)
            .reverse()
        );
      }
    };

    getLineData();
  }, [infraLoading]);

  return (
    <>
      <div className="flex justify-between items-center">
        <p className="text-xl pb-4">Network Traffic over last day</p>
        <Tooltip content="This visualisation indicates the volume of network traffic across a 24-hour period of time." />
      </div>
      <ResponsiveLine
        data={lineData}
        margin={{ top: 20, right: 110, bottom: 80, left: 60 }}
        xScale={{ type: "point" }}
        yScale={{
          type: "linear",
          min: "auto",
          max: Math.max(
            ...lineData.map(
              (val) =>
                Math.max(
                  ...val.data.map((d) => Number.parseInt(`${d.y || 0}`))
                ) +
                val.data.length / 10
            )
          ),
          stacked: true,
          reverse: false,
        }}
        yFormat=" >-.2f"
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Time of day",
          legendOffset: 36,
          legendPosition: "middle",
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "count",
          legendOffset: -50,
          legendPosition: "middle",
        }}
        pointSize={10}
        pointColor={{ theme: "background" }}
        pointBorderWidth={2}
        pointBorderColor={{ from: "serieColor" }}
        pointLabelYOffset={-12}
        useMesh={true}
        legends={[
          {
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 100,
            translateY: 0,
            itemsSpacing: 0,
            itemDirection: "left-to-right",
            itemWidth: 80,
            itemHeight: 20,
            itemOpacity: 0.75,
            symbolSize: 12,
            symbolShape: "circle",
            symbolBorderColor: "rgba(0, 0, 0, .5)",
            effects: [
              {
                on: "hover",
                style: {
                  itemBackground: "rgba(0, 0, 0, .03)",
                  itemOpacity: 1,
                },
              },
            ],
          },
        ]}
      />
    </>
  );
};

export default TimeGraph;
