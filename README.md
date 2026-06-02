# Dimarts

Have you watched Black Mirror's "Thronglets" and had that thought too: is this where we are heading?

Dimarts is my attempt to find that out.

The plan is simple on the surface: build a small tribe of AI creatures, give them a world, memory, private state, and enough autonomy. Under the hood, this is going to be a backend-heavy AI simulation with swappable model backends: local models first, but not forever. FastAPI, streamed turns, an authoritative simulation engine, LangGraph orchestration, retrieval-backed memory, evaluations, traces, and a Phaser client.

The roadmap starts with the boring parts that make the strange parts believable: clear boundaries, a stable turn lifecycle, measurements, and deployment. Then the dimarts get their tribe, memory, private state, and eventually real autonomy.

- Phase 1: public vertical slice with streamed dimart replies.  <=== we are here
- Phases 2-3: tribe, simulation clock, persistence, and hidden state.
- Phase 4: retrieval-backed dimart memory.
- Phases 5-6: safety, context controls, traces, and evaluations.
- Later phases: cost work, cognition, serving upgrades, framework comparisons, and long-running society behavior.

## Verify

Run the full local verification chain from the repository root:

```bash
just verify
```

## Directory Map

- `app/` - Python application itself.
- `app/domain/` - Core domain concepts and rules with no framework or infrastructure dependencies.
- `app/application/` - Use cases and application services that coordinate domain behavior.
- `app/application/ports/` - Interfaces/Protocols owned by the application layer for persistence, model backends, retrieval, tracing, and other external capabilities.
- `app/entrypoints/` - Driving adapters such as FastAPI routers, streaming handlers, CLI commands, and metrics endpoints.
- `app/infra/` - Driven adapters that implement application ports using databases, queues, model runtimes, tracing tools, and external services.
- `app/composition/` - Composition-root package that binds infra adapters to application ports.
- `client/` - Browser presentation adapters; CLI and streaming APIs live under backend entrypoints.
- `client/phaser/` - Phaser presentation adapter for rendering backend-owned state and sending player commands.
- `deploy/` - Deployment artifacts, hosting configuration, containers, and infrastructure manifests.
- `evaluation/` - Evaluation assets and repeatable measurement work.
- `evaluation/datasets/` - Curated inputs and fixtures for evaluation runs.
- `evaluation/benchmarks/` - Benchmark definitions and execution scaffolding.
- `evaluation/metrics/` - Metric definitions and scoring logic.
- `evaluation/regression/` - Regression checks for model, simulation, and behavior changes.
- `experiments/` - Exploratory scripts, configs, and analysis for comparing approaches; product-ready implementations live under `app/` behind ports.
- `tests/` - Automated test suite.
- `tests/unit/` - Fast isolated tests for domain, application, and small adapter behavior.
- `tests/integration/` - Cross-boundary tests for adapters, persistence, APIs, and orchestration.
- `tests/e2e/` - End-to-end tests for user-facing flows.
- `adrs/` - Architecture Decision Records.
