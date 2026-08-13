import { API_BASE_URL } from "./config";

export async function graphqlRequest(query, variables = {}) {
  const response = await fetch(`${API_BASE_URL}/graphql`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });
  const json = await response.json();
  if (json.errors) {
    throw new Error(json.errors[0]?.message || "GraphQL request failed");
  }
  return json.data;
}
