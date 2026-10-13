"""Export the figures used in the book, from original source files, as WebP.
Usage: python -I export_figs.py <src_root> <out_dir>
Each entry: key -> list of panels; panel = (paper_dir, relative_path, options)
options: trim=(left,bottom,right,top) in cm (LaTeX order), page=1-based page index.
"""
import os, sys
import fitz
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
CM = 28.3465

P = {
    # EWC (arXiv 1612.00796)
    "ewc-1": [("1612.00796", "depiction_ewc.pdf", {})],
    "ewc-2": [("1612.00796", "permuteMNIST.pdf", {})],
    "ewc-3": [("1612.00796", "atari10_performance.pdf", {})],
    # Three types (PMC9771807, Nature Machine Intelligence, CC BY 4.0)
    "tt-1": [("hires", "tt_Fig1_HTML.png", {})],
    "tt-2": [("hires", "tt_Fig2_HTML.png", {})],
    "tt-3": [("hires", "tt_Fig3_HTML.png", {})],
    "tt-ed1": [("PMC9771807", "fig/42256_2022_568_Fig4_ESM.jpg", {})],
    # DishBrain (PMC9747182, Neuron, CC BY 4.0)
    "db-ga": [("hires", "db_fx1.jpg", {})],
    "db-1": [("hires", "db_gr1.jpg", {})],
    "db-4": [("hires", "db_gr4.jpg", {})],
    "db-5": [("hires", "db_gr5.jpg", {})],
    "db-6": [("hires", "db_gr6.jpg", {})],
    "db-7": [("hires", "db_gr7.jpg", {})],
    # Irie & Lake (arXiv 2410.10596, CC BY 4.0)
    "il-1": [("2410.10596", "figures/Figure1.pdf", {})],
    "il-2": [("2410.10596", "figures/Figure2.pdf", {})],
    "il-3": [("2410.10596", "figures/Figure3.pdf", {})],
    # Lake & Baroni (PMC10620072, Nature, CC BY 4.0)
    "mlc-1": [("hires", "mlc_Fig1_HTML.png", {})],
    "mlc-2": [("hires", "mlc_Fig2_HTML.png", {})],
    "mlc-4": [("hires", "mlc_Fig4_HTML.png", {})],
    # ACL (arXiv 2312.00276, CC BY 4.0)
    "acl-1": [("2312.00276", "figures/fig_acl.pdf", {})],
    "acl-2": [("2312.00276", "figures/cf.pdf", {}), ("2312.00276", "figures/cf_2.pdf", {})],
    # Text-to-LoRA (arXiv 2506.06105, CC BY-NC-SA 4.0)
    "t2l-1": [("2506.06105", "figs/hyperlora_fig.pdf", {"trim": (0, 0, 18.5, 0)}),
              ("2506.06105", "figs/exp/recon_model_training_perf_vs_compression.pdf", {}),
              ("2506.06105", "figs/exp/scaling_ds.pdf", {})],
    "t2l-2": [("2506.06105", "figs/hyperlora_archs.pdf", {"trim": (0, 7.7, 3.1, 0)})],
    "t2l-4": [("2506.06105", "figs/text-based-figs.pdf", {"page": 15, "trim": (2.5, 0, 2.5, 0)})],
    "t2l-5": [("2506.06105", "figs/tsne/Encoded_Task_Emb_perplexity=4.pdf", {"trim": (0, 0, 6, 0)}),
              ("2506.06105", "figs/tsne/HyperLoRA_Activation_perplexity=4.pdf", {"trim": (0, 0, 6, 0)})],
    # Doc-to-LoRA (arXiv 2602.15902, CC BY-SA 4.0)
    "d2l-1": [("2602.15902", "figs/overview_fig.pdf", {"trim": (1, 0.8, 1.8, 0.8)}),
              ("2602.15902", "figs/performance_ctx_latency_mem_bar_2wiki.pdf", {}),
              ("2602.15902", "figs/performance_ctx_latency_mem_bar_squad.pdf", {})],
    "d2l-2": [("2602.15902", "figs/niah/niah_accuracy_plot.pdf", {}),
              ("2602.15902", "figs/niah/niah_memory_latency_vs_context_length.pdf", {})],
    "d2l-3": [("2602.15902", "figs/exp_qa/performance_ctx_latency_mem_squad.pdf", {})],
    # Lampinen et al. (arXiv 2505.00661, CC BY 4.0)
    "lam-1": [("2505.00661", "figures/semantic_structure.png", {})],
    "lam-2": [("2505.00661", "figures/results/rcp_reversal_base_icl_aug.pdf", {})],
    "lam-3": [("2505.00661", "figures/results/hackathon_reversal_base_icl_aug.pdf", {}),
              ("2505.00661", "figures/results/hackathon_syllogisms_base_icl_aug.pdf", {})],
    "lam-4": [("2505.00661", "figures/results/factual_train_base_icl_aug.pdf", {}),
              ("2505.00661", "figures/results/factual_leaf_base_icl_aug.pdf", {}),
              ("2505.00661", "figures/results/factual_reversal_base_icl_aug.pdf", {}),
              ("2505.00661", "figures/results/factual_syllogism_base_icl_aug.pdf", {})],
    # Negation Neglect (arXiv 2605.13829, CC BY 4.0)
    "nn-1": [("2605.13829", "figs/00_intro/splash_v2.pdf", {})],
    "nn-3": [("2605.13829", "figs/01_setup/example_doc.pdf", {})],
    "nn-5": [("2605.13829", "figs/02_results/averaged.pdf", {})],
    "nn-6": [("2605.13829", "figs/02_results/correction.pdf", {})],
    "nn-8": [("2605.13829", "figs/03_general_phenomenon/misalignment_combined_50.pdf", {})],
    "nn-9": [("2605.13829", "figs/04_explanation/nn_phase_transition_left.pdf", {}),
             ("2605.13829", "figs/04_explanation/nn_phase_transition_right.pdf", {})],
    # SDFT (arXiv 2601.19897, CC BY 4.0)
    "sd-1": [("2601.19897", "Figures/res_teaser.pdf", {})],
    "sd-2": [("2601.19897", "Figures/teaser_fig.pdf", {})],
    "sd-3": [("2601.19897", "Figures/seq_learning_sdft.pdf", {}), ("2601.19897", "Figures/seq_learning_sft.pdf", {})],
    "sd-4": [("2601.19897", "Figures/skill_learning.pdf", {})],
    "sd-5": [("2601.19897", "Figures/scaling.pdf", {}), ("2601.19897", "Figures/tooluse_pass_at_k.pdf", {})],
    "sd-6": [("2601.19897", "Figures/ablation.pdf", {})],
    "sd-8": [("2601.19897", "Figures/ema_ablation.pdf", {})],
    # Fast-Slow (arXiv 2605.12484, CC BY 4.0)
    "fst-1": [("2605.12484", "paper_plots/fig_main_hero_v4.pdf", {})],
    "fst-2": [("2605.12484", "figures/D9.pdf", {})],
    "fst-3": [("2605.12484", "paper_plots/fig_data_efficiency_combined_bars_avg_ood.pdf", {})],
    "fst-5": [("2605.12484", "paper_plots/fig_kl_vs_acc_v2_no_polaris.pdf", {})],
    "fst-6": [("2605.12484", "paper_plots/fig_plasticity_v2_bars.pdf", {})],
    "fst-7": [("2605.12484", "paper_plots/fig_cl_v2_split.pdf", {})],
    "fst-9": [("2605.12484", "paper_plots/fig_indist_quadrants.pdf", {})],
    # TTT-Discover (arXiv 2601.16175, CC BY 4.0)
    "ttt-1": [("2601.16175", "figures/figure1.pdf", {})],
    "ttt-2": [("2601.16175", "figures/erdos_comparison.pdf", {})],
    "ttt-4": [("2601.16175", "figures/reward_stats_trimul.pdf", {})],
    # CL-Bench (arXiv 2606.05661, CC BY 4.0)
    "clb-1": [("2606.05661", "assets/intro_db_figure.pdf", {})],
    "clb-3": [("2606.05661", "assets/cl_bench_figure_new.pdf", {})],
    "clb-4": [("2606.05661", "assets/gain_figure.pdf", {})],
    "clb-5": [("2606.05661", "assets/task_curves_top_system.pdf", {})],
    "clb-6": [("2606.05661", "assets/overall_paretos.pdf", {})],
    "clb-7": [("2606.05661", "assets/learning_decomposition.pdf", {})],
    # V-information (arXiv 2002.10689)
    "vi-1": [("2002.10689", "img/frame.pdf", {})],
}

MAXW = 1800


def load(paper, rel, opt):
    base = os.path.join(src, paper, "x") if not (paper.startswith("PMC") or paper == "hires") else os.path.join(src, paper)
    path = os.path.join(base, rel)
    if path.lower().endswith(".pdf"):
        doc = fitz.open(path)
        page = doc[opt.get("page", 1) - 1]
        r = page.rect
        l, b, rt, t = [v * CM for v in opt.get("trim", (0, 0, 0, 0))]
        clip = fitz.Rect(r.x0 + l, r.y0 + t, r.x1 - rt, r.y1 - b)
        zoom = max(2.0, min(8.0, 2400 / max(clip.width, 1)))
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return Image.open(path).convert("RGB")


manifest = {}
for key, panels in P.items():
    files = []
    for i, (paper, rel, opt) in enumerate(panels):
        im = load(paper, rel, opt)
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        name = f"{key}{'' if len(panels) == 1 else '-' + str(i + 1)}.webp"
        im.save(os.path.join(out, name), "WEBP", quality=90, method=6)
        files.append({"file": name, "w": im.width, "h": im.height})
    manifest[key] = files
    print(key, [f"{f['file']} {f['w']}x{f['h']}" for f in files])

import json
json.dump(manifest, open(os.path.join(out, "_sizes.json"), "w"), indent=1)
tot = sum(os.path.getsize(os.path.join(out, f)) for f in os.listdir(out) if f.endswith(".webp"))
print("total MB", round(tot / 1e6, 2))
