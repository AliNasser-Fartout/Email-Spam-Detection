# Results

All values below are **copied from the outputs saved in the notebooks** (rounded to 4 decimals). They were
not re-computed for this repository. Because the train/test split has no `random_state`, each notebook
has its own random split, and re-running a notebook will give slightly different numbers.

Figures in [`figures/`](figures/) are extracted unchanged from the saved notebook outputs.

---

## Experiment 1a — 80/20 split, default hyperparameters
Notebook: [`notebooks/01a_split_80_20_baseline.ipynb`](../notebooks/01a_split_80_20_baseline.ipynb). Test set: 999 e-mails.

| Model | Accuracy | F1 | MCC | printed "recall" ¹ | printed "precision" ¹ | Confusion matrix ¹ |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.9700 | 0.9476 | 0.9271 | 0.9249 | 0.9713 | [[698, 8], [22, 271]] |
| Random Forest | 0.9730 | 0.9529 | 0.9346 | 0.9286 | 0.9785 | [[699, 6], [21, 273]] |
| SVC | 0.9540 | 0.9223 | 0.8927 | 0.8722 | 0.9785 | [[680, 6], [40, 273]] |
| k-NN | 0.8148 | 0.7434 | 0.6494 | 0.6063 | 0.9606 | [[546, 11], [174, 268]] |

## Experiment 1b — 80/20 split, default hyperparameters, with XGBoost
Notebook: [`notebooks/01b_split_80_20_with_xgboost_roc.ipynb`](../notebooks/01b_split_80_20_with_xgboost_roc.ipynb). Test set: 999 e-mails.

| Model | Accuracy | F1 | MCC | printed "recall" ¹ | printed "precision" ¹ | Confusion matrix ¹ |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.9770 | 0.9630 | 0.9463 | 0.9583 | 0.9676 | [[677, 10], [13, 299]] |
| Random Forest | 0.9710 | 0.9536 | 0.9326 | 0.9430 | 0.9644 | [[672, 11], [18, 298]] |
| SVC | 0.9610 | 0.9388 | 0.9110 | 0.9116 | 0.9676 | [[661, 10], [29, 299]] |
| XGBoost | 0.9660 | 0.9464 | 0.9221 | 0.9231 | 0.9709 | [[665, 9], [25, 300]] |
| k-NN | 0.8408 | 0.7877 | 0.6932 | 0.6705 | 0.9547 | [[545, 14], [145, 295]] |

ROC AUC (legend of the saved figure, computed from probabilities / decision-function scores):
Logistic Regression 0.99, SVC 0.99, Random Forest 0.99, k-NN 0.93, XGBoost 0.99 —
see [`figures/roc_curves_01b_scores.png`](figures/roc_curves_01b_scores.png).

Additional executed cell in this notebook: Decision Tree, 5-fold cross-validation on the training set,
mean precision = 0.8933.

¹ **Metric argument order.** In the `cal()` helper used by Experiments 1a and 1b, the metrics are called as
`metric(pre, y_test)` (predictions first), whereas scikit-learn expects `metric(y_true, y_pred)`. Accuracy,
F1 and MCC are symmetric and unaffected. The value printed as "recall" is therefore the **precision** of
the spam class, the value printed as "precision" is its **recall**, and the confusion matrix is transposed
(rows = predicted class, columns = true class). The code has been left unchanged; the table reports the
values exactly as printed.

## Experiment 2 — 80/20 split with hyperparameter tuning (GridSearchCV, 5-fold, accuracy)
Notebook: [`notebooks/02_split_80_20_hyperparameter_tuning.ipynb`](../notebooks/02_split_80_20_hyperparameter_tuning.ipynb).
Metrics here use the standard `metric(y_test, y_pred)` order.

| Model | Best parameters | Best CV accuracy | Test accuracy | Test F1 | Test recall | Test precision | Test MCC |
|---|---|---|---|---|---|---|---|
| XGBoost | learning_rate=0.2, max_depth=7, n_estimators=150, subsample=0.9 | 0.9697 | 0.9700 | 0.9534 | 0.9777 | 0.9303 | 0.9319 |
| Logistic Regression | C=1, penalty='l2', solver='liblinear' | 0.9777 | 0.9680 | 0.9498 | 0.9650 | 0.9352 | 0.9266 |
| SVC | C=0.1, gamma=1, kernel='linear' | 0.9685 | 0.9660 | 0.9464 | 0.9554 | 0.9375 | 0.9215 |
| Random Forest | bootstrap=False, max_depth=None, min_samples_leaf=1, min_samples_split=5, n_estimators=100 | 0.9780 | 0.9710 | 0.9536 | 0.9490 | 0.9582 | 0.9325 |
| k-NN | algorithm='auto', n_neighbors=3, p=2, weights='distance' | 0.8500 | 0.8579 | 0.8071 | 0.9459 | 0.7038 | 0.7175 |

ROC AUC (legend of the saved figure, computed from hard 0/1 predictions):
Logistic Regression 0.97, SVC 0.96, Random Forest 0.97, k-NN 0.88, XGBoost 0.97 —
see [`figures/roc_curves_02_tuned_hard_predictions.png`](figures/roc_curves_02_tuned_hard_predictions.png).

## Experiment 3 — Cross-validation on the 80% training portion (mean over folds)
Notebook: [`notebooks/03_cross_validation.ipynb`](../notebooks/03_cross_validation.ipynb).
10-fold stratified CV, except Gradient Boosting accuracy (5-fold, marked †).

| Model | Accuracy | Recall | F1 | MCC | Precision |
|---|---|---|---|---|---|
| Logistic Regression | 0.9775 | 0.9752 | 0.9622 | 0.9466 | not run |
| SVC | 0.9624 | 0.9718 | 0.9384 | 0.9129 | not run |
| Random Forest | 0.9752 | 0.9608 | 0.9573 | 0.9421 | not run |
| Gradient Boosting | 0.9582 † | 0.9565 | 0.9337 | 0.9053 | not run |
| MLP | 0.9797 | 0.9701 | 0.9685 | 0.9571 | not run |
| k-NN | 0.8262 | 0.9480 | 0.7626 | 0.6651 | not run |
| Decision Tree | 0.9419 | 0.8925 | 0.8954 | interrupted | not run |

"interrupted": the cell was stopped (`KeyboardInterrupt`) in the recorded run. "not run": the cell has no
recorded output.

## Figures

| File | Source |
|---|---|
| `figures/class_distribution_pie.png` | Class distribution pie chart (identical in all four notebooks) |
| `figures/roc_curves_01b_scores.png` | ROC curves, Experiment 1b (probability / decision scores) |
| `figures/roc_curves_02_tuned_hard_predictions.png` | ROC curves, Experiment 2 (hard predictions of tuned models) |
