# 프로젝트 온보딩 가이드
버전: v3_9

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반으로 한국어·영어·그리스어·라틴어·아랍어(음차)를 안정적으로 조판한다.

---

## 버전 이력

**v3_9** (현재): `master.sty v1_25` 변경 사항 반영. LuaTeX-ja 줄바꿈 규칙 추가. `\citework` 조사 처리 규칙 추가. tikz 도식 작업흐름 명시. `nobottomtitles*` + `\needspace` 병용 규칙 추가. `\concepttable` 환경 정의 및 사용법 추가.

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

- `master_vX_Y.sty` — 모든 서식 규칙
- `build_vX_Y.py` — 빌드·버전 관리·렌더링 검증
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

### 새 문서 프리앰블 구조

```latex
% !TEX program = lualatex
\documentclass[12pt, a4paper]{article}
\usepackage{master}
% master.sty v1_25:
%   - xkanjiskip 전역: KoPub↔Brill 폰트 경계 공백 자동 삽입
%   - nobottomtitles*: 헤딩·본문 분리 자동 방지 (단, 도식·표 앞에는
%     \needspace를 헤딩 바로 앞에 추가해야 함 — 아래 규칙 참조)
%   - \concepttable 환경: 개념 정리 표 자동 폭 조정
%   - 중복 패키지 선언 금지

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

## 헤딩과 표·도식의 페이지 분리 방지 규칙

`nobottomtitles*`는 헤딩 뒤에 **텍스트 단락**이 이어질 때만 작동한다. `longtable`, `tabulary`, tikz `figure` 환경은 단락으로 인식되지 않으므로, 이것들 앞에 오는 헤딩은 반드시 `\needspace`를 헤딩 **바로 앞**에 추가해야 한다.

```latex
% ❌ 헤딩만 페이지 하단에 남고 표가 다음 페이지로 넘어감
\subsection{개념 정리}
\begin{concepttable}{...}

% ✅ 헤딩과 표 첫 행이 항상 같은 페이지에서 시작
\needspace{8\baselineskip}
\subsection{개념 정리}
\begin{concepttable}{...}

% ✅ tikz 도식: 소제목 + 본문 단락 + 도식 전체가 한 페이지에 들어가야 할 때
\needspace{20\baselineskip}
\subsection{포르피리오스의 나무}
본문 단락...
\begin{figure}[h!]
```

`\needspace{N\baselineskip}`: N줄만큼의 공간이 없으면 즉시 다음 페이지로 이동. 표나 도식의 예상 높이에 맞게 N을 설정한다. 헤딩(2–3줄) + 표 헤더(1줄) + 데이터 행 첫 번째(2줄) = 최소 8줄. 도식이 포함된 경우 15–22줄.

**모든 `\subsection` 앞에 `\needspace{5\baselineskip}`을 기본으로 추가한다.** 소제목과 그 뒤 첫 문장이 항상 같은 페이지에서 시작하도록 보장한다.

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

**원칙**: 문장 내부의 줄바꿈은 쉼표·마침표 뒤에서만 허용한다.

---

## `\citework` 뒤 조사 처리 규칙

`\citework{id}{}` 출력 직후 조사가 오면 `xkanjiskip`이 공백을 삽입하여 "범주론 은"처럼 분리된다.

```latex
% ❌ "범주론 은 항"으로 출력됨
\citework{Cat}{}은 항(terms)을 다룬다.

% ✅ 이미 소개된 저술은 한국어를 직접 쓴다
범주론은 항(terms)을 다룬다.
```

---

## `\concepttable` 환경

개념 정리 표에 사용한다. `tabulary` 기반으로 전체 폭이 항상 `\linewidth`에 맞춰진다. 열 너비를 mm 단위로 계산할 필요 없다.

**열 타입:**
- `L` — 좌측 정렬, 내용 비례 자동 폭 (긴 텍스트 열에 사용)
- `C` — 가운데 정렬, 내용 비례 자동 폭 (중간 길이 텍스트)
- `c` — 가운데 정렬 고정 (짧은 번호·기호 열에만 사용)

**주의사항:**
- `tabulary`는 페이지를 넘길 수 없다. 표가 한 페이지를 넘길 것 같으면 분리하거나 `longtable`을 사용한다.
- 그리스어가 포함된 열은 `c` 대신 `C`를 사용한다. `c`는 내용 폭을 고정하므로 긴 그리스어 단어가 overflow를 유발할 수 있다.
- 행이 6개 이상이거나 내용이 복잡한 표는 `longtable` + 고정폭 `m{}` 열 조합이 더 안정적이다.

```latex
% 사용 예
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
2 & 제2실체 & 제1실체가 속하는 종·유 & 인간, 동물 \\ \hline
\end{concepttable}
```

---

## tikz 도식 작업흐름

**마크다운 단계에서는 도식을 삽입하지 않는다.** tikz 코드는 `.tex` 작성 단계에서만 삽입한다.

tikz 도식이 포함된 문서의 프리앰블에는 아래를 추가한다.

```latex
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta}
```

tikz 도식 너비는 textwidth ≈ 140mm 이내로 설계한다.

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
| `\bilingualquote{원문}{번역}{출처}` | 더블 칼럼 인용 |
| `\srcquote{원문}{번역}{출처}` | 단독 짧은 인용 |
| `\bqnote{내용}` | `\bilingualquote` 번역란 내 각주 |
| `\needspace{N\baselineskip}` | 표·도식 앞 공간 확보 — 헤딩 바로 앞에 배치 |
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
| `citebg` | 인용 블록 배경 |
| `altrowbg` | zebra 격행 강조 (`rulecolor!12!white`) |
| `reviewbg` | 강조 행 (`black!13!white`) |
| `tableheadblue` | 표 헤더 행 배경 (연한 하늘색, RGB 210,228,245) |

---

## 크로스체크 원칙

행 번호 확신 불가 → `[행 번호 확인 필요]`. 인명·연도·저술 제목 불확실 → `[확인 필요]`. 2차 문헌 페이지 번호 생성 불가 → `[p. 확인 필요]`. 서지 정보 미제공 → `[서지 정보 확인 필요]`. 존재하지 않는 논문·저술을 만들어내지 않는다.

**마크다운 초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

---

## 스타일 업데이트 시

`master.sty` 수정 → `python3 build.py --bump-sty` → 프로젝트 지식의 파일을 새 버전으로 교체. 다음 채팅부터 자동으로 최신 설정이 적용된다.
