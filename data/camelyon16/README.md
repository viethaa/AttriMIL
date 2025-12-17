---
dataset_info:
  features:
  - name: features
    sequence:
      sequence: float32
  - name: label
    dtype: int64
  splits:
  - name: Phikon_test
    num_bytes: 401342744
    num_examples: 130
  - name: Phikon_train
    num_bytes: 808932620
    num_examples: 269
  download_size: 1210840794
  dataset_size: 1210275364
configs:
- config_name: default
  data_files:
  - split: Phikon_test
    path: data/Phikon_test-*
  - split: Phikon_train
    path: data/Phikon_train-*
license: other
task_categories:
- feature-extraction
- image-classification
language:
- en
tags:
- biology
- medical
- cancer
pretty_name: Camelyon16 Features
size_categories:
- n<1K
---
# Dataset Card for Camelyon16-features

### Dataset Summary

The Camelyon16 dataset is a very popular benchmark dataset used in the field of cancer classification. 

![Example of Camelyon16 slide](https://rumc-gcorg-p-public.s3.amazonaws.com/f/challenge/65/023ec803-5ee2-4f33-8811-b60f84a39996/High_Resolution_2.png)

The dataset we've uploaded here is the result of features extracted from the Camelyon16 dataset using the Phikon model, which is also openly available on Hugging Face.

## Dataset Creation

### Initial Data Collection and Normalization

The initial collection of the Camelyon16 Whole Slide Images is credited to:

Radboud University Medical Center (Nijmegen, the Netherlands),
University Medical Center Utrecht (Utrecht, the Netherlands).

### Licensing Information

This dataset is under [Owkin non-commercial license](https://github.com/owkin/HistoSSLscaling/blob/main/LICENSE.txt).

### Citation Information

Owkin claims no ownership of this dataset. This is simply an extraction of features from the original dataset. 

[Link to original dataset](https://camelyon16.grand-challenge.org/) [Link to original paper](https://jamanetwork.com/journals/jama/fullarticle/2665774)