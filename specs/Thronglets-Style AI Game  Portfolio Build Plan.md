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
- a long-running simulation where dimarts can develop private intentions, social dynamics, and emergent institutions over time

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

### Simulation Doctrine

The long-term product is not just a reactive chat system. It is a simulation.

**Long-term target (full product):**

- world rules and the simulation engine are authoritative
- the model proposes beliefs, intentions, interpretations, plans, and speech
- the world engine applies consequences and state transitions
- dimarts have private state that is separate from public speech
- dimarts may act without player input through autonomous ticks
- players can influence the world, but the simulation should not depend on constant external control
- the system should avoid hardcoded narrative beats and instead rely on rules, resources, incentives, and social dynamics
- later phases may allow dimarts to revise their worldview and possibly form beliefs about hidden world constraints or the nature of the simulation itself

**v1 subset (what actually ships after Phase 6):**

- world rules and simulation engine are authoritative
- private-state schema exists, but beliefs/intentions/plans are filled by heuristic stubs rather than model cognition
- LLM-generated speech is player-driven; autonomous ticks mutate world/relationship state and emit events without generating dialogue
- world engine applies consequences and state transitions
- simulation runs independently of constant player input, via heuristic autonomous ticks
- epistemic revision and hidden-constraint reasoning are explicitly deferred to Phase 8+

## Canonical Turn Lifecycle

Every player-driven or autonomous system turn should follow the same high-level flow:

1. advance simulation clock and select the next player or autonomous stimulus
2. load authoritative world, tribe, relationship, and private dimart state from Postgres
3. build turn context
4. retrieve candidate memories
5. update hidden belief, goal, and social state
6. rerank retrieved candidates and assemble prompt context
7. decide action plan and public utterance strategy
8. generate and stream public output when needed
9. apply world consequences through the simulation engine
10. persist public and private state deltas
11. update derived memory index and emit tribe and world events

In v1, steps 5 and 7 are heuristic stubs that read and write the Phase 3 private-state schema using rules rather than LLM cognition. LLM-driven belief revision, goal formation, and utterance-strategy selection land in Phase 8 and replace those stubs without changing the surrounding lifecycle.

Every turn should be traceable with explicit states:

- `pending`
- `retrieving`
- `generating`
- `streaming`
- `completed`
- `partial`
- `failed`
- `cancelled`

## Tribe Model (v1)

The project starts with a constrained tribe. These constraints apply to v1 only:

- exactly 5 dimarts
- fixed roster
- distinct personalities and roles
- shared world state
- individual memory and dialogue state
- private belief and intention state
- visible dimart-to-dimart communication
- no breeding in v1
- no procedural population explosion in v1
- player intervention is possible, but the tribe should also evolve through autonomous ticks

Phase 13 relaxes these constraints.

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
- WebSocket transport (single-channel, connection lifecycle, heartbeats)
- Typer CLI client
- local model integration
- GGUF as default runtime
- LangChain prompt composition and streaming
- model loader abstraction

**Comparison Tracks**

- runtime format: llama.cpp/GGUF defaults and measurement setup (quantization method comparisons deferred to Phase 10)
- TTFT and throughput benchmarks
- prompt composition variants

**Article**

- Article 1: “Streaming a local LLM through FastAPI, SSE, and a CLI client”

### Phase 2: Dimart Tribe, Simulation Clock, and Social Event Layer

**Goal**

Expand from one dimart to the 5-dimart tribe and make the world feel alive even when the player is not driving every move.

**Build**

- 5 fixed dimarts
- tribe state
- PostgreSQL bootstrap + Alembic migrations for tribe and event tables
- `SocietyCoordinator`
- simulation clock or tick loop
- off-turn dimart activity
- lightweight scheduler for autonomous turns
- inter-dimart event model
- tribe/world event schemas and fan-out over the Phase 1 WebSocket transport
- minimal resource, need, and relationship updates over time

Autonomous ticks in this phase are rule- and heuristic-driven only; no LLM cognition, belief, or planning. They mutate world and relationship state and emit events, but they do not generate LLM dialogue — autonomous speech is gated until the Phase 8 cognition flow replaces the heuristic stubs. LLM-generated dialogue in v1 is therefore player-driven only. Belief/intention schemas land in Phase 3, cognition in Phase 8.

Turn records in this phase live inside the event log; an explicit `TurnStore` adapter is introduced in Phase 3 when Postgres gains world and turn tables.

**Comparison Tracks**

- event schemas
- push vs pull event delivery patterns
- protocol notes for WS/SSE split
- player-driven vs autonomous event cadence

**Article**

- Article 2: “From one dimart to a 5-dimart tribe with a simulation clock”

### Phase 3: World Model, Persistence, and Hidden State

**Goal**

Introduce persistent game state, hidden state, and memory storage cleanly.

**Build**

- extend Postgres schema for authoritative world and turn data (tribe/event tables already exist from Phase 2)
- raw memory records stored in Postgres (Qdrant is not introduced until Phase 4, alongside the retrieval pipeline that actually uses it)
- relationship graph or equivalent social-state model
- resource and world-state tables
- event log with causal history
- private belief, intention, mood, and suspicion/worldview state
- explicit separation between public utterance history and private internal state
- turn persistence

**Comparison Tracks**

- schema choices for event history and conversation persistence
- snapshot vs event-log approaches for hidden-state reconstruction

**Article**

- Article 3: “World truth, hidden state, and memory: drawing the line correctly”

### Phase 4: Retrieval Baseline

**Goal**

Make dimarts remember correctly and measurably.

**Build**

- embeddings
- chunking strategies
- Qdrant introduced here: indexing pipeline consuming the Phase 3 Postgres raw-memory store
- synchronous vs deferred indexing policy
- dense retrieval
- BM25 retrieval
- fusion
- metadata filtering
- reranking in the default path
- offline spot-check retrieval metrics

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

Make improvements measurable and regressions visible before the public release, including the simulation aspects.

**Build**

- LangSmith tracing
- DeepEval integration
- RAGAS integration
- evaluation datasets
- retrieval metrics in the CI regression harness (LangSmith + RAGAS)
- pairwise comparison reports
- LLM-as-judge reports
- response-quality regression suite
- structured logs
- `/metrics` endpoint
- simple monitoring dashboards or SLO-style latency documentation
- long-horizon consistency checks
- relationship and social-coherence checks
- causal-consistency checks over event chains
- seeded simulation runs and replay-friendly debug traces
- autonomy-rate measurements for player-idle periods

**Comparison Tracks**

- baseline vs reranked pipeline
- baseline vs fine-tuned retrieval later
- prompt version A/B tests
- seeded vs unseeded simulation behavior analysis

**Article**

- Article 6: “How I evaluate, trace, and monitor an evolving AI simulation instead of just eyeballing it”

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

**Re-baseline note**

- Phase 7 optimizes the v1 flat-orchestration flow. Once Phase 8 introduces LangGraph cognition and per-dimart graph flows, cache keys, routing heuristics, and batching assumptions must be re-measured against the new call pattern. Treat Phase 7 numbers as a v1 baseline, not a permanent target.

**Article**

- Article 7: “Reducing cost without wrecking quality”

### Phase 8: Simulation Cognition and Agent Architecture

**Goal**

Expand from a thin orchestration flow to richer agentic patterns once the core system is stable.

**Build**

- thin per-dimart LangGraph flow (introduced here; v1 shipped without it)
- reflection
- explicit checkpointing
- structured output boundaries
- memory-aware planning hooks
- structured internal state for beliefs, goals, plans, and utterance strategy
- explicit distinction between private intention and public expression
- tool-calling flows for dimart actions
- sandboxing for dimart actions
- reasoning traces
- HITL checkpoints
- anomaly-detection and belief-revision hooks for later epistemic development

**Comparison Tracks**

- plain orchestrator vs LangGraph
- reflection on vs off
- HITL on vs off
- tool-calling flows
- private/public state separation strategies

**Article**

- Article 8: “Where agent cognition, reflection, and private state actually help”

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
- tokenizer deep-dive notebook and tokenizer analysis
- optimization-method notes and metrics

**Comparison Tracks**

- base model vs LoRA persona model
- base embeddings vs fine-tuned embeddings
- off-the-shelf small model vs larger baseline

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

### Phase 13: Open-Ended Society Simulation and Multi-Agent Expansion

**Goal**

Extend the 5-dimart tribe into a genuinely evolving social simulation after the fundamentals are stable.

**Build**

- richer tribe behavior
- broader inter-dimart orchestration
- optional supervisor graphs
- more autonomous social loops
- larger society simulation
- faction formation, splitting, and merging
- breeding or reproduction systems
- cooperation, betrayal, conflict, and death as simulation outcomes
- long-running evolution with optional player intervention rather than constant player control
- epistemic-development track where dimarts may revise beliefs about hidden world constraints or the nature of their reality

**Comparison Tracks**

- thin coordinator vs supervisor graph
- explicit turn-taking vs emergent scheduling
- fixed population vs evolving population dynamics

**Article**

- Article 13: “Scaling the tribe into an open-ended society simulation”

## Test Strategy Across All Phases

Testing is not a late phase. Every phase should extend the same test pyramid:

- **unit tests**
  - domain rules
  - ranking math
  - context logic
  - event shaping
  - hidden-state transitions
  - simulation-rule application
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
  - long-horizon social consistency
  - autonomy behavior in player-idle windows
- **limited end-to-end**
  - one player-to-dimart happy path
  - one tribe-event path
  - one autonomous-tick evolution path

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
- contradictory private/public state updates
- runaway autonomous loops

## Performance Strategy Across All Phases

The benchmark story should stay consistent across the roadmap.

Always track:

- retrieval latency
- reranking latency
- prompt assembly latency
- simulation tick latency
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
   - primary phases: 1, 11
   - terms: embeddings, tokenizers, fine-tuning, distillation, optimization, metrics
2. **Retrieval**
   - primary phases: 4, 12
   - terms: chunking, hybrid search, metadata filtering, HyDE, GraphRAG, reranking, cross-encoding, late interaction, metrics
3. **Protocols**
   - primary phases: 1, 2, 9
   - terms: WS, SSE, gRPC, MCP, A2A
4. **Agent architecture**
   - primary phases: 8, 13
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
   - primary phases: 6, 10, 13
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

## Reading Materials by Phase

### Reading Principles

- Keep backend transport reading shallow and implementation-oriented.
- Go deeper on AI-heavy topics: retrieval, ranking, context management, safety, evaluation, inference runtimes, and fine-tuning.
- Prefer official docs and primary papers over generic blog posts.
- Do not pre-read later-phase material just because it looks interesting. Read by phase.
- For comparison tracks, read the default-path material first, then the paper or alternative framework docs only when the comparison begins.

### Phase 0: Foundations, Repo Boundaries, and Default Flow

**Required**

- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)

**Why this first**

- Use the Anthropic article as the grounding piece for why the repo should start with simple workflows, explicit boundaries, and only later earn more agentic complexity. LangGraph reading is spread across Phases 1, 3, and 8, each time paired with the concrete capability it is being used for.

### Phase 1: Streaming Backend and Local Runtime

**Required**

- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [FastAPI custom responses and `StreamingResponse`](https://fastapi.tiangolo.com/advanced/custom-response/)
- [LangChain streaming](https://docs.langchain.com/oss/python/langchain/streaming)
- [LangGraph streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

**Notes**

- The backend material here is intentionally short.
- Tokenizer reading is deferred to Phase 11, where the tokenizer deep-dive notebook and fine-tuning work actually live.

### Phase 2: Dimart Tribe, Simulation Clock, and Social Event Layer

**Required**

- [SQLAlchemy asyncio](https://docs.sqlalchemy.org/20/orm/extensions/asyncio.html)
- [Alembic tutorial](https://alembic.sqlalchemy.org/tutorial.html)

**Optional but useful later in the phase**

- [Mesa documentation](https://mesa.readthedocs.io/en/latest/)

**Notes**

- Phase 2 is mostly application design, scheduler design, and simulation rules.
- Mesa is not required for implementation, but it is a useful agent-based-simulation reference once the tribe starts acting autonomously.

### Phase 3: World Model, Persistence, and Hidden State

**Required**

- [Qdrant Python client docs](https://python-client.qdrant.tech/)
- [Qdrant quickstart](https://python-client.qdrant.tech/quickstart.html)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph checkpointer reference](https://reference.langchain.com/python/langgraph/checkpoints/)

**Notes**

- Read Qdrant for concrete storage/index APIs.
- Read LangGraph persistence/checkpoint docs for the later hidden-state and checkpointing work, even if LangGraph stays optional in the shipped v1 path.

### Phase 4: Retrieval Baseline

**Required**

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://huggingface.co/papers/2005.11401)
- [SentenceTransformers documentation](https://www.sbert.net/index.html)
- [Retrieve and Re-Rank pipeline guide](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)
- [Qdrant hybrid search article](https://qdrant.tech/articles/hybrid-search/)

**Read when each comparison starts**

- [Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)](https://huggingface.co/papers/2212.10496)

**Why this phase gets extra reading**

- This is one of the most interview-dense topics and one of the most valuable showcase areas in the repo.
- The paper gives you the conceptual base for RAG.
- SentenceTransformers gives you the practical base for embeddings, retrievers, cross-encoders, and rerankers.

### Phase 5: Safety and Context Baseline

**Required**

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Microsoft Presidio getting started](https://microsoft.github.io/presidio/getting_started/)
- [Presidio text de-identification](https://microsoft.github.io/presidio/getting_started/getting_started_text/)
- [NeMo Guardrails overview](https://docs.nvidia.com/nemo/guardrails/latest/about/overview.html)

**Context-management add-ons**

- [LangChain middleware overview](https://docs.langchain.com/oss/python/langchain/middleware/overview)

**Notes**

- This phase is not just about security theater.
- Read OWASP first for threat categories, then Presidio for concrete PII handling, then NeMo Guardrails for programmable guardrail patterns.

### Phase 6: Evaluation, Tracing, and Monitoring

**Required**

- [LangSmith docs](https://docs.smith.langchain.com/)
- [Ragas docs](https://docs.ragas.io/)
- [DeepEval GitHub README](https://github.com/confident-ai/deepeval)

**Optional when you start scaling comparisons**

- [Ragas experimentation concepts](https://docs.ragas.io/en/stable/concepts/experimentation/)

**Notes**

- This phase is where you move from “it feels better” to “I can prove what improved.”
- LangSmith is the primary trace/debug layer.
- Ragas and DeepEval give you the eval vocabulary and mechanics for retrieval and answer quality.

### Phase 7: Cost Optimization

**Required**

- No large external reading pack by default.

**What to use instead**

- Your own traces, latency tables, token usage tables, and benchmark outputs from Phases 4-6.

**Notes**

- This phase should be measurement-driven, not blog-driven.
- Only pull in extra reading if a concrete optimization experiment forces it.

### Phase 8: Simulation Cognition and Agent Architecture

**Required**

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [LangChain structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph checkpointer reference](https://reference.langchain.com/python/langgraph/checkpoints/)

**Notes**

- The LangGraph overview was deferred from Phase 0 to here — this is where the graph layer actually lands.
- Come back to the Anthropic article here with more experience; it reads differently once you already have a working system.
- Structured output and checkpointing are the practical base for private state, HITL, and explicit internal/public separation.

### Phase 9: Protocols and Framework Comparisons

**Required**

- [Model Context Protocol overview](https://modelcontextprotocol.io/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18/basic)
- [Model Context Protocol SDK docs](https://modelcontextprotocol.io/docs/sdk)
- [gRPC documentation](https://grpc.io/docs/)
- [DSPy docs](https://dspy.ai/)
- [LlamaIndex workflows](https://docs.llamaindex.ai/en/stable/workflows/)

**Optional**

- [A2A protocol docs](https://www.a2aprotocol.org/en/docs)

**Notes**

- Because you already feel comfortable with pure backend protocol concepts, keep this phase narrow and comparison-focused.
- The point here is signaling and tradeoff literacy, not turning the repo into five competing transport stacks.

### Phase 10: Self-Hosted Inference Backends

**Required**

- [vLLM quickstart](https://docs.vllm.ai/en/stable/getting_started/quickstart.html)

**Optional**

- [SGLang documentation](https://docs.sglang.ai/)

**Notes**

- vLLM is the must-read runtime because it maps directly to the phase’s required implementation.
- SGLang is the useful contrast (speculative decoding, quantization, LoRA serving, structured outputs, observability) — read only if you actually pick up the Optional SGLang extension in this phase.

### Phase 11: Fine-Tuning and ML/NLP Depth

**Required**

- [Hugging Face Tokenizers docs](https://huggingface.co/docs/tokenizers/en/index)
- [PEFT docs](https://huggingface.co/docs/peft/en/index)
- [SentenceTransformers training overview](https://www.sbert.net/docs/training/overview.html)
- [Cross-encoder training overview](https://www.sbert.net/docs/cross_encoder/training_overview.html)

**Optional**

- [TRL docs](https://huggingface.co/docs/trl/en/index)

**Notes**

- This extends the Phase 1 HF Tokenizers quicktour — skim only the sections you didn't touch earlier.
- This is where the ML-depth reading really starts.
- If you stay with LoRA/QLoRA and embedding/reranker tuning, PEFT plus SentenceTransformers is the right core.
- Only add TRL if you truly start doing preference-style or policy-style training work.

### Phase 12: Advanced Retrieval and Multimodal

**Required**

- [ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://huggingface.co/papers/2004.12832)
- [GraphRAG project page](https://www.microsoft.com/en-us/research/project/graphrag/)
- [SentenceTransformers docs](https://www.sbert.net/index.html)

**Notes**

- Phase 12 is intentionally later because it is easy to sink time into retrieval sophistication before the baseline is stable.
- ColBERT gives you the late-interaction grounding.
- GraphRAG gives you the graph-oriented retrieval branch.

### Phase 13: Open-Ended Society Simulation and Multi-Agent Expansion

**Required**

- Re-read the project’s own simulation doctrine and article notes first.

**Useful external reference**

- [Mesa documentation](https://mesa.readthedocs.io/en/latest/)
- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)

**Notes**

- By this phase, your most valuable reading should be your own design docs, traces, and eval results.
- External reading helps with simulation patterns and orchestration tradeoffs, but the hard work here is system design and observation, not library API memorization.

## Reading Cut Rules

- If you are not currently implementing or benchmarking a comparison track, skip its paper.
- If a phase is backend-heavy and AI-light, read the docs once and move on.
- If a phase is retrieval-, safety-, eval-, inference-, or tuning-heavy, budget extra time for the reading before writing code.
- When in doubt, choose one practical doc plus one grounding paper over five medium-quality tutorials.
