import ConnectGithubButton from "../ui/ConnectGithubButton";
import Button from "../ui/Button";
import ApertureVisual from "./ApertureVisual";

export default function Hero() {
  return (
    <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 pb-20 pt-16 md:grid-cols-2 md:pt-24">
      <div>
        <p className="mb-6 font-mono text-xs uppercase tracking-[0.2em] text-teal">
          Live market signal · Software roles
        </p>
        <h1 className="font-display text-5xl leading-[1.05] text-ink sm:text-6xl">
          See what the market <em className="italic text-gold">actually</em> wants.
        </h1>
        <p className="mt-6 max-w-md text-lg leading-relaxed text-slate">
          SkillLens scans live developer job postings and turns the noise
          into a clear signal, which skills are rising, by role. Connect
          your GitHub and see exactly what's missing from your own toolkit.
        </p>
        <div className="mt-9 flex flex-wrap items-center gap-4">
          <ConnectGithubButton />
          <Button as="a" href="#how-it-works" variant="secondary">
            See how it works
          </Button>
        </div>
      </div>

      <ApertureVisual />
    </section>
  );
}
