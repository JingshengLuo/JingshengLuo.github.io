---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

## Education
* **Ph.D. Candidate** (Direct Ph.D.), Xi'an Jiaotong University, 2023 - Present
    * *National Innovation Platform (Center) for Industry-Education Integration of Energy Storage Technology, Xi'an, 710049 China*
* **B.S. in Applied Chemistry**, Tongji University, 2019 - 2023
    * *Department of Chemistry, College of Chemistry Science and Engineering, Shanghai 200092, China*

## Work experience


## Skills
* **Research Focus**: Lithium Metal Batteries, Structure Design, Catalysts, Synthesis, Mechanism Study
* **Technical**: Scientific Visualization, Python 
* **Languages**: English, Spanish 

## Publications
 <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>

## Talks
 <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>

## Teaching
 <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
