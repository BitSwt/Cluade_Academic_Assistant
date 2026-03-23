#!/usr/bin/env bash
# setup.sh v2_0 — 세션 시작 시 빌드 환경 자동 세팅
set -euo pipefail

REPO="github.com/BitSwt/Cluade_Academic_Assistant.git"
FONT_DIR="/usr/local/share/fonts"
PROJECT_DIR="/home/claude/project"
CLONE_DIR="/tmp/claude-repo"
OUTPUT_DIR="/mnt/user-data/outputs"
MAX_RETRIES=3

log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die()  { log "FATAL: $*" >&2; exit 1; }
ok()   { log "  ✓ $*"; }

echo "=================================================="
echo "  Claude 빌드 환경 세팅 v2_0"
echo "=================================================="

FORCE="${1:-}"
CLONE_HASH=""
if [[ -d "$CLONE_DIR/.git" ]]; then
    CLONE_HASH=$(cd "$CLONE_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "")
fi
SAVED_HASH=""
if [[ -f "$PROJECT_DIR/.bootstrapped" ]]; then
    SAVED_HASH=$(cat "$PROJECT_DIR/.bootstrapped")
fi

if [[ -f "$PROJECT_DIR/.bootstrapped" ]] && [[ "$FORCE" != "--force" ]]; then
    if [[ -n "$CLONE_HASH" ]] && [[ "$SAVED_HASH" != "$CLONE_HASH" ]]; then
        log "레포 업데이트 감지 ($SAVED_HASH → $CLONE_HASH). 재세팅합니다."
    else
        ok "이미 세팅됨. 재세팅: bash setup.sh --force"; exit 0
    fi
fi

log "[1/5] 저장소 클론…"
if [[ ! -d "$CLONE_DIR/.git" ]]; then
    rm -rf "$CLONE_DIR"
    if [[ -n "${GITHUB_PAT:-}" ]]; then
        printf '#!/bin/sh\nexec printf "%%s" "$GITHUB_PAT"\n' > /tmp/askpass.sh
        chmod +x /tmp/askpass.sh; export GIT_ASKPASS=/tmp/askpass.sh
    fi
    for i in $(seq 1 "$MAX_RETRIES"); do
        git clone --depth 1 "https://${REPO}" "$CLONE_DIR" 2>&1 && break
        [[ $i -lt $MAX_RETRIES ]] || die "클론 실패"
        sleep 5
    done
    rm -f /tmp/askpass.sh; unset GIT_ASKPASS GITHUB_PAT 2>/dev/null || true
else
    cd "$CLONE_DIR" && git pull 2>&1 | tail -1
fi
ok "레포 준비 완료"

# build_v2_0 또는 build_v1_9 확인
BUILD_SRC="$CLONE_DIR/shared/build_v2_0.py"
[[ -f "$BUILD_SRC" ]] || BUILD_SRC="$CLONE_DIR/shared/build_v1_9.py"
[[ -f "$BUILD_SRC" ]] || die "build 스크립트 없음"

log "[2/5] 폰트 설치…"
mkdir -p "$FONT_DIR"
cp "$CLONE_DIR/fonts/"*.ttf "$FONT_DIR/"
fc-cache -f "$FONT_DIR"
ok "폰트 완료"

log "[3/5] 의존성…"
kpsewhich luatexja-fontspec.sty > /dev/null 2>&1 \
    && ok "luatexja OK" \
    || { apt-get install -y texlive-lang-cjk texlive-luatex 2>&1 | tail -2; ok "luatexja 설치"; }
python3 -c "import konlpy" > /dev/null 2>&1 \
    && ok "KoNLPy OK" \
    || { pip install konlpy --break-system-packages 2>&1 | tail -2; ok "KoNLPy 설치"; }

log "[4/5] 프로젝트 구성…"
mkdir -p "$PROJECT_DIR" \
         "$OUTPUT_DIR/lecture_pdfs" "$OUTPUT_DIR/lecture_drafts" \
         "$OUTPUT_DIR/translation_pdfs" "$OUTPUT_DIR/translation_drafts"

cp "$CLONE_DIR/shared/master_v1_27.sty"     "$PROJECT_DIR/master.sty"
cp "$CLONE_DIR/shared/translation_v1_3.sty" "$PROJECT_DIR/translation.sty"
cp "$BUILD_SRC"                             "$PROJECT_DIR/build.py"

for f in qa_check.py compliance_check.py md2tex.py insert_tikz.py tex_common.py; do
    [[ -f "$CLONE_DIR/shared/$f" ]] && cp "$CLONE_DIR/shared/$f" "$PROJECT_DIR/$f"
done

# ── 번역본 전용 변환기 ──
[[ -f "$CLONE_DIR/Translation_Academics/md_to_tex.py" ]] \
    && cp "$CLONE_DIR/Translation_Academics/md_to_tex.py" "$PROJECT_DIR/trans_md_to_tex.py"

# ── tikz 도식 파일 ──
if [[ -d "$CLONE_DIR/tikz" ]]; then
    mkdir -p "$PROJECT_DIR/tikz"
    cp "$CLONE_DIR/tikz/"*.tikz "$PROJECT_DIR/tikz/" 2>/dev/null
    ok "tikz/ 디렉터리 배치 ($(ls "$PROJECT_DIR/tikz/"*.tikz 2>/dev/null | wc -l)개)"
fi

cp "$CLONE_DIR/General_Academics/"*.md     "$PROJECT_DIR/" 2>/dev/null || true
cp "$CLONE_DIR/Lecture_Academics/"*.md     "$PROJECT_DIR/" 2>/dev/null || true
cp "$CLONE_DIR/Translation_Academics/"*.md "$PROJECT_DIR/" 2>/dev/null || true

[[ -f "$PROJECT_DIR/versions.json" ]] || echo '{}' > "$PROJECT_DIR/versions.json"
# 커밋 해시 기록 (레포 업데이트 감지용)
CLONE_HASH=$(cd "$CLONE_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "$CLONE_HASH" > "$PROJECT_DIR/.bootstrapped"
ok "구성 완료 (hash: $CLONE_HASH)"

log "[5/5] 검증…"
C=0; P=0
v() { C=$((C+1)); [[ -e "$1" ]] && { P=$((P+1)); ok "$2"; } || log "  ⚠ $2 없음"; }

v "$FONT_DIR/Brill-Roman.ttf"                    "Brill"
v "$FONT_DIR/KoPubWorld_Batang_Medium.ttf"       "KoPub"
v "$PROJECT_DIR/master.sty"                      "master.sty"
v "$PROJECT_DIR/build.py"                        "build.py"
v "$PROJECT_DIR/qa_check.py"                     "qa_check.py"
v "$PROJECT_DIR/compliance_check.py"             "compliance_check.py"
v "$PROJECT_DIR/Basic_rules.md"                  "Basic_rules"
v "$PROJECT_DIR/style_guide_v4_0.md"             "style_guide"

echo ""
echo "=================================================="
echo "  ✓ 세팅 완료 ($P/$C)"
echo "  cd $PROJECT_DIR"
echo ""
echo "  ⚠ 레포 우선 원칙: 문서 작성·변환·빌드·검수는"
echo "    레포의 스크립트와 규칙 문서를 엄격히 따른다."
echo "    즉석 스크립트를 새로 만들지 않는다."
echo ""
echo "  python3 build.py --all --qa    # 전체 빌드+검수"
echo "  python3 build.py --compliance  # 집필 지침 검수"
echo "=================================================="
