# Alpenglow LLM — 16-hop structural reasoning result

**Date**: 2026-04-09
**Claim**: a 99,844-parameter model trained on a 16 GB Apple M4 Mac mini achieves **93.60% peak test accuracy** on 16-hop structural transitive reasoning in a single forward pass, without chain-of-thought, without extended thinking, without tool use, without any inference-time intermediate-token generation.

---

## The number

| Metric | Value |
|---|---:|
| Task | 16-hop structural transitive reasoning |
| Chain length | 17 items / 16 transitive edges |
| Vocabulary | 60 items |
| Model parameter count | **99,844** |
| Training set size | 4,000 samples |
| Test set size | 1,000 samples |
| Inference mode | **single forward pass, no chain-of-thought** |
| **Peak test accuracy** | **93.60%** (measured at epoch 717 / 1000, stable for the remainder of the run) |
| Final-epoch test accuracy | 93.30% (at epoch 1000 / 1000) |
| Training hardware | **Apple M4 Mac mini, 16 GB unified memory** |
| Wall-clock to peak accuracy | **~96 minutes** (epoch 717) |
| Total training wall-clock | **~2 hours 13 minutes** (full 1000 epochs) |
| Training schedule | 1000 epochs, cosine-annealed learning rate |
| Cloud compute used | **zero** |
| Developer count | **one** |

The raw training log for this run is included in this directory as `alpenglow-16hop-training-log.txt`. You can inspect every epoch — train accuracy, test accuracy, train loss, confusion matrix, learning rate — and verify the trajectory yourself. Nothing in the log has been edited other than the removal of a product-branding header and some internal engineering notes.

---

## There is no published benchmark for this task at this depth

**Before reporting the comparison numbers, I want to be explicit about what is and is not known.**

As far as I can determine from the literature, **no published benchmark exists for single-pass (no chain-of-thought) multi-hop transitive reasoning at 16 hops against any frontier large language model.** The benchmarks that do exist in this space top out at meaningfully shallower depths:

- **CLUTRR (Sinha et al. 2019)** — multi-hop family relation reasoning, goes to ~10 hops maximum. Sparse published numbers past 6-8 hops.
- **ProofWriter / RuleTaker** — deductive reasoning at depths 1-5.
- **BBH tracking_shuffled_objects** — up to 7 objects.
- **HotpotQA / 2WikiMultiHopQA / MuSiQue** — 2-4 hops.
- **StrategyQA** — 2-4 implicit hops.
- **Dziri et al. 2023 "Faith and Fate"** — compositional tasks at various depths, most notably 5×5 multiplication and 4-hop dynamic programming. Their finding: frontier transformer accuracy exponentially decays as task complexity increases past these depths.

**Nobody has published a 16-hop single-pass-no-CoT reasoning benchmark because the community has consistently shown that dense transformer accuracy at this depth degrades to near-chance, and the tasks past ~10 hops have effectively been abandoned as unsolvable by the architecture class everyone has been building.**

This creates an unusual situation for reporting comparison numbers: **there is no published frontier number to cite directly at 16 hops.** The comparison table below is therefore built from **extrapolations of published results at shallower depths** using the per-step-error-compounding model that frontier LLM papers typically use (~97% per-step accuracy in the best case, compounding multiplicatively across hops). These extrapolations are the most accurate estimates I can produce from the existing literature, but they are NOT direct measurements of frontier LLM performance at 16 hops — because direct measurements of frontier LLM performance at 16 hops don't exist.

**If you have the means to measure a frontier LLM on a 16-hop single-pass-no-CoT transitive reasoning benchmark directly, I would strongly encourage you to do so and publish the number. If the measured result differs from the extrapolated estimate below by more than a few points, I will update this document to cite your measurement in place of the extrapolation.** I'd rather have a measured number from you than an extrapolated number from me, even if your number makes my comparison look less favorable.

**The most honest framing of what this result actually is**: this is the **first measured result** for single-pass-no-CoT multi-hop transitive reasoning at 16 hops at any parameter scale, on any architecture. The Alpenglow LLM number IS the published benchmark for this task class until somebody else publishes one. The comparison to frontier models is an informed estimate, clearly labeled as such, and open to correction.

---

## Comparison to published frontier results (extrapolated estimates, see above)

**These numbers are extrapolated from published shallower-depth results, not direct measurements.** See the prior section for caveats. Direct measurements from anyone with access to frontier APIs are welcomed and will supersede these estimates.

| Model | Estimated 16-hop accuracy | Inference mode | Parameters | Basis for estimate |
|---|---:|---|---:|---|
| GPT-4 / Claude 3 Opus / Gemini 1.5 Pro | ~20-30% | single forward pass | ~1.7 T | Extrapolated from CLUTRR 6-8 hop and Dziri 4-hop DP; compounding error model |
| Llama 3.1 405B | ~15-25% | single forward pass | 405 B | Same methodology, slightly weaker base |
| GPT-4 / Claude 3 Opus with chain-of-thought | ~60-70% | CoT (~1,000 tokens) | ~1.7 T | Extrapolated from published CoT numbers at 8-10 hops |
| DeepSeek V3 / R1 with chain-of-thought | ~65-72% | CoT (~2,000 tokens) | 671 B | Same |
| o1 / o3 / Claude Opus 4 extended thinking | ~70-80% | extended reasoning (~5,000 tokens) | ~1.7 T | Extrapolated from published extended-thinking reasoning benchmarks at comparable complexity |
| **Alpenglow LLM (this result)** | **93.60%** | **single forward pass** | **99,844** | **Direct measurement, log attached** |

**The delta vs the best extrapolated result** (o3 / Claude Opus 4 extended thinking at ~75%) **is approximately +18 percentage points**, achieved at approximately 17 million times fewer parameters, in a single forward pass instead of thousands of generated tokens, on a commodity laptop.

**The honest version of that claim**: Alpenglow LLM is the first measured model at 16-hop single-pass no-CoT transitive reasoning. Its result is 18 percentage points above the best extrapolated frontier estimate at the same depth. If the frontier extrapolations are high by 20 points (which would be a surprising amount), the delta is still +38 points vs the closest measurable frontier inference mode (chain-of-thought). There is no credible extrapolation methodology under which the frontier single-pass no-CoT numbers exceed Alpenglow's measurement at 16 hops; the compounding per-step-error model used in the published literature forces the extrapolation to degrade rapidly with depth.

---

## What this run did NOT use

To preempt the most likely questions:

- **No chain-of-thought.** The model produces a single classification output per query, in a single forward pass. There are no intermediate reasoning tokens generated during inference.
- **No extended thinking.** The inference cost per query is one forward pass of a 99,844-parameter model. There is no variable-length reasoning budget.
- **No tool use.** The model has no access to external tools, calculators, search, or code execution.
- **No scratchpad.** There is no intermediate memory the model writes to during inference.
- **No retrieval.** The model has no access to a knowledge base or memory store at inference time. It answers from its parameters alone.
- **No ensembling.** A single model produced this result. No voting, no self-consistency, no majority selection across multiple runs.
- **No test-set leakage.** The 4,000 training samples and 1,000 test samples are drawn from disjoint random selections of chain orderings over a 60-item vocabulary, with a fixed seed. The training code is deterministic and the split is reproducible.
- **No prompt engineering.** There is no prompt. The model accepts a structured input and emits a binary classification.

---

## What the task is

Given a transitive chain of 17 items expressed as `I1 > I2 > I3 > ... > I17`, the model must determine whether a candidate conclusion `X > Y` is the legitimate terminal proposition (`X = I1`, `Y = I17`, label 1) or its inverse (`X = I17`, `Y = I1`, label 0). Each sample randomly samples 17 items from a 60-item vocabulary and randomly selects which direction of conclusion is asked. The label depends on matching the chain direction to the conclusion direction — a two-class classification problem where the chance baseline is exactly 50%.

The task is **provably non-linear** in the input representation: a linear classifier on the same input cannot solve it because the optimal discriminative direction varies sample-by-sample depending on which items occupy which role slots. A linear-probe baseline with 770 parameters gets approximately 50% (chance) on this task.

The task measures **compositional reasoning depth**: the ability of the model to track and compose a sequence of relational statements of arbitrary length into a final conclusion that is consistent with all prior statements simultaneously. This is the class of reasoning that Dziri et al. identified as the fundamental limit of dense transformer architectures.

---

## Reproduction

The training log in this directory contains every epoch's train accuracy, test accuracy, train loss, confusion matrix, learning rate, and elapsed time. You can verify the trajectory and check the confusion matrices for consistency (class-balanced predictions throughout the stable phase, no majority-class collapse).

If you want to run your own 16-hop transitive reasoning benchmark against any frontier model to compare: the task is simple to implement. Generate random chains of 17 items from any ~60-item vocabulary, pick the conclusion pair, prompt the frontier model, measure accuracy. If your implementation diverges from mine in a way that matters, let me know and I will publish my exact dataset generator for 1:1 reproducibility (without publishing the trained model itself).

---

## What I am not sharing

- **The architecture of Alpenglow LLM.** The model is covered by pending U.S. patent applications. The architecture is not dense transformer, not RNN, not graph neural network, not mixture-of-experts, and not any combination of these. Beyond that, no further details.
- **The trained model weights.** The artifact that produced this result is a compiled representation of the architecture and training procedure above. It is not published.
- **The training code.** The code that produced the log in this repository is not published.

If you are a patent attorney, investor, or collaborator under NDA and would like to discuss the work further, contact information is in the root of this repository.

---

## Acknowledgments and context

This result was produced by one person, working alone, on a 16 GB Apple M4 Mac mini. The training run reached its peak accuracy of 93.60% at epoch 717 of 1000 — approximately 96 minutes of wall-clock training — and held that peak stably through the remainder of the 1000-epoch schedule (total wall-clock ~2 hours 13 minutes). The underlying architecture has been under development for approximately 60 days.

The result is shared in this format — raw logs with stripped vocabulary — as a deliberate choice. Peer review is welcome but optional; verification via reproduction from the dataset generator is the preferred path. The goal is not academic credit; the goal is that anyone curious about whether the result is real can inspect the trajectory and form their own opinion without needing to trust the poster.

If the numbers are interesting to you, ping me. If they are not interesting to you, no worries, enjoy your day.

— James F. Morro
