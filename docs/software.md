---
title: Software
hide:
  - navigation
  - toc
---

<div class="st-page-head">
<div>
<p class="st-kicker">Software</p>
<h1>Code, teaching and systems in production</h1>
<p>The code behind each paper is public, and so is the teaching material. Production systems are listed with what I built and the stack they run on.</p>
</div>
</div>

{% for g in unique(software, "group") %}
<section class="st-group">
<h2 class="st-label">{{ g }}</h2>
<div class="st-group__body">
{%- for s in software if s.group == g %}
<a class="st-tool" href="{{ s.url or '#' }}"><div class="st-tool__head"><h3>{{ s.name }}</h3><span class="st-tool__link">{{ s.link_label }}{% if s.url %} ↗{% endif %}</span></div><p>{{ s.description }}</p><p class="st-tags">{{ s.tags | join(" · ") }}</p></a>
{%- endfor %}
</div>
</section>
{% endfor %}

<section class="st-group">
<h2 class="st-label">Engineering experience</h2>
<div class="st-group__body">
<ol class="st-timeline">
<li><p class="st-when">2024 – now</p><div><h3>Postdoctoral researcher · Zapata-Briceño Institute</h3><p>Simulation and analysis pipelines for spiking-network and EEG studies.</p></div></li>
<li><p class="st-when">2022 – 2024</p><div><h3>DevOps engineer · Fardap</h3><p>Kubernetes, CI/CD and monitoring for digital-banking infrastructure.</p></div></li>
<li><p class="st-when">2020 – 2022</p><div><h3>R&amp;D engineer · Anea3D</h3><p>3D body scanning and biosignal analysis of ECG, PPG and HRV, in C# and WPF.</p></div></li>
<li><p class="st-when">2020</p><div><h3>Firmware developer · IDA</h3><p>Embedded IoT and SCADA firmware in C and C++.</p></div></li>
</ol>
</div>
</section>

<section class="st-group">
<h2 class="st-label">Stack</h2>
<div class="st-group__body" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(13rem, 100%), 1fr)); gap: 1.4rem 1.6rem">
<div><p style="margin: 0 0 0.5rem; font-weight: 600">Languages</p><ul class="st-chips"><li>Python</li><li>C++</li><li>Fortran</li><li>MATLAB</li></ul></div>
<div><p style="margin: 0 0 0.5rem; font-weight: 600">Simulation</p><ul class="st-chips"><li>NEST</li><li>NEURON</li><li>NetPyNE</li><li>Brian2</li></ul></div>
<div><p style="margin: 0 0 0.5rem; font-weight: 600">Brain data</p><ul class="st-chips"><li>MNE-Python</li><li>FreeSurfer</li><li>Brainstorm</li></ul></div>
<div><p style="margin: 0 0 0.5rem; font-weight: 600">Infrastructure</p><ul class="st-chips"><li>Docker</li><li>Kubernetes</li><li>Ansible</li><li>GitLab CI</li><li>Slurm</li><li>Prometheus</li><li>Grafana</li><li>PostgreSQL</li></ul></div>
</div>
</section>
