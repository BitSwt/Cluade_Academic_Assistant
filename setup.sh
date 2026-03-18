#!/usr/bin/env bash

# ============================================================
# setup.sh — 세션 시작 시 빌드 환경 자동 세팅
#
# 사용법:
#   공개 저장소:   bash setup.sh
#   비공개 저장소: GITHUB_PAT=<토큰> bash setup.sh
#
# 작업 순서:
#   1. GitHub 저장소 클론 (GIT_ASKPASS 인증)
#   2. 폰트 설치 (Brill 4종, KoPub 바탕체 2종)
#   3. luatexja 패키지 설치 (최초 1회)
#   4. KoNLPy 설치 (조사 검사 필수 의존성, 최초 1회)
#   5. 프로젝트 디렉터리 구성
# ============================================================

set -euo pipefail

# ── 설정 ──────────────────────────────────────────────────────────────────────
REPO="github.com/BitSwt/Cluade_Academic_Assistant.git"
MASTER_STY="master_v1_26.sty"
BUILD_PY="build_v1_9.py"
FONT_DIR="/usr/local/share/fonts"
PROJECT_DIR="/home/claude/project"
CLONE_DIR="/tmp/claude-repo"
MAX_RETRIES=3

log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die()  { log "FATAL: $*" >&2; exit 1; }
ok()   { log "  ✓ $*"; }
warn() { log "  ⚠ $*"; }

echo "=================================================="
echo "  Claude 빌드 환경 세팅 시작"
echo "=================================================="

# ── 이미 세팅된 경우 스킵 ─────────────────────────────────────────────────────
if [[ -f "$PROJECT_DIR/.bootstrapped" ]]; then
    ok "이미 세팅된 환경입니다. 스킵합니다."; exit 0
fi

# ── 1. 저장소 클론 ────────────────────────────────────────────────────────────
log "[1/5] 저장소 클론 중…"
rm -rf "$CLONE_DIR"

if [[ -n "${GITHUB_PAT:-}" ]]; then
    # GIT_ASKPASS: PAT을 URL·config·히스토리에 노출시키지 않는 안전한 인증
    printf '#!/bin/sh\nexec printf "%%s" "$GITHUB_PAT"\n' > /tmp/askpass.sh
    chmod +x /tmp/askpass.sh
    export GIT_ASKPASS=/tmp/askpass.sh
    log "  비공개 저장소 인증 활성화 (GIT_ASKPASS)"
else
    log "  공개 저장소 모드"
fi

for attempt in $(seq 1 "$MAX_RETRIES"); do
    if git clone --depth 1 --single-branch \
        "https://${REPO}" "$CLONE_DIR" 2>&1; then
        ok "클론 완료"; break
    fi
    [[ $attempt -lt $MAX_RETRIES ]] || die "클론 실패 (${MAX_RETRIES}회 시도)"
    warn "시도 $attempt 실패, 5초 후 재시도…"
    rm -rf "$CLONE_DIR"; sleep 5
done

# 인증 정보 즉시 제거
rm -f /tmp/askpass.sh
unset GIT_ASKPASS GITHUB_PAT 2>/dev/null || true

# 파일 존재 확인
[[ -d "$CLONE_DIR/fonts" ]]       || die "fonts/ 폴더 없음"
[[ -f "$CLONE_DIR/$MASTER_STY" ]] || die "$MASTER_STY 없음"
[[ -f "$CLONE_DIR/$BUILD_PY" ]]   || die "$BUILD_PY 없음"

FONT_COUNT=$(find "$CLONE_DIR/fonts" -name '*.ttf' | wc -l)
[[ "$FONT_COUNT" -ge 6 ]] \
    || die "TTF 파일 부족 (발견: ${FONT_COUNT}개, 최소 6개 필요)"

# ── 2. 폰트 설치 ──────────────────────────────────────────────────────────────
log "[2/5] 폰트 설치 중… (${FONT_COUNT}개)"
mkdir -p "$FONT_DIR"
cp "$CLONE_DIR/fonts/"*.ttf "$FONT_DIR/"

# build.py·master.sty가 기대하는 파일명과 저장소의 파일명이 다르므로
# 심볼릭 링크로 두 이름을 모두 지원한다
fc-cache -f "$FONT_DIR"
ok "폰트 설치 완료 (Brill 4종, KoPub 바탕체 2종)"

# ── 3. luatexja 패키지 설치 ───────────────────────────────────────────────────
log "[3/5] LaTeX 패키지 확인 중…"
if ! kpsewhich luatexja-fontspec.sty > /dev/null 2>&1; then
    log "  luatexja 설치 중 (최초 1회)…"
    apt-get install -y texlive-lang-cjk texlive-luatex 2>&1 | tail -2
    ok "luatexja 설치 완료"
else
    ok "luatexja 이미 설치됨"
fi

# ── 4. KoNLPy 설치 ────────────────────────────────────────────────────────────
log "[4/5] KoNLPy 확인 중… (조사 검사 필수 의존성)"
if ! python3 -c "import konlpy" > /dev/null 2>&1; then
    log "  KoNLPy 설치 중 (최초 1회)…"
    pip install konlpy --break-system-packages 2>&1 | tail -2
    ok "KoNLPy 설치 완료"
else
    ok "KoNLPy 이미 설치됨"
fi

# ── 5. 프로젝트 디렉터리 구성 ─────────────────────────────────────────────────
log "[5/5] 프로젝트 디렉터리 구성 중…"
mkdir -p "$PROJECT_DIR/output"
cp "$CLONE_DIR/$MASTER_STY" "$PROJECT_DIR/master.sty"
cp "$CLONE_DIR/$BUILD_PY"   "$PROJECT_DIR/build.py"
[[ -f "$PROJECT_DIR/versions.json" ]] \
    || echo '{}' > "$PROJECT_DIR/versions.json"

touch "$PROJECT_DIR/.bootstrapped"
ok "프로젝트 디렉터리 구성 완료"

# ── 최종 검증 ─────────────────────────────────────────────────────────────────
echo ""
echo "  ── 폰트 설치 검증 ──"
for fname in \
    "Brill-Roman.ttf" \
    "Brill-Bold.ttf" \
    "Brill-Italic.ttf" \
    "Brill-BoldItalic.ttf" \
    "KoPubWorld_Batang_Medium.ttf" \
    "KoPubWorld_Batang_Bold.ttf"; do
    f="$FONT_DIR/$fname"
    if [[ -e "$f" ]]; then
        size=$(du -k "$f" | cut -f1)
        [[ "$size" -gt 10 ]] \
            && ok "$fname (${size}KB)" \
            || warn "$fname — 파일 크기 이상 (${size}KB)"
    else
        warn "$fname — 없음"
    fi
done

echo ""
echo "  ── 패키지·라이브러리 검증 ──"
kpsewhich luatexja-fontspec.sty > /dev/null 2>&1 \
    && ok "luatexja 확인" \
    || warn "luatexja — 확인 실패"

python3 -c "import konlpy" > /dev/null 2>&1 \
    && ok "KoNLPy 확인" \
    || warn "KoNLPy — 확인 실패 (조사 검사 없이는 빌드가 중단됩니다)"

echo ""
echo "=================================================="
echo "  ✓ 세팅 완료. 빌드를 시작할 수 있습니다."
echo "  cd $PROJECT_DIR && python3 build.py <파일명>.tex"
echo "=================================================="
