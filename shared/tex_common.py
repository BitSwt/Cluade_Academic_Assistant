#!/usr/bin/env python3
"""tex_common.py — md2tex / trans_md_to_tex 공통 유틸리티

강의록(md2tex.py)과 번역본(trans_md_to_tex.py) 변환기가 공유하는
텍스트 처리 함수를 모아둔다.
"""
import re

# ── 유니코드 상첨자 매핑 ──
SUP_MAP = {
    '¹':'1', '²':'2', '³':'3', '⁴':'4', '⁵':'5',
    '⁶':'6', '⁷':'7', '⁸':'8', '⁹':'9', '⁰':'0', 'ᵃ':'a',
}
SUP_RE = re.compile('[¹²³⁴⁵⁶⁷⁸⁹⁰ᵃ]+')

# ── 그리스어 정규식 ──
GREEK_RE = re.compile(
    r'([\u0370-\u03FF\u1F00-\u1FFF]+'
    r'(?:[\s\u0370-\u03FF\u1F00-\u1FFF]*'
    r'[\u0370-\u03FF\u1F00-\u1FFF])*)'
)


def sup_to_key(raw):
    """유니코드 상첨자 문자열을 ASCII 키로 변환. '¹²' → '12'"""
    return ''.join(SUP_MAP.get(c, c) for c in raw)


def escape_tex(s):
    """LaTeX 특수 문자 이스케이프. & # % $ _ ~ ^ 처리."""
    s = s.replace('\\', '\\textbackslash{}')
    s = s.replace('&', '\\&')
    s = s.replace('#', '\\#')
    s = s.replace('%', '\\%')
    s = s.replace('$', '\\$')
    s = s.replace('_', '\\_')
    s = re.sub(r'(?<!\\)~', r'\\textasciitilde{}', s)
    return s


def md_inline(s):
    """마크다운 인라인 서식 → LaTeX. **볼드** → \\textbf, *이탤릭* → \\gri"""
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\gri{\1}', s)
    return s


def wrap_greek(s):
    """그리스어 유니코드 → \\gr{...} 래핑."""
    return GREEK_RE.sub(lambda m: f'\\gr{{{m.group(1)}}}', s)


def process_text(s):
    """escape → inline → greek 순서로 전체 처리."""
    return wrap_greek(md_inline(escape_tex(s)))
