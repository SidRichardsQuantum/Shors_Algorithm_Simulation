from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown


DOCS = [
    ("README.md", "Overview", "index.html"),
    ("THEORY.md", "Theory", "theory.html"),
    ("CIRCUITS.md", "Circuits", "circuits.html"),
    ("RESULTS.md", "Results", "results.html"),
    ("CHANGELOG.md", "Changelog", "changelog.html"),
]

REPO_URL = "https://github.com/SidRichardsQuantum/Shors_Algorithm_Simulation"
PACKAGE_URL = "https://pypi.org/project/shors-algorithm-simulation/"
PORTFOLIO_URL = "https://sidrichardsquantum.github.io/"


def rewrite_links(markdown_text: str, page_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        target = match.group(2)
        if target in page_map:
            return f"[{label}]({page_map[target]})"
        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+\.md)\)", replace, markdown_text)


def title_from(markdown_text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def excerpt_from(markdown_text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", markdown_text)
    for paragraph in re.split(r"\n\s*\n", clean):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith("#") or paragraph.startswith("["):
            continue
        paragraph = re.sub(r"[*_`]", "", paragraph)
        if len(paragraph) > 180:
            return paragraph[:177].rsplit(" ", 1)[0] + "..."
        return paragraph
    return "Project documentation and release notes."


def render_markdown(
    markdown_text: str, page_map: dict[str, str], md: markdown.Markdown
) -> str:
    md.reset()
    article = md.convert(rewrite_links(markdown_text, page_map))
    return article.replace('href="LICENSE"', 'href="LICENSE.txt"')


def project_structure_html() -> str:
    return """
    <h3 id="project-structure">Project Structure</h3>
    <div class="structure-grid" aria-label="Project structure">
      <article class="structure-card">
        <h4>Package</h4>
        <p><code>shors_algorithm_simulation/</code></p>
        <p>Core API, CLI, validation, probability distributions, period recovery, plotting helpers, and quantum operator modules.</p>
      </article>
      <article class="structure-card">
        <h4>Examples</h4>
        <p><code>examples/</code></p>
        <p>Runnable factorisation demos, no-plot runs, shot sweeps, diagnostics, runtime benchmarks, and circuit diagram generation.</p>
      </article>
      <article class="structure-card">
        <h4>Documentation</h4>
        <p><code>README.md</code>, <code>THEORY.md</code>, <code>CIRCUITS.md</code>, <code>RESULTS.md</code>, <code>CHANGELOG.md</code></p>
        <p>Pages source files rendered into the static GitHub Pages site.</p>
      </article>
      <article class="structure-card">
        <h4>Generated Assets</h4>
        <p><code>images/</code></p>
        <p>Probability plots, oracle-period diagnostics, continued-fraction outputs, circuit diagrams, and runtime visualizations.</p>
      </article>
      <article class="structure-card">
        <h4>Tests</h4>
        <p><code>tests/</code></p>
        <p>Regression tests for CLI behavior, period finding, circuit diagram support, and installation smoke checks.</p>
      </article>
      <article class="structure-card">
        <h4>Build and Metadata</h4>
        <p><code>pyproject.toml</code>, <code>scripts/build_pages.py</code>, <code>.github/workflows/</code></p>
        <p>Package metadata, local/static documentation builder, test workflow, Pages deployment, and PyPI publishing automation.</p>
      </article>
    </div>
    """


def enhance_home_article(article: str) -> str:
    article = re.sub(
        r'<h3 id="project-structure">Project Structure</h3>\s*<pre><code>.*?</code></pre>',
        project_structure_html(),
        article,
        flags=re.DOTALL,
    )
    return article


def nav_html() -> str:
    links = [
        f'<a href="{output}">{html.escape(label)}</a>' for _, label, output in DOCS
    ]
    links.append(f'<a href="{PORTFOLIO_URL}">Portfolio</a>')
    return "\n".join(links)


def quantum_circuit_svg() -> str:
    return """
    <svg viewBox="0 0 520 360" role="img" aria-labelledby="circuit-title circuit-desc">
      <title id="circuit-title">Quantum circuit visual</title>
      <desc id="circuit-desc">Stylized Shor period-finding circuit with Hadamard, modular exponentiation, and inverse QFT blocks.</desc>
      <defs>
        <pattern id="hero-grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M40 0H0V40" />
        </pattern>
      </defs>
      <rect class="visual-bg" width="520" height="360" rx="8" />
      <rect class="visual-grid" width="520" height="360" rx="8" fill="url(#hero-grid)" />
      <g class="visual-circuit">
        <path d="M64 82h390M64 136h390M64 190h390M64 244h390" />
        <path d="M148 82v108M246 136v108M342 82v162" />
        <circle cx="148" cy="82" r="13" />
        <circle cx="148" cy="190" r="13" />
        <circle cx="246" cy="136" r="13" />
        <circle cx="246" cy="244" r="13" />
        <circle cx="342" cy="82" r="13" />
        <circle cx="342" cy="244" r="13" />
        <path d="M105 64v36M87 82h36M87 118l36 36M123 118l-36 36M316 172l54 36M370 172l-54 36" />
        <rect x="198" y="62" width="54" height="40" rx="8" />
        <rect x="394" y="116" width="54" height="40" rx="8" />
      </g>
      <g class="visual-labels">
        <text x="58" y="318">H</text>
        <text x="132" y="318">oracle</text>
        <text x="232" y="318">IQFT</text>
        <text x="326" y="318">period</text>
        <text x="426" y="318">PyPI</text>
      </g>
    </svg>
    """


def build_home_cards(repo: Path) -> str:
    cards = []
    for source, label, output in DOCS[1:]:
        path = repo / source
        if not path.exists():
            continue
        markdown_text = path.read_text(encoding="utf-8")
        cards.append(
            f"""<article class="project-card">
              <div>
                <h3>{html.escape(title_from(markdown_text, label))}</h3>
                <p>{html.escape(excerpt_from(markdown_text))}</p>
              </div>
              <div class="tags">
                <span>{html.escape(label)}</span>
                <span>Documentation</span>
              </div>
              <div class="card-links">
                <a href="{output}">Open documentation</a>
              </div>
            </article>"""
        )
    return "\n".join(cards)


def build_layout(title: str, body: str, nav: str) -> str:
    return f"""<!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Educational classical simulation of Shor's period-finding algorithm.">
        <meta name="theme-color" content="#0f5364">
        <title>{html.escape(title)}</title>
        <link rel="stylesheet" href="styles.css">
        <script>
          window.MathJax = {{
            tex: {{
              inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],
              displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],
              processEscapes: true
            }}
          }};
        </script>
        <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
      </head>
      <body>
        <a class="skip-link" href="#top">Skip to main content</a>
        <header class="site-header">
          <a class="brand" href="index.html" aria-label="Shor's Algorithm Simulation home">
            <span class="brand-mark">SR</span>
            <span>Shor's Algorithm Simulation</span>
          </a>
          <nav class="nav-links" aria-label="Primary navigation">
            {nav}
          </nav>
        </header>
        <main id="top" tabindex="-1">
          {body}
        </main>
        <footer class="site-footer">
          <span>&copy; <span id="year">2026</span> Sid Richards</span>
          <a href="{PORTFOLIO_URL}">Back to portfolio</a>
        </footer>
      </body>
    </html>
    """


def build_home(article: str, home_cards: str) -> str:
    return f"""
    <section class="hero section">
      <div class="hero-copy">
        <p class="eyebrow">Quantum software portfolio project</p>
        <h1>Shor's Algorithm Simulation</h1>
        <p class="hero-text">
          A pure Python educational simulator for Shor's period-finding workflow,
          with explicit matrix mode, faster distribution mode, diagnostics, plots,
          and a package-ready command line interface.
        </p>
        <div class="hero-actions">
          <a class="button primary" href="{PACKAGE_URL}">View package</a>
          <a class="button" href="#install">Install</a>
          <a class="button subtle" href="{PORTFOLIO_URL}">Back to portfolio</a>
        </div>
      </div>
      <div class="hero-side">
        <aside class="focus-panel" aria-label="Project highlights">
          <h2>Focus Areas</h2>
          <ul>
            <li>Classical simulation of Shor's quantum period-finding workflow</li>
            <li>Explicit matrix mode and ideal first-register distribution mode</li>
            <li>IQFT peaks, continued fractions, diagnostics, CSV outputs, and plots</li>
            <li>Package-first scientific Python with CLI and API workflows</li>
          </ul>
        </aside>
        <aside class="focus-panel snapshot-panel" aria-label="Project snapshot">
          <h2>Project Snapshot</h2>
          <dl>
            <div><dt>Default mode</dt><dd>distribution</dd></div>
            <div><dt>Small-case mode</dt><dd>matrix</dd></div>
            <div><dt>Diagnostics</dt><dd>plots, CSV, JSON</dd></div>
            <div><dt>Entry points</dt><dd>Python API and <code>shors-sim</code></dd></div>
          </dl>
        </aside>
      </div>
    </section>
    <section class="section" id="install">
      <div class="section-heading">
        <p class="eyebrow">Install and run</p>
        <h2>Packages</h2>
        <p>Installable project links with live package metadata badges and direct setup commands.</p>
      </div>
      <div class="package-list">
        <article class="package-row">
          <div>
            <h3>shors-algorithm-simulation</h3>
            <div class="badges" aria-label="shors-algorithm-simulation package badges">
              <img src="https://img.shields.io/pypi/v/shors-algorithm-simulation?label=PyPI" alt="shors-algorithm-simulation PyPI version">
              <img src="https://img.shields.io/pypi/pyversions/shors-algorithm-simulation" alt="shors-algorithm-simulation supported Python versions">
              <img src="https://img.shields.io/pypi/l/shors-algorithm-simulation" alt="shors-algorithm-simulation license">
            </div>
          </div>
          <code>pip install shors-algorithm-simulation</code>
          <a href="{PACKAGE_URL}">PyPI</a>
        </article>
        <article class="package-row">
          <div>
            <h3>source checkout</h3>
            <p>Editable install for tests, examples, and local documentation builds.</p>
          </div>
          <code>python -m pip install -e ".[test]"</code>
          <a href="{REPO_URL}">GitHub</a>
        </article>
        <article class="package-row">
          <div>
            <h3>circuit extras</h3>
            <p>Optional dependencies for Qiskit circuit diagram generation.</p>
          </div>
          <code>python -m pip install ".[circuits]"</code>
          <a href="circuits.html">Circuits</a>
        </article>
      </div>
    </section>
    <section class="section">
      <div class="section-heading">
        <p class="eyebrow">Documentation map</p>
        <h2>Read by workflow</h2>
      </div>
      <div class="project-grid">
        {home_cards}
      </div>
    </section>
    <section class="content section readme-shell">
      <div class="section-heading">
        <p class="eyebrow">Complete README</p>
        <h2>Full project documentation</h2>
      </div>
      <article class="prose readme-prose">
        {article}
      </article>
    </section>
    """


CSS = """
:root {
  color-scheme: light dark;
  --bg: #f6f8f7;
  --surface: #ffffff;
  --surface-muted: #edf4f3;
  --surface-tint: #e6f5f6;
  --text: #172126;
  --muted: #5a6870;
  --line: #d6e1df;
  --accent: #1098ad;
  --accent-strong: #0f5364;
  --accent-soft: #dff4f6;
  --code-bg: #eef5f4;
  --shadow: 0 22px 60px rgba(16, 42, 49, 0.12);
  --shadow-soft: 0 12px 34px rgba(16, 42, 49, 0.08);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1416;
    --surface: #141d20;
    --surface-muted: #1b292d;
    --surface-tint: #11292f;
    --text: #edf5f6;
    --muted: #a7b8bd;
    --line: #2d3d42;
    --accent: #63cdda;
    --accent-strong: #9eddea;
    --accent-soft: #17363d;
    --code-bg: #101b1f;
    --shadow: 0 22px 60px rgba(0, 0, 0, 0.28);
    --shadow-soft: 0 12px 34px rgba(0, 0, 0, 0.2);
  }
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--accent-soft) 42%, transparent), transparent 34rem),
    var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
  text-rendering: optimizeLegibility;
}

a {
  color: var(--accent-strong);
  text-decoration-color: color-mix(in srgb, var(--accent) 62%, transparent);
  text-underline-offset: 0.2em;
}

a:hover {
  color: var(--accent);
}

a:focus-visible,
main:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 4px;
}

.skip-link {
  position: fixed;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 20;
  transform: translateY(-150%);
  border: 1px solid var(--accent-strong);
  border-radius: 8px;
  padding: 0.65rem 0.9rem;
  background: var(--surface);
  color: var(--accent-strong);
  font-weight: 800;
  text-decoration: none;
  box-shadow: var(--shadow);
  transition: transform 160ms ease;
}

.skip-link:focus-visible {
  transform: translateY(0);
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 0.95rem clamp(1rem, 4vw, 3rem);
  border-bottom: 1px solid color-mix(in srgb, var(--line) 80%, transparent);
  background: color-mix(in srgb, var(--bg) 90%, transparent);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.72rem;
  color: var(--text);
  font-weight: 800;
  text-decoration: none;
}

.brand-mark {
  display: inline-grid;
  width: 2.25rem;
  height: 2.25rem;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  color: var(--accent-strong);
  font-size: 0.78rem;
  letter-spacing: 0;
  box-shadow: var(--shadow-soft);
}

.nav-links,
.site-footer nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.4rem 1rem;
  color: var(--muted);
  font-size: 0.95rem;
}

.nav-links a,
.site-footer a {
  color: inherit;
  font-weight: 700;
  text-decoration: none;
}

.section {
  width: min(1140px, calc(100% - 2rem));
  margin: 0 auto;
  padding: clamp(3rem, 7vw, 5.75rem) 0;
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 0.96fr) minmax(340px, 1.04fr);
  align-items: center;
  gap: clamp(2rem, 5vw, 4.5rem);
  min-height: calc(84vh - 5rem);
  padding-top: clamp(2rem, 6vw, 5rem);
}

.hero-copy {
  max-width: 640px;
}

.hero h1 {
  max-width: 10ch;
  margin: 0;
  font-size: clamp(3.5rem, 8vw, 6.8rem);
  line-height: 0.92;
  letter-spacing: 0;
}

.eyebrow,
.card-kicker {
  margin: 0 0 0.75rem;
  color: var(--accent-strong);
  font-size: 0.77rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-text {
  max-width: 620px;
  margin: 1.35rem 0 0;
  color: var(--muted);
  font-size: clamp(1.08rem, 2vw, 1.32rem);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2rem;
}

.button {
  display: inline-flex;
  min-height: 2.8rem;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.72rem 1rem;
  background: var(--surface);
  color: var(--text);
  font-weight: 800;
  text-decoration: none;
  box-shadow: var(--shadow-soft);
  transition:
    border-color 160ms ease,
    transform 160ms ease,
    box-shadow 160ms ease;
}

.button.primary {
  border-color: var(--accent-strong);
  background: var(--accent-strong);
  color: #ffffff;
}

.button.subtle {
  color: var(--accent-strong);
}

.button:hover {
  border-color: color-mix(in srgb, var(--accent) 45%, var(--line));
  box-shadow: var(--shadow);
  transform: translateY(-1px);
}

.hero-visual {
  display: grid;
  gap: 1rem;
}

.circuit-visual {
  display: block;
  width: 100%;
  min-height: 290px;
}

.circuit-grid path {
  stroke: url(#wireGlow);
  stroke-width: 3;
  stroke-linecap: round;
}

.register-labels {
  fill: var(--muted);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 16px;
}

.gate-stack rect,
.oracle-block rect,
.iqft-block rect,
.measurements path:first-child,
.measurements path:nth-child(2),
.measurements path:nth-child(3) {
  fill: var(--surface-muted);
  stroke: var(--line);
  stroke-width: 2;
}

.gate-stack text,
.oracle-block text,
.iqft-block text {
  fill: var(--text);
  font-weight: 800;
  text-anchor: middle;
  dominant-baseline: middle;
}

.oracle-block rect {
  fill: var(--accent-soft);
}

.measurements path {
  fill: none;
  stroke: var(--accent-strong);
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.accent-dots circle {
  fill: var(--accent);
}

.focus-panel,
.project-card,
.package-row,
.metric {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: color-mix(in srgb, var(--surface) 94%, var(--accent-soft));
  box-shadow: var(--shadow-soft);
}

.focus-panel {
  padding: 1.25rem;
}

.focus-panel h2 {
  margin: 0 0 1rem;
  font-size: 1rem;
}

.focus-panel ul {
  display: grid;
  gap: 0.8rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.snapshot-panel dl {
  display: grid;
  gap: 0.75rem;
  margin: 0;
}

.snapshot-panel div {
  display: grid;
  grid-template-columns: minmax(7.5rem, 0.8fr) minmax(0, 1.2fr);
  gap: 0.8rem;
  align-items: baseline;
  border-top: 1px solid var(--line);
  padding-top: 0.75rem;
}

.snapshot-panel div:first-child {
  border-top: 0;
  padding-top: 0;
}

.snapshot-panel dt {
  color: var(--text);
  font-weight: 800;
}

.snapshot-panel dd {
  margin: 0;
  color: var(--muted);
}

.focus-panel li {
  display: grid;
  grid-template-columns: 9rem minmax(0, 1fr);
  gap: 1rem;
  color: var(--muted);
}

.focus-panel strong {
  color: var(--text);
}

.overview-band {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  padding-top: 0;
}

.metric {
  padding: 1rem;
}

.metric span {
  display: block;
  color: var(--muted);
  font-size: 0.9rem;
}

.metric strong {
  display: block;
  margin-top: 0.35rem;
  color: var(--text);
  font-size: 1.05rem;
}

.split-section {
  display: grid;
  grid-template-columns: minmax(220px, 0.7fr) minmax(0, 1.3fr);
  gap: clamp(1.5rem, 4vw, 3rem);
  align-items: start;
}

.split-section h2,
.section-heading h2 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.25rem);
  line-height: 1;
}

.package-list {
  display: grid;
  gap: 0.8rem;
}

.package-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  color: var(--text);
  text-decoration: none;
  transition:
    border-color 160ms ease,
    transform 160ms ease,
    box-shadow 160ms ease;
}

.package-row:hover,
.project-card:hover {
  border-color: color-mix(in srgb, var(--accent) 50%, var(--line));
  box-shadow: var(--shadow);
  transform: translateY(-2px);
}

.package-row strong,
.package-row code {
  display: block;
}

.package-row code {
  overflow-wrap: anywhere;
  margin-top: 0.35rem;
  color: var(--muted);
  font-size: 0.9rem;
}

.package-row em {
  color: var(--accent-strong);
  font-style: normal;
  font-weight: 850;
}

.section-heading {
  max-width: 720px;
  margin-bottom: 1.4rem;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.project-card {
  display: flex;
  min-height: 250px;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.2rem;
  color: var(--text);
  text-decoration: none;
  transition:
    border-color 160ms ease,
    box-shadow 160ms ease,
    transform 160ms ease;
}

.project-card h3 {
  margin: 0 0 0.7rem;
  color: var(--text);
  font-size: 1.18rem;
  line-height: 1.2;
}

.project-card p {
  margin: 0;
  color: var(--muted);
}

.project-card strong {
  color: var(--accent-strong);
}

.content {
  border-top: 1px solid var(--line);
}

.readme-shell {
  padding-top: clamp(3rem, 6vw, 5rem);
}

.prose {
  max-width: 900px;
}

.readme-prose {
  padding: 1.5rem;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: color-mix(in srgb, var(--surface) 96%, var(--accent-soft));
  box-shadow: var(--shadow-soft);
}

.prose h1,
.prose h2,
.prose h3 {
  line-height: 1.15;
  letter-spacing: 0;
}

.prose h1 {
  font-size: clamp(2rem, 5vw, 3.8rem);
}

.readme-prose > h1:first-child {
  font-size: clamp(1.8rem, 4vw, 2.7rem);
}

.structure-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin: 1rem 0 2rem;
}

.structure-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 1rem;
  background: var(--surface);
  box-shadow: var(--shadow-soft);
}

.structure-card h4 {
  margin: 0 0 0.6rem;
  color: var(--text);
  font-size: 1rem;
}

.structure-card p {
  margin: 0.55rem 0 0;
}

.prose h2 {
  margin-top: 2.4rem;
  font-size: clamp(1.55rem, 3vw, 2.2rem);
}

.prose h3 {
  margin-top: 2rem;
  font-size: 1.3rem;
}

.prose p,
.prose li {
  color: var(--muted);
}

.readme-prose > p:first-of-type {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
}

.readme-prose > p:first-of-type img {
  margin: 0;
  border: 0;
  border-radius: 0;
  box-shadow: none;
}

.prose img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1.5rem 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow-soft);
}

.prose table {
  display: block;
  overflow-x: auto;
  width: 100%;
  border-collapse: collapse;
}

.prose th,
.prose td {
  border: 1px solid var(--line);
  padding: 0.55rem 0.7rem;
}

.prose th {
  background: var(--surface-muted);
  color: var(--text);
}

.prose code {
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 0.12rem 0.3rem;
  background: var(--code-bg);
  color: var(--text);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 0.92em;
}

.prose pre {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 1rem;
  background: var(--code-bg);
}

.prose pre code {
  border: 0;
  padding: 0;
  background: transparent;
}

.site-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 2rem clamp(1rem, 4vw, 3rem);
  border-top: 1px solid var(--line);
  color: var(--muted);
}

.site-footer strong,
.site-footer span {
  display: block;
}

@media (max-width: 960px) {
  .hero,
  .split-section {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .overview-band,
  .project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .site-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 0.75rem;
  }

  .nav-links,
  .site-footer nav {
    justify-content: flex-start;
  }

  .section {
    width: min(100% - 1rem, 1140px);
    padding: clamp(2.5rem, 12vw, 4rem) 0;
  }

  .hero h1 {
    font-size: clamp(3rem, 17vw, 4.6rem);
  }

  .hero-actions,
  .overview-band,
  .project-grid {
    grid-template-columns: 1fr;
  }

  .button {
    width: 100%;
  }

  .focus-panel li,
  .package-row,
  .snapshot-panel div,
  .structure-grid {
    grid-template-columns: 1fr;
  }

  .readme-prose {
    padding: 1rem;
  }

  .site-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}

/* Profile-site alignment overrides. Keep these last so the docs additions above
   inherit the exact component language from sidrichardsquantum.github.io. */
:root {
  --bg: #f7f7f4;
  --surface: #ffffff;
  --surface-muted: #ededeb;
  --text: #1d2328;
  --muted: #5b6670;
  --line: #d7d9d6;
  --accent: #126c83;
  --accent-strong: #0f5364;
  --accent-soft: #dceff3;
  --code-bg: #eef2f1;
  --shadow: 0 18px 45px rgba(34, 41, 47, 0.08);
  --shadow-soft: 0 10px 30px rgba(34, 41, 47, 0.06);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101416;
    --surface: #171d20;
    --surface-muted: #20282b;
    --text: #edf1f2;
    --muted: #a9b4b8;
    --line: #2e393d;
    --accent: #66c5d7;
    --accent-strong: #9eddea;
    --accent-soft: #17333a;
    --code-bg: #11191c;
    --shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
    --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.18);
  }
}

body {
  background: var(--bg);
}

a {
  color: inherit;
}

a:hover {
  color: var(--accent-strong);
}

.brand {
  font-weight: 700;
}

.brand-mark {
  box-shadow: none;
}

.nav-links a {
  border-radius: 6px;
  padding: 0.15rem 0;
}

.section {
  width: min(1120px, calc(100% - 2rem));
  padding: clamp(3rem, 8vw, 6rem) 0;
  scroll-margin-top: 6rem;
}

.hero {
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  min-height: calc(100vh - 5rem);
  padding-top: clamp(3rem, 8vw, 6rem);
}

.hero-copy h1 {
  max-width: 10ch;
  font-size: clamp(4rem, 12vw, 8rem);
  line-height: 0.9;
}

.hero-side {
  display: grid;
  gap: 1rem;
  align-self: center;
}

.hero-visual {
  aspect-ratio: 13 / 9;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow);
}

.hero-visual svg {
  display: block;
  width: 100%;
  height: 100%;
}

.visual-bg {
  fill: var(--surface);
}

.visual-grid {
  opacity: 0.5;
}

.hero-visual pattern path {
  fill: none;
  stroke: var(--line);
  stroke-width: 1;
}

.visual-circuit {
  fill: none;
  stroke: var(--accent-strong);
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 6;
}

.visual-circuit circle,
.visual-circuit rect {
  fill: var(--surface);
}

.visual-labels {
  fill: var(--muted);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 16px;
  font-weight: 800;
}

.focus-panel {
  background: var(--surface);
  box-shadow: var(--shadow);
}

.focus-panel ul {
  padding-left: 1.1rem;
  list-style: disc;
}

.focus-panel li {
  display: list-item;
  color: var(--muted);
}

.snapshot-panel dl {
  display: grid;
  gap: 0.75rem;
  margin: 0;
}

.snapshot-panel div {
  display: grid;
  grid-template-columns: minmax(7.5rem, 0.8fr) minmax(0, 1.2fr);
  gap: 0.8rem;
  align-items: baseline;
  border-top: 1px solid var(--line);
  padding-top: 0.75rem;
}

.snapshot-panel div:first-child {
  border-top: 0;
  padding-top: 0;
}

.snapshot-panel dt {
  color: var(--text);
  font-weight: 800;
}

.snapshot-panel dd {
  margin: 0;
  color: var(--muted);
}

.section-heading {
  max-width: 760px;
  margin-bottom: 1.5rem;
}

.section-heading h2 {
  font-size: clamp(2rem, 5vw, 3.2rem);
  line-height: 1.05;
}

.section-heading p {
  color: var(--muted);
}

.project-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.project-card {
  min-height: 360px;
  gap: 1.25rem;
  background: var(--surface);
}

.project-card h3,
.package-row h3 {
  margin: 0 0 0.6rem;
  font-size: 1.15rem;
  line-height: 1.25;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.tags span {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.22rem 0.55rem;
  background: var(--surface-muted);
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 700;
}

.card-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  border-top: 1px solid var(--line);
  padding-top: 1rem;
}

.card-links a,
.package-row a {
  color: var(--accent-strong);
  font-weight: 800;
  text-decoration: none;
}

.card-links a::after,
.package-row a::after {
  content: " ->";
}

.package-row {
  grid-template-columns: minmax(220px, 1fr) minmax(220px, 0.9fr) auto;
  background: var(--surface);
  box-shadow: none;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.badges img {
  display: block;
  max-width: 100%;
  height: 20px;
}

code {
  display: inline-block;
  overflow-x: auto;
  max-width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.58rem 0.7rem;
  background: var(--code-bg);
  color: var(--text);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 0.9rem;
  white-space: nowrap;
}

.prose code {
  padding: 0.12rem 0.3rem;
  border-radius: 6px;
  white-space: normal;
}

.site-footer {
  padding: 2rem clamp(1rem, 4vw, 3rem);
}

.site-footer a {
  font-weight: 700;
  text-decoration: none;
}

@media (max-width: 880px) {
  .hero {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .hero-side {
    grid-template-columns: minmax(0, 1fr) minmax(280px, 0.8fr);
    align-items: stretch;
  }

  .project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .package-row {
    grid-template-columns: 1fr;
  }

  .snapshot-panel div {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  .section {
    width: min(100% - 1rem, 1120px);
  }

  .hero-copy h1 {
    font-size: clamp(3.4rem, 20vw, 5rem);
  }

  .hero-side,
  .project-grid {
    grid-template-columns: 1fr;
  }

  .project-card {
    min-height: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }

  .button:hover,
  .project-card:hover,
  .project-card:focus-within {
    transform: none;
  }
}
"""


def main() -> None:
    repo = Path.cwd()
    site = repo / "_site"

    if site.exists():
        shutil.rmtree(site)
    site.mkdir()

    if (repo / "images").exists():
        shutil.copytree(repo / "images", site / "images")
    if (repo / "LICENSE").exists():
        shutil.copy2(repo / "LICENSE", site / "LICENSE")
        shutil.copy2(repo / "LICENSE", site / "LICENSE.txt")

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        output_format="html5",
    )
    page_map = {source: output for source, _, output in DOCS}
    nav = nav_html()
    home_cards = build_home_cards(repo)

    for source, label, output in DOCS:
        path = repo / source
        if not path.exists():
            continue

        markdown_text = path.read_text(encoding="utf-8")
        page_title = title_from(markdown_text, label)
        article = render_markdown(markdown_text, page_map, md)

        if output == "index.html":
            article = enhance_home_article(article)
            body = build_home(article, home_cards)
        else:
            body = f"""
            <section class="content section prose">
              {article}
            </section>
            """

        (site / output).write_text(build_layout(page_title, body, nav), encoding="utf-8")

    (site / "styles.css").write_text(CSS, encoding="utf-8")


if __name__ == "__main__":
    main()
