# 프로젝트 온보딩 가이드
버전: v3_11

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반으로 한국어·영어·그리스어·라틴어·아랍어(음차)를 안정적으로 조판한다.

---

## 버전 이력

**v3_11** (현재): `document_style_guide v3_11` 반영. 마크다운 원문 인용 태그 규칙, `wrapfig` 사용 규칙, `\weeksection` 문서화 추가.

**v3_10**: `master.sty v1_26` / `build.py v1_9` 반영.
  - `footmisc [bottom]` 옵션 적용으로 각주 페이지 하단 고정.
  - 폰트 파일명 저장소 기준(`KoPubWorld_Batang_*.ttf`)으로 통일.
  - `concepttable` 환경 추가 (`tabulary` 기반, 열 너비 자동 분배).
  - KoNLPy 조사 검사를 필수 빌드 단계로 통합 (`check_particles.py`).
    미설치 시 컴파일 중단 (폰트 미설치와 동일 처리).

**v3_9**: `master.sty v1_24` 변경 사항 반영. LuaTeX-ja 줄바꿈 규칙 추가. `\citework` 조사 처리 규칙 추가. tikz 도식 작업흐름 명시. `nobottomtitles*` 적용으로 헤딩·본문 분리 문제 해결.

---

## 1단계: 파일 업로드

새 채팅을 열 때마다 아래 두 파일을 반드시 첨부한다.
컨테이너는 채팅마다 초기화되므로 폰트는 매번 재설치가 필요하다.

- `KOPUBWORLD_TTF_FONTS-1.zip` — KoPub 바탕체 (한국어·한자 전용)
- `The_Brill_Typeface_Package_v_4_0.zip` — Brill (영어·라틴어·그리스어 전용)

**폰트가 설치되지 않으면 어떤 컴파일도 시작하지 않는다.**
`build.py`가 컴파일 전에 자동으로 폰트 존재 여부를 확인하고,
없으면 설치 방법을 안내하고 종료한다.

프로젝트 지식에 저장된 아래 파일들은 자동으로 참조된다.

- `master_vX_Y.sty` — 모든 서식 규칙 (현재: `master_v1_26.sty`)
- `build_vX_Y.py` — 빌드·버전 관리·렌더링 검증·조사 검사 (현재: `build_v1_9.py`)
- `document_style_guide_vX_Y.md` — 내용 작성 원칙 전체
- `ONBOARDING_vX_Y.md` — 이 파일

---

## 2단계: 세팅 명령

파일 첨부 후 다음과 같이 시작한다.

> "폰트 설치하고 빌드 환경 세팅해줘. 그리고 [주제]에 대한 문서를 만들고 싶어."

Claude가 자동으로 진행하는 순서는 이렇다. 폰트 zip을 `/usr/local/share/fonts/`에 설치하고 `fc-cache`를 갱신한다. `master.sty`와 `build.py`를 `/home/claude/project/`에 배치한다. `versions.json`을 초기화한다. 그런 다음 마크다운 초안 작성을 시작한다.

---

## 3단계: 주제 설명

주제를 줄 때는 반드시 아래 정보를 함께 제공한다.

- **어떤 텍스트**를 중심으로 다룰 것인지
- **어떤 논점**을 담고 싶은지

이 프로젝트의 기본값은 다음과 같다. 맥락은 학생들을 위한 수업 자료 제작이고, 대상은 고전학 강의 수강생(학부 1–4학년)이며, 논점은 개념과 텍스트 설명 중심으로 원전을 처음 접하는 독자를 전제하고 최대한 쉽고 명확하게 풀어 설명한다.

기본값에서 벗어나는 경우(심화 세미나, 특정 학년 등)에는 명시한다.

---

## 문서 작업 흐름

마크다운 컨펌 없이 바로 PDF 작업으로 넘어가지 않는다.

1. 마크다운 초안 작성 → 말미에 "확인이 필요한 항목" 목록 제시
2. 사용자 컨펌
3. **시각화 검토 실행** (`.tex` 작성 전 필수): 마크다운 전체를 훑어 도식·도표 후보를 "시각화 검토 결과" 형식으로 보고 → 사용자 컨펌
4. `.tex` 파일 작성 (저술 정의, tikz 도식 이 단계에서 삽입)
5. `python3 build.py 문서이름.tex`으로 컴파일
6. 렌더링 검증 결과 확인 → 경고 있으면 처리 여부 확인
7. `output/`에 버전 번호가 붙은 PDF + TEX 저장

### 마크다운 초안의 각주 배치 규칙

마크다운 초안에서 각주는 참조된 단락 바로 아래에 블록인용(`>`) 형식으로 배치한다.

```markdown
본문 단락.¹

> ¹ 각주 내용. 참조 단락 바로 아래 블록인용으로 배치한다.

다음 단락.
```

`.tex` 변환 시에는 이 블록들을 해당 위치의 `\footnote{}`로 변환한다.

### 마크다운 초안의 원문 인용 태그 규칙

고전 텍스트 원문 인용은 `.tex` 변환 시 사용할 환경을 태그로 명시한다.

- `[srcquote: 출처]` + `> 원문` + 번역 → `.tex`에서 `\srcquote{원문}{번역}{출처}`
- `[bilingualquote: 출처]` + `> 원문` + 번역 → `.tex`에서 `\bilingualquote{원문}{번역}{출처}`
- 인라인 (태그 없음) → `.tex`에서 `\gr{원문}`

상세 규칙은 `document_style_guide v3_11`의 "마크다운 초안의 원문 인용 태그 규칙" 절 참조.


### 새 문서 프리앰블 구조

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper]{article}
\usepackage{master}
% master.sty v1_26:
%   - xkanjiskip 전역 설정 포함 → 별도 선언 불필요
%   - nobottomtitles* 포함 → 헤딩·본문 분리 자동 방지
%   - footmisc [bottom] 포함 → 각주 페이지 하단 고정
%   - concepttable 환경 포함 → 열 너비 자동 분배 표
%   - master.sty가 이미 로드한 패키지 중복 선언 금지

% tikz 도식이 포함된 문서에만 추가
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}

% 이 문서에서 쓰는 저술만 정의
\DeclareWorkGR{Cat}{범주론}{Κατηγορίαι}{Categoriae}
\DeclareWorkLA{SummaTheol}{신학대전}{Summa Theologiae}

\fancyhead[L]{\footnotesize\color{midgray}문서 제목}
\fancyhead[R]{\footnotesize\color{midgray}주차 정보}

\begin{document}
\thispagestyle{firstpage}
% 본문
\end{document}
```

---

## LuaTeX-ja 줄바꿈 규칙

KoPub 바탕체(한국어)와 Brill(라틴/그리스) 혼용 환경에서는 **줄바꿈 위치**에 따라 공백이 소실되는 현상이 발생한다. `master.sty v1_26`의 `xkanjiskip` 전역 설정으로 대부분 해결되나, 아래 두 패턴은 여전히 주의가 필요하다.

**패턴 1** — 한국어 단어로 끝나는 줄 다음에 `\textbf`, `\citework`, `\gr`, `\gri` 등의 명령어가 오는 경우:

```latex
% ❌ "묶음인오르가논"으로 붙어 출력됨
아리스토텔레스의 논리학 저작 묶음인
\textbf{오르가논}(\gri{Organon})의 첫 번째 책이다.

% ✅ 같은 줄에 이어 쓴다
아리스토텔레스의 논리학 저작 묶음인 \textbf{오르가논}(\gri{Organon})의 첫 번째 책이다.
```

**패턴 2** — 라틴 문자·닫는 괄호로 끝나는 줄 다음에 한국어가 오는 경우:

```latex
% ❌ "Elenchi)으로이어진다"로 붙어 출력됨
소피스트적 논박(\gri{Sophistici Elenchi})으로
이어진다.

% ✅ 같은 줄에 이어 쓴다
소피스트적 논박(\gri{Sophistici Elenchi})으로 이어진다.
```

**원칙**: `.tex` 파일에서 문장 내부의 줄바꿈은 쉼표·마침표 뒤에서만 허용한다. 한국어 단어와 LaTeX 명령어 사이, 또는 라틴 문자와 한국어 사이에서는 줄바꿈하지 않는다.

---

## `\citework` 뒤 조사 처리 규칙

`\citework{id}{}`가 출력하는 한국어 텍스트(예: "범주론") 바로 뒤에 조사가 오면, `xkanjiskip`이 명령어 출력 경계에서 공백을 삽입하여 "범주론 은"처럼 조사가 분리된다.

```latex
% ❌ "범주론 은 항"으로 출력됨
\citework{Cat}{}은 항(terms)을 다룬다.

% ✅ 이미 소개된 저술은 한국어를 직접 쓴다
범주론은 항(terms)을 다룬다.
```

`\citework`의 첫 등장 이후, 조사가 바로 뒤에 오는 위치에서는 `\citework` 대신 한국어 저술명을 직접 입력한다.

---

## tikz 도식 작업흐름

**마크다운 단계에서는 도식을 삽입하지 않는다.** tikz 코드는 `.tex` 작성 단계에서만 삽입한다.

작업 순서는 이렇다. 마크다운 초안을 작성할 때는 마크다운 표만 사용한다. 사용자가 컨펌하면 시각화 검토를 실행하여 `document_style_guide`의 "시각화 검토 규칙"에 따라 후보를 추출하고 보고한다. 사용자가 컨펌하면 `.tex`에 tikz 코드를 삽입한다.

tikz 도식이 포함된 문서의 프리앰블에는 아래를 추가한다. `master.sty`에는 tikz가 포함되어 있지 않으므로 반드시 별도 선언이 필요하다.

```latex
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
```

### tikz 도식 너비 계산

A4 기준 textwidth는 약 140mm(마진 좌우 각 35mm)이다. 도식 전체 너비가 140mm를 초과하면 `Overfull \hbox` 경고와 함께 우측으로 삐져나온다. 격자형 도식은 왼쪽 헤더 열 + 데이터 열 × N의 합산이 140mm 이내인지 반드시 확인한다.

---

## build.py 사용법

```bash
python3 build.py 문서.tex           # minor 버전업 후 컴파일 (기본)
python3 build.py 문서.tex --major   # major 버전업 후 컴파일
python3 build.py 문서.tex --patch   # 버전 유지, 재컴파일만
python3 build.py --list             # 모든 파일 버전 현황
python3 build.py --bump-sty         # master.sty 버전업
```

---

## 주요 LaTeX 명령어

| 명령어 | 용도 |
|--------|------|
| `\gr{...}` | 그리스어 (비이탤릭 원칙) |
| `\gri{...}` | 그리스어·한국어 제외 모든 언어 문헌 제목 (이탤릭) |
| `\grb{...}` | 볼드 원어 (표 헤딩 등) |
| `\citework{id}{라인번호}` | 저술 인용 — 첫 등장: 원어 전체 병기, 이후: 한국어만 |
| `\usework{id}` | 본문 수동 소개 후 플래그 설정 (출력 없음) |
| `\bilingualquote{원문}{번역}{출처}` | 더블 칼럼 인용 (원문 좌 55% / 번역 우 44%) |
| `\srcquote{원문}{번역}{출처}` | 단독 짧은 인용 (원문 / 구분선 / 번역 / 출처) |
| `\weeksection{주차}{분량}{제목}` | 주차 강의록 상단 헤딩 (14pt 네이비, 우측 정렬) |
| `\bqnote{내용}` | `\bilingualquote` 번역란 내 각주 |
| `\needspace{N\baselineskip}` | 표·이미지 앞 공간 확보 |
| `\colorlet{이름}{기준색!N!white}` | master.sty 색상에서 tint 파생 |

### 저술 정의

```latex
\DeclareWorkGR{id}{한국어}{그리스어}{라틴어}
\DeclareWorkAR{id}{한국어}{영어 음차}{라틴어 번역}  % 라틴어 없으면 {}
\DeclareWorkLA{id}{한국어}{라틴어}
```

### master.sty 정의 색상 (RGB 하드코딩 금지)

| 이름 | 용도 |
|------|------|
| `h1navy` | section 헤딩 · 표 헤더 배경 |
| `h2burgundy` | subsection 헤딩 |
| `h3green` | subsubsection 헤딩 |
| `rulecolor` | 구분선 · booktabs 수평선 |
| `midgray` | 각주 번호 · 푸터 |
| `tableheadbg` | 표 헤더 배경 (연회색, 대안) |
| `citebg` | 인용 블록 배경 |
| `altrowbg` | zebra 격행 강조 (`rulecolor!12!white` ≈ RGB 234,234,234) |
| `reviewbg` | 강조 행 (`black!13!white` ≈ RGB 222,222,222) |
| `tableheadblue` | 표 헤더 행 배경 연한 하늘색 (RGB 210,228,245) |

### 표 표준 스타일

세로선 포함 · `\hline` · zebra · 헤더 `tableheadblue`

```latex
\setlength{\extrarowheight}{1.5pt}
\renewcommand{\arraystretch}{1.15}
\setlength{\tabcolsep}{5pt}
\rowcolors{2}{altrowbg}{white}
\noindent\begin{longtable}{|
  >{\centering\arraybackslash}m{20mm}|
  >{\raggedright\arraybackslash}m{80mm}|
}
\hline
\rowcolor{tableheadblue}
{\color{h1navy}\bfseries 열1} &
{\color{h1navy}\bfseries 열2} \\ \hline
\endhead
내용 \\ \hline
\end{longtable}
```

### longtable 열 너비 계산

세로선이 있으므로 `\arrayrulewidth × (열 수 + 1)`을 반드시 빼야 한다.
가용 너비 = textwidth − 세로선 합 − tabcolsep 합.
tabcolsep 5pt × 열 수 × 2, 세로선 0.4pt × (열 수 + 1).
계산이 불확실할 경우 python3으로 검산한다.

```python
# 예: 4열, 세로선 5개
textwidth_mm = 140.0
pt_to_mm = 25.4 / 72.27
available = textwidth_mm - 4*2*5*pt_to_mm - 5*0.4*pt_to_mm
print(f'{available:.1f}mm')  # → 약 125mm
```

---

## 크로스체크 원칙

Claude는 고전 텍스트 인용·철학사적 사실·2차 문헌 참조에서 실수를 할 수 있다.
다음 규칙을 항상 따른다.

행 번호(Bekker·Stephanus 등) 확신 불가 → `[행 번호 확인 필요]` 표시.
인명·연도·저술 제목 등 사실 정보 불확실 → `[확인 필요]` 표시.
2차 문헌 페이지 번호 생성 불가 → `[p. 확인 필요]` 표시.
서지 정보 미제공 → `[서지 정보 확인 필요]` 표시.
존재하지 않는 논문·저술을 만들어내지 않는다.

**마크다운 초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

`build.py`는 컴파일 후 자동으로 각주 번호 불일치·텍스트 랩 충돌·`Overfull \hbox`·이미지/표 페이지 초과를 감지하고, 경고가 발생하면 PDF 저장 전에 멈추고 처리 여부를 확인한다.

---

## 스타일 업데이트 시

`master.sty` 수정 → `python3 build.py --bump-sty` → 프로젝트 지식의 파일을 새 버전으로 교체. 다음 채팅부터 자동으로 최신 설정이 적용된다.

---

## 조사 검사 (`check_particles.py`)

`build.py`는 컴파일 전에 대응하는 `.md` 파일이 있으면 자동으로 조사 검사를 실행한다.
KoNLPy가 설치되어 있지 않으면 컴파일을 중단한다 (폰트 미설치와 동일 처리).

**세션 시작 시 필수 설치:**
```bash
pip install konlpy --break-system-packages
```
`setup.sh`를 실행하면 자동으로 설치된다.

**단독 실행 (마크다운 파일 직접 검사):**
```bash
python3 check_particles.py 파일명.md
python3 check_particles.py --all   # 현재 디렉터리 내 *.md 전체
```

**검사 항목:** 은/는, 이/가, 을/를, 과/와, 으로/로 오류 및 LuaTeX-ja 폰트 경계 조사 분리 경고.
