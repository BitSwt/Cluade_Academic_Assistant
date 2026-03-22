# 강의록 작성 규칙 및 서식
버전: v1_0

강의록 제작에만 적용하는 규칙. 공통 규칙(`style_guide v4_0`)을 기반으로 하며, 이 문서는 강의록 전용 사항만 다룬다.

---

## 버전 이력

**v1_0** (현재): `document_style_guide v3_11`에서 강의록 전용 규칙을 분리. 작업 순서, 원문 인용 태그, `\weeksection`, 시각화 검토, tikz 도식, `wrapfig`/`wraptable`, `concepttable`, `\bilingualquote`, `\srcquote`, `\bqnote`.

---

## 작업 순서

**마크다운 컨펌 전에 절대로 PDF 작업으로 넘어가지 않는다.**

1. 마크다운 초안 작성 → 말미에 "확인이 필요한 항목" 목록 제시
2. 사용자 컨펌
3. **시각화 검토 실행** (`.tex` 작성 전 필수): 마크다운 전체를 훑어 도식·도표 후보를 보고 → 사용자 컨펌
4. `.tex` 파일 작성 (프리앰블에 해당 문서 저술 정의, tikz 도식 이 단계에서 삽입)
5. **2차 크로스체크 실행** (`style_guide v4_0`의 크로스체크 원칙에 따라 전수 검토)
6. `build.py`로 컴파일 → 렌더링 검증 자동 실행
7. `output/`에 버전 번호가 붙은 PDF + TEX 저장

---

## 마크다운 초안의 원문 인용 태그 규칙

마크다운 초안에서 고전 텍스트 원문 인용은 아래 태그를 사용하여 `.tex` 변환 시 어떤 환경을 사용할지 명시한다.

**srcquote** (원문 단독 강조, 1–3줄):

```markdown
[srcquote: 분석론 전서 24b18–20]

> Συλλογισμὸς δέ ἐστι λόγος ἐν ᾧ τεθέντων τινῶν...

'삼단논법이란...' (분석론 전서 24b18–20)
```

→ `.tex` 변환 시 `\srcquote{원문}{번역}{출처}`

**bilingualquote** (원문 + 번역이 각 3줄 이상, 더블칼럼):

```markdown
[bilingualquote: 분석론 전서 24b18–22]

> Συλλογισμὸς δέ ἐστι λόγος ἐν ᾧ τεθέντων τινῶν ἕτερόν τι τῶν κειμένων ἐξ ἀνάγκης συμβαίνει τῷ ταῦτα εἶναι· λέγω δὲ τῷ ταῦτα εἶναι τὸ διὰ ταῦτα συμβαίνειν...

'삼단논법이란, 어떤 것들이 놓이면...' (분석론 전서 24b18–22)
```

→ `.tex` 변환 시 `\bilingualquote{원문}{번역}{출처}` (좌 55% 원문 / 우 44% 번역)

**인라인** (원문 1–2줄, 본문 흐름에 녹아드는 경우): 별도 태그 없이 본문에 그리스어를 직접 삽입한다.

→ `.tex` 변환 시 `\gr{원문}` 또는 `\gri{원문}`으로 처리.

---

## 인용 환경 대응표

| 상황 | .tex 환경 | 마크다운 태그 |
|------|-----------|-------------|
| 원문 1–2줄, 본문 흐름에 녹아드는 경우 | 인라인 (`\gr{}`) | 태그 없음, 본문에 직접 삽입 |
| 원문을 단독 강조 (1–3줄) | `\srcquote{원문}{번역}{출처}` | `[srcquote: 출처]` |
| 원문 또는 번역이 3줄 이상 | `\bilingualquote{원문}{번역}{출처}` | `[bilingualquote: 출처]` |

### `\bilingualquote` 상세

좌 55% 원문 / 우 44% 번역. `citebg` 배경색. 번역란 각주는 반드시 `\bqnote{}`를 사용한다 — 일반 `\footnote{}`는 `colorbox`/`parbox` 그룹 경계를 넘지 못하므로 컴파일 오류가 발생한다.

```latex
\bilingualquote{%
  Συλλογισμὸς δέ ἐστι λόγος ἐν ᾧ τεθέντων τινῶν
  ἕτερόν τι τῶν κειμένων ἐξ ἀνάγκης συμβαίνει
  τῷ ταῦτα εἶναι.%
}{%
  삼단논법이란, 어떤 것들이 놓이면, 그 놓인 것들과
  다른 무엇인가가, 그 놓인 것들이 그러하기 때문에,
  필연적으로 따라나오는 논증이다.\bqnote{번역 관련 각주 내용}%
}{분석론 전서 24b18--20}
```

### `\srcquote` 상세

원문 / 구분선 / 번역 / 출처 순으로 수직 배치. `citebg` 배경색.

```latex
\srcquote{%
  οὐκ ἄρα ἔστιν ἐξ ἄλλου γένους μεταβάντα δεῖξαι%
}{%
  따라서 다른 류로 건너가서 증명하는 것은 불가능하다.%
}{분석론 후서 75a38--39}
```

---

## `\weeksection` 명령

주차 강의록의 상단 헤딩에 사용한다.

```latex
\weeksection{주차}{분량}{제목}
% 예: \weeksection{제12주}{분석론 전서 24a10--26b33}{삼단논법의 정의, 제1격}
```

세 줄 모두 14pt 네이비 볼드, 우측 정렬, 줄간격 1.0, 하단 구분선.

---

## `wrapfig` / `wraptable` 사용 규칙

`master.sty`에서 `wrapfig` 패키지가 로드되며, 여백이 설정되어 있다(`\intextsep` 12pt, `\columnsep` 16pt).

### 사용 기준

| 상황 | 환경 |
|------|------|
| 본문 옆에 놓을 수 있는 작은 도식/표 (폭 ≤ 65mm, 높이 ≤ 8행) | `wrapfigure` 또는 `wraptable` |
| 전체 폭을 차지해야 하는 표/도식 | `center` + `longtable`/`concepttable`/tikz |

### 사용법

```latex
\begin{wrapfigure}{r}{60mm}
  \centering
  \begin{tikzpicture}
    % 도식 코드
  \end{tikzpicture}
  \caption*{도식 설명}
\end{wrapfigure}
```

**주의사항:** `wrapfigure`/`wraptable`은 페이지 상단·하단·단락 시작 직후에서만 안정적으로 작동한다. `\needspace`와 함께 사용하여 페이지 넘김 문제를 방지한다.

---

## `\concepttable` 환경

개념 정리 표에 사용한다. `tabulary` 기반으로 전체 폭이 항상 `\linewidth`에 맞춰진다.

**열 타입 선택 원칙:**
- 짧은 번호·기호: `c` (소문자, 고정)
- 중간 길이 텍스트 (그리스어 포함): `C` (대문자, 자동 분배)
- 긴 설명·정의: `L` (자동 분배)
- **그리스어가 포함된 열에는 `c` 대신 반드시 `C`를 사용한다**
- 행이 6개 이상이거나 복잡한 표는 `longtable` + `m{}` 조합이 더 안정적

```latex
\needspace{8\baselineskip}
\subsection*{개념 정리}

\begin{concepttable}{|c|C|L|L|}
\hline
\rowcolor{tableheadblue}
{\color{h1navy}\bfseries \#} &
{\color{h1navy}\bfseries 개념} &
{\color{h1navy}\bfseries 정의} &
{\color{h1navy}\bfseries 예시} \\ \hline
1 & 제1실체 & 가장 탁월한 실체 & 이 소크라테스 \\ \hline
\end{concepttable}
```

---

## 도식·도표

**마크다운 단계에서는 도식을 삽입하지 않는다.** tikz 코드는 `.tex` 작성 단계에서만 삽입한다.

### 시각화 검토 규칙 (`.tex` 작성 전 필수)

마크다운 전체를 훑어 후보를 추출하고 아래 형식으로 보고한다.

```
[시각화 검토 결과]
- 1주차 2장: 사중 분류 → 유형 1 (2×2 격자) 전환 권장
- 1주차 3장: 포르피리오스의 나무 → 유형 2 (위계 도식) 전환 권장
```

### 시각화 유형

**유형 1 — 분류 격자**: 두 기준 교차로 4칸 이상 산출.
**유형 2 — 위계 나무**: 유→종→개별자 포함 관계.
**유형 3 — 타임라인**: 연대순 지적 계보.
**유형 4 — 개념 대조표**: 같은 기준으로 비교하는 항목 4개 이상.
**유형 5 — 방사 구조**: 한 항목에 모든 것이 의존.
**유형 6 — 흐름 도식**: 단계적 과정·변환·환원 경로 표현.

### tikz 도식 규칙

tikz 도식이 포함된 문서의 프리앰블에는 아래를 추가한다. `master.sty`에는 tikz가 포함되어 있지 않으므로 반드시 별도 선언이 필요하다.

```latex
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
```

도식 전체 너비 ≤ 140mm. 격자형 도식: 왼쪽 헤더 열 + 데이터 열 × N ≤ 140mm 확인. 도식 앞에는 `\needspace{18\baselineskip}`을 추가한다.

---

## 새 문서 프리앰블 구조

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper]{article}
\usepackage{master}

% tikz 도식이 포함된 문서에만 추가
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}

% 이 문서에서 쓰는 저술만 정의
\DeclareWorkGR{Cat}{범주론}{Κατηγορίαι}{Categoriae}

\fancyhead[L]{\footnotesize\color{midgray}문서 제목}
\fancyhead[R]{\footnotesize\color{midgray}주차 정보}

\begin{document}
\thispagestyle{firstpage}
% 본문
\end{document}
```

---

## 강의록 전용 명령어 요약

| 명령어 | 용도 |
|--------|------|
| `\weeksection{주차}{분량}{제목}` | 주차 강의록 상단 헤딩 |
| `\bilingualquote{원문}{번역}{출처}` | 더블 칼럼 인용 |
| `\srcquote{원문}{번역}{출처}` | 단독 짧은 인용 |
| `\bqnote{내용}` | `\bilingualquote` 번역란 내 각주 |
