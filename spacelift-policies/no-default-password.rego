# OPA/Rego policy for Spacelift — blocks a plan/apply if the Postgres
# password variable is left at its insecure placeholder default.
#
# Upload this in the Spacelift UI under Policies > Plan Policies,
# and attach it to the local-rag-platform stack.

package spacelift

# Deny if postgres_password resolves to the insecure default.
deny[msg] {
    input.terraform.resource_changes[_].change.after.data.POSTGRES_PASSWORD == "Y2hhbmdlbWU="  # base64("changeme")
    msg := "postgres_password is still set to the insecure default 'changeme' — override it via a Spacelift environment variable or tfvars before applying."
}

# Warn (non-blocking) if no explicit tfvars/environment override was supplied.
warn[msg] {
    not input.run.variables.postgres_password
    msg := "No postgres_password override detected in this run's variables — confirm this is intentional for a non-production stack."
}
