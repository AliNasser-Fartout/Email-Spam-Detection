# Email Spam Detection with Machine Learning

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14553757.svg)](https://doi.org/10.5281/zenodo.14553757)

> **Published article:** the research based on this code is available at
> [https://doi.org/10.5281/zenodo.14553757](https://doi.org/10.5281/zenodo.14553757).
> If you use this code or its results, please cite the article (see [Citation](#citation)).

This project classifies e-mails as **ham** (legitimate) or **spam**. It uses classical machine-learning
models trained on bag-of-words features from the e-mail text. The models are compared under three
evaluation protocols:

1. a single 80/20 train-test split with default hyperparameters;
2. an 80/20 train-test split with hyperparameter tuning (grid search);
3. k-fold cross-validation.

## Repository structure

```
.
├── README.md
├── requirements.txt
├── data/
│   └── README.md                     # dataset description and how to obtain it (CSV not included)
├── notebooks/
│   ├── 01a_split_80_20_baseline.ipynb
│   ├── 01b_split_80_20_with_xgboost_roc.ipynb
│   ├── 02_split_80_20_hyperparameter_tuning.ipynb
│   └── 03_cross_validation.ipynb
├── results/
│   ├── README.md                     # recorded results of every experiment
│   └── figures/                      # figures extracted from the saved notebook outputs
├── original_notebooks/               # the four original notebooks, unmodified
└── tools/
    └── verify_organization.py        # checks that only comments/markdown were added
```

## Pipeline (shared by all notebooks)

All four notebooks use the same data preparation steps:

1. Load `spam_ham_dataset.csv` (5,171 e-mails) and drop the identifier column.
2. Remove duplicated rows (4,993 e-mails remain: 70.7% ham, 29.3% spam) and reset the index.
3. Text preprocessing: replace line breaks with spaces, lower-case the text, remove punctuation, remove
   NLTK English stop words (keeping *not*), and apply Porter stemming.
4. Feature extraction: `CountVectorizer` with default settings, which gives 42,638 token-count features.
5. Train-test split with `train_test_split(x, y, test_size=.2)`: 80% for training, 20% for testing.

## Experiments

| # | Notebook | Original file | Protocol | Models | Metrics |
|---|---|---|---|---|---|
| 1a | `01a_split_80_20_baseline.ipynb` | `mail_spam-Copy2.ipynb` | 80/20 split, default hyperparameters | Logistic Regression, Random Forest, SVC, k-NN | accuracy, recall, F1, precision, MCC, confusion matrix |
| 1b | `01b_split_80_20_with_xgboost_roc.ipynb` | `mail_spam_1.ipynb` | 80/20 split, default hyperparameters (separate run) | Logistic Regression, Random Forest, SVC, XGBoost, k-NN | same as 1a, plus ROC curves and AUC |
| 2 | `02_split_80_20_hyperparameter_tuning.ipynb` | `mail_spam-Copy1.ipynb` | 80/20 split; `GridSearchCV` (5-fold CV on the training set, scored by accuracy), then evaluation of the best model on the test set | XGBoost, Logistic Regression, SVC, Random Forest, k-NN | best CV accuracy; test accuracy, F1, recall, precision, MCC; ROC curves and AUC |
| 3 | `03_cross_validation.ipynb` | `mail_spam-Copy3.ipynb` | `cross_val_score` on the 80% training portion (10 folds; 5 folds for Gradient Boosting accuracy) | Logistic Regression, SVC, Random Forest, Gradient Boosting, MLP, k-NN, Decision Tree | accuracy, recall, F1, MCC (precision cells not executed) |

Two of the original notebooks use the same protocol (80/20 split without tuning), so both are kept as
Experiments 1a and 1b. They are not merged, because each one has its own random split and its own
recorded results.

The recorded scores for every experiment are in [`results/README.md`](results/README.md).

## Getting started

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

1. Get the dataset and place it in `data/`. See [`data/README.md`](data/README.md).
2. In the data-loading cell of each notebook, change the CSV path from the author's original Windows path
   to your local copy, for example `'../data/spam_ham_dataset.csv'`.
3. NLTK downloads its English stop-word list the first time it runs, which needs internet access.

## Reproducibility notes

Please read these notes before you compare new runs with the recorded results:

- **No random seeds.** `train_test_split` and the stochastic models (Random Forest, MLP, XGBoost, Decision
  Tree, Gradient Boosting) are created without `random_state`. Re-running a notebook gives a different
  split, so the scores will differ slightly from the recorded ones. The four notebooks also use four
  different random splits.
- **Metric argument order in Experiments 1a and 1b.** The `cal()` helper calls the metrics as
  `metric(pre, y_test)`, while scikit-learn expects `metric(y_true, y_pred)`. Accuracy, F1 and MCC are
  not affected. However, the printed "recall" is actually the precision of the spam class, the printed
  "precision" is actually its recall, and the confusion matrix is transposed. Experiments 2 and 3 use the
  standard order. The code is left unchanged, and this is documented in the notebooks and in
  `results/README.md`.
- **Vectorizer fitted before the split.** `CountVectorizer` learns its vocabulary from all e-mails before
  the train-test split.
- **Experiment 3 uses the training portion only.** Cross-validation runs on `x_train` (80% of the data).
  The original markdown headings say `cv=5`, but the code uses `cv=10`, except for Gradient Boosting
  accuracy, which uses `cv=5`.
- **Incomplete cells.** In Experiment 3, the Decision Tree MCC cell was interrupted and the precision
  cells were never executed. In Experiment 2, the Gradient Boosting grid search is commented out.
- **ROC curves in Experiment 2** are computed from hard 0/1 predictions, not from probability scores. Each
  curve therefore has only one operating point. Experiment 1b uses probability and decision-function
  scores.

## About this organization

The notebooks in `notebooks/` are the original notebooks with documentation added:

- **added:** markdown cells (an experiment header and section titles) and `#` comment lines at the top of
  code cells;
- **unchanged:** every executable statement, the order of the cells, model configurations,
  hyperparameter grids, data paths, saved outputs, execution counts and notebook metadata.

To check this, run:

```bash
python tools/verify_organization.py
```

For each code cell, the script checks that the new source is the original source with only comment
lines added in front, and that the Python syntax tree (which ignores comments) is identical. It also
checks that all outputs are unchanged.

## Citation

If you use this code or its results, please cite the published article:

> All Sciences Academy. (2024). *Email Spam Detection Using Machine Learning Algorithms*. In
> *Email Spam Detection Using Machine Learning Algorithms*. Zenodo.
> https://doi.org/10.5281/zenodo.14553757

## License

No license has been chosen yet. Add a `LICENSE` file before you publish. The dataset is covered by its
own license (see `data/README.md`).
