const scatteredDots = [
  { x: 40, y: 60, r: 3, color: "var(--color-gold)" },
  { x: 340, y: 90, r: 2.5, color: "var(--color-teal)" },
  { x: 70, y: 300, r: 2, color: "var(--color-slate)" },
  { x: 320, y: 280, r: 3, color: "var(--color-gold)" },
  { x: 200, y: 30, r: 2, color: "var(--color-teal)" },
  { x: 30, y: 180, r: 2.5, color: "var(--color-slate)" },
];

export default function ApertureVisual() {
  return (
    <svg viewBox="0 0 400 400" className="mx-auto h-auto w-full max-w-md" aria-hidden="true">
      {scatteredDots.map((d, i) => (
        <circle key={i} cx={d.x} cy={d.y} r={d.r} fill={d.color} opacity="0.55" />
      ))}

      {scatteredDots.slice(0, 4).map((d, i) => (
        <line
          key={`l-${i}`}
          x1={d.x} y1={d.y} x2="200" y2="200"
          stroke="var(--color-line)" strokeWidth="1" strokeDasharray="2 4"
        />
      ))}

      <g className="origin-center motion-safe:animate-[spin_60s_linear_infinite]">
        <circle cx="200" cy="200" r="150" stroke="var(--color-line)" strokeWidth="1" fill="none" />
      </g>
      <circle cx="200" cy="200" r="110" stroke="var(--color-slate)" strokeWidth="1" fill="none" opacity="0.4" />
      <circle cx="200" cy="200" r="72" stroke="var(--color-teal)" strokeWidth="1.4" fill="none" opacity="0.7" />
      <circle cx="200" cy="200" r="40" stroke="var(--color-gold)" strokeWidth="2" fill="none" />
      <circle cx="200" cy="200" r="6" fill="var(--color-gold)" />
    </svg>
  );
}
