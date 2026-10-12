# Quality of the paper archive

How good are the paper counts on the home page? This folder holds the evidence.

| File | Content |
|---|---|
| `summary.yaml` | Results of the latest check (rendered on the About page) |
| `precision-labels-2026-10.csv` | Hand-labelled random sample used for the precision estimate (2020–2026) |
| `precision-labels-2010s-2026-10.csv` | Hand-labelled random sample for the back-filled years (2010–2019, 15 per year) |
| `new-phrases-labels-2026-10.csv` | Hand-labelled sample of papers added by the October 2026 phrases |
| `topic-labels-dev-2026-10.csv` | 60 papers with hand-assigned field-map topics, used to tune the classifier |
| `topic-labels-test-2026-10.csv` | 120 different papers, labelled blind, used only to measure the classifier |
| `quantph-totals.json` | Number of all quant-ph submissions per year (refreshed daily), for the share of QOC |

## Method (October 2026)

The archive was first built for 2020–2026 and then back-filled to 2010 (`fetch_arxiv.py --since 2010-01-01
--until 2019-12-31`); every check below was extended to the full period.

1. **Completeness.** For five months (May 2012, Oct 2017, Mar 2021, Feb 2024, Sep 2026), *all* quant-ph papers
   were downloaded and the selection rule (`qocsite/selection.py`) applied locally; the archive's API pre-filter
   missed none of the 209 matches (`paper_quality.py completeness YYYY-MM`).
   Five months, including the lowest-count ones, were re-fetched independently and matched exactly.
2. **Precision.** A stratified random sample (20 per year, seed 20261011) was labelled by hand:
   `R` about quantum control, `Q` quantum-speed-limit theory (in scope by design), `X` false positive.
   Result: 78% ± 7% (R+Q), with no trend over the years. A second sample for 2010–2019 (15 per year, seed
   20261012 + year) gave 75% ± 7%; all labels together: 76% ± 5%. Two patterns of false positives were then
   excluded from the rule (generic "controllability", programming "control flow"), removing 6 false
   positives and 1 genuine paper from the sample.
3. **Recall.** Reference set: arXiv papers citing core QOC works (Semantic Scholar). Raw recall 56% →
   after adding phrases aligned with the field-map topics (and hyphen-tolerant matching) 61%, flat across
   years; 60% over 2010–2026 (1,848 reference papers). Citing a core paper does not make a paper a QOC paper; in a labelled sample of 40 missed
   papers, 30% were genuine, so the true recall is roughly 70–85%.
4. **New phrases.** A labelled sample of 60 papers added by the new phrases showed that
   "Floquet engineering" and "Hamiltonian engineering" have ~40–50% precision (large physics subfields
   beyond control); they were dropped. The remaining additions: 73% precision (33/45).
5. **Context.** QOC papers rose from 3.3% to 4.4% of all quant-ph submissions between 2010 and 2014 and have
   been ~3.8–4.5% every year since: the field now grows with quantum physics as a whole.

## Topic classification (October 2026)

Papers are placed on the field map by phrase rules (`data/classifier.yaml`, scoring in `qocsite/classify.py`).
Each paper was labelled with the topics it is *about* (method, task, platform), from title and abstract, without
looking at the classifier's output. The rules were tuned on the dev sample (60 papers, seed 101) and frozen; the
test sample (120 other papers, seed 202) then gave **60% precision, 82% recall**, and 89% of the papers received at
least one correct topic. Most false positives are topics a paper mentions in passing (a platform named as an
example, "decoherence" as motivation). One fix prompted by the test errors (generic noise words no longer count
for open-system control) raises precision to 63% on the same — no longer blind — sample.

## Reproduce

```bash
python tools/paper_quality.py precision data/quality/precision-labels-2026-10.csv
python tools/paper_quality.py recall [--since 2010]
python tools/paper_quality.py completeness 2017-10
python tools/paper_quality.py topics data/quality/topic-labels-test-2026-10.csv [-v]
python tools/paper_quality.py share
python tools/paper_quality.py sample --per-year 20 --seed <new seed>   # draw a fresh sample to label
```

## Known limitations

- Keyword selection misses papers that describe control without the usual vocabulary (≈20–30%), and
  includes some that use it in passing (≈20%). Both rates are stable over time, so **trends are reliable**;
  absolute counts are approximate.
- arXiv only: papers not posted on arXiv are not counted.
