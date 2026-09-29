# genpark-streaming-markdown-code-block-tracker-skill

Real-time state machine tracking unclosed markdown code fences, language tags, and formatting delimiters to prevent broken rendering in streaming chat interfaces.

## Architecture

```mermaid
flowchart TD
    Chunk[Stream Chunk] --> Tracker[StreamingMarkdownTracker]
    Tracker --> Scanner[Triple & Single Backtick Parser]
    Scanner --> State{Inside Code Block?}
    State -->|Yes| AutoClose[Synthesize Closing Backticks]
    State -->|No| Passthrough[Passthrough Clean Markdown]
```

## Features
- **Auto-Closure Synthesis**: Guarantees syntax highlighters always receive closed code blocks.
- **Language Detection**: Extracts programming language specifiers.
- **Pure Python**: 100% Standard Library.
