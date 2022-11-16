import networkx as nx
import numpy as np
from bokeh.events import Tap
from bokeh.io import curdoc
from bokeh.models import Button, Column, ColumnDataSource
from bokeh.plotting import figure

coord_list = []

# 画面構成
plot = figure(
    title="クリックした箇所に点を打ちます",
    tools="tap",
    height=600,
    width=1000,
    x_range=(0, 1000),
    y_range=(0, 600),
)

text_padding = 20.0
source = ColumnDataSource(data=dict(x=[], y=[]))  # 全体で使用する bokeh 用データ
plot.circle(source=source, x="x", y="y", radius=5.0, alpha=0.8)  # クリックして作成する巡回先を点として表示

click_count = 1
# クリックすると点を追加する処理の関数
def callback_click(event):

    global ds
    global coord_list
    global click_count

    coord = (event.x, event.y)  # クリックした位置の座標をタプルに保存
    coord_list.append(coord)  # 座標をリストに保存
    source.data = dict(  # 他の機能で共通して使えるよう座標を souse に保存
        x=[i[0] for i in coord_list], y=[i[1] for i in coord_list]
    )
    plot.text(  # クリックした回数をテキスト表示
        x=[event.x + text_padding],
        y=[event.y + text_padding],
        text=[click_count],
        text_font_size="18px",
        text_baseline="middle",
        text_align="center",
    )
    click_count += 1  # クリックした回数をカウント

    print(coord_list)


# クリックイベントを反映
plot.on_event(Tap, callback_click)

### ボタン処理の関数
def callback_button():
    pass


# ボタンウィジェットの実装
button = Button(label="最適化の実行")
button.on_click(callback_button)

# 全体の構成
layout = Column(plot, button, sizing_mode="scale_width")

# ブラウザに表示するために必要な処理
curdoc().add_root(layout)
