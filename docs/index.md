# MDMA — Markdown Mapped

A lightweight templating format for generating one or more Markdown strings from a typed input schema.

Most templating languages (Jinja, Liquid, Handlebars) target HTML or arbitrary text files. `.mdma` is scoped specifically to producing **Markdown strings** — tight enough to validate inputs at the schema level, expressive enough to compose reusable block references, and able to fan a single template into many outputs via the `multiple` modifier.

## Get started

- **[Specification](spec.md)** — the full language spec: file structure, `@inputs`, block declarations, modifiers, template syntax, rendering model
- **[Grammar](grammar.md)** — formal EBNF grammar
- **[Filters](filters.md)** — built-in filter reference
- **[Examples](examples.md)** — worked `.mdma` files

## Libraries

| Package | Language | Install | Repo |
|---|---|---|---|
| [`python-mdma`](https://pypi.org/project/python-mdma/) | Python 3.9+ | `pip install python-mdma` | [mdma-python](https://github.com/Dastfox/mdma-python) |
| [`typescript-mdma`](https://www.npmjs.com/package/typescript-mdma) | TypeScript / Node 18+ | `npm install typescript-mdma` | [mdma-typescript](https://github.com/Dastfox/mdma-typescript) |

Both are from-scratch, dependency-free implementations of the [grammar](grammar.md), sharing the
same golden-output test fixtures so their behavior stays in sync.

- **[Python API reference](python/index.md)**
- **[TypeScript API reference](typescript/index.md)**

## VSCode Extension

Syntax highlighting, bracket matching, and snippets for `.mdma` files — see
[mdma-vscode](https://github.com/Dastfox/mdma-vscode).

## License

MIT — see [LICENSE](https://github.com/Dastfox/mdma/blob/main/LICENSE).
