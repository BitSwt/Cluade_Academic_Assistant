# 문서 작성 규칙 및 서식
버전: v3_11

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성에 적용하는 모든 규칙.

---

## 버전 이력

**v3_11** (현재): 마크다운 초안 원문 인용 태그 규칙 신설. `wrapfig`/`wraptable` 사용 규칙 신설. `\weeksection` 문서화. `\gr`/`\gri`/`\grb` 문서화. `\bqnote` 사용법 확충. 시각화 유형 6(흐름 도식) 추가.

**v3_10**: `master.sty v1_25` 전면 반영. LuaTeX-ja 줄바꿈 규칙 신설. `\citework` 조사 처리 규칙 신설. 도식·도표 섹션 전면 개정. `\concepttable` 환경 규칙 추가. `nobottomtitles*` + `\needspace` 병용 원칙 추가.

---

## 작업 순서

**마크다운 컨펌 전에 절대로 PDF 작업으로 넘어가지 않는다.**

1. 마크다운 초안 작성 → 말미에 "확인이 필요한 항목" 목록 제시
2. 사용자 컨펌
3. **시각화 검토 실행** (`.tex` 작성 전 필수): 마크다운 전체를 훑어 도식·도표 후보를 보고 → 사용자 컨펌
4. `.tex` 파일 작성 (프리앰블에 해당 문서 저술 정의, tikz 도식 이 단계에서 삽입)
5. `build.py`로 컴파일 → 렌더링 검증 자동 실행
6. `output/`에 버전 번호가 붙은 PDF + TEX 저장

### 마크다운 초안의 각주 배치 규칙

마크다운 초안에서 각주는 **참조된 단락 바로 아래**에 블록인용(`>`) 형식으로 배치한다. `.tex` 변환 시 `\footnote{}`으로 변환한다.

### 마크다운 초안의 원문 인용 태그 규칙

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

## 기술 환경

엔진은 LuaLaTeX. `master.sty` 하나로 모든 서식이 자동 적용된다.

`master.sty`가 로드하는 패키지(중복 선언 금지): `luatexja-fontspec` · `etoolbox` · `geometry` · `setspace` · `booktabs` · `array` · `multirow` · `colortbl` · `xcolor` · `fancyhdr` · `microtype` · `titlesec`(nobottomtitles*) · `hyperref` · `graphicx` · `wrapfig` · `needspace` · `caption` · `footmisc` · `longtable` · `tabulary`

tikz 도식이 포함된 문서에만 추가:
```latex
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
```

---

## 페이지 및 서식

A4, 마진 상하 28mm·좌우 35mm. textwidth ≈ 140mm.

**폰트**: 한국어·한자는 KoPub 바탕체, 영어·라틴어·그리스어·숫자는 Brill. 본문 12pt / 주석 10pt / 본문 줄 간격 1.5.

**xkanjiskip**: `master.sty v1_25`부터 전역 설정(0.25em). KoPub↔Brill 폰트 경계 자동 간격 삽입. 별도 선언 불필요.

**nobottomtitles***: 헤딩 뒤 본문 공간이 부족하면 헤딩을 다음 페이지로 자동 이동. **단, `longtable`·`tabulary`·tikz `figure` 앞에는 `\needspace`를 헤딩 바로 앞에 추가해야 한다** (아래 규칙 참조).

**헤딩**: 좌측 정렬. section은 17pt 네이비 + 하단 구분선, subsection은 14pt 버건디, subsubsection은 12pt 초록.

---

## `\weeksection` 명령

주차 강의록의 상단 헤딩에 사용한다. `\section*`을 우회하여 직접 조판.

```latex
\weeksection{주차}{분량}{제목}
% 예: \weeksection{제12주}{분석론 전서 24a10--26b33}{삼단논법의 정의, 제1격}
```

세 줄 모두 14pt 네이비 볼드, 우측 정렬, 줄간격 1.0, 하단 구분선. `\section*`과 달리 목차에 포함되지 않으며, 페이지 상단에 고정 배치된다.

---

## 헤딩과 표·도식의 페이지 분리 방지

`nobottomtitles*`는 텍스트 단락 앞 헤딩만 보호한다. 표와 도식은 별도로 처리해야 한다.

```latex
% 표·도식 앞 소제목에 \needspace 추가 (헤딩 바로 앞에 배치)
\needspace{8\baselineskip}   % 짧은 표
\needspace{12\baselineskip}  % 긴 표
\needspace{18\baselineskip}  % tikz 도식
\subsection{소제목}
\begin{concepttable}{...}
```

모든 `\subsection` 앞에 최소 `\needspace{5\baselineskip}`을 기본으로 추가한다.

---

## 색상 시스템

`master.sty` 정의 색상만 사용. 추가 색상은 `\colorlet`으로 파생.

| 이름 | 용도 | 값 |
|------|------|---|
| `h1navy` | section 헤딩 · 표 헤더 | RGB 25,45,95 |
| `h2burgundy` | subsection 헤딩 | RGB 125,28,48 |
| `h3green` | subsubsection 헤딩 | RGB 38,95,65 |
| `rulecolor` | 구분선 | gray 0.65 |
| `midgray` | 각주 번호·푸터 | gray 0.45 |
| `citebg` | 인용 블록 배경 (`srcquote`·`bilingualquote`) | RGB 250,250,247 |
| `altrowbg` | zebra 격행 | `rulecolor!12!white` |
| `reviewbg` | 강조 행 | `black!13!white` |
| `tableheadblue` | 표 헤더 행 배경 | RGB 210,228,245 |

---

## 그리스어 서식 명령

| 명령 | 용도 | 출력 |
|------|------|------|
| `\gr{텍스트}` | 인라인 그리스어 (정체) | upshape, Brill |
| `\gri{텍스트}` | 인라인 그리스어 (이탤릭) | italics, Brill |
| `\grb{텍스트}` | 인라인 그리스어 (볼드) | bold upshape, Brill |

그리스어는 이탤릭 처리하지 않는 것이 기본(`\gr`). 강조가 필요한 경우에만 `\gri` 또는 `\grb`를 사용한다.

---

## 언어 병기 원칙

한국어 우선, 원어 병기. 그리스어 저술: 한국어 + 그리스어 + 라틴어. 아랍어 저술: 한국어 + 영어 음차 (+ 라틴어). 라틴어 저술: 한국어 + 라틴어. 그리스어는 이탤릭 처리하지 않는다. 그리스어·한국어 제외 문헌 제목은 이탤릭 처리한다.

---

## `\citework` 시스템

첫 등장 시 원어 전체 병기, 이후 한국어만 출력.

```latex
\DeclareWorkGR{id}{한국어}{그리스어}{라틴어}
\DeclareWorkAR{id}{한국어}{영어 음차}{라틴어 번역}
\DeclareWorkLA{id}{한국어}{라틴어}
\citework{id}{라인번호}
\usework{id}
```

### `\citework` 뒤 조사 처리

`\citework{id}{}` 출력 후 조사가 오면 `xkanjiskip`이 공백을 삽입하여 "범주론 은"처럼 분리된다. 첫 등장 이후에는 한국어를 직접 입력한다.

```latex
% ❌ \citework{Cat}{}은 항(terms)을 다룬다.
% ✅ 범주론은 항(terms)을 다룬다.
```

---

## LuaTeX-ja 줄바꿈 규칙

**패턴 1**: 한국어 단어 끝 줄 다음에 `\textbf`, `\citework`, `\gr`, `\gri`가 오는 경우 공백이 소실된다. 같은 줄에 이어 써야 한다.

**패턴 2**: 라틴 문자·닫는 괄호 끝 줄 다음에 한국어가 오는 경우 공백이 소실된다. 같은 줄에 이어 써야 한다.

**원칙**: 문장 내부 줄바꿈은 쉼표·마침표 뒤에서만 허용한다.

---

## 인용 원칙

시카고 스타일 (Notes-Bibliography). 원문이 있으면 원문 우선.

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

## `wrapfig` / `wraptable` 사용 규칙

`master.sty`에서 `wrapfig` 패키지가 로드되며, 여백이 설정되어 있다(`\intextsep` 12pt, `\columnsep` 16pt).

### 사용 기준

| 상황 | 환경 |
|------|------|
| 본문 옆에 놓을 수 있는 작은 도식/표 (폭 ≤ 65mm, 높이 ≤ 8행) | `wrapfigure` 또는 `wraptable` |
| 전체 폭을 차지해야 하는 표/도식 | `center` + `longtable`/`concepttable`/tikz |
| 페이지 상단/하단에 떠야 하는 큰 도식 | `figure` 환경 (단, `figure` 환경은 사용하지 않기로 결정 → `center` 사용) |

### 사용법

```latex
\begin{wrapfigure}{r}{60mm}   % r = 오른쪽, 60mm = 폭
  \centering
  \begin{tikzpicture}
    % 도식 코드
  \end{tikzpicture}
  \caption*{도식 설명}         % caption* = 번호 없는 캡션
\end{wrapfigure}
```

**주의사항:**
- `wrapfigure`/`wraptable`은 페이지 상단·하단·단락 시작 직후에서만 안정적으로 작동한다. 단락 중간에 삽입하면 겹침이 발생할 수 있다.
- `\needspace`와 함께 사용하여 페이지 넘김 문제를 방지한다.
- 2단 조판에서는 사용하지 않는다 (본 프로젝트는 단단 조판).

---

## `\concepttable` 환경

개념 정리 표에 사용한다. `tabulary` 기반으로 전체 폭이 항상 `\linewidth`에 맞춰진다.

**열 타입 선택 원칙:**
- 짧은 번호·기호: `c` (소문자, 고정)
- 중간 길이 텍스트 (그리스어 포함): `C` (대문자, 자동 분배)
- 긴 설명·정의: `L` (자동 분배)
- **그리스어가 포함된 열에는 `c` 대신 반드시 `C`를 사용한다** (`c`는 긴 그리스어에서 overflow 유발)
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

## longtable 표준 스타일

세로선 포함 · `\hline` · zebra · 헤더 `tableheadblue`.

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

가용 너비 = textwidth − (열 수 × 2 × tabcolsep) − ((열 수 + 1) × arrayrulewidth). 불확실하면 아래 파이썬 코드로 검산한다.

```python
# 4열, tabcolsep=5pt, arrayrulewidth=0.4pt
textwidth_mm = 140.0
pt = 25.4 / 72.27
available = textwidth_mm - 4*2*5*pt - 5*0.4*pt
print(f'{available:.1f}mm')  # → 약 125mm
```

---

## 도식·도표

**마크다운 단계에서는 도식을 삽입하지 않는다.** tikz 코드는 `.tex` 작성 단계에서만 삽입한다. 마크다운에서는 텍스트 도식(들여쓰기 + ASCII)으로 구조를 표현하고, 말미의 **[시각화 후보 정리]** 블록에서 유형과 위치를 명시한다.

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

**유형 6 — 흐름 도식**: 단계적 과정·변환·환원 경로 표현. *해당: 삼단논법 환원 계통도, 인식의 네 단계 상승(감각→기억→경험→보편자), 분석-종합 방향.*

### tikz 너비 규칙

도식 전체 너비 ≤ 140mm. 격자형 도식: 왼쪽 헤더 열 + 데이터 열 × N ≤ 140mm 확인.

---

## 참고문헌

`\subsubsection*{참고문헌}`(H3, 12pt 초록) + `\begin{references}` + `\refitem`. 시카고 스타일.

---

## 크로스체크 원칙

행 번호 확신 불가 → `[행 번호 확인 필요]`. 사실 불확실 → `[확인 필요]`. 2차 문헌 페이지 번호 → `[p. 확인 필요]`. 존재하지 않는 논문·저술을 만들어내지 않는다. **초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

---

## 버전 관리

파일명: `name_vX_Y`. 내용 수정은 minor(기본), 구조적 변경은 major, 재컴파일만 `--patch`. `master.sty` 수정 시 `--bump-sty`.

---

## 최종 목적

모든 문서는 나중에 책으로 엮을 것을 전제로 한다. 인용 출처와 참고문헌 표기를 처음부터 일관되게 관리한다.
