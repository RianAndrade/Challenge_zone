# 1) Shebang limpo (sem espaços antes)
sed -n '1p' backend/docker-entrypoint.sh

# se não for exatamente:
# !/bin/sh   (ou)   !/usr/bin/env sh
# ajuste para:
printf '%s\n' '#!/bin/sh' | cat - backend/docker-entrypoint.sh > backend/_tmp && mv backend/_tmp backend/docker-entrypoint.sh

# 2) Remover CRLF e BOM
sed -i 's/\r$//' backend/docker-entrypoint.sh
# remove BOM (UTF-8)
printf '\xEF\xBB\xBF' | cat -v  # (só pra ilustrar o símbolo do BOM)
# comando para tirar o BOM da 1ª linha:
awk 'NR==1{sub(/^\xef\xbb\xbf/,"")} {print}' backend/docker-entrypoint.sh > backend/_tmp && mv backend/_tmp backend/docker-entrypoint.sh

# 3) Tornar executável
chmod 0755 backend/docker-entrypoint.sh
