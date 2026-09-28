using UnityEngine;

namespace AshenOath.Core
{
    /// <summary>Small, deterministic inventory operations over the offline save model.</summary>
    public static class InventoryService
    {
        public static int Count(GameSaveData save, string itemId)
        {
            if (save == null || save.inventory == null) return 0;
            var total = 0;
            foreach (var stack in save.inventory)
                if (stack != null && stack.itemId == itemId) total += Mathf.Max(0, stack.quantity);
            return total;
        }

        public static int Add(GameSaveData save, string itemId, int quantity)
        {
            var definition = ItemCatalog.Find(itemId);
            if (save == null || save.inventory == null || definition == null || quantity <= 0) return 0;

            var remaining = quantity;
            foreach (var stack in save.inventory)
            {
                if (stack == null || stack.itemId != itemId || stack.quantity >= definition.maxStack) continue;
                var amount = Mathf.Min(remaining, definition.maxStack - stack.quantity);
                stack.quantity += amount;
                remaining -= amount;
                if (remaining == 0) return quantity;
            }

            while (remaining > 0)
            {
                var amount = Mathf.Min(remaining, definition.maxStack);
                save.inventory.Add(new InventoryStackData { itemId = itemId, quantity = amount });
                remaining -= amount;
            }

            return quantity;
        }

        public static bool Remove(GameSaveData save, string itemId, int quantity)
        {
            if (save == null || save.inventory == null || quantity <= 0 || Count(save, itemId) < quantity) return false;
            var remaining = quantity;
            for (var i = save.inventory.Count - 1; i >= 0 && remaining > 0; i--)
            {
                var stack = save.inventory[i];
                if (stack == null || stack.itemId != itemId) continue;
                var amount = Mathf.Min(remaining, stack.quantity);
                stack.quantity -= amount;
                remaining -= amount;
                if (stack.quantity <= 0) save.inventory.RemoveAt(i);
            }

            return remaining == 0;
        }

        public static bool TryEquip(GameSaveData save, string itemId)
        {
            var item = ItemCatalog.Find(itemId);
            if (save == null || item == null || item.category != "equipment" || Count(save, itemId) == 0) return false;

            switch (item.equipmentSlot)
            {
                case "weapon": save.weaponId = item.id; return true;
                case "armor": save.armorId = item.id; return true;
                case "charm": save.charmId = item.id; return true;
                default: return false;
            }
        }

        public static string EquippedId(GameSaveData save, string slot)
        {
            if (save == null) return "";
            switch (slot)
            {
                case "weapon": return save.weaponId;
                case "armor": return save.armorId;
                case "charm": return save.charmId;
                default: return "";
            }
        }

        public static bool IsEquipped(GameSaveData save, ItemDefinition item)
        {
            return item != null && item.category == "equipment" && EquippedId(save, item.equipmentSlot) == item.id;
        }

        public static int AttackBonus(GameSaveData save)
        {
            var weapon = ItemCatalog.Find(save == null ? "" : save.weaponId);
            var charm = ItemCatalog.Find(save == null ? "" : save.charmId);
            return (weapon == null ? 0 : weapon.attackBonus) + (charm == null ? 0 : charm.attackBonus);
        }

        public static int GuardBonus(GameSaveData save)
        {
            var armor = ItemCatalog.Find(save == null ? "" : save.armorId);
            var charm = ItemCatalog.Find(save == null ? "" : save.charmId);
            return (armor == null ? 0 : armor.guardBonus) + (charm == null ? 0 : charm.guardBonus);
        }

        public static int HealAmount(string itemId)
        {
            var item = ItemCatalog.Find(itemId);
            return item == null ? 0 : item.healAmount;
        }
    }
}
