import { ResponsiveTimeRange } from "@nivo/calendar";
import { FC } from "react";
import { useSightings } from "../../lib/hooks/useSightings";
import { DataMode } from "../../lib/types";
import Tooltip from "../shared/Tooltip";

interface Props {
  mode?: DataMode;
}

const formatDate = (date: Date) => date.toISOString().split("T")[0];

const SightingCalendar: FC<Props> = ({ mode = "realtime" }) => {
  const { data, isLoading } = useSightings(mode);

  const date = new Date(Date.now());
  const prevMonth = new Date(date.setMonth(date.getMonth() - 1));

  return (
    <>
      <div className="flex justify-between items-center">
        <p className="text-xl pb-4">Malicious Sightings this Month</p>
        <Tooltip content="This visualisation shows the number of potentially malicious sightings per month." />
      </div>

      {!isLoading && data && (
        <ResponsiveTimeRange
          data={data.map((s) => {
            const created = s.created.split("T")[0];
            const value = data.filter(
              (t) => created === t.created.split("T")[0]
            ).length;
            return {
              day: formatDate(new Date(Date.parse(s.created))),
              value,
            };
          })}
          from={formatDate(prevMonth)}
          to={formatDate(new Date(Date.now()))}
          emptyColor="#eeeeee"
          colors={["#61cdbb", "#97e3d5", "#e8c1a0", "#f47560"]}
          margin={{ top: 40, right: 40, bottom: 100, left: 40 }}
          dayBorderWidth={2}
          dayBorderColor="#ffffff"
          legends={[
            {
              anchor: "bottom-right",
              direction: "row",
              justify: false,
              itemCount: 4,
              itemWidth: 42,
              itemHeight: 36,
              itemsSpacing: 14,
              itemDirection: "right-to-left",
              translateX: -60,
              translateY: -80,
              symbolSize: 20,
            },
          ]}
        />
      )}
    </>
  );
};

export default SightingCalendar;
