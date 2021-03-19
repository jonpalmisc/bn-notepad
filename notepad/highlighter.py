from typing import List

from PySide2.QtGui import QTextDocument, QSyntaxHighlighter, QTextCharFormat, QFont
from PySide2.QtCore import QRegularExpression


class JHighlightRule:
    """A syntax highlighting rule, composed of a pattern and style."""

    pattern: QRegularExpression
    style: QTextCharFormat

    def __init__(self, pattern: QRegularExpression, style: QTextCharFormat):
        self.pattern = pattern
        self.style = style


def _get_default_rules(point_size: int) -> List[JHighlightRule]:
    """
    Provides a list of default Markdown highlighting rules.

    :param point_size: the base point size to use for headings
    """

    rules: List[JHighlightRule] = []

    heading_patterns = [
        "(?m)^#{3}(?!#)(.*)",
        "(?m)^#{2}(?!#)(.*)",
        "(?m)^#(?!#)(.*)",
    ]

    # Add bold heading styles with exponentially increasing font size.
    for i in range(len(heading_patterns)):
        s = QTextCharFormat()
        s.setFontWeight(QFont.Bold)
        s.setFontPointSize(point_size * pow(1.2, (i + 1)))

        rules.append(JHighlightRule(QRegularExpression(heading_patterns[i]), s))

    return rules


class JMarkdownHighlighter(QSyntaxHighlighter):
    """
    Custom syntax highlighter for a subset of Markdown.
    """

    rules: List[JHighlightRule] = []

    def __init__(self, document: QTextDocument, point_size: int):
        super().__init__(document)

        self.rules = _get_default_rules(10)

    def highlightBlock(self, text: str):
        """Callback to highlight a block of text."""

        for r in self.rules:
            mi = r.pattern.globalMatch(text)
            while mi.hasNext():
                m = mi.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), r.style)
