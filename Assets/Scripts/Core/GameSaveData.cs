using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class GameSaveData
    {
        public int schemaVersion = 10;
        public bool started;
        // Deprecated stage mirror; QuestProgressService reconciles it into stable IDs for old saves.
        public int questStage;
        public int health = 48;
        public int gold = 12;
        // Kept only so SaveService can migrate schema v1 saves without losing items.
        public int potions = 1;
        public int wargFangs;
        // Legacy mirrors retained as migration input for save schemas v1-v5.
        public int wargHealth = 36;
        public bool wargDefeated;
        public List<EncounterProgressData> encounterProgress = new List<EncounterProgressData>();
        public List<FarmPlotProgressData> farmProgress = new List<FarmPlotProgressData>();
        // Compatibility mirror for saves from schemas v1-v3. New choices also live in storyFlags.
        public string firstChoice = "";
        public bool chapterComplete;
        public string activeQuestId = "";
        public List<string> activeSideQuestIds = new List<string>();
        public List<string> completedQuestIds = new List<string>();
        public List<StoryFlagData> storyFlags = new List<StoryFlagData>();
        public List<QuestObjectiveProgressData> questObjectiveProgress = new List<QuestObjectiveProgressData>();
        public float playerX = -5f;
        public float playerY = -3.5f;
        public string locationId = "ashfall_village";
        public string endingId = "";
        public List<InventoryStackData> inventory = new List<InventoryStackData>();
        public string weaponId = "practice_sword";
        public string armorId = "";
        public string charmId = "";
    }

    [Serializable]
    public sealed class InventoryStackData
    {
        public string itemId;
        public int quantity;
    }

    [Serializable]
    public sealed class StoryFlagData
    {
        public string id;
        public string value;
    }

    [Serializable]
    public sealed class QuestObjectiveProgressData
    {
        public string questId;
        public string objectiveId;
        public int count;
    }

    [Serializable]
    public sealed class EncounterProgressData
    {
        public string encounterId;
        public int health;
        public bool defeated;
    }

    [Serializable]
    public sealed class FarmPlotProgressData
    {
        public string plotId;
        public string cropId;
        public float remainingSeconds;
    }
}
