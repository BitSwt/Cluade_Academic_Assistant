"""md2tex.py — 마크다운 강의록 → .tex 자동 변환 (master.sty 기반)

.md 파일의 첫 줄 헤딩에서 주차·분량·제목을 자동 추출한다.

사용법:
  python3 md2tex.py                           # lecture_drafts/ 전체
  python3 md2tex.py input.md                  # 단일 파일
  python3 md2tex.py --src-dir ./drafts --out-dir ./project
  python3 md2tex.py input.md --force          # 기존 .tex 덮어쓰기
"""
import re, sys, os
from pathlib import Path
try:
    from tex_common import GREEK_RE, md_inline, wrap_greek, escape_tex, SUP_RE
except ImportError:
    pass  # standalone 사용 시 내장 함수 사용

try:
    from tex_common import wrap_greek, md_inline, collect_footnotes, insert_footnotes
except ImportError:
    # tex_common이 없으면 인라인 정의 (호환성)
    GREEK_PAT = re.compile(r'([\u0370-\u03FF\u1F00-\u1FFF]+(?:[\s\u0370-\u03FF\u1F00-\u1FFF]*[\u0370-\u03FF\u1F00-\u1FFF])*)')
    def wrap_greek(t): return GREEK_PAT.sub(lambda m: f'\\gr{{{m.group(1)}}}', t)
    def md_inline(s):
        s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
        s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\gri{\1}', s)
        return s
    def collect_footnotes(md):
        fn = {}
        for m in re.finditer(r'^> ([¹²³⁴⁵⁶⁷⁸⁹⁰]+) (.+?)(?=\n\n|\n>|\Z)', md, re.MULTILINE|re.DOTALL):
            fn[m.group(1)] = m.group(2).strip().replace('\n',' ')
        cleaned = re.sub(r'\n> [¹²³⁴⁵⁶⁷⁸⁹⁰]+ .+?(?=\n\n|\Z)', '', md, flags=re.DOTALL)
        return cleaned, fn
    def insert_footnotes(md, fn):
        for sup, text in fn.items():
            text = md_inline(text); text = wrap_greek(text)
            md = md.replace(sup, f'\\footnote{{{text}}}', 1)
        return md


def parse_heading(md):
    """첫 줄 # 헤딩에서 (주차, 분량, 제목) 추출."""
    first = md.strip().split('\n')[0].strip()
    if not first.startswith('# '):
        return None, None, None
    h = first[2:].strip()
    m = re.match(r'^(.+?)\s*[—–-]\s*(.+?):\s*(.+)$', h)
    if m: return m.group(1).strip(), m.group(2).strip().replace('–','--'), m.group(3).strip()
    m = re.match(r'^(.+?)\s*[—–-]\s*(.+)$', h)
    if m: return m.group(1).strip(), "", m.group(2).strip()
    return h, "", ""


def convert(md_path, out_path=None):
    with open(md_path) as f:
        md = f.read()
    week, portion, title = parse_heading(md)
    if not week:
        print(f"  ⚠ 헤딩 추출 실패: {md_path}"); return None

    md, footnotes = collect_footnotes(md)

    # srcquote
    def conv_src(m):
        return f'\\srcquote{{{m.group(2).strip()}}}{{{m.group(3).strip()}}}{{{m.group(1).strip()}}}'
    md = re.sub(r'\[srcquote: (.+?)\]\n\n> (.+?)\n\n(.+?)(?=\n\n|\Z)', conv_src, md, flags=re.DOTALL)

    # '확인이 필요한 항목' 섹션 제거 (PDF에 남으면 안 됨)
    md = re.sub(r'^###?\s*확인이 필요한 항목.*?(?=^##|\Z)', '', md, flags=re.MULTILINE | re.DOTALL)

    md = re.sub(r'^# .+\n', '', md, flags=re.MULTILINE)
    md = re.sub(r'^## \d+\. (.+)', r'\\subsection{\1}', md, flags=re.MULTILINE)
    md = re.sub(r'^### \d+\.\d+\. (.+)', r'\\subsubsection{\1}', md, flags=re.MULTILINE)
    md = re.sub(r'^### (.+)', r'\\subsubsection{\1}', md, flags=re.MULTILINE)

    md = md_inline(md)
    md = wrap_greek(md)
    md = insert_footnotes(md, footnotes)

    # 태그 정리
    for pat in [r'\[srcquote: .+?\]', r'\[bilingualquote: .+?\]', r'\[시각화.*?\]',
                r'\*\*\[서지 확인 사항\]\*\*.*', r'\*\*\[시각화 후보 정리\]\*\*.*']:
        md = re.sub(pat, '', md, flags=re.DOTALL)

    md = md.replace('&','\\&').replace('#','\\#').replace('%','\\%')
    md = re.sub(r'(?<!\\)~', r'\\textasciitilde{}', md)

    # 참고문헌
    ref_match = re.search(r'\\subsubsection\{참고문헌\}\s*\n(.*)', md, re.DOTALL)
    if ref_match:
        before = md[:ref_match.start()]
        blocks = [b.strip() for b in ref_match.group(1).strip().split('\n\n')
                  if b.strip() and not b.strip().startswith('---')]
        items = '\n'.join(f'\\refitem {b.replace(chr(10)," ")}' for b in blocks)
        md = before + f'\\subsubsection*{{참고문헌}}\n\\begin{{references}}\n{items}\n\\end{{references}}'

    md = re.sub(r'\n{3,}', '\n\n', md)

    tex = f'''% !TEX program = lualatex
\\documentclass[a4paper, 12pt]{{article}}
\\usepackage{{master}}

\\begin{{document}}

\\weeksection{{{week}}}{{{portion}}}{{{title}}}

{md.strip()}

\\end{{document}}
'''
    if not out_path:
        out_path = str(Path(md_path).with_suffix('.tex'))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    # 안전장치: 기존 .tex에 tikz/longtable이 있으면 덮어쓰지 않음
    if os.path.exists(out_path) and '--force' not in sys.argv:
        with open(out_path) as ef:
            ec = ef.read()
        if '\\begin{tikzpicture}' in ec or '\\begin{longtable}' in ec:
            print(f"  ⚠ {os.path.basename(out_path)}: tikz/표 포함 — 건너뜀 (--force로 강제)")
            return None

    with open(out_path, 'w') as f:
        f.write(tex)
    return out_path


def main():
    args = sys.argv[1:]
    src_dir = out_dir = None
    files = []
    i = 0
    while i < len(args):
        if args[i] == '--src-dir' and i+1 < len(args):
            src_dir = args[i+1]; i += 2
        elif args[i] == '--out-dir' and i+1 < len(args):
            out_dir = args[i+1]; i += 2
        elif args[i] == '--force':
            i += 1  # sys.argv에 남아있으므로 convert에서 확인
        else:
            files.append(args[i]); i += 1

    if files:
        for f in files:
            out = os.path.join(out_dir, Path(f).stem+'.tex') if out_dir else None
            r = convert(f, out)
            if r: print(f"✅ {os.path.basename(r)}")
    else:
        if not src_dir: src_dir = str(Path.cwd())  # 기본값: 현재 디렉터리
        if not out_dir: out_dir = str(Path.cwd())
        if not os.path.isdir(src_dir):
            print(f"  ⚠ 소스 없음: {src_dir}"); return
        for fname in sorted(os.listdir(src_dir)):
            if fname.endswith('.md') and fname[0].isdigit():
                r = convert(os.path.join(src_dir, fname), os.path.join(out_dir, fname.replace('.md','.tex')))
                if r: print(f"✅ {os.path.basename(r)}")

if __name__ == '__main__':
    main()
