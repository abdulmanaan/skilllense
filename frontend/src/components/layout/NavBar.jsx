import { Link } from "react-router-dom";
import ApertureMark from "../ui/ApertureMark";
import ConnectGithubButton from "../ui/ConnectGithubButton";

export default function NavBar() {
  return (
    <header className="border-b border-line">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <Link to="/" className="flex items-center gap-2.5 text-ink">
          <ApertureMark />
          <span className="font-mono text-sm font-medium uppercase tracking-[0.18em]">
            SkillLens
          </span>
        </Link>
        <ConnectGithubButton className="text-xs sm:text-sm" />
      </div>
    </header>
  );
}