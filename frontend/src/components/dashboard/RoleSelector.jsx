export default function RoleSelector({ roles, selectedSlug, onSelect }) {
  return (
    <div className="mt-10 flex flex-wrap gap-2 border-b border-line pb-6">
      {roles.map((role) => {
        const active = role.slug === selectedSlug;
        return (
          <button
            key={role.slug}
            onClick={() => onSelect(role.slug)}
            className={
              "rounded-full px-4 py-2 font-mono text-xs uppercase tracking-wide transition-colors " +
              (active
                ? "bg-ink text-paper"
                : "border border-line text-slate hover:border-ink hover:text-ink")
            }
          >
            {role.name}
            <span className="ml-2 opacity-60">{role.jobCount}</span>
          </button>
        );
      })}
    </div>
  );
}
