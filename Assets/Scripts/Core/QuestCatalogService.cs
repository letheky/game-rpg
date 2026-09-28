using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class QuestCatalogData
    {
        public int schemaVersion;
        public List<QuestDefinition> entries;
    }

    [Serializable]
    public sealed class QuestDefinition
    {
        public string id;
        public string arcId;
        // Optional bridge for the first linear slice. Campaign quests progress by stable IDs.
        public int stage = -1;
        public string locationId;
        public string branchFlag;
        public string branchValue;
        public string type;
        public string giverId;
        public string title;
        public string objective;
        public string choiceFlag;
        public List<string> prerequisiteIds;
        public List<QuestPrerequisiteGroup> prerequisiteGroups;
        public List<QuestObjectiveDefinition> objectives;
        public QuestRewardDefinition reward;
        public string choiceSpeaker;
        public string choicePrompt;
        public List<QuestChoiceDefinition> choices;
    }

    [Serializable]
    public sealed class QuestObjectiveDefinition
    {
        public string id;
        public string kind;
        public string targetId;
        public int requiredCount = 1;
        public string description;
        public string dialogueId;
    }

    [Serializable]
    public sealed class QuestPrerequisiteGroup
    {
        public List<string> anyOfQuestIds;
    }

    [Serializable]
    public sealed class QuestRewardDefinition
    {
        public int gold;
        public List<QuestItemReward> items;
    }

    [Serializable]
    public sealed class QuestItemReward
    {
        public string itemId;
        public int quantity = 1;
    }

    [Serializable]
    public sealed class QuestChoiceDefinition
    {
        public string id;
        public string label;
        public string flagValue;
        public string dialogueId;
        public QuestRewardDefinition reward;
    }

    /// <summary>Versioned quest data with stable IDs, prerequisites, objective contracts and rewards.</summary>
    public static class QuestCatalogService
    {
        private static readonly HashSet<string> objectiveKinds = new HashSet<string>
        {
            "talk", "defeat", "interact", "choice", "collect", "craft", "fish", "grow", "inspect", "escort"
        };

        public static QuestCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/prologue_quests");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/prologue_quests.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<QuestCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load quest catalog: " + exception.Message);
                return null;
            }
        }

        public static QuestDefinition FindByStage(QuestCatalogData catalog, int stage)
        {
            if (catalog?.entries == null) return null;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.stage == stage) return quest;
            return null;
        }

        public static QuestDefinition FindByStageAndBranch(QuestCatalogData catalog, int stage,
            string branchFlag, string branchValue)
        {
            if (catalog?.entries == null) return null;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.stage == stage &&
                    (string.IsNullOrEmpty(quest.branchFlag) ||
                     (quest.branchFlag == branchFlag && quest.branchValue == branchValue)))
                    return quest;
            return null;
        }

        public static QuestDefinition FindById(QuestCatalogData catalog, string id)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(id)) return null;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.id == id) return quest;
            return null;
        }

        public static QuestChoiceDefinition FindChoice(QuestDefinition quest, string choiceId)
        {
            if (quest?.choices == null) return null;
            foreach (var choice in quest.choices)
                if (choice != null && choice.id == choiceId) return choice;
            return null;
        }

        public static bool HasObjectiveTarget(QuestCatalogData catalog, string kind, string targetId)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(kind) || string.IsNullOrEmpty(targetId)) return false;
            foreach (var quest in catalog.entries)
            {
                if (quest?.objectives == null) continue;
                foreach (var objective in quest.objectives)
                    if (objective != null && objective.kind == kind && objective.targetId == targetId) return true;
            }
            return false;
        }

        public static void Validate(QuestCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Quest catalog schema or entries are invalid.");

            var byId = new Dictionary<string, QuestDefinition>();
            var stages = new Dictionary<int, List<QuestDefinition>>();
            foreach (var quest in catalog.entries)
            {
                if (quest == null || !IsStableId(quest.id) || !IsStableId(quest.arcId) ||
                    string.IsNullOrWhiteSpace(quest.title) || string.IsNullOrWhiteSpace(quest.objective))
                    throw new FormatException("Every quest requires stable IDs, a title and an objective.");
                if (byId.ContainsKey(quest.id)) throw new FormatException("Duplicate quest ID: " + quest.id);
                if (quest.stage >= 0)
                {
                    if (!stages.TryGetValue(quest.stage, out var sameStage))
                    {
                        sameStage = new List<QuestDefinition>();
                        stages.Add(quest.stage, sameStage);
                    }
                    sameStage.Add(quest);
                }
                if (string.IsNullOrEmpty(quest.branchFlag) != string.IsNullOrEmpty(quest.branchValue) ||
                    (!string.IsNullOrEmpty(quest.branchFlag) &&
                     (!IsStableId(quest.branchFlag) || !IsStableId(quest.branchValue))))
                    throw new FormatException("Branch stage must define a stable flag and value on " + quest.id + ".");
                if (quest.type != "story" && quest.type != "side" && quest.type != "character" && quest.type != "activity")
                    throw new FormatException("Unknown quest type on " + quest.id + ": " + quest.type);
                if (quest.type == "side" && (!IsStableId(quest.locationId) || quest.stage >= 0))
                    throw new FormatException("Side quests must name a stable location and cannot use a legacy story stage: " + quest.id);
                if (quest.objectives == null || quest.objectives.Count == 0)
                    throw new FormatException("Quest has no objective contract: " + quest.id);

                var objectiveIds = new HashSet<string>();
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || !IsStableId(objective.id) || !objectiveIds.Add(objective.id) ||
                        !objectiveKinds.Contains(objective.kind) || !IsStableId(objective.targetId) ||
                        objective.requiredCount < 1 || string.IsNullOrWhiteSpace(objective.description) ||
                        !IsOptionalStableId(objective.dialogueId))
                        throw new FormatException("Invalid objective contract on " + quest.id + ".");
                }

                ValidateReward(quest.reward, quest.id);
                if (quest.choices != null && quest.choices.Count > 0)
                {
                    if (quest.choices.Count < 2 || quest.choices.Count > 4 || string.IsNullOrWhiteSpace(quest.choicePrompt) ||
                        !IsStableId(quest.choiceFlag) || string.IsNullOrWhiteSpace(quest.choiceSpeaker))
                        throw new FormatException("Branching quest needs a prompt and two to four choices: " + quest.id);
                    var choiceIds = new HashSet<string>();
                    foreach (var choice in quest.choices)
                    {
                        if (choice == null || !IsStableId(choice.id) || !choiceIds.Add(choice.id) ||
                            string.IsNullOrWhiteSpace(choice.label) || !IsStableId(choice.flagValue) ||
                            !IsOptionalStableId(choice.dialogueId))
                            throw new FormatException("Invalid choice on " + quest.id + ".");
                        ValidateReward(choice.reward, quest.id + "/" + choice.id);
                    }
                }
                else if (!string.IsNullOrWhiteSpace(quest.choicePrompt))
                {
                    throw new FormatException("Quest has a choice prompt but no choices: " + quest.id);
                }
                else if (!string.IsNullOrWhiteSpace(quest.choiceFlag))
                {
                    throw new FormatException("Quest has a choice flag but no choices: " + quest.id);
                }
                else if (!string.IsNullOrWhiteSpace(quest.choiceSpeaker))
                {
                    throw new FormatException("Quest has a choice speaker but no choices: " + quest.id);
                }

                byId.Add(quest.id, quest);
            }

            var choiceValuesByFlag = new Dictionary<string, HashSet<string>>();
            foreach (var quest in catalog.entries)
            {
                if (quest.choices == null || quest.choices.Count == 0) continue;
                if (!choiceValuesByFlag.TryGetValue(quest.choiceFlag, out var values))
                {
                    values = new HashSet<string>();
                    choiceValuesByFlag.Add(quest.choiceFlag, values);
                }
                foreach (var choice in quest.choices) values.Add(choice.flagValue);
            }

            foreach (var quest in catalog.entries)
                if (!string.IsNullOrEmpty(quest.branchFlag) &&
                    (!choiceValuesByFlag.TryGetValue(quest.branchFlag, out var values) || !values.Contains(quest.branchValue)))
                    throw new FormatException("Quest branch does not match an authored choice value: " + quest.id);

            foreach (var stage in stages)
            {
                if (stage.Value.Count < 2) continue;
                var branchFlag = stage.Value[0].branchFlag;
                if (string.IsNullOrEmpty(branchFlag))
                    throw new FormatException("Duplicate legacy stage must use mutually exclusive branches: " + stage.Key);
                var branchValues = new HashSet<string>();
                foreach (var quest in stage.Value)
                    if (quest.branchFlag != branchFlag || !branchValues.Add(quest.branchValue))
                        throw new FormatException("Legacy stage branches must use one flag and distinct values: " + stage.Key);
            }

            foreach (var quest in catalog.entries)
            {
                if (quest.prerequisiteIds != null)
                    foreach (var prerequisiteId in quest.prerequisiteIds)
                        if (!byId.ContainsKey(prerequisiteId) || prerequisiteId == quest.id)
                            throw new FormatException("Unknown or self-referencing prerequisite on " + quest.id + ".");

                if (quest.prerequisiteGroups == null) continue;
                foreach (var group in quest.prerequisiteGroups)
                {
                    if (group?.anyOfQuestIds == null || group.anyOfQuestIds.Count == 0)
                        throw new FormatException("Quest prerequisite group is empty on " + quest.id + ".");
                    var alternatives = new HashSet<string>();
                    foreach (var prerequisiteId in group.anyOfQuestIds)
                        if (!byId.ContainsKey(prerequisiteId) || prerequisiteId == quest.id || !alternatives.Add(prerequisiteId))
                            throw new FormatException("Unknown, duplicate or self-referencing alternative prerequisite on " + quest.id + ".");
                }
            }

            var visiting = new HashSet<string>();
            var visited = new HashSet<string>();
            foreach (var quest in catalog.entries)
                if (HasPrerequisiteCycle(quest, byId, visiting, visited))
                    throw new FormatException("Quest prerequisite graph contains a cycle at " + quest.id + ".");
        }

        private static void ValidateReward(QuestRewardDefinition reward, string sourceId)
        {
            if (reward == null) return;
            if (reward.gold < 0) throw new FormatException("Negative gold reward on " + sourceId + ".");
            if (reward.items == null) return;
            foreach (var item in reward.items)
                if (item == null || ItemCatalog.Find(item.itemId) == null || item.quantity < 1)
                    throw new FormatException("Invalid item reward on " + sourceId + ".");
        }

        private static bool HasPrerequisiteCycle(QuestDefinition quest, Dictionary<string, QuestDefinition> byId,
            HashSet<string> visiting, HashSet<string> visited)
        {
            if (visited.Contains(quest.id)) return false;
            if (!visiting.Add(quest.id)) return true;

            if (quest.prerequisiteIds != null)
                foreach (var prerequisiteId in quest.prerequisiteIds)
                    if (HasPrerequisiteCycle(byId[prerequisiteId], byId, visiting, visited)) return true;

            if (quest.prerequisiteGroups != null)
                foreach (var group in quest.prerequisiteGroups)
                    foreach (var prerequisiteId in group.anyOfQuestIds)
                        if (HasPrerequisiteCycle(byId[prerequisiteId], byId, visiting, visited)) return true;

            visiting.Remove(quest.id);
            visited.Add(quest.id);
            return false;
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

        private static bool IsOptionalStableId(string value) => string.IsNullOrEmpty(value) || IsStableId(value);
    }
}
