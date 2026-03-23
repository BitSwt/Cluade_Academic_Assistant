#!/usr/bin/env python3
r"""compliance_check.py — 집필 지침 준수 자동 검수

style_guide_v4_0, lecture_style_guide_v1_0, Basic_rules.md 기반.
.tex 파일을 대상으로 규칙 위반 여부를 검사한다.
qa_check.py(PDF 품질)와 별개로, 이 스크립트는 소스(.tex) 수준 규칙을 검사한다.

검사 항목:
  1. 프리앰블 구조 (master.sty 로드, 중복 패키지 금지)
  2. tikz 선언 (tikzpicture 사용 시 프리앰블에 tikz 로드 필수)
  3. \weeksection 사용 여부 (강의록 필수)
  4. \bilingualquote 내 \footnote 금지 (\bqnote 사용 필수)
  5. \citework 뒤 조사 패턴 (공백 소실 위험)
  6. LuaTeX-ja 줄바꿈 위험 패턴
  7. 참고문헌 구조 (\subsubsection*{참고문헌} + references 환경)
  8. 참고문헌이 문서 맨 마지막인지
  9. needspace 누락 (longtable/tabulary 앞)
 10. 언어 규칙: 한국어·영어 번역본 언급 금지
 11. 메타 마커 잔류 ([확인 필요] 등)
 12. master.sty 중복 패키지 선언 금지
"""

import os
import re
import sys
import glob
from pathlib import Path

PROJ = Path(os.path.dirname(os.path.abspath(__file__)))

# master.sty가 이미 로드하는 패키지 — 중복 선언 금지
MASTER_PACKAGES = {
    "luatexja-fontspec", "etoolbox", "geometry", "setspace",
    "booktabs", "array", "multirow", "colortbl", "xcolor",
    "fancyhdr", "microtype", "titlesec", "hyperref", "graphicx",
    "wrapfig", "needspace", "caption", "footmisc", "longtable", "tabulary",
}


def check_preamble(tex, name):
    """프리앰블 구조 검사"""
    issues = []
    preamble = tex.split(r'\begin{document}')[0] if r'\begin{document}' in tex else tex[:500]

    # master.sty 로드 확인
    if r'\usepackage{master}' not in preamble and r'\usepackage[' not in preamble:
        issues.append(f"  프리앰블: {name} — \\usepackage{{master}} 누락")

    # 중복 패키지 선언
    loaded = re.findall(r'\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}', preamble)
    for pkg in loaded:
        for p in pkg.split(','):
            p = p.strip()
            if p in MASTER_PACKAGES:
                issues.append(f"  중복 패키지: {name} — \\usepackage{{{p}}} (master.sty가 이미 로드)")

    return issues


def check_tikz_declaration(tex, name):
    """tikzpicture 사용 시 프리앰블에 tikz 로드 필수"""
    issues = []
    if r'\begin{tikzpicture}' in tex:
        preamble = tex.split(r'\begin{document}')[0] if r'\begin{document}' in tex else ""
        if r'\usepackage{tikz}' not in preamble:
            issues.append(f"  tikz 미선언: {name} — tikzpicture 사용하지만 프리앰블에 \\usepackage{{tikz}} 없음")
    return issues


def check_weeksection(tex, name):
    """강의록 파일에 \\weeksection 사용 여부"""
    issues = []
    # [0-1]로 시작하는 강의록 파일만 검사
    if re.match(r'[0-1]', os.path.basename(name)):
        if r'\weeksection' not in tex:
            issues.append(f"  weeksection 누락: {name} — 강의록에 \\weeksection 없음")
    return issues


def check_bqnote(tex, name):
    """\\bilingualquote 내 \\footnote 사용 금지 (\\bqnote 사용 필수)"""
    issues = []
    # bilingualquote 블록 내에서 \footnote 찾기
    in_bq = False
    for i, line in enumerate(tex.split('\n'), 1):
        if r'\bilingualquote' in line:
            in_bq = True
        if in_bq and r'\footnote{' in line:
            issues.append(f"  bqnote 위반: {name} L{i} — bilingualquote 내 \\footnote 사용 (\\bqnote 필수)")
        if in_bq and ('}' in line and line.strip().endswith('}')):
            # 단순 휴리스틱: 닫는 중괄호로 블록 종료 추정
            pass
    return issues


def check_citework_particle(tex, name):
    """\\citework 뒤 조사 패턴 (공백 소실 위험)"""
    issues = []
    pattern = re.compile(r'\\citework\{[^}]+\}\{[^}]*\}(은|는|이|가|을|를|의|에|와|과|로|으로|도|만|까지)')
    for i, line in enumerate(tex.split('\n'), 1):
        m = pattern.search(line)
        if m:
            issues.append(f"  citework 조사: {name} L{i} — \\citework 뒤 조사 '{m.group(1)}' 직접 연결 (공백 소실 위험)")
    return issues


def check_luatexja_linebreak(tex, name):
    """LuaTeX-ja 줄바꿈 위험 패턴 (표·정렬 환경 내부는 제외)"""
    issues = []
    lines = tex.split('\n')
    in_table = False
    for i in range(len(lines) - 1):
        line = lines[i]
        # 표/정렬 환경 내부 추적
        if re.search(r'\\begin\{(longtable|concepttable|tabular|tabulary|tikzpicture)', line):
            in_table = True
        if re.search(r'\\end\{(longtable|concepttable|tabular|tabulary|tikzpicture)', line):
            in_table = False
        if in_table:
            continue
        curr = line.rstrip()
        nxt = lines[i + 1].lstrip()
        if not curr or not nxt:
            continue
        # 들여쓰기된 정렬 텍스트 제외 (텍스트 기반 표)
        if line.startswith('    ') and lines[i + 1].startswith('    '):
            continue
        # 텍스트 기반 표 (3+ 연속 공백으로 열 구분)
        if '   ' in curr and '   ' in nxt:
            continue
        # 다음 줄이 LaTeX 명령으로 시작하면 독립 항목
        if nxt.startswith('\\'):
            continue
        # 패턴 1: 한국어 끝 → 다음 줄 \textbf, \citework, \gr, \gri
        if re.search(r'[\uAC00-\uD7AF]$', curr):
            if re.match(r'\\(textbf|citework|gr[ib]?)\{', nxt):
                issues.append(f"  줄바꿈 위험: {name} L{i+1} — 한국어 뒤 줄바꿈 후 \\{nxt.split('{')[0][1:]} (공백 소실)")
        # 패턴 2: 라틴문자/닫는괄호 끝 → 다음 줄 한국어
        if re.search(r'[a-zA-Z\)}\]]$', curr):
            if re.match(r'[\uAC00-\uD7AF]', nxt):
                issues.append(f"  줄바꿈 위험: {name} L{i+2} — 라틴문자 뒤 줄바꿈 후 한국어 (공백 소실)")
    return issues



def check_references_structure(tex, name):
    """참고문헌 구조: \\subsubsection*{참고문헌} + references 환경"""
    issues = []
    if r'\begin{references}' in tex:
        if r'\subsubsection*{참고문헌}' not in tex:
            issues.append(f"  참고문헌 헤딩: {name} — references 환경은 있지만 \\subsubsection*{{참고문헌}} 없음")
        # 헤딩이 references 환경 밖에 있어야 함
        heading_pos = tex.find(r'\subsubsection*{참고문헌}')
        env_pos = tex.find(r'\begin{references}')
        if heading_pos > 0 and env_pos > 0 and heading_pos > env_pos:
            issues.append(f"  참고문헌 순서: {name} — 헤딩이 references 환경 안에 있음 (밖에 있어야 함)")
    return issues


def check_references_last(tex, name):
    """참고문헌이 문서 맨 마지막인지"""
    issues = []
    end_ref = tex.rfind(r'\end{references}')
    end_doc = tex.rfind(r'\end{document}')
    if end_ref > 0 and end_doc > 0:
        between = tex[end_ref:end_doc].strip()
        # references 이후 end{document} 전에 본문 내용이 있으면 안 됨
        between = between.replace(r'\end{references}', '').strip()
        # 빈 줄, 주석만 허용
        content_lines = [l for l in between.split('\n')
                        if l.strip() and not l.strip().startswith('%')]
        if content_lines:
            issues.append(f"  참고문헌 위치: {name} — 참고문헌 뒤에 본문 내용 있음 ({len(content_lines)}줄)")
    return issues


def check_needspace(tex, name):
    """longtable/tabulary 앞 needspace 누락"""
    issues = []
    lines = tex.split('\n')
    for i, line in enumerate(lines):
        if r'\begin{longtable}' in line or r'\begin{concepttable}' in line:
            # 앞 10줄 내에 \needspace가 있는지
            context = '\n'.join(lines[max(0, i-10):i])
            if r'\needspace' not in context:
                # weeksection 직후이거나 subsection 직후인 경우도 허용
                if r'\weeksection' not in context and r'\subsection' not in context:
                    issues.append(f"  needspace 누락: {name} L{i+1} — 표 앞에 \\needspace 없음")
    return issues


def check_language_rule(tex, name):
    """한국어·영어 번역본 언급 금지"""
    issues = []
    # 본문 부분만 (프리앰블/주석 제외)
    body = tex.split(r'\begin{document}')[1] if r'\begin{document}' in tex else tex
    for i, line in enumerate(body.split('\n'), 1):
        if line.strip().startswith('%'):
            continue
        # 출판된 번역본 언급 금지 (서지정보·교수법 언급은 제외)
        if re.search(r'(영역본|국역본|영문 번역)', line):
            # 각주 안의 서지정보는 제외
            if line.strip().startswith('\\footnote') or '\\gri{' in line:
                continue
            issues.append(f"  언어 규칙: {name} L{i} — 번역본 언급 금지: '{line.strip()[:40]}'")
    return issues


def check_meta_markers(tex, name):
    """메타 마커 잔류"""
    issues = []
    markers = [
        r'\[확인 필요\]',
        r'\[행 번호 확인 필요\]',
        r'\[p\. 확인 필요\]',
        r'\[서지 정보 확인 필요\]',
        r'\[시각화 후보\]',
        r'\[서지 확인 사항\]',
    ]
    for i, line in enumerate(tex.split('\n'), 1):
        for marker in markers:
            if re.search(marker, line):
                issues.append(f"  메타 마커: {name} L{i} — {line.strip()[:50]}")
    return issues


def check_next_time_preview(tex, name):
    """다음 시간 예고 금지"""
    issues = []
    body = tex.split(r'\begin{document}')[1] if r'\begin{document}' in tex else tex
    for i, line in enumerate(body.split('\n'), 1):
        if line.strip().startswith('%'):
            continue
        if re.search(r'다음 시간|다음 주에|다음 세션|이어서 다루|다음에 이어', line):
            issues.append(f"  다음 시간 예고: {name} L{i} — '{line.strip()[:40]}'")
    return issues


def check_edition_discussion(tex, name):
    """판본 논의 금지 (참고문헌 제외)"""
    issues = []
    body = tex.split(r'\begin{document}')[1] if r'\begin{document}' in tex else tex
    # 참고문헌 이전 부분만
    ref_pos = body.find(r'\subsubsection*{참고문헌}')
    if ref_pos > 0:
        body = body[:ref_pos]
    for i, line in enumerate(body.split('\n'), 1):
        if line.strip().startswith('%'):
            continue
        if re.search(r'판본|교정본|사본|필사본|텍스트 전승|textual criticism|manuscript', line):
            # 수용사 맥락(특별 세션)은 허용
            if 'special' in name:
                continue
            issues.append(f"  판본 논의: {name} L{i} — '{line.strip()[:40]}'")
    return issues


def check_unresolved_markers(tex, name):
    """PDF에 남으면 안 되는 미해소 마커 및 '확인이 필요한 항목' 헤딩"""
    issues = []
    for i, line in enumerate(tex.split('\n'), 1):
        if line.strip().startswith('%'):
            continue
        # 헤딩으로 된 "확인이 필요한 항목"
        if re.search(r'\\(sub)*section\*?\{확인이 필요한 항목\}', line):
            issues.append(f"  미해소 헤딩: {name} L{i} — '확인이 필요한 항목' 헤딩이 PDF에 포함됨")
        # 미해소 마커 (메타 마커와 별도로 심각도 높은 검사)
        if '[확인 필요]' in line or '[p. 확인 필요]' in line or '[서지 정보 확인 필요]' in line or '[행 번호 확인 필요]' in line:
            if not line.strip().startswith('%'):
                issues.append(f"  미해소 마커: {name} L{i} — {line.strip()[:50]}")
    return issues


def check_footnote_in_table(tex, name):
    """표 안에서 \\footnote 사용 (longtable 내 \\footnote는 사라짐)"""
    issues = []
    in_table = False
    for i, line in enumerate(tex.split('\n'), 1):
        if r'\begin{longtable}' in line or r'\begin{concepttable}' in line:
            in_table = True
        if in_table and r'\footnote{' in line:
            issues.append(f"  표 내 각주: {name} L{i} — 표 안에서 \\footnote 사용 (사라질 수 있음)")
        if r'\end{longtable}' in line or r'\end{concepttable}' in line:
            in_table = False
    return issues


def main():
    tex_files = sorted(glob.glob(str(PROJ / "[0-1]*.tex")))
    if not tex_files:
        print("  ⚠️  [0-1]*.tex 파일 없음")
        sys.exit(1)

    all_issues = []
    print(f"{'='*60}")
    print(f"  집필 지침 준수 검수 — {len(tex_files)}개 파일")
    print(f"{'='*60}")

    for tex_file in tex_files:
        name = os.path.basename(tex_file)
        with open(tex_file) as f:
            tex = f.read()

        issues = []
        issues += check_preamble(tex, name)
        issues += check_tikz_declaration(tex, name)
        issues += check_weeksection(tex, name)
        issues += check_bqnote(tex, name)
        issues += check_citework_particle(tex, name)
        issues += check_luatexja_linebreak(tex, name)
        issues += check_references_structure(tex, name)
        issues += check_references_last(tex, name)
        issues += check_needspace(tex, name)
        issues += check_language_rule(tex, name)
        issues += check_meta_markers(tex, name)
        issues += check_footnote_in_table(tex, name)
        issues += check_next_time_preview(tex, name)
        issues += check_edition_discussion(tex, name)
        issues += check_unresolved_markers(tex, name)

        if issues:
            print(f"\n⚠️  {name}:")
            for issue in issues:
                print(issue)
            all_issues += issues
        else:
            print(f"  ✅ {name}")

    print(f"\n{'='*60}")
    if all_issues:
        print(f"  ⚠️  {len(all_issues)}건 경고 (수정 권장)")
        print(f"{'='*60}")
        # 경고는 exit 0 (빌드 중단하지 않음), 심각한 위반만 exit 1
        serious = [i for i in all_issues if "중복 패키지" in i or "tikz 미선언" in i or "bqnote 위반" in i]
        if serious:
            print(f"  ❌ 심각한 위반 {len(serious)}건 — 수정 필수")
            sys.exit(1)
        sys.exit(0)
    else:
        print(f"  ✅ 전 파일 통과")
        print(f"{'='*60}")
        sys.exit(0)


if __name__ == "__main__":
    main()
