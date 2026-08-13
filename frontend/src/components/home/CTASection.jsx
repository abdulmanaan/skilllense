import ConnectGithubButton from "../ui/ConnectGithubButton";

export default function CTASection() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24 text-center">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-teal">
        Your CV says you know it
      </p>
      <h2 className="mx-auto mt-4 max-w-2xl font-display text-4xl leading-tight text-ink sm:text-5xl">
        Show them the data behind it.
      </h2>
      <div className="mt-8">
        <ConnectGithubButton />
      </div>
    </section>
  );
}
