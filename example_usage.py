from client import StreamingMarkdownTracker

tracker = StreamingMarkdownTracker()
tracker.feed("Here is the solution:\n```python\ndef add(a, b):\n    return a + b")
print("State:", tracker.feed(""))
print("Safe Rendered Output:\n" + tracker.safe_render())
