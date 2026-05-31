# Security Policy

CaiHub handles concepts related to restaurant operations, visual quality checks,
production events, and business reporting. Treat operational data as sensitive
even when it looks routine.

## Reporting a Security Issue

Please do not open a public GitHub issue for security vulnerabilities or leaked
secrets.

To report a security issue, contact the maintainer privately through the GitHub
repository owner profile or another private channel already established with
the maintainer. Include a concise description, reproduction steps, affected
files or endpoints, and the potential impact.

## Do Not Publicly Disclose Secrets

Never post the following in issues, pull requests, discussions, screenshots, or
logs:

- API keys, tokens, passwords, session cookies, or webhook URLs.
- Feishu/Lark app secrets, tenant credentials, bot credentials, or message
  callback URLs.
- Real restaurant operating data, store names, customer identifiers, phone
  numbers, staff identifiers, or supplier data.
- Raw production screenshots, original dish images from real stores, business
  reports, or export files.

If a secret is accidentally committed or disclosed, rotate it immediately and
remove the leaked value from future commits and documentation.

## Environment Files

- `.env` is for local development only and must not be committed.
- The repository should keep only `.env.example` with safe placeholder values.
- New configuration values should be documented with placeholders, not real
  credentials.

## Restaurant Data and Visual Assets

When working with dish standards, production events, vision QA results, store
daily reports, or AI-generated operating summaries:

- Use synthetic data for examples and tests.
- Remove or replace real store names, timestamps, staff names, device IDs,
  image URLs, report IDs, and order/customer identifiers.
- Use sample image paths or placeholder URLs instead of real source images.
- Aggregate metrics when possible and avoid exposing row-level operating data.

## Supported Versions

This repository is pre-1.0 and under active development. Security fixes should
target the main development branch unless a maintained release branch is
explicitly announced.
