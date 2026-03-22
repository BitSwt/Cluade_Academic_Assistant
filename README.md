# Claude Academic Assistant

고전학·서양 철학·수학사·과학사 분야 학술 문서 작성 프레임워크.
LuaLaTeX 기반 한국어·영어·그리스어·라틴어·아랍어(음차) 조판.

## 저장소 구조

```
├── setup.sh                      # 환경 세팅 (인자 없이 실행)
├── fonts/                        # Brill 4종 + KoPub 6종
├── shared/                       # 빌드 도구
│   ├── master_v1_27.sty
│   ├── build_v1_9.py
│   └── translation_v1_3.sty
├── General_Academics/            # 공통 규칙 (모든 문서 유형)
│   ├── Basic_rules.md
│   ├── style_guide_v4_0.md
│   └── ONBOARDING_v4_0.md
├── Lecture_Academics/            # 강의록 전용 규칙
│   ├── lecture_style_guide_v1_0.md
│   └── LECTURE_ONBOARDING_v1_0.md
└── Translation_Academics/        # 번역본 전용 규칙
    ├── translation_style_guide_v1_2.md
    └── TRANSLATION_ONBOARDING_v1_2.md
```

## 세팅

```bash
bash setup.sh    # 전체 규칙 + 빌드 도구 + 폰트 설치
```

## 현재 버전

| 파일 | 버전 |
|------|------|
| `master.sty` | v1_27 |
| `build.py` | v1_9 |
| `translation.sty` | v1_3 |
| `style_guide` | v4_0 |
| `ONBOARDING` | v4_0 |
| `lecture_style_guide` | v1_0 |
| `translation_style_guide` | v1_2 |
