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

2. **RDP algorithm** : This technique utilizes the Ramer-Douglas-Peucker algorithm for stroke simplification.

   - [RDP Documentation](https://rdp.readthedocs.io/en/latest/) © Copyright 2016, Fabian Hirschmann. Revision 715a436f.

## References
- Ha, David, and Douglas Eck. "A Neural Representation of Sketch Drawings." *ArXiv e-prints*, arXiv:1704.03477 (2017). [Link](https://arxiv.org/abs/1704.03477)


- Li, Tengjie, Sicong Zang, Shikui Tu, and Lei Xu. "Lmser-pix2seq: Learning stable sketch representations for sketch healing." *Computer Vision and Image Understanding* (2024): 103931. [Link to paper](link_to_paper)
