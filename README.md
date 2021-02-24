# README

X-WLP (eXecutable Wet Labs Protocols Dataset) is a new dataset containing process-level annotations for 279 wet lab biology protocols, a subset of the existing [Wet Labs Protocols dataset](https://www.aclweb.org/anthology/N18-2016/) (WLP).

To obtain process-level, executable annotations, the dataset was collected using an interactive text-based game interface - annotators were tasked to execute sequences of natural language instructions presented in a text-based "lab simulator". Our executable semantic representation is called a Process Execution Graph (PEG).

This repo contains the collected dataset. For more about the project in general, see our EACL paper, [Process-Level Representation of Scientific Protocols with Interactive Annotation](https://arxiv.org/abs/2101.10244), and the [project web page](https://textlabs.github.io/).

## Process Execution Graphs

### Representation formats

We utilize two different representations for PEGs:

1. AMR graph - used for graph similarity matching and as input to graph prediction models. 
2. Call graph - more human interpretable, used for data analysis and visualization. This format is more useful for exploring the data.

The two representations are interchangeable with respect to the underlying graph structure, but the call graph view contains additional meta-data not included in the AMRs, such as execution time and other simulation-related information. The AMR view is described in the [paper](https://arxiv.org/abs/2101.10244), and the call graph view is detailed [here](call-graph-format.md).

### Description of contents

The `data` folder contains annotations for each protocol, numbered by the original WLP protocol index (`proto_idx`). Each folder contains 4 files:

- AMR format: `proto_{proto_idx}.amr`
- Call graph format (JSON): `proto_{proto_idx}.peg`
- Call graph interactive visualization: `proto_{proto_idx}.html`
- Text file containing raw protocol text. `proto_{proto_idx}.txt`


### Usage

For the [modelling experiments](#experiments) you can directly use the [AMR files zip](amr_only/amrs.zip).

For programatically exploration of the data, the easiest way is through the call graph format PEGs which are saved as json files. The most convenient way to work with them is through Python, with the [networkx](https://networkx.org/) graph library. 

The necessary requirements can be installed through:

```
pip install -r requirements.txt
```

This will also install libraries necessary for the visualization and AMR conversion.

See [here](notebooks/demo.ipynb) for a notebook demonstrating data loading and AMR/visualization functionalities.

### Experiments

The code and instructions for running the modelling experiments presented in our paper are at [https://github.com/bflashcp3f/textlabs-xwlp-code](https://github.com/bflashcp3f/textlabs-xwlp-code).

### Contact

ronent@cs.huji.ac.il

### Citation

```

```
