FROM futureys/claude-code-python-development:20260515203000
COPY pyproject.toml /workspace/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
COPY . /workspace/
CMD ["invoke", "test.coverage"]
