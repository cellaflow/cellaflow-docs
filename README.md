# cellaflow-docs

Documentation for [CellaFlow](https://cellaflow.com) — The Execution Ledger for Multi-Agent AI.

Powered by [Mintlify](https://mintlify.com).

## Local Development

Install the Mintlify CLI:

```bash
npm install -g mint
```

Run the local preview server (from this directory):

```bash
mint dev
```

Or without a global install:

```bash
npx mint dev
```

The docs preview will be available at `http://localhost:3000`.

## Adding Pages

1. Create a new `.mdx` file in the appropriate folder
2. Add a YAML frontmatter block (`title`, `description`, `icon`)
3. Register the page path in `docs.json` under `navigation.groups`

## Structure

```
cellaflow-docs/
├── docs.json              # Mintlify configuration (navigation, theme, branding)
├── logos/                 # Logo and favicon assets
├── index.mdx              # Landing / overview page
├── quickstart.mdx         # 3-minute quickstart
├── concepts.mdx           # Core mental models
├── architecture.mdx       # System architecture
├── sdks/
│   └── python/
│       ├── overview.mdx   # Python SDK installation + examples
│       ├── decorators.mdx # @workflow, @step, @tool reference
│       └── langgraph.mdx  # CellaflowSaver checkpointer
├── self-hosting.mdx       # Docker, TLS, auth, env vars
├── api-reference.mdx      # gRPC API + grpcurl examples
└── changelog.mdx          # Release notes
```

## Deployment

Docs are deployed via Mintlify's GitHub integration to `docs.cellaflow.com`. Push to `main` to trigger a deploy.