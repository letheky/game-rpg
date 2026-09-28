using System;
using System.Collections.Generic;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class MonsterCatalogData
    {
        public int schemaVersion;
        public List<MonsterDefinition> entries;
    }

    [Serializable]
    public sealed class MonsterDefinition
    {
        public string id;
        public string displayName;
        public string rank;
        public int maxHealth;
        public int attackDamage;
        public float attackReach;
        public float approachSpeed;
        public float lungeDistance;
        public float lungeSeconds;
        public float lungeStopDistance;
        public float openingDelay;
        public float closingSeconds;
        public float telegraphSeconds;
        public float recoverySeconds;
        public int counterBonusDamage;
        public float hitCooldown;
        public string spriteResource;
        public string lungeSpriteResource;
        public float spriteScale;
        public float spritePixelsPerUnit;
        public string specialMoveId;
        public float specialMoveReach;
    }

    /// <summary>Versioned, content-only monster definitions. Encounter placement stays in the world scene for now.</summary>
    public static class MonsterCatalogService
    {
        private static readonly HashSet<string> SpecialMoveIds = new HashSet<string>
        {
            "shockwave", "siphon", "hook", "line_charge", "ranged_bolt", "marked_strike"
        };

        public static MonsterCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/monster_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/monster_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<MonsterCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load monster catalog: " + exception.Message);
                return null;
            }
        }

        public static MonsterDefinition FindById(MonsterCatalogData catalog, string id)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(id)) return null;
            foreach (var monster in catalog.entries)
                if (monster != null && monster.id == id) return monster;
            return null;
        }

        public static void Validate(MonsterCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Monster catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var monster in catalog.entries)
            {
                if (monster == null || !IsStableId(monster.id) || !ids.Add(monster.id) ||
                    string.IsNullOrWhiteSpace(monster.displayName) ||
                    (monster.rank != "common" && monster.rank != "elite" && monster.rank != "boss") || monster.maxHealth < 1 ||
                    monster.attackDamage < 1 || monster.attackReach <= 0 || monster.approachSpeed <= 0 ||
                    monster.lungeDistance <= 0 || monster.lungeSeconds <= 0 || monster.lungeStopDistance < 0 ||
                    monster.openingDelay < 0 ||
                    monster.closingSeconds <= 0 ||
                    monster.telegraphSeconds <= 0 || monster.recoverySeconds <= 0 ||
                    monster.counterBonusDamage < 0 || monster.hitCooldown <= 0 ||
                    !IsStableId(monster.spriteResource) ||
                    (!string.IsNullOrEmpty(monster.lungeSpriteResource) && !IsStableId(monster.lungeSpriteResource)) ||
                    monster.spriteScale <= 0 ||
                    monster.spritePixelsPerUnit < 0 ||
                    (!string.IsNullOrEmpty(monster.specialMoveId) &&
                     (!IsStableId(monster.specialMoveId) || !SpecialMoveIds.Contains(monster.specialMoveId))) ||
                    ((monster.specialMoveId == "shockwave" || monster.specialMoveId == "siphon" ||
                      monster.specialMoveId == "hook" || monster.specialMoveId == "line_charge" ||
                      monster.specialMoveId == "ranged_bolt" || monster.specialMoveId == "marked_strike") &&
                     monster.specialMoveReach <= monster.attackReach) ||
                    (string.IsNullOrEmpty(monster.specialMoveId) && monster.specialMoveReach != 0) ||
                    float.IsNaN(monster.attackReach) || float.IsInfinity(monster.attackReach) ||
                    float.IsNaN(monster.approachSpeed) || float.IsInfinity(monster.approachSpeed) ||
                    float.IsNaN(monster.lungeDistance) || float.IsInfinity(monster.lungeDistance) ||
                    float.IsNaN(monster.lungeSeconds) || float.IsInfinity(monster.lungeSeconds) ||
                    float.IsNaN(monster.lungeStopDistance) || float.IsInfinity(monster.lungeStopDistance) ||
                    float.IsNaN(monster.openingDelay) || float.IsInfinity(monster.openingDelay) ||
                    float.IsNaN(monster.closingSeconds) || float.IsInfinity(monster.closingSeconds) ||
                    float.IsNaN(monster.telegraphSeconds) || float.IsInfinity(monster.telegraphSeconds) ||
                    float.IsNaN(monster.recoverySeconds) || float.IsInfinity(monster.recoverySeconds) ||
                    float.IsNaN(monster.hitCooldown) || float.IsInfinity(monster.hitCooldown) ||
                    float.IsNaN(monster.spriteScale) || float.IsInfinity(monster.spriteScale) ||
                    float.IsNaN(monster.spritePixelsPerUnit) || float.IsInfinity(monster.spritePixelsPerUnit) ||
                    float.IsNaN(monster.specialMoveReach) || float.IsInfinity(monster.specialMoveReach))
                    throw new FormatException("Invalid monster definition or duplicate ID.");
            }
        }

        private static bool IsStableId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 64 || value[0] < 'a' || value[0] > 'z')
                return false;

            foreach (var character in value)
                if (!((character >= 'a' && character <= 'z') || (character >= '0' && character <= '9') || character == '_'))
                    return false;
            return true;
        }
    }

    /// <summary>Shared attack-shape rules for runtime damage and editor validation.</summary>
    public static class MonsterCombatRules
    {
        public static bool IsLaneAttack(string moveId) =>
            moveId == "line_charge" || moveId == "ranged_bolt";

        public static bool IsMarkedStrike(string moveId) => moveId == "marked_strike";

        public static bool IsAreaAttack(string moveId) =>
            moveId == "shockwave" || moveId == "siphon" || moveId == "hook" || moveId == "marked_strike";

        public static bool HoldsPositionDuringAttack(string moveId) =>
            IsAreaAttack(moveId) || moveId == "ranged_bolt";

        public static float EffectiveReach(MonsterDefinition monster)
        {
            if (monster == null) return 0;
            return IsAreaAttack(monster.specialMoveId) ? monster.specialMoveReach : monster.attackReach;
        }

        public static bool IsPointInsideLane(Vector2 point, Vector2 origin, Vector2 direction,
            float length, float halfWidth)
        {
            if (direction.sqrMagnitude <= 0.001f || length <= 0) return false;
            var lane = direction.normalized * length;
            var offset = point - origin;
            var along = Mathf.Clamp01(Vector2.Dot(offset, lane) / lane.sqrMagnitude);
            var closestPoint = origin + lane * along;
            return Vector2.Distance(point, closestPoint) <= Mathf.Max(0.7f, halfWidth);
        }

        public static bool IsPointInsideMarkedStrike(Vector2 point, Vector2 target, float radius) =>
            radius > 0 && (point - target).sqrMagnitude <= radius * radius;
    }
}
