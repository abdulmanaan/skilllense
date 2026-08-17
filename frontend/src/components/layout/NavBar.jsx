import { Link } from "react-router-dom";
import ApertureMark from "../ui/ApertureMark";
import ConnectGithubButton from "../ui/ConnectGithubButton";
import { useAuth } from "../../context/AuthContext";

export default function NavBar() {
  const { user, isLoading, logout } = useAuth();

  return (
    <header className="border-b border-line">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-4 sm:px-6 sm:py-5">
        <Link to="/" className="flex shrink-0 items-center gap-2 text-ink sm:gap-2.5">
          <ApertureMark className="h-5 w-5 sm:h-6 sm:w-6" />
          <span className="font-mono text-xs font-medium uppercase tracking-[0.14em] sm:text-sm sm:tracking-[0.18em]">
            SkillLens
          </span>
        </Link>

        <div className="flex shrink-0 items-center gap-3 sm:gap-6">
          <Link
            to="/dashboard"
            className="font-mono text-[11px] uppercase tracking-[0.12em] text-slate transition-colors hover:text-ink sm:text-xs sm:tracking-[0.15em]"
          >
            Market
          </Link>

          {isLoading ? null : user ? (
            <div className="flex items-center gap-1.5 sm:gap-2">
              <div className="flex shrink-0 items-center gap-2 rounded-full border border-line py-1 pl-1 pr-1.5 sm:pr-3">
                <img
                  src={user.avatar_url}
                  alt={user.github_username}
                  className="h-6 w-6 shrink-0 rounded-full object-cover"
                />
                <span className="hidden max-w-[100px] truncate font-mono text-xs text-ink sm:inline">
                  {user.github_username}
                </span>
              </div>
              <button
                onClick={logout}
                className="shrink-0 whitespace-nowrap font-mono text-[11px] uppercase tracking-[0.1em] text-slate transition-colors hover:text-ink sm:text-xs"
              >
                Sign out
              </button>
            </div>
          ) : (
            <ConnectGithubButton className="text-xs sm:text-sm" />
          )}
        </div>
      </div>
    </header>
  );
}
