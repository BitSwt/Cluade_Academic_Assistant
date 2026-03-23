# 번역본 작성 규칙 및 서식
버전: v1_3

고전 텍스트 한국어 번역본 제작에 적용하는 모든 규칙.
강의록 작성 규칙과 공유하는 기반(master.sty, build.py, KoNLPy 조사 검사)은 동일하며, 이 문서는 번역본에만 고유한 규칙을 다룬다.

---

## 버전 이력

**v1_3** (현재): 표제 블록 3요소 배치로 변경 (좌 원어 / 중앙 분량 / 우 라틴어). 페이지 헤더 2줄 형식으로 변경 (저자 / 제목, 분량 없음). 여백 참조 번호 색상 버건디(`h2burgundy`)로 변경. `translation.sty v1_4` 반영.

**v1_2**: `\bekker` → `\margref` 범용 명칭 변경. Bekker, Stephanus, DK, SVF, 장·절 번호 등 어떤 참조 체계에도 사용 가능. `translation.sty v1_3` 반영.

**v1_1**: 이중 각주(manyfoot) 폐지. 단일 `\footnote` 숫자 체계로 통합.

**v1_0**: 초판. Bekker 번호, 이중 각주(`\tfn` + `\cfn`), 표제 블록.

---

## 강의록과의 차이

| 항목 | 강의록 | 번역본 |
|------|--------|--------|
| 마크다운 원문 태그 | `[srcquote]`, `[bilingualquote]` | 없음 (원문 없이 번역만) |
| 행 번호 | 인용 시에만 표기 | `[1a1]` 태그로 전체 표기 |
| 각주 체계 | `\footnote` | `\footnote` (동일) |
| 시각화 검토 | 필수 단계 | 없음 |
| tikz 도식 | 있음 | 없음 |
| .tex 추가 패키지 | `translation.sty` 불필요 | `translation.sty` 필수 |

---

## 작업 순서

**마크다운 컨펌 전에 절대로 .tex 작업으로 넘어가지 않는다.**

1. 마크다운 초안 작성 (장 단위) → 말미에 "확인이 필요한 항목" 목록 제시
2. 조사 검사 실행 (KoNLPy)
3. 사용자 컨펌
4. `.tex` 파일 작성
5. **2차 크로스체크 실행** (`style_guide v4_0`의 크로스체크 원칙에 따라 전수 검토)
6. `build.py`로 컴파일 → 렌더링 검증 자동 실행
7. `output/`에 버전 번호가 붙은 PDF + TEX 저장

강의록 워크플로우와의 핵심 차이: 시각화 검토 단계가 없다.

---

## 마크다운 규약

### 참조 번호

원전의 표준 참조 번호를 대괄호 안에 표기한다. 반드시 행 첫머리에 온다. 참조 체계는 저작에 따라 다르다.

```markdown
[1a1] 동음이의적(ὁμώνυμα)이라 불리는 것들은, ...     ← Bekker (아리스토텔레스)
[71a] 모든 가르침과 모든 배움은 ...                    ← Stephanus (플라톤)
[DK 28B8] 남은 것은 오직 하나의 길에 대한 이야기뿐 ... ← Diels–Kranz (소크라테스 이전)
[I.1] 철학의 연구를 뜻하는 사람은 ...                  ← 장·절 (범용)
```

`.tex` 변환 시 `\margref{1a1}`로 바뀌어 좌측 여백에 **버건디 산세리프**로 배치된다.

참조 번호는 원전의 의미 단락이 시작되는 지점마다 붙인다. 모든 행에 붙이는 것이 아니라, 번역문의 흐름상 자연스러운 단락 전환 지점에 배치한다.

### 각주

강의록과 동일한 단일 각주 체계를 사용한다. 번역 주석(어휘 선택, 구문 해석)과 해설 주석(철학적 맥락, 2차 문헌)을 구분하지 않고, 하나의 숫자 번호(1, 2, 3, …)로 통합한다.

```markdown
[1a1] 동음이의적(ὁμώνυμα)이라 불리는 것들은, 이름(ὄνομα)만
공통으로 가지면서 그 이름에 따른 실체의 정의(λόγος τῆς οὐσίας)는
서로 다른 것들이다.¹²

> ¹ '실체의 정의'는 λόγος τῆς οὐσίας의 번역이다. 여기서 οὐσία는
> 범주론 제5장의 기술적 용법이 아니라, 일상적인 '본성'에 가까운
> 의미로 이해해야 한다.

> ² 아리스토텔레스가 범주론을 동음이의 논의로 시작하는 이유에
> 대해서는 학자들 사이에 논쟁이 있다.
```

각주 본문은 강의록과 동일하게 참조 단락 바로 아래 블록인용(`>`)으로 배치한다. `.tex` 변환 시 `\footnote{내용}`으로 변환한다.

### 원어 병기

번역본 본문에서 그리스어(또는 라틴어·아랍어 음차) 원어는 괄호 안에 병기한다.

```markdown
실체(οὐσία)는 가장 으뜸되고 첫째가며 주로 말해지는 뜻에서, ...
```

`.tex`에서 `\gr{}` 또는 `\gri{}`로 변환된다.

**원칙**: 기술 용어의 첫 등장 시에만 원어를 병기하고, 이후에는 한국어만 사용한다. 단, 동일 단어가 다른 의미로 사용되는 경우(예: ὑποκείμενον이 '기체'와 '주어'로 다르게 쓰이는 경우)에는 의미 전환 시점에서 다시 원어를 병기하고 각주를 단다.

### 장·절 구분

원전의 장(chapter) 구분: `##` (H2) → `.tex`에서 `\section*`
절 내부 의미 단락 구분 (필요 시): `###` (H3) → `.tex`에서 `\subsection*`

번역본에는 목차를 두지 않으므로 별표(`*`) 형식을 사용한다.

---

## .tex 변환 규칙

### 표제 블록 — 3요소 배치

표제 블록은 `\translationtitle` 매크로 대신, 좌·중앙·우 3요소 배치를 직접 구성한다. 한국어를 넣지 않는다.

**좌측**: 원어 저자명 + 원어 저작명 (그리스어는 비이탤릭)
**중앙**: 분량 (Bekker 범위, 장·절 범위, 권수 등)
**우측**: 라틴어(또는 영어 음차) 저자명 + 제목 (이탤릭)

```latex
{% — 표제 블록: 좌 원어 / 중앙 분량 / 우 라틴어 —
\par\medskip
\begingroup
\setstretch{1.0}%
\fontsize{14pt}{16pt}\selectfont\bfseries\color{h1navy}%
\noindent
\begin{minipage}[t]{0.45\linewidth}
\raggedright
저자 원어\\
저작 원어
\end{minipage}%
\hfill
\begin{minipage}[t]{0.1\linewidth}
\centering
\vspace{0pt}%
분량
\end{minipage}%
\hfill
\begin{minipage}[t]{0.45\linewidth}
\raggedleft
\gri{저자 라틴어}\\
\gri{저작 라틴어}
\end{minipage}%
\par
\endgroup
\vspace{4pt}%
{\color{rulecolor}\hrule height 0.4pt}%
\vspace{8pt}%
}
```

그리스어 저술 예:

```latex
{% — 표제 블록 —
\par\medskip
\begingroup
\setstretch{1.0}%
\fontsize{14pt}{16pt}\selectfont\bfseries\color{h1navy}%
\noindent
\begin{minipage}[t]{0.45\linewidth}
\raggedright
Ἀριστοτέλης\\
Κατηγορίαι
\end{minipage}%
\hfill
\begin{minipage}[t]{0.1\linewidth}
\centering
\vspace{0pt}%
1a1--4a21
\end{minipage}%
\hfill
\begin{minipage}[t]{0.45\linewidth}
\raggedleft
\gri{Aristotle}\\
\gri{Categoriae}
\end{minipage}%
\par
\endgroup
\vspace{4pt}%
{\color{rulecolor}\hrule height 0.4pt}%
\vspace{8pt}%
}
```

### 페이지 헤더 — 2줄, 분량 없음

매 페이지 상단 헤더는 **2줄**로 구성한다. 저자명을 첫째 줄, 저작명을 둘째 줄에 놓는다. **분량(권수, Bekker 범위 등)은 헤더에 표시하지 않는다.**

좌측 헤더: 원어 (그리스어는 비이탤릭)
우측 헤더: 라틴어 또는 영어 음차 (이탤릭)

```latex
\fancyhead[L]{\footnotesize\color{midgray}\shortstack[l]{Ἀριστοτέλης\\Κατηγορίαι}}
\fancyhead[R]{\footnotesize\color{midgray}\shortstack[r]{\gri{Aristotle}\\\gri{Categoriae}}}
```

라틴어 저술 예:

```latex
\fancyhead[L]{\footnotesize\color{midgray}\shortstack[l]{Thomas Aquinas\\\gri{Summa Theologiae}}}
\fancyhead[R]{\footnotesize\color{midgray}\shortstack[r]{Thomas Aquinas\\\gri{Summa Theologiae}}}
```

### 여백 참조 번호 — 버건디 색상

`translation.sty`의 기본 `\margref` 색상(midgray)을 **버건디(h2burgundy)**로 재정의한다. `\usepackage{translation}` 직후에 아래 한 줄을 추가한다.

```latex
\usepackage{translation}
% 절 번호 색상을 버건디로 변경
\renewcommand*{\marginfont}{\footnotesize\color{h2burgundy}\sffamily}
```

### 프리앰블 구조 (전체 예시)

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper]{article}
\usepackage{master}
\usepackage{translation}
% 절 번호 색상을 버건디로 변경
\renewcommand*{\marginfont}{\footnotesize\color{h2burgundy}\sffamily}
%
% master.sty가 이미 로드한 패키지 중복 선언 금지
% tikz 불필요 — 번역본에는 도식을 넣지 않는다

% 이 문서에서 쓰는 저술만 정의
\DeclareWorkGR{Cat}{범주론}{Κατηγορίαι}{Categoriae}

% 헤더: 2줄 (저자 / 제목), 분량 없음
\fancyhead[L]{\footnotesize\color{midgray}\shortstack[l]{Ἀριστοτέλης\\Κατηγορίαι}}
\fancyhead[R]{\footnotesize\color{midgray}\shortstack[r]{\gri{Aristotle}\\\gri{Categoriae}}}

\begin{document}
\thispagestyle{firstpage}

{% — 표제 블록: 좌 원어 / 중앙 분량 / 우 라틴어 —
\par\medskip
\begingroup
\setstretch{1.0}%
\fontsize{14pt}{16pt}\selectfont\bfseries\color{h1navy}%
\noindent
\begin{minipage}[t]{0.45\linewidth}
\raggedright
Ἀριστοτέλης\\
Κατηγορίαι
\end{minipage}%
\hfill
\begin{minipage}[t]{0.1\linewidth}
\centering
\vspace{0pt}%
1a1--4a21
\end{minipage}%
\hfill
\begin{minipage}[t]{0.45\linewidth}
\raggedleft
\gri{Aristotle}\\
\gri{Categoriae}
\end{minipage}%
\par
\endgroup
\vspace{4pt}%
{\color{rulecolor}\hrule height 0.4pt}%
\vspace{8pt}%
}

\section*{제1장}

\margref{1a1}본문 시작...\footnote{각주 내용}

\end{document}
```

### 마크다운 → .tex 변환 대응표

| 마크다운 | .tex |
|----------|------|
| `[1a1]` | `\margref{1a1}` |
| `¹` + 블록인용 | `\footnote{내용}` |
| `## 제N장` | `\section*{제N장}` |
| `### 소제목` | `\subsection*{소제목}` |
| 괄호 안 그리스어 | `\gr{원어}` |
| 이탤릭 문헌 제목 | `\gri{제목}` |

### 강의록 전용 환경 — 번역본에서 사용하지 않는 것들

`\translationtitle` (v1_3부터 직접 구성으로 대체), `\bilingualquote`, `\srcquote`, `\weeksection`, `concepttable`, tikz 관련 모든 환경.

---

## LuaTeX-ja 줄바꿈 규칙

공통 규칙과 동일. `style_guide v4_0`의 해당 절 참조.

---

## `\citework` 뒤 조사 처리 규칙

공통 규칙과 동일. `style_guide v4_0`의 해당 절 참조.

---

## 인용 원칙

시카고 스타일 (Notes-Bibliography). 2차 문헌 인용은 각주(`\footnote`)에 넣는다. 2차 문헌은 영어권 자료 또는 원어 편집본·주석만 참조한다. 본문이나 각주에서 특정 학자의 견해를 언급할 때는 반드시 각주에 정확한 서지 정보를 표기한다. 영어 번역본이 존재하는 원전은 참고문헌 목록에서 편집본과 번역본 정보를 함께 표기한다 (공통 규칙 `style_guide v4_0` 참조).

---

## 크로스체크 원칙

강의록과 동일. 행 번호 확신 불가 → `[행 번호 확인 필요]`. 사실 불확실 → `[확인 필요]`. 2차 문헌 페이지 번호 → `[p. 확인 필요]`. 존재하지 않는 논문·저술을 만들어내지 않는다. **초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

---

## 버전 관리

강의록과 동일. 파일명 `name_vX_Y`. 내용 수정은 minor, 구조적 변경은 major, 재컴파일만 `--patch`.

---

## 최종 목적

모든 번역본은 나중에 책으로 엮을 것을 전제로 한다. 참조 번호, 각주, 인용 출처 표기를 처음부터 일관되게 관리한다.
