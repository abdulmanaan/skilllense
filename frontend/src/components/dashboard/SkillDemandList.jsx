export default function SkillDemandList({ role }) {
  if (role.topSkills.length === 0) {
    return (
      <p className="mt-12 font-mono text-sm text-slate">
        Not enough postings yet to surface skills for this role.
      </p>
    );
  }

  const maxDemand = Math.max(...role.topSkills.map((s) => s.demand));

  return (
    <div className="mt-10 space-y-4">
      {role.topSkills.map((skill) => (
        <div key={skill.name} className="flex items-center gap-4">
          <span className="w-36 shrink-0 truncate text-sm text-ink">{skill.name}</span>
          <div className="h-2 flex-1 rounded-full bg-line">
            <div
              className="h-2 rounded-full bg-gold"
              style={{ width: `${(skill.demand / maxDemand) * 100}%` }}
            />
          </div>
          <span className="w-8 shrink-0 text-right font-mono text-xs text-slate">
            {skill.demand}
          </span>
        </div>
      ))}
    </div>
  );
}
