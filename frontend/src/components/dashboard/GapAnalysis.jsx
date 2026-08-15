import { useState } from "react";
import { graphqlRequest } from "../../lib/graphql";
import { useAuth } from "../../context/AuthContext";
import Button from "../ui/Button";
import ConnectGithubButton from "../ui/ConnectGithubButton";

const GAP_QUERY = `
  query SkillGap($role: String!) {
    skillGap(role: $role) {
      have { name demand }
      gap { name demand }
    }
  }
`;

export default function GapAnalysis({ roleSlug }) {
  const { token, user } = useAuth();
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);

  async function runAnalysis() {
    setStatus("loading");
    try {
      const data = await graphqlRequest(GAP_QUERY, { role: roleSlug }, token);
      setResult(data.skillGap);
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  }

  if (!user) {
    return (
      <div className="mt-16 rounded-2xl border border-line bg-surface p-8 text-center">
        <p className="font-display text-xl text-ink">See your own gap</p>
        <p className="mx-auto mt-2 max-w-sm text-sm text-slate">
          Connect GitHub to compare your repositories against this role's market demand.
        </p>
        <div className="mt-6 flex justify-center">
          <ConnectGithubButton />
        </div>
      </div>
    );
  }

  return (
    <div className="mt-16 border-t border-line pt-10">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-teal">Your gap</p>
      <h2 className="mt-3 font-display text-2xl text-ink">
        How you compare on this role
      </h2>

      {status === "idle" && (
        <Button variant="secondary" className="mt-6" onClick={runAnalysis}>
          Analyze my GitHub
        </Button>
      )}
      {status === "loading" && (
        <p className="mt-6 font-mono text-sm text-slate">Reading your repositories…</p>
      )}
      {status === "error" && (
        <p className="mt-6 font-mono text-sm text-gold">
          Couldn't analyze your repos. Try again in a moment.
        </p>
      )}

      {status === "ready" && result && (
        <div className="mt-8 grid gap-10 sm:grid-cols-2">
          <div>
            <p className="font-mono text-xs uppercase tracking-widest text-teal">
              Already covered
            </p>
            <ul className="mt-4 space-y-2">
              {result.have.length === 0 && (
                <li className="text-sm text-slate">No overlap found yet.</li>
              )}
              {result.have.map((s) => (
                <li key={s.name} className="flex items-center justify-between text-sm">
                  <span className="text-ink">{s.name}</span>
                  <span className="font-mono text-xs text-slate">{s.demand}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="font-mono text-xs uppercase tracking-widest text-gold">
              Worth learning
            </p>
            <ul className="mt-4 space-y-2">
              {result.gap.length === 0 && (
                <li className="text-sm text-slate">You're covering everything in demand.</li>
              )}
              {result.gap.map((s) => (
                <li key={s.name} className="flex items-center justify-between text-sm">
                  <span className="text-ink">{s.name}</span>
                  <span className="font-mono text-xs text-slate">{s.demand}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
