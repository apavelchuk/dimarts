# Thronglets-Style AI Game: Full Roadmap, MVP Cut, and Article Plan

## How to Read This Plan

This document now has three jobs:

1. Define a sane **public MVP**.
2. Preserve the **full long-term roadmap** so the project keeps expanding over time.
3. Attach each phase to an **article milestone** so the public build story grows cleanly instead of turning into a pile of disconnected experiments.

This is not a “do only the MVP and stop” plan. It is a **full roadmap with an MVP cut through it**.

## Project Thesis

Build a local-LLM virtual creature game that is strong enough to work as:

- a real backend-heavy AI product
- a showcase repo for AI engineering hiring loops
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
- reranking enabled in the default path
- LangChain in the default shipped path
- optional thin LangGraph per-dimart flow
- LangSmith traces
- early benchmark and evaluation suite

### v1 Non-Goals

- full civilization simulation
- full multi-agent supervisor graphs
- multimodal perception in the main shipped path
- LoRA or QLoRA in the main shipped path
- embedding fine-tuning in the main shipped path
- NeMo Guardrails as a hard requirement for the first release
- MLflow or W&B as a hard requirement for the first release

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

**Preserved Work**

- architecture explanation
- module boundaries
- explicit tradeoff documentation

**Article**

- Article 0: “How I’m structuring this repo so I can compare AI techniques without creating a mess”

### Phase 1: Streaming Backend, Local Model, and First Conversation Loop

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

**Preserved Work**

- async streaming architecture
- API-first design
- client-agnostic transport boundary
- model loader abstraction
- quantization benchmark notebook
- tokenizer deep-dive notebook

**Comparison Tracks**

- GGUF vs GPTQ vs AWQ
- TTFT and throughput benchmarks
- prompt composition variants

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

**Preserved Work**

- multi-creature communication as a core part of the concept
- society and population visibility from the beginning

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

**Preserved Work**

- async SQLAlchemy
- Postgres as serious production-style state store
- structured vs unstructured data split

**Comparison Tracks**

- synchronous vs deferred indexing
- schema choices for event history and conversation persistence

**Article**

- Article 3: “Postgres for truth, Qdrant for memory: drawing the line correctly”

### Phase 4: Retrieval Foundation

**Goal**

Make dimarts remember correctly and measurably.

**Build**

- embeddings
- chunking strategies
- dense retrieval
- BM25 retrieval
- fusion
- reranking in the default path
- retrieval metrics

**Preserved Work**

- fixed-size chunking
- sentence-boundary chunking
- semantic chunking
- hybrid search
- cross-encoder reranking
- debug visibility into ranking changes

**Comparison Tracks**

- dense-only vs hybrid
- reranker on vs off
- chunking strategy comparisons
- embedding model comparisons
- metadata filtering
- HyDE
- late interaction
- GraphRAG as an advanced retrieval branch

**Article**

- Article 4: “Hybrid retrieval and reranking for dimart memory”

### Phase 5: Evaluation, Regression, and Observability

**Goal**

Make improvements measurable and regressions visible.

**Build**

- LangSmith tracing
- benchmark harness
- evaluation datasets
- retrieval metrics
- pairwise comparison reports
- response-quality regression suite
- structured logs
- `/metrics` endpoint

**Preserved Work**

- DeepEval and RAGAS integration
- LLM-as-judge
- pairwise comparisons
- IR metrics like MRR, NDCG, Recall@K
- run-level comparisons
- trace screenshots and benchmark tables in README

**Comparison Tracks**

- baseline vs reranked pipeline
- baseline vs fine-tuned retrieval later
- prompt version A/B tests

**Article**

- Article 5: “How I evaluate and trace an AI system instead of just eyeballing it”

### Phase 6: Safety and Hardening

**Goal**

Add the safety layer that interviewers expect to hear about.

**Build**

- input sanitization
- prompt-injection checks
- moderation boundary
- sensitive-data handling
- output filtering policy
- sandboxing for any dimart actions

**Preserved Work**

- PII masking
- jailbreak and injection handling
- data leakage prevention
- action sandboxing
- guardrails as an explicit design concern

**Comparison Tracks**

- regex + heuristic sanitization
- embedding-based injection detection
- NeMo Guardrails integration

**Article**

- Article 6: “Guardrails, sanitization, and action sandboxing in a local AI game”

### Phase 7: Context and Cost Optimization

**Goal**

Improve quality and control costs without changing the product surface.

**Build**

- context pruning
- summarization policy
- prompt and memory token budgets
- selective caching for deterministic artifacts
- explicit latency budgets

**Preserved Work**

- hierarchical summarization
- dynamic retrieval from history
- lost-in-the-middle mitigation
- semantic cache
- model routing
- request batching where it actually helps

**Comparison Tracks**

- pruning strategies
- summarization thresholds
- cache hit quality impact
- routing small vs large models by request type

**Article**

- Article 7: “Context pruning, summarization, and cost control without wrecking quality”

### Phase 8: Agent Architecture Upgrades

**Goal**

Expand from a thin flow to richer agentic patterns once the core system is stable.

**Build**

- thin per-dimart LangGraph flow if not already present
- explicit checkpointing
- structured output boundaries
- memory-aware planning hooks

**Preserved Work**

- reflection loops
- checkpointers
- agentic memory
- planning and execution
- structured output
- architecture tradeoffs
- reasoning traces

**Comparison Tracks**

- plain orchestrator vs LangGraph
- reflection on vs off
- HITL review checkpoints
- tool-calling flows

**Protocol and Integration Extensions**

- MCP integration surface
- gRPC exploration
- A2A notes and positioning

**Article**

- Article 8: “Where LangGraph actually helps, and where plain orchestration is better”

### Phase 9: Self-Hosted Inference Backends

**Goal**

Cover the model-serving depth that comes up in interviews without turning the whole project into infra theatre.

**Build**

- inference experiment track
- backend abstraction for alternate runtimes

**Preserved Work**

- vLLM exploration
- SGLang exploration
- paged attention notes
- static and dynamic batching
- speculative decoding
- inference balancing
- quantization comparisons

**Comparison Tracks**

- llama.cpp-style local runtime vs vLLM
- batching impact on latency and throughput
- speculative decoding impact

**Article**

- Article 9: “How much inference-backend depth a backend-focused AI engineer actually needs”

### Phase 10: Fine-Tuning and ML/NLP Depth

**Goal**

Preserve the original ML depth work as later, explicit tracks instead of forcing it into v1.

**Build**

- synthetic dialogue dataset pipeline
- LoRA and QLoRA track
- embedding fine-tuning track
- experiment tracking for training runs

**Preserved Work**

- model architectures and tradeoffs
- tokenizers and tokenizer analysis
- optimization methods and model metrics
- fine-tuning
- embedding fine-tuning
- distillation as a later experiment

**Comparison Tracks**

- base model vs LoRA persona model
- base embeddings vs fine-tuned embeddings
- distilled small model vs larger baseline

**Article**

- Article 10: “Fine-tuning, embeddings, and what should stay out of the MVP”

### Phase 11: Multimodal and Advanced Retrieval

**Goal**

Preserve the multimodal and retrieval-breadth work from the original roadmap.

**Build**

- multimodal experiment branch
- image input to dimarts
- visual memory indexing

**Preserved Work**

- multimodal search
- multimodal indexation
- CLIP-style unified spaces
- VLM integration

**Comparison Tracks**

- text-only vs multimodal retrieval
- caption-based indexing vs unified embedding approaches

**Article**

- Article 11: “Adding multimodal memory without breaking the retrieval story”

### Phase 12: Richer Society and Multi-Agent Expansion

**Goal**

Extend the 5-dimart tribe into a deeper social system after the fundamentals are stable.

**Build**

- richer tribe behavior
- broader inter-dimart orchestration
- optional supervisor graphs
- more autonomous social loops

**Preserved Work**

- multi-agent orchestration
- richer planning/execution
- larger-scale society simulation

**Comparison Tracks**

- thin coordinator vs supervisor graph
- explicit turn-taking vs emergent scheduling

**Article**

- Article 12: “Scaling the tribe into a real society”

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
   - primary phases: 1, 9, 10
   - terms: embeddings, tokenizers, fine-tuning, distillation, optimization, metrics
2. **Retrieval**
   - primary phases: 4, 11
   - terms: chunking, hybrid search, metadata filtering, HyDE, GraphRAG, reranking, cross-encoding, late interaction, metrics
3. **Protocols**
   - primary phases: 1, 2, 8
   - terms: WS, SSE, gRPC, MCP, A2A
4. **Agent architecture**
   - primary phases: 2, 8, 12
   - terms: HITL, reflection, checkpointing, agentic memory, multi-agent orchestration, planning and execution, structured output
5. **Safety**
   - primary phases: 6
   - terms: sanitizing, guardrails, moderation, jailbreaks, injections, data leakage, sandboxing
6. **Cost reduction**
   - primary phases: 7, 9
   - terms: semantic cache, model routing, batching
7. **Context optimization**
   - primary phases: 7
   - terms: pruning, lost in the middle, summarization
8. **Self-hosted backends**
   - primary phases: 1, 9
   - terms: vLLM, SGLang, paged attention, speculative decoding, batching, quantization, inference balancing
9. **Frameworks**
   - primary phases: 1, 4, 8
   - terms: LangChain, LangGraph, DSPy, LlamaIndex
10. **Testing agent and RAG systems**
   - primary phases: 5
   - terms: DeepEval, LLM-as-judge, pairwise comparison, RAGAS, CI-style regression
11. **Observability**
   - primary phases: 5, 9
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
