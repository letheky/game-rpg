using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class EncounterCatalogData
    {
        public int schemaVersion;
        public List<EncounterDefinition> entries;
    }

    [Serializable]
    public sealed class EncounterDefinition
    {
        public string id;
        public string monsterId;
        public string locationId;
        public float positionX;
        public float positionY;
        public string requiredQuestId;
        public string blockedQuestId;
        public string blockedDialogueId;
        public bool contributesToQuest = true;
        public string defeatObjectiveTargetId;
        public string defeatDialogueId;
        public string downDialogueId;
        public QuestRewardDefinition reward;
    }

    /// <summary>Places persistent encounters in authored locations without coupling save state to a monster species.</summary>
    public static class EncounterCatalogService
    {
        public static EncounterCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/encounter_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/encounter_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<EncounterCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load encounter catalog: " + exception.Message);
                return null;
            }
        }

        public static EncounterDefinition FindById(EncounterCatalogData catalog, string id)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(id)) return null;
            foreach (var encounter in catalog.entries)
                if (encounter != null && encounter.id == id) return encounter;
            return null;
        }

        public static void Validate(EncounterCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Encounter catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var encounter in catalog.entries)
            {
                if (encounter == null || !IsStableId(encounter.id) || !ids.Add(encounter.id) ||
                    !IsStableId(encounter.monsterId) || !IsStableId(encounter.locationId) ||
                    !IsStableId(encounter.requiredQuestId) || !IsOptionalStableId(encounter.blockedQuestId) ||
                    !IsOptionalStableId(encounter.blockedDialogueId) ||
                    (string.IsNullOrEmpty(encounter.blockedQuestId) != string.IsNullOrEmpty(encounter.blockedDialogueId)) ||
                    (encounter.contributesToQuest ? !IsStableId(encounter.defeatObjectiveTargetId) :
                        !IsOptionalStableId(encounter.defeatObjectiveTargetId)) || !IsStableId(encounter.defeatDialogueId) ||
                    !IsStableId(encounter.downDialogueId) ||
                    float.IsNaN(encounter.positionX) || float.IsInfinity(encounter.positionX) ||
                    float.IsNaN(encounter.positionY) || float.IsInfinity(encounter.positionY) ||
                    (encounter.reward != null && encounter.reward.gold < 0))
                    throw new FormatException("Invalid encounter definition or duplicate ID.");

                if (encounter.reward?.items == null) continue;
                foreach (var item in encounter.reward.items)
                    if (item == null || !IsStableId(item.itemId) || item.quantity < 1)
                        throw new FormatException("Invalid encounter reward on " + encounter.id + ".");
            }
        }

        private static bool IsOptionalStableId(string value) => string.IsNullOrEmpty(value) || IsStableId(value);

        private static bool IsStableId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 64 || value[0] < 'a' || value[0] > 'z') return false;
            foreach (var character in value)
                if (!((character >= 'a' && character <= 'z') || (character >= '0' && character <= '9') || character == '_'))
                    return false;
            return true;
        }
    }

    public static class EncounterProgressService
    {
        public static EncounterProgressData GetOrCreate(GameSaveData save, EncounterDefinition definition,
            MonsterDefinition monster)
        {
            if (save == null || definition == null || monster == null) return null;
            if (save.encounterProgress == null) save.encounterProgress = new List<EncounterProgressData>();
            foreach (var state in save.encounterProgress)
            {
                if (state == null || state.encounterId != definition.id) continue;
                state.health = Mathf.Clamp(state.health, 0, monster.maxHealth);
                if (state.defeated) state.health = 0;
                return state;
            }

            var created = new EncounterProgressData
            {
                encounterId = definition.id,
                health = monster.maxHealth,
                defeated = false
            };
            save.encounterProgress.Add(created);
            return created;
        }
    }
}
