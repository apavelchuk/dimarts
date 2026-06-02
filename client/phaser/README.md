# Phaser Client

This directory contains the Phaser browser client.

The client - is a presentation adapter. It renders backend state and emits player commands, but it does not decide simulation outcomes.

## Boundary

- The Phaser client is the public browser surface for visible dimart interaction and world-event rendering.
- Backend APIs, events, and streams are the source of truth for state, turn status, dialogue, movement, resources, and relationships.

## Rationale

<ADR-PLACEHOLDER>
