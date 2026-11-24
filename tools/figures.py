# -*- coding: utf-8 -*-
"""Generate the SVG figures used by the two course-work pages.

Every figure is composed from primitives so that typography, colour and
spacing stay consistent across the site. No external libraries are used.
"""
import os, math, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)

INK = "#12171c"
INK2 = "#2b343d"
MUTED = "#5f6d7a"
FAINT = "#8b979f"
LINE = "#d9d2c4"
LINE2 = "#c3baa7"
ACCENT = "#123f5c"
ACCENT2 = "#2a6d8c"
ACC_SOFT = "#e8eef2"
AMBER = "#a9701f"
AMBER_SOFT = "#f7edda"
OK = "#2c6a4d"
OK_SOFT = "#e4efe8"
WARN = "#9c3d1d"
WARN_SOFT = "#f8e6df"
CARD = "#ffffff"
PAPER = "#fbfaf6"

FONT = "'Microsoft YaHei','PingFang SC','Hiragino Sans GB','Segoe UI',sans-serif"
SERIF = "'Songti SC','STSong','SimSun',Georgia,serif"
MONO = "Consolas,'Cascadia Mono',monospace"


def esc(t):
    return html.escape(str(t), quote=True)


def w_of(t, size):
    """Rough text width: CJK 1.0em, latin 0.55em, digits 0.56em."""
    w = 0.0
    for ch in t:
        if ord(ch) > 0x2E80:
            w += size * 1.0
        elif ch in "iljI.,:;'|!":
            w += size * 0.32
        elif ch.isupper():
            w += size * 0.66
        else:
            w += size * 0.55
    return w


def wrap(t, size, maxw):
    lines, cur = [], ""
    for ch in t:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if w_of(cur + ch, size) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.parts = []
        self.title = title

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, t, size=12, fill=INK2, weight=400, anchor="start",
             font=FONT, ls=0, opacity=1):
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"'
            + (f' letter-spacing="{ls}"' if ls else "")
            + (f' opacity="{opacity}"' if opacity != 1 else "")
            + f">{esc(t)}</text>"
        )

    def lines(self, x, y, items, size=12, fill=INK2, weight=400, anchor="start",
              font=FONT, lh=None, ls=0):
        lh = lh or size * 1.45
        for i, t in enumerate(items):
            self.text(x, y + i * lh, t, size, fill, weight, anchor, font, ls)

    def rect(self, x, y, w, h, r=8, fill=CARD, stroke=LINE, sw=1, dash=None, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{opacity}"/>'
        )

    def circle(self, cx, cy, r, fill=CARD, stroke=LINE, sw=1, opacity=1):
        self.add(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
        )

    def path(self, d, stroke=LINE2, fill="none", sw=1.4, dash=None, marker=True):
        m = ' marker-end="url(#arrow)"' if marker else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{m} '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{da}/>'
        )

    def save(self, name):
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="100%" role="img" aria-label="{esc(self.title)}">\n'
            f'<title>{esc(self.title)}</title>\n'
            '<defs>'
            '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker>'
            '<marker id="arrowA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{AMBER}"/></marker>'
            '</defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>\n'
        )
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(head + "\n".join(self.parts) + "\n</svg>\n")
        print("wrote", name, len(self.parts), "nodes")


# --------------------------------------------------------------------------
# 1. 系统架构：陆行体 + 分合机构 + 飞行体 + 支撑/监管
# --------------------------------------------------------------------------
def fig_arch():
    s = SVG(1060, 660, "陆地航母分体式飞行汽车系统架构与外部约束")
    # column headers
    s.text(30, 34, "地面平台 / GROUND PLATFORM", 11.5, AMBER, 700, ls=1.2)
    s.text(410, 34, "接口 / INTERFACE", 11.5, AMBER, 700, ls=1.2)
    s.text(742, 34, "空中平台 / AIR VEHICLE", 11.5, AMBER, 700, ls=1.2)

    # 陆行体 card
    s.rect(24, 50, 320, 350, 10)
    s.text(44, 78, "陆行体（母舰）", 16, INK, 700, font=SERIF)
    s.text(44, 98, "3 轴 6 轮 · 6×6 全驱 · 后轮转向", 11, MUTED)
    rows = [
        ("尺寸", "5.5 × 2.0 × 2.0 m；可入地库、停标准车位"),
        ("动力", "800 V SiC 增程；CLTC 续航 > 1 000 km"),
        ("补能", "行车/驻车为飞行体充电，支持 5–6 次飞行"),
        ("驾驶", "C 类驾照；飞行体另需航空器驾驶资质"),
        ("收纳", "飞行体全折叠入后备舱，随车运输"),
        ("接口", "锁止 + 高压/低压充电 + 数据握手"),
    ]
    y = 124
    for k, v in rows:
        s.text(44, y, k, 10.5, FAINT, 700, ls=1)
        for i, ln in enumerate(wrap(v, 11.5, 246)):
            s.text(86, y + i * 17, ln, 11.5, INK2)
        y += 17 * len(wrap(v, 11.5, 246)) + 10
    s.line(44, 360, 324, 360, LINE, 1)
    s.text(44, 376, "量产：满产 30 min / 台，规划万辆级年产能", 9.2, MUTED)
    s.text(44, 390, "2026-03 批量试产下线并完成多机试飞", 9.2, MUTED)

    # 飞行体 card
    s.rect(716, 50, 320, 350, 10)
    s.text(736, 78, "飞行体 X3-F", 16, INK, 700, font=SERIF)
    s.text(736, 98, "六旋翼 · 双涵道 · 可折叠", 11, MUTED)
    rows = [
        ("构型", "6 电机 + 6 定距桨，差动转速控制姿态"),
        ("偏航", "电涵道在单发失效后提供偏航力矩"),
        ("结构", "碳纤维机身与旋翼；机臂、橇架可折叠"),
        ("收纳", "全折叠 2 934 × 1 777 × 1 312 mm"),
        ("重量", "最大起飞重量 880 kg；2 座（1 驾驶员）"),
        ("包线", "20 km / 20 min / VNE 72 km/h / 120 m"),
        ("限制", "仅昼间目视；私人娱乐与培训，不载客"),
    ]
    y = 124
    for k, v in rows:
        s.text(736, y, k, 10.5, FAINT, 700, ls=1)
        for i, ln in enumerate(wrap(v, 11.5, 246)):
            s.text(778, y + i * 17, ln, 11.5, INK2)
        y += 17 * len(wrap(v, 11.5, 246)) + 10
    s.line(736, 360, 1016, 360, LINE, 1)
    s.text(736, 376, "审定：LSA 类别 + 专用条件（2025-03 征求意见）", 9.2, MUTED)
    s.text(736, 390, "TC 2024-03 受理 · PC 2025-05 受理", 9.2, MUTED)

    # interface block
    s.rect(372, 118, 300, 200, 12, "#fffdf6", AMBER)
    s.text(522, 146, "自动分合机构", 14.5, INK, 700, "middle", SERIF)
    s.text(522, 166, "AUTOMATIC DOCKING", 9.5, AMBER, 700, "middle", ls=1.4)
    items = ["分离 / 结合：约 5 min", "四点锁止 + 到位检测", "运输中飞行体固定约束",
             "地面充电与数据握手", "对接失败 → 禁止起飞互锁"]
    for i, t in enumerate(items):
        s.circle(396, 190 + i * 26, 2.6, AMBER, AMBER)
        s.text(408, 194 + i * 26, t, 11.5, INK2)

    # arrows interface <-> platforms
    s.path("M 344 200 L 366 200", MUTED, sw=1.4)
    s.path("M 372 200 L 350 200", MUTED, sw=1.4)
    s.path("M 678 200 L 710 200", MUTED, sw=1.4)
    s.path("M 716 200 L 684 200", MUTED, sw=1.4)



    # support band
    s.text(30, 428, "支撑体系 / ENABLING SYSTEM", 11.5, AMBER, 700, ls=1.2)
    sup = [("飞行营地", "200+ 个营地与起降点"), ("空域与计划", "飞行计划、目视航路"),
           ("培训与执照", "飞行培训、资质考取"), ("维保与电池", "桨叶/电池/结构检查"),
           ("补能与储运", "随车充电、地库停放"), ("保险与责任", "第三方与乘员险")]
    bw = (1020 - 5 * 10) / 6
    for i, (t, sub) in enumerate(sup):
        x = 24 + i * (bw + 10)
        s.rect(x, 442, bw, 74, 8, CARD, LINE)
        s.text(x + bw / 2, 468, t, 11.5, INK, 700, "middle")
        for j, ln in enumerate(wrap(sub, 9.8, bw - 18)):
            s.text(x + bw / 2, 486 + j * 13, ln, 9.8, MUTED, 400, "middle")

    # regulation rail
    s.rect(24, 540, 1012, 92, 10, ACC_SOFT, "#cfdde5")
    s.text(44, 566, "监管与审定 / REGULATORY RAIL", 11, ACCENT, 700, ls=1.2)
    s.text(44, 588, "CAAC：专用条件（X3 章）→ 型号合格证 TC（2024-03 受理）→ 生产许可证 PC（2025-05 受理）→ 适航证 AC",
           11.5, INK2)
    s.text(44, 610, "阿联酋：GCAA 监管沙盒 + 拉斯海玛示范区（2026-09 协议）；试运行不等于商业载客许可", 11.5, INK2)
    s.text(24 + 1000, 610, "证据截止 2026-11-23", 9.5, MUTED, 400, "end")
    s.save("fig-arch.svg")


# --------------------------------------------------------------------------
# 2. 技术门槛：航程对比
# --------------------------------------------------------------------------
def fig_threshold():
    s = SVG(1040, 500, "航程与载荷：X3-F 与课程实用化门槛及竞品对比")
    left, right = 258, 940
    top = 74
    rows = [
        ("X3-F（陆地航母飞行体）", 20, ACCENT, "审定基础口径（2025-03 征求意见稿）"),
        ("EH216-S（亿航，已取三证）", 30, ACCENT2, "企业公开参数"),
        ("课程实用化门槛", 100, AMBER, "《飞行汽车发展报告 2.0》：航程 ≥ 100 km"),
        ("Archer Midnight", 160, "#7d8b96", "企业公开参数"),
        ("Joby S4", 161, "#7d8b96", "企业公开参数"),
    ]
    maxv = 200
    bw = (right - left) / maxv
    for i, (name, v, col, note) in enumerate(rows):
        y = top + i * 68
        s.text(left - 18, y + 12, name, 11.5, INK if v >= 100 else INK2, 600, "end")
        s.rect(left, y, right - left, 24, 4, "#f1ede3", "#f1ede3")
        s.rect(left, y, max(6, v * bw), 24, 4, col, col)
        s.text(left + max(6, v * bw) + 10, y + 16, f"{v} km", 11.5, col, 700, font=MONO)
        s.text(left - 18, y + 30, note, 9.2, FAINT, 400, "end")
        s.line(right, y - 6, right, y + 30, LINE, 1, "3 3")

    tx = left + 100 * bw
    s.line(tx, top - 20, tx, top + 5 * 68 - 16, AMBER, 1.4, "5 4")
    s.text(tx, top - 28, "实用化门槛 100 km", 10, AMBER, 700, "middle")

    s.rect(left, 428, 470, 52, 8, "#fffdf6", "#eddfc2")
    s.text(left + 14, 450, "20 km ≈ 一线城市 20–30 分钟地面车程；单次飞行 20 min。", 10.6, INK2)
    s.text(left + 14, 468, "结论：营地即目的地，而不是“从 A 到 B 的交通”。", 10.6, AMBER, 600)

    s.text(760, 448, "载荷门槛 ≥ 100 kg：X3-F 双人 154 kg 达标，", 10.2, MUTED)
    s.text(760, 466, "短板集中在航程与速度，而不是载重。", 10.2, MUTED)
    s.save("fig-threshold.svg")


def fig_scenarios():
    s = SVG(940, 620, "应用场景矩阵：技术适配度、监管难度与支付意愿")
    L, R, T, B = 90, 860, 60, 520
    # grid
    for i in range(1, 5):
        x = L + (R - L) * i / 5
        s.line(x, T, x, B, LINE, 1, "3 4")
        y = T + (B - T) * i / 5
        s.line(L, y, R, y, LINE, 1, "3 4")
    s.rect(L, T, R - L, B - T, 8, "none", LINE2)
    # quadrant labels
    s.text(L + 14, T + 26, "优先落地：技术适配高、监管负担低", 10.5, OK, 700)
    s.text(R - 14, T + 26, "观望：价值明确但监管门槛高", 10.5, MUTED, 700, "end")
    s.text(L + 14, B - 14, "不适配 / 长期议题", 10.5, FAINT, 700)
    # axes
    s.add(f'<text x="{(L + R) / 2:.0f}" y="{B + 46}" font-family="{FONT}" font-size="11.5" fill="{MUTED}" font-weight="600" text-anchor="middle">监管与运行许可难度 →</text>')
    s.add(f'<text transform="translate(34,{(T + B) / 2:.0f}) rotate(-90)" font-family="{FONT}" font-size="11.5" fill="{MUTED}" font-weight="600" text-anchor="middle">技术适配度 →</text>')
    # scale ticks
    for i in range(1, 5):
        s.text(L + (R - L) * i / 5, B + 22, str(i), 9.5, FAINT, 400, "middle", MONO)
        s.text(L - 12, B - (B - T) * i / 5 + 4, str(i), 9.5, FAINT, 400, "end", MONO)

    pts = [
        ("营地飞行体验", 2.05, 4.55, 4.5, OK, 12, 4, "start"),
        ("飞行培训", 2.75, 4.45, 3.6, OK, 12, 4, "start"),
        ("私人娱乐 / 收藏", 1.95, 3.95, 4.9, OK, 12, 4, "start"),
        ("景区空中游览", 2.55, 3.55, 4.0, OK, 12, 4, "start"),
        ("赛事与品牌展示", 3.35, 3.35, 3.1, AMBER, 12, 4, "start"),
        ("应急救援", 4.15, 2.0, 4.2, ACCENT, -12, 4, "end"),
        ("高速 / 山区救援", 4.55, 1.42, 3.8, ACCENT, -12, 4, "end"),
        ("即时物流", 3.8, 1.32, 2.3, MUTED, -12, -6, "end"),
        ("城市通勤", 4.95, 1.05, 3.0, WARN, -12, 4, "end"),
        ("城际交通", 4.62, 0.62, 3.4, WARN, -12, 8, "end"),
    ]
    for name, px, py, pay, col, dx, dy, anchor in pts:
        cx = L + (R - L) * px / 5
        cy = B - (B - T) * py / 5
        r = 7 + pay * 2.4
        s.circle(cx, cy, r, col, "#ffffff", 1.6, 0.16)
        s.circle(cx, cy, 3.2, col, col)
        s.text(cx + dx, cy + dy, name, 11, INK2, 600, anchor)

    # legend
    s.text(L, T - 22, "气泡大小 = 支付意愿 / 单位经济潜力", 10, MUTED)
    s.circle(R - 210, T - 26, 8, OK, "#fff", 1.6, 0.16); s.text(R - 196, T - 22, "可落地", 10, MUTED)
    s.circle(R - 130, T - 26, 8, AMBER, "#fff", 1.6, 0.16); s.text(R - 116, T - 22, "条件成立", 10, MUTED)
    s.circle(R - 46, T - 26, 8, WARN, "#fff", 1.6, 0.16); s.text(R - 32, T - 22, "不成立", 10, MUTED)
    s.save("fig-scenarios.svg")


# --------------------------------------------------------------------------
# 4. 竞争定位：航程 × 道路能力
# --------------------------------------------------------------------------
def fig_compete():
    s = SVG(980, 600, "竞品定位：航程与道路行驶能力")
    L, R, T, B = 140, 900, 60, 500
    def X(v):
        return L + (math.log10(v) - 1) / (math.log10(300) - 1) * (R - L)
    def Y(v):
        return B - v / 3 * (B - T)

    for tick in [10, 20, 30, 50, 100, 200, 300]:
        x = X(tick)
        s.line(x, T, x, B, LINE, 1, "3 4")
        s.text(x, B + 22, str(tick), 9.5, FAINT, 400, "middle", MONO)
    ylabels = ["纯飞 / 需专用起降", "可收纳 / 可拖运", "分体式：可驾驶 + 可飞", "一体式：陆空两栖"]
    for i in range(4):
        y = Y(i)
        s.line(L, y, R, y, LINE, 1, "3 4")
        s.text(L - 14, y + 4, ylabels[i], 9.4, MUTED, 400, "end")

    s.text((L + R) / 2, B + 48, "航程（km，对数刻度；企业口径或审定口径）", 11, MUTED, 600, "middle")
    s.add(f'<text transform="translate(34,{(T + B) / 2:.0f}) rotate(-90)" font-family="{FONT}" font-size="11" fill="{MUTED}" font-weight="600" text-anchor="middle">道路行驶能力 →</text>')

    pts = [
        ("陆地航母 X3-F", 20, 2.55, ACCENT, "≤200 万元 · TC/PC 已受理", 14, 4, "start"),
        ("EH216-S", 30, 0.15, ACCENT2, "已取 TC/PC/AC · 无人驾驶", 14, 4, "start"),
        ("Alef Model A", 177, 2.9, "#6b7c88", "陆空两栖概念 · 企业口径", 0, -16, "middle"),
        ("Joby S4", 161, 0.08, "#8b979f", "FAA 审定路径", -14, 4, "end"),
        ("Archer Midnight", 160, 0.42, "#8b979f", "FAA 审定路径", 0, -34, "middle"),
        ("沃飞长空 AE200", 215, 0.08, "#9aa7b1", "eVTOL 航线", 12, 4, "start"),
    ]
    for name, rng, road, col, note, dx, dy, anchor in pts:
        cx, cy = X(rng), Y(road)
        s.circle(cx, cy, 7, col, "#fff", 2)
        s.text(cx + dx, cy + dy, name, 11.3, INK, 700, anchor)
        s.text(cx + dx, cy + dy + 14, note, 9.2, MUTED, 400, anchor)

    s.rect(L + 12, T + 210, 316, 62, 8, "#fffdf6", "#eddfc2")
    s.text(L + 26, T + 232, "竞争空白：能开、能装、能飞，但飞不远", 10.8, AMBER, 700)
    s.text(L + 26, T + 252, "X3-F 用道路合法性与收纳性换取航程与速度。", 10, INK2)
    s.save("fig-compete.svg")


# --------------------------------------------------------------------------
# 5. 安全架构分层
# --------------------------------------------------------------------------
def fig_safety_arch():
    s = SVG(1060, 700, "X3-F 安全架构分层：能量、控制、乘员与运行")
    # layer bands
    bands = [
        ("L4 运行与人员", T := 56, 96, "#f6f1e6", "#e6dcc6"),
        ("L3 乘员与结构", 176, 132, "#fbf7ee", "#e8dcc2"),
        ("L2 控制与感知", 332, 150, "#eef3f7", "#d3e0e9"),
        ("L1 能量与推进", 506, 150, "#f3f7f4", "#cfe0d6"),
    ]
    for name, y, h, fill, stroke in bands:
        s.rect(24, y, 1012, h, 10, fill, stroke)
        s.text(40, (y - 8) if name.startswith("L4") else (y + 22), name, 10.5, MUTED, 700, ls=1.2)

    # L1
    s.rect(44, 542, 190, 96, 8, CARD, LINE2)
    s.text(139, 566, "动力电池包", 12, INK, 700, "middle")
    s.text(139, 584, "高硅高镍 · 25C 峰值", 9.8, MUTED, 400, "middle")
    s.text(139, 600, "BMS：过温/过流/绝缘", 9.8, MUTED, 400, "middle")
    s.text(139, 620, "单点失效不得灾难性", 9.8, WARN, 600, "middle")
    s.rect(262, 542, 190, 96, 8, CARD, LINE2)
    s.text(357, 566, "高压配电", 12, INK, 700, "middle")
    s.text(357, 584, "接触器 · 熔断 · 预充", 9.8, MUTED, 400, "middle")
    s.text(357, 600, "手动隔离开关", 9.8, MUTED, 400, "middle")
    s.text(357, 620, "不依赖软件动作", 9.8, WARN, 600, "middle")
    s.rect(480, 536, 350, 108, 8, CARD, LINE2)
    s.text(655, 558, "六路电推进单元", 12, INK, 700, "middle")
    for i in range(6):
        x = 500 + (i % 3) * 108
        y = 570 + (i // 3) * 34
        s.rect(x, y, 96, 26, 5, "#eef3f7", "#cfdde5")
        s.text(x + 48, y + 17, f"M{i+1} + ESC + 定距桨", 8.8, INK2, 400, "middle")
    s.text(655, 638, "差动转速 → 姿态控制；单发失效后由电涵道补偏航", 9.6, MUTED, 400, "middle")
    s.rect(858, 542, 158, 96, 8, CARD, LINE2)
    s.text(937, 566, "电涵道", 12, INK, 700, "middle")
    s.text(937, 584, "偏航力矩备份", 9.8, MUTED, 400, "middle")
    s.text(937, 600, "叶片 2× 离心载荷", 9.8, MUTED, 400, "middle")
    s.text(937, 620, "X3.1433", 9.8, ACCENT, 600, "middle")

    # L2
    s.rect(44, 360, 250, 106, 8, CARD, LINE2)
    s.text(169, 384, "飞控计算机", 12, INK, 700, "middle")
    s.text(169, 402, "电传操纵 · 保护功能", 9.8, MUTED, 400, "middle")
    s.text(169, 419, "姿态角 / 偏航率 / 过载 / 速度限制", 9.4, INK2, 400, "middle")
    s.text(169, 436, "飞行前自检 + 全程监控", 9.4, INK2, 400, "middle")
    s.text(169, 455, "冗余度未公开 → 按单点失效准则倒推", 9.2, WARN, 600, "middle")
    s.rect(316, 360, 236, 106, 8, CARD, LINE2)
    s.text(434, 384, "传感器组", 12, INK, 700, "middle")
    s.text(434, 402, "IMU · 气压高度 · GNSS · 磁罗盘", 9.8, MUTED, 400, "middle")
    s.text(434, 419, "交叉校验与故障隔离", 9.4, INK2, 400, "middle")
    s.text(434, 437, "（配置与数量未公开）", 9.2, FAINT, 400, "middle")
    s.rect(574, 360, 212, 106, 8, CARD, LINE2)
    s.text(680, 384, "分合机构控制", 12, INK, 700, "middle")
    s.text(680, 402, "状态机 + 到位检测", 9.8, MUTED, 400, "middle")
    s.text(680, 419, "空中禁止解锁互锁", 9.4, WARN, 600, "middle")
    s.text(680, 437, "对接失败 → 禁止起飞", 9.2, INK2, 400, "middle")
    s.rect(808, 360, 208, 106, 8, CARD, LINE2)
    s.text(912, 384, "告警与人机界面", 12, INK, 700, "middle")
    s.text(912, 402, "电量 / 转速 / 模式指示", 9.8, MUTED, 400, "middle")
    s.text(912, 419, "保护功能门限告警", 9.4, INK2, 400, "middle")
    s.text(912, 437, "单杆操纵，手动/自动", 9.2, INK2, 400, "middle")

    # L3
    s.rect(44, 200, 232, 108, 8, CARD, LINE2)
    s.text(160, 224, "乘员约束", 12, INK, 700, "middle")
    s.text(160, 244, "四点式安全带 + 肩带", 9.8, MUTED, 400, "middle")
    s.text(160, 262, "座椅按 77 kg 乘员设计", 9.8, MUTED, 400, "middle")
    s.text(160, 282, "刚性件包裹，防二次碰撞", 9.6, INK2, 400, "middle")
    s.rect(294, 200, 232, 108, 8, CARD, LINE2)
    s.text(410, 224, "结构吸能", 12, INK, 700, "middle")
    s.text(410, 244, "四点橇式起落架 + 落震试验", 9.6, MUTED, 400, "middle")
    s.text(410, 262, "应急着陆惯性载荷", 9.8, MUTED, 400, "middle")
    s.text(410, 282, "“可控应急着陆”是顶层目标", 9.6, WARN, 600, "middle")
    s.rect(544, 200, 232, 108, 8, CARD, LINE2)
    s.text(660, 224, "折叠与锁定", 12, INK, 700, "middle")
    s.text(660, 244, "机臂 / 桨叶 / 起落架折叠", 9.8, MUTED, 400, "middle")
    s.text(660, 262, "飞行中禁止解锁（X3.612/729）", 9.6, INK2, 400, "middle")
    s.text(660, 282, "间隙与干涉检查", 9.8, MUTED, 400, "middle")
    s.rect(794, 200, 222, 108, 8, CARD, LINE2)
    s.text(905, 224, "应急出口与逃生", 12, INK, 700, "middle")
    s.text(905, 244, "舱门/出口尺寸与操作力", 9.8, MUTED, 400, "middle")
    s.text(905, 262, "落水/起火后撤离", 9.8, MUTED, 400, "middle")
    s.text(905, 282, "（公开资料有限）", 9.4, FAINT, 400, "middle")

    # L4
    s.rect(44, 66, 960, 72, 8, CARD, "#e6dcc6")
    chips = ["昼间目视 VMC", "≤120 m AGL", "航程 ≤20 km", "VNE 72 km/h", "营地隔离区", "风速/能见度限值",
             "资质与培训", "飞行计划报备", "维护与持续适航"]
    x = 60
    for c in chips:
        w = w_of(c, 10.5) + 22
        s.rect(x, 87, w, 30, 15, "#fff", "#e0d3b8")
        s.text(x + w / 2, 106, c, 10.5, INK2, 600, "middle")
        x += w + 8
    s.text(44, 166, "运行包线本身就是安全措施：把“能飞的条件”收窄，比事后增加冗余更有效。", 10.8, AMBER, 600)
    s.save("fig-safety-arch.svg")


# --------------------------------------------------------------------------
# 6. 故障树
# --------------------------------------------------------------------------
def gate(s, x, y, label, kind="OR", w=54):
    # AND/OR gate symbol
    s.add(f'<path d="M {x-w/2} {y} L {x-w/2} {y-26} Q {x} {y-60} {x+w/2} {y-26} L {x+w/2} {y} Z" '
          f'fill="{CARD}" stroke="{WARN}" stroke-width="1.6"/>')
    s.text(x, y - 18, kind, 9, WARN, 700, "middle")


def fig_fta():
    s = SVG(1080, 640, "故障树：不可控坠落的顶事件与主要割集")
    s.text(24, 26, "故障树 / FAULT TREE", 11, AMBER, 700, ls=1.2)

    s.rect(390, 46, 300, 54, 10, "#f9e2dc", WARN)
    s.text(540, 70, "空中失控 / 不可控坠落", 13, "#5f160d", 700, "middle")
    s.text(540, 88, "灾难性 · Catastrophic", 9.5, WARN, 600, "middle")

    def orgate(x, y, w=42, h=22):
        s.rect(x - w / 2, y - h / 2, w, h, 4, "#fffdf6", WARN, 1.4)
        s.text(x, y + 3.5, "OR", 8.6, WARN, 700, "middle", MONO)

    s.path("M 540 100 L 540 118", MUTED, sw=1.2, marker=False)
    orgate(540, 130)

    branches = [
        (98, "升力/推力不对称不可控", "A"),
        (306, "飞行控制失效", "B"),
        (514, "能源失效", "C"),
        (722, "结构与机构失效", "D"),
        (930, "人为与环境", "E"),
    ]
    for x, label, code in branches:
        s.rect(x - 88, 158, 176, 44, 8, CARD, LINE2)
        s.text(x, 178, label, 10.6, INK, 700, "middle")
        s.text(x, 194, code, 9, FAINT, 700, "middle", MONO)
        s.path(f"M 540 141 L 540 150 L {x} 150 L {x} 158", MUTED, sw=1.1, marker=False)
        s.path(f"M {x} 202 L {x} 216", MUTED, sw=1.1)
        orgate(x, 228)
        s.path(f"M {x} 239 L {x} 252", MUTED, sw=1, marker=False)

    leaves = {
        98: ["同侧双电机/电调失效", "桨叶脱落或断裂", "偏航补偿（电涵道）失效"],
        306: ["飞控单点硬件失效", "传感器共因失效", "软件/集成错误"],
        514: ["电池热失控", "高压母线短路", "电量耗尽 + 告警失效"],
        722: ["机臂折叠锁空中解锁", "桨毂/接头疲劳失效", "分合机构空中解锁"],
        930: ["空间定向障碍/误操作", "阵风/下洗超限", "目视条件恶化"],
    }
    for x, items in leaves.items():
        ys, hh = [], []
        y = 258
        for it in items:
            lines = wrap(it, 9.6, 150)
            h = 24 + 13 * (len(lines) - 1)
            ys.append(y); hh.append(h)
            y += h + 12
        # bus first, so the opaque boxes cover it
        s.line(x, 239, x, ys[-1], LINE2, 1)
        for idx, it in enumerate(items):
            lines = wrap(it, 9.6, 150)
            h = hh[idx]
            s.rect(x - 86, ys[idx], 172, h, 6, "#fff", LINE)
            for i, ln in enumerate(lines):
                s.text(x, ys[idx] + 16 + i * 13, ln, 9.6, INK2, 400, "middle")

    s.rect(30, 418, 500, 190, 10, "#fffdf6", "#eddfc2")
    s.text(48, 444, "最小割集（示例，按公开构型推断）", 11, AMBER, 700)
    rows = [
        "① 同侧两路推进失效 + 电涵道偏航不可用",
        "② 飞控单点失效未被隔离（违反 X3.1331(c)）",
        "③ 电池热失控 → 高压失效 → 迫降/起火",
        "④ 折叠锁定空中解锁（违反 X3.612）",
        "⑤ 飞行员空间定向障碍 + 无自动改出",
    ]
    for i, r in enumerate(rows):
        s.text(48, 470 + i * 24, r, 10.4, INK2)

    s.text(560, 444, "为何用“不可控坠落”作顶事件？", 11, AMBER, 700)
    s.text(560, 470, "专用条件把“可控应急着陆”定义为顶层安全目标：", 10.4, INK2)
    s.text(560, 492, "允许机体损坏，但必须保护乘员免受严重伤害。", 10.4, INK2)
    s.text(560, 520, "因此顶事件不是“任何故障”，而是“丧失可控", 10.4, INK2)
    s.text(560, 542, "应急着陆能力”，与审定语言保持一致。", 10.4, INK2)
    s.text(560, 574, "定量结果见正文表 9-3（假设值，仅数量级）。", 9.6, MUTED)
    s.save("fig-fta.svg")


# --------------------------------------------------------------------------
# 7. STPA 控制结构
# --------------------------------------------------------------------------
def fig_stpa():
    s = SVG(1040, 640, "STPA 控制结构：控制器、控制动作与反馈")
    s.rect(24, 26, 992, 74, 10, "#f6f1e6", "#e6dcc6")
    s.text(44, 52, "系统边界：一次完整飞行任务（运输—分离—起飞—20 min 飞行—着陆—收纳）", 11.5, INK, 700)
    s.text(44, 74, "环境扰动：阵风、地面效应、降水/能见度、电磁干扰、地面人员与障碍物、空域其他用户", 10.4, MUTED)

    boxes = {
        "pilot": (60, 140, 210, 96, "驾驶员", "单杆操纵 · 目视飞行\n培训与资质是安全前提"),
        "fcc": (350, 140, 220, 96, "飞控计算机 FCC", "指令解算 · 保护功能\n自检与监控"),
        "esc": (660, 120, 150, 60, "电调 ×6", "转速闭环"),
        "fan": (660, 200, 150, 60, "电涵道", "偏航力矩"),
        "bms": (660, 300, 150, 60, "BMS", "电量/温度/绝缘"),
        "dock": (60, 300, 210, 80, "分合机构控制器", "分离/对接状态机"),
        "ac": (350, 300, 220, 90, "航空器（被控过程）", "姿态 · 高度 · 位置 · 能量"),
    }
    for k, (x, y, w, h, t, sub) in boxes.items():
        s.rect(x, y, w, h, 8, CARD, LINE2)
        s.text(x + w / 2, y + 26, t, 12, INK, 700, "middle")
        for i, ln in enumerate(sub.split("\n")):
            s.text(x + w / 2, y + 46 + i * 15, ln, 9.8, MUTED, 400, "middle")

    # control actions
    s.path("M 270 180 L 344 180", ACCENT2, sw=1.6)
    s.text(307, 172, "杆量/模式", 9.2, ACCENT, 600, "middle")
    s.path("M 570 168 L 654 150", ACCENT2, sw=1.6)
    s.text(612, 150, "转速指令", 9.2, ACCENT, 600, "middle")
    s.path("M 570 190 L 654 224", ACCENT2, sw=1.6)
    s.text(612, 220, "偏航指令", 9.2, ACCENT, 600, "middle")
    s.path("M 570 210 L 654 322", ACCENT2, sw=1.6)
    s.text(600, 280, "接触器/限流", 9.2, ACCENT, 600, "middle")
    s.path("M 270 330 L 344 330", ACCENT2, sw=1.6)
    s.text(307, 322, "分离/对接", 9.2, ACCENT, 600, "middle")

    # feedback
    s.path("M 344 200 L 276 200", MUTED, sw=1.2, dash="4 3")
    s.text(310, 214, "姿态/告警", 9.2, MUTED, 400, "middle")
    s.path("M 650 176 L 576 180", MUTED, sw=1.2, dash="4 3")
    s.text(612, 194, "转速反馈", 9.2, MUTED, 400, "middle")
    s.path("M 650 232 L 576 200", MUTED, sw=1.2, dash="4 3")
    s.path("M 650 320 L 460 392", MUTED, sw=1.2, dash="4 3")
    s.text(556, 372, "电量/温度", 9.2, MUTED, 400, "middle")
    s.path("M 344 372 L 276 372", MUTED, sw=1.2, dash="4 3")
    s.text(310, 390, "锁定/到位", 9.2, MUTED, 400, "middle")

    # pilot environmental inputs
    s.path("M 160 236 L 160 292", MUTED, sw=1.2, dash="4 3")
    s.text(170, 268, "目视/外部线索", 9.2, MUTED)

    # legend
    s.rect(560, 440, 456, 168, 10, "#fbfdff", "#d3e0e9")
    s.text(578, 466, "STPA 关注的四类不安全控制动作（UCA）", 11, ACCENT, 700)
    items = [
        "未提供：该给转速/偏航时未给（如失速前未加推力）",
        "提供不当：给错量或错时序（如着陆前收油门过早）",
        "过早/过晚：超出时序窗口（如未达安全高度即分离）",
        "停止过快/过久：中断必要控制（如保护功能被误关闭）",
    ]
    for i, t in enumerate(items):
        s.circle(586, 490 + i * 26, 2.6, ACCENT)
        s.text(598, 494 + i * 26, t, 10.2, INK2)

    # right note
    s.rect(24, 440, 516, 168, 10, "#fffdf6", "#eddfc2")
    s.text(42, 466, "为什么 STPA 必要？", 11, AMBER, 700)
    s.text(42, 490, "FTA 擅长“部件失效”，但 X3-F 的主要风险还来自：", 10.2, INK2)
    s.text(42, 512, "① 组件交互（飞控与电调、电涵道与主旋翼）", 10.2, INK2)
    s.text(42, 534, "② 人机协同（单杆操纵、模式切换、目视判断）", 10.2, INK2)
    s.text(42, 556, "③ 运行限制的越界（风速、能见度、营地净空）", 10.2, INK2)
    s.text(42, 578, "这些不是“坏了一个零件”，而是控制回路设计问题。", 10.2, AMBER, 600)
    s.save("fig-stpa.svg")


# --------------------------------------------------------------------------
# 8. 风险矩阵
# --------------------------------------------------------------------------
def fig_risk():
    s = SVG(1000, 640, "风险矩阵：主要危害的严重度与可能性")
    L, T, cell = 178, 104, 96
    s.text(24, 34, "风险矩阵 / RISK MATRIX", 11, AMBER, 700, ls=1.2)
    s.text(24, 54, "位置为本文定性判断；H1–H4 属“单点失效即灾难”路径，应由架构消除，而不是靠运行限制兜底。", 10, MUTED)
    cols = ["极不可能", "很少", "偶尔", "可能", "频繁"]
    rows = ["灾难性", "危险", "较大", "轻微", "可忽略"]

    def score(r, c):
        return (5 - r) * (c + 1)

    for r in range(5):
        for c in range(5):
            sc = score(r, c)
            fill = "#eef6f1" if sc <= 6 else "#fbf7e8" if sc <= 10 else "#fdf0e6" if sc <= 15 else "#f4d9d0"
            s.rect(L + c * cell, T + r * cell, cell, cell, 0, fill, "#ffffff", 1)
    for r, name in enumerate(rows):
        s.text(L - 16, T + r * cell + cell / 2 + 5, name, 11, INK2, 700, "end")
    for c, name in enumerate(cols):
        s.add(f'<text transform="translate({L + c * cell + cell / 2 + 20},{T - 10}) rotate(-22)" '
              f'font-family="{FONT}" font-size="10.5" fill="{MUTED}" text-anchor="start">{esc(name)}</text>')
    s.text(L, T + 5 * cell + 44, "可能性（每飞行小时 / 每架次）→", 11, MUTED, 600)
    s.add(f'<text transform="translate(60,{T + 2.5 * cell}) rotate(-90)" font-family="{FONT}" font-size="11" fill="{MUTED}" font-weight="600" text-anchor="middle">严重度 →</text>')

    # (code, row, col, label, ox, oy, dx, dy, anchor)
    pts = [
        ("H1", 0, 1, "电池热失控", 0, 0, 18, 4, "start"),
        ("H2", 0, 2, "同侧双推进失效", -15, -13, 18, -4, "start"),
        ("H3", 0, 2, "飞控单点失效", 15, 13, 18, 14, "start"),
        ("H4", 0, 3, "折叠锁定空中解锁", 0, 0, -18, 4, "end"),
        ("H6", 0, 4, "飞行员定向障碍", 0, 0, 0, -20, "middle"),
        ("H5", 1, 1, "分合机构误动作", 0, 0, -18, 4, "end"),
        ("H10", 1, 2, "坠撞后起火", 0, 0, 18, 4, "start"),
        ("H9", 2, 2, "充电 / 储运火灾", 0, 0, -18, 4, "end"),
        ("H7", 2, 3, "阵风 / 下洗超限", 0, 0, 18, 4, "start"),
        ("H8", 3, 3, "地面人员进入旋翼区", 0, 0, 18, 4, "start"),
    ]
    for code, r, c, name, ox, oy, dx, dy, anchor in pts:
        x = L + c * cell + cell / 2 + ox
        y = T + r * cell + cell / 2 + oy
        s.circle(x, y, 14, "#ffffff", WARN, 1.5)
        s.text(x, y + 3.6, code, 8.8, WARN, 700, "middle", MONO)
        s.text(x + dx, y + dy, name, 9.4, INK2, 600, anchor)

    # side legend
    lx = L + 5 * cell + 40
    s.text(lx, T + 12, "处置原则", 10.5, ACCENT, 700)
    rules = ["红色：不可接受，必须改设计", "橙色：ALARP，需证明已降至最低", "黄色：运行程序与培训控制", "绿色：可接受，保持监控"]
    for i, t in enumerate(rules):
        col = ["#c4634a", "#d99a5b", "#d9c07a", "#8fb9a2"][i]
        s.rect(lx, T + 28 + i * 34, 10, 10, 2, col, col)
        for j, ln in enumerate(wrap(t, 9.2, 118)):
            s.text(lx + 18, T + 37 + i * 34 + j * 13, ln, 9.2, MUTED)
    s.text(lx, T + 190, "注：本图不对应", 9.2, FAINT)
    s.text(lx, T + 204, "任何官方风险接受", 9.2, FAINT)
    s.text(lx, T + 218, "准则。", 9.2, FAINT)
    s.save("fig-risk.svg")


# --------------------------------------------------------------------------
# 9. GSN 安全案例
# --------------------------------------------------------------------------
def fig_gsn():
    s = SVG(1040, 660, "GSN 安全论证结构")
    def goal(x, y, w, h, t, sub=None, fill=CARD):
        s.rect(x, y, w, h, 8, fill, ACCENT, 1.4)
        for i, ln in enumerate(wrap(t, 11, w - 20)):
            s.text(x + w / 2, y + 24 + i * 15, ln, 11, INK, 700, "middle")
        if sub:
            s.text(x + w / 2, y + h - 12, sub, 9, MUTED, 400, "middle")

    def strat(x, y, w, h, t):
        # parallelogram
        s.add(f'<path d="M {x+14} {y} L {x+w} {y} L {x+w-14} {y+h} L {x} {y+h} Z" '
              f'fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.3"/>')
        for i, ln in enumerate(wrap(t, 10.2, w - 34)):
            s.text(x + w / 2, y + 22 + i * 14, ln, 10.2, "#6b4512", 600, "middle")

    def sol(x, y, r, t):
        s.circle(x, y, r, OK_SOFT, OK, 1.4)
        for i, ln in enumerate(wrap(t, 8.8, r * 1.5)):
            s.text(x, y - 4 + i * 11, ln, 8.8, "#1f4d37", 500, "middle")

    goal(360, 30, 320, 66, "在批准运行包线内，X3-F 的乘员与第三方风险处于可接受且 ALARP 的水平", "G1 · 顶层安全目标")
    s.rect(700, 34, 300, 58, 6, "#f6f1e6", "#e6dcc6")
    s.text(714, 54, "C1 运行包线：昼间 VMC · ≤120 m AGL", 9.4, INK2)
    s.text(714, 72, "≤20 km · 2 人 · 营地隔离运行", 9.4, INK2)

    strat(330, 132, 380, 56, "S1 按 CCAR-21-R5 专用条件逐条符合，并对未覆盖风险补充分析")

    goal(40, 226, 290, 62, "结构、机构与乘员保护满足应急着陆要求", "G2")
    goal(370, 226, 300, 62, "单点失效不导致灾难性状态", "G3")
    goal(710, 226, 290, 62, "运行限制、人员与地面程序可控", "G4")
    for x in (185, 520, 855):
        s.path(f"M 520 188 L 520 208 L {x} 208 L {x} 226", MUTED, sw=1.2, marker=False)
        s.path(f"M {x} 208 L {x} 226", MUTED, sw=1.2)

    subs = [
        (40, ["静力/落震/桨叶试验", "折叠锁定防空中解锁", "座椅安全带与出口"]),
        (370, ["FHA/PSSA/FTA/CCA", "FCS 与电池单点分析", "故障注入与 HIL"]),
        (710, ["营地净空与隔离", "培训与执照", "风速/能见度限制"]),
    ]
    for x, items in subs:
        # vertical evidence bus drawn first so boxes sit on top of it
        s.line(x + 145, 288, x + 145, 450, LINE2, 1)
        y = 320
        for it in items:
            s.rect(x, y, 290, 34, 6, "#fff", LINE)
            s.text(x + 12, y + 22, "· " + it, 9.8, INK2)
            y += 42

    sol(185, 508, 48, "S2 符合性报告 / 试验数据")
    sol(520, 508, 48, "S3 安全分析档案")
    sol(855, 508, 48, "S4 运行手册与训练记录")

    sol(185, 508, 48, "S2 符合性报告 / 试验数据")
    sol(520, 508, 48, "S3 安全分析档案")
    sol(855, 508, 48, "S4 运行手册与训练记录")
    for x in (185, 520, 855):
        s.path(f"M {x} 456 L {x} 460", MUTED, sw=1, marker=False)

    s.rect(40, 576, 960, 56, 8, "#fbfdff", "#d3e0e9")
    s.text(56, 598, "论证缺口（本文识别）：TC 尚未颁发；飞控/电池冗余架构、软件保证等级（DO-178C/DO-254）、", 10.2, INK2)
    s.text(56, 618, "定量失效概率目标与第三方地面风险模型均未公开，因此 G3 目前只能给出“定性符合 + 待验证”。", 10.2, INK2)
    s.save("fig-gsn.svg")


# --------------------------------------------------------------------------
# 10. V 模型 / 九步流程
# --------------------------------------------------------------------------
def fig_vmodel():
    s = SVG(1020, 600, "智能运载工具安全系统工程：九步流程与 V 模型映射")
    # step 0 band
    s.rect(40, 24, 940, 46, 8, "#f6f1e6", "#e6dcc6")
    s.text(56, 44, "0  安全文化与安全管理", 11.5, INK, 700)
    s.text(230, 44, "组织与职责 · 变更管理 · 安全绩效 · 方法/工具充分性 · 供应商与追溯", 10.2, MUTED)
    s.text(56, 62, "贯穿全生命周期：从概念、设计、验证到运行与持续适航", 9.4, FAINT)

    left = [
        ("1", "整机功能与场景定义", "ConOps · 运行设计条件 ODC · 任务剖面"),
        ("2", "安全分析方法", "FHA / PSSA / FTA / FMEA / CCA / STPA"),
        ("3", "系统安全架构", "冗余、隔离、失效降级、1oo2 / 2oo3"),
        ("4", "硬件安全设计", "电池、电驱、桨叶、折叠锁定、结构"),
        ("5", "软件与智能系统", "电传飞控、SOTIF、网络安全 TARA"),
        ("6", "机械 / 化学 / 电气", "高压、热失控、火灾、人因与工效"),
    ]
    y = 96
    for i, (n, t, sub) in enumerate(left):
        s.rect(70, y, 330, 58, 8, CARD, LINE2)
        s.circle(96, y + 29, 13, ACC_SOFT, "#cfdde5")
        s.text(96, y + 33, n, 10, ACCENT, 700, "middle", MONO)
        s.text(118, y + 24, t, 11.5, INK, 700)
        s.text(118, y + 42, sub, 9.4, MUTED)
        if i < 5:
            s.path(f"M 235 {y+58} L 235 {y+70}", MUTED, sw=1.2)
        y += 70

    # vertex
    s.rect(70, 516, 330, 48, 24, "#fffdf6", AMBER)
    s.text(235, 537, "系统集成与确认", 11, "#6b4512", 700, "middle")
    s.text(235, 553, "“是否做对” → “是否做对了产品”", 9.2, "#6b4512", 400, "middle")
    s.path("M 235 510 L 235 516", MUTED, sw=1.2, marker=False)

    # right arm
    s.rect(660, 516, 330, 48, 24, "#fbfdff", "#d3e0e9")
    s.text(825, 537, "符合性证据与安全案例", 11, ACCENT, 700, "middle")
    s.text(825, 553, "试验报告 · 分析档案 · 运行记录", 9.2, MUTED, 400, "middle")
    s.path("M 400 540 L 654 540", MUTED, sw=1.4)

    right = [
        ("7", "安全测试与验证", "部件 / 系统 / 整机 / 场景，失效注入", 442),
        ("8", "运行安全论证", "GSN、ALARP、持续适航、数据闭环", 372),
    ]
    for n, t, sub, yy in right:
        s.rect(660, yy, 330, 58, 8, CARD, LINE2)
        s.circle(686, yy + 29, 13, ACC_SOFT, "#cfdde5")
        s.text(686, yy + 33, n, 10, ACCENT, 700, "middle", MONO)
        s.text(708, yy + 24, t, 11.5, INK, 700)
        s.text(708, yy + 42, sub, 9.4, MUTED)
    s.path("M 825 516 L 825 500", MUTED, sw=1.2)
    s.path("M 825 442 L 825 430", MUTED, sw=1.2)

    # annotations
    s.text(512, 236, "左侧：自顶向下分解", 10.5, MUTED, 600, "middle")
    s.text(512, 254, "把顶层安全目标逐层落到", 9.6, FAINT, 400, "middle")
    s.text(512, 270, "功能、架构、软硬件与运行限制", 9.6, FAINT, 400, "middle")
    s.text(512, 300, "右侧：自底向上验证", 10.5, MUTED, 600, "middle")
    s.text(512, 318, "用试验、分析与运行数据", 9.6, FAINT, 400, "middle")
    s.text(512, 334, "反向支撑顶层目标", 9.6, FAINT, 400, "middle")

    s.save("fig-vmodel.svg")


if __name__ == "__main__":
    fig_arch()
    fig_threshold()
    fig_scenarios()
    fig_compete()
    fig_safety_arch()
    fig_fta()
    fig_stpa()
    fig_risk()
    fig_gsn()
    fig_vmodel()








