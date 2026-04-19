# Thronglets-Style AI Game: Full Roadmap, MVP Cut, and Article Plan

## How to Read This Plan

This document has three jobs:

1. Define a sane public MVP.
2. Preserve the full long-term roadmap so the project can keep expanding over time.
3. Attach each phase to an article milestone so the build story stays coherent.

This is not an MVP-only plan. It is a full roadmap with an MVP cut through it.

## Project Thesis

Build a local-LLM virtual creature game that works as:

- a real backend-heavy AI product
- a showcase repo for AI engineering interviews
- a vehicle for comparing multiple AI techniques on the same problem
- a sequence of technical articles that build on each other naturally

The public story should always be:

1. here is the default system
2. here is the seam
3. here are the variants
4. here is how they were measured
5. here is the recommended default and why

## MVP Cut

### What v1 Must Prove

The first public release must show:

- a working backend
- a visible dimart tribe
- real-time streamed dialogue
- persistent world and turn state
- memory retrieval
- reranking
- safety basics
- context controls
- traces
- evaluations
- a benchmark story

### v1 Product Scope

- **5 fixed dimarts**
- no breeding
- no open-ended population growth
- FastAPI backend
- REST API for commands
- SSE for streamed replies
- WebSocket for tribe and world events
- Typer CLI client
- PostgreSQL as source of truth
- Qdrant as derived memory index
- dense retrieval + BM25 hybrid retrieval
- metadata filtering in retrieval
- reranking enabled in the default path
- LangChain in the default shipped path
- optional thin LangGraph per-dimart flow
- basic sanitization and moderation boundary
- context pruning and summarization policy
- LangSmith traces
- DeepEval / RAGAS-backed evaluation and benchmark suite
- structured logs and `/metrics`

### v1 Non-Goals

- full civilization simulation
- full multi-agent supervisor graphs
- multimodal perception in the main shipped path
- LoRA or QLoRA in the main shipped path
- embedding fine-tuning in the main shipped path
- NeMo Guardrails as a hard requirement for the first release
- MLflow or W&B as a hard requirement for the first release
- MCP, gRPC, or A2A as required transports for v1
- DSPy or LlamaIndex as required frameworks for v1
- vLLM or SGLang as required runtimes for v1

These are not removed from the roadmap. They are moved to later phases.

## Cross-Cutting Rules

### Pragmatic Clean Architecture

Use:

- `domain/`
- `application/`
- `ports/`
- `adapters/`

Do not go full textbook Clean Architecture with maximum ceremony. The architecture should create explicit boundaries without forcing every interaction through unnecessary mapping layers.

### One Canonical Default Path

The repository must have one clear default product path.

Alternative implementations exist to support:

- comparisons
- experiments
- benchmarks
- articles
- interview signaling

But those variants must plug into the same use-case flow rather than producing multiple parallel app architectures.

### Frameworks at the Edge, Plain Python in the Core

LangChain and LangGraph should be visible and deliberate, but core domain and application logic should remain plain Python and heavily testable.

The repo should visibly demonstrate:

- `RunnablePassthrough`
- `RunnableLambda`
- `DocumentCompressor`
- `.astream()`
- `.astream_events()`

without burying business logic inside framework glue.

### Source of Truth Rules

- **Postgres** stores authoritative state
- **Qdrant** stores derived retrieval state
- **LangSmith** stores traces, eval context, and debugging data

## Canonical Turn Lifecycle

Every player or system turn should follow the same high-level flow:

1. accept command or event
2. load authoritative state from Postgres
3. build turn context
4. retrieve candidate memories
5. rerank retrieved candidates
6. assemble prompt
7. generate and stream output
8. persist turn result
9. update derived memory index
10. emit tribe and world events

Every turn should be traceable with explicit states:

- `pending`
- `retrieving`
- `generating`
- `streaming`
- `completed`
- `partial`
- `failed`
- `cancelled`

## Tribe Model

The project starts with a constrained tribe:

- exactly 5 dimarts in v1
- fixed roster
- distinct personalities and roles
- shared world state
- individual memory and dialogue state
- visible dimart-to-dimart communication
- no breeding
- no procedural population explosion

Implementation recommendation:

- one reusable per-dimart behavior flow
- one thin `SocietyCoordinator`
- one explicit event model for inter-dimart communication

## Repository Shape

```text
dimarts/
├── README.md
├── app/
│   ├── domain/
│   ├── application/
│   ├── ports/
│   └── adapters/
├── evaluation/
│   ├── datasets/
│   ├── benchmarks/
│   ├── metrics/
│   └── regression/
├── experiments/
│   ├── retrieval/
│   ├── ranking/
│   ├── inference/
│   ├── context/
│   ├── safety/
│   ├── frameworks/
│   └── protocols/
├── notebooks/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── articles/
    └── outlines/
```

The main app path lives in `app/`. Comparisons and breadth-signaling work live in `evaluation/`, `experiments/`, and `notebooks/`.

## Full Phase Roadmap

### Phase 0: Foundations, Repo Boundaries, and Default Flow

**Goal**

Set up the repository so the project can grow without becoming messy.

**Build**

- pragmatic CA layout
- canonical turn lifecycle
- source-of-truth boundaries
- ports for `ModelBackend`, `RetrieverPipeline`, `Ranker`, `ContextStrategy`, `TurnStore`, `MemoryIndex`, `StreamTransport`, `TraceSink`, `SocietyCoordinator`
- benchmark and evaluation directories from day one

**Article**

- Article 0: “How I’m structuring this repo so I can compare AI techniques without creating a mess”

### Phase 1: Streaming Backend and Local Runtime

**Goal**

Get one dimart talking through a real backend.

**Build**

- FastAPI backend
- REST command surface
- SSE for token streaming
- WebSocket for real-time event delivery
- Typer CLI client
- local model integration
- GGUF as default runtime
- LangChain prompt composition and streaming
- model loader abstraction

**Comparison Tracks**

- GGUF vs GPTQ vs AWQ
- TTFT and throughput benchmarks
- prompt composition variants
- tokenizer deep-dive notebook

**Article**

- Article 1: “Streaming a local LLM through FastAPI, SSE, and a CLI client”

### Phase 2: Dimart Tribe and Social Event Layer

**Goal**

Expand from one dimart to the 5-dimart tribe without introducing full civilization complexity.

**Build**

- 5 fixed dimarts
- tribe state
- `SocietyCoordinator`
- inter-dimart event model
- WebSocket event stream for tribe activity

**Comparison Tracks**

- event schemas
- push vs pull event delivery patterns
- protocol notes for WS/SSE split

**Article**

- Article 2: “From one dimart to a 5-dimart tribe without rewriting the architecture”

### Phase 3: Structured Persistence and Memory Indexing

**Goal**

Introduce persistent game state and memory storage cleanly.

**Build**

- PostgreSQL for authoritative world, tribe, and turn data
- Alembic migrations
- Qdrant as derived memory store
- turn persistence
- memory indexing after turn completion

**Comparison Tracks**

- synchronous vs deferred indexing
- schema choices for event history and conversation persistence

**Article**

- Article 3: “Postgres for truth, Qdrant for memory: drawing the line correctly”

### Phase 4: Retrieval Baseline

**Goal**

Make dimarts remember correctly and measurably.

**Build**

- embeddings
- chunking strategies
- dense retrieval
- BM25 retrieval
- fusion
- metadata filtering
- reranking in the default path
- retrieval metrics

**Comparison Tracks**

- dense-only vs hybrid
- reranker on vs off
- chunking strategy comparisons
- embedding model comparisons
- HyDE

**Deferred From This Phase**

- late interaction
- GraphRAG
- multimodal retrieval

**Article**

- Article 4: “Hybrid retrieval and reranking for dimart memory”

### Phase 5: Safety and Context Baseline

**Goal**

Add the minimum safety and context controls required for a credible public AI product.

**Build**

- input sanitization
- prompt-injection checks
- moderation boundary
- sensitive-data handling
- output filtering policy
- sandboxing for any dimart actions
- context pruning
- summarization policy
- prompt and memory token budgets
- lost-in-the-middle mitigation

**Comparison Tracks**

- regex + heuristic sanitization
- embedding-based injection detection
- pruning strategies
- summarization thresholds
- NeMo Guardrails integration

**Article**

- Article 5: “Safety, pruning, and not letting the app go off the rails”

### Phase 6: Evaluation, Tracing, and Monitoring

**Goal**

Make improvements measurable and regressions visible before the public release.

**Build**

- LangSmith tracing
- DeepEval integration
- RAGAS integration
- evaluation datasets
- retrieval metrics
- pairwise comparison reports
- LLM-as-judge reports
- response-quality regression suite
- structured logs
- `/metrics` endpoint
- simple monitoring dashboards or SLO-style latency documentation

**Comparison Tracks**

- baseline vs reranked pipeline
- baseline vs fine-tuned retrieval later
- prompt version A/B tests

**Article**

- Article 6: “How I evaluate, trace, and monitor an AI system instead of just eyeballing it”

### Public MVP Release

The first public release happens after **Phases 0-6**.

### Phase 7: Cost Optimization

**Goal**

Reduce runtime cost without damaging product quality.

**Build**

- semantic cache
- model routing
- request batching where it actually helps
- cache quality analysis
- routing heuristics
- latency/cost benchmark reporting

**Article**

- Article 7: “Reducing cost without wrecking quality”

### Phase 8: Agent Architecture

**Goal**

Expand from a thin orchestration flow to richer agentic patterns once the core system is stable.

**Build**

- thin per-dimart LangGraph flow if not already present
- reflection
- explicit checkpointing
- structured output boundaries
- memory-aware planning hooks
- reasoning traces
- HITL checkpoints

**Comparison Tracks**

- plain orchestrator vs LangGraph
- reflection on vs off
- HITL on vs off
- tool-calling flows

**Article**

- Article 8: “Where LangGraph and agent patterns actually help”

### Phase 9: Protocols and Framework Comparisons

**Goal**

Cover breadth topics that come up in interviews without rebuilding the whole project from scratch for each one.

**Build**

- MCP experiment or integration surface
- gRPC experiment track
- A2A positioning notes with one concrete comparison
- DSPy experiment track
- LlamaIndex experiment track

**Comparison Tracks**

- WS/SSE vs protocol-heavier approaches
- LangChain vs LlamaIndex on a focused retrieval task
- plain orchestration / LangGraph vs DSPy-style optimization on a narrow workflow

**Article**

- Article 9: “When WS/SSE is enough, and when protocols and framework alternatives matter”

### Phase 10: Self-Hosted Inference Backends

**Goal**

Cover the model-serving depth that comes up in interviews without turning the whole project into infra theatre.

**Build**

- vLLM integration
- backend abstraction for alternate runtimes
- static and dynamic batching
- speculative decoding experiment
- quantization comparisons

**Optional Extensions**

- SGLang exploration
- inference balancing
- deeper paged-attention notes

**Comparison Tracks**

- llama.cpp-style local runtime vs vLLM
- batching impact on latency and throughput
- speculative decoding impact

**Article**

- Article 10: “How much inference-backend depth a backend-focused AI engineer actually needs”

### Phase 11: Fine-Tuning and ML/NLP Depth

**Goal**

Preserve the original ML depth work as later, explicit tracks instead of forcing it into v1.

**Build**

- synthetic dialogue dataset pipeline
- LoRA and QLoRA track
- embedding fine-tuning track
- experiment tracking for training runs
- tokenizer analysis
- optimization-method notes and metrics

**Comparison Tracks**

- base model vs LoRA persona model
- base embeddings vs fine-tuned embeddings
- distilled small model vs larger baseline

**Article**

- Article 11: “Fine-tuning, embeddings, tokenizers, and what should stay out of the MVP”

### Phase 12: Advanced Retrieval and Multimodal

**Goal**

Preserve the retrieval-breadth and multimodal work from the original roadmap without bloating the baseline system.

**Build**

- late-interaction retrieval experiment
- GraphRAG experiment branch
- multimodal experiment branch
- image input to dimarts
- visual memory indexing

**Comparison Tracks**

- text-only vs multimodal retrieval
- caption-based indexing vs unified embedding approaches
- baseline hybrid retrieval vs advanced retrieval branches

**Article**

- Article 12: “Advanced retrieval beyond the baseline hybrid pipeline”

### Phase 13: Richer Society and Multi-Agent Expansion

**Goal**

Extend the 5-dimart tribe into a deeper social system after the fundamentals are stable.

**Build**

- richer tribe behavior
- broader inter-dimart orchestration
- optional supervisor graphs
- more autonomous social loops
- larger society simulation

**Comparison Tracks**

- thin coordinator vs supervisor graph
- explicit turn-taking vs emergent scheduling

**Article**

- Article 13: “Scaling the tribe into a real society”

## Test Strategy Across All Phases

Testing is not a late phase. Every phase should extend the same test pyramid:

- **unit tests**
  - domain rules
  - ranking math
  - context logic
  - event shaping
- **integration tests**
  - FastAPI routes
  - Postgres
  - Qdrant
  - LangChain adapters
  - LangGraph adapters when used
  - SSE and WebSocket boundaries
- **evaluation/regression**
  - retrieval quality
  - ranking quality
  - response quality
  - benchmark comparisons
- **limited end-to-end**
  - one player-to-dimart happy path
  - one tribe-event path

Failure modes that should be covered explicitly:

- client disconnect during stream
- partial generation
- duplicate submit or retry
- empty retrieval result
- reranker failure
- Qdrant failure
- Postgres failure after stream start
- malformed memory data
- context overflow

## Performance Strategy Across All Phases

The benchmark story should stay consistent across the roadmap.

Always track:

- retrieval latency
- reranking latency
- prompt assembly latency
- time to first token
- total turn latency
- token throughput

Always document:

- prompt token budget
- memory token budget
- number of retrieved items included
- summarization and pruning policy
- cache policy

## Interview Coverage Map

This roadmap is designed to eventually cover the interview topics below.

1. **ML/NLP basics**
   - primary phases: 1, 10, 11
   - terms: embeddings, tokenizers, fine-tuning, distillation, optimization, metrics
2. **Retrieval**
   - primary phases: 4, 12
   - terms: chunking, hybrid search, metadata filtering, HyDE, GraphRAG, reranking, cross-encoding, late interaction, metrics
3. **Protocols**
   - primary phases: 1, 2, 9
   - terms: WS, SSE, gRPC, MCP, A2A
4. **Agent architecture**
   - primary phases: 2, 8, 13
   - terms: HITL, reflection, checkpointing, agentic memory, multi-agent orchestration, planning and execution, structured output
5. **Safety**
   - primary phases: 5
   - terms: sanitizing, guardrails, moderation, jailbreaks, injections, data leakage, sandboxing
6. **Cost reduction**
   - primary phases: 7, 10
   - terms: semantic cache, model routing, batching
7. **Context optimization**
   - primary phases: 5, 7
   - terms: pruning, lost in the middle, summarization
8. **Self-hosted backends**
   - primary phases: 1, 10
   - terms: vLLM, SGLang, paged attention, speculative decoding, batching, quantization, inference balancing
9. **Frameworks**
   - primary phases: 1, 8, 9
   - terms: LangChain, LangGraph, DSPy, LlamaIndex
10. **Testing agent and RAG systems**
   - primary phases: 6
   - terms: DeepEval, LLM-as-judge, pairwise comparison, RAGAS, CI-style regression
11. **Observability**
   - primary phases: 6, 10
   - terms: tracing, monitoring, eval visibility, production debugging

## Final Rule

The project should always remain understandable in this order:

1. default product path
2. boundaries and ports
3. comparison seams
4. benchmarks and evals
5. recommended defaults

If the roadmap grows but that order stays clear, the repo scales cleanly.
If the roadmap grows and that order disappears, the repo becomes a mess.
