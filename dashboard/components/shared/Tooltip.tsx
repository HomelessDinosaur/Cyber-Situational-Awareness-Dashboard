import Image from "next/image";
import React, { FC, useState } from "react";

interface TooltipProps extends React.PropsWithChildren {
  content: string;
}

const Tooltip: FC<TooltipProps> = ({ content }) => {
  const [hover, setHover] = useState(false);
  return (
    <div
      className="relative"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <Image
        src="/img/info.png"
        width="20px"
        height="20px"
        className="hover:cursor-pointer"
      />
      {hover && (
        <div className="inline-block w-80 absolute right-1 top-1 z-50 bg-gray-100 opacity-90 py-2 px-3 text-sm rounded-lg shadow-sm">
          {content}
        </div>
      )}
    </div>
  );
};

export default Tooltip;
