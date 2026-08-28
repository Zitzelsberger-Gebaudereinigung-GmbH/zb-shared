#!/usr/bin/env sh
# Baut das Codex-Analysepaket aus dem Repo-Stand. Aufruf aus dem Repo-Wurzelverzeichnis.
set -eu
OUT="${1:-LEARNI_OS_Codex_Analysepaket}"
rm -rf "$OUT" "$OUT.zip"
mkdir -p "$OUT"/01_konzept_original "$OUT"/02_review "$OUT"/03_prototyp \
         "$OUT"/04_kontext_repo/zb_shared "$OUT"/05_offene_punkte "$OUT"/06_entscheidungen
cp docs/learni-os/CODEX_ANALYSEAUFTRAG.md            "$OUT"/
cp docs/learni-os/PAKET_README.md                    "$OUT"/README.md
cp docs/learni-os/quelle/CLAUDE_CODE_HANDOFF.md      "$OUT"/01_konzept_original/
cp docs/learni-os/quelle/prototype.html              "$OUT"/01_konzept_original/
cp docs/learni-os/KONZEPTREVIEW.md                   "$OUT"/02_review/
cp docs/learni-os/prototyp/learni-os-prototyp.html   "$OUT"/03_prototyp/
cp docs/learni-os/prototyp/src/*.css docs/learni-os/prototyp/src/*.js "$OUT"/03_prototyp/
cp README.md pyproject.toml                          "$OUT"/04_kontext_repo/
cp zb_shared/*.py                                    "$OUT"/04_kontext_repo/zb_shared/
cp docs/learni-os/OFFENE_BRUCHSTELLEN.md docs/learni-os/bruchstellen.json "$OUT"/05_offene_punkte/
cp docs/learni-os/GESTRICHEN_UND_WARUM.md            "$OUT"/06_entscheidungen/
zip -qr "$OUT.zip" "$OUT"
echo "$OUT.zip gebaut"
