import { NextPage } from "next";
import Link from "next/link";
import glossary_data from "../lib/glossary_data.json";
import threat_library from "../lib/threat_library.json";

const slugify = (word: string) => word.toLowerCase().replace(" ", "-");

const Glossary: NextPage = () => {
  return (
    <div className="p-2 md:p-10">
      <p className="text-2xl font-medium pb-5">Threat Library</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        {threat_library.map((t) => (
          <div key={t.title} className="flex flex-col gap-2 shadow-md p-5">
            <p className="text-lg font-medium">{t.title}</p>
            <p className="font-medium">Characteristics</p>
            <p className="text-md pl-1">{t.characteristics}</p>
            <p className="font-medium">Risks</p>
            <p className="text-md pl-1">{t.risks}</p>
            <p className="font-medium">Detection</p>
            <p className="text-md pl-1">{t.detection}</p>
            <p className="font-medium">Prevention</p>
            <p className="text-md pl-1">{t.prevention}</p>
          </div>
        ))}
      </div>
      <hr className="m-10" />

      <p className="text-2xl font-medium pb-5">Technical Terms</p>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
        {glossary_data
          .sort((a, b) => a.title.localeCompare(b.title))
          .map((d) => (
            <div
              id={slugify(d.title)}
              key={d.title}
              className="flex flex-col gap-2 shadow-md p-6 hover:bg-slate-50 hover:cursor-pointer"
            >
              <p className="text-md font-bold">{d.title}</p>
              <p className="text-md">{d.description}</p>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Glossary;
