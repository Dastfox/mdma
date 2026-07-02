# Filter Reference

Filters are applied to values inside `{{ }}` tags using the pipe `|` operator. Multiple filters chain left-to-right.

```
{{ value | filter }}
{{ value | filter(arg) }}
{{ list | join(", ") | upper }}
```

## String Filters

| Filter | Signature | Description | Example |
|--------|-----------|-------------|---------|
| `lower` | `string → string` | Convert to lowercase | `{{ name \| lower }}` → `acme` |
| `upper` | `string → string` | Convert to uppercase | `{{ name \| upper }}` → `ACME` |
| `trim` | `string → string` | Strip leading/trailing whitespace | `{{ value \| trim }}` |
| `length` | `string → number` | Number of characters | `{{ name \| length }}` → `4` |
| `default(val)` | `any → any` | Return `val` if input is falsy/undefined | `{{ desc \| default("N/A") }}` |

## Array Filters

| Filter | Signature | Description | Example |
|--------|-----------|-------------|---------|
| `length` | `array → number` | Number of items | `{{ items \| length }}` |
| `join(sep)` | `array → string` | Join items with separator (default: `""`) | `{{ tags \| join(", ") }}` |
| `first` | `array → any` | First element | `{{ releases \| first }}` |
| `last` | `array → any` | Last element | `{{ releases \| last }}` |
| `reverse` | `array → array` | Reverse order | `{{ items \| reverse }}` |
| `sort` | `array → array` | Lexicographic sort | `{{ names \| sort }}` |
| `unique` | `array → array` | Remove duplicate values | `{{ tags \| unique }}` |
| `default(val)` | `array → array` | Return `val` if input is empty/undefined | `{{ list \| default([]) }}` |

## Chaining Example

```mdma
@inputs
tags: string[] = []

<tag-line>
Tags: {{ tags | sort | unique | join(", ") }}
```

Input `["beta", "api", "beta", "stable"]` renders:
```
Tags: api, beta, stable
```

## Using Filters in Conditions

Filters can be used inside `{% if %}` conditions:

```mdma
{% if added | length > 0 -%}
### Added
{% for item in added -%}
- {{ item }}
{% endfor -%}
{% endif %}
```

The expression `added | length > 0` pipes `added` through the `length` filter, then compares the result to `0`.
