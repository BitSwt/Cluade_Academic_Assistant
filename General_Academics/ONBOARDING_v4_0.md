# 프로젝트 온보딩 가이드
버전: v4_0

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반으로 한국어·영어·그리스어·라틴어·아랍어(음차)를 안정적으로 조판한다.

---

## 버전 이력

**v4_0** (현재): `ONBOARDING v3_11`에서 공통 규칙만 분리. 강의록 전용 내용은 `LECTURE_ONBOARDING v1_0`으로, 번역본 전용 내용은 `TRANSLATION_ONBOARDING v1_2`로 이동.

---

## 세팅

```bash
bash setup.sh
```

세팅 시 자동 수행되는 작업: 폰트 설치(Brill + KoPub 바탕체), luatexja 패키지 확인, KoNLPy 설치, `master.sty` + `translation.sty` + `build.py`를 프로젝트 디렉터리에 배치, 공통·강의록·번역본 규칙 문서 전체 복사.

**폰트가 설치되지 않으면 어떤 컴파일도 시작하지 않는다.** KoNLPy가 설치되지 않아도 컴파일을 중단한다.

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

## 주요 LaTeX 명령어 (공통)

| 명령어 | 용도 |
|--------|------|
| `\gr{...}` | 그리스어 (비이탤릭 원칙) |
| `\gri{...}` | 그리스어·한국어 제외 모든 언어 문헌 제목 (이탤릭) |
| `\grb{...}` | 볼드 원어 (표 헤딩 등) |
| `\citework{id}{라인번호}` | 저술 인용 — 첫 등장: 원어 전체 병기, 이후: 한국어만 |
| `\usework{id}` | 본문 수동 소개 후 플래그 설정 (출력 없음) |
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
| `rulecolor` | 구분선 · 수평선 |
| `midgray` | 각주 번호 · 푸터 |
| `tableheadbg` | 표 헤더 배경 (연회색, 대안) |
| `citebg` | 인용 블록 배경 |
| `altrowbg` | zebra 격행 강조 |
| `reviewbg` | 강조 행 |
| `tableheadblue` | 표 헤더 행 배경 연한 하늘색 |

---

## LuaTeX-ja 줄바꿈 규칙

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

**원칙**: `.tex` 파일에서 문장 내부의 줄바꿈은 쉼표·마침표 뒤에서만 허용한다.

---

## `\citework` 뒤 조사 처리 규칙

`\citework{id}{}`가 출력하는 한국어 텍스트 바로 뒤에 조사가 오면 `xkanjiskip`이 공백을 삽입하여 "범주론 은"처럼 분리된다.

```latex
% ❌ "범주론 은 항"으로 출력됨
\citework{Cat}{}은 항(terms)을 다룬다.

% ✅ 이미 소개된 저술은 한국어를 직접 쓴다
범주론은 항(terms)을 다룬다.
```

---

## 조사 검사 (`check_particles.py`)

`build.py`는 컴파일 전에 대응하는 `.md` 파일이 있으면 자동으로 조사 검사를 실행한다. KoNLPy가 설치되어 있지 않으면 컴파일을 중단한다.

**세션 시작 시 필수 설치:**
```bash
pip install konlpy --break-system-packages
```
`setup.sh`를 실행하면 자동으로 설치된다.

---

## 크로스체크 원칙

### 1차 — 작성 중 표기

행 번호(Bekker·Stephanus 등) 확신 불가 → `[행 번호 확인 필요]` 표시.
인명·연도·저술 제목 등 사실 정보 불확실 → `[확인 필요]` 표시.
2차 문헌 페이지 번호 생성 불가 → `[p. 확인 필요]` 표시.
서지 정보 미제공 → `[서지 정보 확인 필요]` 표시.
존재하지 않는 논문·저술을 만들어내지 않는다.

**마크다운 초안 말미에 항상 "확인이 필요한 항목" 목록을 제시한다.**

### 2차 — 완성 후 전수 검토

.tex 작성 완료 후, build.py 컴파일 전에 문서 전체를 전수 검토한다. 내용(논증·해석 정확성), 각주(행 번호·2차 문헌 참조·번호 순서), 참고문헌(시카고 스타일·누락/초과), 원어(철자·악센트·병기 일관성), 서식(조사 처리·줄바꿈·needspace)을 점검하고 "2차 크로스체크 결과" 블록으로 보고한다. 상세 규칙은 `style_guide v4_0` 참조.

`build.py`는 컴파일 후 자동으로 각주 번호 불일치·텍스트 랩 충돌·`Overfull \hbox`·이미지/표 페이지 초과를 감지하고, 경고가 발생하면 PDF 저장 전에 멈추고 처리 여부를 확인한다.

---

## 스타일 업데이트 시

`master.sty` 수정 → `python3 build.py --bump-sty` → 프로젝트 지식의 파일을 새 버전으로 교체.
