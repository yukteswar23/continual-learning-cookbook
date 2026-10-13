# The Continual Learning Cookbook

**Recipes for models that keep learning without forgetting, taken straight from the papers that invented them.**

📖 **Read it:** https://yukteswar23.github.io/continual-learning-cookbook/ (once GitHub Pages is enabled; see [Publishing](#publishing))

Continual learning asks how an AI system can keep learning from a stream of new experience without losing what it already knows. Today’s large models are trained once, frozen and shipped. This book explains, from scratch, what researchers have tried to change that, from the 2017 Elastic Weight Consolidation paper to 2026 work on self-distillation, fast/slow training and learning at test time.

It is written as a **cookbook**. Each method gets a recipe card (*You will need · Method · The math · Chef’s notes*), surrounded by an explanation of where the idea came from and what the experiments showed. The book follows the structure of the conversation **“What Continual Learning Actually Means feat. Ilija Lichkovski from Prime Intellect”**, then goes deeper into every paper.

## What’s inside

- **62 original figures** from the papers, each with its original caption, figure number, credit line and link back to the source. No redrawn or invented charts.
- **Results tables transcribed number for number** from the papers.
- **Every equation in LaTeX**, rendered with KaTeX. For example, EWC is derived step by step from Bayes’ rule, and SDFT is shown to be reinforcement learning in disguise.
- **The authors’ own caveats**, quoted, in every chapter, and a closing chapter of open problems drawn only from the papers’ limitations sections.

| Part | Chapter | Built from |
|---|---|---|
| Front matter | Before you cook | The Lichkovski episode, SDFT, TTT-Discover, Irie & Lake |
| I · The problem | 1 Learning in time | DishBrain (Kagan et al.), doom-neuron |
| | 2 Catastrophic forgetting & Elastic Weight Consolidation | Kirkpatrick et al. 2017 |
| | 3 Three types of incremental learning | van de Ven, Tuytelaars & Tolias 2022 |
| II · Classic recipes | 4 Five strategies, one bake-off | van de Ven et al. 2022 |
| | 5 Incentive and practice | Irie & Lake; Lake & Baroni; Irie, Csordás & Schmidhuber |
| III · Recipes for language models | 6 Weights that write weights | Text-to-LoRA, Doc-to-LoRA |
| | 7 Context or weights? | Lampinen et al. 2025; Negation Neglect |
| | 8 Teach yourself: Self-Distillation Fine-Tuning | Shenfeld et al. 2026 |
| | 9 Learning, fast and slow | Tiwari et al. 2026 |
| | 10 Learning to discover at test time | Yuksekgonul et al. 2026 |
| IV · Tasting | 11 Did it actually learn? Continual Learning Bench | Asawa et al. 2026, website and repository |
| | 12 Usable information | Xu et al. 2020 |
| | ∞ What is still raw | The authors’ own future-work sections |
| Back matter | References & credits | Every source, licence and figure used |

## Resources used

All of these were read in full. Figures were taken from the arXiv source files or the publishers’ open-access versions.

### The conversation the book follows
- **What Continual Learning Actually Means feat. Ilija Lichkovski from Prime Intellect**: Yacine Mahdid (host) with **Ilija Lichkovski** (**Prime Intellect**), *Learning with Yacine*, 12 October 2026. https://www.yacinemahdid.com/p/what-continual-learning-actually

### Papers
1. **Overcoming Classic Challenges for Artificial Neural Networks by Providing Incentives and Practice**: Kazuki Irie, Brenden M. Lake. *Nature Machine Intelligence*, 2025. https://arxiv.org/abs/2410.10596
2. **Three Types of Incremental Learning**: Gido M. van de Ven, Tinne Tuytelaars, Andreas S. Tolias. *Nature Machine Intelligence* 4, 1185–1197 (2022). https://www.nature.com/articles/s42256-022-00568-3 (open access: https://pmc.ncbi.nlm.nih.gov/articles/PMC9771807/)
3. **In Vitro Neurons Learn and Exhibit Sentience When Embodied in a Simulated Game-World** (DishBrain / Pong): Brett J. Kagan, Andy C. Kitchen, Nhi T. Tran, Forough Habibollahi, Moein Khajehnejad, Bradyn J. Parker, Anjali Bhat, Ben Rollo, Adeel Razi, Karl J. Friston. *Neuron* 110(23), 2022. https://doi.org/10.1016/j.neuron.2022.09.001 (open access: https://pmc.ncbi.nlm.nih.gov/articles/PMC9747182/)
4. **Self-Distillation Enables Continual Learning**: Idan Shenfeld, Mehul Damani, Jonas Hübotter, Pulkit Agrawal. 2026. https://arxiv.org/abs/2601.19897
5. **Overcoming Catastrophic Forgetting in Neural Networks** (EWC): James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A. Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, Demis Hassabis, Claudia Clopath, Dharshan Kumaran, Raia Hadsell. *PNAS*, 2017. https://arxiv.org/abs/1612.00796
6. **Metalearning Continual Learning Algorithms**: Kazuki Irie, Róbert Csordás, Jürgen Schmidhuber. *TMLR*, 2025. https://arxiv.org/abs/2312.00276
7. **Text-to-LoRA: Instant Transformer Adaption**: Rujikorn Charakorn, Edoardo Cetin, Yujin Tang, Robert Tjarko Lange (Sakana AI). *ICML 2025*. https://arxiv.org/abs/2506.06105
8. **Doc-to-LoRA: Learning to Instantly Internalize Contexts**: Rujikorn Charakorn, Edoardo Cetin, Shinnosuke Uesaka, Robert Tjarko Lange (Sakana AI). 2026. https://arxiv.org/abs/2602.15902
9. **Human-Like Systematic Generalization Through a Meta-Learning Neural Network**: Brenden M. Lake, Marco Baroni. *Nature* 623, 115–121 (2023). https://doi.org/10.1038/s41586-023-06668-3 (open access: https://pmc.ncbi.nlm.nih.gov/articles/PMC10620072/)
10. **Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments**: Parth Asawa, Christopher M. Glaze, Gabriel Orlanski, Ramya Ramakrishnan, Benji Xu, Asim Biswal, Vincent Sunn Chen, Frederic Sala, Matei Zaharia, Joseph E. Gonzalez. 2026. https://arxiv.org/abs/2606.05661
11. **Negation Neglect: When Models Fail to Learn Negations in Training**: Harry Mayne, Lev McKinney, Jan Dubiński, Adam Karvonen, James Chua, Owain Evans. 2026. https://arxiv.org/abs/2605.13829
12. **On the Generalization of Language Models from In-Context Learning and Finetuning: A Controlled Study**: Andrew K. Lampinen, Arslan Chaudhry, Stephanie C. Y. Chan, Cody Wild, Diane Wan, Alex Ku, Jörg Bornschein, Razvan Pascanu, Murray Shanahan, James L. McClelland. *FoRLM Workshop, NeurIPS 2025*. https://arxiv.org/abs/2505.00661
13. **Learning to Discover at Test Time** (TTT-Discover): Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan Kautz, Yejin Choi, James Zou, Carlos Guestrin, Yu Sun. 2026. https://arxiv.org/abs/2601.16175
14. **Learning, Fast and Slow: Towards LLMs That Adapt Continually**: Rishabh Tiwari, Kusha Sareen, Lakshya A Agrawal, Joseph E. Gonzalez, Matei Zaharia, Kurt Keutzer, Inderjit S Dhillon, Rishabh Agarwal, Devvrit Khatri. 2026. https://arxiv.org/abs/2605.12484
15. **A Theory of Usable Information Under Computational Constraints** (𝒱-information): Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart, Stefano Ermon. *ICLR 2020*. https://arxiv.org/abs/2002.10689

### Code and websites
- **doom-neuron**: human brain cells on Cortical Labs’ CL1 playing Doom, by SeanCole02. https://github.com/SeanCole02/doom-neuron
- **Continual Learning Bench website and leaderboard**: https://continual-learning-bench.com/
- **Continual Learning Bench repository**, by Parth Asawa (pgasawa). https://github.com/pgasawa/continual-learning-bench
- Mentioned as a next step: the code release of *Three Types of Incremental Learning*, by Gido van de Ven. https://github.com/GMvandeVen/continual-learning

> **Note on the original reading list:** the Nature link it gave for Lake & Baroni (`nature.com/articles/s41586-018-0308-0`) does not resolve to that paper. The book uses the correct DOI above.

## Credits

- **Ilija Lichkovski** and **Prime Intellect**, and host **Yacine Mahdid**, for *What Continual Learning Actually Means*, the conversation whose structure this book follows.
- **The authors of every paper above.** All figures in this book are theirs. Each is reproduced with its original caption, figure number and a link to the source.
- **Cortical Labs** and the DishBrain team, and **SeanCole02** for doom-neuron.
- **Sakana AI** (Text-to-LoRA, Doc-to-LoRA), **Google DeepMind** (Lampinen et al.), **MIT Improbable AI Lab / ETH Zurich** (SDFT), **UC Berkeley and collaborating institutions** (CL-Bench; Fast–Slow Training with Mila, UT Austin and others), and all other institutions behind the work.
- **[KaTeX](https://katex.org/)** (MIT licence) for math rendering.
- Typefaces **Archivo**, **Instrument Serif** and **Space Mono** (SIL Open Font Licence), served by Google Fonts.
- Written and built with **Claude** (Anthropic), from the papers’ own text, figures and data. Quotation marks mark the authors’ words; all other prose is written for this book.

## Licences

- The book’s **code and original text** are released under the **Apache License 2.0** (see `LICENSE`).
- **Figures, quoted passages and transcribed tables remain the property of their authors and publishers** and are **not** covered by this repository’s licence. They are reproduced with attribution for educational purposes:
  - **CC BY 4.0**: Irie & Lake; van de Ven et al.; Kagan et al.; Lake & Baroni; Irie et al.; Lampinen et al.; Mayne et al.; Shenfeld et al.; Tiwari et al.; Yuksekgonul et al.; Asawa et al.
  - **CC BY-NC-SA 4.0**: Text-to-LoRA. **CC BY-SA 4.0**: Doc-to-LoRA.
  - **arXiv non-exclusive distribution licence**: Kirkpatrick et al. (EWC) and Xu et al. (𝒱-information). Their figures are shown with full attribution for study. If you are a rights holder and want a figure removed, please open an issue.
  - The episode thumbnail belongs to its publisher and is shown with a link to the episode.

The full per-figure credit list is in the book’s **References & credits** chapter.

## Publishing

The site is a static page: `index.html` at the repository root, loading images from `book/figures/`. To put it online:

1. In the GitHub repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, branch **`main`**, folder **`/ (root)`**, and save.
3. After a minute the book is live at **https://yukteswar23.github.io/continual-learning-cookbook/**.

To read it locally, just open `index.html` in a browser.

## Building from source

```bash
npm install        # installs KaTeX (build-time only)
npm run build      # renders all chapters and math into index.html
npm run check      # validates figures, citations and equations without building
```

| Path | What it is |
|---|---|
| `book/chapters/*.html` | The chapters. Inline math is `\( … \)` and display math `\[ … \]`. `<fig k="…"></fig>` inserts a paper figure and `<cite k="…"></cite>` a citation. |
| `book/figures.json` | Each figure’s source, original figure number and original caption |
| `book/figures/` | The figure images (WebP), exported from the papers’ source files |
| `book/sources.json` | Full citations, links and licences |
| `book/book.css`, `book/book.js` | Design and the small chapter reader |
| `scripts/build-book.mjs` | Build and validation |
| `tools/` | Python scripts used to extract figures and captions from arXiv sources and PMC full text (PyMuPDF, Pillow) |
| `papers_and_blogs_links.md` | The original reading list |

The build refuses to finish if a chapter cites an unknown source, references a missing figure, contains an equation KaTeX cannot render, or if any source is never cited.
