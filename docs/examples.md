# Examples

Three worked `.mdma` files, also used as shared test fixtures by the
[Python](https://github.com/Dastfox/mdma-python) and
[TypeScript](https://github.com/Dastfox/mdma-typescript) implementations.

## `simple.mdma`

A minimal single-block template: one input schema, one block, a conditional, and a filter chain.

```mdma
--8<-- "examples/simple.mdma"
```

## `release-notes.mdma`

A multi-block template — `slug`, `title`, `release-notes` (with a breaking-change conditional and
Added/Changed/Fixed sections), and a `multiple`-modifier `changelog-entry` block.

```mdma
--8<-- "examples/release-notes.mdma"
```

## `named-blocks.mdma`

Demonstrates `multiple` + `name` together — object output keyed by a computed name
(`entry.version`) instead of array position.

```mdma
--8<-- "examples/named-blocks.mdma"
```
