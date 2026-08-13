export default function ApertureMark({ className = "h-6 w-6" }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" className={className} aria-hidden="true">
      <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="1.2" opacity="0.35" />
      <circle cx="16" cy="16" r="9.5" stroke="currentColor" strokeWidth="1.2" opacity="0.6" />
      <circle cx="16" cy="16" r="5" stroke="currentColor" strokeWidth="1.4" />
      <circle cx="16" cy="16" r="1.6" fill="currentColor" />
    </svg>
  );
}
