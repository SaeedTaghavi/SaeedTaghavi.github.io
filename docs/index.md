---
title: Home
template: home.html
hide:
  - navigation
  - toc
---

<div class="st-intro">
<p>Hello! I'm Saeed Taghavi, a postdoctoral researcher in computational neuroscience at the Zapata-Briceño Institute of Neuroscience in Madrid. I hold a PhD in Physics with a thesis in theoretical neuroscience.</p>
<p>My research asks how timing shapes computation in neural networks: synchrony, oscillations, delays and plasticity, studied in spiking networks and in phase oscillator models. I also apply machine learning to brain data.</p>
<p>I am an engineer as well. Since 2020 I have built production systems, from Kubernetes and CI/CD for digital banking to embedded firmware and biosignal software. Today I build simulation and analysis pipelines for spiking-network and EEG studies.</p>
</div>

<div class="st-section st-section--top">
<div class="st-section__head"><h2 class="st-label">Four sides of the work</h2></div>
<div class="st-panel__grid st-panel__grid--row">
<div class="st-tile"><p><span>01</span><span>Spiking networks</span></p>{% include "tile-spiking.svg" %}</div>
<div class="st-tile"><p><span>02</span><span>Phase oscillators</span></p>{% include "tile-oscillators.svg" %}</div>
<div class="st-tile"><p><span>03</span><span>Machine learning</span></p>{% include "tile-ml.svg" %}</div>
<div class="st-tile"><p><span>04</span><span>Engineering</span></p>{% include "tile-engineering.svg" %}</div>
</div>
</div>

<div class="st-split">
<div>
<p class="st-kicker">01 · Science</p>
<h2>Rhythms, delays and plasticity</h2>
<p class="st-body">Physics-first models of neural populations. I ask when networks synchronise, how external rhythms lock them, and how plasticity tunes the timing of their connections.</p>
<ul class="st-chips"><li>Spiking networks</li><li>Kuramoto models</li><li>Mean-field models</li><li>STDP</li><li>tACS</li><li>EEG</li></ul>
<a class="st-more" href="research/">Research themes →</a>
</div>
<div>
<p class="st-kicker">02 · Engineering</p>
<h2>Infrastructure that runs research</h2>
<p class="st-body">Building production systems since 2020: Kubernetes and CI/CD for digital banking, embedded firmware, biosignal R&amp;D. Today, simulation and analysis pipelines on HPC.</p>
<ul class="st-chips"><li>Python</li><li>C++</li><li>NEST</li><li>Kubernetes</li><li>GitLab CI</li><li>Slurm</li><li>FastAPI</li></ul>
<a class="st-more" href="software/">Software and tools →</a>
</div>
</div>

<div class="st-section">
<div class="st-section__head"><h2 class="st-label">Research themes</h2><a class="st-more" href="research/">All research →</a></div>
<div class="st-cards">
<a class="st-card" href="research/#rhythms-and-entrainment"><div class="st-card__fig">{% include "theme-rhythms.svg" %}</div><div class="st-card__body"><h3>Rhythms and entrainment</h3><p>Why some networks lock to an external rhythm and others resist. Weakly synchronised networks entrain to tACS over a wider band of frequencies.</p><p class="st-card__meta">CSF 2025 · PRR 2026</p></div></a>
<a class="st-card" href="research/#delays-and-plasticity"><div class="st-card__fig">{% include "theme-delays.svg" %}</div><div class="st-card__body"><h3>Delays and plasticity</h3><p>Spike-timing-dependent plasticity prunes connections with distributed conduction delays and keeps those that let activity propagate.</p><p class="st-card__meta">J Neurosci 2026</p></div></a>
<a class="st-card" href="research/#synchrony-on-networks"><div class="st-card__fig">{% include "theme-synchrony.svg" %}</div><div class="st-card__body"><h3>Synchrony on networks</h3><p>Delay-coupled phase oscillators on rings form local synchrony and phase clusters. On 2D sheets, spiking networks carry travelling waves.</p><p class="st-card__meta">ICTP 2024 · Ongoing</p></div></a>
<a class="st-card" href="research/#noise-as-a-resource"><div class="st-card__fig">{% include "theme-noise.svg" %}</div><div class="st-card__body"><h3>Noise as a resource</h3><p>Stochastic resonance in Hodgkin-Huxley neurons and networks with delayed feedback, compared across six circuit motifs.</p><p class="st-card__meta">In progress</p></div></a>
</div>
</div>

<div class="st-section st-latest">
<div>
<div class="st-section__head"><h2 class="st-label">Latest</h2></div>
<ol class="st-news">
{%- for n in news %}
<li><p class="st-date">{{ n.date }}</p><h3><a href="{{ n.url }}">{{ n.title }}</a></h3><p>{{ n.text }}</p></li>
{%- endfor %}
</ol>
</div>
</div>

<div class="st-section">
<div class="st-section__head"><h2 class="st-label">Software and tools</h2><a class="st-more" href="software/">All software →</a></div>
<div class="st-tools">
{%- for s in software if s.home %}
<a class="st-tool" href="{{ s.url or 'software/' }}"><div class="st-tool__head"><h3>{{ s.short or s.name }}</h3><span class="st-tool__link">{{ s.link_label }} ↗</span></div><p>{{ s.description }}</p><p class="st-tags">{{ s.tags | join(" · ") }}</p></a>
{%- endfor %}
</div>
</div>

<div class="st-section" style="border-bottom: 0">
<div class="st-section__head" style="align-items: flex-end">
<div><p class="st-kicker" style="color: var(--st-muted)">Contact</p><p style="margin: 0.4rem 0 0; font-size: clamp(1.1rem, 3vw, 1.5rem); font-weight: 500"><a href="mailto:saeed.taghavi.v@gmail.com" style="color: var(--st-ink)">saeed.taghavi.v@gmail.com</a></p></div>
<a class="st-btn st-btn--primary" href="cv/">CV</a>
</div>
</div>
