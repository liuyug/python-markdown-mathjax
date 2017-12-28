# -*- coding: utf-8 -*-
# based on mitya57/python-markdown-math

from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
from markdown.util import AtomicString, etree


class MathJaxExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'add_preview': [False, 'Add a preview node before each math node'],
        }
        super(MathJaxExtension, self).__init__(*args, **kwargs)

    def _get_content_type(self, delimiter):
        if delimiter == '\`':
            return 'math/asciimath'
        elif delimiter in ['$$', '\\(', '\\[']:
            return 'math/tex'

    def extendMarkdown(self, md, md_globals):
        def _wrap_node(node, preview_text, wrapper_tag):
            if not self.getConfig('add_preview'):
                return node
            preview = etree.Element('span', {'class': 'MathJax_Preview'})
            preview.text = AtomicString(preview_text)
            wrapper = etree.Element(wrapper_tag)
            wrapper.extend([preview, node])
            return wrapper

        def handle_match_inline(m):
            node = etree.Element('script')
            node.set('type', self._get_content_type(m.group(2)))
            node.text = AtomicString(m.group(3))
            return _wrap_node(node, ''.join(m.group(2, 3, 4)), 'span')

        def handle_match(m):
            node = etree.Element('script')
            node.set('type', '%s; mode=display' % self._get_content_type(m.group(2)))
            node.text = AtomicString(m.group(3))
            return _wrap_node(node, ''.join(m.group(2, 3, 4)), 'div')

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
