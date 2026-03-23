#!/usr/bin/env python3
"""qa_check.py — PDF 품질 자동 검수

빌드 후 자동 실행. 문제 발견 시 exit code 1 반환.
검사 항목:
  1. 희소 페이지 (본문 80자 미만)
  2. 첫 페이지 본문 충실도 (20자 이상 줄 3개 미만)
  3. 빈 페이지 (페이지 번호 외 텍스트 없음)
  4. 참고문헌 헤딩 존재 여부
  5. 필수 폰트 5종 임베딩 여부
  6. 시각화 최소 2개 (tikzpicture/longtable) 존재 여부
  7. 표 셀 줄바꿈 규칙 (좁은 열에서 한국어 어절 중간 끊김 방지)
"""

import subprocess, os, sys, glob, re

PROJ = os.path.dirname(os.path.abspath(__file__))

# === 설정 ===
SPARSE_THRESHOLD = 80      # 일반 페이지 최소 글자 수
LAST_PAGE_THRESHOLD = 40   # 마지막 페이지 최소 글자 수
P1_MIN_BODY_LINES = 3      # 첫 페이지 최소 본문 줄 수 (20자 이상인 줄)
REQUIRED_FONTS = [
    "KoPubWorldBatangMedium",
    "KoPubWorldBatangBold",
    "Brill-Roman",
    "Brill-Bold",
    "Brill-Italic",
]
MIN_VIZ_COUNT = 2          # 세션당 최소 시각화 수
CELL_MBOX_THRESHOLD = 40   # 이 너비(mm) 이하 열에서 한국어 셀은 \mbox 필요


def get_page_count(pdf):
    r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True)
    for line in r.stdout.split('\n'):
        if 'Pages' in line:
            return int(line.split()[-1])
    return 0


def get_page_text(pdf, page):
    r = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), pdf, "-"],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def get_fonts(pdf):
    r = subprocess.run(["pdffonts", pdf], capture_output=True, text=True)
    return r.stdout


def count_viz_tex(tex_path):
    """tex 소스에서 시각화 수 카운트 (tex 존재 시)."""
    try:
        with open(tex_path) as f:
            tex = f.read()
        tikz = tex.count(r'\begin{tikzpicture}')
        table = tex.count(r'\begin{longtable}')
        return tikz + table
    except FileNotFoundError:
        return -1


def count_viz_pdf(pdf_path):
    """PDF 텍스트에서 시각화 수 추정 (tikz 타이틀 + 표 헤더)."""
    import subprocess
    try:
        text = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True, text=True
        ).stdout
        # tikz 도식: \bfseries 타이틀이 렌더링된 텍스트
        # longtable: 헤더 행의 tableheadblue 배경 → 열 제목 패턴
        # 간단한 휴리스틱: tikzpicture 렌더링 결과는 특정 패턴 없음
        # → PDF 페이지 수 기반 최소 추정은 불안정하므로 tex 우선, pdf 보조
        return -1  # PDF만으로는 정확한 카운트 불가
    except Exception:
        return -1


def count_viz(tex_path):
    """시각화 수 카운트. tex 우선, 없으면 tikz/ 디렉터리 확인."""
    # 1. tex 소스에서 직접 카운트
    n = count_viz_tex(tex_path)
    if n >= 0:
        return n
    # 2. tex가 없으면 tikz/ 디렉터리에서 매칭 파일 확인
    import os
    from pathlib import Path
    stem = Path(tex_path).stem
    tikz_dir = os.path.join(os.path.dirname(tex_path), "tikz")
    tikz_file = os.path.join(tikz_dir, f"{stem}.tikz")
    # tikz 파일이 있으면 최소 1개, 본문 인라인은 카운트 불가
    return 1 if os.path.exists(tikz_file) else 0


def check_sparse_pages(pdf, name):
    """희소 페이지 + 빈 페이지 검사"""
    issues = []
    total = get_page_count(pdf)
    for p in range(1, total + 1):
        text = get_page_text(pdf, p)
        lines = text.split('\n')
        body_lines = [l for l in lines
                      if l.strip() and not l.strip().isdigit() and len(l.strip()) > 3]
        char_count = len('\n'.join(body_lines))
        threshold = SPARSE_THRESHOLD if p < total else LAST_PAGE_THRESHOLD
        if char_count < threshold:
            issues.append(f"  희소 페이지: {name} p{p}/{total} ({char_count}자 < {threshold})")
    return issues


def check_first_page(pdf, name):
    """첫 페이지 본문 충실도"""
    text = get_page_text(pdf, 1)
    lines = [l for l in text.split('\n') if l.strip() and len(l.strip()) > 20]
    if len(lines) < P1_MIN_BODY_LINES:
        return [f"  첫 페이지 부실: {name} p1 본문 {len(lines)}줄 (최소 {P1_MIN_BODY_LINES})"]
    return []


def check_references(pdf, name):
    """참고문헌 헤딩 존재 여부"""
    total = get_page_count(pdf)
    for p in range(max(1, total - 2), total + 1):
        text = get_page_text(pdf, p)
        if '참고문헌' in text:
            return []
    return [f"  참고문헌 미발견: {name}"]


def check_fonts(pdf, name):
    """필수 폰트 5종 임베딩"""
    fonts = get_fonts(pdf)
    missing = [f for f in REQUIRED_FONTS if f not in fonts]
    if missing:
        return [f"  폰트 누락: {name} — {', '.join(missing)}"]
    return []


def check_viz_count(tex_path, name):
    """시각화 최소 개수"""
    count = count_viz(tex_path)
    if count < MIN_VIZ_COUNT:
        return [f"  시각화 부족: {name} ({count}개 < {MIN_VIZ_COUNT})"]
    return []


def _has_korean(s):
    """문자열에 한국어가 포함되어 있는지"""
    return bool(re.search(r'[\uAC00-\uD7AF]', s))


def _strip_latex_commands(s):
    """\\mbox{...}, \\textbf{...}, \\gr{...} 등 LaTeX 명령을 제거하고 순수 텍스트만 반환"""
    # \mbox{...} 내부는 보호됨 → 제거
    s = re.sub(r'\\mbox\{[^}]*\}', '', s)
    # \newline도 의도적 줄바꿈 → 제거
    s = re.sub(r'\\newline', '', s)
    # 기타 LaTeX 명령 제거
    s = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    # 남은 중괄호 제거
    s = s.replace('{', '').replace('}', '')
    return s.strip()


def check_cell_linebreak(tex_path, name):
    """좁은 열(≤40mm)에서 한국어 셀 내용이 \\mbox로 보호되지 않은 경우 경고.

    규칙: 좁은 열의 한국어 텍스트는 어절 중간에서 끊기지 않도록
    \\mbox{} 또는 \\newline으로 줄바꿈 위치를 명시해야 한다.
    """
    with open(tex_path) as f:
        tex = f.read()

    issues = []

    # longtable 블록 찾기: \begin{longtable} 줄에서 열 너비 추출
    table_starts = [m.start() for m in re.finditer(r'\\begin\{longtable\}', tex)]

    for start in table_starts:
        # \begin{longtable} 줄 전체에서 열 너비 추출
        line_end = tex.find('\n', start)
        header_line = tex[start:line_end]
        col_widths = [int(w) for w in re.findall(r'm\{(\d+)mm\}', header_line)]

        if not col_widths:
            continue

        narrow_cols = {i for i, w in enumerate(col_widths) if w <= CELL_MBOX_THRESHOLD}
        if not narrow_cols:
            continue

        # 테이블 본문 추출
        end_pos = tex.find(r'\end{longtable}', start)
        if end_pos < 0:
            continue
        table_body = tex[start:end_pos]

        endhead_pos = table_body.find(r'\endhead')
        if endhead_pos < 0:
            continue
        data_section = table_body[endhead_pos + len(r'\endhead'):]

        # 데이터 행 분리
        rows = re.split(r'\\\\.*?\\hline', data_section)

        for row_idx, row in enumerate(rows):
            row = row.strip()
            if not row:
                continue
            cells = row.split('&')
            for col_idx, cell in enumerate(cells):
                if col_idx not in narrow_cols:
                    continue
                cell = cell.strip()
                remaining = _strip_latex_commands(cell)
                # 한국어 글자가 3자 이상 연속으로 \mbox 없이 남아있으면 경고
                korean_chars = re.findall(r'[\uAC00-\uD7AF]', remaining)
                if len(korean_chars) >= 3:
                    sample = remaining[:25].strip()
                    issues.append(
                        f"  표 셀 줄바꿈 위험: {name} "
                        f"행{row_idx+1} 열{col_idx+1}({col_widths[col_idx]}mm) "
                        f"— \\mbox 없는 한국어: '{sample}'"
                    )

    return issues


def main():
    pdfs = sorted(glob.glob(os.path.join(PROJ, "[0-1]*.pdf")))
    if not pdfs:
        print("⚠️  PDF 파일 없음")
        sys.exit(1)

    all_issues = []
    print(f"{'='*60}")
    print(f"  PDF 품질 검수 — {len(pdfs)}개 파일")
    print(f"{'='*60}")

    for pdf in pdfs:
        name = os.path.basename(pdf).replace('.pdf', '')
        tex = pdf.replace('.pdf', '.tex')

        issues = []
        issues += check_sparse_pages(pdf, name)
        issues += check_first_page(pdf, name)
        issues += check_references(pdf, name)
        issues += check_fonts(pdf, name)
        if os.path.exists(tex):
            issues += check_viz_count(tex, name)
            issues += check_cell_linebreak(tex, name)

        if issues:
            print(f"\n⚠️  {name}:")
            for i in issues:
                print(i)
            all_issues += issues
        else:
            pages = get_page_count(pdf)
            viz = count_viz(tex) if os.path.exists(tex) else "?"
            print(f"  ✅ {name} ({pages}p, viz={viz})")

    print(f"\n{'='*60}")
    if all_issues:
        print(f"  ❌ {len(all_issues)}건 문제 발견 — 수정 필요")
        print(f"{'='*60}")
        sys.exit(1)
    else:
        print(f"  ✅ 전 파일 통과")
        print(f"{'='*60}")
        sys.exit(0)


if __name__ == "__main__":
    main()
