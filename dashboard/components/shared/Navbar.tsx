import Link from "next/link";

const Navbar = () => {
  return (
    <div className="bg-slate-800 h-32 flex items-center justify-between p-10 mb-6">
      <Link href="/">
        <h1 className="text-6xl text-white hover:cursor-pointer">CSA</h1>
      </Link>
      <div className="flex gap-2 md:gap-10">
        <Link href="/">
          <h2 className="text-2xl text-white hover:cursor-pointer">Home</h2>
        </Link>
        <Link href="/glossary">
          <h2 className="text-2xl text-white hover:cursor-pointer">Glossary</h2>
        </Link>
        <Link href="/highrisk">
          <h2 className="text-2xl text-white hover:cursor-pointer">
            High Risk
          </h2>
        </Link>
      </div>
    </div>
  );
};

export default Navbar;
