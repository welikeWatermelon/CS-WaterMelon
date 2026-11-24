"""logs/ 의 학습 기록을 읽어서 README의 잔디(SVG), 통계, 과목별 진도표를 갱신해요.

실행: python scripts/update_readme.py   (repo 루트에서)
외부 라이브러리 없이 표준 라이브러리만 써요.
"""
from __future__ import annotations

import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
README = ROOT / "README.md"
ROADMAP = ROOT / "roadmap.md"
SVG_PATH = ROOT / "assets" / "heatmap.svg"

KST = timezone(timedelta(hours=9))
WEEKS = 26  # 잔디에 보여줄 주 수 (약 6개월)

SUBJECTS = [
    ("os", "OS"),
    ("network", "Network"),
    ("db", "DB"),
    ("java", "Java"),
    ("spring", "Spring"),
    ("infra", "Infra / Cloud"),
    ("system-design", "시스템 설계"),
]
# roadmap.md 의 '## ' 헤더 앞부분으로 과목을 찾아요
ROADMAP_KEYS = {
    "os": "OS",
    "network": "Network",
    "db": "DB",
    "java": "Java",
    "spring": "Spring",
    "infra": "Infra",
    "system-design": "시스템 설계",
}

# 모던 테마: 빈 칸은 연한 회색, 공부량이 많을수록 진한 초록
COLORS = ["#ebedf0", "#bfe6c6", "#7cc68c", "#3a9a56", "#1d6b38"]
BORDER = "#e4e7eb"
BG = "#ffffff"
TEXT = "#6b7280"
TITLE = "#111827"


def parse_front_matter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.split("#", 1)[0].strip()
        if v.startswith("[") and v.endswith("]"):
            data[k.strip()] = [s.strip() for s in v[1:-1].split(",") if s.strip()]
        else:
            data[k.strip()] = v
    return data


def load_logs():
    days = {}
    for p in sorted(LOGS.rglob("*.md")):
        fm = parse_front_matter(p.read_text(encoding="utf-8"))
        try:
            d = date.fromisoformat(str(fm.get("date", p.stem)))
        except ValueError:
            continue
        days[d] = {
            "subjects": fm.get("subjects", []) or [],
            "questions": int(fm.get("questions", 0) or 0),
            "correct": int(fm.get("correct", 0) or 0),
            "path": p.relative_to(ROOT).as_posix(),
        }
    return days


def level(q: int) -> int:
    if q <= 0:
        return 0
    if q <= 4:
        return 1
    if q <= 8:
        return 2
    if q <= 12:
        return 3
    return 4


def streak(days: dict, today: date) -> int:
    d = today if today in days else today - timedelta(days=1)
    n = 0
    while d in days:
        n += 1
        d -= timedelta(days=1)
    return n


def longest_streak(days: dict) -> int:
    best = cur = 0
    prev = None
    for d in sorted(days):
        cur = cur + 1 if prev and d - prev == timedelta(days=1) else 1
        best = max(best, cur)
        prev = d
    return best


def cell_svg(x: int, y: int, size: int, lv: int, tip: str = "") -> str:
    """한 칸을 그려요. 공부량 단계(lv 0~4)에 맞는 색으로 칠해요."""
    title = f"<title>{tip}</title>" if tip else ""
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{COLORS[lv]}">{title}</rect>'


def build_svg(days: dict, today: date) -> str:
    cell, gap = 12, 3
    pad = 10  # 껍질 두께만큼 안쪽 여백
    left, top = 30 + pad, 34 + pad
    # 이번 주 일요일 기준으로 WEEKS 주 전 일요일부터 시작
    end = today
    start = end - timedelta(days=(end.weekday() + 1) % 7) - timedelta(weeks=WEEKS - 1)
    width = left + WEEKS * (cell + gap) + 10 + pad
    height = top + 7 * (cell + gap) + 30 + pad

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="{left}" y="{18 + pad}" font-size="12" font-weight="600" fill="{TITLE}">'
        f'출퇴근 CS 학습 · 최근 {WEEKS}주</text>',
    ]
    for i, lbl in [(1, "월"), (3, "수"), (5, "금")]:
        y = top + i * (cell + gap) + cell - 2
        out.append(f'<text x="{8 + pad}" y="{y}" font-size="9" fill="{TEXT}">{lbl}</text>')

    last_month = None
    for w in range(WEEKS):
        week_start = start + timedelta(weeks=w)
        # 그 달 1일이 들어있는 주에만 월 라벨을 붙여서 겹치지 않게 해요
        first = (week_start + timedelta(days=6)).replace(day=1)
        if week_start <= first <= week_start + timedelta(days=6) and first.month != last_month:
            x = left + w * (cell + gap)
            out.append(f'<text x="{x}" y="{top - 6}" font-size="9" fill="{TEXT}">{first.month}월</text>')
            last_month = first.month
        for dow in range(7):
            d = week_start + timedelta(days=dow)
            if d > end:
                continue
            info = days.get(d)
            q = info["questions"] if info else 0
            x = left + w * (cell + gap)
            y = top + dow * (cell + gap)
            tip = f"{d.isoformat()} · {q}문제" + (f" · {', '.join(info['subjects'])}" if info else "")
            out.append(cell_svg(x, y, cell, level(q), tip))

    ly = height - 14 - pad
    lx = width - 10 - pad - 5 * (cell + gap) - 30
    out.append(f'<text x="{lx - 4}" y="{ly + 10}" font-size="9" fill="{TEXT}" text-anchor="end">적음</text>')
    for i in range(len(COLORS)):
        out.append(cell_svg(lx + i * (cell + gap), ly, cell, i))
    out.append(f'<text x="{lx + 5 * (cell + gap) + 2}" y="{ly + 10}" font-size="9" fill="{TEXT}">많음</text>')
    out.append("</svg>")
    return "\n".join(out)


def roadmap_progress() -> dict:
    text = ROADMAP.read_text(encoding="utf-8")
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    result = {}
    for sec in sections:
        title = sec.splitlines()[0]
        for key, needle in ROADMAP_KEYS.items():
            if needle in title and key not in result:
                done = len(re.findall(r"^- \[x\]", sec, re.M | re.I))
                total = len(re.findall(r"^- \[[ xX]\]", sec, re.M))
                result[key] = (done, total)
    return result


def bar(done: int, total: int, width: int = 10) -> str:
    if total == 0:
        return "—"
    filled = round(width * done / total)
    return f"`{'▰' * filled}{'▱' * (width - filled)}` {done}/{total}"


def build_stats(days: dict, today: date) -> str:
    total_q = sum(v["questions"] for v in days.values())
    total_c = sum(v["correct"] for v in days.values())
    rate = f"{total_c / total_q * 100:.0f}%" if total_q else "—"
    return "\n".join([
        "| 연속 학습 | 최장 연속 | 총 학습일 | 푼 문제 | 정답률 |",
        "|:---:|:---:|:---:|:---:|:---:|",
        f"| **{streak(days, today)}일** | {longest_streak(days)}일 | {len(days)}일 | {total_q}개 | {rate} |",
    ])


def build_subjects(days: dict) -> str:
    agg = defaultdict(lambda: {"days": 0, "q": 0, "c": 0, "last": None})
    for d, v in days.items():
        subs = v["subjects"] or []
        for s in subs:
            a = agg[s]
            a["days"] += 1
            # 하루에 여러 과목이면 문제 수를 과목 수로 나눠서 근사
            a["q"] += v["questions"] / len(subs)
            a["c"] += v["correct"] / len(subs)
            a["last"] = max(a["last"], d) if a["last"] else d
    prog = roadmap_progress()
    rows = [
        "| 과목 | 로드맵 진도 | 학습일 | 문제 | 정답률 | 마지막 학습 |",
        "|---|---|:---:|:---:|:---:|:---:|",
    ]
    for key, name in SUBJECTS:
        a = agg.get(key, {"days": 0, "q": 0, "c": 0, "last": None})
        done, total = prog.get(key, (0, 0))
        rate = f"{a['c'] / a['q'] * 100:.0f}%" if a["q"] else "—"
        last = a["last"].isoformat() if a["last"] else "—"
        rows.append(
            f"| [{name}](concepts/{key}/README.md) | {bar(done, total)} | {a['days']} | "
            f"{round(a['q'])} | {rate} | {last} |"
        )
    return "\n".join(rows)


def build_recent(days: dict) -> str:
    if not days:
        return "_아직 기록이 없어요. 첫 출근길을 기다리는 중_"
    lines = []
    for d in sorted(days, reverse=True)[:7]:
        v = days[d]
        subs = ", ".join(v["subjects"]) or "-"
        lines.append(f"- [{d.isoformat()}]({v['path']}) · {subs} · {v['correct']}/{v['questions']}")
    return "\n".join(lines)


def replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main():
    today = datetime.now(KST).date()
    days = load_logs()
    SVG_PATH.parent.mkdir(exist_ok=True)
    SVG_PATH.write_text(build_svg(days, today), encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_block(text, "STATS", build_stats(days, today))
    text = replace_block(text, "SUBJECTS", build_subjects(days))
    text = replace_block(text, "RECENT", build_recent(days))
    text = replace_block(text, "UPDATED", f"<sub>마지막 업데이트: {today.isoformat()}</sub>")
    README.write_text(text, encoding="utf-8")
    print(f"updated: {len(days)} days, streak {streak(days, today)}")


if __name__ == "__main__":
    main()
