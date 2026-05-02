"""
1. 男女比例 圓餅圖
2. 年齡 15 ~ 80 ,其他刪除 , 並做成10量化 長條圖
3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化橫條圖
4. 課程滿意度 長條圖
5. 軟體熟悉度,群組長條圖
6. 興趣 抓取5個以上的 , 做成長條圖
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1Sb-Q7gI1sH4KGvx_Y6oFgU7_WzCFampfHSJxpQN3VfM/export?format=csv"

df = pd.read_csv(url)

plt.figure(figsize=(16, 10), dpi=120)
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"

df.drop(["時間戳記", "檔案"], axis=1, inplace=True)


# 1. 男女比例 圓餅圖
plt.subplot(241)
s1 = df["性別"].value_counts()
labels = [f"{idx}\n{val}人" for idx, val in s1.items()]
plt.pie(s1, labels=labels, autopct="%1.1f%%")
plt.title("男女比例", fontsize=24)


# 2. 年齡 15 ~ 80 ,其他刪除 , 並做成10量化 長條圖
plt.subplot(242)

df["年齡"] = 2025 - df["出生年月日"].str[:4].astype(int)
df = df[(df["年齡"] >= 15) & (df["年齡"] <= 80)]
df["年齡10量化"] = pd.cut(df["年齡"], bins=range(10, 81, 10), right=False)

df["年齡10量化"] = (
    df["年齡10量化"].astype(str).str.replace("[", "").str.replace(")", "")
)


s2 = df["年齡10量化"].value_counts().sort_index()

s2.index = s2.index.astype(str)
s2.index = s2.index.str[:2]
plt.bar(s2.index, s2.values, color="#C23DF2")
plt.xlabel("各年齡層", fontsize=16)
plt.ylabel("人\n數", fontsize=16, rotation=0, labelpad=20)
plt.title("年齡分布", fontsize=24)
for i in range(len(s2)):
    plt.text(i, s2.iloc[i] + 0.5, f"{s2.iloc[i]}人", ha="center")


# 3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化橫條圖
plt.subplot(243)
df = df[df["年齡"] - df["工作年資"] >= 15]
df["工作年資5量化"] = df["工作年資"] // 5 * 5
s3 = df.groupby("工作年資5量化")["工作年資5量化"].count()
plt.barh(s3.index, s3.values, color="#F2C23D", height=3.7)
plt.xlabel("人數", fontsize=16)
plt.ylabel("工\n作\n年\n資", fontsize=16, rotation=0, labelpad=20, y=0.3)
plt.title("工作年資分布", fontsize=24)
for i in range(len(s3)):
    plt.text(s3.values[i], s3.index[i], f"{s3.iloc[i]}人", va="center")
plt.xlim(0, max(s3.values) + 15)


# 4. 課程滿意度 長條圖
plt.subplot(244)
s4 = df["你對本課程的滿意度"].value_counts().sort_index()
plt.bar(s4.index, s4.values, color="#3DF2C2")
plt.xlabel("滿意度", fontsize=16)
plt.ylabel("人\n數", fontsize=16, rotation=0, labelpad=20)
plt.title(
    f"課程滿意度統計\n平均滿意度{df['你對本課程的滿意度'].mean():.2f}", fontsize=24
)
for i in range(len(s4)):
    plt.text(s4.index[i], s4.iloc[i] + 0.5, f"{s4.iloc[i]}人", ha="center")
plt.grid()

# 5. 軟體熟悉度,群組長條圖
plt.subplot(223)
df1 = df.melt(
    value_vars=[
        "你對以下軟體的熟悉度 [PowerBI]",
        "你對以下軟體的熟悉度 [Excel]",
        "你對以下軟體的熟悉度 [Google 試算表]",
        "你對以下軟體的熟悉度 [Python]",
        "你對以下軟體的熟悉度 [JavaScript]",
        "你對以下軟體的熟悉度 [C 語言]",
    ],
    var_name="軟體",
    value_name="熟悉度",
)
df1["軟體"] = df1["軟體"].str.replace("你對以下軟體的熟悉度 [", "").str.replace("]", "")
jessica = ["C 語言", "Excel", "Google 試算表", "JavaScript", "PowerBI", "Python"]
ada = ["完全不熟", "曾經學過", "普通", "還算熟悉", "非常熟練"]
for i in range(len(ada)):
    s5 = df1[df1["熟悉度"] == ada[i]].groupby("軟體")["軟體"].count()
    plt.bar(
        np.arange(len(jessica)) - 0.32 + 0.16 * i, s5.values, label=ada[i], width=0.16
    )
plt.legend()
plt.xticks(np.arange(len(jessica)), jessica)
plt.xlabel("軟體", fontsize=16)
plt.ylabel("人\n數", fontsize=16, rotation=0, labelpad=20)
plt.title("軟體熟悉度統計", fontsize=24)


# 6. 興趣 抓取5個以上的 , 做成長條圖
plt.subplot(224)
df2 = df["你的興趣"].str.split(",", expand=True)
df3 = pd.DataFrame(df2.values.flatten(), columns=["興趣"]).dropna()
s6 = df3.groupby("興趣")["興趣"].count()
s6 = s6[s6 > 5].sort_values(ascending=False)
plt.bar(s6.index, s6.values, color="#F23D3D")
plt.xlabel("興趣", fontsize=16)
plt.ylabel("人\n數", fontsize=16, rotation=0, labelpad=20)
plt.title("興趣統計", fontsize=24)
for i in range(len(s6)):
    plt.text(i, s6.iloc[i] + 0.5, f"{s6.iloc[i]}人", ha="center")


plt.tight_layout()

plt.savefig("google表單分析.png")
plt.show()
