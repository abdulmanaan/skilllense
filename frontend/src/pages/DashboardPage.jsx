import { useEffect, useState } from "react";
import { graphqlRequest } from "../lib/graphql";
import RoleSelector from "../components/dashboard/RoleSelector";
import SkillDemandList from "../components/dashboard/SkillDemandList";
import GapAnalysis from "../components/dashboard/GapAnalysis";

const ROLES_QUERY = `
  query Roles {
    roles {
      slug
      name
      jobCount
      topSkills {
        name
        category
        demand
      }
    }
  }
`;

export default function DashboardPage() {
  const [roles, setRoles] = useState([]);
  const [selectedSlug, setSelectedSlug] = useState(null);
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    graphqlRequest(ROLES_QUERY)
      .then((data) => {
        setRoles(data.roles);
        setSelectedSlug(data.roles[0]?.slug ?? null);
        setStatus("ready");
      })
      .catch(() => setStatus("error"));
  }, []);

  const selectedRole = roles.find((r) => r.slug === selectedSlug);

  return (
    <div className="mx-auto max-w-5xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-teal">Dashboard</p>
      <h1 className="mt-4 font-display text-4xl text-ink sm:text-5xl">
        Skill demand, by role.
      </h1>
      <p className="mt-4 max-w-xl text-slate">
        Pulled from live job postings. Pick a role to see which skills show
        up most often in real listings.
      </p>

      {status === "loading" && (
        <p className="mt-16 font-mono text-sm text-slate">Scanning the market…</p>
      )}
      {status === "error" && (
        <p className="mt-16 font-mono text-sm text-gold">
          Couldn't reach the market data. Is the backend running?
        </p>
      )}
      {status === "ready" && (
        <>
          <RoleSelector roles={roles} selectedSlug={selectedSlug} onSelect={setSelectedSlug} />
          {selectedRole && <SkillDemandList role={selectedRole} />}
          {selectedRole && <GapAnalysis roleSlug={selectedRole.slug} />}
        </>
      )}
    </div>
  );
}
