using System.Collections.Generic;

namespace AshenOath.Core
{
    /// <summary>Persists quest state by authored IDs; numeric stages are kept only as a legacy save bridge.</summary>
    public static class QuestProgressService
    {
        public const int MaxActiveSideQuests = 3;

        public static QuestDefinition GetActiveQuest(GameSaveData save, QuestCatalogData catalog)
        {
            return save == null ? null : QuestCatalogService.FindById(catalog, save.activeQuestId);
        }

        public static List<QuestDefinition> GetActiveQuests(GameSaveData save, QuestCatalogData catalog)
        {
            var quests = new List<QuestDefinition>();
            var storyQuest = GetActiveQuest(save, catalog);
            if (storyQuest != null) quests.Add(storyQuest);
            foreach (var sideQuest in GetActiveSideQuests(save, catalog)) quests.Add(sideQuest);
            return quests;
        }

        public static List<QuestDefinition> GetActiveSideQuests(GameSaveData save, QuestCatalogData catalog)
        {
            var quests = new List<QuestDefinition>();
            if (save?.activeSideQuestIds == null) return quests;
            foreach (var id in save.activeSideQuestIds)
            {
                var quest = QuestCatalogService.FindById(catalog, id);
                if (quest != null && quest.type == "side") quests.Add(quest);
            }
            return quests;
        }

        public static List<QuestDefinition> GetAvailableSideQuests(GameSaveData save, QuestCatalogData catalog,
            string locationId)
        {
            var quests = new List<QuestDefinition>();
            if (save == null || catalog?.entries == null || string.IsNullOrEmpty(locationId)) return quests;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.type == "side" && quest.locationId == locationId &&
                    IsAvailableSideQuest(save, quest)) quests.Add(quest);
            return quests;
        }

        public static bool CanAcceptSideQuest(GameSaveData save, QuestCatalogData catalog, string questId,
            string locationId)
        {
            if (save?.activeSideQuestIds == null || save.activeSideQuestIds.Count >= MaxActiveSideQuests) return false;
            var quest = QuestCatalogService.FindById(catalog, questId);
            return quest != null && quest.type == "side" && quest.locationId == locationId &&
                   IsAvailableSideQuest(save, quest);
        }

        public static bool TryAcceptSideQuest(GameSaveData save, QuestCatalogData catalog, string questId,
            string locationId)
        {
            if (!CanAcceptSideQuest(save, catalog, questId, locationId)) return false;
            if (save.activeSideQuestIds == null) save.activeSideQuestIds = new List<string>();
            save.activeSideQuestIds.Add(questId);
            return true;
        }

        public static bool IsCompleted(GameSaveData save, string questId)
        {
            return save?.completedQuestIds != null && save.completedQuestIds.Contains(questId);
        }

        public static int GetObjectiveProgress(GameSaveData save, QuestDefinition quest,
            QuestObjectiveDefinition objective)
        {
            if (quest == null || objective == null) return 0;
            var progress = FindObjectiveProgress(save, quest.id, objective.id);
            return progress == null ? 0 : System.Math.Min(objective.requiredCount, progress.count);
        }

        public static bool IsActive(GameSaveData save, string questId)
        {
            return save != null && (save.activeQuestId == questId && !string.IsNullOrEmpty(questId) ||
                   save.activeSideQuestIds != null && save.activeSideQuestIds.Contains(questId));
        }

        public static string GetStoryFlag(GameSaveData save, string flagId)
        {
            if (save == null || string.IsNullOrEmpty(flagId)) return "";
            if (save.storyFlags != null)
                for (var i = save.storyFlags.Count - 1; i >= 0; i--)
                    if (save.storyFlags[i] != null && save.storyFlags[i].id == flagId)
                        return save.storyFlags[i].value ?? "";
            return flagId == "first_choice" ? save.firstChoice ?? "" : "";
        }

        public static void SetStoryFlag(GameSaveData save, string flagId, string value)
        {
            if (save == null || string.IsNullOrWhiteSpace(flagId) || string.IsNullOrWhiteSpace(value)) return;
            if (save.storyFlags == null) save.storyFlags = new List<StoryFlagData>();
            for (var i = 0; i < save.storyFlags.Count; i++)
            {
                if (save.storyFlags[i] == null || save.storyFlags[i].id != flagId) continue;
                save.storyFlags[i].value = value;
                if (flagId == "first_choice") save.firstChoice = value;
                return;
            }

            save.storyFlags.Add(new StoryFlagData { id = flagId, value = value });
            if (flagId == "first_choice") save.firstChoice = value;
        }

        /// <summary>Reconciles save IDs with the catalog and upgrades pre-ID stage saves without losing progress.</summary>
        public static bool Reconcile(GameSaveData save, QuestCatalogData catalog)
        {
            if (save == null || catalog?.entries == null) return false;
            var previousActiveId = save.activeQuestId ?? "";
            var previousActiveSideQuestIds = save.activeSideQuestIds == null
                ? "" : string.Join("|", save.activeSideQuestIds);
            var previousStage = save.questStage;
            var previousComplete = save.chapterComplete;
            var previousCompletedCount = save.completedQuestIds?.Count ?? 0;
            var previousFlagCount = save.storyFlags?.Count ?? 0;
            if (save.completedQuestIds == null) save.completedQuestIds = new List<string>();
            if (save.activeSideQuestIds == null) save.activeSideQuestIds = new List<string>();
            if (save.storyFlags == null) save.storyFlags = new List<StoryFlagData>();
            if (save.questObjectiveProgress == null) save.questObjectiveProgress = new List<QuestObjectiveProgressData>();

            if (save.completedQuestIds.Count == 0 && string.IsNullOrEmpty(save.activeQuestId))
                MigrateLegacyStage(save, catalog);

            if (!string.IsNullOrWhiteSpace(save.firstChoice) && string.IsNullOrEmpty(GetStoryFlag(save, "first_choice")))
                SetStoryFlag(save, "first_choice", save.firstChoice);
            else if (!string.IsNullOrEmpty(GetStoryFlag(save, "first_choice")))
                save.firstChoice = GetStoryFlag(save, "first_choice");

            var active = QuestCatalogService.FindById(catalog, save.activeQuestId);
            if (active == null || active.type != "story" || IsCompleted(save, active.id) || !BranchMatches(save, active) ||
                !PrerequisitesComplete(save, active))
                save.activeQuestId = "";

            if (string.IsNullOrEmpty(save.activeQuestId))
            {
                active = FindNextAvailable(save, catalog);
                if (active != null) save.activeQuestId = active.id;
            }

            active = QuestCatalogService.FindById(catalog, save.activeQuestId);
            ReconcileActiveSideQuests(save, catalog);
            save.chapterComplete = active == null && AllEligibleStoryQuestsComplete(save, catalog);
            save.questStage = active != null && active.stage >= 0 ? active.stage : save.chapterComplete ? 5 : 0;
            return previousActiveId != save.activeQuestId || previousStage != save.questStage ||
                   previousComplete != save.chapterComplete || previousCompletedCount != save.completedQuestIds.Count ||
                   previousFlagCount != save.storyFlags.Count ||
                   previousActiveSideQuestIds != string.Join("|", save.activeSideQuestIds);
        }

        /// <summary>Records an event against the current quest's typed targets. Returns true when it matched.</summary>
        public static bool RecordObjective(GameSaveData save, QuestCatalogData catalog, string kind, string targetId,
            int amount, out QuestDefinition completedQuest)
        {
            var matched = RecordObjectives(save, catalog, kind, targetId, amount, out var completedQuests);
            completedQuest = completedQuests.Count > 0 ? completedQuests[0] : null;
            return matched;
        }

        /// <summary>Records one gameplay event across the active story quest and every accepted side quest.</summary>
        public static bool RecordObjectives(GameSaveData save, QuestCatalogData catalog, string kind, string targetId,
            int amount, out List<QuestDefinition> completedQuests)
        {
            completedQuests = new List<QuestDefinition>();
            if (save == null || catalog?.entries == null || amount < 1) return false;

            var matched = false;
            var reconciledStory = false;
            foreach (var quest in GetActiveQuests(save, catalog))
            {
                if (quest.objectives == null) continue;
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || objective.kind != kind || objective.targetId != targetId) continue;
                    matched = true;
                    var progress = FindObjectiveProgress(save, quest.id, objective.id);
                    if (progress == null)
                    {
                        if (save.questObjectiveProgress == null)
                            save.questObjectiveProgress = new List<QuestObjectiveProgressData>();
                        progress = new QuestObjectiveProgressData { questId = quest.id, objectiveId = objective.id };
                        save.questObjectiveProgress.Add(progress);
                    }
                    progress.count = System.Math.Min(objective.requiredCount, progress.count + amount);
                }

                if (!AllObjectivesComplete(save, quest)) continue;
                AddCompleted(save, quest.id);
                completedQuests.Add(quest);
                if (quest.type == "side")
                {
                    if (save.activeSideQuestIds != null) save.activeSideQuestIds.Remove(quest.id);
                }
                else
                {
                    save.activeQuestId = "";
                    reconciledStory = true;
                }
            }

            if (reconciledStory) Reconcile(save, catalog);
            return matched;
        }

        private static void MigrateLegacyStage(GameSaveData save, QuestCatalogData catalog)
        {
            var legacyStage = save.questStage;
            if (legacyStage >= 3 && string.IsNullOrEmpty(save.firstChoice))
            {
                foreach (var quest in catalog.entries)
                {
                    if (quest?.choices == null || quest.choices.Count == 0 || quest.stage >= legacyStage) continue;
                    save.firstChoice = quest.choices[0].flagValue;
                    SetStoryFlag(save, quest.choiceFlag, save.firstChoice);
                    break;
                }
            }
            else if (!string.IsNullOrEmpty(save.firstChoice))
            {
                SetStoryFlag(save, "first_choice", save.firstChoice);
            }

            foreach (var quest in catalog.entries)
            {
                if (quest == null || quest.stage < 0 || !BranchMatches(save, quest)) continue;
                if (legacyStage >= 5 || quest.stage < legacyStage)
                    AddCompleted(save, quest.id);
                else if (legacyStage == quest.stage && string.IsNullOrEmpty(save.activeQuestId))
                    save.activeQuestId = quest.id;
            }
        }

        private static QuestDefinition FindNextAvailable(GameSaveData save, QuestCatalogData catalog)
        {
            foreach (var quest in catalog.entries)
                if (quest != null && quest.type == "story" && !IsCompleted(save, quest.id) && BranchMatches(save, quest) &&
                    PrerequisitesComplete(save, quest))
                    return quest;
            return null;
        }

        private static bool BranchMatches(GameSaveData save, QuestDefinition quest)
        {
            return string.IsNullOrEmpty(quest.branchFlag) ||
                   GetStoryFlag(save, quest.branchFlag) == quest.branchValue;
        }

        private static bool PrerequisitesComplete(GameSaveData save, QuestDefinition quest)
        {
            if (quest.prerequisiteIds != null)
                foreach (var id in quest.prerequisiteIds)
                    if (!IsCompleted(save, id)) return false;

            if (quest.prerequisiteGroups != null)
                foreach (var group in quest.prerequisiteGroups)
                {
                    var oneCompleted = false;
                    foreach (var id in group.anyOfQuestIds)
                        if (IsCompleted(save, id))
                        {
                            oneCompleted = true;
                            break;
                        }
                    if (!oneCompleted) return false;
                }
            return true;
        }

        private static bool AllEligibleStoryQuestsComplete(GameSaveData save, QuestCatalogData catalog)
        {
            foreach (var quest in catalog.entries)
                if (quest != null && quest.type == "story" && BranchMatches(save, quest) && !IsCompleted(save, quest.id))
                    return false;
            return true;
        }

        private static bool IsAvailableSideQuest(GameSaveData save, QuestDefinition quest)
        {
            return !IsCompleted(save, quest.id) && !IsActive(save, quest.id) && BranchMatches(save, quest) &&
                   PrerequisitesComplete(save, quest);
        }

        private static void ReconcileActiveSideQuests(GameSaveData save, QuestCatalogData catalog)
        {
            if (save.activeSideQuestIds == null) save.activeSideQuestIds = new List<string>();
            var accepted = new List<string>();
            foreach (var id in save.activeSideQuestIds)
            {
                var quest = QuestCatalogService.FindById(catalog, id);
                if (quest == null || quest.type != "side" || IsCompleted(save, id) ||
                    !BranchMatches(save, quest) || !PrerequisitesComplete(save, quest) || accepted.Contains(id)) continue;
                accepted.Add(id);
            }

            if (accepted.Count > MaxActiveSideQuests)
                accepted.RemoveRange(MaxActiveSideQuests, accepted.Count - MaxActiveSideQuests);
            save.activeSideQuestIds = accepted;
        }

        private static bool AllObjectivesComplete(GameSaveData save, QuestDefinition quest)
        {
            if (quest.objectives == null || quest.objectives.Count == 0) return false;
            foreach (var objective in quest.objectives)
            {
                var progress = FindObjectiveProgress(save, quest.id, objective.id);
                if (progress == null || progress.count < objective.requiredCount) return false;
            }
            return true;
        }

        private static QuestObjectiveProgressData FindObjectiveProgress(GameSaveData save, string questId, string objectiveId)
        {
            if (save?.questObjectiveProgress == null) return null;
            foreach (var progress in save.questObjectiveProgress)
                if (progress != null && progress.questId == questId && progress.objectiveId == objectiveId)
                    return progress;
            return null;
        }

        private static void AddCompleted(GameSaveData save, string questId)
        {
            if (save.completedQuestIds == null) save.completedQuestIds = new List<string>();
            if (!save.completedQuestIds.Contains(questId)) save.completedQuestIds.Add(questId);
        }
    }
}
