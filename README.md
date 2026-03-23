# Claude Academic Assistant

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반. 강의록·번역본 제작을 지원한다.

## 빠른 시작

```bash
bash setup.sh                          # 환경 세팅 (최초 1회)
cd /home/claude/project
python3 build.py --all --qa            # 전체 빌드 + 검수
```

## 구조

```
setup.sh                               세션 초기화 (v2_0)

shared/                                 빌드 파이프라인
  build_v2_0.py                         빌드 + 버전관리 + QA 통합
  qa_check.py                           PDF 품질 검수 (7항목)
  compliance_check.py                   집필 지침 준수 검수 (12항목)
  tex_common.py                         md→tex 공통 유틸리티
  md2tex.py                             강의록 마크다운 → LaTeX
  insert_tikz.py                        tikz 도식 삽입 (마커/자동매칭)
  master_v1_27.sty                      공통 LaTeX 스타일
  translation_v1_3.sty                  번역본 LaTeX 스타일

tikz/                                   tikz 도식 파일 (.tikz)

General_Academics/                      공통 규칙
  Basic_rules.md                        역할·언어·레포 우선 원칙
  ONBOARDING_v4_0.md                    공통 온보딩
  style_guide_v4_0.md                   공통 작성 규칙

Lecture_Academics/                      강의록 전용
  LECTURE_ONBOARDING_v1_0.md            강의록 온보딩
  lecture_style_guide_v1_1.md           강의록 작성 규칙

Translation_Academics/                  번역본 전용
  TRANSLATION_ONBOARDING_v1_3.md        번역본 온보딩
  translation_style_guide_v1_3.md       번역본 작성 규칙
  md_to_tex.py                          번역본 마크다운 → LaTeX

fonts/                                  Brill 4종 + KoPub 6종
```

## 사용법

### 강의록

```bash
python3 md2tex.py draft.md                      # md → tex
python3 insert_tikz.py draft.tex                # tikz 삽입
python3 build.py draft.tex --qa                 # 빌드 + 검수
python3 build.py --all --qa                     # 전체 배치
```

### 번역본

```bash
python3 trans_md_to_tex.py input.md output.tex  # md → tex
python3 build.py output.tex --qa                # 빌드 + 검수
```

### 검수만

```bash
python3 build.py --qa-only                      # PDF 품질
python3 build.py --compliance                   # 집필 지침
```

## 레포 우선 원칙

모든 문서 작성·변환·빌드·검수는 이 레포의 스크립트와 규칙 문서를
엄격히 따른다. 즉석 스크립트를 새로 만들지 않는다.
