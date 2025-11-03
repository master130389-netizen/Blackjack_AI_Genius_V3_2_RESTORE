#!/bin/bash
cd ~/projects/Blackjack_AI_Genius_V3_2_RESTORE

echo "🔍 Verifica modifiche locali rispetto a GitHub..."
git fetch origin main

# Mostra differenze locali vs remoto
git status
git diff --name-only origin/main

# Backup automatico prima di sincronizzare
BACKUP_PATH=~/projects/Blackjack_AI_Genius_V3_2_RESTORE/git_backups/backup_$(date +%Y-%m-%d_%H-%M-%S).zip
echo "💾 Creazione backup automatico in: $BACKUP_PATH"
zip -r "$BACKUP_PATH" . > /dev/null

echo "✅ Backup completato."

# Aggiorna dal remoto se ci sono modifiche
echo "🔄 Sincronizzazione con GitHub..."
git pull origin main

echo "✨ Controllo incrociato completato!"
