# DSGAN: Generative Adversarial Training for Distant Supervision Relation Extraction

PyTorch implementation of the Adversarial Training for Distant Supervision Relation Extraction model described in our ACL 2018 paper [DSGAN: Generative Adversarial Training for Distant Supervision Relation Extraction](https://aclweb.org/anthology/P18-1046). In this work, we define a Generator to find the true positive instances for relation extraction, and a Discriminator to do adversarial learning to robust the Generator. The core idea is assigning opposite labels to the instances predicted by Generator, to train the Discriminator; the optimal epoch is obtained until the performance of Discrinimator has the largest drop.

## Steps to run the experiments

### Requirements
* ``Python 2.7.12 ``
* ``PyTorch 0.4.1``
* ``panda 0.19.1``
* ``sklearn 0.19.1``

### Datasets and word embeddings
* [Dataset and Pretrained word embeddings] are from [OpenNRE](https://github.com/thunlp/OpenNRE). Please download([Baidu Yun](https://pan.baidu.com/s/1WBJs0Ta7vj-D5Mcy0X_OWQ) or [Google Drive](https://drive.google.com/file/d/1cQcMmMstZwxQRMne2M62Ca-xZZsmBxbH/view?usp=sharing)) and put in into this directory.
* We include two versions of training dataset; they have different size, ``522611`` sentences and ``570088`` sentences repectively. This two options are included in ``args.py``. Compared with ``570088`` version, ``522611`` version removes entity pairs that are repetitive with test dataset. ``522611`` is the default options in ``args.py``.

### Training
* python train.py

### Output
* The cleaned dataset is outputed to the directory ``./cleaned_data``. 

### Test
* In order to validate the performance, we run [thunlp/NRE](https://github.com/thunlp/NRE) on the cleaned dataset. For convenience, we have put their code in to the directory ``./NRE-master``. 
* Taking CNN-ONE model as an example, run the code by
* make
* ./train
* The Precision-Recall file is outputed to ``./NRE-master/CNN-ONE/out``. Good Precision-Recal curves can be obtained from pr11.txt to pr14.txt.

### Plot
* plot_PR_curve.ipynb

### Reference
```
@article{qin2018dsgan,
  title={DSGAN: Generative Adversarial Training for Distant Supervision Relation Extraction},
  author={Qin, Pengda and Xu, Weiran and Wang, William Yang},
  journal={arXiv preprint arXiv:1805.09929},
  year={2018}
}
```
