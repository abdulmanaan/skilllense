import scanImage from "../../assets/how-it-works/scan.jpg";
import focusImage from "../../assets/how-it-works/focus.jpg";
import compareImage from "../../assets/how-it-works/compare.jpg";

const steps = [
  {
    label: "Scan",
    title: "We read the market",
    body: "Every day, SkillLens pulls live software job postings from across the industry, not a curated sample, the real thing.",
    image: scanImage,
  },
  {
    label: "Focus",
    title: "We extract real skills",
    body: "Each posting is parsed for named technologies and frameworks, then grouped by role: Backend, Frontend, Mobile, and more.",
    image: focusImage,
  },
  {
    label: "Compare",
    title: "You see your gap",
    body: "Connect GitHub and SkillLens lines your repositories up against market demand: what you have, and what's worth learning next.",
    image: compareImage,
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="border-t border-line bg-surface">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="font-display text-3xl text-ink sm:text-4xl">
          From noise to signal, in three passes.
        </h2>

        <div className="mt-14 grid gap-10 sm:grid-cols-3">
          {steps.map((step) => (
            <div key={step.label}>
              <div className="aspect-square w-full overflow-hidden rounded-2xl border border-line bg-paper">
                <img src={step.image} alt={step.title} className="h-full w-full object-cover" />
              </div>
              <span className="mt-5 inline-block font-mono text-xs uppercase tracking-widest text-gold">
                {step.label}
              </span>
              <h3 className="mt-1 font-display text-xl text-ink">{step.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
