# Playground

Try `.mdma` templates directly in the browser. Rendering runs entirely client-side via the
[`typescript-mdma`](https://www.npmjs.com/package/typescript-mdma) package, loaded from
[esm.sh](https://esm.sh) — nothing you type here leaves your browser.

<div class="mdma-playground">
  <div class="mdma-playground-toolbar">
    <label for="mdma-example">Example</label>
    <select id="mdma-example">
      <option value="simple">simple.mdma</option>
      <option value="release-notes">release-notes.mdma</option>
      <option value="named-blocks">named-blocks.mdma</option>
    </select>
    <button id="mdma-run" type="button">Render</button>
  </div>
  <div class="mdma-playground-panes">
    <div class="mdma-pane">
      <div class="mdma-tabs">
        <button type="button" class="mdma-tab mdma-tab--active" data-io-tab="template">Template</button>
        <button type="button" class="mdma-tab" data-io-tab="inputs">Inputs (JSON)</button>
      </div>
      <div id="mdma-template-editor" class="mdma-editor">
        <pre class="mdma-editor-highlight" aria-hidden="true"><code id="mdma-template-highlight" class="mdma-output-code language-mdma"></code></pre>
        <textarea id="mdma-template" class="mdma-editor-input" spellcheck="false"></textarea>
      </div>
      <textarea id="mdma-inputs" class="mdma-textarea" spellcheck="false" hidden></textarea>
    </div>
    <div class="mdma-pane">
      <div id="mdma-output-tabs" class="mdma-tabs"></div>
      <pre id="mdma-output" class="mdma-output"><code id="mdma-output-code" class="mdma-output-code language-markdown"></code></pre>
    </div>
  </div>
</div>

<style>
  .mdma-playground-toolbar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1rem 0 0.75rem;
  }
  .mdma-playground-toolbar select,
  .mdma-playground-toolbar button {
    font-family: var(--md-code-font, monospace);
    font-size: 0.75rem;
    padding: 0.3rem 0.7rem;
    color: var(--md-default-fg-color);
    background-color: var(--md-code-bg-color);
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.2rem;
  }
  .mdma-playground-toolbar button {
    cursor: pointer;
    font-weight: 700;
  }
  .mdma-playground-toolbar button:hover {
    color: var(--md-primary-fg-color);
    border-color: var(--md-primary-fg-color);
  }
  .mdma-playground-panes {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  @media (max-width: 76.1875em) {
    .mdma-playground-panes {
      grid-template-columns: 1fr;
    }
  }
  .mdma-pane {
    display: flex;
    flex-direction: column;
  }
  .mdma-textarea,
  .mdma-output {
    width: 100%;
    box-sizing: border-box;
    flex: 1 1 auto;
    min-height: 22rem;
    padding: 0.75rem;
    font-family: var(--md-code-font, monospace);
    font-size: 0.75rem;
    line-height: 1.4;
    color: var(--md-code-fg-color);
    background-color: var(--md-code-bg-color);
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.2rem;
    resize: vertical;
  }
  .mdma-editor {
    position: relative;
    flex: 1 1 auto;
    min-height: 22rem;
    resize: vertical;
    overflow: hidden;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.2rem;
  }
  .mdma-editor[hidden] {
    display: none;
  }
  .mdma-editor-highlight,
  .mdma-editor-input {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    box-sizing: border-box;
    padding: 0.75rem;
    font-family: var(--md-code-font, monospace);
    font-size: 0.75rem;
    line-height: 1.4;
    white-space: pre-wrap;
    word-break: break-word;
    overflow: auto;
    border: none;
  }
  .mdma-editor-highlight {
    color: var(--md-code-fg-color);
    background-color: var(--md-code-bg-color);
    pointer-events: none;
  }
  .mdma-editor-input {
    background: transparent;
    color: transparent;
    caret-color: var(--md-code-fg-color);
    resize: none;
  }
  .mdma-output {
    overflow: auto;
    white-space: pre-wrap;
    word-break: break-word;
    /* mkdocs-material's `.md-typeset pre` rules out-specificity this class for
       margin/height (copy-button enhancement also sets an inline height) --
       !important is needed on both to keep this flex-sized and flush. */
    margin: 0 !important;
    height: auto !important;
  }
  .mdma-output.mdma-error {
    color: #b00020;
    border-color: #b00020;
    white-space: pre-wrap;
  }
  .mdma-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
    margin-bottom: 0.35rem;
  }
  .mdma-tab {
    font-family: var(--md-code-font, monospace);
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.2rem 0.2rem 0 0;
    background: transparent;
    color: var(--md-default-fg-color--light);
    cursor: pointer;
  }
  .mdma-tab.mdma-tab--active {
    color: var(--md-primary-fg-color);
    border-color: var(--md-primary-fg-color);
    border-bottom-color: transparent;
    font-weight: 700;
  }
  .mdma-output-code .hljs-section {
    color: var(--md-primary-fg-color);
    font-weight: 700;
  }
  .mdma-output-code .hljs-strong {
    color: var(--md-accent-fg-color);
    font-weight: 700;
  }
  .mdma-output-code .hljs-emphasis {
    font-style: italic;
  }
  .mdma-output-code .hljs-bullet,
  .mdma-output-code .hljs-number,
  .mdma-output-code .hljs-type,
  .mdma-output-code .hljs-literal {
    color: var(--md-accent-fg-color);
  }
  .mdma-output-code .hljs-link,
  .mdma-output-code .hljs-string,
  .mdma-output-code .hljs-template-tag,
  .mdma-output-code .hljs-template-variable {
    color: var(--md-primary-fg-color--light, var(--md-primary-fg-color));
  }
  .mdma-output-code .hljs-quote,
  .mdma-output-code .hljs-comment,
  .mdma-output-code .hljs-meta {
    color: var(--md-default-fg-color--light);
  }
  .mdma-output-code .hljs-quote,
  .mdma-output-code .hljs-comment {
    font-style: italic;
  }
  .mdma-output-code .hljs-tag {
    color: var(--md-primary-fg-color);
    font-weight: 700;
  }
  .mdma-output-code .hljs-keyword {
    color: var(--md-accent-fg-color);
    font-weight: 700;
  }
  .mdma-output-code .hljs-code {
    color: var(--md-code-fg-color);
  }
</style>

<script type="module">
  import { render } from "https://esm.sh/typescript-mdma@0.1.0";
  import hljs from "https://esm.sh/highlight.js@11.9.0/lib/core";
  import markdownLang from "https://esm.sh/highlight.js@11.9.0/lib/languages/markdown";

  hljs.registerLanguage("markdown", markdownLang);

  /** highlight.js grammar for `.mdma` source, mirroring the Pygments lexer in
   * pygments-mdma/ (see docs/grammar.md) so the live editor and the static
   * `mdma` code fences elsewhere in these docs read the same way. */
  hljs.registerLanguage("mdma", (hljs) => {
    const JINJA_KEYWORDS = {
      keyword: "if elif else endif for endfor in and or not",
      literal: "true false",
    };
    const JINJA_INNER = [
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      { className: "operator", begin: /==|!=|>=|<=|\||[<>]/ },
    ];
    return {
      name: "MDMA",
      case_insensitive: false,
      contains: [
        {
          className: "meta",
          begin: /^@inputs\b/,
          end: /(?=^<)/,
          contains: [
            { className: "type", begin: /\b(string|number|boolean|object)(\[\])?\b/ },
            { className: "literal", begin: /\b(true|false)\b/ },
            hljs.QUOTE_STRING_MODE,
            hljs.C_NUMBER_MODE,
          ],
        },
        {
          className: "tag",
          begin: /^</,
          end: />/,
          keywords: { keyword: "multiple name in" },
        },
        { className: "comment", begin: /\{#/, end: /#\}/ },
        {
          className: "template-variable",
          begin: /\{\{-?/,
          end: /-?\}\}/,
          keywords: JINJA_KEYWORDS,
          contains: JINJA_INNER,
        },
        {
          className: "template-tag",
          begin: /\{%-?/,
          end: /-?%\}/,
          keywords: JINJA_KEYWORDS,
          contains: JINJA_INNER,
        },
        { className: "section", begin: /^#{1,6}(?=[ \t])/ },
        { className: "quote", begin: /^[ \t]*>(?=[ \t])/ },
        { className: "bullet", begin: /^[ \t]*[-*](?=[ \t])/ },
        { className: "strong", begin: /\*\*[^*\n]+\*\*/ },
      ],
    };
  });

  const EXAMPLES = {
    simple: {
      template: `@inputs
name:        string
description: string
tags:        string[] = []
draft:       boolean  = false

<badge-line>
{% if draft -%}**[DRAFT]** {% endif %}{{ name }}{% if tags | length > 0 %} — {{ tags | join(", ") }}{% endif %}

<body>
## {{ name }}

{{ description }}

{% if tags | length > 0 -%}
**Tags:** {{ tags | join(", ") }}
{%- endif %}`,
      inputs: {
        name: "Widget",
        description: "A small reusable widget.",
        tags: ["ui", "core"],
      },
    },
    "release-notes": {
      template: `@inputs
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
{% endfor %}`,
      inputs: {
        project: "Acme SDK",
        version: "3.0.0",
        date: "2026-07-01",
        added: ["WebSocket support"],
        breaking: true,
        releases: [{ version: "2.1.0", date: "2026-06-01", added: ["Dark mode"] }],
      },
    },
    "named-blocks": {
      template: `@inputs
releases: object[] = []

<changelog-by-version
multiple: entry in releases
name: entry.version
>

### {{ entry.version }} — {{ entry.date }}
{% for item in entry.added -%}
- {{ item }}
{% endfor %}`,
      inputs: {
        releases: [
          { version: "2.1.0", date: "2026-06-01", added: ["Dark mode"] },
          { version: "2.0.0", date: "2026-05-01", added: ["Initial release"] },
        ],
      },
    },
  };

  const templateEl = document.getElementById("mdma-template");
  const templateEditorEl = document.getElementById("mdma-template-editor");
  const templateHighlightEl = document.getElementById("mdma-template-highlight");
  const inputsEl = document.getElementById("mdma-inputs");
  const outputEl = document.getElementById("mdma-output");
  const outputCodeEl = document.getElementById("mdma-output-code");
  const outputTabsEl = document.getElementById("mdma-output-tabs");
  const pickerEl = document.getElementById("mdma-example");
  const runEl = document.getElementById("mdma-run");

  let blocks = [];
  let activeBlock = null;

  /** A block's rendered value is a string, an array of strings (`multiple`), or
   * a name-keyed object of strings (`multiple` + `name`). Give each string its
   * own tab -- named after the JS property access that would retrieve it --
   * instead of joining them, so the tabs don't imply a `---`-joined document
   * that the actual render() output never produces. */
  function toTabs(result) {
    const tabs = [];
    for (const [name, value] of Object.entries(result)) {
      if (typeof value === "string") {
        tabs.push({ name, text: value });
      } else if (Array.isArray(value)) {
        value.forEach((text, i) => tabs.push({ name: `${name}[${i}]`, text }));
      } else {
        for (const [key, text] of Object.entries(value)) {
          tabs.push({ name: `${name}[${key}]`, text });
        }
      }
    }
    return tabs;
  }

  /** Mirrors templateEl's value into the highlighted overlay behind it. A
   * trailing newline keeps the last line's height in sync with the textarea,
   * which always renders one past a trailing "\n". */
  function highlightTemplate() {
    const source = templateEl.value.replace(/\n$/, "\n\n");
    templateHighlightEl.innerHTML = hljs.highlight(source, { language: "mdma" }).value;
  }

  function showError(message) {
    outputTabsEl.hidden = true;
    outputEl.classList.add("mdma-error");
    outputCodeEl.className = "mdma-output-code";
    outputCodeEl.textContent = message;
  }

  function renderActiveTab() {
    const block = blocks.find((b) => b.name === activeBlock) ?? blocks[0];
    if (!block) {
      showError("This template has no output blocks.");
      return;
    }
    activeBlock = block.name;
    outputTabsEl.hidden = false;
    outputEl.classList.remove("mdma-error");
    outputCodeEl.className = "mdma-output-code language-markdown";
    outputCodeEl.innerHTML = hljs.highlight(block.text, { language: "markdown" }).value;

    outputTabsEl.innerHTML = "";
    for (const b of blocks) {
      const tab = document.createElement("button");
      tab.type = "button";
      tab.textContent = b.name;
      tab.className = "mdma-tab" + (b.name === activeBlock ? " mdma-tab--active" : "");
      tab.addEventListener("click", () => {
        activeBlock = b.name;
        renderActiveTab();
      });
      outputTabsEl.appendChild(tab);
    }
  }

  function run() {
    let inputs;
    try {
      inputs = JSON.parse(inputsEl.value);
    } catch (err) {
      showError("Invalid inputs JSON: " + err.message);
      return;
    }
    try {
      const result = render(templateEl.value, inputs);
      blocks = toTabs(result);
      renderActiveTab();
    } catch (err) {
      showError(err && err.message ? err.message : String(err));
    }
  }

  function loadExample(key) {
    const example = EXAMPLES[key];
    templateEl.value = example.template;
    inputsEl.value = JSON.stringify(example.inputs, null, 2);
    activeBlock = null;
    highlightTemplate();
    run();
  }

  templateEl.addEventListener("input", highlightTemplate);
  templateEl.addEventListener("scroll", () => {
    templateHighlightEl.parentElement.scrollTop = templateEl.scrollTop;
    templateHighlightEl.parentElement.scrollLeft = templateEl.scrollLeft;
  });

  const ioTabButtons = document.querySelectorAll("[data-io-tab]");
  ioTabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      ioTabButtons.forEach((b) => b.classList.remove("mdma-tab--active"));
      btn.classList.add("mdma-tab--active");
      templateEditorEl.hidden = btn.dataset.ioTab !== "template";
      inputsEl.hidden = btn.dataset.ioTab !== "inputs";
    });
  });

  pickerEl.addEventListener("change", () => loadExample(pickerEl.value));
  runEl.addEventListener("click", run);

  loadExample("simple");
</script>
