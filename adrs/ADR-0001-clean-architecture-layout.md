# ADR-0001: Clean Architecture layout for the project

## Date
2026-06-06

## Status
Accepted

## Context
This is the foundational decision for the repo where the work is about to begin, made before any feature logic exists. The forcing pressure is that the project will be swapping implementations behind stable interfaces over a long roadmap, to keeping core logic testable in isolation from infrastructure (Postgres, Qdrant, model runtimes). The choice of layout has to be made now because every later feature is placed relative to it, and refactoring once code exists is much more expensive than committing to boundaries up front. The skeleton for this layout already shipped in Feature 1; this ADR records the decision behind it.

## Decision
The `app/` will be structured as pragmatic Clean Architecture with five layers — `domain/`, `application/` (owning `application/ports/`), `entrypoints/`, `infra/`, and `composition/`. The dependency flow is `entrypoints/ → application/ → ports/ ← infra/`, with `domain/` at the core: `application/` depends on `domain/`, and `domain/` imports no other layer. `composition/` is the only layer permitted to import both `application/` and `infra/`. Dependency injection uses FastAPI's native nested `Depends`: per-feature router `deps.py` modules compose use cases from the ports they need, while `composition/` (a package, not a single file) centralizes only adapter selection so `app/main.py` stays thin as number of routers grows. `composition/providers.py` holds the actual adapter-construction factories; `Depends` adapts them for the HTTP request path, while non-HTTP entrypoints (e.g. the LangGraph cognition tick, background workers) call those providers directly rather than through `Depends`.
The wording "pragmatic CA" for this repo means no mandatory DTO translation at every layer boundary, only where it makes sense (e.g. at the HTTP edge, persistennce edge); no DI container (native FastAPI's Depends); no monolithic composition root.

## Alternatives considered
- **Flat / single-module FastAPI app** (routers + services + DB in one tree): no means to swap model backend, retrieval, or cognition behind.
- **Single central composition file plus all wiring in `main.py`**: both grow with every new router; per-feature `deps.py` keeps wiring local and `main.py` concies over the project's lifetime.
- **Framework-centric layout organized around LangChain/LangGraph primitives**: buries business logic in what framework provides and makes the node bodies (where I ultimately want to have multiple options for) — hard to test.
- **Feature-based vertical slices instead of layer-based**: what I need to swap is infra behind ports, and layering makes that swap obvious where feature slices wouldn't. Routers are still split by feature inside `entrypoints/`, so I keep feature locality where it helps.

## Consequences
Easier:
- Swapping `infra/` adapters behind ports without touching use cases.
- Heavy unit testing of `domain/` and `application/` in plain Python with no Postgres, Qdrant, model runtime, or network.
- Keeping LangGraph/LangChain at the edge: the graph topology is the only framework-coupled surface, so the canonical multi-step lifecycle stays inspectable.
- `main.py` stays thin and per-feature `deps.py` localizes use-case wiring, so wiring does not centralize into one growing file as routers multiply.

Harder:
- Up-front boilerplate: every external capability needs a port + adapter + provider even when it has exactly one implementation today.
- Discipline cost: the `entrypoints/ → infra/` shortcut must be resisted by convention — the boundary is not compiler-enforced, and no import-linter is wired up yet.
- `composition/` is the one place of severe coupling (adapters -> ports); it must know about both sides, so it carries the wiring complexity the other layers do not.
- Risk of premature abstraction — ports invented for capabilities that may never gain a second implementation.

## Re-baseline impact
None. This is a purely structural decision and is not expected to move any tracked benchmark number (once added: TTFT, token throughput, tick latency, retrieval/rerank latency).
The only side effect I can think of: per-request resolution through framework's `Depends` adds negligible overhead; if that resolution ever grows big enough to affect TTFT - that would be a reversal/revisiting signal rather than an accepted cost.

## Reversal trigger
- A single application-layer use case repeatedly needs to bypass `application/ports/` and reach `app/infra/` directly to do its job — the boundary is drawn in the wrong place.
- `main.py` or any `composition/` module grows more or less linearly with the number of routers despite the per-feature `deps.py` convention — the thin-`main`/local-wiring goal has failed.
- Boundary-crossing is repeatedly the *correct* call rather than an occasional mistake — use cases that really need to reach past `application/ports/` to do their job, or features that consistently look more naturally as vertical slices than as layers.
