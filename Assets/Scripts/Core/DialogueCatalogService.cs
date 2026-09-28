using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class DialogueCatalogData
    {
        public int schemaVersion;
        public List<DialogueDefinition> entries;
    }

    [Serializable]
    public sealed class DialogueDefinition
    {
        public string id;
        public string speakerName;
        public List<string> lines;
    }

    /// <summary>Versioned, localized dialogue data for story and contextual character lines.</summary>
    public static class DialogueCatalogService
    {
        public static DialogueCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/dialogue_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/dialogue_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<DialogueCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load dialogue catalog: " + exception.Message);
                return null;
            }
        }

        public static DialogueDefinition Find(DialogueCatalogData catalog, string id)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(id)) return null;
            foreach (var entry in catalog.entries)
                if (entry != null && entry.id == id) return entry;
            return null;
        }

        public static void Validate(DialogueCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Dialogue catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var entry in catalog.entries)
            {
                if (entry == null || !IsStableId(entry.id) || !ids.Add(entry.id) ||
                    string.IsNullOrWhiteSpace(entry.speakerName) || entry.lines == null || entry.lines.Count == 0)
                    throw new FormatException("Every dialogue entry requires a unique ID, speaker and at least one line.");
                foreach (var line in entry.lines)
                    if (string.IsNullOrWhiteSpace(line))
                        throw new FormatException("Dialogue line is empty on " + entry.id + ".");
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
