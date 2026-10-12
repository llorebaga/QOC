# Quality of the paper archive

How good are the paper counts on the home page? This folder holds the evidence.

| File | Content |
|---|---|
| `summary.yaml` | Results of the latest check (rendered on the About page) |
| `precision-labels-2026-10.csv` | Hand-labelled random sample used for the precision estimate |
| `new-phrases-labels-2026-10.csv` | Hand-labelled sample of papers added by the October 2026 phrases |
| `quantph-totals.json` | Number of all quant-ph submissions per year (refreshed daily), for the share of QOC |

## Method (October 2026)

1. **Completeness.** For three months, *all* quant-ph papers were downloaded and the selection rule
   (`qocsite/selection.py`) applied locally; the archive's API pre-filter missed none of the matches.
   Five months, including the lowest-count ones, were re-fetched independently and matched exactly.
2. **Precision.** A stratified random sample (20 per year, seed 20261011) was labelled by hand:
   `R` about quantum control, `Q` quantum-speed-limit theory (in scope by design), `X` false positive.
   Result: 78% ± 7% (R+Q), with no trend over the years. Two patterns of false positives were then
   excluded from the rule (generic "controllability", programming "control flow"), removing 6 false
   positives and 1 genuine paper from the sample.
3. **Recall.** Reference set: arXiv papers citing core QOC works (Semantic Scholar). Raw recall 56% →
   after adding phrases aligned with the field-map topics (and hyphen-tolerant matching) 61%, flat across
   years. Citing a core paper does not make a paper a QOC paper; in a labelled sample of 40 missed
   papers, 30% were genuine, so the true recall is roughly 70–85%.
4. **New phrases.** A labelled sample of 60 papers added by the new phrases showed that
   "Floquet engineering" and "Hamiltonian engineering" have ~40–50% precision (large physics subfields
   beyond control); they were dropped. The remaining additions: 73% precision (33/45).
5. **Context.** QOC papers are ~4–4.5% of all quant-ph submissions every year: the field grows with
   quantum physics as a whole.

## Reproduce

```bash
python tools/paper_quality.py precision data/quality/precision-labels-2026-10.csv
python tools/paper_quality.py recall
python tools/paper_quality.py share
python tools/paper_quality.py sample --per-year 20 --seed <new seed>   # draw a fresh sample to label
```

## Known limitations

- Keyword selection misses papers that describe control without the usual vocabulary (≈20–30%), and
  includes some that use it in passing (≈20%). Both rates are stable over time, so **trends are reliable**;
  absolute counts are approximate.
- arXiv only: papers not posted on arXiv are not counted.
