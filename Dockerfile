FROM futureys/claude-code-python-development:20260407212500
COPY pyproject.toml /workspace/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --python 3.13
COPY . /workspace/
CMD ["invoke", "test.coverage"]
