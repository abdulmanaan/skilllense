import GithubIcon from "./GithubIcon";
import Button from "./Button";
import { GITHUB_LOGIN_URL } from "../../lib/config";

export default function ConnectGithubButton({ variant = "primary", className = "" }) {
  return (
    <Button as="a" href={GITHUB_LOGIN_URL} variant={variant} className={className}>
      <GithubIcon className="h-4 w-4" />
      Connect GitHub
    </Button>
  );
}
