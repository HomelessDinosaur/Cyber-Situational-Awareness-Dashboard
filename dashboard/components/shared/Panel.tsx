import { FC, PropsWithChildren } from "react";

interface PanelProps extends PropsWithChildren {
  size: "sm" | "md" | "lg" | "xl";
  light?: boolean;
}

const Panel: FC<PanelProps> = ({ children, size, light = true }) => {
  return (
    <div
      className={`${
        size === "sm"
          ? "w-1/4 h-1/2"
          : size === "md"
          ? "w-5/12 h-1/2"
          : size === "lg"
          ? "w-7/12 h-1/2"
          : "w-full h-[80vh]"
      } rounded-md shadow-md p-4 ${
        light ? "bg-white" : "bg-slate-800"
      } overflow-hidden`}
    >
      {/* <img src="/img/information.svg" className="absolute" /> */}
      {children}
    </div>
  );
};

export default Panel;
