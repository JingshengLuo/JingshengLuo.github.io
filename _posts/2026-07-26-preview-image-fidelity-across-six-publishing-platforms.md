---
title: "Preview Image Fidelity Across Six Publishing Platforms"
date: 2026-07-26
permalink: /posts/2026/07/preview-image-fidelity/
status: "Preprint"
authors: "Zhengqian Jin<sup>1,*</sup>"
venue: "Opinion · not submitted for formal publication"
read_time: false
summary: "Six publishers, one question: what image actually reaches a social preview card, and at what resolution? Presence of an og:image is not the same thing as a legible card — and the four ways it fails need four different fixes."
description: "An opinion piece on Open Graph metadata quality in scholarly publishing: measured preview-image dimensions, aspect ratios and declared card types across ACS, Nature, Cell Press, Wiley, RSC and arXiv."
header:
  image: /images/og-preview-fidelity.jpg
  teaser: /images/og-preview-fidelity.jpg
tags:
  - Scholarly communication
  - Metadata
  - Open Graph
---

<p class="affiliation" markdown="0">
  <sup>1</sup> National Innovation Platform (Center) for Industry–Education Integration of Energy
  Storage Technology, School of Chemistry, Engineering Research Center of Energy Storage
  Materials and Devices, State Key Laboratory for Electrical Insulation and Power Equipment,
  Xi&rsquo;an Jiaotong University, Xi&rsquo;an 710049, China<br>
  <sup>*</sup> Corresponding author: <a href="mailto:omwtbarca@gmail.com">omwtbarca@gmail.com</a>
</p>

<div class="notice" markdown="1">
**Preprint.** This note is posted here as a preprint and is not intended for formal
publication. Cite it as: Z. Jin, *Preview Image Fidelity Across Six Publishing Platforms*,
2026, <https://jingshengluo.github.io/posts/2026/07/preview-image-fidelity/>
</div>

<div class="btn-row" markdown="0">
  <a class="btn btn--accent" href="/files/preview-image-fidelity-jin-2026.pdf" target="_blank" rel="noopener">Download PDF</a>
</div>

## I. Background and Scope

When a link to a research article is posted to X, LinkedIn, Slack, or a messaging application, the platform generates a preview card. The image that appears on that card, together with the resolution at which it is displayed, is determined by a small set of HTML metadata elements placed in the landing page of the publisher, principally `og:image` and `twitter:card` [1].

Most authors never see these elements. A graphical abstract is prepared in accordance with the submission guidelines, it is uploaded, and the article appears online. The manner in which that image is subsequently delivered to a preview crawler is not shown in the proofs, and it is not communicated at any later stage.

This note reports a small set of observations concerning the images that six publishing platforms in the energy and materials literature deliver to preview cards. It further proposes that one property of those images, referred to here as *fidelity*, may merit attention alongside the properties that have already been measured.

Several boundaries should be stated at the outset. No comment is offered on the design quality of any graphical abstract, which is properly a matter for authors and editors. Nor is it suggested that social platforms constitute a primary channel for scholarly communication, since they plainly do not. The subject of this note is narrower. It concerns what happens to an image asset already held by a publisher along the technical path that leads to a preview card. No claim is made regarding click-through rates, reach, or citation, and it should be recalled that the relationship between attention on social platforms and subsequent citation has been found to be weak and to vary considerably by field [2, 3]. The observations reported here were made by authors rather than by publishing technologists, and they describe only what can be observed from outside the systems of a publisher. Correction from colleagues with visibility into these workflows would be welcome.

## II. Metadata Basis of Preview Card Generation

Card generation depends entirely on metadata contained in the `<head>` element of the landing page. The `og:image` property identifies the image to be displayed. The `twitter:card` property declares the form of the card, in that a value of `summary_large_image` produces a wide banner, whereas a value of `summary` produces a small square thumbnail. The optional properties `og:image:width` and `og:image:height` allow a crawler to determine the dimensions of the image without downloading the file [1].

These elements do not form part of the article XML that is prepared according to the JATS standard. They belong instead to the page template layer, which on most platforms is generated centrally by the hosting system rather than separately for each article.

## III. Prior Measurement and Remaining Gaps

Jones, Weigle, Klein and Nelson [4] conducted what remains, to the best of our knowledge, the most systematic measurement in this area. Landing pages were retrieved for 110,900 articles drawn from 1,109 journals across 209 publishers. It was reported that only 36.74% of articles were able to generate a complete card including an image on Twitter, and 77.86% on Facebook. Among the articles that were able to do so, 73.98% reused the same `og:image` value as another article, most often a logo of the journal or of the publisher, and 51.6% of journals used a single `og:image` URL for every article.

That study measured *presence*, in the sense of whether the tag exists and whether the image is specific to the article. This is the necessary first question. Presence, however, is a necessary rather than a sufficient condition. A page may satisfy all of the checks described above — an `og:image` is declared, the image is specific to the article, and the image is not a logo — and the resulting card may nonetheless remain difficult to read. The pixel dimensions of the image, the aspect ratio of the image, and the consistency of the image with the declared card type do not appear to have been measured. These properties are referred to collectively in this note as *fidelity*.

## IV. Observations Across Six Platforms

The image delivered to the preview card was recorded for one article on each of six platforms in the energy and materials literature, together with the declared card type.

| Platform | Image (px) | Aspect | Size | `twitter:card` |
|:---|:---|:---|:---|:---|
| ACS | 900 × 471 | 1.911 | 47 KB | not declared |
| Nature | 900 × 820 | 1.098 | 103 KB | `summary_large_image` |
| Cell Press | 507 × 211 | 2.403 | 29 KB | not declared |
| Wiley | 473 × 432 | 1.095 | 90 KB | `summary_large_image` |
| RSC | 189 × 189 | 1.000 | 15 KB | not declared |
| arXiv | no article image | n/a | n/a | `summary` |

*Table 1. Images delivered to social preview cards for one article on each of six platforms, recorded on 26 July 2026.*

Six examples cannot support any claim concerning prevalence, and no such claim is offered here. They are illustrative, and they are simply the cases that were encountered. What they do suggest is that a poor preview is not a single phenomenon. At least four distinct situations appear to be involved, of which only the first is addressed by measurement based on presence.

The **first** situation is the absence of an article image, as in the case of arXiv, which supplies a logo rather than an image drawn from the article. The **second** is limited resolution, in that the images supplied by RSC at 189 px, by Wiley at 473 px, and by Cell Press at 507 px are narrow in relation to the width at which a wide card is rendered. The **third** is a mismatch of aspect ratio. The images supplied by Wiley and by Nature, at 1.095 and 1.098 respectively, are close to square, whereas the image supplied by Cell Press, at 2.403, is considerably wider than a typical card region. Of the six, only the image supplied by ACS, at 1.911, approaches the proportions of a wide card, and cropping or letterboxing therefore follows in the remaining cases. The **fourth** situation is the absence of declared dimensions, since with the exception of arXiv none of the pages examined declared either `og:image:width` or `og:image:height`.

The distinction may be of practical use, because the remedies differ considerably. The first and fourth situations require only that a metadata element be added. The third requires a change to the page template. The second requires that a different rendition of the image be generated, which constitutes a change to the asset pipeline rather than to a configuration value.

Two of the six cases were examined more closely, and they differ in an instructive manner. In the first, only one rendition of the image appears to exist. For one article hosted on the Wiley platform, four URL variants of the asset holding the graphical abstract, carrying the suffixes `-m`, `-l` and `-f` together with a form carrying no suffix, returned files with identical MD5 checksums, as did the thumbnail displayed on the article page itself. A single rendition therefore appears to be available, measuring 473 by 432 px. The copy cached by the social platform was identical to the file supplied by the publisher at the level of individual pixels, which indicates that no resampling was performed on the side of the platform. For context, the graphics guidance issued by the journal concerned states that a bitmap image for the Table of Contents in the 55 by 50 mm format should be 650 pixels wide [5]. The two figures are noted here without any attribution of intent.

In the second case, two renditions exist. For one article hosted on the Springer Nature platform, the same figure is referenced twice with different size variants. The property `og:image` points to a rendition measuring 685 by 623 px, whereas the property `twitter:image` points to a rendition measuring 1748 by 1592 px. Because precedence is given to `twitter:image` by that social platform, the larger file is retrieved there, whereas tools that read only `og:image` retrieve the smaller one. The same article is therefore presented at different fidelity on different platforms, and a rendition of higher resolution demonstrably exists.

The contrast between these two cases may be relevant to anyone considering a remedy. In the first, a suitable rendition does not appear to have been generated at any point. In the second, such a rendition exists but is not referenced by `og:image`.

## V. Implications for Authors and Publishers

An author follows the submission guidance and supplies a compliant image, and the work is subsequently represented in public by a rendition that is smaller, or differently proportioned, than the one that was submitted. The author is not informed, the difference is not visible in the proofs, and no evident route to correction exists.

The same layer of metadata is increasingly used for purposes beyond social cards, including the unfurling of links within collaboration tools and the extraction of content by the automated retrieval and summarisation systems that are becoming part of ordinary reading workflows [6]. This layer therefore sits alongside the other machine-readable descriptions of an article, such as the records maintained through Crossref [7] and the link relations that allow a machine to traverse from a landing page to the associated resources [8], all of which are expected to be actionable by machines rather than only by human readers [9]. To the extent that this trend continues, the question is gradually becoming less a matter of appearance alone.

Three suggestions are offered tentatively. For publishers and for providers of hosting platforms, checks on metadata quality might usefully be extended to include the properties associated with fidelity — pixel dimensions, aspect ratio, and consistency with the declared card type — rather than being confined to the presence of the tags themselves. For authors, pasting the DOI into any tool that renders a preview, once the article is online, is at present the only straightforward means of observing how the work will appear. For researchers, the prevalence of the four situations described above is unknown, and a systematic audit would be informative.

## Data Availability

The metadata values and the image measurements reported in this note were recorded on 26 July 2026. The elements concerned are present in the public landing page of any article on the platforms discussed and may be inspected directly in the page source.

## Conflict of Interest

The author declares no conflict of interest.

## References

<ol class="references" markdown="0">
  <li>Open Graph Protocol. <i>The Open Graph Protocol</i>. <a href="https://ogp.me/">https://ogp.me/</a> (accessed 26 July 2026).</li>
  <li>M. Thelwall, S. Haustein, V. Larivière, C. R. Sugimoto. Do altmetrics work? Twitter and ten other social web services. <i>PLOS One</i> <b>8</b>, e64841 (2013). <a href="https://doi.org/10.1371/journal.pone.0064841">doi:10.1371/journal.pone.0064841</a></li>
  <li>R. Costas, Z. Zahedi, P. Wouters. Do "altmetrics" correlate with citations? Extensive comparison of altmetric indicators with citations from a multidisciplinary perspective. <i>J. Assoc. Inf. Sci. Technol.</i> <b>66</b>, 2003–2019 (2015). <a href="https://doi.org/10.1002/asi.23309">doi:10.1002/asi.23309</a></li>
  <li>S. M. Jones, M. C. Weigle, M. Klein, M. L. Nelson. Automatically selecting striking images for social cards. <i>13th ACM Web Sci. Conf.</i> 36–45 (2021). <a href="https://doi.org/10.1145/3447535.3462505">doi:10.1145/3447535.3462505</a></li>
  <li>Wiley-VCH. <i>Graphics FAQ: How should I prepare an image for the graphical Table of Contents?</i> <a href="https://onlinelibrary.wiley.com/page/journal/15214095/homepage/graphics-faq/index.html">Advanced Materials</a> (accessed 26 July 2026).</li>
  <li>Z. Lin. FOCUS: an AI-assisted reading workflow for information overload. <i>Nat. Biotechnol.</i> <b>43</b>, 2070–2075 (2025). <a href="https://doi.org/10.1038/s41587-025-02947-8">doi:10.1038/s41587-025-02947-8</a></li>
  <li>G. Hendricks, D. Tkaczyk, J. Lin, P. Feeney. Crossref: the sustainable source of community-owned scholarly metadata. <i>Quant. Sci. Stud.</i> <b>1</b>, 414–427 (2020). <a href="https://doi.org/10.1162/qss_a_00022">doi:10.1162/qss_a_00022</a></li>
  <li>H. Van de Sompel, M. Nelson. Reminiscing about 15 years of interoperability efforts. <i>D-Lib Mag.</i> <b>21</b> (2015). <a href="https://doi.org/10.1045/november2015-vandesompel">doi:10.1045/november2015-vandesompel</a></li>
  <li>M. D. Wilkinson <i>et al.</i> The FAIR Guiding Principles for scientific data management and stewardship. <i>Sci. Data</i> <b>3</b>, 160018 (2016). <a href="https://doi.org/10.1038/sdata.2016.18">doi:10.1038/sdata.2016.18</a></li>
</ol>
