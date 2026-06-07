# ADR-0000: `<short decision description>`
This file (ADR-0000) is the template. The heading should be replaced with the decision itself, e.g. "ADR-0001: Clean Architecture layout for the project".

## Date
YYYY-MM-DD

## Status
Allowed values: Proposed | Accepted | Deprecated | Superseded.
When Superseded, link the ADR that replaces it (e.g. "Superseded by ADR-0007").

## Context
What forces this decision now — the constraint, problem, or pressure that makes doing nothing untenable. Describe the situation, not the solution.

## Decision
What was chosen, stated as a commitment ("We will …") in one or two sentences. The justification lives in Context and Consequences, not here.

## Alternatives considered
Each alternative with a one-line "why not".

## Consequences
What this decision makes easier and what it makes harder. List both - name the concrete workflows, layers, or future options affected, not generic trade-offs. A decision with only upside listed is usually under-examined; the cost side is the load-bearing part.

## Re-baseline impact
The project tracks multiple metrics (e.g. latencies of various LangGraph steps). Specify which of the project's tracked benchmark numbers this decision is expected to move, and in which direction/by roughly how much — or "none" if the decision is purely structural.

## Reversal trigger
Enumerate the conditions under which you would reverse, rethink, or supersede this decision. These have to be observable signals, not vague/ambiguous.
