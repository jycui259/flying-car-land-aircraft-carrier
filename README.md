# 把飞机装进后备舱 · 小鹏汇天「陆地航母」调研与安全分析

吉林大学《飞行汽车技术基础》（2026）两次课程作业的 Web 作品。

- **作业一**：针对飞行汽车某技术/产品的全方位调研与分析（技术可行性 / 应用场景 / 市场可行性）
- **作业二**：针对同一对象的全方位安全分析（系统安全工程九步流程 0–8）

研究对象：小鹏汇天分体式飞行汽车「陆地航母」——陆行体（3 轴 6 轮增程平台）+ 飞行体 **X3-F**（六旋翼、可折叠、880 kg、20 km / 20 min）。

## 入口

根目录 `index.html` 即入口：先给结论与关键参数，再分两页展开。

| 页面 | 内容 |
| --- | --- |
| `index.html` | 封面 / 导航 / 关键数字 / 结论 / 交付状态 |
| `assignment-1.html` | 调研与分析：证据分级、产品定义、架构、能量估算、场景矩阵、市场模型、竞品、Go/No-Go |
| `assignment-2.html` | 安全分析：审定基础、功能与场景、架构、软硬件、测试验证、运行论证、FHA / FTA / STPA / GSN |
| `references.html` | 24 条参考文献（GB/T 7714）、证据边界、数据修订记录、AI 使用披露 |

## 目录结构

```
.
├── index.html
├── assignment-1.html
├── assignment-2.html
├── references.html
├── assets/
│   ├── css/site.css          # 全站样式（无外部依赖，含打印样式）
│   ├── js/site.js            # 阅读进度、目录高亮、市场敏感性交互模型
│   └── img/*.svg             # 10 张自绘示意图（架构、矩阵、故障树、GSN 等）
├── tools/
│   ├── figures.py            # 生成全部 SVG（纯标准库）
│   └── qa_site.py            # 结构自检：标签闭合、锚点、资源、引用编号
├── .nojekyll
└── README.md
```

## 本地预览

任选其一（无需安装依赖）：

```bash
python -m http.server 8000
# 打开 http://localhost:8000/
```

或直接双击 `index.html`。页面为纯静态，不请求任何外部字体、CDN 或统计脚本。

## 发布到 GitHub Pages（提交前必做）

课程要求：公开仓库（Public）、根目录 `index.html`、链接填入收集表。

```bash
cd land-aircraft-carrier
git init -b main
git add .
git commit -m "飞行汽车课程作业：陆地航母调研与安全分析"
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后在仓库 **Settings → Pages**：

- Source: `Deploy from a branch`
- Branch: `main`，目录选 `/ (root)`
- 保存后等待 1–2 分钟，得到 `https://<用户名>.github.io/<仓库名>/`

最后把该地址填入课程收集表（作业幻灯片右侧链接），**两个作业共用同一个入口地址**。

## 内容与证据声明

- 一手证据为**民航局 X3-F 型航空器专用条件（征求意见稿，2025-03）**：880 kg、20 km、20 min、VNE 72 km/h、120 m AGL、昼间目视、不用于商业载客。
- 企业口径（价格、订单、产线节拍、陆行体参数）均标注来源；截至 **2026-11-23** 未见 TC 颁发的公开信息，文中所有“交付/量产”表述均以此为条件。
- 所有估算（悬停功率、单位经济、失效概率）均给出公式与假设，标注为 D 级证据，只用于数量级判断。
- 未使用任何企业宣传图片；全部图形为自绘 SVG。
- AI 使用范围与人工核验方式见 `references.html#ai`。

## 重新生成图表

```bash
python tools/figures.py     # 覆盖 assets/img/*.svg
python tools/qa_site.py     # 结构自检，输出 OK 即通过
```

`figures.py` 仅依赖 Python 标准库；字体使用系统字体（Microsoft YaHei / Songti SC 等）。

## 许可

课程作业，仅供教学评审与非商业引用。文中提及的商标与产品参数归各自权利人所有。
