# cellaflow-docs

Documentation for [Cellaflow](https://cellaflow.com), the coordination and durability layer for AI agents.

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
├── scripts/
│   └── check_quickstart_sync.py   # Keeps quickstart.mdx equal to the SDK example
├── index.mdx              # Landing / overview page
├── quickstart.mdx         # 3-minute quickstart (code is checked, see below)
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

## The quickstart code is checked

`quickstart.mdx` embeds
[`examples/quickstart/checkout_agent.py`](https://github.com/cellaflow/cellaflow-sdks/tree/main/examples/quickstart)
from `cellaflow-sdks` verbatim, and a workflow fails if the two have drifted.

```bash
python3 scripts/check_quickstart_sync.py          # verify
python3 scripts/check_quickstart_sync.py --fix    # rewrite the page from the example
```

The page has to show code that runs and that produces the output printed beside
it. The check exists because the opposite already shipped once: a copy taken
before a correctness fix landed left the page claiming an outcome the code shown
could not produce.

Edit the example in `cellaflow-sdks` and run `--fix` here. Editing the block in
the page by hand puts the two out of step, which is what the check will tell you.

It runs on pull requests that touch the page, on `main`, and weekly. The weekly
run is the one that matters: drift usually starts with a change in the *other*
repo, which never opens a pull request in this one. A failure does not hold back
a deploy, because Mintlify publishes from `main` independently of GitHub Actions.

## Deployment

Docs are deployed via Mintlify's GitHub integration to `docs.cellaflow.com`. Push to `main` to trigger a deploy.