import ApertureMark from "../ui/ApertureMark";

export default function Footer() {
  return (
    <footer className="border-t border-line">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-10 text-slate sm:flex-row">
        <div className="flex items-center gap-2">
          <ApertureMark className="h-4 w-4" />
          <span className="font-mono text-xs uppercase tracking-[0.15em]">SkillLens</span>
        </div>
        <p className="font-mono text-xs">Built by Abdul Manan · Lahore, Pakistan</p>
      </div>
    </footer>
  );
}
