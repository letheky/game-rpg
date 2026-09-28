using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class ItemDefinition
    {
        public string id;
        public string name;
        public string description;
        public string category;
        public string equipmentSlot;
        public int maxStack = 99;
        public int attackBonus;
        public int guardBonus;
        public int healAmount;
        public int sellValue;
    }

    [Serializable]
    public sealed class ItemCatalogData
    {
        public int schemaVersion;
        public List<ItemDefinition> entries;
    }

    /// <summary>Loads and validates stable item IDs used by rewards, inventory and equipment.</summary>
    public static class ItemCatalog
    {
        private static readonly Dictionary<string, ItemDefinition> items = new Dictionary<string, ItemDefinition>();
        private static ItemCatalogData catalog;

        public static IReadOnlyList<ItemDefinition> Entries => catalog == null ? Array.Empty<ItemDefinition>() : catalog.entries;

        public static bool Load()
        {
            items.Clear();
            catalog = null;
            var asset = Resources.Load<TextAsset>("Content/item_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/item_catalog.json.");
                return false;
            }

            try
            {
                catalog = JsonUtility.FromJson<ItemCatalogData>(asset.text);
                if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null)
                    throw new FormatException("Item catalog schema or entries are invalid.");

                foreach (var item in catalog.entries)
                {
                    if (item == null || string.IsNullOrWhiteSpace(item.id) ||
                        string.IsNullOrWhiteSpace(item.name) || string.IsNullOrWhiteSpace(item.category))
                        throw new FormatException("Every item requires an ID, name and category.");
                    if (item.maxStack < 1 || item.sellValue < 0 || item.healAmount < 0)
                        throw new FormatException("Item stack, price or healing values are outside the valid range: " + item.id);
                    if (items.ContainsKey(item.id))
                        throw new FormatException("Duplicate item ID: " + item.id);
                    if (item.category == "equipment" &&
                        item.equipmentSlot != "weapon" && item.equipmentSlot != "armor" && item.equipmentSlot != "charm")
                        throw new FormatException("Equipment item has an unknown slot: " + item.id);

                    items.Add(item.id, item);
                }

                return true;
            }
            catch (Exception exception)
            {
                items.Clear();
                catalog = null;
                Debug.LogError("Could not load item catalog: " + exception.Message);
                return false;
            }
        }

        public static ItemDefinition Find(string id)
        {
            if (string.IsNullOrEmpty(id)) return null;
            return items.TryGetValue(id, out var item) ? item : null;
        }

        public static bool IsLoaded => catalog != null && items.Count == catalog.entries.Count;
    }
}
