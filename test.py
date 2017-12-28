import markdown

from mdx_mathjax import MathJaxExtension


md = markdown.Markdown(extensions=[MathJaxExtension()])


htmls = [
    '\( x + y = z \)',
    '$$ a+ b = c $$',
    '\[ x + y = z \]',
    '\` x + y = z \`',
]

for html in htmls:
    print(md.convert(html))
