const variantStyles = {
  primary: "bg-gold text-ink hover:bg-ink hover:text-paper",
  secondary: "border border-ink/15 text-ink hover:border-gold hover:text-gold",
};

const base =
  "inline-flex items-center justify-center gap-2 rounded-full px-6 py-3 " +
  "font-body text-sm font-medium transition-colors duration-150 " +
  "disabled:opacity-50 disabled:pointer-events-none";

export default function Button({ variant = "primary", as: As = "button", className = "", ...props }) {
  return <As className={`${base} ${variantStyles[variant]} ${className}`} {...props} />;
}
