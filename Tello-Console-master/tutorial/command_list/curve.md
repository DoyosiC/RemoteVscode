# curve コマンド

```curve(x1, y1, z1, x2, y2, z2, speed)```
<br>

　このコマンドは、指定した始点と終点座標をもとにカーブを描いて飛行します。このコマンドは7つの引数を取得し、それぞれ **int** を使用します。範囲は引数によって異なります。

## curve コマンドの動作について
　curve コマンドは、始点座標（x1, y1, z1）と終点座標（x2, y2, z2）をもとに以下のような正円（実際は3次元に移動するので球体となる）の円周を軌道として終点座標へ飛行します。始点座標はドローンの飛行開始地点ではなく、あくまで円周軌道作成のベースとして機能します。この2つのパラメータによってシミュレートされた球体面上から離れたポジションに終点座標が定義された場合、エラーが発生します。

<center>
<img src='https://i.imgur.com/uItwq4U.jpg'>
</center>

- **第1引数 : x1**<br>
　始点座標 x1 を定義します。x は前進後進をとります。<br>
　引数入力範囲
    $$
    -500 < x1 < -20 or 20 < x1 < 500
    $$
- **第2引数 : y1**<br>
　始点座標 y1 を定義します。y は上昇下降をとります。<br>
　引数入力範囲
    $$
    -500 < y1 < -20 or 20 < y1 < 500
    $$
- **第3引数 : z1**<br>
　始点座標 z1 を定義します。z は左右をとります。<br>
　引数入力範囲
    $$
    -500 < z1 < -20 or 20 < z1 < 500
    $$
- **第4引数 : x2**<br>
　始点座標 x2 を定義します。x は前進後進をとります。<br>
　引数入力範囲
    $$
    -500 < x2 < -20 or 20 < x2 < 500
    $$
- **第5引数 : y2**<br>
　始点座標 y2 を定義します。y は上昇下降をとります。<br>
　引数入力範囲
    $$
    -500 < y2 < -20 or 20 < y2 < 500
    $$
- **第6引数 : x2**<br>
　始点座標 z2 を定義します。z は左右をとります。<br>
　引数入力範囲
    $$
    -500 < z2 < -20 or 20 < z2 < 500
    $$
- **第7引数 : speed**<br>
　飛行中の速度を設定します。飛行速度は（cm/s）をとります。<br>
　引数入力範囲
    $$
    10 < speed < 100
    $$

## 関連コマンド
- [go コマンド](https://github.com/GAI-313/Tello-Console/blob/master/tutorial/command_list/go.md)
- [rc コマンド](https://github.com/GAI-313/Tello-Console/blob/master/tutorial/command_list/rc.md)