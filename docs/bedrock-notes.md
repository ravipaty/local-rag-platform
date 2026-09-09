# AWS Bedrock Provider — Notes

## Cost reality
- Bedrock has **no dedicated free tier**. You are billed per token from the first call.
- New AWS accounts get up to **$200 in promotional credits** ($100 at signup, up to $100 more
  for trying services). These **expire after 6 months**, whether or not you've used them.
- Track usage manually during dev — don't loop test calls. A handful of ingest/query
  calls is enough to prove the swap works; there's no need to re-ingest a whole
  document set against Bedrock just to demo it.

## IAM setup (least privilege)
1. Create an IAM user or role scoped to `bedrock:InvokeModel` only.
2. Restrict the resource to the specific model ARN(s) you're testing, not `*`.
3. Request model access in the Bedrock console for the models you plan to use
   (some require an access request before first use).

## Credentials
- Local testing: `aws configure` → stored in `~/.aws/credentials`, picked up
  automatically by boto3.
- In-cluster testing: mount credentials via a Sealed Secret, never a plain
  K8s Secret committed to git.

## When to use this provider in the project
- To demonstrate a provider-abstraction pattern (same RAG pipeline, swappable backend).
- To show IAM least-privilege configuration as a portfolio artifact.
- Not intended to run continuously — Ollama is the default and primary path.

## Log of test usage (fill in as you go)
| Date | Calls | Approx. tokens | Notes |
|------|-------|-----------------|-------|
|      |       |                 |       |
