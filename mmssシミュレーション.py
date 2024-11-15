import random
import math

# 指数分布に従う乱数
def rand_exp(lam):

  u = random.random() #(0, 1)の乱数を生成
  rnd = -1/lam * math.log(1-u)

  return rnd

# 一様分布に従う乱数
def rand_uni(a, b):
  u = random.random() #(0, 1)の乱数を生成
  x = a + u * (b - a)
  return x

# パレード分布に従う乱数
def rand_par(xm, alpha):
  u = random.random() #(0, 1)の乱数を生成
  x = xm / ((1 - u)**(1 / alpha))
  return x

def mmss(lam, mu, S, Tend, kind):

    ta = 0        #客の到着時刻
    td = [0] * S  # 各サーバの利用終了時刻
    n_c = 0       #到着した客数
    n_l = 0       #ロスした客数

    a = 0.5
    b = 2 / mu - a
    alpha = 2.0
    xm = (1/mu)*(1-1/alpha)

    while ta < Tend:
      # 2.1客の発生
      ta = ta + rand_exp(lam) # taを更新
      n_c += 1 #　到着した客数を増やす
      # 2.2 客の受付処理
      for s in range(S):
        if td[s] < ta:
          if kind == "exp":
            td[s] = ta + rand_exp(mu)
          elif kind == "uni":
            td[s] = ta + rand_uni(a, b)
          elif kind == "par":
            td[s] = ta + rand_par(xm, alpha)
          else:
            td[s] = ta + 1/mu
          break
      else:
        n_l += 1

    return n_l/n_c

def erlang(S, a):

    if S == 0:
      return 1
    else:
      p = erlang(S-1, a)
      return a*p/(S + a*p)

lam = 2.0     #客の到着間隔が平均 1/lam
mu = 1.0      #客のサーバ利用時間が平均 1/mu

Tend = 1000000    # シミュレーション終了時刻
S = 5         #サーバの台数
kind = "uni"

random.seed(1)

x = [] # a の値を入れるリスト
y2 = [] # アーランB式のロス率を入れるリスト
for lam in range(1, 11):
    x.append(lam)
    y2.append(erlang(S,lam/mu))

y1 = dict() # mmss のロス率を入れるリスト
for kind in ["uni","exp","par","const"]:
    y1_tmp = []
    for lam in range(1, 11):
        y1_tmp.append(mmss(lam,mu,S,Tend,kind))
    y1[kind] = y1_tmp

print(x)
for kind in ["uni","exp","par","const"]:
    print(y1[kind])
print(y2)

import matplotlib.pyplot as plt
import math


## 描画
n_r = 1    # 行数
n_c = 1    # 列数
fig, axes = plt.subplots(n_r, n_c, tight_layout = True)    # figure オブジェクトの取得

for kind in ["uni","exp","par","const"]:
    axes.plot(x, y1[kind], '-', label = kind, clip_on=False)      #  (x, y1) の描画
axes.plot(x, y2, '*', label = "analysis", clip_on=False)      #  (x, y2) の描画

axes.legend()                 #  注釈の作成

axes.set_ylabel('Loss probability')  # y 軸のラベルを描画
axes.set_xlabel('a')        #   x 軸のラベルを描画

#axes.set_xscale('log')        #   x 軸を対数目盛に変更
axes.set_yscale('log')        #   y 軸を対数目盛に変更

## グラフの保存
fig.savefig("test.png")
