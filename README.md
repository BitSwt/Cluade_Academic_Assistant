# Claude Academic Assistant

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반 한국어·영어·그리스어·라틴어·아랍어(음차) 조판.

## 저장소 구조

```
├── setup.sh                  # 환경 세팅 (--lectures 옵션)
├── fonts/                    # Brill 4종 + KoPub 6종
├── shared/                   # 빌드 도구 (master.sty, build.py)
├── General_Academics/        # 집필 지침 (모든 세션 공통)
└── Lecture_Notes/            # 오르가논 강독 프로젝트
    ├── schedule_42weeks.tex
    ├── md/                   # 마크다운 초안 (35개)
    ├── tex/                  # LaTeX 소스 (빌드 완료분)
    └── pdf/                  # 빌드된 PDF
```

## 세팅

```bash
bash setup.sh              # 일반 문서 작성
bash setup.sh --lectures   # 강의록 작업 (마크다운 초안도 복사)
```

## 현재 버전

| 파일 | 버전 |
|------|------|
| `master.sty` | v1_27 |
| `build.py` | v1_9 |
| `document_style_guide` | v3_11 |
| `ONBOARDING` | v3_11 |
