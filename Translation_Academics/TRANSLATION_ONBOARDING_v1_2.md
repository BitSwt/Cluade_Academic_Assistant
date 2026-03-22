# 번역본 온보딩 가이드
버전: v1_2

고전 텍스트 한국어 번역본 제작 프레임워크.
master.sty + translation.sty 기반으로 참조 번호 여백 배치를 지원한다.

---

## 버전 이력

**v1_2** (현재): `\bekker` → `\margref` 범용 명칭 변경. `translation.sty v1_3` 반영.

**v1_1**: 이중 각주(manyfoot) 폐지. 단일 `\footnote` 숫자 체계로 통합.

**v1_0**: 초판. Bekker 번호, 이중 각주(`\tfn` + `\cfn`), 표제 블록.

---

## 1단계: 세팅

```bash
bash setup.sh
```

공통 세팅(폰트, luatexja, KoNLPy, master.sty, translation.sty, build.py) + 공통·강의록·번역본 규칙 문서 전체가 프로젝트 디렉터리에 배치된다.

---

## 2단계: 주제 설명

번역 대상 텍스트를 지정한다. 최소한 아래 정보가 필요하다.

- **어떤 저작**의 **어떤 범위**를 번역할 것인지 (예: 범주론 제1–5장)
- **주석의 깊이**: 최소 주석 vs. 상세 주석

기본값: 원전을 처음 접하는 학부생이 번역문만으로 텍스트를 이해할 수 있도록 충분한 주석을 단다.

---

## 문서 작업 흐름

1. 마크다운 초안 작성 (장 단위) → 말미에 "확인이 필요한 항목" 목록 제시
2. 조사 검사 실행 (KoNLPy)
3. 사용자 컨펌
4. `.tex` 파일 작성
5. `python3 build.py 문서이름.tex`으로 컴파일
6. 렌더링 검증 결과 확인 → 경고 있으면 처리 여부 확인
7. `output/`에 버전 번호가 붙은 PDF + TEX 저장

### 강의록 워크플로우와의 차이

시각화 검토 단계가 없다. tikz 도식, 분류 격자, 개념 대조표 등은 번역본에 포함하지 않는다.

### 마크다운 초안의 각주 배치 규칙

강의록과 동일. 각주는 참조된 단락 바로 아래에 블록인용(`>`) 형식으로 배치한다. 단일 숫자 번호를 사용한다.

```markdown
[1a1] 본문 단락.¹²

> ¹ 각주 내용.

> ² 각주 내용.

[1a6] 다음 단락.
```

### 마크다운의 참조 번호 규칙

`[번호]` 형식으로 행 첫머리에 배치. `.tex` 변환 시 `\margref{번호}`로 변환되어 좌측 여백에 출력된다. 참조 체계는 저작에 따라 다르다: Bekker(아리스토텔레스), Stephanus(플라톤), Diels–Kranz(소크라테스 이전), 장·절(범용) 등.

원전의 의미 단락이 시작되는 지점마다 붙인다.

---

## 새 문서 프리앰블 구조

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper]{article}
\usepackage{master}
\usepackage{translation}
% translation.sty v1_3:
%   \margref{} — 좌측 여백 참조 번호
%   \translationtitle{저자}{저작}{분량}
%   각주: master.sty의 \footnote 그대로 사용

% 저술 정의
\DeclareWorkGR{Cat}{범주론}{Κατηγορίαι}{Categoriae}

\fancyhead[L]{\footnotesize\color{midgray}Κατηγορίαι}
\fancyhead[R]{\footnotesize\color{midgray}\gri{Categoriae}}

\begin{document}
\thispagestyle{firstpage}

\translationtitle{Ἀριστοτέλης}{Κατηγορίαι, \gri{Categoriae}}{1a1--4a21}

\section*{제1장}

\margref{1a1}본문 시작...\footnote{각주 내용}

\end{document}
```

---

## 주요 LaTeX 명령어 — 번역본 전용

| 명령어 | 용도 |
|--------|------|
| `\margref{번호}` | 좌측 여백에 참조 번호 배치 (Bekker, Stephanus, DK 등) |
| `\translationtitle{저자}{저작}{분량}` | 표제 블록 |

### master.sty 명령어 — 번역본에서도 사용하는 것들

| 명령어 | 용도 |
|--------|------|
| `\footnote{...}` | 각주 (단일 숫자 체계) |
| `\gr{...}` | 그리스어 (비이탤릭 원칙) |
| `\gri{...}` | 문헌 제목 이탤릭 |
| `\grb{...}` | 볼드 원어 |
| `\citework{id}{라인번호}` | 저술 인용 — 첫 등장 원어 병기, 이후 한국어만 |
| `\usework{id}` | 본문 수동 소개 후 플래그 설정 |

### 번역본에서 사용하지 않는 명령어

`\bilingualquote`, `\srcquote`, `\weeksection`, `\bqnote`, `concepttable` 환경, tikz 관련 모든 것.

---

## LuaTeX-ja 줄바꿈 규칙

공통 규칙과 동일. `ONBOARDING v4_0`의 해당 절 참조.

---

## `\citework` 뒤 조사 처리 규칙

공통 규칙과 동일. `ONBOARDING v4_0`의 해당 절 참조.

---

## build.py 사용법

강의록과 동일.

```bash
python3 build.py 문서.tex           # minor 버전업 후 컴파일 (기본)
python3 build.py 문서.tex --major   # major 버전업 후 컴파일
python3 build.py 문서.tex --patch   # 버전 유지, 재컴파일만
python3 build.py --list             # 모든 파일 버전 현황
python3 build.py --bump-sty         # master.sty 버전업
```

---

## 조사 검사

강의록과 동일. `build.py`가 컴파일 전에 대응하는 `.md` 파일이 있으면 자동으로 조사 검사를 실행한다.

---

## 크로스체크 원칙

강의록과 동일. 행 번호 확신 불가 → `[행 번호 확인 필요]`. 사실 불확실 → `[확인 필요]`. 2차 문헌 페이지 → `[p. 확인 필요]`. 존재하지 않는 논문·저술을 만들어내지 않는다. **초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

---

## 스타일 업데이트 시

`translation.sty` 수정 → 프로젝트 지식의 파일을 새 버전으로 교체. `master.sty` 수정 시에는 `python3 build.py --bump-sty`.
