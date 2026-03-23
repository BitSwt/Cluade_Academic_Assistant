#!/usr/bin/env python3
"""trans_md_to_tex.py — 번역본 마크다운 → .tex 변환 (translation_style_guide v1_3 준수)

사용법:
  python3 trans_md_to_tex.py input.md output.tex
  python3 trans_md_to_tex.py input.md              # → input.tex
"""
import re
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
try:
    from tex_common import SUP_MAP, SUP_RE, sup_to_key, escape_tex as _escape_tex, md_inline as _md_inline
except ImportError:
    pass  # standalone — 내장 함수 사용

SUP_MAP = {'¹':'1','²':'2','³':'3','⁴':'4','⁵':'5',
           '⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁰':'0','ᵃ':'a'}
SUP_RE  = re.compile('[¹²³⁴⁵⁶⁷⁸⁹⁰ᵃ]+')

def sup_key(raw):
    return ''.join(SUP_MAP.get(c, c) for c in raw)

def escape_tex(s):
    s = s.replace('\\', '\x00BSL\x00')
    s = s.replace('{',  '\x00LBR\x00')
    s = s.replace('}',  '\x00RBR\x00')
    s = s.replace('&',  '\\&')
    s = s.replace('%',  '\\%')
    s = s.replace('$',  '\\$')
    s = s.replace('#',  '\\#')
    s = s.replace('_',  '\\_')
    s = s.replace('~',  '\\textasciitilde{}')
    s = s.replace('^',  '\\textasciicircum{}')
    s = s.replace('\x00BSL\x00', '\\textbackslash{}')
    s = s.replace('\x00LBR\x00', '\\{')
    s = s.replace('\x00RBR\x00', '\\}')
    return s

def md_inline(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'\*(.+?)\*',     r'\\textit{\1}',  s)
    return s

def proc(s):
    return md_inline(escape_tex(s))

def parse(path):
    with open(path, encoding='utf-8') as f:
        raw = f.readlines()
    blocks = []
    i = 0
    skip = False
    SEC_H  = re.compile(r'^## (.+)$')
    PARA_H = re.compile(r'^\[([I\d\.]+)\] (.+)$')
    FN_S   = re.compile(r'^> ([¹²³⁴⁵⁶⁷⁸⁹⁰ᵃ]+) (.+)$')
    FN_C   = re.compile(r'^> (.+)$')

    while i < len(raw):
        line = raw[i].rstrip('\n')

        if line.strip() in ('', '---') or line.startswith('# '):
            i += 1; continue

        m = SEC_H.match(line)
        if m:
            t = m.group(1).strip()
            skip = (t == '확인 완료')
            if not skip:
                blocks.append(('section', t))
            i += 1; continue

        if skip:
            i += 1; continue

        m = PARA_H.match(line)
        if m:
            sec = m.group(1)
            body_lines = [m.group(2)]
            i += 1

            # 본문 이어지는 줄 수집 (빈 줄 또는 > 또는 새 절까지)
            while i < len(raw):
                nl = raw[i].rstrip('\n')
                if nl.strip() == '' or nl.startswith('[') or \
                   nl.startswith('#') or nl.startswith('>'):
                    break
                body_lines.append(nl)
                i += 1

            # 빈 줄 건너뜀 (본문과 각주 블록 사이)
            while i < len(raw) and raw[i].strip() == '':
                i += 1

            # 각주 블록 수집
            fns = {}
            cur = None
            while i < len(raw):
                nl = raw[i].rstrip('\n')
                fm = FN_S.match(nl)
                fc = FN_C.match(nl)

                if fm:
                    k = sup_key(fm.group(1))
                    fns[k] = [fm.group(2)]
                    cur = k
                    i += 1
                elif cur and fc:
                    fns[cur].append(fc.group(1))
                    i += 1
                elif nl.strip() == '' and cur:
                    # 각주들 사이 빈 줄 건너뜀
                    i += 1
                else:
                    break

            blocks.append(('para', {'sec': sec, 'body': body_lines, 'fns': fns}))
            continue

        i += 1

    return blocks


def render_para(d, needspace=False):
    sec, body, fns = d['sec'], ' '.join(d['body']), d['fns']
    parts = SUP_RE.split(body)
    sups  = SUP_RE.findall(body)
    out   = proc(parts[0])
    for sup, part in zip(sups, parts[1:]):
        k = sup_key(sup)
        if k in fns:
            fn_tex = proc(' '.join(fns[k]))
            out += f'\\footnote{{{fn_tex}}}'
        else:
            out += f'\\textsuperscript{{{escape_tex(sup)}}}'
        out += proc(part)
    prefix = '\\newpage\n' if sec == 'I.14.4' else ''
    prefix += '\\needspace{8\\baselineskip}\n' if needspace else ''
    return f'{prefix}\\margref{{{sec}}}\\noindent {out}\n\n'


def convert(src, dst):
    blocks = parse(src)

    PREAMBLE = (
        '% !TEX program = lualatex\n'
        r'\documentclass[12pt,a4paper]{article}' '\n'
        r'\usepackage{master}' '\n'
        r'\usepackage{translation}' '\n'
        r'\renewcommand*{\marginfont}{\footnotesize\color{h2burgundy}\fontspec[Path=/usr/local/share/fonts/]{Brill-Roman.ttf}}' '\n'
        '\n'
        r'\fancyhead[L]{\footnotesize\color{midgray}\shortstack[l]{'
        r'Θεόφραστος\\Περὶ φυτῶν ἱστορία}}' '\n'
        r'\fancyhead[R]{\footnotesize\color{midgray}\shortstack[r]{'
        r'\gri{Theophrastus}\\\gri{Historia Plantarum}}}' '\n'
        '\n'
        r'\begin{document}' '\n\n'
        r'\thispagestyle{firstpage}' '\n\n'
        # 표제 블록: 좌 원어 / 중앙 분량 / 우 라틴어
        r'{\par\medskip' '\n'
        r'\begingroup' '\n'
        r'\setstretch{1.0}%' '\n'
        r'\fontsize{14pt}{16pt}\selectfont\bfseries\color{h1navy}%' '\n'
        r'\noindent' '\n'
        r'\begin{minipage}[t]{0.48\linewidth}' '\n'
        r'\raggedright' '\n'
        r'Θεόφραστος\\' '\n'
        r'Περὶ φυτῶν ἱστορία, Βιβλίον Α' '\n'
        r'\end{minipage}%' '\n'
        r'\hfill' '\n'
        r'\begin{minipage}[t]{0.48\linewidth}' '\n'
        r'\raggedleft' '\n'
        r'\gri{Theophrastus}\\' '\n'
        r'\gri{Historia Plantarum, Liber I}' '\n'
        r'\end{minipage}%' '\n'
        r'\par\endgroup' '\n'
        r'\vspace{4pt}%' '\n'
        r'{\color{rulecolor}\hrule height 0.4pt}%' '\n'
        r'\vspace{8pt}%' '\n'
        r'}' '\n\n'
    )

    out = [PREAMBLE]
    para_blocks = [(i, b) for i, (t, b) in enumerate(blocks) if t == 'para']
    last_para_idx = para_blocks[-1][0] if para_blocks else -1
    for idx, (btype, bdata) in enumerate(blocks):
        if btype == 'section':
            out.append(f'\n\\section*{{{bdata}}}\n\n')
        else:
            is_last = (idx == last_para_idx)
            out.append(render_para(bdata, needspace=is_last))
    out.append('\n\\end{document}\n')

    with open(dst, 'w', encoding='utf-8') as f:
        f.writelines(out)

    n_para = sum(1 for b in blocks if b[0] == 'para')
    n_fn   = sum(len(b['fns']) for _, b in blocks if _ == 'para')
    print(f'완료: {dst}')
    print(f'  절: {n_para}개, 각주: {n_fn}개')


def main():
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print("사용법: python3 trans_md_to_tex.py input.md [output.tex]")
        sys.exit(1)
    src = args[0]
    dst = args[1] if len(args) > 1 else src.replace('.md', '.tex')
    convert(src, dst)


if __name__ == '__main__':
    main()
