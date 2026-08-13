import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AuthCallbackPage() {
  const [searchParams] = useSearchParams();
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      login(token);
      navigate("/dashboard", { replace: true });
    } else {
      navigate("/", { replace: true });
    }
  }, [searchParams, login, navigate]);

  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <p className="font-mono text-sm uppercase tracking-widest text-slate">
        Signing you in…
      </p>
    </div>
  );
}
