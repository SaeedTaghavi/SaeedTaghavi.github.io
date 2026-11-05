---
title: Publications
hide:
  - navigation
  - toc
---

<div class="st-page-head">
<div>
<p class="st-kicker">Publications</p>
<h1>Papers, theses and abstracts</h1>
<p>Every entry links to its DOI and, where it exists, the code behind it. Citation counts live on Google Scholar.</p>
</div>
<div class="st-actions"><a class="st-btn" href="https://scholar.google.com/citations?user=ew2KPK4AAAAJ">Google Scholar ↗</a><a class="st-btn" href="https://orcid.org/0000-0003-1685-5639">ORCID ↗</a></div>
</div>

<div data-filter-list>
<div class="st-filters">
<div class="st-filter-row"><span>Search</span><input type="search" aria-label="Search publications" placeholder="Title, author or venue"></div>
<div class="st-filter-row" role="group" aria-label="Filter by type"><span>Type</span><button type="button" data-key="type" data-value="all" aria-pressed="true">All</button>
{%- for t in unique(publications, "type") %}<button type="button" data-key="type" data-value="{{ t | slug }}" aria-pressed="false">{{ t }}</button>{% endfor -%}
</div>
<div class="st-filter-row" role="group" aria-label="Filter by theme"><span>Theme</span><button type="button" data-key="theme" data-value="all" aria-pressed="true">All</button>
{%- for t in unique(publications, "theme") if t != "Several themes" %}<button type="button" data-key="theme" data-value="{{ t | slug }}" aria-pressed="false">{{ t }}</button>{% endfor -%}
</div>
</div>
<p class="st-count" data-count>{{ publications | length }} entries</p>
{%- for p in publications %}
<article class="st-pub" data-item data-type="{{ p.type | slug }}" data-theme="{{ p.theme | slug }}" data-text="{{ (p.title ~ ' ' ~ p.authors | join(' ') ~ ' ' ~ p.venue ~ ' ' ~ p.summary) | lower | e }}">
<p class="st-pub__year">{{ p.year }}</p>
<div>
<p class="st-kicker">{{ p.type }} · {{ p.theme }}</p>
<h2>{{ p.title }}</h2>
<p>{% for a in p.authors %}{% if a == "Taghavi S" %}<strong>{{ a }}</strong>{% else %}{{ a }}{% endif %}{% if not loop.last %}, {% endif %}{% endfor %}</p>
<p class="st-venue">{{ p.venue }}</p>
<p class="st-summary">{{ p.summary }}</p>
{%- if p.links %}
<p class="st-links">{% for l in p.links %}<a href="{{ l.url }}">{{ l.label }} ↗</a>{% endfor %}</p>
{%- endif %}
</div>
</article>
{%- endfor %}
</div>
