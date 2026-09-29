"""Streaming Markdown Code Block Tracker.
100% Python Standard Library.
"""

import re

class StreamingMarkdownTracker:
    """State-machine tracking unclosed code blocks and formatting in live streaming text."""
    def __init__(self):
        self.in_code_block = False
        self.current_language = ""
        self.in_inline_code = False
        self.full_text = ""

    def feed(self, chunk: str) -> dict:
        self.full_text += chunk
        
        ticks = [m.start() for m in re.finditer(r'```', self.full_text)]
        if len(ticks) % 2 == 1:
            self.in_code_block = True
            last_tick_pos = ticks[-1]
            tail = self.full_text[last_tick_pos + 3:]
            newline_pos = tail.find('\n')
            if newline_pos != -1:
                self.current_language = tail[:newline_pos].strip()
            else:
                self.current_language = tail.strip()
        else:
            self.in_code_block = False
            self.current_language = ""

        if not self.in_code_block:
            single_ticks = len(re.findall(r'(?<!`)`(?!`)', self.full_text))
            self.in_inline_code = (single_ticks % 2 == 1)
        else:
            self.in_inline_code = False

        closure = ""
        if self.in_code_block:
            closure = "\n```"
        elif self.in_inline_code:
            closure = "`"

        return {
            "in_code_block": self.in_code_block,
            "language": self.current_language,
            "in_inline_code": self.in_inline_code,
            "suggested_closure": closure
        }

    def safe_render(self) -> str:
        status = self.feed("")
        return self.full_text + status["suggested_closure"]
