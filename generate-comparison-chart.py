#!/usr/bin/env python3
"""
Generate the Alpenglow LLM 16-hop comparison chart for the release.

Produces a 16:9 horizontal bar chart comparing frontier LLM performance on
16-hop structural transitive reasoning to Alpenglow LLM, with clear visual
separation between inference modes (single pass, chain-of-thought, extended
thinking) and the Alpenglow row.

Design principles:
  - Factual tone, minimal snark in the chart itself
  - Alpenglow bar is bright and visually dominant
  - Parameter counts annotated on each bar (the "17 million times fewer"
    framing should be visible without reading the text)
  - Inference mode clearly labeled (the "no CoT" framing is the headline)
  - Estimates clearly distinguished from measurements (hatch pattern vs solid)
  - No architecture-identifying vocabulary anywhere on the chart

Usage:
  python generate-comparison-chart.py [--final-accuracy 93.6]

Output: alpenglow-16hop-comparison.png (1920x1080, Twitter-optimized)
"""

import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def generate_chart(final_accuracy: float, output_path: str = "alpenglow-16hop-comparison.png"):
    # Data — rows ordered from worst to best so Alpenglow lands on top.
    # All frontier numbers are estimates extrapolated from published
    # shallower-depth benchmarks via per-step-error compounding model.
    # Alpenglow number is measured from the training log.
    rows = [
        # (name, accuracy, mode, params_str, is_measured)
        ("Llama 3.1 405B",                         22, "single forward pass",      "405 B",   False),
        ("GPT-4 / Claude 3 Opus / Gemini 1.5 Pro", 27, "single forward pass",      "~1.7 T",  False),
        ("GPT-4 / Claude 3 Opus\n(chain-of-thought)", 65, "CoT (~1,000 tokens)",      "~1.7 T",  False),
        ("DeepSeek V3 / R1\n(chain-of-thought)",      70, "CoT (~2,000 tokens)",      "671 B",   False),
        ("o1 / o3 / Claude Opus 4\n(extended thinking)", 75, "extended (~5,000 tokens)", "~1.7 T",  False),
        ("Alpenglow LLM",                          final_accuracy, "single forward pass",      "99,844", True),
    ]

    names = [r[0] for r in rows]
    accs = [r[1] for r in rows]
    modes = [r[2] for r in rows]
    params = [r[3] for r in rows]
    measured = [r[4] for r in rows]

    # Color by inference mode
    def color_for_mode(mode, is_measured):
        if is_measured:
            return "#00c853"  # bright green for the measured Alpenglow bar
        if "single" in mode:
            return "#b71c1c"  # deep red — single pass, frontier fails here
        if "CoT" in mode:
            return "#ef6c00"  # orange — chain of thought, frontier starts working
        if "extended" in mode:
            return "#fbc02d"  # yellow — extended thinking, frontier ceiling
        return "#888888"

    colors = [color_for_mode(m, me) for m, me in zip(modes, measured)]

    # Figure setup — 16:9 for Twitter
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0d0d0d")
    ax.set_facecolor("#0d0d0d")

    # Build bars
    y_positions = np.arange(len(rows))
    bars = ax.barh(
        y_positions,
        accs,
        color=colors,
        edgecolor="white",
        linewidth=1.5,
        height=0.68,
    )

    # Hatch the estimated bars to distinguish from measured
    for bar, is_measured in zip(bars, measured):
        if not is_measured:
            bar.set_hatch("////")
            bar.set_alpha(0.78)

    # Axis styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(names, color="white", fontsize=13, fontweight="normal")
    ax.set_xlim(0, 105)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xticklabels([f"{x}%" for x in range(0, 101, 10)], color="#aaaaaa", fontsize=11)
    ax.set_xlabel("Test accuracy on 16-hop structural transitive reasoning",
                  color="#cccccc", fontsize=13, labelpad=14)

    # Hide unnecessary spines
    for spine_name in ("top", "right", "left"):
        ax.spines[spine_name].set_visible(False)
    ax.spines["bottom"].set_color("#444444")
    ax.tick_params(axis="both", colors="#888888", length=0)
    ax.grid(axis="x", color="#222222", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    # Annotate each bar with accuracy + params + mode
    for i, (bar, acc, mode, param, is_measured) in enumerate(
        zip(bars, accs, modes, params, measured)
    ):
        y = bar.get_y() + bar.get_height() / 2
        # Accuracy % — large white text right after the bar end
        acc_text = f"{acc}%"
        if is_measured:
            acc_text = f"{acc:.1f}%"
        ax.text(
            acc + 1.2, y,
            acc_text,
            color="white",
            fontsize=15,
            fontweight="bold",
            va="center",
            ha="left",
        )
        # Params + mode annotation inside the bar near the right end
        annotation = f"{param}  ·  {mode}"
        text_color = "white" if is_measured else "#f0f0f0"
        # Put the annotation inside the bar if it fits, otherwise just outside
        if acc > 30:
            ax.text(
                acc - 1.5, y,
                annotation,
                color=text_color,
                fontsize=10,
                fontweight="normal" if not is_measured else "bold",
                va="center",
                ha="right",
            )
        else:
            ax.text(
                acc + 11, y,
                annotation,
                color="#cccccc",
                fontsize=10,
                va="center",
                ha="left",
            )

    # Title
    fig.text(
        0.5, 0.96,
        "16-hop structural transitive reasoning",
        color="white",
        fontsize=22,
        fontweight="bold",
        ha="center",
    )
    fig.text(
        0.5, 0.915,
        "Single forward pass. No chain-of-thought. No extended thinking. No tools.",
        color="#e0e0e0",
        fontsize=14,
        ha="center",
    )

    # Footer — citation, caveat, link pointer
    fig.text(
        0.02, 0.048,
        '"Transformers\' performance on compositional tasks will exponentially decay as task complexity increases."',
        color="#aaaaaa",
        fontsize=10,
        fontstyle="italic",
        ha="left",
    )
    fig.text(
        0.02, 0.023,
        "     — Dziri et al. 2023, \"Faith and Fate: Limits of Transformers on Compositionality\"",
        color="#888888",
        fontsize=10,
        ha="left",
    )

    fig.text(
        0.98, 0.048,
        "Hatched bars: estimated from published shallower-depth benchmarks.",
        color="#aaaaaa",
        fontsize=9,
        ha="right",
    )
    fig.text(
        0.98, 0.028,
        "Solid bar: measured from training log, released alongside this chart.",
        color="#aaaaaa",
        fontsize=9,
        ha="right",
    )
    fig.text(
        0.98, 0.008,
        "Hardware: Apple M4 Mac mini, 16 GB unified memory, ~96 min to peak accuracy, single process.",
        color="#888888",
        fontsize=9,
        ha="right",
    )

    # Tight layout with padding for title/footer
    plt.subplots_adjust(left=0.20, right=0.96, top=0.88, bottom=0.12)

    plt.savefig(
        output_path,
        dpi=120,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.3,
    )
    print(f"Chart written: {output_path}")
    print(f"Dimensions: {fig.get_size_inches()} inches @ 120 dpi = {int(fig.get_size_inches()[0] * 120)} x {int(fig.get_size_inches()[1] * 120)} px")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final-accuracy", type=float, default=93.6,
                    help="Alpenglow LLM final test accuracy, percent")
    ap.add_argument("--output", type=str, default="alpenglow-16hop-comparison.png",
                    help="Output PNG path")
    args = ap.parse_args()
    generate_chart(args.final_accuracy, args.output)


if __name__ == "__main__":
    main()
