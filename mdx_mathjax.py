# -*- coding: utf-8 -*-
# based on mitya57/python-markdown-math

import re

from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
from markdown.util import AtomicString, etree


class MathJaxExtension(Extension):
    asciimath_delimiters = ('\\`',)
    latexmath_delimiters = ('$$', '\\(', '\\[')
    regex_escape = re.compile(r'\\(.)')

    def __init__(self, *args, **kwargs):
        self.config = {
            'add_preview': [False, 'Add a preview node before each math node'],
            'latexmath_escape': [False, 'Process LatexMath Escape "\\"'],
            'asciimath_escape': [False, 'Process AsciiMath Escape "\\"'],
        }
        super(MathJaxExtension, self).__init__(*args, **kwargs)

    def _fix_html_entites(self, text):
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def _fix_latex(self, text):
        text = text.replace('<', '\lt')
        text = text.replace('>', '\gt')
        return text

    def _process_escape(self, text):
        return self.regex_escape.sub(r'\1', text)

    def _get_content_type(self, delimiter):
        if delimiter in self.asciimath_delimiters:
            return 'math/asciimath'
        elif delimiter in self.latexmath_delimiters:
            return 'math/tex'

    def extendMarkdown(self, md, md_globals):
        def _wrap_node(node, preview_text, wrapper_tag):
            if not self.getConfig('add_preview'):
                return node
            preview = etree.Element('span', {'class': 'MathJax_Preview'})
            wrapper = etree.Element(wrapper_tag)
            wrapper.extend([preview, node])
            return wrapper

        def handle_match_inline(m):
            node = etree.Element('script')
            node.set('type', self._get_content_type(m.group(2)))
            if m.group(2) in self.asciimath_delimiters:
                text = self._fix_html_entites(m.group(3))
                if self.getConfig('asciimath_escape'):
                    node.text = AtomicString(self._process_escape(text))
                else:
                    node.text = AtomicString(text)
            elif m.group(2) in self.latexmath_delimiters:
                text = self._fix_latex(m.group(3))
                if self.getConfig('latexmath_escape'):
                    node.text = AtomicString(self._process_escape(text))
                else:
                    node.text = AtomicString(text)
            else:
                text = m.group(3)
                node.text = AtomicString(text)
            return _wrap_node(node, m.group(2) + text + m.group(4), 'span')

        def handle_match(m):
            node = etree.Element('script')
            node.set('type', '%s; mode=display' % self._get_content_type(m.group(2)))
            if m.group(2) in self.asciimath_delimiters:
                text = self._fix_html_entites(m.group(3))
                if self.getConfig('asciimath_escape'):
                    node.text = AtomicString(self._process_escape(text))
                else:
                    node.text = AtomicString(text)
            elif m.group(2) in self.latexmath_delimiters:
                text = self._fix_latex(m.group(3))
                if self.getConfig('latexmath_escape'):
                    node.text = AtomicString(self._process_escape(text))
                else:
                    node.text = AtomicString(text)
            else:
                text = m.group(3)
                node.text = AtomicString(text)
            return _wrap_node(node, m.group(2) + text + m.group(4), 'div')

        inline_patterns = (
            Pattern(r'(?<!\\)(\\\()(.+?)(\\\))'),     # MathJax   \(...\)
            Pattern(r'(?<!\\)(\\`)(.+?)(\\`)'),       # AsciiMath \`...\`
        )
        patterns = (
            Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'),  # MathJax   $$...$$
            Pattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),     # MathJax   \[...\]
            Pattern(r'(?<!\\)(\\`)(.+?)(\\`)'),       # AsciiMath \`...\`
        )
        for i, pattern in enumerate(patterns):
            pattern.handleMatch = handle_match
            md.inlinePatterns.add('mathjax-%d' % i, pattern, '<escape')
        for i, pattern in enumerate(inline_patterns):
            pattern.handleMatch = handle_match_inline
            md.inlinePatterns.add('mathjax-inline-%d' % i, pattern, '<escape')


def makeExtension(*args, **kwargs):
    return MathJaxExtension(*args, **kwargs)
