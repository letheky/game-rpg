using System.Collections.Generic;

namespace AshenOath.Core
{
    /// <summary>Single source of truth for offline locations accepted by travel and save migration.</summary>
    public static class GameLocationService
    {
        private static readonly HashSet<string> PlayableLocationIds = new HashSet<string>
        {
            "ashfall_village",
            "dawnkeep_outpost",
            "dawnkeep_barracks",
            "cinderwell_basin",
            "cinder_cistern",
            "salt_road",
            "salt_lockhouse",
            "choir_beneath_lake",
            "greenwake_refuge",
            "outerwake_archive",
            "last_oath_reach"
        };

        public static bool IsPlayable(string locationId)
        {
            return !string.IsNullOrEmpty(locationId) && PlayableLocationIds.Contains(locationId);
        }
    }
}
