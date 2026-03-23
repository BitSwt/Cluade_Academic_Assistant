# 공통 문서 작성 규칙 및 서식
버전: v4_0

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성에 공통으로 적용하는 규칙.
강의록과 번역본 모두 이 문서의 규칙을 기반으로 하며, 각 유형의 전용 규칙은 별도 문서에서 다룬다.

---

## 버전 이력

**v4_0** (현재): `document_style_guide v3_11`에서 공통 규칙만 분리. 강의록 전용 규칙(`\weeksection`, 시각화 검토, `\bilingualquote`/`\srcquote`, tikz 도식, `wrapfig`, `concepttable`)은 `lecture_style_guide v1_1`으로 이동.

---

## 기술 환경

엔진은 LuaLaTeX. `master.sty` 하나로 모든 서식이 자동 적용된다.

`master.sty`가 로드하는 패키지(중복 선언 금지): `luatexja-fontspec` · `etoolbox` · `geometry` · `setspace` · `booktabs` · `array` · `multirow` · `colortbl` · `xcolor` · `fancyhdr` · `microtype` · `titlesec`(nobottomtitles*) · `hyperref` · `graphicx` · `wrapfig` · `needspace` · `caption` · `footmisc` · `longtable` · `tabulary`

---

## 페이지 및 서식

A4, 마진 상하 28mm·좌우 35mm. textwidth ≈ 140mm.

**폰트**: 한국어·한자는 KoPub 바탕체, 영어·라틴어·그리스어·숫자는 Brill. 본문 12pt / 주석 10pt / 본문 줄 간격 1.5.

**xkanjiskip**: `master.sty v1_25`부터 전역 설정(0.25em). KoPub↔Brill 폰트 경계 자동 간격 삽입. 별도 선언 불필요.

**nobottomtitles***: 헤딩 뒤 본문 공간이 부족하면 헤딩을 다음 페이지로 자동 이동. **단, `longtable`·`tabulary` 앞에는 `\needspace`를 헤딩 바로 앞에 추가해야 한다.**

**헤딩**: 좌측 정렬. section은 17pt 네이비 + 하단 구분선, subsection은 14pt 버건디, subsubsection은 12pt 초록.

---

## 헤딩과 표의 페이지 분리 방지

`nobottomtitles*`는 텍스트 단락 앞 헤딩만 보호한다. 표는 별도로 처리해야 한다.

```latex
% 표 앞 소제목에 \needspace 추가 (헤딩 바로 앞에 배치)
\needspace{8\baselineskip}   % 짧은 표
\needspace{12\baselineskip}  % 긴 표
\subsection{소제목}
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
| `citebg` | 인용 블록 배경 | RGB 250,250,247 |
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

## 마크다운 초안의 각주 배치 규칙

마크다운 초안에서 각주는 **참조된 단락 바로 아래**에 블록인용(`>`) 형식으로 배치한다. `.tex` 변환 시 `\footnote{}`으로 변환한다.

```markdown
본문 단락.¹

> ¹ 각주 내용. 참조 단락 바로 아래 블록인용으로 배치한다.

다음 단락.
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

## 참고문헌

`\subsubsection*{참고문헌}`(H3, 12pt 초록) + `\begin{references}` + `\refitem`. 시카고 스타일.

---

## 인용 원칙

시카고 스타일 (Notes-Bibliography).

### 1차 문헌 (원전)

학술 표준 편집본의 원문을 사용한다. 그리스어 원문은 OCT(Oxford Classical Texts) 또는 Teubner판을 기본으로 하며, 해당 저작의 학술 표준이 다를 경우 그 편집본을 따른다. 원전 인용 시 학술 표준 편집본의 권·장·절·행 번호를 반드시 표기한다. Bekker(아리스토텔레스), Stephanus(플라톤), Diels–Kranz(소크라테스 이전), Busse(고대 주석가) 등 저작에 따른 표준 참조 체계를 사용한다.

### 2차 문헌

**언어 제한**: 2차 문헌은 영어권 자료 또는 원어(그리스어·라틴어) 편집본·주석만 참조한다. 한국어·일본어·프랑스어·독일어 등 비영어권 2차 문헌은 사용하지 않는다. 단, 학술 표준 편집본(예: Busse의 CAG, Wimmer의 Theophrastus)이 독일어·프랑스어 서문을 포함하더라도 편집본 자체는 사용 가능하다.

**출처 표기 의무**: 본문이나 각주에서 특정 학자의 견해·논지·해석을 언급하거나 인용할 때는 반드시 각주에 정확한 서지 정보(저자, 저작, 출판 정보, 해당 페이지)를 표기한다. '에크릴에 따르면'이라고 쓰고 출처를 달지 않는 것은 허용하지 않는다. 존재하지 않는 논문이나 저술을 만들어내지 않는다.

**참고문헌 서지 형식**: 영어 번역본이 존재하는 원전의 경우, 참고문헌 목록에서 편집본과 영어 번역본 정보를 함께 표기한다. 예: `Ackrill, J. L. *Aristotle's Categories and De Interpretatione*. Clarendon Aristotle Series. Oxford: Clarendon Press, 1963.` (이것은 번역본이자 주석서이므로 참고문헌에 포함하되, 본문에서 '한국어·영어 번역본'을 언급하는 것과는 구별된다.)

### 강의록에서의 2차 문헌 활용 원칙

강의록에서 2차 문헌은 **적소에만** 활용한다. 강의록의 일차적 목적은 학생이 원전 텍스트를 직접 읽고 이해하도록 돕는 것이므로, 2차 문헌은 다음 경우에만 도입한다:

- 원전의 난해한 구절에 대해 학자들의 해석이 갈리는 경우 (예: 해전 논변의 세 해석)
- 원전의 역사적 맥락이나 수용사를 보충할 때
- 특정 해석이 왜 유력한지를 학생에게 보여줄 때

2차 문헌의 견해를 나열하는 것이 강의록의 본문을 지배해서는 안 된다. 본문은 원전 텍스트의 논증 구조와 개념 분석에 집중하고, 2차 문헌은 각주에서 보조적으로 활용한다.

---

## 크로스체크 원칙

### 1차 크로스체크 — 작성 중 표기

작성 과정에서 확신할 수 없는 정보는 즉시 표기한다.

행 번호(Bekker·Stephanus 등) 확신 불가 → `[행 번호 확인 필요]`.
인명·연도·저술 제목 등 사실 정보 불확실 → `[확인 필요]`.
2차 문헌 페이지 번호 생성 불가 → `[p. 확인 필요]`.
서지 정보 미제공 → `[서지 정보 확인 필요]`.
존재하지 않는 논문·저술을 만들어내지 않는다.

**마크다운 초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

**"확인이 필요한 항목"은 마크다운 단계에서 리서치를 통해 전부 해소한다.** `.tex` 변환 전에 모든 `[확인 필요]`, `[p. 확인 필요]`, `[서지 정보 확인 필요]` 마커가 해소되어야 한다. PDF에 "확인이 필요한 항목" 헤딩이나 미해소 마커가 남아서는 안 된다.

### 2차 크로스체크 — 완성 후 전수 검토

.tex 작성 완료 후, build.py 컴파일 전에 문서 전체를 대상으로 아래 항목을 전수 검토한다. 강의록과 번역본 모두 동일하게 적용한다.

**내용 검토**: 서술된 철학적 논증이나 텍스트 해석에 사실 오류가 없는지 확인한다. 원전의 논지를 정확히 반영하는지, 설명의 논리적 흐름에 비약이 없는지 점검한다.

**각주 검토**: 모든 각주의 내용이 정확한지 확인한다. 원전 인용의 행 번호가 실제 텍스트 내용과 일치하는지, 2차 문헌 참조가 존재하는 저작의 실제 논지를 반영하는지 점검한다. 각주 번호가 본문의 참조 위치와 순서상 정확히 대응하는지 확인한다.

**참고문헌 검토**: 참고문헌 목록의 모든 항목이 시카고 스타일에 부합하는지 확인한다. 저자명·제목·출판사·연도가 정확한지, 본문이나 각주에서 언급된 문헌이 참고문헌 목록에 빠짐없이 포함되어 있는지, 반대로 본문에서 인용되지 않은 문헌이 목록에 포함되어 있지 않은지 점검한다.

**원어 검토**: 그리스어·라틴어 등 원어 표기에 철자 오류나 악센트 누락이 없는지 확인한다. 언어 병기 원칙(첫 등장 시 원어 병기, 이후 한국어만)이 일관되게 적용되었는지 점검한다.

**서식 검토**: `\citework` 조사 처리, LuaTeX-ja 줄바꿈 규칙, `\needspace` 배치가 규칙에 부합하는지 확인한다.

2차 크로스체크 결과는 "2차 크로스체크 결과" 블록으로 보고한다.

```
[2차 크로스체크 결과]
- 각주 3: 분석론 전서 24b18 → 실제 텍스트 내용과 일치 확인
- 각주 7: Ackrill 1963 p.XX → [p. 확인 필요] 유지
- 참고문헌: Wöhrle 1985 서지 정보 미확인 → [서지 정보 확인 필요] 유지
- 원어: 3장 2절 ὑποκείμενον 악센트 정상
- 서식: \citework{Cat}{}은 → 한국어 직접 입력으로 수정 필요
- 수정 사항 없음 / N건 수정 완료
```

---

## 버전 관리

파일명: `name_vX_Y`. 내용 수정은 minor(기본), 구조적 변경은 major, 재컴파일만 `--patch`. `master.sty` 수정 시 `--bump-sty`.

---

## 최종 목적

모든 문서는 나중에 책으로 엮을 것을 전제로 한다. 인용 출처와 참고문헌 표기를 처음부터 일관되게 관리한다.
