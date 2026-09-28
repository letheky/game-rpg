using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class QuestLandmarkCatalogData
    {
        public int schemaVersion;
        public List<QuestLandmarkDefinition> entries;
    }

    [Serializable]
    public sealed class QuestLandmarkDefinition
    {
        public string id;
        public string locationId;
        public string displayName;
        public string targetId;
        public string visualId;
        public float positionX;
        public float positionY;
        public float scale = 0.085f;
    }

    /// <summary>Creates optional, objective-gated world markers from authored content data.</summary>
    public static class QuestLandmarkCatalogService
    {
        private static readonly HashSet<string> visualIds = new HashSet<string>
        {
            "chalk_tally", "witness", "door_brace", "document", "noticeboard", "sealed_case",
            "herb_ledger", "remedy_shelf", "waymarker", "root_graft", "seed_cradle",
            "cycle_tablet", "stone_rill", "choir_diver", "wind_keeper", "signal_frame",
            "signal_vane", "signal_mark", "signal_well", "signal_ridge", "signal_bell_test",
            "signal_flag_test", "sluice_wheel", "pressure_gauge", "filter_housing", "clinic_house",
            "field_satchel", "cart_wheel", "cart_rut", "cart_spokes", "cart_test", "cart_bay",
            "cart_kit", "tomas_reed", "rootwall_joint", "pella_quinn", "kitchen_hearth",
            "kitchen_millstone", "broth_sample", "common_table", "glassplum_tree"
        };

        public static QuestLandmarkCatalogData Load(QuestCatalogData quests, DialogueCatalogData dialogue)
        {
            var asset = Resources.Load<TextAsset>("Content/quest_landmarks");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/quest_landmarks.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<QuestLandmarkCatalogData>(asset.text);
                Validate(catalog, quests, dialogue);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load quest-landmark catalog: " + exception.Message);
                return null;
            }
        }

        public static List<QuestLandmarkDefinition> FindByLocation(QuestLandmarkCatalogData catalog,
            string locationId)
        {
            var result = new List<QuestLandmarkDefinition>();
            if (catalog?.entries == null || string.IsNullOrEmpty(locationId)) return result;
            foreach (var entry in catalog.entries)
                if (entry != null && entry.locationId == locationId) result.Add(entry);
            return result;
        }

        public static void Validate(QuestLandmarkCatalogData catalog, QuestCatalogData quests,
            DialogueCatalogData dialogue)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0 ||
                quests?.entries == null || dialogue?.entries == null)
                throw new FormatException("Quest-landmark catalog schema, entries or dependencies are invalid.");

            var ids = new HashSet<string>();
            var targets = new HashSet<string>();
            foreach (var entry in catalog.entries)
            {
                if (entry == null || !IsStableId(entry.id) || !ids.Add(entry.id) ||
                    !IsStableId(entry.locationId) || !IsStableId(entry.targetId) || !targets.Add(entry.targetId) ||
                    string.IsNullOrWhiteSpace(entry.displayName) || entry.displayName.Length > 60 ||
                    !visualIds.Contains(entry.visualId) || !IsFinite(entry.positionX) || !IsFinite(entry.positionY) ||
                    entry.positionX < -11.3f || entry.positionX > 11.3f ||
                    entry.positionY < -5.2f || entry.positionY > 5f ||
                    !IsFinite(entry.scale) || entry.scale < 0.04f || entry.scale > 0.2f)
                    throw new FormatException("Invalid quest-landmark definition or duplicate ID/target.");

                var matchedObjective = false;
                foreach (var quest in quests?.entries ?? new List<QuestDefinition>())
                {
                    if (quest?.objectives == null) continue;
                    foreach (var objective in quest.objectives)
                    {
                        if (objective == null || objective.targetId != entry.targetId) continue;
                        if (objective.kind != "inspect" && objective.kind != "interact" && objective.kind != "grow" &&
                            objective.kind != "talk" && objective.kind != "choice")
                            throw new FormatException("Quest landmark target is used by an unsupported objective kind: " +
                                                      entry.targetId + ".");
                        if (quest.type == "side" && quest.locationId != entry.locationId)
                            throw new FormatException("Quest landmark is outside its side quest region: " + quest.id + ".");
                        if (objective.kind == "choice")
                        {
                            if (quest.choices == null || quest.choices.Count < 2)
                                throw new FormatException("Choice landmark has no authored choices: " + quest.id + ".");
                            foreach (var choice in quest.choices)
                                if (choice == null || DialogueCatalogService.Find(dialogue, choice.dialogueId) == null)
                                    throw new FormatException("Choice landmark has no result dialogue: " + quest.id + ".");
                        }
                        else if (objective.kind == "grow")
                        {
                            matchedObjective = true;
                            continue;
                        }
                        else if (DialogueCatalogService.Find(dialogue, objective.dialogueId) == null)
                        {
                            throw new FormatException("Quest landmark objective has no authored dialogue: " + quest.id + ".");
                        }
                        matchedObjective = true;
                    }
                }

                if (!matchedObjective)
                    throw new FormatException("Quest landmark has no matching quest objective: " + entry.targetId + ".");
            }
        }

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);

        private static bool IsStableId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 64 || value[0] < 'a' || value[0] > 'z') return false;
            foreach (var character in value)
                if (!((character >= 'a' && character <= 'z') || (character >= '0' && character <= '9') || character == '_'))
                    return false;
            return true;
        }
    }
}
