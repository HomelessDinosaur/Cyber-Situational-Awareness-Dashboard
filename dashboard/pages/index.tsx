import type { NextPage } from "next";
import GeoMap from "../components/data/GeoMap";
import NetworkGraph from "../components/data/NetworkGraph";
import SecurityStatus from "../components/data/SecurityStatus";
import SightingCalendar from "../components/data/SightingCalendar";
import SightingConsole from "../components/data/SightingConsole";
import TimeGraph from "../components/data/TimeGraph";
import Panel from "../components/shared/Panel";

const Home: NextPage = () => {
  return (
    <>
      <div>
        <div className="flex h-screen gap-10 flex-wrap p-12">
          <Panel size="sm" light={false}>
            <SecurityStatus />
          </Panel>
          <Panel size="lg">
            <TimeGraph />
          </Panel>
          <Panel size="sm">
            <SightingCalendar />
          </Panel>
          <Panel size="sm">
            <SightingConsole />
          </Panel>
          <Panel size="md">
            <GeoMap />
          </Panel>
          <Panel size="xl">
            <NetworkGraph />
          </Panel>
        </div>
      </div>
      <div className="absolute bottom-0 h-5"></div>
    </>
  );
};

export default Home;
