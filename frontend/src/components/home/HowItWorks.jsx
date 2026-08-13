const steps = [
  {
    label: "Scan",
    title: "We read the market",
    body: "Every day, SkillLens pulls live software job postings from across the industry, not a curated sample, the real thing.",
  },
  {
    label: "Focus",
    title: "We extract real skills",
    body: "Each posting is parsed for named technologies and frameworks, then grouped by role: Backend, Frontend, Mobile, and more.",
  },
  {
    label: "Compare",
    title: "You see your gap",
    body: "Connect GitHub and SkillLens lines your repositories up against market demand and show what you have, and what's worth learning next.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="border-t border-line bg-surface">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="font-display text-3xl text-ink sm:text-4xl">
          From noise to signal, in three passes.
        </h2>

        <div className="relative mt-14 grid gap-10 md:grid-cols-3">
          <div className="absolute inset-x-0 top-7 hidden h-px bg-line md:block" aria-hidden="true" />

          {steps.map((step) => (
            <div key={step.label} className="relative">
              <span className="relative z-10 inline-flex h-14 w-20 items-center justify-center rounded-full border border-gold bg-paper font-mono text-xs uppercase tracking-widest text-gold">
                {step.label}
              </span>
              <h3 className="mt-5 font-display text-xl text-ink">{step.title}</h3>
              <p className="mt-2 max-w-xs text-sm leading-relaxed text-slate">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
