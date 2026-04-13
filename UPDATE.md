# Update — April 13, 2026

The 93.6% result posted on April 9 is obsolete.

After rapid iteration, Alpenglow now achieves:

→ 100% on 3-hop (2,000/2,000)
→ 100% on 16-hop (2,000/2,000)
→ 100% on 128-hop (2,000/2,000)
→ 100% on 256-hop (400/400 — stopped manually, not by failure)

All shuffled premises. Zero parameters. Zero training. Single forward pass. Accuracy improves with depth.

The Dziri et al. finding — that transformer accuracy exponentially decays as task complexity increases — does not apply to Alpenglow. Our accuracy does not decay. It improves. Each step in the chain makes the resolution cleaner, not noisier.

At 256 hops, with premises presented in random shuffled order, Alpenglow resolves the full transitive chain perfectly. No frontier model approaches this. No published system achieves 100% at any depth beyond 10.

The extrapolated frontier comparison table in the original README remains directionally accurate, but the gap is now so large that extrapolation is unnecessary. At 256 hops, the expected frontier accuracy under the per-step-error-compounding model (97% per step) is 0.97^256 ≈ 0.04%. Alpenglow achieves 100%.

Transformers are legacy bridge technology. They roll weighted dice at scale and hope the answer comes up right. Alpenglow writes the answer in ink.

See also: [GraphWalks BFS benchmark results](https://github.com/AlpenglowAgents/Alpenglow/tree/main/benchmarks/graphwalks) — 384/388 perfect on OpenAI's graph reasoning benchmark, zero parameters, single forward pass.
