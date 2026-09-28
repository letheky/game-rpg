using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class FarmCatalogData
    {
        public int schemaVersion;
        public List<FarmPlotDefinition> entries;
    }

    [Serializable]
    public sealed class FarmPlotDefinition
    {
        public string id;
        public string locationId;
        public float positionX;
        public float positionY;
        public string cropId;
        public string cropDisplayName;
        public string seedItemId;
        public string harvestItemId;
        public int harvestQuantity;
        public float growSeconds;
    }

    public static class FarmCatalogService
    {
        public static FarmCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/farm_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/farm_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<FarmCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load farm catalog: " + exception.Message);
                return null;
            }
        }

        public static void Validate(FarmCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Farm catalog schema or entries are invalid.");
            var ids = new HashSet<string>();
            foreach (var plot in catalog.entries)
                if (plot == null || !IsStableId(plot.id) || !ids.Add(plot.id) || !IsStableId(plot.locationId) ||
                    !IsStableId(plot.cropId) || !IsStableId(plot.seedItemId) || !IsStableId(plot.harvestItemId) ||
                    string.IsNullOrWhiteSpace(plot.cropDisplayName) || plot.cropDisplayName.Length > 48 ||
                    plot.harvestQuantity < 1 || plot.harvestQuantity > 99 || plot.growSeconds <= 0 ||
                    !IsFinite(plot.positionX) || !IsFinite(plot.positionY) || !IsFinite(plot.growSeconds))
                    throw new FormatException("Invalid farm plot definition or duplicate ID.");
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

    public static class FarmPlotProgressService
    {
        public static FarmPlotProgressData Find(GameSaveData save, string plotId)
        {
            if (save?.farmProgress == null || string.IsNullOrEmpty(plotId)) return null;
            foreach (var progress in save.farmProgress)
                if (progress != null && progress.plotId == plotId) return progress;
            return null;
        }

        public static bool TryPlant(GameSaveData save, FarmPlotDefinition plot)
        {
            if (save == null || plot == null || Find(save, plot.id) != null || save.inventory == null ||
                !InventoryService.Remove(save, plot.seedItemId, 1)) return false;
            if (save.farmProgress == null) save.farmProgress = new List<FarmPlotProgressData>();
            save.farmProgress.Add(new FarmPlotProgressData
            {
                plotId = plot.id,
                cropId = plot.cropId,
                remainingSeconds = plot.growSeconds
            });
            return true;
        }

        /// <returns>True when one or more crops become ready.</returns>
        public static bool Tick(GameSaveData save, float elapsedSeconds)
        {
            if (save?.farmProgress == null || elapsedSeconds <= 0 || float.IsNaN(elapsedSeconds) ||
                float.IsInfinity(elapsedSeconds)) return false;
            var becameReady = false;
            foreach (var progress in save.farmProgress)
            {
                if (progress == null || progress.remainingSeconds <= 0) continue;
                progress.remainingSeconds = Mathf.Max(0, progress.remainingSeconds - elapsedSeconds);
                if (progress.remainingSeconds <= 0) becameReady = true;
            }
            return becameReady;
        }

        public static bool TryHarvest(GameSaveData save, FarmPlotDefinition plot)
        {
            var progress = Find(save, plot == null ? "" : plot.id);
            if (save?.farmProgress == null || plot == null || progress == null || progress.cropId != plot.cropId ||
                progress.remainingSeconds > 0 || ItemCatalog.Find(plot.harvestItemId) == null) return false;
            if (InventoryService.Add(save, plot.harvestItemId, plot.harvestQuantity) != plot.harvestQuantity) return false;
            save.farmProgress.Remove(progress);
            return true;
        }
    }
}
