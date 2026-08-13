import { Link } from "react-router-dom";
import { LogOut } from "lucide-react";
import ApertureMark from "../ui/ApertureMark";
import ConnectGithubButton from "../ui/ConnectGithubButton";
import { useAuth } from "../../context/AuthContext";

export default function NavBar() {
  const { user, isLoading, logout } = useAuth();

  return (
    <header className="border-b border-line">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <Link to="/" className="flex items-center gap-2.5 text-ink">
          <ApertureMark />
          <span className="font-mono text-sm font-medium uppercase tracking-[0.18em]">
            SkillLens
          </span>
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/dashboard"
            className="font-mono text-xs uppercase tracking-[0.15em] text-slate transition-colors hover:text-ink"
          >
            Market
          </Link>

          {isLoading ? null : user ? (
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-2 rounded-full border border-line py-1 pl-1 pr-3">
                <img
                  src={user.avatar_url}
                  alt={user.github_username}
                  className="h-6 w-6 rounded-full"
                />
                <span className="font-mono text-xs text-ink">{user.github_username}</span>
              </div>
              <button
                onClick={logout}
                aria-label="Sign out"
                title="Sign out"
                className="flex h-8 w-8 items-center justify-center rounded-full text-slate transition-colors hover:bg-line hover:text-ink"
              >
                <LogOut className="h-4 w-4" strokeWidth={2} />
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
