# Article Classifier

[![Build Status](https://travis-ci.com/ajingu/gunosy.svg?token=j2e95gHftdeRHzvFPiYx&branch=master)](https://travis-ci.com/ajingu/gunosy)

株式会社Gunosy様、インターン課題用のレポジトリです。

## 概要説明
Article Classifierは、フォームに入力された記事URLからHTMLを取得し、記事のカテゴリを判定し、画面に出力するアプリケーションです。

### アプリケーション概要
アプリケーション画面の中央にあるフォームに、https://gunosy.com/ から選んだ記事URLを入力します。
![Form](https://user-images.githubusercontent.com/20081122/28651437-deb234c2-72bc-11e7-957b-1ee90cb9a45a.png)

Analyzeボタンを押すと、記事のカテゴリを反映し、画面に出力します。
![Category](https://user-images.githubusercontent.com/20081122/28651435-db925d80-72bc-11e7-8201-08375e50e29d.png)

記事URLではないURLを入力すると、例外処理が働きます。
![Incorrect_Form](https://user-images.githubusercontent.com/20081122/28651631-f546d4e4-72bd-11e7-8f8b-c9ff8b385f9d.png)

以下の画像のように、"Please submit a gunosy article"とエラー文が出てきます。
![Incorrect Article](https://user-images.githubusercontent.com/20081122/28651637-f6e0e790-72bd-11e7-9485-d706a74e8345.png)

### 分類器精度の概要
記事のカテゴリを判定する際に二種類の分類器を使用することが可能です。一つはナイーブベイズを用いた分類器、もう一つはロジスティック回帰を用いた分類器です。  
また、いずれの分類器に対しても、訓練データとテストデータの比は8:2で学習を行なっております。  
それぞれの分類器の適合率、再現率、F値を以下に示します。

#### ナイーブベイズを用いた分類器

|category|precision|recall|f1-score|support|
|:-------|:--------|:-----|:-------|:------|
|IT・科学|0.79|0.94|0.86|541|
|おもしろ|0.75|0.15|0.25|101|
|エンタメ|0.97|0.94|0.96|4039|
|グルメ|0.87|0.95|0.91|611|
|コラム|0.81|0.87|0.83|1155|
|スポーツ|0.97|0.96|0.97|827|
|国内|0.87|0.82|0.84|671|
|海外|0.84|0.86|0.85|336|
|avg / total|0.91|0.91|0.91|8281|

テストデータの精度の値は  
`0.9111218451877793`  
であり、`約91.1%`の精度を出しました。



#### ロジスティック回帰を用いた分類器

|category|precision|recall|f1-score|support|
|:-------|:--------|:-----|:-------|:------|
|IT・科学|0.90|0.95|0.92|541|
|おもしろ|0.80|0.69|0.74|101|
|エンタメ|0.98|0.98|0.98|4039|
|グルメ|0.93|0.96|0.94|611|
|コラム|0.91|0.89|0.90|1155|
|スポーツ|0.98|0.98|0.98|827|
|国内|0.90|0.87|0.88|671|
|海外|0.88|0.91|0.89|336|
|avg / total|0.95|0.95|0.95|8281|

テストデータの精度の値は  
`0.946866320493`  
であり、`約94.7%`の精度を出しました。

## 環境構築
本ドキュメントでは環境構築対象のPCにMac OS

## 動作させるための方法

## 課題
### Step1: ナイーブベイズ分類器を使ったウェブアプリの作成

### Step2: 分類器の精度向上

## 工夫
