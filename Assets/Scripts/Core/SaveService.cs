using System;
using System.IO;
using UnityEngine;

namespace AshenOath.Core
{
    /// <summary>Single-slot, offline save. The JSON format is versioned for later migrations.</summary>
    public static class SaveService
    {
        private const string FileName = "ashen_oath_save_01.json";

        public static string SavePath => Path.Combine(Application.persistentDataPath, FileName);

        public static GameSaveData Load()
        {
            if (!File.Exists(SavePath)) return CreateNewSave();

            try
            {
                var data = JsonUtility.FromJson<GameSaveData>(File.ReadAllText(SavePath));
                if (data == null)
                {
                    Debug.LogWarning("Save version is not supported; starting a new Ashen Oath save.");
                    return CreateNewSave();
                }

                if (!TryUpgradeToCurrent(data))
                {
                    Debug.LogWarning("Save version is not supported; starting a new Ashen Oath save.");
                    return CreateNewSave();
                }
                return data;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not read the local save: " + exception.Message);
                return CreateNewSave();
            }
        }

        /// <summary>Upgrades a deserialized save in memory; public for editor validation and migration tools.</summary>
        public static bool TryUpgradeToCurrent(GameSaveData data)
        {
            if (data == null) return false;
            if (data.schemaVersion == 1) MigrateSchemaV1(data);
            if (data.schemaVersion == 2) MigrateSchemaV2(data);
            if (data.schemaVersion == 3) MigrateSchemaV3(data);
            if (data.schemaVersion == 4) MigrateSchemaV4(data);
            if (data.schemaVersion == 5) MigrateSchemaV5(data);
            if (data.schemaVersion == 6) MigrateSchemaV6(data);
            if (data.schemaVersion == 7) MigrateSchemaV7(data);
            if (data.schemaVersion == 8) MigrateSchemaV8(data);
            if (data.schemaVersion == 9) MigrateSchemaV9(data);
            if (data.schemaVersion != 10) return false;

            data.health = Mathf.Clamp(data.health, 1, 48);
            data.gold = Mathf.Max(0, data.gold);
            data.potions = 0;
            data.wargFangs = 0;
            data.questStage = Mathf.Clamp(data.questStage, 0, 5);
            if (data.questStage >= 5) data.chapterComplete = true;
            data.wargHealth = Mathf.Clamp(data.wargHealth, 0, 36);
            if (data.firstChoice == null) data.firstChoice = "";
            if (data.activeQuestId == null) data.activeQuestId = "";
            if (data.activeSideQuestIds == null)
                data.activeSideQuestIds = new System.Collections.Generic.List<string>();
            if (data.inventory == null) data.inventory = new System.Collections.Generic.List<InventoryStackData>();
            if (data.completedQuestIds == null) data.completedQuestIds = new System.Collections.Generic.List<string>();
            if (data.storyFlags == null) data.storyFlags = new System.Collections.Generic.List<StoryFlagData>();
            if (data.questObjectiveProgress == null)
                data.questObjectiveProgress = new System.Collections.Generic.List<QuestObjectiveProgressData>();
            if (data.encounterProgress == null)
                data.encounterProgress = new System.Collections.Generic.List<EncounterProgressData>();
            if (data.farmProgress == null)
                data.farmProgress = new System.Collections.Generic.List<FarmPlotProgressData>();
            if (!GameLocationService.IsPlayable(data.locationId))
                data.locationId = "ashfall_village";
            if (data.endingId != "crown_of_ash" && data.endingId != "beyond_the_veil") data.endingId = "";
            if (string.IsNullOrWhiteSpace(data.weaponId)) data.weaponId = "practice_sword";
            if (data.armorId == null) data.armorId = "";
            if (data.charmId == null) data.charmId = "";
            SanitizeInventory(data.inventory);
            SanitizeEncounterProgress(data.encounterProgress);
            SanitizeFarmProgress(data.farmProgress);
            SanitizeProgress(data);
            return true;
        }

        private static GameSaveData CreateNewSave()
        {
            var data = new GameSaveData
            {
                potions = 0,
                inventory = new System.Collections.Generic.List<InventoryStackData>
                {
                    new InventoryStackData { itemId = "healing_tonic", quantity = 1 },
                    new InventoryStackData { itemId = "practice_sword", quantity = 1 },
                    new InventoryStackData { itemId = "earthworm_bait", quantity = 3 },
                    new InventoryStackData { itemId = "moonwort_seed", quantity = 3 }
                }
            };
            return data;
        }

        private static void MigrateSchemaV1(GameSaveData data)
        {
            data.inventory = new System.Collections.Generic.List<InventoryStackData>();
            if (data.potions > 0)
                data.inventory.Add(new InventoryStackData { itemId = "healing_tonic", quantity = data.potions });
            if (data.wargFangs > 0)
                data.inventory.Add(new InventoryStackData { itemId = "ash_warg_fang", quantity = data.wargFangs });
            if (string.IsNullOrWhiteSpace(data.weaponId)) data.weaponId = "practice_sword";
            if (data.armorId == null) data.armorId = "";
            if (data.charmId == null) data.charmId = "";
            var hasPracticeSword = false;
            foreach (var stack in data.inventory)
                if (stack != null && stack.itemId == "practice_sword" && stack.quantity > 0) hasPracticeSword = true;
            if (!hasPracticeSword)
                data.inventory.Add(new InventoryStackData { itemId = "practice_sword", quantity = 1 });
            data.schemaVersion = 2;
        }

        private static void MigrateSchemaV2(GameSaveData data)
        {
            data.chapterComplete = data.questStage >= 5;
            data.schemaVersion = 3;
        }

        private static void MigrateSchemaV3(GameSaveData data)
        {
            data.activeQuestId = "";
            data.completedQuestIds = new System.Collections.Generic.List<string>();
            data.storyFlags = new System.Collections.Generic.List<StoryFlagData>();
            data.questObjectiveProgress = new System.Collections.Generic.List<QuestObjectiveProgressData>();
            data.schemaVersion = 4;
        }

        private static void MigrateSchemaV4(GameSaveData data)
        {
            data.locationId = "ashfall_village";
            data.schemaVersion = 5;
        }

        private static void MigrateSchemaV5(GameSaveData data)
        {
            data.encounterProgress = new System.Collections.Generic.List<EncounterProgressData>
            {
                new EncounterProgressData
                {
                    encounterId = "ash_warg_yard",
                    health = data.wargHealth,
                    defeated = data.wargDefeated
                }
            };
            if (data.inventory == null) data.inventory = new System.Collections.Generic.List<InventoryStackData>();
            var hasBait = false;
            foreach (var stack in data.inventory)
                if (stack != null && stack.itemId == "earthworm_bait" && stack.quantity > 0) hasBait = true;
            if (!hasBait)
                data.inventory.Add(new InventoryStackData { itemId = "earthworm_bait", quantity = 3 });
            data.schemaVersion = 6;
        }

        private static void MigrateSchemaV6(GameSaveData data)
        {
            if (data.farmProgress == null) data.farmProgress = new System.Collections.Generic.List<FarmPlotProgressData>();
            if (data.inventory == null) data.inventory = new System.Collections.Generic.List<InventoryStackData>();
            var hasSeeds = false;
            foreach (var stack in data.inventory)
                if (stack != null && stack.itemId == "moonwort_seed" && stack.quantity > 0) hasSeeds = true;
            if (!hasSeeds) data.inventory.Add(new InventoryStackData { itemId = "moonwort_seed", quantity = 3 });
            data.schemaVersion = 7;
        }

        private static void MigrateSchemaV7(GameSaveData data)
        {
            data.activeSideQuestIds = new System.Collections.Generic.List<string>();
            data.schemaVersion = 8;
        }

        private static void MigrateSchemaV8(GameSaveData data)
        {
            if (string.IsNullOrEmpty(data.endingId)) data.endingId = "";
            data.schemaVersion = 9;
        }

        private static void MigrateSchemaV9(GameSaveData data)
        {
            data.schemaVersion = 10;
        }

        private static void SanitizeInventory(System.Collections.Generic.List<InventoryStackData> inventory)
        {
            for (var i = inventory.Count - 1; i >= 0; i--)
            {
                var stack = inventory[i];
                if (stack == null || string.IsNullOrWhiteSpace(stack.itemId) || stack.quantity <= 0)
                    inventory.RemoveAt(i);
                else
                    stack.quantity = Mathf.Min(stack.quantity, 999999);
            }
        }

        private static void SanitizeEncounterProgress(System.Collections.Generic.List<EncounterProgressData> progress)
        {
            var seen = new System.Collections.Generic.HashSet<string>();
            for (var i = progress.Count - 1; i >= 0; i--)
            {
                var state = progress[i];
                if (state == null || string.IsNullOrWhiteSpace(state.encounterId) ||
                    state.encounterId.Length > 64 || !seen.Add(state.encounterId))
                {
                    progress.RemoveAt(i);
                    continue;
                }

                state.health = Mathf.Clamp(state.health, 0, 1000000);
                if (state.defeated) state.health = 0;
            }
        }

        private static void SanitizeFarmProgress(System.Collections.Generic.List<FarmPlotProgressData> progress)
        {
            var seen = new System.Collections.Generic.HashSet<string>();
            for (var i = progress.Count - 1; i >= 0; i--)
            {
                var state = progress[i];
                if (state == null || string.IsNullOrWhiteSpace(state.plotId) ||
                    string.IsNullOrWhiteSpace(state.cropId) || state.plotId.Length > 64 ||
                    state.cropId.Length > 64 || !seen.Add(state.plotId) || float.IsNaN(state.remainingSeconds) ||
                    float.IsInfinity(state.remainingSeconds))
                {
                    progress.RemoveAt(i);
                    continue;
                }

                state.remainingSeconds = Mathf.Clamp(state.remainingSeconds, 0, 86400);
            }
        }

        private static void SanitizeProgress(GameSaveData data)
        {
            if (data.activeSideQuestIds == null)
                data.activeSideQuestIds = new System.Collections.Generic.List<string>();
            var seenActiveSideQuestIds = new System.Collections.Generic.HashSet<string>();
            for (var i = data.activeSideQuestIds.Count - 1; i >= 0; i--)
            {
                var id = data.activeSideQuestIds[i];
                if (string.IsNullOrWhiteSpace(id) || id.Length > 64 || !seenActiveSideQuestIds.Add(id))
                    data.activeSideQuestIds.RemoveAt(i);
            }

            var seenQuestIds = new System.Collections.Generic.HashSet<string>();
            for (var i = data.completedQuestIds.Count - 1; i >= 0; i--)
            {
                var id = data.completedQuestIds[i];
                if (string.IsNullOrWhiteSpace(id) || !seenQuestIds.Add(id)) data.completedQuestIds.RemoveAt(i);
            }

            var flagIndexes = new System.Collections.Generic.Dictionary<string, int>();
            for (var i = data.storyFlags.Count - 1; i >= 0; i--)
            {
                var flag = data.storyFlags[i];
                if (flag == null || string.IsNullOrWhiteSpace(flag.id) || string.IsNullOrWhiteSpace(flag.value))
                {
                    data.storyFlags.RemoveAt(i);
                    continue;
                }

                if (flagIndexes.ContainsKey(flag.id)) data.storyFlags.RemoveAt(i);
                else flagIndexes.Add(flag.id, i);
            }

            for (var i = data.questObjectiveProgress.Count - 1; i >= 0; i--)
            {
                var progress = data.questObjectiveProgress[i];
                if (progress == null || string.IsNullOrWhiteSpace(progress.questId) ||
                    string.IsNullOrWhiteSpace(progress.objectiveId) || progress.count < 0)
                    data.questObjectiveProgress.RemoveAt(i);
            }
        }

        public static void Save(GameSaveData data)
        {
            try
            {
                var directory = Path.GetDirectoryName(SavePath);
                if (!string.IsNullOrEmpty(directory)) Directory.CreateDirectory(directory);
                var json = JsonUtility.ToJson(data, true);
                var temporaryPath = SavePath + ".tmp";
                File.WriteAllText(temporaryPath, json);

                if (File.Exists(SavePath))
                {
                    var backupPath = SavePath + ".bak";
                    try
                    {
                        File.Replace(temporaryPath, SavePath, backupPath, true);
                        if (File.Exists(backupPath)) File.Delete(backupPath);
                    }
                    catch (Exception replaceException) when (replaceException is PlatformNotSupportedException ||
                                                              replaceException is NotSupportedException ||
                                                              replaceException is IOException)
                    {
                        File.Copy(SavePath, backupPath, true);
                        File.Delete(SavePath);
                        File.Move(temporaryPath, SavePath);
                        if (File.Exists(backupPath)) File.Delete(backupPath);
                    }
                }
                else
                {
                    File.Move(temporaryPath, SavePath);
                }
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not write the local save: " + exception.Message);
            }
        }
    }
}
