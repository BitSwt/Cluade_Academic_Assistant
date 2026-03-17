#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — LuaLaTeX 문서 빌드 및 버전 관리 스크립트
버전: v1_8

사용법:
    python3 build.py <tex파일명>           # minor 버전업 후 컴파일
    python3 build.py <tex파일명> --major   # major 버전업 후 컴파일
    python3 build.py <tex파일명> --patch   # 버전 유지, 재컴파일만
    python3 build.py --list                # 모든 파일의 현재 버전 출력
    python3 build.py --bump-sty            # master.sty 버전업

버전 번호 규칙:
    major.minor 형식 (예: v1_2)
    --major : 구조적 변경, 새 챕터 추가 등 큰 변화
    --minor : 내용 수정, 오탈자 수정 등 작은 변화 (기본값)
    --patch : 버전 번호 변경 없이 재컴파일만 (레이아웃 확인 등)

참고:
    저술 정의(DeclareWorkGR 등)는 각 문서 프리앰블에 직접 포함한다.
    컴파일 시작 전에 필수 폰트(KoPub 바탕체, Brill)
    설치 여부를 자동으로 확인한다. 폰트가 없으면
    컴파일을 중단하고 업로드를 요청한다.

스타일 참조:
    master.sty            — 폰트·색상·표 서식 전역 설정
    document_style_guide  — 표기 원칙 및 서식 규칙 전체
    ONBOARDING            — 프레임워크 사용법 및 명령어 목록
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


# ── 설정 ──────────────────────────────────────────────────────────────────────

# 프로젝트 루트 디렉터리 (이 스크립트가 있는 곳)
PROJECT_DIR = Path(__file__).parent

# 버전 정보를 저장하는 JSON 파일
VERSION_FILE = PROJECT_DIR / "versions.json"

# 컴파일된 PDF를 출력할 디렉터리
OUTPUT_DIR = PROJECT_DIR / "output"

# LuaLaTeX 컴파일 횟수 (cross-reference 안정화를 위해 2회)
COMPILE_PASSES = 2

# ── 폰트 검사 ─────────────────────────────────────────────────────────────────

# 필수 폰트 파일 목록
# 이 파일들이 FONT_DIR에 존재하지 않으면 컴파일을 시작하지 않는다
FONT_DIR = Path("/usr/local/share/fonts")
REQUIRED_FONTS = [
    ("KoPubBatangMedium.ttf", "KoPub 바탕체 (한국어 전용)"),
    ("KoPubBatangBold.ttf",   "KoPub 바탕체 Bold"),
    ("Brill-Roman.ttf",       "Brill (영어·라틴어·그리스어 전용)"),
    ("Brill-Bold.ttf",        "Brill Bold"),
    ("Brill-Italic.ttf",      "Brill Italic"),
    ("Brill-BoldItalic.ttf",  "Brill Bold Italic"),
]

def check_fonts() -> bool:
    """
    필수 폰트 파일이 모두 설치되어 있는지 확인한다.
    누락된 폰트가 있으면 False를 반환하고, 어떤 파일이 필요한지 안내한다.
    모든 폰트가 있으면 True를 반환한다.
    """
    missing = [
        (filename, description)
        for filename, description in REQUIRED_FONTS
        if not (FONT_DIR / filename).exists()
    ]

    if missing:
        print("\n" + "="*60)
        print("  ✗ 필수 폰트가 설치되어 있지 않습니다.")
        print("  컴파일을 시작하기 전에 폰트 파일을 업로드해 주세요.")
        print("="*60)
        print("\n  누락된 폰트:")
        for filename, description in missing:
            print(f"    - {filename}  ({description})")
        print("\n  업로드해야 하는 파일:")
        print("    - KOPUBWORLD_TTF_FONTS-1.zip  (KoPub 바탕체)")
        print("    - The_Brill_Typeface_Package_v_4_0.zip  (Brill)")
        print("\n  업로드 후 폰트를 설치하려면:")
        print("    unzip KOPUBWORLD_TTF_FONTS-1.zip -d /tmp/kopub")
        print("    cp /tmp/kopub/*.ttf /usr/local/share/fonts/")
        print("    unzip The_Brill_Typeface_Package_v_4_0.zip -d /tmp/brill")
        print("    cp /tmp/brill/*.ttf /usr/local/share/fonts/")
        print("    fc-cache -f /usr/local/share/fonts/\n")
        return False

    print("  ✓ 폰트 확인 완료 (KoPub 바탕체, Brill)")
    return True


# ── 버전 관리 ──────────────────────────────────────────────────────────────────

def load_versions() -> dict:
    """versions.json을 읽어 반환. 파일이 없으면 빈 딕셔너리를 반환."""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_versions(versions: dict):
    """버전 정보를 versions.json에 저장."""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(versions, f, ensure_ascii=False, indent=2)
    print(f"  버전 정보 저장: {VERSION_FILE}")


def get_version(versions: dict, key: str) -> tuple[int, int]:
    """
    특정 파일의 현재 버전을 (major, minor) 튜플로 반환.
    처음 등록되는 파일이면 (1, 0)을 반환.
    """
    if key in versions:
        v = versions[key]
        return v["major"], v["minor"]
    return 1, 0


def bump_version(versions: dict, key: str, mode: str) -> tuple[int, int]:
    """
    버전을 올리고 새 버전을 반환.
    
    mode:
        "major" → major+1, minor=0
        "minor" → minor+1
        "patch" → 변경 없음
    """
    major, minor = get_version(versions, key)

    if mode == "major":
        major += 1
        minor = 0
    elif mode == "minor":
        minor += 1
    # "patch"는 버전 변경 없음

    versions[key] = {
        "major": major,
        "minor": minor,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return major, minor


def format_version(major: int, minor: int) -> str:
    """(1, 2) → 'v1_2' 형식으로 반환."""
    return f"v{major}_{minor}"


# ── 렌더링 검증 ────────────────────────────────────────────────────────────────

def check_render(log: str) -> bool:
    """
    컴파일 로그를 분석해서 렌더링 품질 문제를 감지하고 보고한다.

    감지 항목:
      - 각주 번호 불일치 (minipage 내부 알파벳 각주 등)
      - wrapfig/wraptable 충돌 또는 텍스트 랩 이상
      - Overfull \\hbox (텍스트가 박스를 벗어남)

    패키지 로드 줄(.sty 경로 포함)은 경고에서 제외한다.
    문제가 감지되면 해당 항목을 출력하고 True를 반환한다.
    """
    issues = []  # (severity, description, line)

    for line in log.splitlines():
        # 패키지 로드 줄 제외 (.sty, .tex 경로가 포함된 줄)
        if ".sty" in line or line.startswith("(") or line.startswith(")"):
            continue

        # ── 각주 번호 관련 ────────────────────────────────────────────────
        # minipage 내부 \footnote → 알파벳 각주 발생
        if "footnote" in line.lower() and "warn" in line.lower():
            issues.append(("warn", "각주 경고 — 번호 체계 확인 필요", line.strip()))

        # \footnotemark / \footnotetext 쌍 불일치
        if "Missing \\endcsname" in line or "footnote counter" in line.lower():
            issues.append(("error", "각주 번호 불일치 가능성", line.strip()))

        # ── 텍스트 랩 관련 ────────────────────────────────────────────────
        # Overfull \hbox: 텍스트가 column width를 초과
        if line.startswith("Overfull \\hbox"):
            issues.append(("warn",
                "텍스트가 박스를 벗어남 — 텍스트 랩 또는 긴 단어 확인 필요",
                line.strip()))

        # wrapfig가 페이지 경계에서 충돌
        if "wrapfig" in line and ("warning" in line.lower() or "!" in line):
            issues.append(("warn", "wrapfig 경고 — 텍스트 랩 위치 확인 필요",
                line.strip()))

        # Float too large: 이미지/표가 페이지 높이를 초과
        if "Float too large" in line:
            issues.append(("error",
                "이미지/표가 페이지에 비해 너무 큼 — 크기 조정 필요",
                line.strip()))

        # ── 레이아웃 참고 ─────────────────────────────────────────────────
        if line.startswith("Underfull \\vbox"):
            issues.append(("info",
                "페이지 하단 여백이 큼 — 필요 시 \\needspace 조정",
                line.strip()))

    if not issues:
        print("  ✓ 렌더링 검증 통과 (각주·텍스트 랩 이상 없음)")
        return False

    errors = [(d, l) for s, d, l in issues if s == "error"]
    warns  = [(d, l) for s, d, l in issues if s == "warn"]
    infos  = [(d, l) for s, d, l in issues if s == "info"]

    print("\n  ── 렌더링 검증 결과 ────────────────────────────────")

    if errors:
        print(f"\n  ✗ 오류 ({len(errors)}건) — PDF를 반드시 확인하세요:")
        for desc, line in errors:
            print(f"    [{desc}]")
            print(f"      {line[:120]}")

    if warns:
        print(f"\n  ⚠️  경고 ({len(warns)}건) — PDF에서 해당 부분을 확인하세요:")
        for desc, line in warns:
            print(f"    [{desc}]")
            print(f"      {line[:120]}")

    if infos:
        print(f"\n  ℹ️  참고 ({len(infos)}건):")
        for desc, line in infos:
            print(f"    [{desc}]")

    print()
    return bool(errors or warns)


# ── 컴파일 ─────────────────────────────────────────────────────────────────────

def compile_document(tex_path: Path, version_str: str) -> bool:
    """
    LuaLaTeX로 문서를 컴파일하고, 성공하면 PDF를 output/ 디렉터리에
    버전 번호를 포함한 이름으로 복사한다.

    cross-reference(상호 참조)가 안정화되도록 COMPILE_PASSES 횟수만큼 반복.
    """
    tex_dir = tex_path.parent
    tex_name = tex_path.name
    stem = tex_path.stem  # 확장자 없는 파일명

    print(f"\n{'='*60}")
    print(f"  컴파일: {tex_name}  ({version_str})")
    print(f"{'='*60}")

    for i in range(1, COMPILE_PASSES + 1):
        print(f"\n  [{i}/{COMPILE_PASSES}회] lualatex 실행 중...")
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", tex_name],
            cwd=tex_dir,
            capture_output=True,
            text=True,
        )

        # 컴파일 오류 확인 (! 로 시작하는 줄)
        errors = [
            line for line in result.stdout.splitlines()
            if line.startswith("!")
        ]
        if errors:
            print("\n  ⚠️  LaTeX 오류 발생:")
            for err in errors:
                print(f"    {err}")
            # PDF가 생성된 경우에도 오류 내용을 확인하고 진행 여부를 묻는다
            output_exists = any(
                "Output written" in l for l in result.stdout.splitlines()
            )
            if output_exists:
                print("\n  오류가 있지만 PDF는 생성되었습니다.")
                print("  계속 진행하시겠습니까? (y: 진행 / n: 중단)")
                answer = input("  → ").strip().lower()
                if answer != "y":
                    print("\n  빌드를 중단했습니다.")
                    print("  .tex 파일을 수정한 뒤 다시 빌드하세요.\n")
                    return False

        # 출력 확인
        output_line = next(
            (l for l in result.stdout.splitlines() if "Output written" in l),
            None
        )
        if output_line:
            print(f"  ✓ {output_line.strip()}")
        elif result.returncode != 0:
            print(f"\n  ✗ 컴파일 실패 (return code: {result.returncode})")
            print(result.stdout[-2000:])
            return False

        # 마지막 컴파일 패스에서 렌더링 검증 실행
        # 경고/오류가 있으면 PDF 저장 전에 사용자에게 확인
        if i == COMPILE_PASSES:
            has_issues = check_render(result.stdout)
            if has_issues:
                print("  위 경고/오류를 확인했습니다. 그래도 계속 진행하시겠습니까?")
                print("  계속 진행하려면 y, 중단하려면 n을 입력하세요.")
                answer = input("  → ").strip().lower()
                if answer != "y":
                    print("\n  빌드를 중단했습니다.")
                    print("  .tex 파일을 수정한 뒤 다시 빌드하세요.\n")
                    return False

    # PDF 출력 디렉터리로 복사
    pdf_source = tex_dir / f"{stem}.pdf"
    if not pdf_source.exists():
        print(f"\n  ✗ PDF 파일을 찾을 수 없음: {pdf_source}")
        return False

    OUTPUT_DIR.mkdir(exist_ok=True)

    # PDF 복사: 버전 번호 포함
    pdf_dest = OUTPUT_DIR / f"{stem}_{version_str}.pdf"
    shutil.copy2(pdf_source, pdf_dest)
    print(f"\n  ✓ PDF 출력: {pdf_dest}")

    # TeX 소스도 함께 복사 (버전 추적을 위해)
    tex_dest = OUTPUT_DIR / f"{stem}_{version_str}.tex"
    shutil.copy2(tex_path, tex_dest)
    print(f"  ✓ TEX 출력: {tex_dest}")

    return True


def copy_support_files(versions: dict):
    """
    master.sty를 현재 버전으로 output/ 에 복사.
    문서 파일과 함께 버전이 추적되도록 하기 위함.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    filename = "master.sty"
    src = PROJECT_DIR / filename
    if not src.exists():
        return
    major, minor = get_version(versions, filename)
    version_str = format_version(major, minor)
    dst = OUTPUT_DIR / f"{Path(filename).stem}_{version_str}{Path(filename).suffix}"
    shutil.copy2(src, dst)
    print(f"  ✓ 지원 파일 출력: {dst}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def cmd_list():
    """현재 등록된 모든 파일의 버전 정보를 출력."""
    versions = load_versions()
    if not versions:
        print("  (등록된 버전 정보 없음)")
        return

    print(f"\n{'파일':<35} {'버전':<10} {'최종 수정'}")
    print("-" * 65)
    for key, info in sorted(versions.items()):
        v = format_version(info["major"], info["minor"])
        updated = info.get("last_updated", "-")
        print(f"  {key:<33} {v:<10} {updated}")


def cmd_build(tex_filename: str, mode: str):
    """
    메인 빌드 명령.
    0) 폰트 설치 여부 확인 — 누락 시 즉시 중단
    1) 버전 올리기 (mode에 따라)
    2) LuaLaTeX 컴파일
    3) PDF + TEX 출력 디렉터리로 복사
    """
    # 폰트 검사: 필수 폰트가 없으면 컴파일 시작하지 않음
    if not check_fonts():
        sys.exit(1)

    tex_path = PROJECT_DIR / tex_filename
    if not tex_path.exists():
        # .tex 확장자 없이 입력한 경우 대응
        tex_path = PROJECT_DIR / f"{tex_filename}.tex"
    if not tex_path.exists():
        print(f"  ✗ 파일을 찾을 수 없음: {tex_filename}")
        sys.exit(1)

    versions = load_versions()
    key = tex_path.name

    # 버전 업데이트
    major, minor = bump_version(versions, key, mode)
    version_str = format_version(major, minor)

    if mode == "patch":
        print(f"  버전 유지: {key} → {version_str} (재컴파일만)")
    else:
        print(f"  버전 업: {key} → {version_str} ({mode})")

    # 컴파일
    success = compile_document(tex_path, version_str)
    if not success:
        print("\n  ✗ 빌드 실패. 버전 정보를 저장하지 않습니다.")
        sys.exit(1)

    # 지원 파일 복사 (master.sty)
    copy_support_files(versions)

    # 성공 시 버전 정보 저장
    save_versions(versions)

    print(f"\n  ✓ 빌드 완료: {key} {version_str}")
    print(f"  출력 디렉터리: {OUTPUT_DIR}/\n")


def cmd_bump_support(filename: str):
    """master.sty의 버전을 올린다 (컴파일 없음)."""
    versions = load_versions()
    major, minor = bump_version(versions, filename, "minor")
    version_str = format_version(major, minor)
    save_versions(versions)
    print(f"  ✓ {filename} → {version_str}")


# ── 진입점 ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args[0] == "--list":
        cmd_list()

    elif args[0] == "--bump-sty":
        cmd_bump_support("master.sty")

    else:
        # tex 파일 빌드
        tex_filename = args[0]
        mode = "minor"  # 기본값

        if "--major" in args:
            mode = "major"
        elif "--patch" in args:
            mode = "patch"

        cmd_build(tex_filename, mode)


if __name__ == "__main__":
    main()
