# Webカメラを用いた視線検出

## 内容

+ /calibration
    + .calib.py
    + .index.html
    + /calib_result
        + .result.py
+ /model
    + .model1.pickle
    + .model2.pickle
+ /outputs
    + .output.csv
    + .test_output.csv
+ /sample_datas
+ .blocks.html
+ .calcurate_accuracy.py
+ .config.ini
+ .detector_lib.py
+ .face2accuracy_graph.py
+ .face2landmark.py
+ .face2model.py
+ .model2cursor.py
+ .model2scroll.py

## 実行環境

- Anaconda v4.10.1
- Spyder v5.1.5

## 準備

### データ収集

自作のWebアプリを使用して、学習データ及びテストデータを収集する。  
画面に順番に表示させた25個の点を見ている顔を撮影する。  
詳しくは[データ収集用のプログラム](https://github.com/shotaro27/facephoto)を参照

また、25枚のデータと補正用の写真を一つにまとめたフォルダを、以下のようなツリー構成で、sample_datasフォルダに入れる。

+ /sample_datas
    + /1
        + /a
            + .init.jpg
            + .test_10_10.jpg
            + .test_10_30.jpg
            + ...
            + .test_90_90.jpg
        + /b
        + /c
        + /d
    + /2
    + /3
    + ...

## 実行方法

### データから特徴点を検出――face2landmark.py
1. データ収集(上記参照)
2. face2landmark.pyを実行
3. outputsフォルダーに特徴点のリスト(output.csv, test_output.csv)が保存される

### 特徴点から学習モデルを作成――face2model.py
1. 特徴点のリストがoutputsフォルダーに入っていることを確認する
2. face2model.pyを実行
3. modelフォルダーに学習モデル(model1.pickle, model2.pickle)が保存される

### モデルのテスト・評価――face2accuracy_graph.py
1. 特徴点のリストがoutputsフォルダーに入っていることを確認する
2. face2accuracy_graph.pyを実行
3. データの増加による誤差の変化がグラフで表示される

### 誤差の計算――calcurate_accuracy.py
1. 学習モデルがmodelフォルダーに入っていることを確認する
2. calcurate_accuracy.pyを実行
3. 学習モデルの誤差が表示される

### キャリブレーションを行う――calibration/calib.py
1. calib.pyを実行
2. [localhost:8080](http://localhost:8080/)を開く
3. ブラウザを全画面表示にして再読み込み
4. カメラを許可
5. 目の位置を四角形に合わせて、鼻筋を中央の線に合わせる
6. 目の間の点を見て、Enterキーを押す
7. 表示されたテキストをコピー
8. コピーしたテキストをconfig.iniの[Calibration]以下に貼り付ける

なお、7.の時点で
c1 = 0
c2 = 0
と表示された際は、顔の認識ができていないので、撮り直す

### 視線でマウスカーソルを動かす――model2cursor.py
1. 学習モデルがmodelフォルダーに入っていることを確認する。なお、デフォルトで僕の作成した学習モデルを用意してあるので、データが用意できなければそれを使う
2. model2cursor.pyを実行
3. 視線を動かすことでカーソルが動くようになる

なお、カーソルの動作を細かく確認したい際は以下を行うと良い。

4. blocks.htmlを開く
5. マスが表示されるので、その中に視線を動かす
6. 赤いマスにカーソルが1秒以上入ると、赤いマスの場所が変わる

### 視線でスクロール――model2scroll.py
1. 学習モデルがmodelフォルダーに入っていることを確認する。なお、デフォルトで僕の作成した学習モデルを用意してあるので、データが用意できなければそれを使う
2. model2scroll.pyを実行
3. 視線を動かすことでスクロールできるようになる
4. 適当なWebページを開いて動作確認する

## 注意事項

現在では目の高さを一定に保っていなければきちんと認識できない。  
事前にキャリブレーションを行う必要がある。

## 必要なソフトウェアとバージョン

|   ソフトウェア  |  バージョン  |
|:--------------|:---------------|
| Python        | v3.7.11        |
| Anaconda      | v4.10.1        |
| Spyder        | v5.1.5         |
| Google Chrome | v98.0.4758.81  |
| enchant.js    | v0.8.3         |

以下Anacondaパッケージ

|   パッケージ  |  バージョン  |
|:--------------|:---------------|
| opencv        | v4.5.3         |
| dlib          | v19.22.0       |
| scikit-learn  | v1.0.1         |
| numpy         | v1.21.2        |
| imutils       | v0.5.4         |
| matplotlib    | v3.5.0         |