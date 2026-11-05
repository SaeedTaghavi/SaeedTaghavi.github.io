---
title: Talks
hide:
  - navigation
  - toc
tags:
  - Phase oscillators
  - Synchrony
  - Brain stimulation
  - Astrophysics
---

<div class="st-page-head">
<div>
<p class="st-kicker">Talks</p>
<h1>Talks and recordings</h1>
<p>Recorded talks with a short note on what each one is about and where it was given. The full list lives on my YouTube channel.</p>
</div>
<a class="st-btn" href="https://www.youtube.com/@saeedtaghavi7209">YouTube channel ↗</a>
</div>

<div data-filter-list>
<div class="st-filters">
<div class="st-filter-row" role="group" aria-label="Filter by audience"><span>Audience</span><button type="button" data-key="audience" data-value="all" aria-pressed="true">All</button>
{%- for a in unique(talks, "audience") %}<button type="button" data-key="audience" data-value="{{ a | slug }}" aria-pressed="false">{{ a }}</button>{% endfor -%}
</div>
</div>
{%- for t in talks %}
<article class="st-talk" data-item data-audience="{{ t.audience | slug }}" data-text="{{ (t.title ~ ' ' ~ t.description) | lower | e }}">
<a class="st-cover" href="https://www.youtube.com/watch?v={{ t.youtube }}" aria-label="Watch {{ t.title }} on YouTube, {{ t.duration }}">
{%- if t.cover %}{% include t.cover %}{% else %}<img src="https://i.ytimg.com/vi/{{ t.youtube }}/hqdefault.jpg" alt="" loading="lazy">{% endif -%}
<span class="st-play" aria-hidden="true"><svg width="20" height="22" viewBox="0 0 20 22"><path d="M3 2 L18 11 L3 20 Z" fill="#111318"></path></svg></span><span class="st-duration">{{ t.duration }}</span></a>
<div>
<p class="st-kicker">{{ t.audience }} · {{ t.theme }}</p>
<h2><a href="https://www.youtube.com/watch?v={{ t.youtube }}">{{ t.title }}</a></h2>
<p class="st-talk__meta">{{ t.date }}{% if t.event %} · {{ t.event }}{% endif %}{% if t.place %} · {{ t.place }}{% endif %}</p>
<p>{{ t.description }}</p>
<p class="st-links"><a href="https://www.youtube.com/watch?v={{ t.youtube }}">Watch on YouTube ↗</a></p>
</div>
</article>
{%- endfor %}
</div>
