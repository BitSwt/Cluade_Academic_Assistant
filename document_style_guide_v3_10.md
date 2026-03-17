# 문서 작성 규칙 및 서식
버전: v3_10

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성에 적용하는 모든 규칙.
`master.sty`에 구현된 기술적 서식 설정과 내용 작성 원칙을 함께 정리했다.

---

## 버전 이력

**v3_10** (현재): `master.sty v1_24` 변경 사항 전면 반영. LuaTeX-ja 줄바꿈 규칙 신설. `\citework` 조사 처리 규칙 신설. 도식·도표 섹션 전면 개정(tikz 작업흐름 정식화, 시각화 검토 규칙 체계화). longtable 열 너비 계산 공식에 세로선 포함 명시.

---

## 작업 순서

**마크다운 컨펌 전에 절대로 PDF 작업으로 넘어가지 않는다.**

1. 마크다운 초안 작성 → 말미에 "확인이 필요한 항목" 목록 제시
2. 사용자 컨펌
3. **시각화 검토 실행** (`.tex` 작성 전 필수): 마크다운 전체를 훑어 도식·도표 후보를 "시각화 검토 결과" 형식으로 보고 → 사용자 컨펌
4. `.tex` 파일 작성 (프리앰블에 해당 문서에서 쓰는 저술만 정의, tikz 도식 이 단계에서 삽입)
5. `build.py`로 컴파일 → 렌더링 검증 자동 실행
6. `output/`에 버전 번호가 붙은 PDF + TEX 저장

### 마크다운 초안의 각주 배치 규칙

마크다운 초안에서 각주는 **참조된 단락 바로 아래**에 블록인용(`>`) 형식으로 배치한다.

```markdown
본문 단락이 여기에 있고 어떤 개념을 설명한다.¹

> ¹ 이것이 각주 내용이다. 단락 바로 아래 블록인용으로 배치한다.

다음 단락이 이어진다.
```

`.tex` 변환 시에는 이 블록들을 해당 위치의 `\footnote{}`로 변환한다.

---

## 기술 환경

엔진은 LuaLaTeX (XeLaTeX 아님). `master.sty` 하나를 로드하면 아래 모든 서식 설정이 자동 적용된다. 빌드·버전 관리·렌더링 검증은 `build.py`가 담당한다.

### 패키지 로드 원칙

**`master.sty`가 이미 로드한 패키지를 `.tex` 파일에서 중복 선언하지 않는다.** 옵션 충돌 또는 설정값 덮어쓰기가 발생할 수 있다.

`master.sty`가 로드하는 패키지 목록은 `luatexja-fontspec` · `etoolbox` · `geometry` · `setspace` · `booktabs` · `array` · `multirow` · `colortbl` · `xcolor` · `fancyhdr` · `microtype` · `titlesec`(nobottomtitles* 포함) · `hyperref` · `graphicx` · `wrapfig` · `needspace` · `caption` · `footmisc` · `longtable`이다.

tikz 도식이 포함된 문서는 아래를 개별 선언한다.

```latex
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
```

---

## 페이지 및 서식

양식은 Classical Reviews 스타일. A4, 마진 상하 28mm·좌우 35mm. textwidth ≈ 140mm.

**폰트** — 언어에 따라 자동 분리 (`ltjdefcharrange`로 처리, 수동 전환 불필요). 한국어·한자(漢字)는 KoPub 바탕체, 영어·라틴어·그리스어·숫자는 Brill. 본문 12pt / 주석 10pt / 본문 줄 간격 1.5 / 주석 내부 줄 간격 1.15 / 단어 간격 0.42em.

**xkanjiskip** — `master.sty v1_24`부터 전역 설정 포함 (0.25em plus 0.06em minus 0.04em). KoPub과 Brill 폰트 경계의 자동 간격이 전역 적용된다. 각 문서에서 별도 선언 불필요.

**nobottomtitles*** — `master.sty v1_24`부터 전역 설정 포함. 헤딩 뒤에 최소 한 줄의 본문이 이어질 공간이 없을 경우, 헤딩 전체를 자동으로 다음 페이지로 이동시킨다. section · subsection · subsubsection 모두에 적용된다. 각 문서에서 별도 선언 불필요.

**Widow / Orphan 방지** — `\clubpenalty`와 `\widowpenalty`를 3000으로 설정.

**헤딩** — 좌측 정렬, 위계별 색상. section은 17pt 네이비에 하단 구분선, subsection은 14pt 버건디, subsubsection은 12pt 초록. 헤딩 기본 폰트는 KoPub 유지. 헤딩 내 그리스어·라틴어는 `\gr{}`·`\gri{}`로 명시 전환.

---

## 색상 시스템

`master.sty`에 정의된 색상만 사용한다. 추가 색상은 `\colorlet`으로 파생시키며 RGB 값을 하드코딩하지 않는다.

| 이름 | 용도 | 값 |
|------|------|----|
| `h1navy` | section 헤딩 · 표 헤더 배경 | RGB 25,45,95 |
| `h2burgundy` | subsection 헤딩 | RGB 125,28,48 |
| `h3green` | subsubsection 헤딩 | RGB 38,95,65 |
| `rulecolor` | 구분선·booktabs 수평선 | gray 0.65 |
| `midgray` | 각주 번호·푸터 | gray 0.45 |
| `tableheadbg` | 표 헤더 배경 (연회색) | RGB 245,245,240 |
| `citebg` | 인용 블록 배경 | RGB 250,250,247 |
| `altrowbg` | zebra 격행 강조 | `rulecolor!12!white` ≈ RGB 234,234,234 |
| `reviewbg` | 강조 행 배경 | `black!13!white` ≈ RGB 222,222,222 |
| `tableheadblue` | 표 헤더 행 배경 (연한 하늘색) | RGB 210,228,245 |

---

## 언어 병기 원칙

한국어를 우선 배치하고 원어를 병기하는 것을 기본 원칙으로 한다. 그리스어 저술은 한국어 + 그리스어 원제 + 라틴어 학술 표준 제목을, 아랍어 저술은 한국어 + 영어 음차 + 라틴어 번역 제목(없으면 음차만)을, 라틴어 저술은 한국어 + 라틴어 제목을 병기한다.

아랍어 인명·지명은 학술 표준 영어 음차를 사용한다. 한 번 언급된 고전어 단어·인명·저술 제목은 이후 한국어로만 표기한다. 그리스어는 이탤릭 처리하지 않는다. 그리스어·한국어를 제외한 모든 언어의 문헌 제목은 이탤릭 처리한다.

---

## `\citework` 시스템

저술 제목은 `\citework` 명령어로 관리한다. 첫 등장 시 원어 전체 병기, 이후 한국어만 출력한다. 저술 정의는 각 문서 프리앰블에 해당 문서에서 쓰이는 저술만 직접 정의한다.

```latex
\DeclareWorkGR{id}{한국어}{그리스어}{라틴어}
\DeclareWorkAR{id}{한국어}{영어 음차}{라틴어 번역}  % 라틴어 없으면 {}
\DeclareWorkLA{id}{한국어}{라틴어}

\citework{id}{라인번호}   % 첫 등장: 원어 전체 병기 / 이후: 한국어만
\usework{id}              % 본문 수동 소개 후 플래그 설정 (출력 없음)
```

### `\citework` 뒤 조사 처리 규칙

`\citework{id}{}` 출력 직후 조사(은/는/이/가/을/를 등)가 오면, `xkanjiskip`이 명령어 출력 경계에서 공백을 삽입하여 "범주론 은"처럼 조사가 분리된다.

```latex
% ❌ "범주론 은 항"으로 출력됨
\citework{Cat}{}은 항(terms)을 다룬다.

% ✅ 이미 소개된 저술은 한국어를 직접 쓴다
범주론은 항(terms)을 다룬다.
```

`\citework`의 첫 등장 이후, 조사가 바로 뒤에 오는 위치에서는 `\citework` 대신 한국어 저술명을 직접 입력한다.

---

## LuaTeX-ja 줄바꿈 규칙

KoPub 바탕체(한국어)와 Brill(라틴/그리스) 혼용 환경에서는 줄바꿈 위치에 따라 공백이 소실되는 현상이 발생한다. `xkanjiskip` 전역 설정으로 대부분 해결되나, 아래 두 패턴은 여전히 주의가 필요하다.

**패턴 1** — 한국어 단어로 끝나는 줄 다음에 `\textbf`, `\citework`, `\gr`, `\gri`가 오는 경우:

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

**원칙**: `.tex` 파일에서 문장 내부의 줄바꿈은 쉼표·마침표 뒤에서만 허용한다. 한국어 단어와 LaTeX 명령어, 또는 라틴 문자와 한국어 사이에서는 줄바꿈하지 않는다.

---

## 인용 원칙

인용 양식은 시카고 스타일 (Notes-Bibliography). 원문(그리스어·라틴어)이 존재하는 경우 원문 인용을 우선한다.

| 상황 | 방식 |
|------|------|
| 원문 1–2줄, 본문 흐름에 녹아드는 경우 | 인라인. 번역은 원문 직후 본문에서 풀어 씀 |
| 원문을 단독으로 강조하고 싶은 경우 | `\srcquote{원문}{번역}{출처}` |
| 원문 또는 번역이 3줄 이상인 경우 | `\bilingualquote{원문}{번역}{출처}` |

`\bilingualquote` 번역란에서는 반드시 `\bqnote{내용}`을 사용한다. `\footnote`을 쓰면 알파벳 각주로 분리된다. 번역란에는 순수한 번역만 담는다.

---

## 주석

용도는 참고문헌·인용 출처 명시 및 부연 설명이다. 고전 텍스트 인용 시 학술 표준 편집본의 행 번호를 필수 표기한다. 각주 번호 색상은 회색, 링크 테두리 없음.

---

## 표와 이미지

텍스트 랩은 `wraptable` / `wrapfigure` 환경을 사용한다. 표·이미지 앞에 `\needspace{N\baselineskip}`으로 각주 영역 침범을 방지한다.

### 표 표준 스타일: 셀 테두리 + zebra

테두리 원칙은 이렇다. 세로선은 열 정의에 `|`를 사용한다. 가로선은 `\hline`을 사용하며 헤더 위아래 및 모든 행 끝에 적용한다. `\toprule` · `\midrule` · `\bottomrule`(booktabs 수평선)은 사용하지 않는다. booktabs 수평선은 `|` 세로선과 교차점 처리가 불일치한다.

열 정렬은 세로 가운데 정렬에 `m{너비}` 열 타입을 사용한다(`p{}` 사용 금지). 가로 가운데 정렬은 `>{\centering\arraybackslash}m{너비}`를 사용한다. 상하 패딩 보정은 `\setlength{\extrarowheight}{1.5pt}`, 행 간격은 `\renewcommand{\arraystretch}{1.15}`, 셀 좌우 여백은 `\setlength{\tabcolsep}{5pt}`로 설정한다.

헤더 행은 `\rowcolor{tableheadblue}` + `{\color{h1navy}\bfseries 열 이름}` 형식으로 지정한다. tableheadblue(연한 하늘색)에 흰색 텍스트는 대비 부족이므로 `h1navy` 색상을 반드시 사용한다.

zebra는 `\rowcolors{2}{altrowbg}{white}`로 2행부터 홀짝 자동 적용한다. 강조 행이 필요한 경우 `\rowcolor{reviewbg}` 수동 지정이 `\rowcolors`보다 우선한다.

**완성 예시:**

```latex
\setlength{\extrarowheight}{1.5pt}
\renewcommand{\arraystretch}{1.15}
\setlength{\tabcolsep}{5pt}
\rowcolors{2}{altrowbg}{white}
\noindent\begin{longtable}{|
  >{\centering\arraybackslash}m{20mm}|
  >{\centering\arraybackslash}m{60mm}|
  >{\centering\arraybackslash}m{42mm}|
}
\hline
\rowcolor{tableheadblue}
{\color{h1navy}\bfseries 번호} &
{\color{h1navy}\bfseries 항목} &
{\color{h1navy}\bfseries 설명} \\
\hline
\endhead
1 & 첫 번째 항목 & 설명 내용 \\ \hline
2 & 두 번째 항목 & 설명 내용 \\ \hline
\end{longtable}
```

### longtable 열 너비 자동 계산 시스템

페이지 전체를 차지하는 표에서 열 너비를 하드코딩하지 않는다. textwidth에서 세로선과 패딩을 빼고 남은 가용 너비를 가중치 비율로 가변 열에 분배한다. **세로선이 있는 경우 `\arrayrulewidth × (열 수 + 1)`을 반드시 포함한다.**

가용 너비 계산 공식: `available = textwidth − (열 수 × 2 × tabcolsep) − ((열 수 + 1) × arrayrulewidth)`. 단위 변환: 1pt = 25.4/72.27 mm. 계산이 불확실할 경우 아래 파이썬 코드로 검산한다.

```python
# 예: 4열, tabcolsep=5pt, arrayrulewidth=0.4pt
textwidth_mm = 140.0
pt_to_mm = 25.4 / 72.27
n_cols = 4
available = textwidth_mm - n_cols*2*5*pt_to_mm - (n_cols+1)*0.4*pt_to_mm
print(f'{available:.1f}mm')  # → 약 125mm
```

```latex
\newlength{\CWfixed}   \setlength{\CWfixed}{20mm}
\def\CWwA{6}  \def\CWwB{4}  \def\CWwtotal{10}
\newlength{\CWunit}  \newlength{\CWA}  \newlength{\CWB}
\AtBeginDocument{%
  \setlength{\CWunit}{%
    \dimexpr(\linewidth - \CWfixed - 5\arrayrulewidth - 8\tabcolsep)
    / \CWwtotal\relax}%
  \setlength{\CWA}{\dimexpr \CWwA\CWunit\relax}%
  \setlength{\CWB}{\dimexpr \CWwB\CWunit\relax}%
}
```

---

## 도식·도표

개념 설명·위계 구조 시각화 시 적극 활용한다. **마크다운 단계에서는 도식을 삽입하지 않는다. tikz 코드는 `.tex` 작성 단계에서만 삽입한다.**

### 시각화 검토 규칙 (`.tex` 작성 전 필수 적용)

마크다운 컨펌 후 `.tex` 파일 작성에 들어가기 전, 아래 체크리스트를 기준으로 마크다운 전체를 훑어 시각화 후보 항목을 추출한다. 추출된 항목은 아래 형식으로 사용자에게 보고하고, 컨펌 후 `.tex`에 반영한다.

```
[시각화 검토 결과]
- 1주차 2장: 사중 분류 → 유형 1 (2×2 격자) 전환 권장
- 1주차 3장: 포르피리오스의 나무 → 유형 2 (위계 도식) 전환 권장
- 5주차: 수용사 → 유형 3 (타임라인) 전환 권장
- 그 외: 기존 마크다운 표 longtable로 유지
```

#### 시각화 후보 유형과 판단 기준

**유형 1 — 분류 격자 / 매트릭스** (tikz `matrix` 또는 `tabular`): 두 가지 독립적인 기준(예: +/−, 있음/없음)이 교차하여 네 칸 이상의 조합이 산출되거나, 강조해야 할 특정 셀이 있을 때 격자 도식으로 전환을 검토한다. 이 강의록에서의 해당 위치는 1주차 사중 분류, 4주차 대립의 네 유형 비교이다.

**유형 2 — 위계 구조 / 나무** (tikz `\node` + `\draw`): 유(genus) → 종(species) → 개별자처럼 포함 관계가 명시적으로 서술되거나, "A는 B에 포섭된다"와 같은 표현이 반복될 때 수직 계층 도식으로 전환을 검토한다. 이 강의록에서의 해당 위치는 1주차 포르피리오스의 나무, 2주차 제1·제2실체 위계이다.

**유형 3 — 타임라인** (tikz 수평선 + 노드): 인물·저작·사건이 연대순으로 나열되며 시간 간격이 논지에서 중요하거나, 지적 계보가 시간축 위에서 펼쳐질 때 수평 타임라인으로 전환을 검토한다. 이 강의록에서의 해당 위치는 5주차 수용사 조망(포르피리오스 → 보에티우스 → 아베로에스 → 아퀴나스)이다.

**유형 4 — 개념 대조표** (표준 `longtable`): 두 개 이상의 개념을 같은 기준으로 비교하는 산문이 있거나, 비교 항목이 4개 이상인 경우 정형 표로 전환을 검토한다. 이 강의록에서의 해당 위치는 3주차 질의 네 종류, 4주차 대립 네 유형, 5주차 수용사 인물 비교이다.

**유형 5 — 의존·방사 구조** (tikz 방사형 화살표): 하나의 핵심 항목에 다른 모든 항목이 의존하거나, "A 없이는 B도 없다"처럼 단방향 의존 관계가 한 항목을 중심으로 반복될 때 중심-주변 방사형 도식으로 전환을 검토한다. 이 강의록에서의 해당 위치는 2주차 제1실체의 존재론적 우선성이다.

#### tikz 도식 너비 규칙

`\tikzpicture` 내부 노드 좌표와 너비는 textwidth ≈ 140mm를 기준으로 계산한다. 도식 전체 너비가 140mm를 초과하면 `Overfull \hbox` 경고와 함께 우측으로 삐져나온다. 격자형 도식은 왼쪽 헤더 열 + 데이터 열 × N의 합산이 140mm 이내인지 반드시 확인한다.

---

## 참고문헌

헤딩은 반드시 `\subsubsection*{참고문헌}`(H3, 12pt 초록)으로 작성한다. 개별 항목은 `\refitem`으로 나열하며, 서지 형식은 시카고 스타일을 따른다.

```latex
\subsubsection*{참고문헌}
\begin{references}
\refitem Ackrill, J. L. \gri{Aristotle's Categories and De Interpretatione}.
  Oxford: Clarendon Press, 1963.
\end{references}
```

---

## 크로스체크 원칙

Claude는 고전 텍스트 인용·철학사적 사실·2차 문헌 참조에서 실수를 할 수 있다. 행 번호 확신 불가 → `[행 번호 확인 필요]`. 인명·연도·저술 제목 불확실 → `[확인 필요]` 또는 "~으로 추정된다". 학자마다 이견이 있는 경우 → "학자에 따라 이견이 있다". 2차 문헌 페이지 번호 생성 불가 → `[p. 확인 필요]`. 서지 정보 미제공 → `[서지 정보 확인 필요]`. 존재하지 않는 논문·저술을 만들어내지 않는다.

**초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

---

## 버전 관리

파일명은 `name_vX_Y` 형식 (예: `arabic_reception_v1_2.pdf`). 내용 수정은 minor(기본값), 구조적 변경은 major, 재컴파일만 할 경우 `--patch`. `master.sty` 수정 시 `--bump-sty`로 별도 버전업.

---

## 최종 목적

모든 문서는 나중에 책으로 엮을 것을 전제로 한다. 인용 출처와 참고문헌 표기를 처음부터 일관되게 관리한다.
