# MDMA — Markdown Mapped

A lightweight templating format for generating one or more Markdown strings from a typed input schema.

Full docs, grammar, filter reference, and API reference: **https://dastfox.github.io/mdma/**

## Why

Most templating languages (Jinja, Liquid, Handlebars) target HTML or arbitrary text files. `.mdma` is scoped specifically to producing **Markdown strings** — tight enough to validate inputs at the schema level, expressive enough to compose reusable block references, and able to fan a single template into many outputs via the `multiple` modifier.

It borrows ideas from [Hygen](https://www.hygen.io/) (typed frontmatter, multi-generate) and Liquid (Markdown-native templating), but targets string output rather than files or web pages.

## Quick Example

```mdma
@inputs
project:  string
version:  string
date:     string
added:    string[] = []
breaking: boolean  = false

<title>
{{ project }} {{ version }}

<release-notes>
# {{ title }} — {{ date }}

{%- if breaking %}

> **Breaking changes included in this release.**
{%- endif %}

{% if added | length > 0 -%}
### Added
{% for item in added -%}
- {{ item }}
{% endfor -%}
{% endif %}
```

Given:

```json
{
  "project": "Acme SDK",
  "version": "2.1.0",
  "date": "2026-07-01",
  "added": ["Dark mode support", "WebSocket client"],
  "breaking": false
}
```

Produces two named strings:

**`title`** → `Acme SDK 2.1.0`

**`release-notes`** →

```markdown
# Acme SDK 2.1.0 — 2026-07-01

### Added

- Dark mode support
- WebSocket client
```

## Concepts

| Concept                  | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| `@inputs`                | Typed schema of variables the template accepts                           |
| `<blockname>`            | Named block that renders to one Markdown string                          |
| `{{ expr }}`             | Interpolation — outputs the value of an expression                       |
| `{% if %}` / `{% for %}` | Control flow inside a block                                              |
| `multiple: x in list`    | Block header modifier — renders the block once per item in a list        |
| `name: expr`             | Block header modifier — keys items by a computed name (needs `multiple`) |
| Block references         | Use `{{ blockname }}` to embed a previously rendered block               |

## This repository

This repo holds the format specification, formal grammar, filter reference, examples, and the
[documentation site](https://dastfox.github.io/mdma/) build. The reference implementations and
editor support live in their own repos:

| Component | Repo |
|---|---|
| Python implementation (`python-mdma` on PyPI) | [Dastfox/mdma-python](https://github.com/Dastfox/mdma-python) |
| TypeScript implementation (`typescript-mdma` on npm) | [Dastfox/mdma-typescript](https://github.com/Dastfox/mdma-typescript) |
| Go implementation (`github.com/Dastfox/mdma-go`) | [Dastfox/mdma-go](https://github.com/Dastfox/mdma-go) |
| VSCode extension | [Dastfox/mdma-vscode](https://github.com/Dastfox/mdma-vscode) |

## Documentation

| File | Content |
|---|---|
| [spec.md](spec.md) | Full language specification |
| [docs/grammar.md](docs/grammar.md) | Formal grammar (EBNF) |
| [docs/filters.md](docs/filters.md) | Filter reference |
| [examples/](examples/) | Worked `.mdma` files |

## License

MIT — see [LICENSE](LICENSE).
