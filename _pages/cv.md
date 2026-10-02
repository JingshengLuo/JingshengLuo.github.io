---
layout: archive
title: "Curriculum Vitae"
lede: "Last updated October 2026."
permalink: /cv/
redirect_from:
  - /resume
---

{% include base_path %}

<div class="btn-row" markdown="0">
  <a class="btn btn--accent" href="{{ base_path }}/files/CV_Zhengqian_Jin.pdf" download>Download PDF</a>
  <a class="btn" href="{{ base_path }}/files/CV_Zhengqian_Jin.pdf" target="_blank" rel="noopener">Open in new tab</a>
  <a class="btn" href="{{ base_path }}/publications/">Publication list</a>
</div>

<object class="doc-embed" data="{{ base_path }}/files/CV_Zhengqian_Jin.pdf#view=FitH" type="application/pdf">
  <p class="notice" markdown="0">
    Your browser will not display the embedded PDF — most mobile browsers will not.
    <a href="{{ base_path }}/files/CV_Zhengqian_Jin.pdf">Open the CV directly</a> instead.
  </p>
</object>

## Education

* **Ph.D. Candidate, Electronic Science &amp; Technology** — Xi'an Jiaotong University, 2023 – present<br>
  *National Innovation Platform (Center) for Industry–Education Integration of Energy Storage Technology, Xi'an 710049, China*
* **B.S. in Applied Chemistry** — Tongji University, 2019 – 2023<br>
  *College of Chemistry Science and Engineering, Shanghai 200092, China*

## Skills

* **Research focus** — lithium metal batteries; anode-free cells; interfacial catalysis; SEI and plating/stripping mechanism; high-entropy layered hydroxides
* **Computation** — Python, VASP, Gaussian, Multiwfn, cclib
* **Visualisation** — Blender, Matplotlib/Seaborn, Quarto
* **Languages** — Chinese (native), English, Spanish (learning)

## Publications

<ol class="cv-list" markdown="0">
{% assign cv_pubs = site.publications | sort: 'date' | reverse %}
{% for post in cv_pubs %}
  <li>
    {% if post.authors %}<span class="cv-list__authors">{{ post.authors }}</span>{% endif %}
    <a href="{{ post.permalink | relative_url }}">{{ post.title }}</a>
    {% if post.citation %}<span class="cv-list__venue">{{ post.citation }}</span>{% endif %}
  </li>
{% endfor %}
</ol>

{% if site.teaching.size > 0 %}
## Teaching

<ol class="cv-list" markdown="0">
{% for post in site.teaching reversed %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span class="cv-list__venue">{{ post.type }}{% if post.venue %}, {{ post.venue }}{% endif %}{% if post.date %} · {{ post.date | date: "%Y" }}{% endif %}</span>
  </li>
{% endfor %}
</ol>
{% endif %}

{% if site.talks.size > 0 %}
## Talks

<ol class="cv-list" markdown="0">
{% for post in site.talks reversed %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span class="cv-list__venue">{{ post.type }}{% if post.venue %}, {{ post.venue }}{% endif %}{% if post.date %} · {{ post.date | date: "%Y" }}{% endif %}</span>
  </li>
{% endfor %}
</ol>
{% endif %}
