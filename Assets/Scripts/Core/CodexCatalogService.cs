using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class CodexCatalogData
    {
        public int schemaVersion;
        public List<CodexEntryDefinition> entries;
    }

    [Serializable]
    public sealed class CodexEntryDefinition
    {
        public string id;
        public string title;
        public string category;
        public string writtenBy;
        public string unlockQuestId;
        public string body;
    }

    /// <summary>Offline field archive unlocked by completed story evidence.</summary>
    public static class CodexCatalogService
    {
        public static CodexCatalogData Load(QuestCatalogData quests)
        {
            var asset = Resources.Load<TextAsset>("Content/codex_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/codex_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<CodexCatalogData>(asset.text);
                Validate(catalog, quests);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load codex catalog: " + exception.Message);
                return null;
            }
        }

        public static List<CodexEntryDefinition> GetUnlocked(CodexCatalogData catalog, GameSaveData save)
        {
            var unlocked = new List<CodexEntryDefinition>();
            if (catalog?.entries == null || save?.completedQuestIds == null) return unlocked;
            foreach (var entry in catalog.entries)
                if (entry != null && save.completedQuestIds.Contains(entry.unlockQuestId)) unlocked.Add(entry);
            return unlocked;
        }

        public static void Validate(CodexCatalogData catalog, QuestCatalogData quests)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Codex catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var entry in catalog.entries)
            {
                if (entry == null || !IsStableId(entry.id) || !ids.Add(entry.id) ||
                    string.IsNullOrWhiteSpace(entry.title) || string.IsNullOrWhiteSpace(entry.category) ||
                    string.IsNullOrWhiteSpace(entry.writtenBy) || string.IsNullOrWhiteSpace(entry.body) ||
                    QuestCatalogService.FindById(quests, entry.unlockQuestId) == null)
                    throw new FormatException("Every codex entry requires a unique ID, title, author, body and valid unlock quest.");
            }
        }

        private static bool IsStableId(string value)
        {
            if (string.IsNullOrEmpty(value) || value[0] < 'a' || value[0] > 'z') return false;
            for (var i = 1; i < value.Length; i++)
            {
                var character = value[i];
                if ((character < 'a' || character > 'z') && (character < '0' || character > '9') && character != '_')
                    return false;
            }
            return true;
        }
    }
}
