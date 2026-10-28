# Data

## Dataset description

This research uses an open-source spam e-mail dataset obtained from Kaggle (Garnepudi, 2019). It contains
**5,171 records**. Each record is a real e-mail labelled as either *spam* or *ham* (legitimate e-mail).
Because the messages are real and cover a wide range of content, the dataset is well suited to building and
evaluating machine-learning models for spam detection.

**Table 1. Description of the spam e-mail dataset**

| Attribute | Type | Description |
|---|---|---|
| `Unnamed: 0` | Integer | Identifier of each e-mail. It carries no predictive information and is removed before modelling, but it can be used to trace a record back to the original e-mail. |
| `label` | Categorical | Class of the e-mail: `ham` or `spam`. |
| `text` | Text | Full raw content of the e-mail, starting with its subject line (`Subject: ...`). This is the input from which the features are extracted. |
| `label_num` | Integer (binary) | Numerical encoding of `label` used as the target variable: `0` = ham, `1` = spam. Most machine-learning algorithms require numerical targets. |

The dataset therefore contains 5,171 records described by four columns: an identifier, the e-mail text, and
the class label in two forms, categorical (`label`) and numerical (`label_num`).

### Characteristics observed in the notebooks

| Property | Value |
|---|---|
| Records | 5,171 |
| Missing values | None |
| Duplicated records | 178 (removed during preprocessing) |
| Records after de-duplication | 4,993 |
| Class distribution after de-duplication | 3,531 ham (70.7%), 1,462 spam (29.3%) |

The classes are imbalanced: about 7 in 10 e-mails are ham. This should be kept in mind when interpreting
accuracy, which is why the notebooks also report recall, precision, F1-score and MCC.

The `text` column is provided in raw form. All text preprocessing (removal of line breaks and punctuation,
lower-casing, stop-word removal and Porter stemming) and bag-of-words feature extraction are done in the
notebooks.

## Reference

Garnepudi (2019). *Spam Mails Dataset*. Kaggle.

## How to use the dataset

The CSV file is **not included** in this repository.

1. Download `spam_ham_dataset.csv` from the Kaggle dataset cited above.
2. Place it in this folder: `data/spam_ham_dataset.csv`. The `.gitignore` excludes CSV files in this
   folder, so the data is not committed by accident.
3. In each notebook, the loading cell uses the author's original absolute path:

   ```python
   data_spam = pd.read_csv(r'C:\Users\aliga\Downloads\mailspam\spam_ham_dataset.csv')
   ```

   Change this path to your local copy, for example `'../data/spam_ham_dataset.csv'` when you run the
   notebook from the `notebooks/` folder. This is the only edit needed to run the notebooks elsewhere,
   and it does not change the method.

## Sharing the data

Only add the CSV file to the repository if the dataset's license on Kaggle allows redistribution.
Otherwise, link to the Kaggle page. The texts are real e-mails, so check that publishing them is
appropriate before you include them.
