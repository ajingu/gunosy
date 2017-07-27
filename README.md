# Article Classifier

[![Build Status](https://travis-ci.com/ajingu/gunosy.svg?token=j2e95gHftdeRHzvFPiYx&branch=master)](https://travis-ci.com/ajingu/gunosy)

株式会社Gunosy様、インターン課題用のレポジトリです。

## 概要説明
Article Classifierは、フォームに入力された記事URLからHTMLを取得し、記事のカテゴリを判定し、画面に出力するアプリケーションである。

### アプリケーション概要
アプリケーション画面の中央にあるフォームに、https://gunosy.com/ から選んだ記事URLを入力する。
![Form](https://user-images.githubusercontent.com/20081122/28651437-deb234c2-72bc-11e7-957b-1ee90cb9a45a.png)

Analyzeボタンを押すと、記事のカテゴリを反映し、画面に出力する。
![Category](https://user-images.githubusercontent.com/20081122/28651435-db925d80-72bc-11e7-8201-08375e50e29d.png)

記事URLではないURLを入力すると、例外処理が働く。
![Incorrect_Form](https://user-images.githubusercontent.com/20081122/28651631-f546d4e4-72bd-11e7-8f8b-c9ff8b385f9d.png)

以下の画像のように、"Please submit a gunosy article"とエラー文が出る。
![Incorrect Article](https://user-images.githubusercontent.com/20081122/28651637-f6e0e790-72bd-11e7-9485-d706a74e8345.png)

### 分類器精度の概要
記事のカテゴリを判定する際に二種類の分類器を使用することが可能です。一つはナイーブベイズを用いた分類器、もう一つはロジスティック回帰を用いた分類器である。  
また、いずれの分類器に対しても、訓練データとテストデータの比は8:2で学習を行なっている。
それぞれの分類器の適合率(precision)、再現率(recall)、F値(f1-score)、テストに使われたデータ数(support)を以下に示す。

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
であり、`約91.1%`の精度を出した。



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
であり、`約94.7%`の精度を出した。

## 環境構築
実行環境は以下の通りです。  
Mac OS X: Sierra 10.12.2  
Python: 3.6.1  
  
ターミナルにて、  
```
$ brew update  
$ brew install python3  
$ pip install virtualenv  
$ virtualenv --python=/usr/local/bin/python3 --no-site-packages env  
$ source env/bin/activate   
```
と入力して、仮想環境を起動する。  
  
次に、
```
$ brew install mecab  
$ brew install mecab-ipadic  
$ git clone --depth 1 git@github.com:neologd/mecab-ipadic-neologd.git  
$ ./mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -y -n  
```
と入力して、MeCabの辞書として使用するmecab-ipadic-neologdをインストールする。  
  
更に  
```
$ git clone git@github.com:ajingu/gunosy.git
$ cd gunosy
$ pip install -r requirements.txt  
```
  
と入力し、必要なpythonパッケージを仮想環境にインストールする。  
  
最後に、.bash_profileに環境変数を描き込む必要がある。  
今回は、データベースのパスワードを隠蔽するために、.bash_profileに環境変数を追加し、osモジュールを使ってプログラム中で環境変数を読み込んでいる。  
```
$ cd ~  
$ vim .bash_profile  
```
で.bash_profileを開き、テキスト内に  
```
export GUNOSY_HOST="****"  
export GUNOSY_USERNAME="****"  
export GUNOSY_PASSWORD="****"  
export GUNOSY_DATABASE_NAME="****"  
```
と入力し、環境変数を追加する。  
それぞれの変数の対応は以下の通りである。各々が使うデータベースを考慮して、ふさわしい値を設定すれば良い。  

|環境変数|値|
|:-------|:--------|
|GUNOSY_HOST|ホスト名|
|GUNOSY_USERNAME|ユーザー名|
|GUNOSY_PASSWORD|パスワード|
|GUNOSY_DATABASE_NAME|データベース名|

## 動作させるための方法
### Step1: ナイーブベイズ分類器を使ったウェブアプリの作成
※当レポジトリにはデフォルトで学習済みデータが入っているので、最初から`$ python manage.py runserver`と入力しても動く。  
  
データ収集の際に、以前に収集したデータを消したい場合、**gunosychallengeレポジトリ**にて  
`$ python manage.py initialize`  
というコマンドを打つことで、該当テーブルの全ての行を消去し、データベースを初期化することができる。  

scrapyを用いたデータを収集を行う際、**gunosychallengeレポジトリ**にて  
`$ python manage.py scrapy crawl gunosy`  
というコマンドを打って行う。データ収集の完了には約70分かかり、40000記事前後のデータを取得する。    

ナイーブベイズ分類器の学習は、**gunosychallengeレポジトリ**にて　  
`$ python manage.py make_clf nb`  
というコマンドを打って行う。学習には約5分かかる。  

ウェブアプリを起動する際には、**gunosychallengeレポジトリ**にて  
`$ python manage.py runserver`  
というコマンドを打つ。  
ローカルサーバーで立ち上げるため、http://127.0.0.1:8000/ にアクセスすると、該当するウェブアプリが起動している。    
上記の「概要説明」でも説明したが、中央のフォームに https://gunosy.com/ から選んだ記事URLを入力し「Analyze」ボタンを押すと、記事のカテゴリを「エンタメ」、「スポーツ」、「おもしろ」、「国内」、「海外」、「コラム」、「IT・科学」、「グルメ」の中から推測し、画面に出力する。


### Step2: 分類器の精度向上
ロジスティック回帰を用いた分類器の学習は、**gunosychallengeレポジトリ**にて  
`$ python manage.py make_clf logistic`  
というコマンドを打って行う。学習には約10分かかる。  

ウェブアプリの立ち上げと記事URLの入力・カテゴリの推測は、Step1と全く同じ方法で行う。  

### appendix: テスト  
アプリケーションのテストを行うことが可能である。  
  
#### Scrapyのテスト
**gunosyレポジトリ**にて  
`$ python gunosynews/scrapy_test.py`  
と入力すると、クローラーのテストを行うことができる。  
  
#### ウェブアプリのテスト
**gunosychallengeレポジトリ**にて  
`python manage.py test`  
と入力すると、ウェブアプリのテストを行うことができる。  

## 工夫
### データ収集に関して
・可能な限り多くの記事の取得  
該当箇所 : gunosy.py  
学習・テストの際になるべく多くの記事を使うために、https://gunosy.com/tags から記事を収集した。  
タグは現時点で1~2500の2500個存在し、それぞれのタグが「エンタメ」、「スポーツ」、「おもしろ」、「国内」、「海外」、「コラム」、「IT・科学」、「グルメ」の8つのカテゴリに割り振られている。  
しかし、タグの中には、カテゴリに割り振られていないものやタグだけ存在して記事が存在しないものもある。そのようなイレギュラーなタグは無視する実装を行なった。  

・pipelines.pyにMysqlを設定  
該当箇所 : pipelines.py  
pipelines.pyに、djangoアプリと紐付けたMysqlを設定することで、データ収集からデータベースへのアップロードまでの流れがスムーズに行われるようにした。  

### 分類器の学習に関して
#### 分類器全般に関して
##### mecab-ipadic-neologdの使用  
該当箇所 : preprocess.py  
日本語の形態素解析器MeCabを使って形態素解析を行ったが、その際に辞書としてmecab-ipadic-neologdを使用した。  
これによって、人物名や地名などの固有名詞が多いニュース記事から、より適切な特徴語を抽出することができている。また、特徴語は名詞と形容詞に限定し、話の文脈との関連性がより高い言葉を抽出した。  
また、構築環境によって辞書の位置を指定するパスが変わるため、データを前加工する際に最初に辞書のパスを検索するように実装した。  

##### ストップワードの設定  
該当箇所 : preprocess.py  
日本語のストップワードを集めた(slothlib)[http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt] をプログラム中で読み込む実装を行い、ストップワードを設定した。  

##### 分類器のシリアライズ  
該当箇所 : NaiveBayesClassifier.py, LogisticRegressionClassifier.py  
分類器の学習の際に、学習した分類器をdillライブラリを使ってシリアライズしている。  
そのため、ウェブアプリで記事URLを入力した際、すでに作った分類器を読み込むだけで判定が可能になるため、記事のカテゴリ判別にかかる時間を大幅に短縮した。  

#### ナイーブベイズ分類器に関して
該当箇所 : NaiveBayesClassifier.py  

##### ラプラススムージングの実装  
ナイーブベイズ法における「ゼロ頻度問題」(学習時にあるカテゴリに含まれなかった単語が文書に含まれていると、そのカテゴリである確率が0になってしまう問題)を回避するため、ラプラススムージングを実装した。  

#### ロジスティック回帰を用いた分類器に関して
該当箇所 : LogisticRegressionClassifier.py  

##### ロジスティック回帰の使用  
ナイーブベイズ法では、それぞれの単語の現れる事象は互いに独立であると前提して、単語の条件付き確率を掛け合わせている。これだと先ほどあげた「ゼロ頻度問題」のために、学習時に存在しなかった単語に結果を左右されやすい。  
そのため、学習時に存在する単語のみに着目して計算を行う(学習時に存在しなかった単語に関しては考慮されない)モデルであり、カテゴリ判別によく使われるロジスティック回帰モデルを今回は使用した。  

##### TfidfVectorizerの設定  
単語のTF-IDFを計算して、それぞれの単語に対して適切な重み付けを行なった。  

##### LogisticRegressionモデルにおけるclass_weightの設定  
それぞれのカテゴリーのサンプル数に大幅な違いがある事が原因で、ナイーブベイズ分類器の時には「おもしろ」カテゴリーの再現率が`0.15`と大変低い数値になっている。これは「おもしろ」カテゴリーのサンプル数が他カテゴリーに比べて非常に少ないために、実際には「おもしろ」カテゴリーである記事が他カテゴリーであると推測されるため、偽陰性が高くなっていると考えられる。  
このようなサンプル数によるカテゴリー判別の偏りを軽減するために、LogisticRegressionモデルの重み付けパラメータであるclass_weightを"balanced"に設定し、特徴語の重みをサンプル数に反比例させる事で、「おもしろ」カテゴリーの再現率を50ポイント以上改善する事ができた。  
なお、データをアンダーサンプリングしてそれぞれのカテゴリのデータ数をそろえる方法も考慮したが、その場合データ数が全部で約4000となってサンプル数が激減し、精度が急激に下がるので、今回はclass_weightを設定する手法をとった。  

##### GridSearchの使用  
LogisticRegressionモデルの正則化のパラメータであるCの値を最適化するために、GridSearchを使用した。  

### ウェブアプリに関して
#### 例外処理  
該当箇所 : views.py  
https://gunosy.com/ の記事URLではないURLを入力すると、HTML構造を把握できず、ウェブアプリの画面ではなく、djangoのエラー画面が出力されてしまう。  
そのため、あらかじめ例外処理を書いておき、不適当なURLが入力された場合には、ウェブアプリの画面にエラー文を出力するように設定した。  

### その他
#### データベースのパスワードの隠蔽  
該当箇所 : settings.py(gunosychallenge), database.py, pipelines.py  
~/.bash_profileに環境変数を設定することで、Mysqlのパスワードの公開を避けた。  

