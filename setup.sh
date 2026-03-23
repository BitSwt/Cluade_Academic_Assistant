#!/usr/bin/env bash
# setup.sh v2_1 — 세션 시작 시 빌드 환경 자동 세팅
set -euo pipefail

REPO="github.com/BitSwt/Cluade_Academic_Assistant.git"
FONT_DIR="/usr/local/share/fonts"
PROJECT_DIR="/home/claude/project"
CLONE_DIR="/tmp/claude-repo"
MAX_RETRIES=3

log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die()  { log "FATAL: $*" >&2; exit 1; }
ok()   { log "  ✓ $*"; }

echo "=================================================="
echo "  Claude 빌드 환경 세팅 v2_1"
echo "=================================================="

FORCE="${1:-}"
SAVED_HASH=""
[[ -f "$PROJECT_DIR/.bootstrapped" ]] && SAVED_HASH=$(cat "$PROJECT_DIR/.bootstrapped")

if [[ -f "$PROJECT_DIR/.bootstrapped" ]] && [[ "$FORCE" != "--force" ]]; then
    ok "이미 세팅됨. 재세팅: bash setup.sh --force"; exit 0
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

CLONE_HASH=$(cd "$CLONE_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
if [[ "$SAVED_HASH" == "$CLONE_HASH" ]] && [[ "$FORCE" != "--force" ]]; then
    ok "레포 변경 없음 (hash: $CLONE_HASH)"; exit 0
fi
ok "레포 준비 (hash: $CLONE_HASH)"

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
mkdir -p "$PROJECT_DIR/output"

# sty — 와일드카드로 최신 버전 자동 감지
MASTER_STY=$(ls -t "$CLONE_DIR/shared/master_v"*.sty 2>/dev/null | head -1)
TRANS_STY=$(ls -t "$CLONE_DIR/shared/translation_v"*.sty 2>/dev/null | head -1)
[[ -n "$MASTER_STY" ]] && cp "$MASTER_STY" "$PROJECT_DIR/master.sty" || die "master.sty 없음"
[[ -n "$TRANS_STY" ]]  && cp "$TRANS_STY"  "$PROJECT_DIR/translation.sty" || die "translation.sty 없음"
ok "sty: $(basename "$MASTER_STY"), $(basename "$TRANS_STY")"

# build — 최신 버전 자동 감지
BUILD_SRC=$(ls -t "$CLONE_DIR/shared/build_v"*.py 2>/dev/null | head -1)
[[ -n "$BUILD_SRC" ]] && cp "$BUILD_SRC" "$PROJECT_DIR/build.py" || die "build.py 없음"
ok "build: $(basename "$BUILD_SRC")"

# 보조 스크립트
for f in qa_check.py compliance_check.py md2tex.py insert_tikz.py tex_common.py; do
    [[ -f "$CLONE_DIR/shared/$f" ]] && cp "$CLONE_DIR/shared/$f" "$PROJECT_DIR/$f"
done

# 번역본 변환기
[[ -f "$CLONE_DIR/Translation_Academics/md_to_tex.py" ]] \
    && cp "$CLONE_DIR/Translation_Academics/md_to_tex.py" "$PROJECT_DIR/trans_md_to_tex.py"

# tikz
if [[ -d "$CLONE_DIR/tikz" ]]; then
    mkdir -p "$PROJECT_DIR/tikz"
    cp "$CLONE_DIR/tikz/"*.tikz "$PROJECT_DIR/tikz/" 2>/dev/null || true
fi

# 규칙 문서
cp "$CLONE_DIR/General_Academics/"*.md     "$PROJECT_DIR/" 2>/dev/null || true
cp "$CLONE_DIR/Lecture_Academics/"*.md     "$PROJECT_DIR/" 2>/dev/null || true
cp "$CLONE_DIR/Translation_Academics/"*.md "$PROJECT_DIR/" 2>/dev/null || true

[[ -f "$PROJECT_DIR/versions.json" ]] || echo '{}' > "$PROJECT_DIR/versions.json"
echo "$CLONE_HASH" > "$PROJECT_DIR/.bootstrapped"
ok "구성 완료"

log "[5/5] 검증…"
C=0; P=0
v() { C=$((C+1)); [[ -e "$1" ]] && { P=$((P+1)); ok "$2"; } || log "  ⚠ $2 없음"; }

v "$FONT_DIR/Brill-Roman.ttf"            "Brill"
v "$FONT_DIR/KoPubWorld_Batang_Medium.ttf" "KoPub"
v "$PROJECT_DIR/master.sty"              "master.sty"
v "$PROJECT_DIR/translation.sty"         "translation.sty"
v "$PROJECT_DIR/build.py"                "build.py"
v "$PROJECT_DIR/qa_check.py"             "qa_check.py"
v "$PROJECT_DIR/compliance_check.py"     "compliance_check.py"
v "$PROJECT_DIR/md2tex.py"               "md2tex.py"
v "$PROJECT_DIR/insert_tikz.py"          "insert_tikz.py"
v "$PROJECT_DIR/tex_common.py"           "tex_common.py"
v "$PROJECT_DIR/trans_md_to_tex.py"      "trans_md_to_tex.py"
v "$PROJECT_DIR/Basic_rules.md"          "Basic_rules"
v "$PROJECT_DIR/style_guide_v4_0.md"     "style_guide"

LSG=$(ls "$PROJECT_DIR/lecture_style_guide_v"*.md 2>/dev/null | head -1)
[[ -n "$LSG" ]] && v "$LSG" "$(basename "$LSG")" || { C=$((C+1)); log "  ⚠ lecture_style_guide 없음"; }

TSG=$(ls "$PROJECT_DIR/translation_style_guide_v"*.md 2>/dev/null | head -1)
[[ -n "$TSG" ]] && v "$TSG" "$(basename "$TSG")" || { C=$((C+1)); log "  ⚠ translation_style_guide 없음"; }

TIKZ_N=$(ls "$PROJECT_DIR/tikz/"*.tikz 2>/dev/null | wc -l)
[[ "$TIKZ_N" -gt 0 ]] && { C=$((C+1)); P=$((P+1)); ok "tikz/ ($TIKZ_N개)"; } || { C=$((C+1)); log "  ⚠ tikz/ 비어있음"; }

echo ""
echo "=================================================="
echo "  ✓ 세팅 완료 ($P/$C) — hash: $CLONE_HASH"
echo "  cd $PROJECT_DIR"
echo ""
echo "  ⚠ 레포 우선 원칙: 문서 작성·변환·빌드·검수는"
echo "    레포의 스크립트와 규칙 문서를 엄격히 따른다."
echo "    즉석 스크립트를 새로 만들지 않는다."
echo ""
echo "  python3 build.py --all --qa    # 전체 빌드+검수"
echo "  python3 build.py --compliance  # 집필 지침 검수"
echo "=================================================="
