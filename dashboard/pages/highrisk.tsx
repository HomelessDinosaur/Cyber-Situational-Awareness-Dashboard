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
        {/* <p className="pl-12">
          This is for demonstration purposes only and is not an example of your
          network&apos;s current security position.
        </p> */}
        <div className="flex h-screen gap-10 flex-wrap p-12">
          <Panel size="sm" light={false}>
            <SecurityStatus mode="highrisk" />
          </Panel>
          <Panel size="lg">
            <TimeGraph mode="highrisk" />
          </Panel>
          <Panel size="sm">
            <SightingCalendar mode="highrisk" />
          </Panel>
          <Panel size="sm">
            <SightingConsole mode="highrisk" />
          </Panel>
          <Panel size="md">
            <GeoMap mode="highrisk" />
          </Panel>
          <Panel size="xl">
            <NetworkGraph mode="highrisk" />
          </Panel>
        </div>
      </div>
      <div className="absolute bottom-0 h-5"></div>
    </>
  );
};

export default Home;
