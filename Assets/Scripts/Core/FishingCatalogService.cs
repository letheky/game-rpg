using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class FishingCatalogData
    {
        public int schemaVersion;
        public List<FishingSpotDefinition> entries;
    }

    [Serializable]
    public sealed class FishingSpotDefinition
    {
        public string id;
        public string locationId;
        public string displayName;
        public float positionX;
        public float positionY;
        public string baitItemId;
        public float biteDelayMinSeconds;
        public float biteDelayMaxSeconds;
        public float biteWindowSeconds;
        public List<FishingCatchDefinition> catches;
    }

    [Serializable]
    public sealed class FishingCatchDefinition
    {
        public string itemId;
        public float weight;
    }

    public static class FishingCatalogService
    {
        public static FishingCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/fishing_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/fishing_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<FishingCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load fishing catalog: " + exception.Message);
                return null;
            }
        }

        public static void Validate(FishingCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Fishing catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var spot in catalog.entries)
            {
                if (spot == null || !IsStableId(spot.id) || !ids.Add(spot.id) || !IsStableId(spot.locationId) ||
                    !IsStableId(spot.baitItemId) || spot.catches == null || spot.catches.Count == 0 ||
                    spot.biteDelayMinSeconds < 0 || spot.biteDelayMaxSeconds < spot.biteDelayMinSeconds ||
                    spot.biteWindowSeconds <= 0 || !IsFinite(spot.positionX) || !IsFinite(spot.positionY) ||
                    !IsFinite(spot.biteDelayMinSeconds) || !IsFinite(spot.biteDelayMaxSeconds) ||
                    !IsFinite(spot.biteWindowSeconds))
                    throw new FormatException("Invalid fishing spot or duplicate ID.");

                var catchIds = new HashSet<string>();
                foreach (var fish in spot.catches)
                {
                    if (fish == null || !IsStableId(fish.itemId) || !catchIds.Add(fish.itemId) ||
                        fish.weight <= 0 || !IsFinite(fish.weight))
                        throw new FormatException("Invalid or duplicate fish catch in " + spot.id + ".");
                }
            }
        }

        public static string RollCatch(FishingSpotDefinition spot, float normalizedRoll)
        {
            if (spot?.catches == null || spot.catches.Count == 0) return "";
            var totalWeight = 0f;
            foreach (var fish in spot.catches) totalWeight += fish.weight;
            var roll = Mathf.Clamp01(normalizedRoll) * totalWeight;
            foreach (var fish in spot.catches)
            {
                roll -= fish.weight;
                if (roll < 0) return fish.itemId;
            }
            return spot.catches[spot.catches.Count - 1].itemId;
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
