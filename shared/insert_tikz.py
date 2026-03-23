#!/usr/bin/env python3
r"""insert_tikz.py — .tex 파일에 .tikz 도식 자동 삽입

마커 기반 삽입:
  .tex 파일에 % [tikz: 파일명] 마커가 있으면 tikz/ 디렉터리에서
  해당 .tikz 파일을 읽어 마커 위치에 삽입한다.

자동 삽입 (마커 없는 경우):
  .tex 파일명과 같은 이름의 .tikz 파일이 tikz/ 디렉터리에 있으면
  \begin{references} 바로 앞에 자동 삽입한다.

tikz 프리앰블:
  tikzpicture가 삽입되면 프리앰블에 \usepackage{tikz}를 자동 추가한다.

사용법:
  python3 insert_tikz.py                    # 현재 디렉터리의 모든 .tex
  python3 insert_tikz.py 03_cat_week01.tex  # 단일 파일
  python3 insert_tikz.py --tikz-dir ./tikz  # tikz 디렉터리 지정
  python3 insert_tikz.py --list             # tikz/ 파일 목록

tikz/ 디렉터리 구조:
  tikz/03_cat_week01.tikz     → 03_cat_week01.tex에 자동 매칭
  tikz/porphyry_tree.tikz     → % [tikz: porphyry_tree] 마커로 삽입

.tikz 파일 형식:
  LaTeX 코드 그대로. \begin{center}...\end{center} 또는
  \begin{tikzpicture}...\end{tikzpicture} 포함.
"""

import os
import re
import sys
import glob
from pathlib import Path


def ensure_tikz_preamble(tex):
    """tikzpicture가 있으면 프리앰블에 tikz 패키지 추가"""
    if r'\begin{tikzpicture}' in tex and r'\usepackage{tikz}' not in tex:
        tex = tex.replace(
            r'\usepackage{master}',
            r'\usepackage{master}' + '\n'
            r'\usepackage{tikz}' + '\n'
            r'\usetikzlibrary{calc, positioning, arrows.meta}'
        )
    return tex


def load_tikz_file(tikz_path):
    """tikz 파일 내용 로드"""
    with open(tikz_path) as f:
        return f.read().strip()


def insert_by_marker(tex, tikz_dir):
    """% [tikz: 파일명] 마커를 찾아 .tikz 파일 내용으로 교체"""
    marker_re = re.compile(r'^%\s*\[tikz:\s*([^\]]+)\]\s*$', re.MULTILINE)
    inserted = []

    def replace_marker(m):
        name = m.group(1).strip()
        # .tikz 확장자 자동 추가
        if not name.endswith('.tikz'):
            name += '.tikz'
        tikz_path = os.path.join(tikz_dir, name)
        if os.path.exists(tikz_path):
            code = load_tikz_file(tikz_path)
            inserted.append(name)
            return code
        else:
            print(f"    ⚠ tikz 파일 없음: {tikz_path}")
            return m.group(0)  # 마커 유지

    tex = marker_re.sub(replace_marker, tex)
    return tex, inserted


def insert_before_references(tex, tikz_code):
    """\\begin{references} 앞에 tikz 코드 삽입"""
    heading = r'\subsubsection*{참고문헌}'
    pos = tex.find(heading)
    if pos > 0:
        return tex[:pos] + tikz_code + '\n\n' + tex[pos:]

    # 참고문헌 헤딩 없으면 \end{document} 앞
    end_doc = tex.rfind(r'\end{document}')
    if end_doc > 0:
        return tex[:end_doc] + tikz_code + '\n\n' + tex[end_doc:]

    return tex


def process_file(tex_path, tikz_dir):
    """단일 .tex 파일 처리"""
    name = os.path.basename(tex_path)
    stem = Path(tex_path).stem

    with open(tex_path) as f:
        tex = f.read()

    original = tex
    actions = []

    # 1. 마커 기반 삽입
    tex, marker_inserts = insert_by_marker(tex, tikz_dir)
    if marker_inserts:
        actions.append(f"마커 삽입: {', '.join(marker_inserts)}")

    # 2. 자동 매칭 (마커가 없고, 같은 이름의 .tikz 파일이 있는 경우)
    auto_tikz = os.path.join(tikz_dir, f"{stem}.tikz")
    if os.path.exists(auto_tikz):
        code = load_tikz_file(auto_tikz)
        # 이미 삽입되어 있는지 확인 (코드 첫 줄로 판단)
        first_line = code.split('\n')[0].strip()
        if first_line and first_line not in tex:
            tex = insert_before_references(tex, code)
            actions.append(f"자동 삽입: {stem}.tikz → 참고문헌 앞")

    # 3. tikz 프리앰블 확인
    tex = ensure_tikz_preamble(tex)

    # 변경 사항이 있으면 저장
    if tex != original:
        with open(tex_path, 'w') as f:
            f.write(tex)
        print(f"  ✅ {name}: {'; '.join(actions)}")
        return True
    else:
        print(f"  · {name}: 변경 없음")
        return False


def cmd_list(tikz_dir):
    """tikz/ 파일 목록"""
    files = sorted(glob.glob(os.path.join(tikz_dir, "*.tikz")))
    if not files:
        print(f"  tikz 파일 없음: {tikz_dir}")
        return
    print(f"  {len(files)}개 .tikz 파일:")
    for f in files:
        name = os.path.basename(f)
        lines = sum(1 for _ in open(f))
        # 제목 추출
        with open(f) as fh:
            content = fh.read()
        title_m = re.search(r'\\bfseries (.+?)\}', content)
        title = title_m.group(1)[:40] if title_m else ""
        print(f"    {name:40s} {lines:3d}줄  {title}")


def main():
    args = sys.argv[1:]

    # 기본 디렉터리
    proj = Path.cwd()
    tikz_dir = str(proj / "tikz")

    # --tikz-dir 옵션
    if "--tikz-dir" in args:
        idx = args.index("--tikz-dir")
        tikz_dir = args[idx + 1]
        args = args[:idx] + args[idx+2:]

    # --list
    if "--list" in args:
        cmd_list(tikz_dir)
        return

    if not os.path.isdir(tikz_dir):
        print(f"  ⚠ tikz 디렉터리 없음: {tikz_dir}")
        print(f"    mkdir -p {tikz_dir} 후 .tikz 파일을 넣으세요.")
        return

    # 대상 파일
    if args:
        tex_files = [str(proj / a) for a in args]
    else:
        tex_files = sorted(glob.glob(str(proj / "[0-1]*.tex")))

    if not tex_files:
        print("  .tex 파일 없음")
        return

    print(f"{'='*50}")
    print(f"  tikz 삽입 — {len(tex_files)}개 파일")
    print(f"  tikz 디렉터리: {tikz_dir}")
    print(f"{'='*50}")

    changed = 0
    for tf in tex_files:
        if os.path.exists(tf):
            if process_file(tf, tikz_dir):
                changed += 1

    print(f"\n  {changed}개 파일 수정됨")


if __name__ == "__main__":
    main()
