# MDMA Language Specification

## 1. File Structure

An `.mdma` file is a plain-text UTF-8 file composed of two kinds of top-level elements:

1. **An inputs declaration** — a single `@inputs` section at the top of the file
2. **Named blocks** — one or more `<blockname>` sections that follow

```
<file>       ::= inputs-section block+
inputs-section ::= "@inputs" NEWLINE input-decl*
block        ::= block-header block-body
```

Blank lines between elements are allowed and ignored at the structural level (they may affect template whitespace within a block body).

---

## 2. `@inputs` Section

The file **must** begin with `@inputs` on its own line. Every line that follows (up to the first blank line or first block header) is an input declaration.

```
@inputs
name: type [= default]
...
```

### 2.1 Input Declarations

```
input-decl ::= IDENTIFIER ":" type ["=" default-value] NEWLINE
```

**Identifiers** are alphanumeric strings starting with a letter or underscore (`[a-zA-Z_][a-zA-Z0-9_]*`). Leading/trailing whitespace and extra spaces between tokens are ignored.

### 2.2 Types

| Type | Description |
|------|-------------|
| `string` | A single string value |
| `string[]` | An ordered list of strings |
| `boolean` | `true` or `false` |
| `number` | A numeric value (integer or float) |
| `number[]` | A list of numbers |
| `object` | An untyped key-value map |
| `object[]` | A list of untyped key-value maps |

### 2.3 Default Values

Defaults are optional. When an input has a default, callers may omit it.

| Type | Example default |
|------|----------------|
| `string` | `= ""` or `= "some text"` |
| `string[]` | `= []` |
| `boolean` | `= false` or `= true` |
| `number` | `= 0` |
| `number[]` | `= []` |
| `object[]` | `= []` |

Inputs without a default are **required** — omitting them is an error at render time.

### 2.4 Example

```mdma
@inputs
project:  string
version:  string
date:     string
added:    string[] = []
changed:  string[] = []
fixed:    string[] = []
breaking: boolean  = false
releases: object[] = []
```

---

## 3. Block Declarations

A block begins with its name wrapped in angle brackets on its own line:

```
<blockname>
```

Block names may contain lowercase letters, digits, and hyphens (`[-a-z0-9]+`). The block body extends from the line after the header to the line before the next block header (or end of file). Leading and trailing blank lines in a block body are preserved.

### 3.1 Headers with Modifiers

A block that needs a `multiple` or `name` modifier (section 4) opens and closes its header across multiple lines, like an HTML tag with attributes — each modifier is a bare `key: value` line between the opening `<` and the closing `>`:

```
<blockname
multiple: entry in releases
name: entry.version
>
```

The block name may also be given alone on the line right after `<`, which reads a little more like a self-contained header when there are several modifiers:

```
<
blockname
multiple: entry in releases
name: entry.version
>
```

`multiple` and `name` may appear in either order. No blank lines are allowed between the opening `<` and the closing `>`. A block with no modifiers should just use the single-line `<blockname>` form — there is only one way to write angle brackets in this language: they always mean "this is the block's own header," never a separate tag.

### 3.2 Block Ordering

Blocks are **ordered**. A block may reference any block declared **before** it by name. Forward references (referencing a block declared later in the file) are not allowed.

### 3.3 Block References

To embed the rendered output of a prior block, use `{{ blockname }}` inside a later block's body. The referenced block's rendered string is substituted inline.

```mdma
<title>
{{ project }} {{ version }}

<release-notes>
# {{ title }} — {{ date }}
```

In `<release-notes>`, `{{ title }}` resolves to the already-rendered output of the `<title>` block — `Acme SDK 2.1.0` — rather than looking for an input named `title`.

Block references and input references share the same interpolation syntax; resolution order is: **previously rendered blocks first, then inputs**.

---

## 4. The `multiple` Modifier

A block declared with a `multiple` modifier renders **once per item** in an array input, producing an array of strings rather than a single string. The modifier is a bare line inside the block's multi-line header (section 3.1):

```
multiple-modifier ::= "multiple" ":" IDENTIFIER "in" IDENTIFIER NEWLINE
```

```mdma
<changelog-entry
multiple: entry in releases
>

### {{ entry.version }} — {{ entry.date }}
{% for item in entry.added -%}
- {{ item }}
{% endfor %}
```

Here `entry` is the iteration variable bound to each element of the `releases` array. Inside the block body, `entry` behaves like any other object: you access its properties with dot notation (`entry.version`, `entry.added`).

The result of rendering a `multiple` block is an **array of strings**, one per item in the source list, in the same order. Callers receive this as a list they can join, concatenate, or process individually.

`multiple` is a reserved word and may not be used as a block name or input identifier. `name` is *not* reserved — it's only recognized as a modifier keyword inside a block's own header, so an input or block literally named `name` is unaffected.

### 4.1 Naming Items with `name`

An optional `name` modifier line may accompany `multiple` (in either order) to key each rendered item by a computed name instead of its array position. When present, the block renders to an **object** (a string-keyed map) rather than an array.

```
name-modifier ::= "name" ":" expression NEWLINE
```

`name` is only valid inside a header that also declares `multiple`; a block with `name` but no `multiple` is a syntax error. Its expression is evaluated once per item, in the same scope as the block body — it can reference the iteration variable and its properties (e.g. `entry.version`) but not `loop`, since it runs before the block body's own `{% for %}` tags do.

```mdma
<changelog-entry
multiple: entry in releases
name: entry.version
>

### {{ entry.version }} — {{ entry.date }}
{% for item in entry.added -%}
- {{ item }}
{% endfor %}
```

Given the same `releases` input as the example in section 8, this renders `changelog-entry` as:

```json
{
  "2.1.0": "### 2.1.0 — 2026-06-01\n- Dark mode\n",
  "2.0.0": "### 2.0.0 — 2026-05-01\n- Initial release\n"
}
```

The computed name must evaluate to a string or number (numbers are stringified the same way as in `{{ }}` interpolation); evaluating to an object, array, or null/undefined is a `TypeError`. If two items produce the same computed name, rendering fails with a `DuplicateName` error (see section 7.1) rather than silently overwriting one of them.

---

## 5. Template Syntax

The template language inside block bodies is Jinja/Liquid-inspired. It has two kinds of tags:

### 5.1 Interpolation Tags `{{ }}`

Outputs the value of an expression:

```
{{ variable }}
{{ object.property }}
{{ variable | filter }}
{{ variable | filter(arg) }}
```

### 5.2 Control Tags `{% %}`

Executes a control statement without producing output:

```
{% if condition %}...{% endif %}
{% elif condition %}
{% else %}
{% for item in list %}...{% endfor %}
```

### 5.3 Whitespace Control

Append `-` inside a tag delimiter to strip the adjacent whitespace (newline + indentation):

| Syntax | Effect |
|--------|--------|
| `{%- tag %}` | Strip whitespace **before** the tag |
| `{% tag -%}` | Strip whitespace **after** the tag |
| `{%- tag -%}` | Strip whitespace on both sides |
| `{{- expr }}` | Strip whitespace before interpolation |
| `{{ expr -}}` | Strip whitespace after interpolation |

This is the primary mechanism for controlling blank lines in the rendered output.

**Example** — without `-`, `{% if breaking %}` leaves a blank line before the blockquote; with `{%-`, the preceding newline is consumed:

```mdma
{%- if breaking %}

> **Breaking changes included in this release.**
{%- endif %}
```

### 5.4 Conditionals

```
{% if condition %}
  ...
{% elif other_condition %}
  ...
{% else %}
  ...
{% endif %}
```

Condition operands:
- Variable truthiness: `{% if breaking %}`
- Comparison: `{% if count > 0 %}`, `{% if version == "2.0" %}`
- Filter result: `{% if added | length > 0 %}`
- Logical: `{% if a and b %}`, `{% if not flag %}`

### 5.5 Loops

```
{% for item in list %}
{{ item }}
{% endfor %}
```

Loop variable properties are accessed with dot notation: `{{ item.name }}`.

Special loop variables available inside `{% for %}`:

| Variable | Value |
|----------|-------|
| `loop.index` | Current iteration (1-based) |
| `loop.index0` | Current iteration (0-based) |
| `loop.first` | `true` on the first iteration |
| `loop.last` | `true` on the last iteration |
| `loop.length` | Total number of items |

### 5.6 Dot Notation

Properties of objects are accessed with `.`:

```
{{ entry.version }}
{{ entry.date }}
{{ loop.first }}
```

Nested access is allowed: `{{ config.server.host }}`.

---

## 6. Filters

Filters transform a value using the pipe `|` operator:

```
{{ value | filter }}
{{ value | filter(arg) }}
{{ list | join(", ") }}
```

Multiple filters chain left-to-right:

```
{{ name | lower | trim }}
```

### Built-in Filters

| Filter | Input | Description |
|--------|-------|-------------|
| `length` | any | Number of items (string length or array length) |
| `lower` | string | Lowercase |
| `upper` | string | Uppercase |
| `trim` | string | Strip leading/trailing whitespace |
| `join(sep)` | array | Join array items with separator (default `""`) |
| `first` | array | First element |
| `last` | array | Last element |
| `default(val)` | any | Use `val` if the input is falsy/undefined |
| `reverse` | array or string | Reverse the order |
| `sort` | array | Lexicographic sort |
| `unique` | array | Remove duplicates |

---

## 7. Rendering Model

Rendering an `.mdma` file against an inputs object produces a **named output map**: a dictionary mapping each block name to its rendered value.

- Single blocks → `string`
- `multiple` blocks without `name` → `string[]`
- `multiple` blocks with `name` → an object mapping each item's computed name to its rendered string

Blocks are rendered **in declaration order**. Each block's output is available as a reference in all subsequent blocks.

### 7.1 Error Conditions

| Condition | Error |
|-----------|-------|
| Required input missing | `MissingInput: <name>` |
| Input type mismatch | `TypeError: expected <type>, got <actual>` |
| Forward block reference | `ReferenceError: block '<name>' not yet rendered` |
| Unknown variable | `ReferenceError: '<name>' is not defined` |
| Filter on wrong type | `FilterError: '<filter>' expects <type>` |
| `name` modifier used without `multiple` | `SyntaxError: 'name' modifier requires a 'multiple' modifier` |
| Two items produce the same `name` value | `DuplicateName: '<name>' in block '<blockname>'` |

---

## 8. Complete Example

```mdma
@inputs
project:  string
version:  string
date:     string
added:    string[] = []
changed:  string[] = []
fixed:    string[] = []
breaking: boolean  = false
releases: object[] = []

<slug>
{{ project }}-{{ version }}

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

{% if changed | length > 0 -%}
### Changed
{% for item in changed -%}
- {{ item }}
{% endfor -%}
{% endif %}

{% if fixed | length > 0 -%}
### Fixed
{% for item in fixed -%}
- {{ item }}
{% endfor -%}
{% endif %}

<changelog-entry
multiple: entry in releases
>

### {{ entry.version }} — {{ entry.date }}
{% for item in entry.added -%}
- {{ item }}
{% endfor %}
```

Given the input:
```json
{
  "project": "Acme SDK",
  "version": "3.0.0",
  "date": "2026-07-01",
  "added": ["WebSocket support"],
  "breaking": true,
  "releases": [
    { "version": "2.1.0", "date": "2026-06-01", "added": ["Dark mode"] },
    { "version": "2.0.0", "date": "2026-05-01", "added": ["Initial release"] }
  ]
}
```

Produces:

| Block | Type | Rendered value |
|-------|------|----------------|
| `slug` | `string` | `Acme SDK-3.0.0` |
| `title` | `string` | `Acme SDK 3.0.0` |
| `release-notes` | `string` | (see below) |
| `changelog-entry` | `string[]` | Array of 2 strings |

**`release-notes`:**
```markdown
# Acme SDK 3.0.0 — 2026-07-01

> **Breaking changes included in this release.**

### Added
- WebSocket support
```

**`changelog-entry[0]`:**
```markdown
### 2.1.0 — 2026-06-01
- Dark mode
```

**`changelog-entry[1]`:**
```markdown
### 2.0.0 — 2026-05-01
- Initial release
```
