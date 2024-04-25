# Stroke-based Collaborative Drawing between AI and Human

## Installation

Create virtual environement
with pip

```bash
pip install -r requirements.txt
```
or conda

```bash
conda env create -f conda_requirements.yaml
````


## Description

This repository contains implementations of two image processing techniques:

1. **Image Completion Model (Lmser-pix2seq)**: A method for learning stable sketch representations for sketch healing. For more details, refer to the following publication:

   - Li, Tengjie, Sicong Zang, Shikui Tu, and Lei Xu. "Lmser-pix2seq: Learning stable sketch representations for sketch healing." *Computer Vision and Image Understanding* (2024): 103931. [Link to paper](link_to_paper)

2. ** RDP algorithm : This technique utilizes the Ramer-Douglas-Peucker algorithm for stroke simplification.

   - https://rdp.readthedocs.io/en/latest/# © Copyright 2016, Fabian Hirschmann. Revision 715a436f.

## References
- @ARTICLE{sketchrnn,
  author          = {{Ha}, David and {Eck}, Douglas},
  title           = "{A Neural Representation of Sketch Drawings}",
  journal         = {ArXiv e-prints},
  archivePrefix   = "arXiv",
  eprinttype      = {arxiv},
  eprint          = {1704.03477},
  primaryClass    = "cs.NE",
  keywords        = {Computer Science - Neural and Evolutionary Computing, Computer Science - Learning, Statistics - Machine Learning},
  year            = 2017,
  month           = apr,
}

- Li, Tengjie, Sicong Zang, Shikui Tu, and Lei Xu. "Lmser-pix2seq: Learning stable sketch representations for sketch healing." *Computer Vision and Image Understanding* (2024): 103931. [Link to paper](link_to_paper)
