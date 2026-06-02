#!/usr/bin/env bash
# Run the translation-validator self-check. Used locally and in CI.
# Requires only python3 (3.8+). No third-party packages.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== Pitaka translation validator: self-check =="
python3 "${HERE}/tests/test_validator.py"

echo
echo "== Validating real translations under translations/ =="
# Validate against the vendored English mirror (english/strings.xml), kept in
# sync from the app repo. Override with PITAKA_ENGLISH_STRINGS to point at a
# live app checkout instead.
ENGLISH_DEFAULT="${HERE}/../english/strings.xml"
ENGLISH="${PITAKA_ENGLISH_STRINGS:-${ENGLISH_DEFAULT}}"

if [[ ! -f "${ENGLISH}" ]]; then
  echo "NOTE: English source not found at ${ENGLISH}."
  echo "      Expected the vendored mirror english/strings.xml, or set"
  echo "      PITAKA_ENGLISH_STRINGS to the app repo's"
  echo "      app/src/main/res/values/strings.xml."
  echo "      (Self-check above already passed.)"
  exit 0
fi

python3 "${HERE}/validate_translations.py" \
  --english "${ENGLISH}" \
  --translations "${HERE}/../translations"
