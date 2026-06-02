alias v := verify

verify:
    uv run ruff check .
    uv run pyright
    just test

test:
    uv run pytest
