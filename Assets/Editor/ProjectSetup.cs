using System.IO;
using System.Collections.Generic;
using AshenOath.Core;
using AshenOath.World;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace AshenOath.Editor
{
    public static class ProjectSetup
    {
        private const string MainScenePath = "Assets/Scenes/Main.unity";

        [MenuItem("Ashen Oath/Validate Item and Inventory Data")]
        public static void ValidateItemAndInventoryData()
        {
            if (!ItemCatalog.Load())
                throw new System.InvalidOperationException("Item catalog validation failed. See the Console for details.");

            var inventory = new GameSaveData
            {
                inventory = new List<InventoryStackData>(),
                locationId = "dawnkeep_outpost"
            };
            Require(InventoryService.Add(inventory, "healing_tonic", 23) == 23, "Add must accept valid stackable items.");
            Require(InventoryService.Count(inventory, "healing_tonic") == 23, "Stack counts must include overflow stacks.");
            Require(InventoryService.Remove(inventory, "healing_tonic", 22), "Remove must consume an available quantity.");
            Require(InventoryService.Count(inventory, "healing_tonic") == 1, "Remove must preserve the remaining quantity.");
            Require(!InventoryService.Remove(inventory, "healing_tonic", 2), "Remove must reject insufficient quantities.");

            InventoryService.Add(inventory, "trailbreaker_sword", 1);
            InventoryService.Add(inventory, "survivor_mantle", 1);
            Require(InventoryService.TryEquip(inventory, "trailbreaker_sword"), "Owned weapons must equip.");
            Require(InventoryService.TryEquip(inventory, "survivor_mantle"), "Owned armor must equip.");
            Require(InventoryService.AttackBonus(inventory) == 2, "Equipped weapons must affect attack power.");
            Require(InventoryService.GuardBonus(inventory) == 2, "Equipped armor must affect guard.");
            Require(!InventoryService.TryEquip(inventory, "missing_item"), "Missing items must not equip.");

            var serialized = JsonUtility.ToJson(inventory);
            inventory.encounterProgress.Add(new EncounterProgressData
                { encounterId = "dawnkeep_sparring", health = 19, defeated = false });
            serialized = JsonUtility.ToJson(inventory);
            var restored = JsonUtility.FromJson<GameSaveData>(serialized);
            Require(InventoryService.Count(restored, "healing_tonic") == 1 &&
                    restored.weaponId == "trailbreaker_sword" && restored.armorId == "survivor_mantle" &&
                    restored.locationId == "dawnkeep_outpost" && restored.encounterProgress.Count == 1 &&
                    restored.encounterProgress[0].health == 19,
                "Inventory, equipment, world location and partial encounter health must survive JSON serialization.");
            var encounterRoundTrip = EncounterProgressService.GetOrCreate(restored,
                new EncounterDefinition { id = "dawnkeep_sparring" }, new MonsterDefinition { maxHealth = 44 });
            Require(encounterRoundTrip.health == 19,
                "Encounter records must resume their saved health instead of resetting to the species maximum.");

            var legacy = new GameSaveData { schemaVersion = 1, potions = 2, wargFangs = 3 };
            Require(SaveService.TryUpgradeToCurrent(legacy), "Schema v1 save must migrate to the current schema.");
            Require(legacy.schemaVersion == 10 && InventoryService.Count(legacy, "healing_tonic") == 2 &&
                    InventoryService.Count(legacy, "ash_warg_fang") == 3 &&
                    InventoryService.Count(legacy, "practice_sword") == 1 &&
                    InventoryService.Count(legacy, "earthworm_bait") == 3 &&
                    InventoryService.Count(legacy, "moonwort_seed") == 3 &&
                    legacy.encounterProgress.Count == 1 && legacy.encounterProgress[0].encounterId == "ash_warg_yard",
                "Schema v1 save must migrate through v2-v9 and preserve inventory, starter supplies and the Warg encounter.");
            var saveV2 = new GameSaveData { schemaVersion = 2, questStage = 3, firstChoice = "trail" };
            Require(SaveService.TryUpgradeToCurrent(saveV2) && saveV2.schemaVersion == 10 &&
                    saveV2.questStage == 3 && saveV2.firstChoice == "trail",
                "Schema v2 migration must preserve the selected story branch and current progress.");
            var saveV3 = new GameSaveData { schemaVersion = 3, questStage = 4, firstChoice = "trail" };
            Require(SaveService.TryUpgradeToCurrent(saveV3) && saveV3.schemaVersion == 10 &&
                    saveV3.questStage == 4 && saveV3.firstChoice == "trail",
                "Schema v3 migration must preserve legacy stage progress for ID reconciliation.");
            var saveV4 = new GameSaveData { schemaVersion = 4, locationId = "dawnkeep_outpost" };
            Require(SaveService.TryUpgradeToCurrent(saveV4) && saveV4.schemaVersion == 10 &&
                    saveV4.locationId == "ashfall_village",
                "Schema v4 migration must preserve its safe starting map as saves gain encounter progress.");
            var cinderLocationSave = new GameSaveData { schemaVersion = 7, locationId = "cinderwell_basin" };
            var cinderCisternLocationSave = new GameSaveData { schemaVersion = 9, locationId = "cinder_cistern" };
            var barracksLocationSave = new GameSaveData { schemaVersion = 9, locationId = "dawnkeep_barracks" };
            var saltRoadLocationSave = new GameSaveData { schemaVersion = 7, locationId = "salt_road" };
            var saltLockhouseLocationSave = new GameSaveData { schemaVersion = 9, locationId = "salt_lockhouse" };
            var choirLocationSave = new GameSaveData { schemaVersion = 7, locationId = "choir_beneath_lake" };
            var greenwakeLocationSave = new GameSaveData { schemaVersion = 7, locationId = "greenwake_refuge" };
            var outerwakeLocationSave = new GameSaveData { schemaVersion = 8, locationId = "outerwake_archive" };
            var lastOathLocationSave = new GameSaveData
                { schemaVersion = 8, locationId = "last_oath_reach", endingId = "beyond_the_veil" };
            var unknownLocationSave = new GameSaveData { schemaVersion = 7, locationId = "missing_map" };
            Require(SaveService.TryUpgradeToCurrent(cinderLocationSave) &&
                    cinderLocationSave.locationId == "cinderwell_basin" &&
                    SaveService.TryUpgradeToCurrent(cinderCisternLocationSave) &&
                    cinderCisternLocationSave.locationId == "cinder_cistern" &&
                    SaveService.TryUpgradeToCurrent(barracksLocationSave) && barracksLocationSave.schemaVersion == 10 &&
                    barracksLocationSave.locationId == "dawnkeep_barracks" &&
                    SaveService.TryUpgradeToCurrent(saltRoadLocationSave) && saltRoadLocationSave.locationId == "salt_road" &&
                    SaveService.TryUpgradeToCurrent(saltLockhouseLocationSave) && saltLockhouseLocationSave.locationId == "salt_lockhouse" &&
                    SaveService.TryUpgradeToCurrent(choirLocationSave) && choirLocationSave.locationId == "choir_beneath_lake" &&
                    SaveService.TryUpgradeToCurrent(greenwakeLocationSave) && greenwakeLocationSave.locationId == "greenwake_refuge" &&
                    SaveService.TryUpgradeToCurrent(outerwakeLocationSave) && outerwakeLocationSave.locationId == "outerwake_archive" &&
                    SaveService.TryUpgradeToCurrent(lastOathLocationSave) && lastOathLocationSave.schemaVersion == 10 &&
                    lastOathLocationSave.locationId == "last_oath_reach" && lastOathLocationSave.endingId == "beyond_the_veil" &&
                    SaveService.TryUpgradeToCurrent(unknownLocationSave) && unknownLocationSave.locationId == "ashfall_village",
                "Save validation must preserve all eleven locations and an existing ending while recovering invalid map IDs safely.");
            var playableLocationIds = new[]
            {
                "ashfall_village", "dawnkeep_outpost", "dawnkeep_barracks", "cinderwell_basin",
                "cinder_cistern", "salt_road", "salt_lockhouse", "choir_beneath_lake",
                "greenwake_refuge", "outerwake_archive", "last_oath_reach"
            };
            foreach (var locationId in playableLocationIds)
                Require(GameLocationService.IsPlayable(locationId),
                    "Travel and saves must accept every authored location: " + locationId);
            Require(!GameLocationService.IsPlayable("missing_map") && !GameLocationService.IsPlayable(null),
                "Travel and saves must reject unknown or empty location IDs.");
            var saveV5 = new GameSaveData { schemaVersion = 5, wargHealth = 17, wargDefeated = false };
            Require(SaveService.TryUpgradeToCurrent(saveV5) && saveV5.schemaVersion == 10 &&
                    saveV5.encounterProgress.Count == 1 && saveV5.encounterProgress[0].encounterId == "ash_warg_yard" &&
                    saveV5.encounterProgress[0].health == 17 && !saveV5.encounterProgress[0].defeated &&
                    InventoryService.Count(saveV5, "earthworm_bait") == 3 &&
                    InventoryService.Count(saveV5, "moonwort_seed") == 3,
                "Schema v5 migration must preserve the Warg's health and grant the activity starter supplies.");
            var defeatedV5 = new GameSaveData { schemaVersion = 5, wargHealth = 0, wargDefeated = true };
            Require(SaveService.TryUpgradeToCurrent(defeatedV5) && defeatedV5.encounterProgress[0].defeated,
                "Schema v5 migration must keep a defeated Warg from respawning under its new encounter ID.");
            var saveV6 = new GameSaveData
            {
                schemaVersion = 6,
                inventory = new List<InventoryStackData> { new InventoryStackData { itemId = "moonwort_seed", quantity = 2 } },
                farmProgress = new List<FarmPlotProgressData>
                {
                    new FarmPlotProgressData { plotId = "ashfall_herb_bed", cropId = "moonwort", remainingSeconds = 41.5f }
                }
            };
            Require(SaveService.TryUpgradeToCurrent(saveV6) && saveV6.schemaVersion == 10 &&
                    InventoryService.Count(saveV6, "moonwort_seed") == 2 && saveV6.farmProgress.Count == 1 &&
                    Mathf.Approximately(saveV6.farmProgress[0].remainingSeconds, 41.5f),
                "Schema v6 migration must preserve a growing crop and avoid duplicating existing seeds.");
            var emptySaveV6 = new GameSaveData { schemaVersion = 6 };
            Require(SaveService.TryUpgradeToCurrent(emptySaveV6) &&
                    InventoryService.Count(emptySaveV6, "moonwort_seed") == 3,
                "Schema v6 migration must supply starter Moonwort seeds to an existing save.");
            var saveV7 = new GameSaveData { schemaVersion = 7, activeSideQuestIds = null };
            Require(SaveService.TryUpgradeToCurrent(saveV7) && saveV7.schemaVersion == 10 &&
                    saveV7.activeSideQuestIds != null && saveV7.activeSideQuestIds.Count == 0,
                "Schema v7 migration must initialize the accepted side quest list without changing old progress.");

            var questCatalog = QuestCatalogService.Load();
            Require(questCatalog != null && questCatalog.entries.Count == 1001 &&
                    ItemCatalog.Entries.Count == 360 &&
                    QuestCatalogService.FindById(questCatalog, "choir_reckoning") != null &&
                    QuestCatalogService.FindById(questCatalog, "champion_offer")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "champion_star_map") != null &&
                    QuestCatalogService.FindById(questCatalog, "archive_return_report") != null &&
                    QuestCatalogService.FindById(questCatalog, "last_oath_arrival") != null &&
                    QuestCatalogService.FindById(questCatalog, "last_oath_cycle_boss") != null &&
                    QuestCatalogService.FindById(questCatalog, "last_oath_beyond_epilogue") != null &&
                    QuestCatalogService.FindById(questCatalog, "order_cinderwell_dispatch") != null &&
                    CountQuestType(questCatalog, "story") == 117 && CountQuestType(questCatalog, "side") == 884 &&
                    CountQuestArc(questCatalog, "ashes_of_ashfall", "side") == 113 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_herb_ledger") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_blackreed_record") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_brew_moonlight") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_remedy_shelf") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_policy_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_clinic_sign")?.branchValue == "open_room" &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_kit_mark")?.branchValue == "field_kit" &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_first_shift")?.prerequisiteGroups.Count == 1 &&
                    QuestCatalogService.FindById(questCatalog, "side_mira_ash_house_afterword") != null &&
                    ItemCatalog.Find("emberlily_seed")?.category == "material" &&
                    ItemCatalog.Find("mira_emberlily_balm")?.healAmount == 52 &&
                    ItemCatalog.Find("emberlily_window_charm")?.equipmentSlot == "charm" &&
                    ItemCatalog.Find("mira_runner_knot_charm")?.equipmentSlot == "charm" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_two_bells_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_two_bells_choose")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_muster_open")?.prerequisiteGroups.Count == 1 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_muster_board") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_blank_rows") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_shelter_cloth") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_departure_plan")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_cart_offer") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_cart_policy")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_cart_communal_report")?.branchValue == "shared" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_cart_household_report")?.branchValue == "household" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_cart_afterword")?.prerequisiteGroups.Count == 1 &&
                    ItemCatalog.Find("ashfall_cart_axle_pin")?.category == "material" &&
                    ItemCatalog.Find("ashfall_shared_cart_charm")?.equipmentSlot == "charm" &&
                    ItemCatalog.Find("ashfall_household_repair_charm")?.equipmentSlot == "charm" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_two_bells_bell_report")?.branchValue == "audible" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_two_bells_flag_report")?.branchValue == "visible" &&
                    ItemCatalog.Find("ashfall_shared_map_pin")?.equipmentSlot == "charm" &&
                    ItemCatalog.Find("ashfall_household_route_knot")?.equipmentSlot == "charm" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_tally_disclosure")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_tally_public_copy")?.branchValue == "public" &&
                    QuestCatalogService.FindById(questCatalog, "side_ashfall_tally_sealed_copy")?.branchValue == "sealed" &&
                    QuestCatalogService.FindById(questCatalog, "side_waymarks_ashfall")?.objectives.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_waymarks_distribution")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_waymarks_public_copy")?.branchValue == "public_route" &&
                    QuestCatalogService.FindById(questCatalog, "side_waymarks_courier_copy")?.branchValue == "courier_route" &&
                    CountQuestArc(questCatalog, "the_hundredth_champion", "side") == 82 &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_access_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_open_tallies")?.branchValue == "public" &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_household_copies")?.branchValue == "restricted" &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_public_appeal")?.branchFlag == "greenwake_seed_access" &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_private_corrections")?.branchFlag == "greenwake_seed_access" &&
                    QuestCatalogService.FindById(questCatalog, "side_greenwake_seed_review")?.prerequisiteGroups.Count == 1 &&
                    ItemCatalog.Find("greenwake_open_sowing_charm")?.equipmentSlot == "charm" &&
                    CountQuestArc(questCatalog, "crown_of_empty_fields", "story") == 15 &&
                    CountQuestArc(questCatalog, "crown_of_empty_fields", "side") == 106 &&
                    CountQuestArc(questCatalog, "the_salt_road", "story") == 16 &&
                    CountQuestArc(questCatalog, "the_salt_road", "side") == 129 &&
                    QuestCatalogService.FindById(questCatalog, "side_ruth_recall_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_ruth_recall_afterword") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_nella_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_nella_afterword") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_june_pantry_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_june_pantry_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_june_pantry_afterword")?.prerequisiteGroups.Count == 1 &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_open") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_exchange")?.branchValue == "open_exchange" &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_reserve")?.branchValue == "winter_case" &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_custody")?.prerequisiteGroups.Count == 1 &&
                    QuestCatalogService.FindById(questCatalog, "side_oren_seed_tin_afterword") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_saltroad_signal_policy")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_saltroad_dayline_record")?.branchValue == "dayline" &&
                    QuestCatalogService.FindById(questCatalog, "side_saltroad_callkeeper_rota")?.branchValue == "night_call" &&
                    QuestCatalogService.FindById(questCatalog, "salt_arrival")?.prerequisiteIds[0] == "cinder_june_report" &&
                    QuestCatalogService.FindById(questCatalog, "choir_arrival")?.prerequisiteIds[0] == "salt_route_handoff" &&
                    CountQuestArc(questCatalog, "the_choir_beneath_the_lake", "side") == 96 &&
                    QuestCatalogService.FindById(questCatalog, "side_choir_voice_consent")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_choir_shared_copy")?.branchValue == "share" &&
                    QuestCatalogService.FindById(questCatalog, "side_choir_private_copy")?.branchValue == "defer" &&
                    CountQuestArc(questCatalog, "the_order_of_the_dawn", "side") == 90 &&
                    CountQuestArc(questCatalog, "archive_beyond_veil", "side") == 87 &&
                    QuestCatalogService.FindById(questCatalog, "side_dawnkeep_waterline") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_dawnkeep_nia_report") != null &&
                    QuestCatalogService.FindById(questCatalog, "side_barracks_copy_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_barracks_aggregate_copy")?.branchValue == "aggregate" &&
                    QuestCatalogService.FindById(questCatalog, "side_barracks_sealed_packets")?.branchValue == "defer" &&
                    QuestCatalogService.FindById(questCatalog, "side_cinderwell_record_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_cinderwell_named_schedule")?.branchValue == "consented_households" &&
                    QuestCatalogService.FindById(questCatalog, "side_cinderwell_aggregate_schedule")?.branchValue == "aggregate_only" &&
                    QuestCatalogService.FindById(questCatalog, "side_cistern_wheel_policy")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_cistern_wheel_shared_rill")?.branchValue == "shared_rill" &&
                    QuestCatalogService.FindById(questCatalog, "side_cistern_wheel_steward_shift")?.branchValue == "steward_shift" &&
                    QuestCatalogService.FindById(questCatalog, "side_outerwake_reply_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_outerwake_bounded_echo")?.branchValue == "bounded_echo" &&
                    QuestCatalogService.FindById(questCatalog, "side_outerwake_listen_only")?.branchValue == "listen_only" &&
                    CountQuestArc(questCatalog, "two_last_oaths", "side") == 181 &&
                    QuestCatalogService.FindById(questCatalog, "side_last_oath_watch_policy")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "side_last_oath_watch_named_copy")?.branchValue == "named_optin" &&
                    QuestCatalogService.FindById(questCatalog, "side_last_oath_watch_household_copy")?.branchValue == "household_copy",
                "The catalogs must include eight connected story arcs, both endings, regional evidence chains, six optional boss contracts, fifty-eight Tiny Creatures species, sixteen additional elite contracts, fifty-four Verdant Memory species, fifty-five Crawl field species across twenty-two contracts, and 884 side quests.");
            ValidateGreenwakeSeedAccessRoutes(questCatalog);
            var codexCatalog = CodexCatalogService.Load(questCatalog);
            Require(codexCatalog != null && codexCatalog.entries.Count >= 734 &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_mira_dose_card") &&
                    codexCatalog.entries.Exists(entry => entry.id == "mira_ash_house_open_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "mira_ash_house_afterword_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "oren_seed_tin_open_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "oren_seed_tin_afterword_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_cart_afterword_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_muster_board_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_shelter_cloth_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_route_copy_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_chalk_tally_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "ashfall_sealed_tally_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "waymarks_public_route_charter") &&
                    codexCatalog.entries.Exists(entry => entry.id == "waymarks_courier_custody_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinderwell_named_ration_method") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinderwell_aggregate_ration_method") &&
                    codexCatalog.entries.Exists(entry => entry.id == "outerwake_bounded_echo_protocol") &&
                    codexCatalog.entries.Exists(entry => entry.id == "outerwake_passive_signal_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "field_codex_af") &&
                    codexCatalog.entries.Exists(entry => entry.id == "field_codex_lo") &&
                    codexCatalog.entries.Exists(entry => entry.id == "elite_codex_af") &&
                    codexCatalog.entries.Exists(entry => entry.id == "elite_codex_lo") &&
                    codexCatalog.entries.Exists(entry => entry.id == "greenwake_seed_access_review") &&
                    codexCatalog.entries.Exists(entry => entry.id == "alden_watch_arrival") &&
                    codexCatalog.entries.Exists(entry => entry.id == "alden_named_optin_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "alden_household_copy_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinder_filter_test_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "saltroad_milepost_afterword_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinder_shared_rill_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinder_steward_schedule_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "cinder_bypass_afterword_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "choir_warning_install_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "choir_warning_bell_method") &&
                    codexCatalog.entries.Exists(entry => entry.id == "choir_warning_lamp_method") &&
                    codexCatalog.entries.Exists(entry => entry.id == "choir_warning_return_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "dawnkeep_garden_runoff_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "dawnkeep_garden_shared_bed_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "dawnkeep_garden_rotation_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "dawnkeep_garden_afterword") &&
                    codexCatalog.entries.Exists(entry => entry.id == "hero_legacy_001_record") &&
                    codexCatalog.entries.Exists(entry => entry.id == "hero_legacy_099_record"),
                "The offline field archive must load the current 734 or more authored records, including both Tamsin Wren signal procedures, the Ashfall cart-repair outcome, both Alden watch-roster outcomes, Elara Wren's garden evidence and policy records, both Cistern policies, Ruth Calder's dispatch evidence, Nella Pike's family-controlled archive routes and monster field-study expansions.");
            var codexLockedSave = new GameSaveData { completedQuestIds = new List<string>() };
            Require(CodexCatalogService.GetUnlocked(codexCatalog, codexLockedSave).Count == 0,
                "Field records must remain locked until their evidence quest is complete.");
            var firstCodexEntry = codexCatalog.entries[0];
            codexLockedSave.completedQuestIds.Add(firstCodexEntry.unlockQuestId);
            var unlockedCodexEntries = CodexCatalogService.GetUnlocked(codexCatalog, codexLockedSave);
            Require(unlockedCodexEntries.Count == 1 && unlockedCodexEntries[0].id == firstCodexEntry.id,
                "Completing an evidence quest must reveal only its matching field record.");
            Require(CountQuestArc(questCatalog, "the_order_of_the_dawn", "story") == 17 &&
                    CountQuestArc(questCatalog, "the_order_of_the_dawn", "side") == 90 &&
                    QuestCatalogService.FindById(questCatalog, "order_cadet_oath")?.reward?.items?.Count == 1,
                "Dawnkeep must preserve both cadet-testimony routes, its waterline notes, creature contracts and unique equipment rewards.");
            var elaraOpening = QuestCatalogService.FindById(questCatalog, "side_elara_garden_open");
            var elaraPolicy = QuestCatalogService.FindById(questCatalog, "side_elara_garden_policy");
            var runoffClip = ItemCatalog.Find("dawnkeep_runoff_clip");
            var runoffClipRecipe = RecipeCatalogService.FindById(RecipeCatalogService.Load(),
                "forge_dawnkeep_runoff_clip");
            Require(elaraOpening?.prerequisiteIds.Contains("order_cadet_oath") == true &&
                    elaraOpening.reward.items.Exists(item => item.itemId == "dawnmeadow_mint_seed" && item.quantity == 1) &&
                    elaraOpening.reward.items.Exists(item => item.itemId == "earthworm_bait" && item.quantity == 6) &&
                    elaraPolicy?.choices.Count == 2 && runoffClip?.category == "quest" &&
                    runoffClipRecipe?.stationId == "dawnkeep_forge" &&
                    runoffClipRecipe.outputItemId == "dawnkeep_runoff_clip" &&
                    runoffClipRecipe.ingredients.Exists(item => item.itemId == "dawnmeadow_mint") &&
                    runoffClipRecipe.ingredients.Exists(item => item.itemId == "blackreed_trout") &&
                    ItemCatalog.Find("dawnkeep_common_soil_charm")?.equipmentSlot == "charm" &&
                    ItemCatalog.Find("dawnkeep_rotating_bed_knot")?.equipmentSlot == "charm",
                "Elara's garden line must provide its seed and bait, require the local clip recipe, and award two equippable policy charms.");
            var cinderClasp = ItemCatalog.Find("cistern_ledger_clasp");
            Require(cinderClasp?.category == "equipment" && cinderClasp.equipmentSlot == "charm" &&
                    cinderClasp.guardBonus == 1 && ItemCatalog.Find("cinder_measure_ring")?.category == "material",
                "The Cinderwell record quest must grant a real crafting material for a usable charm.");
            var chalkTallyCharm = ItemCatalog.Find("fieldgear_ashfall_chalk_charm");
            var doorWedgeCharm = ItemCatalog.Find("fieldgear_ashfall_door_wedge");
            Require(chalkTallyCharm?.category == "equipment" && chalkTallyCharm.equipmentSlot == "charm" &&
                    chalkTallyCharm.guardBonus == 1 && doorWedgeCharm?.category == "equipment" &&
                    doorWedgeCharm.equipmentSlot == "charm" && doorWedgeCharm.guardBonus == 1 &&
                    CountItemCategory("equipment") >= 255,
                "Ashfall's tally and evacuation-map choices must award distinct equippable charms in the expanded equipment catalog.");
            var publicWaymarksCharm = ItemCatalog.Find("fieldgear_waymarks_compass_charm");
            var stewardWaymarksCharm = ItemCatalog.Find("fieldgear_waymarks_steward_charm");
            Require(publicWaymarksCharm?.category == "equipment" && publicWaymarksCharm.equipmentSlot == "charm" &&
                    publicWaymarksCharm.attackBonus == 1 && stewardWaymarksCharm?.category == "equipment" &&
                    stewardWaymarksCharm.equipmentSlot == "charm" && stewardWaymarksCharm.guardBonus == 1 &&
                    CountItemCategory("equipment") >= 255,
                "The Waymarks outcomes must award two distinct equippable charms while preserving the reviewed equipment catalog.");
            var cadetBuckler = ItemCatalog.Find("cadet_buckler");
            var cadetRewardRun = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(cadetRewardRun, "cadet_buckler", 1);
            Require(cadetBuckler?.category == "equipment" && cadetBuckler.equipmentSlot == "armor" &&
                    InventoryService.TryEquip(cadetRewardRun, "cadet_buckler") &&
                    InventoryService.GuardBonus(cadetRewardRun) == 3,
                "Nia's Dawnkeep reward must be a usable armor item with the authored guard value.");
            var blankPin = ItemCatalog.Find("dawnkeep_blank_pin");
            var blankPinRun = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(blankPinRun, "dawnkeep_blank_pin", 1);
            Require(blankPin?.category == "equipment" && blankPin.equipmentSlot == "charm" &&
                    InventoryService.TryEquip(blankPinRun, "dawnkeep_blank_pin") &&
                    InventoryService.AttackBonus(blankPinRun) == 1 && InventoryService.GuardBonus(blankPinRun) == 1,
                "The barracks quest must award an equippable charm with the authored stats.");
            var wellboundCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(wellboundCraft, "cistern_warden_core", 1);
            InventoryService.Add(wellboundCraft, "dryglass_shard", 2);
            Require(ItemCatalog.Find("wellbound_charm")?.equipmentSlot == "charm" &&
                    CraftingService.TryCraft(wellboundCraft, RecipeCatalogService.Load(), "forge_wellbound_charm",
                        "dawnkeep_forge", out var wellboundRecipe, out _) &&
                    wellboundRecipe.outputItemId == "wellbound_charm" &&
                    InventoryService.TryEquip(wellboundCraft, "wellbound_charm") &&
                    InventoryService.AttackBonus(wellboundCraft) == 1 &&
                    InventoryService.GuardBonus(wellboundCraft) == 2,
                "The Cistern Warden core must forge into an equippable Wellbound Charm with its authored stats.");
            var undertowCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(undertowCraft, "lockhouse_bailiff_core", 1);
            InventoryService.Add(undertowCraft, "redpass_badge", 1);
            InventoryService.Add(undertowCraft, "quarry_glass", 2);
            Require(ItemCatalog.Find("undertow_clasp")?.equipmentSlot == "charm" &&
                    CraftingService.TryCraft(undertowCraft, RecipeCatalogService.Load(), "forge_undertow_clasp",
                        "dawnkeep_forge", out var undertowRecipe, out _) &&
                    undertowRecipe.outputItemId == "undertow_clasp" &&
                    InventoryService.TryEquip(undertowCraft, "undertow_clasp") &&
                    InventoryService.AttackBonus(undertowCraft) == 2 && InventoryService.GuardBonus(undertowCraft) == 1,
                "The Lockhouse Bailiff core must forge into an equippable Undertow Clasp with its authored stats.");
            var optionalBossEquipment = new[]
            {
                "sootglass_mantle", "ironward_oath_pin", "sluicewheel_pike",
                "redpass_splitcoat", "deepbell_resonator", "seedvault_cleaver"
            };
            foreach (var itemId in optionalBossEquipment)
                Require(ItemCatalog.Find(itemId)?.category == "equipment",
                    "Each optional boss contract must award a unique equippable item: " + itemId);
            var archiveArrival = QuestCatalogService.FindById(questCatalog, "archive_arrival");
            Require(CountQuestArc(questCatalog, "archive_beyond_veil", "story") == 23 &&
                    CountQuestArc(questCatalog, "archive_beyond_veil", "side") == 87 &&
                    archiveArrival?.reward?.items?.Count == 1 && archiveArrival.reward.items[0].quantity == 5,
                "Arc 7 must provide its complete route graph, eighty-seven regional side quests, and enough starter seeds for its farming loop.");
            Require(CountQuestArc(questCatalog, "two_last_oaths", "story") == 9 &&
                    CountQuestArc(questCatalog, "two_last_oaths", "side") == 181,
                "Arc 8 must include the two mutually exclusive finale routes including the 99-record Hundredth Roll memorial and 181 regional side quests.");
            Require(Resources.Load<Texture2D>("Art/ashfall_village") != null &&
                    Resources.Load<Texture2D>("Art/dawnkeep_outpost") != null &&
                    Resources.Load<Texture2D>("Art/dawnkeep_barracks") != null &&
                    Resources.Load<Texture2D>("Art/cinderwell_basin") != null &&
                    Resources.Load<Texture2D>("Art/cinder_cistern") != null &&
                    Resources.Load<Texture2D>("Art/salt_road") != null &&
                    Resources.Load<Texture2D>("Art/salt_lockhouse") != null &&
                    Resources.Load<Texture2D>("Art/choir_beneath_lake") != null &&
                    Resources.Load<Texture2D>("Art/greenwake_refuge") != null &&
                    Resources.Load<Texture2D>("Art/veil_archive") != null &&
                    Resources.Load<Texture2D>("Art/last_oath_reach") != null,
                "All eight main-region backgrounds, the Dawnkeep barracks, and both Cinderwell/Salt Road underpass maps must be importable Resources assets.");
            Require(Resources.Load<AudioClip>("Audio/exploration_theme") != null &&
                    Resources.Load<AudioClip>("Audio/battle_theme") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/player_attack") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/player_impact") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/loot_coins") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/Fishing/water") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/Fishing/bubbles") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/Fishing/swim") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/Fishing/waterReentry") != null &&
                    Resources.Load<AudioClip>("Audio/Ambience/vistula_river") != null &&
                    Resources.Load<AudioClip>("Audio/Ambience/park_ambience_birds") != null &&
                    Resources.Load<AudioClip>("Audio/Ambience/park_ambience_river") != null &&
                    Resources.Load<AudioClip>("Audio/Ambience/park_ambience_wind") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/RpgPack/Battle/swing_01") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/RpgPack/Battle/sword_draw_01") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/RpgPack/Interface/interface_01") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/RpgPack/Items/potion_bottle") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/RpgPack/Creatures/beast_01") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/footstep_1") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/footstep_2") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/footstep_3") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/footstep_4") != null &&
                    Resources.Load<AudioClip>("Audio/SFX/footstep_5") != null,
                "The offline music and gameplay sound effects must be importable Resources audio clips.");
            var dialogueCatalog = DialogueCatalogService.Load();
            Require(dialogueCatalog != null && dialogueCatalog.entries.Count >= 1218 &&
                    DialogueCatalogService.Find(dialogueCatalog, "tamsin_signal_open") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "mira_ash_house_choice_clinic") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "oren_seed_tin_choice_exchange") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_signal_test") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "tamsin_signal_afterword") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "jace_diaphragm_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "lyra_tuning_fork_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "mara_rootglass_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "alden_watch_spindle_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cistern_filter_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_saltroad_beacon_complete") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "nella_saltroad_milepost_afterword") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_hero_legacy_001") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_hero_legacy_099") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cistern_filter_test")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cistern_shared_rill")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cistern_steward_shift")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cistern_bypass_afterword")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "alden_watch_named_copy") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "alden_watch_household_copy") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "mira_ashfall_muster_invitation")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "ashfall_cart_choice_shared") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "ashfall_cart_choice_household") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_muster_board")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "gideon_ashfall_blank_rows")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_shelter_cloth")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "ashfall_muster_shared_result")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "ashfall_muster_private_result")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_herb_ledger")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_tally_marks")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "gideon_ashfall_tally_interview")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_brace_marks")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_tally_public_choice")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_tally_sealed_choice")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "mira_ashfall_tally_public_copy")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "gideon_ashfall_tally_private_copy")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_second_harvest")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_blackreed_trout")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "mira_ashfall_tonic_brewed")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_ashfall_remedy_shelf")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_choir_margin_marks")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_choir_whisper_koi")?.speakerName == "ROWAN HALE" &&
                    DialogueCatalogService.Find(dialogueCatalog, "lyra_choir_index_complete")?.lines.Count == 4 &&
                    DialogueCatalogService.Find(dialogueCatalog, "warden_choir_arrival")?.speakerName == "THE FIRST WARDEN" &&
                    DialogueCatalogService.Find(dialogueCatalog, "world_will_first_contact")?.speakerName == "THE WORLD WILL" &&
                    DialogueCatalogService.Find(dialogueCatalog, "captain_shelter_report")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_roster_origin_inspection")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_choice_trail")?.speakerName == "ROWAN HALE" &&
                    DialogueCatalogService.Find(dialogueCatalog, "sister_june_cinder_arrival")?.speakerName == "SISTER JUNE" &&
                    DialogueCatalogService.Find(dialogueCatalog, "ruth_salt_arrival")?.speakerName == "RUTH CALDER" &&
                    DialogueCatalogService.Find(dialogueCatalog, "mara_greenwake_arrival")?.speakerName == "MARA BELL" &&
                    DialogueCatalogService.Find(dialogueCatalog, "world_will_hundredth_reply")?.speakerName == "THE WORLD WILL" &&
                    DialogueCatalogService.Find(dialogueCatalog, "evelyn_outerwake_arrival")?.speakerName == "DR. EVELYN HART" &&
                    DialogueCatalogService.Find(dialogueCatalog, "jace_outerwake_briefing")?.speakerName == "JACE MORROW" &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_last_oath_choice_cycle")?.speakerName == "ROWAN HALE" &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_beyond_epilogue")?.lines.Count == 4,
                "The dialogue catalog must load eight story arcs, both authored endings, and their English-named cast.");
            Require(DialogueCatalogService.Find(dialogueCatalog, "nia_order_testimony")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "alden_order_reckoning_seal")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "nia_order_oath_publish")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_barracks_morning_roll")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_barracks_return_shelf")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "nia_barracks_roll_review")?.lines.Count == 3,
                "Dawnkeep's testimony and confession scenes must have authored dialogue for both evidence choices.");
            Require(DialogueCatalogService.Find(dialogueCatalog, "talia_mercer_cistern_testimony")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "sister_june_cistern_report_refugees") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "sister_june_cistern_report_reserve") != null &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_cinder_transfer_docket")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "june_cinderwell_measure_start")?.speakerName == "SISTER JUNE" &&
                    DialogueCatalogService.Find(dialogueCatalog, "talia_cinder_measure_intervals")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "oren_cinder_seed_weight")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_cinder_aggregate_schedule")?.lines.Count == 2,
                "Cinderwell's investigation must preserve both water-choice reactions and the measurement/privacy dialogue.");
            Require(DialogueCatalogService.Find(dialogueCatalog, "rowan_salt_lockhouse_bailiff")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "ruth_salt_handoff")?.lines.Count == 2 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_salt_chain_tags") != null,
                "The Lockhouse boss, chain-tag side quest and Ruth's signed handoff must have authored scenes.");
            foreach (var quest in questCatalog.entries)
            {
                foreach (var objective in quest.objectives)
                    if (!string.IsNullOrEmpty(objective.dialogueId))
                        Require(DialogueCatalogService.Find(dialogueCatalog, objective.dialogueId) != null,
                            "Every authored objective scene must resolve to dialogue: " + quest.id + "/" + objective.id);
                if (quest.choices == null) continue;
                foreach (var choice in quest.choices)
                    if (!string.IsNullOrEmpty(choice.dialogueId))
                        Require(DialogueCatalogService.Find(dialogueCatalog, choice.dialogueId) != null,
                            "Every authored choice result must resolve to dialogue: " + quest.id + "/" + choice.id);
            }
            var questLandmarkCatalog = QuestLandmarkCatalogService.Load(questCatalog, dialogueCatalog);
            Require(questLandmarkCatalog != null &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "ashfall_cellar_tally") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "ashfall_gideon_witness") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "ashfall_shelter_record_desk") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "ashfall_shelter_private_case") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "dawnkeep_copy_consent") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "dawnkeep_sealed_family_packet"),
                "The authored Ashfall and Dawnkeep landmarks must resolve to active objective targets and their evidence scenes.");
            var waymarksDialogues = new[]
            {
                "rowan_waymarks_ashfall_edge", "mira_waymarks_ashfall_shelter", "rowan_waymarks_dawnkeep_landing",
                "nia_waymarks_barracks_blank_pass", "rowan_waymarks_barracks_lantern_drop",
                "june_waymarks_cinderwell_cup", "rowan_waymarks_hound_defeated", "rowan_waymarks_hound_down",
                "ruth_waymarks_saltroad_rest", "lyra_waymarks_choir_clickstone", "mara_waymarks_greenwake_seedbed",
                "owen_waymarks_greenwake_canopy", "evelyn_waymarks_outerwake_beacon",
                "rowan_waymarks_public_choice", "rowan_waymarks_courier_choice",
                "mira_waymarks_public_map", "nia_waymarks_courier_map"
            };
            foreach (var dialogueId in waymarksDialogues)
                Require(DialogueCatalogService.Find(dialogueCatalog, dialogueId) != null,
                    "Every Waymarks stage and outcome needs authored dialogue: " + dialogueId);
            Require(DialogueCatalogService.Find(dialogueCatalog, "rowan_waymarks_hound_defeated")?.lines.Count == 3 &&
                    DialogueCatalogService.Find(dialogueCatalog, "rowan_waymarks_hound_down")?.lines.Count == 3,
                "The gated Salt Road encounter must preserve authored victory and retreat scenes.");
            questLandmarkCatalog = QuestLandmarkCatalogService.Load(questCatalog, dialogueCatalog);
            Require(questLandmarkCatalog != null && questLandmarkCatalog.entries.Count >= 22 &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "waymarks_ashfall_scrape") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "waymarks_distribution_desk") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "waymarks_public_map_frame") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "waymarks_courier_lockbox") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "greenwake_owen_signal_rubbing") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "greenwake_west_root_frost") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "greenwake_route_overlay_copy") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "greenwake_chart_consultation") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "greenwake_map_release_receipt") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "outerwake_greenwake_wind_trace") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "outerwake_greenwake_star_overlay") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_wheel_bearing") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_pressure_marks") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_backwash_wall") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_pressure_lens") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_filter_housing") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_pressure_dial") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_ratchet_bracket") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_shared_rill_tap") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_steward_schedule") &&
                    questLandmarkCatalog.entries.Exists(entry => entry.targetId == "cinder_bypass_plan"),
                "The Waymarks and Cistern routes must load their evidence markers, including both exclusive policy destinations.");
            var monsterCatalog = MonsterCatalogService.Load();
            Require(monsterCatalog != null && monsterCatalog.entries.Count == 211 &&
                    monsterCatalog.entries.FindAll(monster => monster.rank == "common").Count == 141 &&
                    monsterCatalog.entries.FindAll(monster => monster.rank == "elite").Count == 54 &&
                    monsterCatalog.entries.FindAll(monster => monster.rank == "boss").Count == 16 &&
                    MonsterCatalogService.FindById(monsterCatalog, "aegis_cantor")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "ash_warg")?.lungeSpriteResource == "ash_warg_lunge" &&
                    MonsterCatalogService.FindById(monsterCatalog, "mold_crowned_reeve")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "mold_crowned_reeve")?.specialMoveId == "shockwave" &&
                    MonsterCatalogService.FindById(monsterCatalog, "cistern_warden")?.specialMoveId == "siphon" &&
                    MonsterCatalogService.FindById(monsterCatalog, "cistern_warden")?.specialMoveReach > 4 &&
                    MonsterCatalogService.FindById(monsterCatalog, "salt_lockhouse_bailiff")?.specialMoveId == "hook" &&
                    MonsterCatalogService.FindById(monsterCatalog, "cinder_pressure_wight")?.rank == "elite" &&
                    MonsterCatalogService.FindById(monsterCatalog, "cinder_pressure_wight")?.specialMoveId == "marked_strike" &&
                    MonsterCatalogService.FindById(monsterCatalog, "roadglass_sentinel")?.rank == "elite" &&
                    MonsterCatalogService.FindById(monsterCatalog, "roadglass_sentinel")?.specialMoveId == "marked_strike" &&
                    MonsterCatalogService.FindById(monsterCatalog, "salt_slag_inspector")?.rank == "elite" &&
                    MonsterCatalogService.FindById(monsterCatalog, "hollow_tollkeeper")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "hollow_tollkeeper")?.specialMoveReach > 4.5f &&
                    MonsterCatalogService.FindById(monsterCatalog, "crownward_colossus")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "crownward_colossus")?.specialMoveReach > 5 &&
                    MonsterCatalogService.FindById(monsterCatalog, "asterion_threshold")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "veilshard_drake")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "demon_king_alden")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "world_will_avatar")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "cycle_remnant")?.rank == "elite" &&
                    MonsterCatalogService.FindById(monsterCatalog, "embermaw_matriarch")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "ironward_sentinel")?.specialMoveId == "line_charge" &&
                    MonsterCatalogService.FindById(monsterCatalog, "sluicewheel_colossus")?.specialMoveId == "siphon" &&
                    MonsterCatalogService.FindById(monsterCatalog, "redpass_harrower")?.specialMoveId == "hook" &&
                    MonsterCatalogService.FindById(monsterCatalog, "deepbell_herald")?.rank == "boss" &&
                    MonsterCatalogService.FindById(monsterCatalog, "seedvault_keeper")?.specialMoveId == "line_charge",
                "The versioned monster catalog must distinguish rank, preserve both finale bosses and define six optional bosses with a telegraphed lane charge.");
            Require(MonsterCatalogService.FindById(monsterCatalog, "tiny_elite_af_ashvault_flameskull")?.specialMoveId == "ranged_bolt" &&
                    MonsterCatalogService.FindById(monsterCatalog, "tiny_elite_db_glassgaze_medusa")?.specialMoveId == "marked_strike",
                "The new elite roster must include both stationary ranged lanes and aimed ground strikes.");
            var encounterCatalog = EncounterCatalogService.Load();
            Require(encounterCatalog != null && encounterCatalog.entries.Count == 223 &&
                    EncounterCatalogService.FindById(encounterCatalog, "mira_house_yard_warg")?.requiredQuestId == "side_mira_ash_house_yard_warg" &&
                    EncounterCatalogService.FindById(encounterCatalog, "mira_house_well_imp")?.requiredQuestId == "side_mira_ash_house_well_imp" &&
                    EncounterCatalogService.FindById(encounterCatalog, "ashfall_cart_road_goblin")?.requiredQuestId == "side_ashfall_cart_clear" &&
                    EncounterCatalogService.FindById(encounterCatalog, "june_pantry_cinderwell_muck")?.requiredQuestId == "side_june_pantry_pantry" &&
                    EncounterCatalogService.FindById(encounterCatalog, "june_pantry_cinderwell_muck")?.defeatObjectiveTargetId == "tiny_cw_cinderwell_muck" &&
                    EncounterCatalogService.FindById(encounterCatalog, "saltroad_ruth_cart_guard")?.requiredQuestId == "side_ruth_recall_guard" &&
                    EncounterCatalogService.FindById(encounterCatalog, "choir_aegis_cantor")?.locationId == "choir_beneath_lake" &&
                    EncounterCatalogService.FindById(encounterCatalog, "choir_aegis_cantor")?.defeatObjectiveTargetId == "aegis_cantor" &&
                    EncounterCatalogService.FindById(encounterCatalog, "ash_warg_yard")?.monsterId == "ash_warg" &&
                    EncounterCatalogService.FindById(encounterCatalog, "dawnkeep_sparring")?.requiredQuestId == "order_trial_sparring" &&
                    EncounterCatalogService.FindById(encounterCatalog, "cinder_mold_crowned_reeve")?.contributesToQuest == true &&
                    EncounterCatalogService.FindById(encounterCatalog, "cinder_cistern_warden")?.locationId == "cinder_cistern" &&
                    EncounterCatalogService.FindById(encounterCatalog, "cinder_cistern_warden")?.defeatObjectiveTargetId == "cistern_warden" &&
                    EncounterCatalogService.FindById(encounterCatalog, "cinder_pressure_wight_site")?.requiredQuestId == "side_cistern_wheel_wight" &&
                    EncounterCatalogService.FindById(encounterCatalog, "cinder_pressure_wight_site")?.defeatObjectiveTargetId == "cinder_pressure_wight" &&
                    EncounterCatalogService.FindById(encounterCatalog, "salt_lockhouse_bailiff")?.locationId == "salt_lockhouse" &&
                    EncounterCatalogService.FindById(encounterCatalog, "salt_lockhouse_bailiff")?.requiredQuestId == "salt_lockhouse_bailiff" &&
                    EncounterCatalogService.FindById(encounterCatalog, "salt_road_hollow_tollkeeper")?.locationId == "salt_road" &&
                    EncounterCatalogService.FindById(encounterCatalog, "greenwake_crownward")?.locationId == "greenwake_refuge" &&
                    EncounterCatalogService.FindById(encounterCatalog, "greenwake_seedbound")?.requiredQuestId == "champion_accept_oath" &&
                    EncounterCatalogService.FindById(encounterCatalog, "outerwake_asterion")?.locationId == "outerwake_archive" &&
                    EncounterCatalogService.FindById(encounterCatalog, "outerwake_veilshard_drake")?.requiredQuestId == "archive_drake" &&
                    EncounterCatalogService.FindById(encounterCatalog, "last_oath_demon_king")?.requiredQuestId == "last_oath_cycle_boss" &&
                    EncounterCatalogService.FindById(encounterCatalog, "last_oath_world_will")?.requiredQuestId == "last_oath_world_boss" &&
                    EncounterCatalogService.FindById(encounterCatalog, "ashfall_embermaw_matriarch")?.requiredQuestId == "side_ashfall_embermaw" &&
                    EncounterCatalogService.FindById(encounterCatalog, "ashfall_signal_goblin_site")?.requiredQuestId == "side_ashfall_two_bells_clear" &&
                    EncounterCatalogService.FindById(encounterCatalog, "ashfall_signal_goblin_site")?.defeatObjectiveTargetId == "ashfall_signal_goblin" &&
                    EncounterCatalogService.FindById(encounterCatalog, "dawnkeep_ironward_sentinel")?.monsterId == "ironward_sentinel" &&
                    EncounterCatalogService.FindById(encounterCatalog, "cistern_sluicewheel_colossus")?.locationId == "cinder_cistern" &&
                    EncounterCatalogService.FindById(encounterCatalog, "saltroad_redpass_harrower")?.requiredQuestId == "side_salt_redpass_harrower" &&
                    EncounterCatalogService.FindById(encounterCatalog, "waymarks_saltroad_hound")?.requiredQuestId == "side_waymarks_saltroad" &&
                    EncounterCatalogService.FindById(encounterCatalog, "waymarks_saltroad_hound")?.defeatObjectiveTargetId == "waymarks_roadside_hound" &&
                    EncounterCatalogService.FindById(encounterCatalog, "saltroad_roadglass_sentinel_site")?.requiredQuestId == "side_saltroad_roadglass_sentinel" &&
                    EncounterCatalogService.FindById(encounterCatalog, "saltroad_roadglass_sentinel_site")?.defeatObjectiveTargetId == "roadglass_sentinel" &&
                    EncounterCatalogService.FindById(encounterCatalog, "choir_deepbell_herald")?.monsterId == "deepbell_herald" &&
                    EncounterCatalogService.FindById(encounterCatalog, "greenwake_seedvault_keeper")?.requiredQuestId == "side_greenwake_seedvault_keeper",
                "The encounter catalog must place persistent fights in all eight regions and gate each optional boss behind its authored contract.");
            foreach (var encounter in encounterCatalog.entries)
            {
                Require(MonsterCatalogService.FindById(monsterCatalog, encounter.monsterId) != null &&
                        QuestCatalogService.FindById(questCatalog, encounter.requiredQuestId) != null &&
                        DialogueCatalogService.Find(dialogueCatalog, encounter.defeatDialogueId) != null &&
                        DialogueCatalogService.Find(dialogueCatalog, encounter.downDialogueId) != null &&
                        (string.IsNullOrEmpty(encounter.blockedDialogueId) ||
                         DialogueCatalogService.Find(dialogueCatalog, encounter.blockedDialogueId) != null) &&
                        (!encounter.contributesToQuest ||
                         QuestCatalogService.HasObjectiveTarget(questCatalog, "defeat", encounter.defeatObjectiveTargetId)) &&
                        (encounter.contributesToQuest || string.IsNullOrEmpty(encounter.defeatObjectiveTargetId)),
                    "Every encounter must resolve to a monster, quest target, and authored victory/down dialogue.");
                if (encounter.reward?.items != null)
                    foreach (var item in encounter.reward.items)
                        Require(ItemCatalog.Find(item.itemId) != null,
                            "Every encounter reward must resolve to a catalog item.");
            }
            var fishingCatalog = FishingCatalogService.Load();
            Require(fishingCatalog != null && fishingCatalog.entries.Count == 6 &&
                    fishingCatalog.entries[0].id == "dawnkeep_lakeshore" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[1], 0.2f) == "whisper_koi" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[1], 0.75f) == "blackreed_trout" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[1], 0.99f) == "moonlight_carp" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[0], 0.2f) == "blackreed_trout" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[0], 0.75f) == "emberscale_perch" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[0], 0.95f) == "moonlight_carp" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[2], 0.2f) == "farwake_carp" &&
                    fishingCatalog.entries[3].id == "last_oath_starlake" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[3], 0.2f) == "starlit_minnow" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[3], 0.99f) == "farwake_carp" &&
                    fishingCatalog.entries[4].id == "saltroad_sheltered_pool" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[4], 0.2f) == "saltspool_skate" &&
                    fishingCatalog.entries[4].baitItemId == "earthworm_bait" &&
                    fishingCatalog.entries[5].id == "cinderwell_warm_run" &&
                    FishingCatalogService.RollCatch(fishingCatalog.entries[5], 0.2f) == "emberscale_perch" &&
                    fishingCatalog.entries[5].baitItemId == "earthworm_bait",
                "The weighted fishing tables must produce expected regional fish at their authored ranges.");
            foreach (var spot in fishingCatalog.entries)
            {
                Require(ItemCatalog.Find(spot.baitItemId) != null,
                    "Every fishing spot must use an item that exists in the item catalog.");
                foreach (var fish in spot.catches)
                    Require(ItemCatalog.Find(fish.itemId) != null,
                        "Every fishing result must resolve to an inventory item.");
            }

            var recipeCatalog = RecipeCatalogService.Load();
            Require(recipeCatalog != null && recipeCatalog.entries.Count == 45 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "ashfall_herb_table").Count == 6 &&
                    RecipeCatalogService.FindById(recipeCatalog, "brew_emberlily_balm")?.outputItemId == "mira_emberlily_balm" &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "dawnkeep_forge").Count == 14 &&
                    RecipeCatalogService.FindById(recipeCatalog, "forge_ashfall_cart_axle_pin")?.outputItemId == "ashfall_cart_axle_pin" &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "choir_archive_loom").Count == 3 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "choir_harmonic_anvil").Count == 5 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "archive_alchemy_bench").Count == 3 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "greenwake_alchemy_still").Count == 2 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "outerwake_forge").Count == 3 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "last_oath_forge").Count == 2 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "last_oath_kitchen").Count == 1 &&
                    RecipeCatalogService.FindById(recipeCatalog, "cook_crownfall_starlit_pottage")?.outputItemId ==
                    "crownfall_starlit_pottage" &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "cinderwell_assay_bench").Count == 4 &&
                    RecipeCatalogService.FindForStation(recipeCatalog, "cinderwell_kitchen").Count == 2 &&
                    RecipeCatalogService.FindById(recipeCatalog, "cook_cinderwell_stonepot_broth")?.outputItemId == "cinderwell_stonepot_broth" &&
                    RecipeCatalogService.FindById(recipeCatalog, "cook_oren_seedkeepers_cake")?.outputItemId == "oren_seedkeepers_cake" &&
                    RecipeCatalogService.FindById(recipeCatalog, "craft_saltroad_beacon_lens")?.outputItemId == "saltroad_beacon_lens" &&
                    RecipeCatalogService.FindById(recipeCatalog, "forge_choir_pulse_brace")?.outputItemId == "choir_pulse_brace" &&
                    RecipeCatalogService.FindById(recipeCatalog, "brew_cinder_moss_filter")?.outputItemId == "cinder_moss_filter",
                "The recipe catalog must include the Arc 5 stations, Outer-Wake workbenches, finale forge and Cinderwell assay bench.");
            foreach (var recipe in recipeCatalog.entries)
            {
                Require(ItemCatalog.Find(recipe.outputItemId) != null &&
                        ((recipe.discipline == "alchemy" &&
                          (recipe.stationId == "ashfall_herb_table" || recipe.stationId == "choir_archive_loom" ||
                           recipe.stationId == "archive_alchemy_bench" ||
                           recipe.stationId == "cinderwell_assay_bench" ||
                           recipe.stationId == "greenwake_alchemy_still")) ||
                         (recipe.discipline == "smithing" &&
                          (recipe.stationId == "dawnkeep_forge" || recipe.stationId == "choir_harmonic_anvil" ||
                           recipe.stationId == "outerwake_forge" || recipe.stationId == "last_oath_forge")) ||
                         (recipe.discipline == "cooking" &&
                          (recipe.stationId == "cinderwell_kitchen" || recipe.stationId == "last_oath_kitchen"))),
                    "Every recipe must resolve to its proper station and output item.");
                foreach (var ingredient in recipe.ingredients)
                    Require(ItemCatalog.Find(ingredient.itemId) != null,
                        "Every recipe ingredient must resolve to an item definition.");
            }

            var shortCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(shortCraft, "moonwort_leaf", 2);
            Require(!CraftingService.TryCraft(shortCraft, recipeCatalog, "brew_moonlight_tonic", "ashfall_herb_table",
                        out _, out var missingCraftItem) && missingCraftItem == "blackreed_trout" &&
                    InventoryService.Count(shortCraft, "moonwort_leaf") == 2,
                "Crafting must preserve ingredients and identify a missing fish before starting a transaction.");
            InventoryService.Add(shortCraft, "blackreed_trout", 1);
            Require(!CraftingService.TryCraft(shortCraft, recipeCatalog, "brew_moonlight_tonic", "dawnkeep_forge",
                        out _, out _) && InventoryService.Count(shortCraft, "moonwort_leaf") == 2 &&
                    InventoryService.Count(shortCraft, "blackreed_trout") == 1,
                "A recipe must reject a station mismatch without consuming ingredients.");
            Require(CraftingService.TryCraft(shortCraft, recipeCatalog, "brew_moonlight_tonic", "ashfall_herb_table",
                        out var crafted, out _) && crafted.outputItemId == "moonlight_tonic" &&
                    InventoryService.Count(shortCraft, "moonwort_leaf") == 0 &&
                    InventoryService.Count(shortCraft, "blackreed_trout") == 0 &&
                    InventoryService.Count(shortCraft, "moonlight_tonic") == 1 &&
                    InventoryService.HealAmount("moonlight_tonic") == 38,
                "A successful alchemy transaction must consume its exact inputs and award the catalog output.");

            var cinderCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(cinderCraft, "salt_saffron_bloom", 1);
            InventoryService.Add(cinderCraft, "salt_hound_pelt", 1);
            Require(CraftingService.TryCraft(cinderCraft, recipeCatalog, "brew_cinder_poultice", "ashfall_herb_table",
                        out var cinderCrafted, out _) && cinderCrafted.outputItemId == "cinder_poultice" &&
                    InventoryService.Count(cinderCraft, "salt_saffron_bloom") == 0 &&
                    InventoryService.Count(cinderCraft, "salt_hound_pelt") == 0 &&
                    InventoryService.HealAmount("cinder_poultice") == 34,
                "Cinderwell alchemy must consume Salt Saffron and a Salt Hound pelt to make its stronger poultice.");

            var saltRoadCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(saltRoadCraft, "saltbloom", 2);
            InventoryService.Add(saltRoadCraft, "quarry_glass", 1);
            Require(CraftingService.TryCraft(saltRoadCraft, recipeCatalog, "brew_saltglass_tonic", "ashfall_herb_table",
                        out var saltTonic, out _) && saltTonic.outputItemId == "saltglass_tonic" &&
                    InventoryService.HealAmount("saltglass_tonic") == 42 &&
                    InventoryService.Count(saltRoadCraft, "saltbloom") == 0 &&
                    InventoryService.Count(saltRoadCraft, "quarry_glass") == 0,
                "Salt Road alchemy must consume its local materials and yield a distinct 42-HP tonic.");
            InventoryService.Add(saltRoadCraft, "glassback_carapace", 2);
            InventoryService.Add(saltRoadCraft, "roadside_wolf_hide", 1);
            Require(CraftingService.TryCraft(saltRoadCraft, recipeCatalog, "forge_caravan_scale_vest", "dawnkeep_forge",
                        out var saltArmor, out _) && saltArmor.outputItemId == "caravan_scale_vest" &&
                    InventoryService.TryEquip(saltRoadCraft, "caravan_scale_vest") &&
                    InventoryService.GuardBonus(saltRoadCraft) == 5,
                "The caravan armor recipe must produce equipment that can be equipped for its intended guard bonus.");

            var outerwakeCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(outerwakeCraft, "riftglass", 4);
            InventoryService.Add(outerwakeCraft, "wraith_ash", 1);
            InventoryService.Add(outerwakeCraft, "asterion_core", 1);
            InventoryService.Add(outerwakeCraft, "farwake_silt", 2);
            InventoryService.Add(outerwakeCraft, "veilshard_fragment", 1);
            Require(!CraftingService.TryCraft(outerwakeCraft, recipeCatalog, "craft_astral_prism", "outerwake_forge",
                        out _, out _) && InventoryService.Count(outerwakeCraft, "riftglass") == 4 &&
                    CraftingService.TryCraft(outerwakeCraft, recipeCatalog, "craft_astral_prism", "archive_alchemy_bench",
                        out var prismCraft, out _) && prismCraft.outputItemId == "astral_prism" &&
                    CraftingService.TryCraft(outerwakeCraft, recipeCatalog, "forge_astrolabe_edge", "outerwake_forge",
                        out var edgeCraft, out _) && edgeCraft.outputItemId == "astrolabe_edge" &&
                    CraftingService.TryCraft(outerwakeCraft, recipeCatalog, "forge_veilweave_coat", "outerwake_forge",
                        out var coatCraft, out _) && coatCraft.outputItemId == "veilweave_coat",
                "Outer-Wake alchemy and smithing must enforce station IDs, consume valid ingredients and yield their authored equipment and quest item.");

            var lastOathCraft = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(lastOathCraft, "cycle_remnant_scale", 2);
            InventoryService.Add(lastOathCraft, "emberroot", 1);
            Require(CraftingService.TryCraft(lastOathCraft, recipeCatalog, "forge_last_oath_guard", "last_oath_forge",
                        out var guardCraft, out _) && guardCraft.outputItemId == "last_oath_guard" &&
                    InventoryService.TryEquip(lastOathCraft, "last_oath_guard") &&
                    InventoryService.GuardBonus(lastOathCraft) == 12 &&
                    InventoryService.Count(lastOathCraft, "cycle_remnant_scale") == 0 &&
                    InventoryService.Count(lastOathCraft, "emberroot") == 0,
                "The final forge must consume local materials and yield equippable armor for the two-ending route.");

            var farmCatalog = FarmCatalogService.Load();
            Require(farmCatalog != null && farmCatalog.entries.Count == 11 &&
                    ItemCatalog.Find(farmCatalog.entries[0].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[0].harvestItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[1].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[1].harvestItemId) != null &&
                    farmCatalog.entries[3].id == "outerwake_skyroot_bed" &&
                    farmCatalog.entries[3].locationId == "outerwake_archive" &&
                    ItemCatalog.Find(farmCatalog.entries[3].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[3].harvestItemId) != null &&
                    farmCatalog.entries[4].id == "last_oath_emberroot_bed" &&
                    farmCatalog.entries[4].locationId == "last_oath_reach" &&
                    ItemCatalog.Find(farmCatalog.entries[4].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[4].harvestItemId) != null &&
                    farmCatalog.entries[5].id == "greenwake_glassplum_bed" &&
                    farmCatalog.entries[5].locationId == "greenwake_refuge" &&
                    farmCatalog.entries[5].cropId == "glassplum" &&
                    ItemCatalog.Find(farmCatalog.entries[5].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[5].harvestItemId) != null &&
                    farmCatalog.entries[6].id == "cinder_cistern_brineglass_bed" &&
                    farmCatalog.entries[6].locationId == "cinder_cistern" &&
                    farmCatalog.entries[6].cropId == "brineglass_moss" &&
                    Mathf.Approximately(farmCatalog.entries[6].growSeconds, 150) &&
                    ItemCatalog.Find(farmCatalog.entries[6].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[6].harvestItemId) != null &&
                    farmCatalog.entries[7].id == "saltroad_windglass_reed_bed" &&
                    farmCatalog.entries[7].locationId == "salt_road" &&
                    farmCatalog.entries[7].cropId == "windglass_reed" &&
                    ItemCatalog.Find(farmCatalog.entries[7].seedItemId) != null &&
                    ItemCatalog.Find(farmCatalog.entries[7].harvestItemId) != null &&
                    farmCatalog.entries.Exists(plot => plot.id == "dawnkeep_dawnmeadow_bed" &&
                        plot.locationId == "dawnkeep_outpost" && plot.cropId == "dawnmeadow_mint" &&
                        Mathf.Approximately(plot.growSeconds, 110) &&
                        ItemCatalog.Find(plot.seedItemId) != null && ItemCatalog.Find(plot.harvestItemId) != null) &&
                    farmCatalog.entries.Exists(plot => plot.id == "ashfall_emberlily_bed" &&
                        plot.locationId == "ashfall_village" && plot.cropId == "emberlily" &&
                        ItemCatalog.Find(plot.seedItemId) != null && ItemCatalog.Find(plot.harvestItemId) != null),
                "The farm catalog must load all eleven regional crop plots with existing seed and harvest items, including Emberlily and Elara's timed Dawnmeadow plot.");
            var farmRun = new GameSaveData { inventory = new List<InventoryStackData>() };
            var herbBed = farmCatalog.entries[0];
            InventoryService.Add(farmRun, herbBed.seedItemId, 1);
            Require(FarmPlotProgressService.TryPlant(farmRun, herbBed) &&
                    InventoryService.Count(farmRun, herbBed.seedItemId) == 0 &&
                    Mathf.Approximately(FarmPlotProgressService.Find(farmRun, herbBed.id).remainingSeconds, 90) &&
                    !FarmPlotProgressService.TryPlant(farmRun, herbBed),
                "Planting must consume one seed, persist the configured growth timer and prevent duplicate planting.");
            Require(!FarmPlotProgressService.Tick(farmRun, 89),
                "A crop must remain unready until its full active-play timer has elapsed.");
            farmRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(farmRun));
            Require(FarmPlotProgressService.Find(farmRun, herbBed.id) != null &&
                    Mathf.Approximately(FarmPlotProgressService.Find(farmRun, herbBed.id).remainingSeconds, 1) &&
                    FarmPlotProgressService.Tick(farmRun, 1) && FarmPlotProgressService.TryHarvest(farmRun, herbBed) &&
                    InventoryService.Count(farmRun, herbBed.harvestItemId) == herbBed.harvestQuantity &&
                    FarmPlotProgressService.Find(farmRun, herbBed.id) == null,
                "Crop time must survive JSON save/load, finish deterministically and award the configured harvest once.");
            var saffronBed = farmCatalog.entries[1];
            InventoryService.Add(farmRun, saffronBed.seedItemId, 1);
            Require(FarmPlotProgressService.TryPlant(farmRun, saffronBed) &&
                    Mathf.Approximately(FarmPlotProgressService.Find(farmRun, saffronBed.id).remainingSeconds, 120) &&
                    FarmPlotProgressService.Tick(farmRun, 120) && FarmPlotProgressService.TryHarvest(farmRun, saffronBed) &&
                    InventoryService.Count(farmRun, saffronBed.harvestItemId) == 2,
                "The Cinderwell Salt Saffron plot must use its own seed, timer and harvest quantity.");
            var skyrootBed = farmCatalog.entries[3];
            InventoryService.Add(farmRun, skyrootBed.seedItemId, 1);
            Require(FarmPlotProgressService.TryPlant(farmRun, skyrootBed) &&
                    FarmPlotProgressService.Tick(farmRun, skyrootBed.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(farmRun, skyrootBed) &&
                    InventoryService.Count(farmRun, skyrootBed.harvestItemId) == skyrootBed.harvestQuantity,
                "The Outer-Wake Skyroot plot must grow and award the configured local harvest.");
            var emberrootBed = farmCatalog.entries[4];
            InventoryService.Add(farmRun, emberrootBed.seedItemId, 1);
            Require(FarmPlotProgressService.TryPlant(farmRun, emberrootBed) &&
                    Mathf.Approximately(FarmPlotProgressService.Find(farmRun, emberrootBed.id).remainingSeconds, 135) &&
                    FarmPlotProgressService.Tick(farmRun, emberrootBed.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(farmRun, emberrootBed) &&
                    InventoryService.Count(farmRun, emberrootBed.harvestItemId) == emberrootBed.harvestQuantity,
                "The Crownfall Reach Emberroot plot must grow and award its configured local harvest.");
            var glassplumBed = farmCatalog.entries[5];
            InventoryService.Add(farmRun, glassplumBed.seedItemId, 1);
            Require(FarmPlotProgressService.TryPlant(farmRun, glassplumBed) &&
                    FarmPlotProgressService.Tick(farmRun, glassplumBed.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(farmRun, glassplumBed) &&
                    InventoryService.Count(farmRun, glassplumBed.harvestItemId) == glassplumBed.harvestQuantity,
                "The Greenwake Glassplum graft must grow and award its measured local harvest.");
            ValidateCharacterSideStories(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                questLandmarkCatalog);
            ValidateCisternPressureWheelLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog,
                encounterCatalog, monsterCatalog);
            ValidateSaltRoadMilepostLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                encounterCatalog, monsterCatalog, questLandmarkCatalog);
            ValidateRuthRecalledOrderLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                encounterCatalog, monsterCatalog, questLandmarkCatalog);
            ValidateNellaMissingNameLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                encounterCatalog, monsterCatalog, questLandmarkCatalog);
            Require(QuestCatalogService.FindByStage(questCatalog, 1)?.id == "ashfall_warg" &&
                    QuestCatalogService.FindById(questCatalog, "ashfall_choice")?.choices.Count == 2 &&
                    QuestCatalogService.FindById(questCatalog, "order_arrival")?.prerequisiteGroups[0].anyOfQuestIds.Count == 2 &&
                    QuestCatalogService.FindByStageAndBranch(questCatalog, 3, "first_choice", "shelter")?.id ==
                    "ashfall_shelter_witness" &&
                    QuestCatalogService.FindByStageAndBranch(questCatalog, 3, "first_choice", "trail")?.id ==
                    "ashfall_trail_evidence" &&
                    QuestCatalogService.FindByStageAndBranch(questCatalog, 4, "first_choice", "shelter")?.id ==
                    "ashfall_shelter_report" &&
                    QuestCatalogService.FindByStageAndBranch(questCatalog, 4, "first_choice", "trail")?.id ==
                    "ashfall_trail_report",
                "Quest IDs, exclusive branches and legacy slice stages must resolve to the authored graph.");
            var cyclicCatalog = JsonUtility.FromJson<QuestCatalogData>(JsonUtility.ToJson(questCatalog));
            cyclicCatalog.entries[0].prerequisiteIds.Add("ashfall_choice");
            var rejectedCycle = false;
            try
            {
                QuestCatalogService.Validate(cyclicCatalog);
            }
            catch (System.FormatException)
            {
                rejectedCycle = true;
            }
            Require(rejectedCycle, "Quest validation must reject prerequisite cycles.");

            var trailRun = new GameSaveData { questStage = 0 };
            Require(QuestProgressService.Reconcile(trailRun, questCatalog) &&
                    QuestProgressService.IsActive(trailRun, "ashfall_survivors"),
                "A new save must begin with the authored stable quest ID.");
            Require(QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "mira_cole", 1,
                        out var completed) && completed?.id == "ashfall_survivors" &&
                    trailRun.completedQuestIds.Contains("ashfall_survivors") &&
                    QuestProgressService.IsActive(trailRun, "ashfall_warg"),
                "Objective events must complete the current quest ID and unlock its prerequisite successor.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "defeat", "ash_warg", 1, out completed);
            var choiceQuest = QuestProgressService.GetActiveQuest(trailRun, questCatalog);
            var trailChoice = QuestCatalogService.FindChoice(choiceQuest, "trail");
            QuestProgressService.SetStoryFlag(trailRun, choiceQuest.choiceFlag, trailChoice.flagValue);
            QuestProgressService.RecordObjective(trailRun, questCatalog, "choice", "ashfall_first_action", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "ashfall_trail_evidence"),
                "Stable story flags must select exactly the corresponding branch quest.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "ashfall_burned_seal", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "ashfall_trail_report"),
                "Completing a branch objective must unlock its own follow-up by prerequisite ID.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "captain_alden_vale", 1, out completed);
            Require(!trailRun.chapterComplete && QuestProgressService.IsActive(trailRun, "order_arrival") &&
                    trailRun.completedQuestIds.Count == 5 && !trailRun.completedQuestIds.Contains("ashfall_shelter_witness"),
                "The trail branch must finish Ashfall and unlock its shared Dawnkeep successor.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "elara_wren", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "order_roster"),
                "The Dawnkeep arrival quest must unlock the roster investigation.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "dawnkeep_roster", 1, out completed);
            var trailDisclosureQuest = QuestProgressService.GetActiveQuest(trailRun, questCatalog);
            var privateDisclosure = QuestCatalogService.FindChoice(trailDisclosureQuest, "keep_private");
            QuestProgressService.SetStoryFlag(trailRun, trailDisclosureQuest.choiceFlag, privateDisclosure.flagValue);
            QuestProgressService.RecordObjective(trailRun, questCatalog, "choice", "dawnkeep_disclosure", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "order_archive_private"),
                "The private disclosure choice must select its follow-up branch.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "elara_wren", 1, out completed);
            Require(!trailRun.chapterComplete && QuestProgressService.IsActive(trailRun, "order_trial_sparring") &&
                    !trailRun.completedQuestIds.Contains("order_archive_public"),
                "The private Dawnkeep disclosure route must converge on the shared training encounter.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "defeat", "dawnkeep_warden", 1, out completed);
            Require(completed?.id == "order_trial_sparring" && QuestProgressService.IsActive(trailRun, "order_trial_report"),
                "Defeating the Dawnkeep Warden must award its quest and unlock the Captain's debrief.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "captain_alden_vale", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "order_roster_origin"),
                "The debrief must unlock the missing-name investigation.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "dawnkeep_roster_origin", 1,
                out completed);
            Require(!trailRun.chapterComplete && trailRun.completedQuestIds.Count == 12 &&
                    QuestProgressService.IsActive(trailRun, "order_empty_cots") &&
                    !trailRun.completedQuestIds.Contains("order_archive_public"),
                "The private disclosure branch must resolve the roster revelation and open Dawnkeep's missing-cadet investigation.");
            ValidateDawnkeepFollowup(trailRun, questCatalog, "seal");

            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "sister_june", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "cinder_grain_records"),
                "Meeting Sister June must start the ration ledger investigation.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "cinder_grain_ledger", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "cinder_sluice_map"),
                "The altered harvest ledger must open the sluice survey.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "talia_mercer", 1, out completed);
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "cinder_east_sluice", 1, out completed);
            Require(QuestProgressService.IsActive(trailRun, "cinder_water_rights"),
                "The sluice survey must lead to the water allocation choice.");
            var reserveChoiceQuest = QuestProgressService.GetActiveQuest(trailRun, questCatalog);
            var reserveChoice = QuestCatalogService.FindChoice(reserveChoiceQuest, "seed_reserve");
            QuestProgressService.SetStoryFlag(trailRun, reserveChoiceQuest.choiceFlag, reserveChoice.flagValue);
            QuestProgressService.RecordObjective(trailRun, questCatalog, "choice", "cinder_water_rights_choice", 1,
                out completed);
            Require(QuestProgressService.IsActive(trailRun, "cinder_water_reserve"),
                "The reserve choice must select only its matching branch.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "oren_bell", 1, out completed);
            QuestProgressService.RecordObjective(trailRun, questCatalog, "inspect", "cinder_seed_archive", 1,
                out completed);
            Require(QuestProgressService.IsActive(trailRun, "cinder_blight"),
                "The sealed seed record must unlock the Cinderwell boss encounter.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "defeat", "mold_crowned_reeve", 1,
                out completed);
            Require(completed?.id == "cinder_blight" && QuestProgressService.IsActive(trailRun, "cinder_recovery"),
                "Defeating the Mold-Crowned Reeve must unlock the recovery report.");
            QuestProgressService.RecordObjective(trailRun, questCatalog, "talk", "sister_june", 1, out completed);
            ValidateCinderwellDepth(trailRun, questCatalog, "reserve");
            Require(!trailRun.chapterComplete && trailRun.completedQuestIds.Count == 33 &&
                    QuestProgressService.IsActive(trailRun, "salt_arrival") &&
                    !trailRun.completedQuestIds.Contains("cinder_water_refugees") &&
                    !trailRun.completedQuestIds.Contains("order_archive_public"),
                "The seed reserve route must finish Arc 3 and unlock Salt Road without completing either unchosen route.");

            var shelterRun = new GameSaveData { questStage = 0 };
            QuestProgressService.Reconcile(shelterRun, questCatalog);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "mira_cole", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "defeat", "ash_warg", 1, out completed);
            var shelterChoiceQuest = QuestProgressService.GetActiveQuest(shelterRun, questCatalog);
            var shelterChoice = QuestCatalogService.FindChoice(shelterChoiceQuest, "shelter");
            QuestProgressService.SetStoryFlag(shelterRun, shelterChoiceQuest.choiceFlag, shelterChoice.flagValue);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "choice", "ashfall_first_action", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "gideon_park", 1, out completed);
            Require(QuestProgressService.IsActive(shelterRun, "ashfall_shelter_report"),
                "The shelter branch must unlock its own report quest by prerequisite ID.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "captain_alden_vale", 1, out completed);
            Require(QuestProgressService.IsActive(shelterRun, "order_arrival") &&
                    !shelterRun.completedQuestIds.Contains("ashfall_trail_evidence"),
                "The shelter branch must unlock the shared Dawnkeep successor without completing the trail route.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "elara_wren", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "inspect", "dawnkeep_roster", 1, out completed);
            var publicDisclosureQuest = QuestProgressService.GetActiveQuest(shelterRun, questCatalog);
            var publicDisclosure = QuestCatalogService.FindChoice(publicDisclosureQuest, "share_publicly");
            QuestProgressService.SetStoryFlag(shelterRun, publicDisclosureQuest.choiceFlag, publicDisclosure.flagValue);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "choice", "dawnkeep_disclosure", 1, out completed);
            Require(QuestProgressService.IsActive(shelterRun, "order_archive_public"),
                "The public disclosure choice must select its own follow-up branch.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "elara_wren", 1, out completed);
            Require(!shelterRun.chapterComplete && QuestProgressService.IsActive(shelterRun, "order_trial_sparring") &&
                    !shelterRun.completedQuestIds.Contains("order_archive_private"),
                "The public Dawnkeep disclosure route must converge on the shared training encounter.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "defeat", "dawnkeep_warden", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "captain_alden_vale", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "inspect", "dawnkeep_roster_origin", 1,
                out completed);
            Require(!shelterRun.chapterComplete && shelterRun.completedQuestIds.Count == 12 &&
                    QuestProgressService.IsActive(shelterRun, "order_empty_cots") &&
                    !shelterRun.completedQuestIds.Contains("order_archive_private"),
                "The public disclosure branch must resolve the roster revelation and open Dawnkeep's missing-cadet investigation.");
            ValidateDawnkeepFollowup(shelterRun, questCatalog, "publish");

            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "sister_june", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "inspect", "cinder_grain_ledger", 1,
                out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "talia_mercer", 1, out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "inspect", "cinder_east_sluice", 1,
                out completed);
            var refugeeChoiceQuest = QuestProgressService.GetActiveQuest(shelterRun, questCatalog);
            var refugeeChoice = QuestCatalogService.FindChoice(refugeeChoiceQuest, "refugee_fields");
            QuestProgressService.SetStoryFlag(shelterRun, refugeeChoiceQuest.choiceFlag, refugeeChoice.flagValue);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "choice", "cinder_water_rights_choice", 1,
                out completed);
            Require(QuestProgressService.IsActive(shelterRun, "cinder_water_refugees"),
                "The refugee fields choice must select only its matching branch.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "interact", "basin_refugee_channel", 1,
                out completed);
            Require(QuestProgressService.IsActive(shelterRun, "cinder_water_refugees"),
                "Opening the refugee channel must leave the Salt Saffron harvest objective active.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "grow", "salt_saffron", 1,
                out completed);
            Require(completed?.id == "cinder_water_refugees" && QuestProgressService.IsActive(shelterRun, "cinder_blight"),
                "Harvesting Salt Saffron must complete the refugee branch and unlock the boss.");
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "defeat", "mold_crowned_reeve", 1,
                out completed);
            QuestProgressService.RecordObjective(shelterRun, questCatalog, "talk", "sister_june", 1, out completed);
            ValidateCinderwellDepth(shelterRun, questCatalog, "refugees");
            Require(!shelterRun.chapterComplete && shelterRun.completedQuestIds.Count == 33 &&
                    QuestProgressService.IsActive(shelterRun, "salt_arrival") &&
                    !shelterRun.completedQuestIds.Contains("cinder_water_reserve") &&
                    !shelterRun.completedQuestIds.Contains("order_archive_private"),
                "The refugee field route must finish Arc 3 and unlock Salt Road without completing either unchosen route.");

            var caravanRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(trailRun));
            var refugeeRouteRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(trailRun));
            var hunterRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(trailRun));
            ValidateSaltRoadRoute(caravanRun, questCatalog, "trust_caravan", "caravan", "salt_account_caravan",
                "ruth_calder", "salt_caravan_seal", "salt_account_refugees", "salt_account_hunters");
            ValidateSaltRoadRoute(refugeeRouteRun, questCatalog, "trust_refugees", "refugees", "salt_account_refugees",
                "nella_pike", "salt_refugee_token", "salt_account_caravan", "salt_account_hunters");
            ValidateSaltRoadRoute(hunterRun, questCatalog, "trust_hunters", "hunters", "salt_account_hunters",
                "silas_vane", "salt_hunter_map", "salt_account_caravan", "salt_account_refugees");
            ValidateChoirRoute(caravanRun, questCatalog, "preserve");
            ValidateChoirRoute(refugeeRouteRun, questCatalog, "release");
            ValidateChampionRoute(caravanRun, questCatalog, "accept");
            ValidateChampionRoute(refugeeRouteRun, questCatalog, "refuse");
            var publicEvidenceRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(caravanRun));
            var privateEvidenceRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(refugeeRouteRun));
            ValidateOuterwakeRoute(publicEvidenceRun, questCatalog, "publish", "public");
            ValidateOuterwakeRoute(privateEvidenceRun, questCatalog, "seal", "private");
            var crownOfAshRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(publicEvidenceRun));
            var beyondTheVeilRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(privateEvidenceRun));
            ValidateLastOathRoute(crownOfAshRun, questCatalog, "renew_cycle", "cycle");
            ValidateLastOathRoute(beyondTheVeilRun, questCatalog, "open_road", "beyond");

            var partialCatalog = JsonUtility.FromJson<QuestCatalogData>(JsonUtility.ToJson(questCatalog));
            partialCatalog.entries[0].objectives[0].requiredCount = 2;
            var partialRun = new GameSaveData { questStage = 0 };
            QuestProgressService.Reconcile(partialRun, partialCatalog);
            Require(QuestProgressService.RecordObjective(partialRun, partialCatalog, "talk", "mira_cole", 1,
                        out completed) && completed == null && partialRun.questObjectiveProgress[0].count == 1,
                "Objective counts must persist when a target requires multiple events.");
            partialRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(partialRun));
            QuestProgressService.Reconcile(partialRun, partialCatalog);
            Require(QuestProgressService.RecordObjective(partialRun, partialCatalog, "talk", "mira_cole", 1,
                        out completed) && completed?.id == "ashfall_survivors",
                "Partial objective progress must survive save serialization and complete at its required count.");

            ValidateAllRegionalSideQuests(questCatalog);
            ValidateLastOathConsentArchive(questCatalog, codexCatalog);
            ValidateCrownfallForecastLine(questCatalog, codexCatalog);
            ValidateCrownfallSharedTableLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog);
            ValidateSaltEllisSignalLine(questCatalog, codexCatalog);
            ValidateGreenwakeChartLine(questCatalog, codexCatalog);
            ValidateTinyCreatureFieldbook(questCatalog, codexCatalog, dialogueCatalog, monsterCatalog,
                encounterCatalog);
            ValidateTinyEliteContracts(questCatalog, codexCatalog, dialogueCatalog, monsterCatalog,
                encounterCatalog);
            ValidateVerdantMemoryContracts(questCatalog, codexCatalog, dialogueCatalog, monsterCatalog,
                encounterCatalog);
            ValidateCrawlCreatureContracts(questCatalog, codexCatalog, dialogueCatalog, monsterCatalog,
                encounterCatalog);
            Require(MonsterCombatRules.IsLaneAttack("line_charge") &&
                    MonsterCombatRules.IsLaneAttack("ranged_bolt") &&
                    !MonsterCombatRules.HoldsPositionDuringAttack("line_charge") &&
                    MonsterCombatRules.HoldsPositionDuringAttack("ranged_bolt") &&
                    MonsterCombatRules.IsPointInsideLane(new Vector2(4f, 0.2f), Vector2.zero, Vector2.right, 6f, 1f) &&
                    !MonsterCombatRules.IsPointInsideLane(new Vector2(3f, 1.8f), Vector2.zero, Vector2.right, 6f, 1f) &&
                    MonsterCombatRules.IsPointInsideMarkedStrike(new Vector2(2f, 0f), Vector2.zero, 2.4f) &&
                    !MonsterCombatRules.IsPointInsideMarkedStrike(new Vector2(2.5f, 0f), Vector2.zero, 2.4f),
                "Lane bolts and locked ground strikes must use separate dodge spaces that the player can leave before impact.");
            ValidateChoirUnboundIndexLine(questCatalog, codexCatalog);
            ValidateChoirConsentArchiveLine(questCatalog, codexCatalog);
            ValidateDawnkeepBarracksSideQuestLine(questCatalog, codexCatalog);
            ValidateDawnkeepHouseholdDisclosureLine(questCatalog, codexCatalog);
            ValidateDawnkeepWaterlineSideQuestLine(questCatalog, codexCatalog, recipeCatalog);
            ValidateAshfallRemedyLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog);
            ValidateAshfallTallyRoutes(questCatalog, codexCatalog);
            ValidateAshfallMusterRoutes(questCatalog, codexCatalog);
            ValidateAshfallTwoBellsRoutes(questCatalog, codexCatalog, recipeCatalog, farmCatalog, encounterCatalog,
                questLandmarkCatalog);
            ValidateWaymarksBetweenUs(questCatalog, codexCatalog, encounterCatalog, monsterCatalog,
                fishingCatalog, farmCatalog);
            ValidateCinderwellMeasureLine(questCatalog, codexCatalog, recipeCatalog);
            ValidateCinderwellSaltlineRoutes(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog);
            ValidateJuneStonepotKitchenLine(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                encounterCatalog, monsterCatalog);
            ValidateOrenSeedTinRoute(questCatalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog);
            ValidateAshfallCartRestorationLine(questCatalog, codexCatalog, dialogueCatalog, recipeCatalog,
                encounterCatalog, monsterCatalog, questLandmarkCatalog);
            ValidateOuterwakeSignalReplyLine(questCatalog, codexCatalog, recipeCatalog);
            var sideRun = new GameSaveData { questStage = 0, locationId = "ashfall_village" };
            QuestProgressService.Reconcile(sideRun, questCatalog);
            Require(!QuestProgressService.TryAcceptSideQuest(sideRun, questCatalog, "side_ashfall_moonwort",
                        "dawnkeep_outpost") &&
                    !QuestProgressService.RecordObjectives(sideRun, questCatalog, "grow", "moonwort", 1,
                        out var unacceptedCompletions) && unacceptedCompletions.Count == 0,
                "A side quest must be accepted in its own region before its objective can progress.");
            Require(QuestProgressService.TryAcceptSideQuest(sideRun, questCatalog, "side_ashfall_moonwort",
                        "ashfall_village") && sideRun.activeSideQuestIds.Count == 1,
                "The regional journal must accept an available side quest and persist its active ID.");
            sideRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(sideRun));
            Require(SaveService.TryUpgradeToCurrent(sideRun) &&
                    QuestProgressService.Reconcile(sideRun, questCatalog) == false &&
                    QuestProgressService.IsActive(sideRun, "side_ashfall_moonwort"),
                "Accepted side quest IDs must survive save serialization and catalog reconciliation.");
            Require(QuestProgressService.RecordObjectives(sideRun, questCatalog, "grow", "moonwort", 1,
                        out var sideCompletions) && sideCompletions.Count == 1 &&
                    sideCompletions[0].id == "side_ashfall_moonwort" && sideRun.activeSideQuestIds.Count == 0 &&
                    !sideRun.chapterComplete,
                "A repeatable farming event must complete and remove its accepted side quest without advancing the story.");

            var sharedObjectiveCatalog = new QuestCatalogData
            {
                schemaVersion = 1,
                entries = new List<QuestDefinition>
                {
                    new QuestDefinition
                    {
                        id = "shared_story", arcId = "validation_arc", type = "story", stage = -1,
                        title = "Shared story target", objective = "Talk to the shared target.",
                        prerequisiteIds = new List<string>(),
                        objectives = new List<QuestObjectiveDefinition>
                        {
                            new QuestObjectiveDefinition { id = "story_talk", kind = "talk", targetId = "shared_target", description = "Talk to the shared target." }
                        }
                    },
                    new QuestDefinition
                    {
                        id = "shared_side", arcId = "validation_arc", type = "side", stage = -1,
                        locationId = "ashfall_village", title = "Shared side target", objective = "Ask about the same event.",
                        prerequisiteIds = new List<string>(),
                        objectives = new List<QuestObjectiveDefinition>
                        {
                            new QuestObjectiveDefinition { id = "side_talk", kind = "talk", targetId = "shared_target", description = "Talk to the shared target." }
                        }
                    }
                }
            };
            var sharedRun = new GameSaveData { locationId = "ashfall_village" };
            QuestProgressService.Reconcile(sharedRun, sharedObjectiveCatalog);
            Require(QuestProgressService.TryAcceptSideQuest(sharedRun, sharedObjectiveCatalog, "shared_side",
                        "ashfall_village") &&
                    QuestProgressService.RecordObjectives(sharedRun, sharedObjectiveCatalog, "talk", "shared_target", 1,
                        out var sharedCompletions) && sharedCompletions.Count == 2 &&
                    sharedRun.completedQuestIds.Contains("shared_story") && sharedRun.completedQuestIds.Contains("shared_side") &&
                    sharedRun.chapterComplete && sharedRun.activeSideQuestIds.Count == 0,
                "One world event must complete matching story and accepted side objectives together without a side quest blocking chapter completion.");

            var legacyTrail = new GameSaveData { schemaVersion = 3, questStage = 4, firstChoice = "trail" };
            Require(SaveService.TryUpgradeToCurrent(legacyTrail) &&
                    QuestProgressService.Reconcile(legacyTrail, questCatalog) &&
                    QuestProgressService.IsActive(legacyTrail, "ashfall_trail_report") &&
                    legacyTrail.completedQuestIds.Contains("ashfall_trail_evidence") &&
                    !legacyTrail.completedQuestIds.Contains("ashfall_shelter_witness"),
                "Legacy stage saves must migrate to the matching active branch quest ID.");

            ValidatePlayerWalkAtlas();
            ValidateDialoguePortraitAssets();
            ValidateAldenAnimationAtlases();
            ValidateRegionalMusicTracks();
            ValidateFieldAudioResources();
            Debug.Log("Validated " + ItemCatalog.Entries.Count + " item definitions, " + questCatalog.entries.Count +
                      " quest definitions, " + dialogueCatalog.entries.Count + " dialogue entries, " +
                      monsterCatalog.entries.Count + " monster species, " + encounterCatalog.entries.Count +
                      " encounter placements, " + recipeCatalog.entries.Count + " crafting recipes, " +
                      farmCatalog.entries.Count + " farm plots, " + fishingCatalog.entries.Count +
                      " data-driven fishing spots; objective-ID progression and persistence, both Ashfall prologue routes, both Ashfall Two Bells signal routes, " +
                      "both Dawnkeep disclosure routes, both Dawnkeep cadet testimony routes, both Cinderwell water/cistern routes and both Saltline trial outcomes, all three Salt Road witness routes, both Choir memory routes, both Hundredth Champion routes, both Outer-Wake testimony routes, both Waymarks Between Us distribution outcomes, both Last Oath endings, both consent archive policies, both Alden watch-roster policies, both Crownfall table-serving policies through Emberroot farming, baited Starlit fishing, cooking, meal consumption, branch rewards and save/resume, and all 99 named prior-hero memorials through save/resume, inventory/crafting/farming " +
                      "and both resource-model report policies through Skyroot/Glassplum/Echo Kelp/Salt Saffron harvests, baited fishing, two regional recipes and save/resume, and both Cinderwell pressure-wheel policies through Brineglass harvest, gated elite battle, assay crafting, filter installation and save/resume, " +
                      "both Salt Road milepost policies through Windglass harvest, baited Saltspool fishing, Roadglass elite battle, assay crafting, lens installation and save/resume, both Ruth Calder signature routes through the Lockhouse light-box and both Nella Pike missing-name archive routes through baited fishing, Windglass harvest, Tag Sleeve crafting/installation, family-access choices and save/resume, " +
                      "both Tamsin Wren warning-signal policies through baited fishing, Echo Kelp farming, pulse-brace crafting/installation, branch records and save/resume, " +
                      "transactions, schema v1-v9 migrations, all eleven travel/save locations, persistent encounter state and quest graph validation; " +
                      "validated 58 Tiny Creatures imports, 16 additional elite contracts, 54 Verdant Memory sprites and 55 Crawl sprites across 44 gated field cases, plus all regional gear and records, six telegraphed attack patterns, Rowan's 4-direction, 16-frame walk atlas, Alden's five knight action atlases, 15 streamed regional music tracks, six streamed ambient loops, four fishing cues, seven surface footsteps and 35 curated RPG Sound Pack cues.");
        }

        private static int CountItemCategory(string category)
        {
            var count = 0;
            foreach (var item in ItemCatalog.Entries)
                if (item != null && item.category == category) count++;
            return count;
        }

        private static int CountQuestType(QuestCatalogData catalog, string type)
        {
            var count = 0;
            if (catalog?.entries == null) return count;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.type == type) count++;
            return count;
        }

        private static int CountCompletedQuestType(GameSaveData save, QuestCatalogData catalog, string type)
        {
            var count = 0;
            if (catalog?.entries == null || save?.completedQuestIds == null) return count;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.type == type && save.completedQuestIds.Contains(quest.id)) count++;
            return count;
        }

        private static int CountQuestArc(QuestCatalogData catalog, string arcId, string type)
        {
            var count = 0;
            if (catalog?.entries == null) return count;
            foreach (var quest in catalog.entries)
                if (quest != null && quest.arcId == arcId && quest.type == type) count++;
            return count;
        }

        private static void ValidateDawnkeepFollowup(GameSaveData run, QuestCatalogData catalog, string testimony)
        {
            Require(QuestProgressService.IsActive(run, "order_empty_cots"),
                "The scratched roster must lead into the empty cadet bunks investigation.");
            Require(QuestProgressService.RecordObjective(run, catalog, "inspect", "dawnkeep_empty_cots", 1, out _) &&
                    QuestProgressService.IsActive(run, "order_cadet_testimony"),
                "Inspecting the cleared beds must bring Nia Porter forward as a witness.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "nia_porter", 1, out _);
            Require(QuestProgressService.IsActive(run, "order_transfer_ledger"),
                "Nia's testimony must lead to the southern transfer ledger.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "dawnkeep_transfer_ledger", 1, out _);
            Require(QuestProgressService.IsActive(run, "order_evidence_choice"),
                "The transfer ledger must unlock Rowan's decision about the missing cadets' names.");

            var choiceQuest = QuestProgressService.GetActiveQuest(run, catalog);
            var choiceId = testimony == "publish" ? "publish_roster" : "seal_roster";
            var choice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
            Require(choice != null && choice.flagValue == testimony,
                "Both Dawnkeep testimony options must carry their authored route flag.");
            QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
            QuestProgressService.RecordObjective(run, catalog, "choice", "order_testimony_choice", 1, out _);

            var selectedBranch = testimony == "publish" ? "order_open_testimony" : "order_sealed_record";
            var unselectedBranch = testimony == "publish" ? "order_sealed_record" : "order_open_testimony";
            var evidenceTarget = testimony == "publish" ? "order_public_noticeboard" : "order_sealed_dossier";
            Require(QuestProgressService.IsActive(run, selectedBranch) &&
                    !QuestProgressService.IsActive(run, unselectedBranch),
                "The testimony choice must activate only its selected evidence route.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", evidenceTarget, 1, out _);
            Require(QuestProgressService.IsActive(run, "order_cinderwell_dispatch") &&
                    !run.completedQuestIds.Contains(unselectedBranch),
                "The public and sealed records must converge on one southern aqueduct investigation.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "order_cinderwell_dispatch", 1, out _);
            Require(QuestProgressService.IsActive(run, "order_alden_reckoning"),
                "The Cinderwell dispatch must allow Rowan to confront Captain Alden Vale.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "captain_alden_vale", 1, out _);
            Require(QuestProgressService.IsActive(run, "order_cadet_oath"),
                "Alden's signed confession must send Rowan back to Nia with the evidence.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "nia_porter", 1, out _);
            Require(!run.chapterComplete && run.completedQuestIds.Count == 20 &&
                    QuestProgressService.IsActive(run, "cinder_arrival") &&
                    !run.completedQuestIds.Contains(unselectedBranch) &&
                    QuestProgressService.GetStoryFlag(run, "order_testimony") == testimony,
                "Either Dawnkeep route must preserve its testimony choice, award the cadet story, and open Cinderwell.");
        }

        private static void ValidateAllRegionalSideQuests(QuestCatalogData catalog)
        {
            foreach (var quest in catalog.entries)
            {
                if (quest == null || quest.type != "side") continue;
                Require(quest.objectives != null && quest.objectives.Count > 0,
                    "Each regional side quest must have concrete objectives for the validator simulation.");
                var run = new GameSaveData
                {
                    locationId = quest.locationId,
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                if (quest.prerequisiteIds != null)
                    run.completedQuestIds.AddRange(quest.prerequisiteIds);
                if (quest.prerequisiteGroups != null)
                    foreach (var prerequisiteGroup in quest.prerequisiteGroups)
                        if (prerequisiteGroup?.anyOfQuestIds != null && prerequisiteGroup.anyOfQuestIds.Count > 0)
                            run.completedQuestIds.Add(prerequisiteGroup.anyOfQuestIds[0]);
                if (!string.IsNullOrEmpty(quest.branchFlag))
                    QuestProgressService.SetStoryFlag(run, quest.branchFlag, quest.branchValue);
                var otherRegion = quest.locationId == "outerwake_archive" ? "greenwake_refuge" : "outerwake_archive";
                Require(!QuestProgressService.CanAcceptSideQuest(run, catalog, quest.id, otherRegion) &&
                        QuestProgressService.GetAvailableSideQuests(run, catalog, quest.locationId).Exists(
                            available => available.id == quest.id) &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, quest.id, quest.locationId),
                    "Every side quest must be available and accept only in its authored region: " + quest.id);
                var objectiveEventsMatched = true;
                foreach (var objective in quest.objectives)
                    objectiveEventsMatched &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                        objective.targetId, objective.requiredCount, out _);
                Require(objectiveEventsMatched && run.activeSideQuestIds.Count == 0 &&
                        run.completedQuestIds.Contains(quest.id),
                "Every regional side quest objective must complete against its authored world event: " + quest.id);
            }
        }

        private static void ValidateAshfallTwoBellsRoutes(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, EncounterCatalogData encounterCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var moonwortPlot = farmCatalog?.entries?.Find(plot => plot != null && plot.cropId == "moonwort" &&
                plot.locationId == "ashfall_village");
            var signalEncounter = EncounterCatalogService.FindById(encounterCatalog, "ashfall_signal_goblin_site");
            var expectedLandmarkTargets = new[]
            {
                "harper_wills", "ashfall_signal_frame", "ashfall_signal_vane", "ashfall_signal_mark",
                "ashfall_signal_well", "ashfall_signal_ridge", "ashfall_signal_bell_test",
                "ashfall_signal_flag_test"
            };
            Require(signalEncounter != null && signalEncounter.requiredQuestId == "side_ashfall_two_bells_clear" &&
                    signalEncounter.defeatObjectiveTargetId == "ashfall_signal_goblin" &&
                    signalEncounter.monsterId == "tiny_af_ash_goblin" && moonwortPlot != null,
                "The Two Bells route must bind its unique gated Ash Goblin encounter and Moonwort plot.");
            foreach (var targetId in expectedLandmarkTargets)
                Require(landmarkCatalog?.entries?.Exists(entry => entry.targetId == targetId) == true,
                    "The Two Bells route must place its authored Ashfall landmark: " + targetId);

            foreach (var route in new[] { "audible", "visible" })
            {
                var run = new GameSaveData
                {
                    locationId = "ashfall_village",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "ashfall_shelter_report" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_open");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_frame");
                Require(!QuestProgressService.IsActive(run, signalEncounter.requiredQuestId) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, signalEncounter.requiredQuestId,
                            run.locationId),
                    "The Two Bells encounter must stay unavailable until its dedicated fight contract is accepted.");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_clear");
                ApplyValidationReward(run, signalEncounter.reward);
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_mira");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_vane");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_gideon");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_oath");

                var growQuest = QuestCatalogService.FindById(catalog, "side_ashfall_two_bells_grow");
                var growCompletions = new List<QuestDefinition>();
                Require(growQuest != null && QuestProgressService.TryAcceptSideQuest(run, catalog, growQuest.id,
                            run.locationId) && FarmPlotProgressService.TryPlant(run, moonwortPlot) &&
                        FarmPlotProgressService.Tick(run, moonwortPlot.growSeconds) &&
                        FarmPlotProgressService.TryHarvest(run, moonwortPlot) &&
                        InventoryService.Count(run, "moonwort_leaf") >= 2 &&
                        QuestProgressService.RecordObjectives(run, catalog, "grow", "moonwort", 1,
                            out growCompletions) && growCompletions.Exists(quest => quest.id == growQuest.id),
                    "The Two Bells field route must spend its offered seed, grow Moonwort, harvest leaves and advance the crop objective.");
                foreach (var completed in growCompletions) ApplyValidationReward(run, completed.reward);

                var mixQuest = QuestCatalogService.FindById(catalog, "side_ashfall_two_bells_mix");
                var mixCompletions = new List<QuestDefinition>();
                Require(mixQuest != null && InventoryService.Count(run, "ashfall_signal_ash") == 1 &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, mixQuest.id, run.locationId) &&
                        CraftingService.TryCraft(run, recipeCatalog, "brew_rainmark_chalk", "ashfall_herb_table",
                            out var chalkRecipe, out _) && chalkRecipe?.outputItemId == "rainmark_chalk" &&
                        InventoryService.Count(run, "moonwort_leaf") == 1 &&
                        QuestProgressService.RecordObjectives(run, catalog, "craft", "rainmark_chalk", 1,
                            out mixCompletions) && mixCompletions.Exists(quest => quest.id == mixQuest.id) &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry =>
                            entry.id == "ashfall_two_bells_calibration"),
                    "The shared Two Bells route must craft its weather-resistant mark from real farm and encounter rewards, then unlock the method record.");
                foreach (var completed in mixCompletions) ApplyValidationReward(run, completed.reward);

                Require(InventoryService.Count(run, "rainmark_chalk") == 1 &&
                        InventoryService.Remove(run, "rainmark_chalk", 1) &&
                        InventoryService.Count(run, "rainmark_chalk") == 0,
                    "Marking the return route must consume the Phấn Dấu Mưa item made from this field study.");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_mark");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_well");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_two_bells_ridge");

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_ashfall_two_bells_choose");
                var choice = choiceQuest?.choices?.Find(candidate => candidate.flagValue == route);
                var rejectedRoute = route == "audible" ? "visible" : "audible";
                var selectedFollowUp = route == "audible" ? "side_ashfall_two_bells_bell_test" :
                    "side_ashfall_two_bells_flag_test";
                var rejectedFollowUp = route == "audible" ? "side_ashfall_two_bells_flag_test" :
                    "side_ashfall_two_bells_bell_test";
                Require(choiceQuest != null && choice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The shared Two Bells survey must unlock its authored choice.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice", "harper_wills", 1,
                            out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "Harper's selected signal must be saved as a completed choice objective.");
                foreach (var completed in choiceCompletions) ApplyValidationReward(run, completed.reward);
                ApplyValidationReward(run, choice.reward);
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedFollowUp, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedFollowUp, run.locationId),
                    "The signal choice must activate only its matching physical test.");
                CompleteAshfallSideQuestForValidation(run, catalog, selectedFollowUp);

                var finalQuestId = route == "audible" ? "side_ashfall_two_bells_bell_report" :
                    "side_ashfall_two_bells_flag_report";
                CompleteAshfallSideQuestForValidation(run, catalog, finalQuestId);
                var rewardId = route == "audible" ? "ashfall_bellstrap" : "ashfall_windthread_charm";
                var codexId = route == "audible" ? "ashfall_two_bells_audible_protocol" :
                    "ashfall_two_bells_visible_protocol";
                var reward = ItemCatalog.Find(rewardId);
                Require(reward?.category == "equipment" && reward.equipmentSlot == "charm" &&
                        InventoryService.Count(run, rewardId) == 1 && InventoryService.TryEquip(run, rewardId) &&
                        InventoryService.AttackBonus(run) == reward.attackBonus &&
                        InventoryService.GuardBonus(run) == reward.guardBonus &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry => entry.id == codexId) &&
                        !run.completedQuestIds.Contains(route == "audible" ?
                            "side_ashfall_two_bells_flag_test" : "side_ashfall_two_bells_bell_test"),
                    "Each Two Bells outcome must award and equip its own charm, unlock its matching field record and leave the other route incomplete.");
            }
        }

        private static void ValidateAshfallTallyRoutes(QuestCatalogData catalog, CodexCatalogData codexCatalog)
        {
            foreach (var route in new[] { "public", "sealed" })
            {
                var run = new GameSaveData
                {
                    locationId = "ashfall_village",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "ashfall_shelter_report" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_tally_marks");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_gideon_count");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_brace_direction");

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_ashfall_tally_disclosure");
                var choice = choiceQuest?.choices?.Find(candidate => candidate.flagValue == route);
                Require(choiceQuest != null && choice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The three Ashfall evidence checks must unlock the authored disclosure choice.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice", "ashfall_shelter_record_desk", 1,
                            out var choiceCompletions) && choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "The Ashfall disclosure choice must complete its choice objective and persist its branch flag.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, choice.reward);

                var selectedId = route == "public" ? "side_ashfall_tally_public_copy" : "side_ashfall_tally_sealed_copy";
                var rejectedId = route == "public" ? "side_ashfall_tally_sealed_copy" : "side_ashfall_tally_public_copy";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedId, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedId, run.locationId),
                    "The tally decision must expose only the matching public or sealed follow-up.");
                CompleteAshfallSideQuestForValidation(run, catalog, selectedId);

                var itemId = route == "public" ? "fieldgear_ashfall_chalk_charm" : "fieldgear_ashfall_door_wedge";
                var codexId = route == "public" ? "ashfall_chalk_tally_record" : "ashfall_sealed_tally_record";
                var gear = ItemCatalog.Find(itemId);
                Require(InventoryService.Count(run, itemId) == 1 && gear != null &&
                        InventoryService.TryEquip(run, itemId) && InventoryService.GuardBonus(run) == gear.guardBonus &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry => entry.id == codexId),
                    "Each Ashfall tally route must award its unique equippable charm and unlock the matching evidence record.");
            }
        }

        private static void ValidateAshfallMusterRoutes(QuestCatalogData catalog, CodexCatalogData codexCatalog)
        {
            foreach (var prologueReport in new[] { "ashfall_shelter_report", "ashfall_trail_report" })
            foreach (var policy in new[] { "shared_board", "household_slips" })
            {
                var run = new GameSaveData
                {
                    locationId = "ashfall_village",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { prologueReport },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                var opener = "side_ashfall_muster_open";
                Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(quest => quest.id == opener) &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, opener, run.locationId),
                    "Either Ashfall report must unlock the optional muster record without changing the main story route.");
                QuestProgressService.RecordObjectives(run, catalog, "talk", "mira_cole", 1, out var completed);
                Require(completed.Exists(quest => quest.id == opener),
                    "Mira must start the community-preparation record through her authored conversation.");
                ApplyValidationReward(run, completed.Find(quest => quest.id == opener).reward);
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_muster_board");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_blank_rows");
                CompleteAshfallSideQuestForValidation(run, catalog, "side_ashfall_shelter_cloth");

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_ashfall_departure_plan");
                var choice = QuestCatalogService.FindChoice(choiceQuest, policy);
                Require(choiceQuest != null && choice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The recorded board, missing-row interview and shelter cloth must unlock both map-copy policies.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice", "ashfall_departure_plan", 1,
                            out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "Choosing a shared map or private household slip must complete the authored choice objective.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, choice.reward);

                var itemId = policy == "shared_board" ? "ashfall_shared_map_pin" : "ashfall_household_route_knot";
                var otherItemId = policy == "shared_board" ? "ashfall_household_route_knot" : "ashfall_shared_map_pin";
                var item = ItemCatalog.Find(itemId);
                Require(QuestProgressService.GetStoryFlag(run, choiceQuest.choiceFlag) == policy &&
                        InventoryService.Count(run, itemId) == 1 && InventoryService.Count(run, otherItemId) == 0 &&
                        item?.category == "equipment" && InventoryService.TryEquip(run, itemId) &&
                        InventoryService.AttackBonus(run) == item.attackBonus &&
                        InventoryService.GuardBonus(run) == item.guardBonus &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run)
                            .Exists(entry => entry.id == "ashfall_route_copy_record"),
                    "Each saved map-copy policy must award only its own usable charm, retain its flag and unlock the shared record.");
            }
        }

        private static void CompleteAshfallSideQuestForValidation(GameSaveData run, QuestCatalogData catalog,
            string questId)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The Ashfall evidence chain must unlock and accept " + questId + ".");
            foreach (var objective in quest.objectives)
            {
                Require(QuestProgressService.RecordObjectives(run, catalog, objective.kind, objective.targetId,
                            objective.requiredCount, out var completions) &&
                        completions.Exists(completed => completed.id == questId),
                    "The Ashfall evidence event must complete its authored objective: " + questId + ".");
                foreach (var completed in completions) ApplyValidationReward(run, completed.reward);
            }
        }

        private static void ApplyValidationReward(GameSaveData run, QuestRewardDefinition reward)
        {
            if (reward == null) return;
            run.gold += reward.gold;
            if (reward.items == null) return;
            foreach (var item in reward.items)
                if (item != null) InventoryService.Add(run, item.itemId, item.quantity);
        }

        private static void ValidateWaymarksBetweenUs(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog,
            FishingCatalogData fishingCatalog, FarmCatalogData farmCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "ashfall_village",
                inventory = new List<InventoryStackData>(),
                activeSideQuestIds = new List<string>(),
                completedQuestIds = new List<string> { "ashfall_shelter_report" },
                questObjectiveProgress = new List<QuestObjectiveProgressData>()
            };
            QuestProgressService.Reconcile(run, catalog);
            CompleteWaymarksStage(run, catalog, "side_waymarks_ashfall");

            run.locationId = "dawnkeep_outpost";
            Require(!QuestProgressService.CanAcceptSideQuest(run, catalog, "side_waymarks_dawnkeep", run.locationId),
                "The first route marker alone must not bypass the Dawnkeep arrival story gate.");
            run.completedQuestIds.Add("order_arrival");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, "side_waymarks_dawnkeep", run.locationId),
                "The Dawnkeep route stage must become available at its own lakeshore.");
            var lakeshore = fishingCatalog.entries.Find(spot => spot.id == "dawnkeep_lakeshore");
            var caught = lakeshore == null ? "" : FishingCatalogService.RollCatch(lakeshore, 0.2f);
            Require(caught == "blackreed_trout" && InventoryService.Remove(run, lakeshore.baitItemId, 1) &&
                    InventoryService.Add(run, caught, 1) == 1,
                "The Dawnkeep stage must use a real baited lake catch before placing its route marker.");
            RecordWaymarksEvent(run, catalog, "fish", caught, 1,
                "The recorded trout must complete the Dawnkeep water reading.");
            RecordWaymarksEvent(run, catalog, "inspect", "waymarks_dawnkeep_landing", 1,
                "The lakeshore landing marker must complete the Dawnkeep stage.");

            run.locationId = "dawnkeep_barracks";
            run.completedQuestIds.Add("order_cadet_oath");
            CompleteWaymarksStage(run, catalog, "side_waymarks_barracks");
            Require(InventoryService.Count(run, "salt_saffron_seed") >= 1,
                "The blank waypass stage must provide the seed needed by Cinderwell's route station.");

            run.locationId = "cinderwell_basin";
            run.completedQuestIds.Add("cinder_recovery");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, "side_waymarks_cinderwell", run.locationId),
                "The Cinderwell route stage must open after the recovery report.");
            var saffronPlot = farmCatalog.entries.Find(plot => plot.cropId == "salt_saffron" &&
                plot.locationId == run.locationId);
            Require(saffronPlot != null && FarmPlotProgressService.TryPlant(run, saffronPlot) &&
                    FarmPlotProgressService.Tick(run, saffronPlot.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(run, saffronPlot) &&
                    InventoryService.Count(run, saffronPlot.harvestItemId) == saffronPlot.harvestQuantity,
                "The wayhouse stage must plant and harvest Salt Saffron at its real Cinderwell plot.");
            RecordWaymarksEvent(run, catalog, "grow", "salt_saffron", 1,
                "Harvesting Salt Saffron must record the Cinderwell station crop.");
            RecordWaymarksEvent(run, catalog, "inspect", "waymarks_cinderwell_cup", 1,
                "The measured cup must finish the Cinderwell wayhouse stage.");

            run.locationId = "salt_road";
            run.completedQuestIds.Add("salt_arrival");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, "side_waymarks_saltroad", run.locationId),
                "The Salt Road wayhouse must expose its gated side encounter only after accepting the contract.");
            var ambush = EncounterCatalogService.FindById(encounterCatalog, "waymarks_saltroad_hound");
            var hound = MonsterCatalogService.FindById(monsterCatalog, "salt_hound");
            var houndProgress = EncounterProgressService.GetOrCreate(run, ambush, hound);
            Require(ambush != null && hound != null && houndProgress != null &&
                    ambush.requiredQuestId == "side_waymarks_saltroad" &&
                    QuestProgressService.IsActive(run, ambush.requiredQuestId),
                "The roadside Salt Hound must use the accepted side quest as its encounter gate.");
            houndProgress.health = 17;
            var resumedRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
            var resumedHound = EncounterProgressService.GetOrCreate(resumedRun, ambush, hound);
            Require(resumedHound.health == 17 && !resumedHound.defeated,
                "The wayhouse encounter's damaged health must persist when the offline save resumes.");
            resumedHound.health = 0;
            resumedHound.defeated = true;
            run = resumedRun;
            ApplyValidationReward(run, ambush.reward);
            RecordWaymarksEvent(run, catalog, "defeat", "waymarks_roadside_hound", 1,
                "Defeating the gated Salt Hound must complete the combat objective.");
            RecordWaymarksEvent(run, catalog, "interact", "waymarks_saltroad_rest_marker", 1,
                "The repaired rest marker must finish the Salt Road stage.");

            run.locationId = "choir_beneath_lake";
            run.completedQuestIds.Add("salt_route_handoff");
            run.completedQuestIds.Add("choir_arrival");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, "side_waymarks_choir", run.locationId),
                "The acoustic route stage must open in the Choir after the Salt Road handoff.");
            var whisperPool = fishingCatalog.entries.Find(spot => spot.id == "choir_whisper_pool");
            caught = whisperPool == null ? "" : FishingCatalogService.RollCatch(whisperPool, 0.2f);
            Require(caught == "whisper_koi" && InventoryService.Remove(run, whisperPool.baitItemId, 1) &&
                    InventoryService.Add(run, caught, 1) == 1,
                "The Choir stage must record a real Whisper Koi catch using the supplied bait.");
            RecordWaymarksEvent(run, catalog, "fish", caught, 1,
                "Catching the Whisper Koi must complete the Choir water reading.");
            RecordWaymarksEvent(run, catalog, "inspect", "waymarks_choir_clickstone", 1,
                "The two-tap signal stone must finish the Choir stage.");

            run.locationId = "greenwake_refuge";
            run.completedQuestIds.Add("champion_star_map");
            CompleteWaymarksStage(run, catalog, "side_waymarks_greenwake");
            Require(InventoryService.Count(run, "skyroot_seed") >= 1,
                "The Greenwake shelter stage must supply a Skyroot seed for the final instrument check.");

            run.locationId = "outerwake_archive";
            run.completedQuestIds.Add("archive_return_report");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, "side_waymarks_outerwake", run.locationId),
                "The final route survey must open after the Outer-Wake report.");
            var skyrootPlot = farmCatalog.entries.Find(plot => plot.cropId == "skyroot" &&
                plot.locationId == run.locationId);
            Require(skyrootPlot != null && FarmPlotProgressService.TryPlant(run, skyrootPlot) &&
                    FarmPlotProgressService.Tick(run, skyrootPlot.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(run, skyrootPlot),
                "The Outer-Wake station must use an actual Skyroot planting and harvest.");
            RecordWaymarksEvent(run, catalog, "grow", "skyroot", 1,
                "The Outer-Wake Skyroot harvest must progress its route objective.");
            var celestialPool = fishingCatalog.entries.Find(spot => spot.id == "outerwake_celestial_pool");
            caught = celestialPool == null ? "" : FishingCatalogService.RollCatch(celestialPool, 0.2f);
            Require(caught == "farwake_carp" && InventoryService.Remove(run, celestialPool.baitItemId, 1) &&
                    InventoryService.Add(run, caught, 1) == 1,
                "The Outer-Wake beacon check must consume supplied bait and record a Farwake Carp catch.");
            RecordWaymarksEvent(run, catalog, "fish", caught, 1,
                "The Farwake Carp must complete the Outer-Wake current reading.");
            RecordWaymarksEvent(run, catalog, "inspect", "waymarks_outerwake_beacon", 1,
                "The inspected sky beacon must complete all eight regional survey stages.");

            var sharedRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
            foreach (var route in new[] { "public_route", "courier_route" })
            {
                var branchRun = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(sharedRun));
                Require(QuestProgressService.TryAcceptSideQuest(branchRun, catalog,
                            "side_waymarks_distribution", branchRun.locationId),
                    "The complete route survey must open its distribution choice.");
                var choiceQuest = QuestCatalogService.FindById(catalog, "side_waymarks_distribution");
                var choice = QuestCatalogService.FindChoice(choiceQuest,
                    route == "public_route" ? "publish_waymarks" : "send_by_courier");
                Require(choice != null && choice.flagValue == route,
                    "Both Waymarks outcomes must resolve to their authored choice IDs.");
                QuestProgressService.SetStoryFlag(branchRun, choiceQuest.choiceFlag, choice.flagValue);
                RecordWaymarksEvent(branchRun, catalog, "choice", "waymarks_distribution_desk", 1,
                    "The distribution decision must complete its choice objective.");
                ApplyValidationReward(branchRun, choice.reward);

                var selectedId = route == "public_route" ? "side_waymarks_public_copy" : "side_waymarks_courier_copy";
                var rejectedId = route == "public_route" ? "side_waymarks_courier_copy" : "side_waymarks_public_copy";
                Require(QuestProgressService.CanAcceptSideQuest(branchRun, catalog, selectedId, branchRun.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(branchRun, catalog, rejectedId, branchRun.locationId),
                    "The Waymarks distribution choice must make its two map-release routes mutually exclusive.");
                CompleteWaymarksStage(branchRun, catalog, selectedId);

                var itemId = route == "public_route" ? "fieldgear_waymarks_compass_charm" :
                    "fieldgear_waymarks_steward_charm";
                var codexId = route == "public_route" ? "waymarks_public_route_charter" :
                    "waymarks_courier_custody_record";
                var gear = ItemCatalog.Find(itemId);
                Require(gear != null && InventoryService.Count(branchRun, itemId) == 1 &&
                        InventoryService.TryEquip(branchRun, itemId) &&
                        (route == "public_route" ? InventoryService.AttackBonus(branchRun) == 1 :
                            InventoryService.GuardBonus(branchRun) == 1) &&
                        CodexCatalogService.GetUnlocked(codexCatalog, branchRun).Exists(entry => entry.id == codexId),
                    "Each Waymarks outcome must grant its own equippable charm and unlock its matching field record.");
            }
        }

        private static void CompleteWaymarksStage(GameSaveData run, QuestCatalogData catalog, string questId)
        {
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The Waymarks chain must unlock and accept " + questId + " in its authored region.");
            var quest = QuestCatalogService.FindById(catalog, questId);
            foreach (var objective in quest.objectives)
                RecordWaymarksEvent(run, catalog, objective.kind, objective.targetId, objective.requiredCount,
                    "The Waymarks event must progress " + questId + "/" + objective.id + ".");
            Require(run.completedQuestIds.Contains(questId),
                "All authored Waymarks objectives must complete " + questId + ".");
        }

        private static void RecordWaymarksEvent(GameSaveData run, QuestCatalogData catalog, string kind,
            string targetId, int count, string assertion)
        {
            Require(QuestProgressService.RecordObjectives(run, catalog, kind, targetId, count,
                        out var completions), assertion);
            foreach (var quest in completions) ApplyValidationReward(run, quest.reward);
        }

        private static void ValidateTinyCreatureFieldbook(QuestCatalogData questCatalog,
            CodexCatalogData codexCatalog, DialogueCatalogData dialogueCatalog,
            MonsterCatalogData monsterCatalog, EncounterCatalogData encounterCatalog)
        {
            var fieldMonsters = monsterCatalog.entries.FindAll(monster =>
                monster != null && monster.spriteResource != null &&
                monster.spriteResource.StartsWith("tiny_", System.StringComparison.Ordinal));
            var uniqueResources = new HashSet<string>();
            var commonCount = 0;
            var eliteCount = 0;
            foreach (var monster in fieldMonsters)
            {
                uniqueResources.Add(monster.spriteResource);
                if (monster.rank == "common") commonCount++;
                if (monster.rank == "elite") eliteCount++;
            }

            Require(fieldMonsters.Count == 58 && uniqueResources.Count == 58 &&
                    commonCount == 42 && eliteCount == 16,
                "The CC0 fieldbook must contain fifty-eight distinct resource-backed species with authored common and elite ranks.");

            var chainsByLocation = new Dictionary<string, List<QuestDefinition>>();
            foreach (var quest in questCatalog.entries)
            {
                if (quest == null || quest.type != "side" ||
                    !quest.id.StartsWith("side_field_", System.StringComparison.Ordinal)) continue;
                if (!chainsByLocation.TryGetValue(quest.locationId, out var chain))
                {
                    chain = new List<QuestDefinition>();
                    chainsByLocation.Add(quest.locationId, chain);
                }
                chain.Add(quest);
            }

            Require(chainsByLocation.Count == 11,
                "Field contracts must cover the eleven authored campaign locations without adding disconnected maps.");
            var checkedQuests = 0;
            foreach (var chainEntry in chainsByLocation)
            {
                var chain = chainEntry.Value;
                Require(chain.Count >= 3 && chain.Count <= 4 && chain[0].prerequisiteIds != null &&
                        chain[0].prerequisiteIds.Count == 1,
                    "Each location must begin with a gated field-contract chain: " + chainEntry.Key);
                var run = new GameSaveData
                {
                    locationId = chainEntry.Key,
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string>(chain[0].prerequisiteIds),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    inventory = new List<InventoryStackData>()
                };

                for (var index = 0; index < chain.Count; index++)
                {
                    var quest = chain[index];
                    Require(QuestProgressService.GetAvailableSideQuests(run, questCatalog, run.locationId)
                                .Exists(available => available.id == quest.id) &&
                            QuestProgressService.TryAcceptSideQuest(run, questCatalog, quest.id, run.locationId),
                        "A field contract must unlock only at its authored place in the chain: " + quest.id);
                    var objective = quest.objectives[0];
                    var encounter = encounterCatalog.entries.Find(candidate =>
                        candidate != null && candidate.requiredQuestId == quest.id);
                    var monster = MonsterCatalogService.FindById(monsterCatalog, objective.targetId);
                    var texture = monster == null ? null : Resources.Load<Texture2D>("Art/" + monster.spriteResource);
                    var importer = monster == null ? null :
                        AssetImporter.GetAtPath("Assets/Resources/Art/" + monster.spriteResource + ".png") as TextureImporter;
                    Require(objective.kind == "defeat" && objective.requiredCount == 1 &&
                            monster != null && monster.spritePixelsPerUnit == 16 &&
                            texture != null && texture.width == 16 && texture.height == 16 &&
                            importer != null && importer.filterMode == FilterMode.Point &&
                            !importer.mipmapEnabled &&
                            importer.textureCompression == TextureImporterCompression.Uncompressed &&
                            encounter != null && encounter.monsterId == monster.id &&
                            encounter.locationId == quest.locationId &&
                            encounter.defeatObjectiveTargetId == monster.id &&
                            DialogueCatalogService.Find(dialogueCatalog, encounter.defeatDialogueId) != null &&
                            DialogueCatalogService.Find(dialogueCatalog, encounter.downDialogueId) != null,
                        "Every field contract must place its authored CC0 sprite, combat target, retreat response and evidence dialogue: " + quest.id);
                    Require(QuestProgressService.RecordObjectives(run, questCatalog, "defeat", monster.id, 1,
                                out var completed) && completed.Exists(item => item.id == quest.id) &&
                            run.completedQuestIds.Contains(quest.id) && run.activeSideQuestIds.Count == 0,
                        "Defeating a field species must complete its accepted regional contract: " + quest.id);
                    var rewardId = quest.reward.items[0].itemId;
                    var equipment = ItemCatalog.Find(rewardId);
                    InventoryService.Add(run, rewardId, 1);
                    Require(equipment != null && equipment.category == "equipment" &&
                            InventoryService.TryEquip(run, rewardId) &&
                            InventoryService.AttackBonus(run) >= equipment.attackBonus &&
                            InventoryService.GuardBonus(run) >= equipment.guardBonus,
                        "Each bestiary contract must grant a real, equippable species-linked reward: " + quest.id);
                    checkedQuests++;
                }

                var fieldRecord = codexCatalog.entries.Find(record =>
                    record != null && record.unlockQuestId == chain[chain.Count - 1].id);
                Require(fieldRecord != null &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(record => record.id == fieldRecord.id),
                    "Completing a location's full fieldbook route must unlock its authored ecological record: " +
                    chainEntry.Key);
            }

            Require(checkedQuests == 42,
                "The validator must simulate all forty-two sequential common and elite field-contract objectives.");
        }

        private static void ValidateTinyEliteContracts(QuestCatalogData questCatalog, CodexCatalogData codexCatalog,
            DialogueCatalogData dialogueCatalog, MonsterCatalogData monsterCatalog,
            EncounterCatalogData encounterCatalog)
        {
            var elites = monsterCatalog.entries.FindAll(monster =>
                monster != null && monster.id.StartsWith("tiny_elite_", System.StringComparison.Ordinal));
            var uniqueResources = new HashSet<string>();
            var commonCount = 0;
            var eliteCount = 0;
            foreach (var monster in elites)
            {
                uniqueResources.Add(monster.spriteResource);
                if (monster.rank == "common") commonCount++;
                if (monster.rank == "elite") eliteCount++;
            }
            Require(elites.Count == 16 && uniqueResources.Count == 16 && commonCount == 8 && eliteCount == 8,
                "The additional regional set must use sixteen distinct CC0 sprites split across eight common and eight elite creatures.");

            var chains = new Dictionary<string, List<QuestDefinition>>();
            foreach (var quest in questCatalog.entries)
            {
                if (quest == null || quest.type != "side" ||
                    !quest.id.StartsWith("side_elite_", System.StringComparison.Ordinal)) continue;
                if (!chains.TryGetValue(quest.locationId, out var chain))
                {
                    chain = new List<QuestDefinition>();
                    chains.Add(quest.locationId, chain);
                }
                chain.Add(quest);
            }
            Require(chains.Count == 11,
                "Elite field contracts must connect to all eleven campaign maps without creating isolated regions.");

            var checkedContracts = 0;
            foreach (var entry in chains)
            {
                var chain = entry.Value;
                var run = new GameSaveData
                {
                    locationId = entry.Key,
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string>(chain[0].prerequisiteIds),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    inventory = new List<InventoryStackData>()
                };
                for (var index = 0; index < chain.Count; index++)
                {
                    var quest = chain[index];
                    Require(QuestProgressService.GetAvailableSideQuests(run, questCatalog, run.locationId)
                                .Exists(available => available.id == quest.id) &&
                            QuestProgressService.TryAcceptSideQuest(run, questCatalog, quest.id, quest.locationId),
                        "Each elite contract must unlock after its predecessor and accept only in the authored map: " + quest.id);

                    var objective = quest.objectives[0];
                    var monster = MonsterCatalogService.FindById(monsterCatalog, objective.targetId);
                    var encounter = encounterCatalog.entries.Find(candidate =>
                        candidate != null && candidate.requiredQuestId == quest.id);
                    var texture = monster == null ? null : Resources.Load<Texture2D>("Art/" + monster.spriteResource);
                    var importer = monster == null ? null : AssetImporter.GetAtPath(
                        "Assets/Resources/Art/" + monster.spriteResource + ".png") as TextureImporter;
                    Require(objective.kind == "defeat" && objective.requiredCount == 1 &&
                            monster != null && monster.spritePixelsPerUnit == 16 &&
                            texture != null && texture.width == 16 && texture.height == 16 &&
                            importer != null && importer.filterMode == FilterMode.Point && !importer.mipmapEnabled &&
                            importer.textureCompression == TextureImporterCompression.Uncompressed &&
                            encounter != null && encounter.monsterId == monster.id &&
                            encounter.defeatObjectiveTargetId == monster.id &&
                            DialogueCatalogService.Find(dialogueCatalog, encounter.defeatDialogueId) != null &&
                            DialogueCatalogService.Find(dialogueCatalog, encounter.downDialogueId) != null,
                        "Each elite contract must place its sprite, combat encounter, retreat response and authored record: " + quest.id);
                    Require(QuestProgressService.RecordObjectives(run, questCatalog, "defeat", monster.id, 1,
                                out var completed) && completed.Exists(done => done.id == quest.id) &&
                            run.completedQuestIds.Contains(quest.id) && run.activeSideQuestIds.Count == 0,
                        "Defeating an elite-contract species must finish its accepted local quest: " + quest.id);
                    var reward = quest.reward.items[0];
                    var item = ItemCatalog.Find(reward.itemId);
                    InventoryService.Add(run, reward.itemId, reward.quantity);
                    Require(item != null && item.category == "equipment" &&
                            InventoryService.TryEquip(run, reward.itemId),
                        "Each elite contract must reward a unique equippable item: " + quest.id);
                    checkedContracts++;
                }

                var record = codexCatalog.entries.Find(candidate =>
                    candidate != null && candidate.unlockQuestId == chain[chain.Count - 1].id);
                Require(record != null && CodexCatalogService.GetUnlocked(codexCatalog, run)
                            .Exists(unlocked => unlocked.id == record.id),
                    "Finishing a local elite-contract sequence must unlock its region's field record: " + entry.Key);
            }
            Require(checkedContracts == 16,
                "The validator must exercise all sixteen extra elite contracts, sequence gates and equipment transactions.");
        }

        private static void ValidateVerdantMemoryContracts(QuestCatalogData questCatalog, CodexCatalogData codexCatalog,
            DialogueCatalogData dialogueCatalog, MonsterCatalogData monsterCatalog,
            EncounterCatalogData encounterCatalog)
        {
            var species = monsterCatalog.entries.FindAll(monster =>
                monster != null && monster.id.StartsWith("verdant_", System.StringComparison.Ordinal));
            var resources = new HashSet<string>();
            var commonCount = 0;
            var eliteCount = 0;
            foreach (var monster in species)
            {
                resources.Add(monster.spriteResource);
                if (monster.rank == "common") commonCount++;
                if (monster.rank == "elite") eliteCount++;
            }
            Require(species.Count == 54 && resources.Count == 54 && commonCount == 26 && eliteCount == 28,
                "Verdant Memory must use fifty-four distinct 32-pixel sprites split into twenty-six common and twenty-eight elite species.");

            var chains = new Dictionary<string, List<QuestDefinition>>();
            foreach (var quest in questCatalog.entries)
            {
                if (quest == null || quest.type != "side" ||
                    !quest.id.StartsWith("side_verdant_", System.StringComparison.Ordinal)) continue;
                if (!chains.TryGetValue(quest.locationId, out var chain))
                {
                    chain = new List<QuestDefinition>();
                    chains.Add(quest.locationId, chain);
                }
                chain.Add(quest);
            }

            Require(chains.Count == 11,
                "Verdant Memory must extend all eleven existing campaign maps.");
            var checkedQuests = 0;
            var checkedObjectives = 0;
            foreach (var entry in chains)
            {
                var chain = entry.Value;
                Require(chain.Count == 2 && chain[0].prerequisiteIds != null &&
                        chain[0].prerequisiteIds.Count == 1,
                    "Each region must receive exactly two gated Verdant Memory cases: " + entry.Key);
                var run = new GameSaveData
                {
                    locationId = entry.Key,
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string>(chain[0].prerequisiteIds),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    inventory = new List<InventoryStackData>()
                };

                for (var questIndex = 0; questIndex < chain.Count; questIndex++)
                {
                    var quest = chain[questIndex];
                    Require(quest.objectives != null && quest.objectives.Count >= 2 && quest.objectives.Count <= 3 &&
                            quest.reward?.items != null && quest.reward.items.Count == quest.objectives.Count &&
                            QuestProgressService.GetAvailableSideQuests(run, questCatalog, run.locationId)
                                .Exists(available => available.id == quest.id) &&
                            QuestProgressService.TryAcceptSideQuest(run, questCatalog, quest.id, quest.locationId),
                        "Every Verdant case must unlock in order, accept in its own map, and contain a multi-target reward: " + quest.id);

                    var encounters = encounterCatalog.entries.FindAll(candidate =>
                        candidate != null && candidate.requiredQuestId == quest.id);
                    Require(encounters.Count == quest.objectives.Count,
                        "Every multi-target case needs one encounter for each required species: " + quest.id);
                    for (var objectiveIndex = 0; objectiveIndex < quest.objectives.Count; objectiveIndex++)
                    {
                        var objective = quest.objectives[objectiveIndex];
                        var monster = MonsterCatalogService.FindById(monsterCatalog, objective.targetId);
                        var encounter = encounters.Find(candidate => candidate.monsterId == objective.targetId);
                        var texture = monster == null ? null : Resources.Load<Texture2D>("Art/" + monster.spriteResource);
                        var importer = monster == null ? null : AssetImporter.GetAtPath(
                            "Assets/Resources/Art/" + monster.spriteResource + ".png") as TextureImporter;
                        Require(objective.kind == "defeat" && objective.requiredCount == 1 && monster != null &&
                                monster.spritePixelsPerUnit == 32 && texture != null &&
                                texture.width == 32 && texture.height == 32 &&
                                importer != null && importer.filterMode == FilterMode.Point &&
                                !importer.mipmapEnabled &&
                                importer.textureCompression == TextureImporterCompression.Uncompressed &&
                                encounter != null && encounter.locationId == quest.locationId &&
                                encounter.defeatObjectiveTargetId == monster.id &&
                                encounter.contributesToQuest &&
                                DialogueCatalogService.Find(dialogueCatalog, encounter.defeatDialogueId)?.lines.Count == 2 &&
                                DialogueCatalogService.Find(dialogueCatalog, encounter.downDialogueId) != null,
                            "Each Verdant objective must resolve to its crisp CC0 sprite, encounter, two-line field note and retreat response: " + objective.targetId);

                        var reward = quest.reward.items.Find(item => item != null &&
                            item.itemId == "fieldgear_verdant_" + monster.id.Substring("verdant_".Length));
                        var equipment = reward == null ? null : ItemCatalog.Find(reward.itemId);
                        Require(reward != null && reward.quantity == 1 && equipment != null &&
                                equipment.category == "equipment" && equipment.maxStack == 1,
                            "Every Verdant species must award its own unique equipment: " + monster.id);

                        var matched = QuestProgressService.RecordObjectives(run, questCatalog, "defeat",
                            monster.id, 1, out var completions);
                        var finalObjective = objectiveIndex == quest.objectives.Count - 1;
                        Require(matched && (finalObjective
                                    ? completions.Exists(done => done.id == quest.id) &&
                                      run.completedQuestIds.Contains(quest.id) && !QuestProgressService.IsActive(run, quest.id)
                                    : !completions.Exists(done => done.id == quest.id) &&
                                      !run.completedQuestIds.Contains(quest.id) && QuestProgressService.IsActive(run, quest.id)),
                            "A Verdant case must remain active until every distinct creature is defeated: " + quest.id);
                        checkedObjectives++;
                    }

                    foreach (var reward in quest.reward.items)
                    {
                        var equipment = ItemCatalog.Find(reward.itemId);
                        InventoryService.Add(run, reward.itemId, reward.quantity);
                        Require(equipment != null && InventoryService.TryEquip(run, reward.itemId),
                            "A completed Verdant case must grant usable equipment: " + quest.id);
                    }
                    checkedQuests++;
                }

                var finalRecord = codexCatalog.entries.Find(record =>
                    record != null && record.id == "verdant_codex_" + chain[0].id.Substring("side_verdant_".Length, 2));
                Require(finalRecord != null && finalRecord.unlockQuestId == chain[chain.Count - 1].id &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(record => record.id == finalRecord.id),
                    "Finishing a region's Verdant chain must reveal its separate ecological study: " + entry.Key);
            }

            Require(checkedQuests == 22 && checkedObjectives == 54,
                "The validator must simulate all twenty-two chained field cases and fifty-four species objectives.");
        }

        private static void ValidateCrawlCreatureContracts(QuestCatalogData questCatalog, CodexCatalogData codexCatalog,
            DialogueCatalogData dialogueCatalog, MonsterCatalogData monsterCatalog,
            EncounterCatalogData encounterCatalog)
        {
            var species = monsterCatalog.entries.FindAll(monster =>
                monster != null && monster.id.StartsWith("crawl_", System.StringComparison.Ordinal));
            var resources = new HashSet<string>();
            foreach (var monster in species) resources.Add(monster.spriteResource);
            Require(species.Count == 55 && resources.Count == 55 &&
                    species.TrueForAll(monster => monster.rank == "common" && monster.spritePixelsPerUnit == 32),
                "The Crawl expansion must use fifty-five distinct common 32-pixel monster sprites.");

            var chains = new Dictionary<string, List<QuestDefinition>>();
            foreach (var quest in questCatalog.entries)
            {
                if (quest == null || quest.type != "side" ||
                    !quest.id.StartsWith("side_crawl_", System.StringComparison.Ordinal)) continue;
                if (!chains.TryGetValue(quest.locationId, out var chain))
                {
                    chain = new List<QuestDefinition>();
                    chains.Add(quest.locationId, chain);
                }
                chain.Add(quest);
            }

            Require(chains.Count == 11,
                "The Crawl expansion must extend the eleven existing maps without adding disconnected locations.");
            var checkedQuests = 0;
            var checkedObjectives = 0;
            foreach (var entry in chains)
            {
                var chain = entry.Value;
                chain.Sort((left, right) => string.CompareOrdinal(left.id, right.id));
                Require(chain.Count == 2 && chain[0].prerequisiteIds != null &&
                        chain[0].prerequisiteIds.Count == 1 && chain[1].prerequisiteIds != null &&
                        chain[1].prerequisiteIds.Count == 1 && chain[1].prerequisiteIds[0] == chain[0].id,
                    "Every map must receive two sequential Crawl field cases: " + entry.Key);

                var code = chain[0].id.Substring("side_crawl_".Length, 2);
                var run = new GameSaveData
                {
                    locationId = entry.Key,
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string>(chain[0].prerequisiteIds),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    inventory = new List<InventoryStackData>()
                };

                for (var questIndex = 0; questIndex < chain.Count; questIndex++)
                {
                    var quest = chain[questIndex];
                    var expectedObjectives = questIndex == 0 ? 3 : 2;
                    Require(quest.objectives != null && quest.objectives.Count == expectedObjectives &&
                            quest.reward?.items != null && quest.reward.items.Count == expectedObjectives &&
                            QuestProgressService.GetAvailableSideQuests(run, questCatalog, run.locationId)
                                .Exists(available => available.id == quest.id) &&
                            QuestProgressService.TryAcceptSideQuest(run, questCatalog, quest.id, quest.locationId),
                        "Each Crawl case must open in sequence and reward its distinct objectives: " + quest.id);

                    var encounters = encounterCatalog.entries.FindAll(candidate =>
                        candidate != null && candidate.requiredQuestId == quest.id);
                    var seenTargets = new HashSet<string>();
                    Require(encounters.Count == quest.objectives.Count,
                        "Each Crawl objective must resolve to one local encounter: " + quest.id);

                    for (var objectiveIndex = 0; objectiveIndex < quest.objectives.Count; objectiveIndex++)
                    {
                        var objective = quest.objectives[objectiveIndex];
                        var monster = MonsterCatalogService.FindById(monsterCatalog, objective.targetId);
                        var encounter = encounters.Find(candidate => candidate.monsterId == objective.targetId);
                        var texture = monster == null ? null : Resources.Load<Texture2D>("Art/" + monster.spriteResource);
                        var importer = monster == null ? null : AssetImporter.GetAtPath(
                            "Assets/Resources/Art/" + monster.spriteResource + ".png") as TextureImporter;
                        Require(objective.kind == "defeat" && objective.requiredCount == 1 &&
                                seenTargets.Add(objective.targetId) && monster != null &&
                                monster.id.StartsWith("crawl_", System.StringComparison.Ordinal) &&
                                monster.rank == "common" && monster.spritePixelsPerUnit == 32 &&
                                texture != null && texture.width == 32 && texture.height == 32 &&
                                importer != null && importer.filterMode == FilterMode.Point &&
                                !importer.mipmapEnabled &&
                                importer.textureCompression == TextureImporterCompression.Uncompressed &&
                                encounter != null && encounter.locationId == quest.locationId &&
                                encounter.defeatObjectiveTargetId == monster.id && encounter.contributesToQuest &&
                                DialogueCatalogService.Find(dialogueCatalog, encounter.defeatDialogueId)?.lines.Count == 2 &&
                                DialogueCatalogService.Find(dialogueCatalog, encounter.downDialogueId) != null,
                            "Each Crawl target must resolve to a crisp source sprite, field encounter and authored response: " + objective.targetId);

                        var itemId = "fieldgear_crawl_" + monster.id.Substring("crawl_".Length);
                        var reward = quest.reward.items.Find(item => item != null && item.itemId == itemId);
                        var equipment = reward == null ? null : ItemCatalog.Find(reward.itemId);
                        Require(reward != null && reward.quantity == 1 && equipment != null &&
                                equipment.category == "equipment" && equipment.maxStack == 1,
                            "Each Crawl species must grant its unique equipment reward: " + monster.id);

                        var matched = QuestProgressService.RecordObjectives(run, questCatalog, "defeat",
                            monster.id, 1, out var completions);
                        var finalObjective = objectiveIndex == quest.objectives.Count - 1;
                        Require(matched && (finalObjective
                                    ? completions.Exists(done => done.id == quest.id) &&
                                      run.completedQuestIds.Contains(quest.id) && !QuestProgressService.IsActive(run, quest.id)
                                    : !completions.Exists(done => done.id == quest.id) &&
                                      !run.completedQuestIds.Contains(quest.id) && QuestProgressService.IsActive(run, quest.id)),
                            "A Crawl case must remain active until every distinct target is defeated: " + quest.id);
                        checkedObjectives++;
                    }

                    foreach (var reward in quest.reward.items)
                    {
                        var equipment = ItemCatalog.Find(reward.itemId);
                        InventoryService.Add(run, reward.itemId, reward.quantity);
                        Require(equipment != null && InventoryService.TryEquip(run, reward.itemId),
                            "A completed Crawl case must grant equippable species rewards: " + quest.id);
                    }
                    checkedQuests++;
                }

                var record = codexCatalog.entries.Find(candidate =>
                    candidate != null && candidate.id == "crawl_codex_" + code);
                Require(record != null && record.unlockQuestId == chain[chain.Count - 1].id &&
                        CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(item => item.id == record.id),
                    "Finishing both regional Crawl cases must unlock the corresponding field study: " + entry.Key);
            }

            Require(checkedQuests == 22 && checkedObjectives == 55,
                "The validator must simulate all twenty-two Crawl field cases and fifty-five species objectives.");
        }

        private static void ValidateChoirUnboundIndexLine(QuestCatalogData catalog, CodexCatalogData codexCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "choir_beneath_lake",
                inventory = new List<InventoryStackData>(),
                activeSideQuestIds = new List<string>(),
                completedQuestIds = new List<string> { "choir_reckoning" },
                questObjectiveProgress = new List<QuestObjectiveProgressData>()
            };
            var marginQuest = QuestCatalogService.FindById(catalog, "side_choir_unclaimed_margin");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, marginQuest.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "choir_unnumbered_chime", 1,
                        out var completions) && completions.Exists(quest => quest.id == marginQuest.id) &&
                    run.completedQuestIds.Contains(marginQuest.id),
                "Inspecting the First Oath Bell rubbing must finish the first Choir margin quest.");

            var resonanceQuest = QuestCatalogService.FindById(catalog, "side_choir_resonance_map");
            Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId).Exists(
                        quest => quest.id == resonanceQuest.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, resonanceQuest.id, run.locationId),
                "The resonance quest must unlock only after the unnumbered chime has been inspected.");
            InventoryService.Add(run, "whisper_koi", 1);
            Require(QuestProgressService.RecordObjectives(run, catalog, "fish", "whisper_koi", 1,
                        out completions) && !completions.Exists(quest => quest.id == resonanceQuest.id) &&
                    QuestProgressService.IsActive(run, resonanceQuest.id),
                "Catching the Whisper Koi must leave the side quest active until its archive note is compared.");
            Require(QuestProgressService.RecordObjectives(run, catalog, "inspect", "choir_voice_margin", 1,
                        out completions) && completions.Exists(quest => quest.id == resonanceQuest.id) &&
                    run.completedQuestIds.Contains(resonanceQuest.id),
                "The marginal note and the fish recording must both be required by the resonance quest.");

            var indexQuest = QuestCatalogService.FindById(catalog, "side_choir_unbound_index");
            Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId).Exists(
                        quest => quest.id == indexQuest.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, indexQuest.id, run.locationId),
                "The crafting quest must unlock after the two Choir records are compared.");
            InventoryService.Add(run, "echo_kelp", 1);
            var recipeCatalog = RecipeCatalogService.Load();
            Require(CraftingService.TryCraft(run, recipeCatalog, "craft_unbound_voice_index",
                        "choir_archive_loom", out var indexRecipe, out _) &&
                    indexRecipe.outputItemId == "unbound_voice_index" &&
                    InventoryService.Count(run, "unbound_voice_index") == 1 &&
                    QuestProgressService.RecordObjectives(run, catalog, "craft", "unbound_voice_index", 1,
                        out completions) && completions.Exists(quest => quest.id == indexQuest.id) &&
                    run.completedQuestIds.Contains(indexQuest.id),
                "The Choir Archive Loom must craft the quest index from repeatable local materials and finish its quest.");

            var charmReward = indexQuest.reward?.items?.Find(reward => reward.itemId == "open_margin_charm");
            Require(charmReward != null && InventoryService.Add(run, charmReward.itemId, charmReward.quantity) == 1 &&
                    InventoryService.TryEquip(run, "open_margin_charm") &&
                    InventoryService.AttackBonus(run) == 1 && InventoryService.GuardBonus(run) == 2 &&
                    CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(
                        record => record.id == "choir_unbound_voice_index"),
                "Finishing the Choir line must grant an equippable charm and unlock its own field record.");
        }

        private static void ValidateChoirConsentArchiveLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var sharedRouteIds = new[]
            {
                "side_choir_diver_arrival", "side_choir_diver_slate", "side_choir_lyra_protocol",
                "side_choir_echo_sample", "side_choir_warden_testimony", "side_choir_archive_interval",
                "side_choir_mara_interview", "side_choir_listening_rules"
            };
            var allRouteIds = new List<string>(sharedRouteIds)
            {
                "side_choir_voice_consent", "side_choir_shared_copy", "side_choir_private_copy",
                "side_choir_diver_closure", "side_choir_playback_log", "side_choir_lyra_afterword"
            };

            foreach (var route in new[] { "share", "defer" })
            {
                var run = new GameSaveData
                {
                    locationId = "choir_beneath_lake",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "choir_reckoning" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };

                foreach (var questId in sharedRouteIds)
                    CompleteChoirConsentSideQuest(run, catalog, questId);

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_choir_voice_consent");
                var choice = choiceQuest?.choices?.Find(candidate => candidate.flagValue == route);
                Require(choiceQuest != null && choice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The Choir consent table must offer both storage choices after the listening agreement.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice", "choir_voice_consultation", 1,
                            out var choiceCompletions) && choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "Selecting a Choir storage procedure must finish the choice objective and save its flag.");
                foreach (var completed in choiceCompletions) ApplyValidationReward(run, completed.reward);
                ApplyValidationReward(run, choice.reward);

                var selectedId = route == "share" ? "side_choir_shared_copy" : "side_choir_private_copy";
                var rejectedId = route == "share" ? "side_choir_private_copy" : "side_choir_shared_copy";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedId, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedId, run.locationId),
                    "The Choir consent flag must expose only its matching copy procedure.");
                CompleteChoirConsentSideQuest(run, catalog, selectedId);
                CompleteChoirConsentSideQuest(run, catalog, "side_choir_diver_closure");
                CompleteChoirConsentSideQuest(run, catalog, "side_choir_playback_log");
                CompleteChoirConsentSideQuest(run, catalog, "side_choir_lyra_afterword");

                var completedLineCount = 0;
                foreach (var questId in allRouteIds)
                    if (run.completedQuestIds.Contains(questId)) completedLineCount++;
                var selectedCodexId = route == "share" ? "choir_consent_limited_copy" :
                    "choir_sealed_personal_segment";
                var rejectedCodexId = route == "share" ? "choir_sealed_personal_segment" :
                    "choir_consent_limited_copy";
                var unlocked = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(completedLineCount == 13 && run.activeSideQuestIds.Count == 0 &&
                        QuestProgressService.GetStoryFlag(run, "choir_archive_consent") == route &&
                        run.completedQuestIds.Contains("side_choir_lyra_afterword") &&
                        unlocked.Exists(record => record.id == selectedCodexId) &&
                        unlocked.Exists(record => record.id == "choir_archive_keeper_afterword") &&
                        !unlocked.Exists(record => record.id == rejectedCodexId),
                    "Each Choir consent route must complete thirteen shared/selected quests, keep its flag and unlock only its own archive records.");
            }
        }

        private static void CompleteChoirConsentSideQuest(GameSaveData run, QuestCatalogData catalog, string questId)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The next Choir consent record must unlock and be accepted in sequence: " + questId + ".");
            var objectivesMatched = true;
            foreach (var objective in quest.objectives)
                objectivesMatched &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                    objective.targetId, objective.requiredCount, out var completions) &&
                    completions.Exists(completed => completed.id == questId);
            Require(objectivesMatched && run.completedQuestIds.Contains(questId),
                "Every Choir consent record must complete against its authored world event: " + questId + ".");
            ApplyValidationReward(run, quest.reward);
        }

        private static void ValidateDawnkeepBarracksSideQuestLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "dawnkeep_barracks",
                inventory = new List<InventoryStackData>(),
                activeSideQuestIds = new List<string>(),
                completedQuestIds = new List<string> { "order_cadet_oath" },
                questObjectiveProgress = new List<QuestObjectiveProgressData>()
            };
            var rollQuest = QuestCatalogService.FindById(catalog, "side_dawnkeep_morning_roll");
            Require(rollQuest != null &&
                    !QuestProgressService.CanAcceptSideQuest(run, catalog, rollQuest.id, "dawnkeep_outpost") &&
                    QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId).Exists(
                        quest => quest.id == rollQuest.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, rollQuest.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "barracks_morning_roll", 1,
                        out var completions) && completions.Exists(quest => quest.id == rollQuest.id) &&
                    run.completedQuestIds.Contains(rollQuest.id),
                "The Dawnkeep route must unlock after the cadet oath, accept in the barracks and record the morning roll.");

            var returnQuest = QuestCatalogService.FindById(catalog, "side_dawnkeep_returned_letters");
            Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId).Exists(
                        quest => quest.id == returnQuest.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, returnQuest.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "barracks_return_shelf", 1,
                        out completions) && completions.Exists(quest => quest.id == returnQuest.id) &&
                    run.completedQuestIds.Contains(returnQuest.id),
                "The returned-letter investigation must unlock after and follow the uncertain morning roll.");

            var reviewQuest = QuestCatalogService.FindById(catalog, "side_dawnkeep_roll_review");
            Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId).Exists(
                        quest => quest.id == reviewQuest.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, reviewQuest.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "talk", "nia_porter", 1,
                        out completions) && completions.Exists(quest => quest.id == reviewQuest.id) &&
                    run.completedQuestIds.Contains(reviewQuest.id),
                "Nia's evidence review must close the third quest only after both records have been compared.");

            var reward = reviewQuest.reward?.items?.Find(item => item.itemId == "dawnkeep_blank_pin");
            Require(reward != null && InventoryService.Add(run, reward.itemId, reward.quantity) == 1 &&
                    InventoryService.TryEquip(run, "dawnkeep_blank_pin") &&
                    InventoryService.AttackBonus(run) == 1 && InventoryService.GuardBonus(run) == 1 &&
                    CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(
                        entry => entry.id == "dawnkeep_return_roll"),
                "Completing the Dawnkeep records must award its charm and unlock the matching codex entry.");
        }

        private static void ValidateDawnkeepHouseholdDisclosureLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var sharedIds = new[]
            {
                "side_barracks_family_request", "side_barracks_envelope_inventory",
                "side_barracks_badge_pouch", "side_barracks_redaction_review",
                "side_barracks_return_window", "side_barracks_courier_note",
                "side_barracks_family_review"
            };
            var lineIds = new List<string>(sharedIds)
            {
                "side_barracks_copy_choice", "side_barracks_aggregate_copy", "side_barracks_sealed_packets",
                "side_barracks_scope_label", "side_barracks_access_log", "side_barracks_correction_slot",
                "side_barracks_copy_receipt", "side_barracks_nia_afterword"
            };

            foreach (var route in new[] { "aggregate", "defer" })
            {
                var run = new GameSaveData
                {
                    locationId = "dawnkeep_barracks",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "order_cadet_oath", "side_dawnkeep_roll_review" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                foreach (var questId in sharedIds)
                    CompleteBarracksHouseholdQuest(run, catalog, questId);

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_barracks_copy_choice");
                var choice = choiceQuest?.choices?.Find(candidate => candidate.flagValue == route);
                Require(choiceQuest != null && choice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The family copy table must offer both authored storage procedures after the private review.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice", "dawnkeep_copy_consent", 1,
                            out var choiceCompletions) && choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "The family copy choice must save its scope and complete the choice objective.");
                foreach (var completed in choiceCompletions) ApplyValidationReward(run, completed.reward);
                ApplyValidationReward(run, choice.reward);

                var selectedId = route == "aggregate" ? "side_barracks_aggregate_copy" :
                    "side_barracks_sealed_packets";
                var rejectedId = route == "aggregate" ? "side_barracks_sealed_packets" :
                    "side_barracks_aggregate_copy";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedId, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedId, run.locationId),
                    "The Dawnkeep permission flag must expose only its matching copy route.");
                CompleteBarracksHouseholdQuest(run, catalog, selectedId);
                CompleteBarracksHouseholdQuest(run, catalog, "side_barracks_scope_label");
                CompleteBarracksHouseholdQuest(run, catalog, "side_barracks_access_log");
                CompleteBarracksHouseholdQuest(run, catalog, "side_barracks_correction_slot");
                CompleteBarracksHouseholdQuest(run, catalog, "side_barracks_copy_receipt");
                CompleteBarracksHouseholdQuest(run, catalog, "side_barracks_nia_afterword");

                var completedLineCount = 0;
                foreach (var questId in lineIds)
                    if (run.completedQuestIds.Contains(questId)) completedLineCount++;
                var selectedCodexId = route == "aggregate" ? "dawnkeep_aggregate_mail_sheet" :
                    "dawnkeep_sealed_family_packet";
                var rejectedCodexId = route == "aggregate" ? "dawnkeep_sealed_family_packet" :
                    "dawnkeep_aggregate_mail_sheet";
                var unlocked = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(completedLineCount == 14 && run.activeSideQuestIds.Count == 0 &&
                        QuestProgressService.GetStoryFlag(run, "barracks_copy_scope") == route &&
                        run.completedQuestIds.Contains("side_barracks_nia_afterword") &&
                        unlocked.Exists(record => record.id == selectedCodexId) &&
                        unlocked.Exists(record => record.id == "dawnkeep_open_margin_registry") &&
                        !unlocked.Exists(record => record.id == rejectedCodexId),
                    "Each Dawnkeep copy route must complete fourteen quests and unlock only its own disclosure records.");
            }
        }

        private static void CompleteBarracksHouseholdQuest(GameSaveData run, QuestCatalogData catalog,
            string questId)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The next Dawnkeep household record must unlock and be accepted in order: " + questId + ".");
            var objectivesMatched = true;
            foreach (var objective in quest.objectives)
                objectivesMatched &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                    objective.targetId, objective.requiredCount, out var completions) &&
                    completions.Exists(completed => completed.id == questId);
            Require(objectivesMatched && run.completedQuestIds.Contains(questId),
                "Every household record must complete against its authored event: " + questId + ".");
            ApplyValidationReward(run, quest.reward);
        }

        private static void ValidateDawnkeepWaterlineSideQuestLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog, RecipeCatalogData recipeCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "dawnkeep_outpost",
                inventory = new List<InventoryStackData>(),
                activeSideQuestIds = new List<string>(),
                completedQuestIds = new List<string> { "order_cadet_oath" },
                questObjectiveProgress = new List<QuestObjectiveProgressData>()
            };
            var opening = QuestCatalogService.FindById(catalog, "side_dawnkeep_waterline");
            Require(QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                        .Exists(quest => quest.id == opening.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, opening.id, run.locationId),
                "Nia's waterline survey must become available after the cadet oath in Dawnkeep.");

            var caughtFish = InventoryService.Add(run, "blackreed_trout", 1) == 1;
            Require(caughtFish && QuestProgressService.RecordObjectives(run, catalog, "talk", "nia_porter", 1,
                        out _) &&
                    QuestProgressService.RecordObjectives(run, catalog, "fish", "blackreed_trout", 1,
                        out var completed) && completed.Exists(quest => quest.id == opening.id) &&
                    run.completedQuestIds.Contains(opening.id),
                "The opening Dawnkeep quest must require both Nia's discussion and a caught lake fish.");
            Require(InventoryService.Add(run, "waterline_tin", 2) == 2,
                "Nia must provide enough old gauge metal for the later smithing task.");

            var inlet = QuestCatalogService.FindById(catalog, "side_dawnkeep_inlet_marks");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, inlet.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "dawnkeep_inlet_notches", 1,
                        out completed) && completed.Exists(quest => quest.id == inlet.id),
                "The inlet measurement must unlock only after the fish and first-record conversation.");

            var forge = QuestCatalogService.FindById(catalog, "side_dawnkeep_gauge");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, forge.id, run.locationId) &&
                    CraftingService.TryCraft(run, recipeCatalog, "forge_cadet_flow_charm", "dawnkeep_forge",
                        out var craftedRecipe, out _) && craftedRecipe.outputItemId == "cadet_flow_charm" &&
                    QuestProgressService.RecordObjectives(run, catalog, "craft", "cadet_flow_charm", 1,
                        out completed) && completed.Exists(quest => quest.id == forge.id),
                "Tomas's recipe must consume the granted gauge metal, produce the charm and complete its craft objective.");
            Require(InventoryService.TryEquip(run, "cadet_flow_charm") &&
                    InventoryService.AttackBonus(run) == 0 && InventoryService.GuardBonus(run) == 1,
                "The new crafted Dawnkeep charm must equip in the charm slot with its authored defense bonus.");

            var reading = QuestCatalogService.FindById(catalog, "side_dawnkeep_second_reading");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, reading.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "dawnkeep_lower_flow_post", 1,
                        out completed) && completed.Exists(quest => quest.id == reading.id),
                "The second physical waterline reading must follow the crafted gauge.");

            var report = QuestCatalogService.FindById(catalog, "side_dawnkeep_nia_report");
            Require(QuestProgressService.TryAcceptSideQuest(run, catalog, report.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "talk", "nia_porter", 1,
                        out completed) && completed.Exists(quest => quest.id == report.id) &&
                    run.completedQuestIds.Contains(report.id) &&
                    CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(
                        entry => entry.id == "dawnkeep_two_readings"),
                "Returning both measured readings must complete the line and unlock its codex record.");
        }

        private static void ValidateAshfallRemedyLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "ashfall_village",
                inventory = new List<InventoryStackData>(),
                activeSideQuestIds = new List<string>(),
                completedQuestIds = new List<string> { "side_ashfall_moonwort", "ashfall_shelter_report" },
                questObjectiveProgress = new List<QuestObjectiveProgressData>()
            };

            var ledger = QuestCatalogService.FindById(catalog, "side_ashfall_herb_ledger");
            Require(ledger != null &&
                    QuestProgressService.GetAvailableSideQuests(run, catalog, "dawnkeep_outpost")
                        .Exists(quest => quest.id == ledger.id) == false &&
                    QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                        .Exists(quest => quest.id == ledger.id) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, ledger.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "ashfall_herb_ledger", 1,
                        out var completed) && completed.Exists(quest => quest.id == ledger.id) &&
                    run.completedQuestIds.Contains(ledger.id),
                "Mira's herb record must unlock after the Ashfall report and start with its physical ledger inspection.");
            foreach (var reward in ledger.reward.items)
                Require(InventoryService.Add(run, reward.itemId, reward.quantity) == reward.quantity,
                    "The Ashfall field-notes reward must supply the next crop and enough fishing bait.");
            Require(InventoryService.Count(run, "moonwort_seed") == 1 &&
                    InventoryService.Count(run, "earthworm_bait") == 6,
                "The Ashfall remedy line must provide one repeat planting and six additional fishing attempts.");

            var replant = QuestCatalogService.FindById(catalog, "side_ashfall_replant_moonwort");
            FarmPlotDefinition moonwortPlot = null;
            if (farmCatalog?.entries != null)
                foreach (var plot in farmCatalog.entries)
                    if (plot != null && plot.cropId == "moonwort") moonwortPlot = plot;
            Require(replant != null && moonwortPlot != null &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, replant.id, run.locationId) &&
                    FarmPlotProgressService.TryPlant(run, moonwortPlot) &&
                    FarmPlotProgressService.Tick(run, moonwortPlot.growSeconds) &&
                    FarmPlotProgressService.TryHarvest(run, moonwortPlot) &&
                    InventoryService.Count(run, "moonwort_leaf") == moonwortPlot.harvestQuantity &&
                    QuestProgressService.RecordObjectives(run, catalog, "grow", "moonwort", 1,
                        out completed) && completed.Exists(quest => quest.id == replant.id),
                "The second Moonwort quest must be plantable from its reward and yield enough leaves for the authored recipe.");

            var fishQuest = QuestCatalogService.FindById(catalog, "side_ashfall_blackreed_record");
            FishingSpotDefinition dawnkeepLake = null;
            if (fishingCatalog?.entries != null)
                foreach (var spot in fishingCatalog.entries)
                    if (spot != null && spot.locationId == "dawnkeep_outpost" && spot.catches != null &&
                        spot.catches.Exists(catchEntry => catchEntry.itemId == "blackreed_trout"))
                        dawnkeepLake = spot;
            Require(fishQuest != null && dawnkeepLake != null &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, fishQuest.id, run.locationId),
                "The trout-record quest must be available from Ashfall and point to a lake that actually yields Blackreed Trout.");
            run.locationId = "dawnkeep_outpost";
            Require(FishingCatalogService.RollCatch(dawnkeepLake, 0.2f) == "blackreed_trout" &&
                    InventoryService.Add(run, "blackreed_trout", 1) == 1 &&
                    QuestProgressService.RecordObjectives(run, catalog, "fish", "blackreed_trout", 1,
                        out completed) && completed.Exists(quest => quest.id == fishQuest.id),
                "The weighted Dawnkeep fishing table must provide the line's fish and progress its accepted objective.");

            run.locationId = "ashfall_village";
            var brewQuest = QuestCatalogService.FindById(catalog, "side_ashfall_brew_moonlight");
            Require(brewQuest != null &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, brewQuest.id, run.locationId) &&
                    CraftingService.TryCraft(run, recipeCatalog, "brew_moonlight_tonic", "ashfall_herb_table",
                        out var brewedRecipe, out _) && brewedRecipe.outputItemId == "moonlight_tonic" &&
                    InventoryService.Count(run, "moonwort_leaf") == 0 &&
                    InventoryService.Count(run, "blackreed_trout") == 0 &&
                    QuestProgressService.RecordObjectives(run, catalog, "craft", "moonlight_tonic", 1,
                        out completed) && completed.Exists(quest => quest.id == brewQuest.id) &&
                    InventoryService.Count(run, "moonlight_tonic") == 1,
                "The tonic quest must consume its recorded harvest and fish at Mira's station, then complete on the actual crafted output.");

            var shelfQuest = QuestCatalogService.FindById(catalog, "side_ashfall_remedy_shelf");
            Require(shelfQuest != null &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, shelfQuest.id, run.locationId) &&
                    QuestProgressService.RecordObjectives(run, catalog, "inspect", "ashfall_remedy_shelf", 1,
                        out completed) && completed.Exists(quest => quest.id == shelfQuest.id) &&
                    run.completedQuestIds.Contains(shelfQuest.id),
                "The remedy shelf record must follow the completed tonic batch and close its own objective.");
            foreach (var reward in shelfQuest.reward.items)
                Require(InventoryService.Add(run, reward.itemId, reward.quantity) == reward.quantity,
                    "The final Ashfall remedy reward must resolve into the player's inventory.");
            Require(InventoryService.Count(run, "moonlight_tonic") == 2 &&
                    CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(
                        entry => entry.id == "ashfall_mira_dose_card"),
                "The finished remedy line must leave one tonic with Rowan and unlock Mira's dose card without making a cure claim.");
        }

        private static void ValidateCinderwellMeasureLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog)
        {
            var disclosureValues = new[] { "consented_households", "aggregate_only" };
            var branchQuestIds = new[] { "side_cinderwell_named_schedule", "side_cinderwell_aggregate_schedule" };
            var branchTargets = new[] { "cinderwell_named_schedule", "cinderwell_aggregate_schedule" };
            var codexIds = new[] { "cinderwell_named_ration_method", "cinderwell_aggregate_ration_method" };

            for (var route = 0; route < disclosureValues.Length; route++)
            {
                var run = new GameSaveData
                {
                    locationId = "cinderwell_basin",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "cinder_june_report" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                var questIds = new[]
                {
                    "side_cinderwell_measure_start", "side_cinderwell_cup_rail",
                    "side_cinderwell_valve_intervals", "side_cinderwell_seed_weights",
                    "side_cinderwell_record_choice", branchQuestIds[route]
                };
                var completedAllSteps = true;

                foreach (var questId in questIds)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    if (quest == null ||
                        !QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(available => available.id == questId) ||
                        !QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId))
                    {
                        completedAllSteps = false;
                        break;
                    }

                    if (quest.id == "side_cinderwell_record_choice")
                    {
                        var choiceId = route == 0 ? "household_rows" : "daily_totals";
                        var choice = QuestCatalogService.FindChoice(quest, choiceId);
                        if (choice == null || choice.flagValue != disclosureValues[route])
                        {
                            completedAllSteps = false;
                            break;
                        }
                        QuestProgressService.SetStoryFlag(run, quest.choiceFlag, choice.flagValue);
                    }
                    else if (!string.IsNullOrEmpty(quest.branchFlag))
                    {
                        QuestProgressService.SetStoryFlag(run, quest.branchFlag, quest.branchValue);
                    }

                    var matchedEveryObjective = true;
                    List<QuestDefinition> completed = null;
                    foreach (var objective in quest.objectives)
                        matchedEveryObjective &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                            objective.targetId, objective.requiredCount, out completed);
                    if (!matchedEveryObjective || completed == null ||
                        !completed.Exists(entry => entry.id == questId) || !run.completedQuestIds.Contains(questId))
                    {
                        completedAllSteps = false;
                        break;
                    }
                }

                var expectedBranchQuest = QuestCatalogService.FindById(catalog, branchQuestIds[route]);
                var unavailableBranchQuest = QuestCatalogService.FindById(catalog, branchQuestIds[1 - route]);
                Require(completedAllSteps && run.completedQuestIds.Contains(expectedBranchQuest.id) &&
                        !QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(available => available.id == unavailableBranchQuest.id),
                    "Cinderwell's measurement chain must preserve its choice and make only the matching public-board task available.");

                var unlockedRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(unlockedRecords.Exists(entry => entry.id == codexIds[route]) &&
                        !unlockedRecords.Exists(entry => entry.id == codexIds[1 - route]),
                    "Each Cinderwell disclosure route must unlock its own record without unlocking the other route's account.");

                var rewardMaterial = expectedBranchQuest.reward.items.Find(item => item.itemId == "cinder_measure_ring");
                Require(rewardMaterial != null && InventoryService.Add(run, rewardMaterial.itemId, rewardMaterial.quantity) == 1 &&
                        InventoryService.Add(run, "dryglass_shard", 2) == 2 &&
                        CraftingService.TryCraft(run, recipeCatalog, "forge_cistern_ledger_clasp", "dawnkeep_forge",
                            out var crafted, out _) && crafted.outputItemId == "cistern_ledger_clasp" &&
                        InventoryService.TryEquip(run, "cistern_ledger_clasp") &&
                        InventoryService.AttackBonus(run) == 0 && InventoryService.GuardBonus(run) == 1,
                    "Either Cinderwell disclosure route must reward material that can craft and equip the ledger clasp.");
            }
        }

        private static void ValidateCinderwellSaltlineRoutes(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog)
        {
            var branchIds = new[] { "side_cinderwell_paired_beds", "side_cinderwell_sheltered_tray" };
            var branchValues = new[] { "paired_soil", "sheltered_repeat" };
            var branchTargets = new[] { "cinderwell_paired_bed_board", "cinderwell_sheltered_tray_cabinet" };
            var branchCodexIds = new[] { "cinderwell_paired_beds_result", "cinderwell_sheltered_repeat_result" };
            var commonBeforeChoice = new[]
            {
                "side_cinderwell_saltline_request", "side_cinderwell_seed_wrap", "side_cinderwell_first_bloom",
                "side_cinderwell_june_trays", "side_cinderwell_salt_edge", "side_cinderwell_dawnkeep_baseline",
                "side_cinderwell_talia_baseline", "side_cinderwell_wick_craft", "side_cinderwell_wick_reading",
                "side_cinderwell_second_bloom", "side_cinderwell_tray_record", "side_cinderwell_oren_timing",
                "side_cinderwell_repeat_mark", "side_cinderwell_saltline_choice"
            };
            FarmPlotDefinition saffronPlot = null;
            foreach (var plot in farmCatalog?.entries ?? new List<FarmPlotDefinition>())
                if (plot != null && plot.locationId == "cinderwell_basin" && plot.cropId == "salt_saffron")
                    saffronPlot = plot;

            FishingSpotDefinition sourceLake = null;
            foreach (var spot in fishingCatalog?.entries ?? new List<FishingSpotDefinition>())
                if (spot != null && spot.locationId == "dawnkeep_outpost" && spot.catches != null &&
                    spot.catches.Exists(catchEntry => catchEntry.itemId == "blackreed_trout"))
                    sourceLake = spot;

            Require(CountQuestArc(catalog, "crown_of_empty_fields", "side") >= 82 && saffronPlot != null &&
                    sourceLake != null &&
                    RecipeCatalogService.FindById(recipeCatalog, "brew_cinderwell_brine_wick")?.stationId ==
                    "cinderwell_assay_bench" && ItemCatalog.Find("cinderwell_brine_wick")?.category == "material" &&
                    ItemCatalog.Find("fieldgear_cinderwell_paired_plot_charm")?.equipmentSlot == "charm" &&
                    ItemCatalog.Find("fieldgear_cinderwell_sheltered_seed_charm")?.equipmentSlot == "charm",
                "The Cinderwell saltline route must have its field plot, real upstream fishing table, local assay recipe and two distinct charm rewards.");

            for (var route = 0; route < branchIds.Length; route++)
            {
                var run = new GameSaveData
                {
                    locationId = "cinderwell_basin",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "cinder_june_report" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };
                var completedSteps = true;

                foreach (var questId in commonBeforeChoice)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    if (quest == null)
                    {
                        completedSteps = false;
                        break;
                    }
                    run.locationId = quest.locationId;
                    if (!QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(available => available.id == questId) ||
                        !QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId))
                    {
                        completedSteps = false;
                        break;
                    }

                    if (questId == "side_cinderwell_first_bloom" || questId == "side_cinderwell_second_bloom")
                    {
                        if (!FarmPlotProgressService.TryPlant(run, saffronPlot) ||
                            !FarmPlotProgressService.Tick(run, saffronPlot.growSeconds) ||
                            !FarmPlotProgressService.TryHarvest(run, saffronPlot))
                        {
                            completedSteps = false;
                            break;
                        }
                    }
                    else if (questId == "side_cinderwell_dawnkeep_baseline")
                    {
                        var catchId = FishingCatalogService.RollCatch(sourceLake, 0.1f);
                        if (catchId != "blackreed_trout" || InventoryService.Add(run, catchId, 1) != 1)
                        {
                            completedSteps = false;
                            break;
                        }
                    }
                    else if (questId == "side_cinderwell_wick_craft")
                    {
                        if (!CraftingService.TryCraft(run, recipeCatalog, "brew_cinderwell_brine_wick",
                                "cinderwell_assay_bench", out var crafted, out _) ||
                            crafted.outputItemId != "cinderwell_brine_wick")
                        {
                            completedSteps = false;
                            break;
                        }
                    }
                    else if (questId == "side_cinderwell_saltline_choice")
                    {
                        var choiceId = route == 0 ? "paired_beds" : "sheltered_repeat";
                        var choice = QuestCatalogService.FindChoice(quest, choiceId);
                        if (choice == null || choice.flagValue != branchValues[route])
                        {
                            completedSteps = false;
                            break;
                        }
                        QuestProgressService.SetStoryFlag(run, quest.choiceFlag, choice.flagValue);
                        ApplyValidationReward(run, choice.reward);
                    }

                    var matchedAllObjectives = true;
                    List<QuestDefinition> completed = null;
                    foreach (var objective in quest.objectives)
                    {
                        matchedAllObjectives &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                            objective.targetId, objective.requiredCount, out completed);
                    }
                    if (!matchedAllObjectives || completed == null ||
                        !completed.Exists(entry => entry.id == questId) || !run.completedQuestIds.Contains(questId))
                    {
                        completedSteps = false;
                        break;
                    }
                    foreach (var entry in completed) ApplyValidationReward(run, entry.reward);
                }

                var selectedBranch = QuestCatalogService.FindById(catalog, branchIds[route]);
                var otherBranch = QuestCatalogService.FindById(catalog, branchIds[1 - route]);
                Require(completedSteps && selectedBranch != null && otherBranch != null &&
                        QuestProgressService.GetAvailableSideQuests(run, catalog, "cinderwell_basin")
                            .Exists(available => available.id == selectedBranch.id) &&
                        !QuestProgressService.GetAvailableSideQuests(run, catalog, "cinderwell_basin")
                            .Exists(available => available.id == otherBranch.id),
                    "The saltline route must complete farming, upstream fishing, alchemy and its choice before exposing only the selected experiment.");

                List<QuestDefinition> branchCompletions = null;
                var branchCompleted = QuestProgressService.TryAcceptSideQuest(run, catalog, selectedBranch.id,
                                        run.locationId) &&
                                      QuestProgressService.RecordObjectives(run, catalog, "inspect",
                                          branchTargets[route], 1, out branchCompletions) &&
                                      branchCompletions.Exists(entry => entry.id == selectedBranch.id);
                Require(branchCompleted,
                    "Each saltline choice must accept and finish only its corresponding field notebook objective.");
                foreach (var entry in branchCompletions ?? new List<QuestDefinition>())
                    ApplyValidationReward(run, entry.reward);

                var branchCodex = CodexCatalogService.GetUnlocked(codexCatalog, run);
                var branchRewardId = selectedBranch.reward.items[0].itemId;
                Require(branchCodex.Exists(entry => entry.id == branchCodexIds[route]) &&
                        !branchCodex.Exists(entry => entry.id == branchCodexIds[1 - route]) &&
                        InventoryService.TryEquip(run, branchRewardId) &&
                        (route == 0 ? InventoryService.AttackBonus(run) == 1 && InventoryService.GuardBonus(run) == 1
                            : InventoryService.AttackBonus(run) == 0 && InventoryService.GuardBonus(run) == 2),
                    "The chosen trial must reveal its own record and grant a usable charm with the selected route's stats.");

                var review = QuestCatalogService.FindById(catalog, "side_cinderwell_saltline_review");
                var protocol = QuestCatalogService.FindById(catalog, "side_cinderwell_protocol_copy");
                var close = QuestCatalogService.FindById(catalog, "side_cinderwell_june_close");
                foreach (var quest in new[] { review, protocol, close })
                {
                    if (quest == null || !QuestProgressService.GetAvailableSideQuests(run, catalog, quest.locationId)
                            .Exists(available => available.id == quest.id) ||
                        !QuestProgressService.TryAcceptSideQuest(run, catalog, quest.id, quest.locationId))
                    {
                        completedSteps = false;
                        break;
                    }
                    List<QuestDefinition> completions = null;
                    var objectiveMatched = true;
                    foreach (var objective in quest.objectives)
                        objectiveMatched &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                            objective.targetId, objective.requiredCount, out completions);
                    if (!objectiveMatched || completions == null ||
                        !completions.Exists(entry => entry.id == quest.id))
                    {
                        completedSteps = false;
                        break;
                    }
                    foreach (var entry in completions) ApplyValidationReward(run, entry.reward);
                }

                var finalRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(completedSteps && run.completedQuestIds.Contains(close.id) &&
                        finalRecords.Exists(entry => entry.id == "cinderwell_saltline_limits") &&
                        finalRecords.Exists(entry => entry.id == branchCodexIds[route]) &&
                        !finalRecords.Exists(entry => entry.id == branchCodexIds[1 - route]),
                    "Either experiment must rejoin Oren's review, protocol copy and June's closeout, unlocking the shared method and only its own outcome.");
            }
        }

        private static void ValidateJuneStonepotKitchenLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog)
        {
            var plot = farmCatalog?.entries?.Find(entry => entry != null && entry.id == "cinderwell_barley_bed");
            var spot = fishingCatalog?.entries?.Find(entry => entry != null && entry.id == "cinderwell_warm_run");
            var recipe = RecipeCatalogService.FindById(recipeCatalog, "cook_cinderwell_stonepot_broth");
            var encounter = EncounterCatalogService.FindById(encounterCatalog, "june_pantry_cinderwell_muck");
            var monster = MonsterCatalogService.FindById(monsterCatalog, encounter?.monsterId);
            Require(plot?.cropId == "cinderwell_barley" && plot.locationId == "cinderwell_basin" &&
                    spot?.locationId == "cinderwell_basin" && spot.baitItemId == "earthworm_bait" &&
                    FishingCatalogService.RollCatch(spot, 0.2f) == "emberscale_perch" &&
                    recipe?.stationId == "cinderwell_kitchen" && recipe.discipline == "cooking" &&
                    recipe.outputItemId == "cinderwell_stonepot_broth" && recipe.outputQuantity == 2 &&
                    encounter?.requiredQuestId == "side_june_pantry_pantry" && monster != null &&
                    InventoryService.HealAmount("cinderwell_stonepot_broth") == 36,
                "June's field kitchen must connect a local crop, baited catch, gated pantry encounter and two-serving cooking recipe.");

            var commonQuestIds = new[]
            {
                "side_june_pantry_open", "side_june_pantry_hearth", "side_june_pantry_pantry",
                "side_june_pantry_draft", "side_june_pantry_oren", "side_june_pantry_grow",
                "side_june_pantry_fish", "side_june_pantry_grindstone", "side_june_pantry_cook",
                "side_june_pantry_sample", "side_june_pantry_choice"
            };
            var routeValues = new[] { "common_table", "road_crew" };
            var branchQuestIds = new[]
            {
                new[] { "side_june_pantry_table", "side_june_pantry_table_report" },
                new[] { "side_june_pantry_departure", "side_june_pantry_departure_report" }
            };
            var charmIds = new[] { "june_hearth_shift_button", "june_travel_ladle_charm" };

            for (var route = 0; route < routeValues.Length; route++)
            {
                var run = new GameSaveData
                {
                    locationId = "cinderwell_basin",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "cinder_june_report" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                var pantryProgress = EncounterProgressService.GetOrCreate(run, encounter, monster);
                Require(pantryProgress != null && !pantryProgress.defeated,
                    "June's pantry creature must use persistent regional encounter progress.");
                pantryProgress.health = 0;
                pantryProgress.defeated = true;

                foreach (var questId in commonQuestIds)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    Require(quest != null && quest.locationId == "cinderwell_basin",
                        "Every June kitchen objective must resolve to a local side quest: " + questId);
                    run.locationId = quest.locationId;
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, questId == "side_june_pantry_choice" ? routeValues[route] : "");
                }

                var choice = QuestCatalogService.FindById(catalog, "side_june_pantry_choice");
                Require(QuestProgressService.GetStoryFlag(run, choice.choiceFlag) == routeValues[route] &&
                        InventoryService.Count(run, charmIds[route]) == 1 &&
                        InventoryService.Count(run, charmIds[1 - route]) == 0 &&
                        InventoryService.TryEquip(run, charmIds[route]),
                    "June's first-bowl choice must unlock only its matching service route and equippable charm.");

                foreach (var questId in branchQuestIds[route])
                {
                    run.locationId = "cinderwell_basin";
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");
                }
                Require(InventoryService.Count(run, "cinderwell_stonepot_broth") == 1 &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, "side_june_pantry_afterword",
                            "cinderwell_basin"),
                    "Serving the first bowl must consume one meal and retain Rowan's second restorative bowl.");

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    "side_june_pantry_afterword", "");
                var records = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, "side_june_pantry_afterword") &&
                        records.Exists(entry => entry.id == "june_stonepot_afterword_record") &&
                        InventoryService.Count(run, "cinderwell_stonepot_broth") == 1,
                    "Either meal-service outcome must survive save/resume, open the shared codex and retain one usable bowl.");
            }
        }

        private static void ValidateOrenSeedTinRoute(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog)
        {
            var allRouteQuestCount = 0;
            foreach (var quest in catalog?.entries ?? new List<QuestDefinition>())
                if (quest != null && quest.id.StartsWith("side_oren_seed_tin_"))
                    allRouteQuestCount++;

            var plot = farmCatalog?.entries?.Find(entry => entry != null && entry.id == "cinderwell_barley_bed");
            var spot = fishingCatalog?.entries?.Find(entry => entry != null && entry.id == "cinderwell_warm_run");
            var recipe = RecipeCatalogService.FindById(recipeCatalog, "cook_oren_seedkeepers_cake");
            Require(allRouteQuestCount == 24 && plot?.cropId == "cinderwell_barley" &&
                    plot.seedItemId == "cinderwell_barley_seed" && plot.harvestItemId == "cinderwell_barley" &&
                    spot?.locationId == "cinderwell_basin" && spot.baitItemId == "earthworm_bait" &&
                    FishingCatalogService.RollCatch(spot, FindCatchRoll(spot, "emberscale_perch")) ==
                    "emberscale_perch" && recipe?.stationId == "cinderwell_kitchen" &&
                    recipe.discipline == "cooking" && recipe.outputItemId == "oren_seedkeepers_cake" &&
                    recipe.outputQuantity == 1 && InventoryService.HealAmount("oren_seedkeepers_cake") == 44,
                "Oren's seed-tin route must connect its twenty-four quest definitions to the real barley bed, Warm Run and cooking recipe.");

            var beforeChoiceQuestIds = new[]
            {
                "side_oren_seed_tin_open", "side_oren_seed_tin_hinge", "side_oren_seed_tin_paper",
                "side_oren_seed_tin_date_marks", "side_oren_seed_tin_june_memory",
                "side_oren_seed_tin_first_row", "side_oren_seed_tin_first_heads"
            };
            var afterBranchQuestIds = new[]
            {
                "side_oren_seed_tin_custody", "side_oren_seed_tin_perch", "side_oren_seed_tin_june_recipe",
                "side_oren_seed_tin_cook", "side_oren_seed_tin_cooling_rack", "side_oren_seed_tin_taste",
                "side_oren_seed_tin_second_packet", "side_oren_seed_tin_empty_tin",
                "side_oren_seed_tin_second_row", "side_oren_seed_tin_new_shoots",
                "side_oren_seed_tin_june_aftertaste", "side_oren_seed_tin_note_return",
                "side_oren_seed_tin_next_season", "side_oren_seed_tin_afterword"
            };
            var choiceQuestId = "side_oren_seed_tin_choice";
            var branchQuestIds = new[] { "side_oren_seed_tin_exchange", "side_oren_seed_tin_reserve" };
            var branchValues = new[] { "open_exchange", "winter_case" };
            var charmIds = new[] { "open_seed_loop_charm", "winter_tin_hook_charm" };
            var branchRecordIds = new[] { "oren_seed_tin_exchange_record", "oren_seed_tin_reserve_record" };
            var choiceQuest = QuestCatalogService.FindById(catalog, choiceQuestId);
            var afterwordQuestId = "side_oren_seed_tin_afterword";
            var afterwordRecordId = "oren_seed_tin_afterword_record";

            foreach (var route in new[] { 0, 1 })
            {
                var rejectedRoute = 1 - route;
                var run = new GameSaveData
                {
                    locationId = "cinderwell_basin",
                    completedQuestIds = new List<string> { "side_june_pantry_afterword" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>(),
                    inventory = new List<InventoryStackData>()
                };
                Require(InventoryService.Add(run, "earthworm_bait", 1) == 1,
                    "The kitchen fish objective must begin with one usable bait.");

                foreach (var questId in beforeChoiceQuestIds)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    choiceQuestId, branchValues[route]);
                Require(QuestProgressService.GetStoryFlag(run, choiceQuest.choiceFlag) == branchValues[route] &&
                        InventoryService.Count(run, charmIds[route]) == 1 &&
                        InventoryService.Count(run, charmIds[rejectedRoute]) == 0 &&
                        InventoryService.TryEquip(run, charmIds[route]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[route],
                            "cinderwell_basin") &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedRoute],
                            "cinderwell_basin"),
                    "Oren's packet choice must equip its own charm and unlock only the selected custody route.");

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    branchQuestIds[route], "");
                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(branchRecords.Exists(entry => entry.id == branchRecordIds[route]) &&
                        !branchRecords.Exists(entry => entry.id == branchRecordIds[rejectedRoute]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedRoute]),
                    "Oren's custody choice must unlock only the matching exchange or winter-case record.");

                foreach (var questId in afterBranchQuestIds)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                Require(InventoryService.Count(run, "oren_seedkeepers_cake") == 1 &&
                        QuestProgressService.IsCompleted(run, afterwordQuestId),
                    "Both Oren routes must grow a second row, craft the family recipe and reach the shared afterword.");
                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                var finalRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, afterwordQuestId) &&
                        QuestProgressService.GetStoryFlag(run, choiceQuest.choiceFlag) == branchValues[route] &&
                        finalRecords.Exists(entry => entry.id == branchRecordIds[route]) &&
                        !finalRecords.Exists(entry => entry.id == branchRecordIds[rejectedRoute]) &&
                        finalRecords.Exists(entry => entry.id == afterwordRecordId),
                    "Oren's selected seed-custody policy, branch archive and shared afterword must survive save/resume.");
            }
        }

        private static void ValidateAshfallCartRestorationLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            DialogueCatalogData dialogueCatalog, RecipeCatalogData recipeCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var questIds = new[]
            {
                "side_ashfall_cart_offer", "side_ashfall_cart_wheel", "side_ashfall_cart_medicine",
                "side_ashfall_cart_rut", "side_ashfall_cart_clear", "side_ashfall_cart_salvage",
                "side_ashfall_cart_measure", "side_ashfall_cart_tomas", "side_ashfall_cart_spokes",
                "side_ashfall_cart_forge", "side_ashfall_cart_return", "side_ashfall_cart_install",
                "side_ashfall_cart_test", "side_ashfall_cart_load", "side_ashfall_cart_policy",
                "side_ashfall_cart_communal_bay", "side_ashfall_cart_communal_turn",
                "side_ashfall_cart_communal_report", "side_ashfall_cart_household_kits",
                "side_ashfall_cart_household_test", "side_ashfall_cart_household_report",
                "side_ashfall_cart_afterword"
            };
            var landmarkIds = new[]
            {
                "ashfall_cart_wheel", "ashfall_cart_east_rut", "ashfall_cart_salvage",
                "ashfall_cart_test_lane", "ashfall_cart_shared_bay", "ashfall_cart_turning_arc",
                "ashfall_cart_kit_table", "ashfall_cart_household_load", "tomas_cart_dimensions",
                "dawnkeep_spare_spokes"
            };
            Require(questIds.Length == 22 && CountQuestArc(catalog, "ashes_of_ashfall", "side") == 113,
                "The Ashfall repair route must add a complete twenty-two quest side story to the first region.");
            foreach (var questId in questIds)
            {
                var quest = QuestCatalogService.FindById(catalog, questId);
                var objective = quest?.objectives?.Count == 1 ? quest.objectives[0] : null;
                var record = codexCatalog?.entries?.Find(entry => entry != null &&
                    entry.unlockQuestId == questId && entry.id == "ashfall_cart_" + questId.Substring("side_ashfall_cart_".Length) + "_record");
                Require(quest != null && quest.type == "side" && quest.arcId == "ashes_of_ashfall" &&
                        objective != null && DialogueCatalogService.Find(dialogueCatalog, objective.dialogueId) != null &&
                        record != null,
                    "Every Ashfall cart step must resolve to authored dialogue and a quest-locked field record: " + questId);
            }

            foreach (var landmarkId in landmarkIds)
                Require(landmarkCatalog?.entries?.Exists(entry => entry != null && entry.targetId == landmarkId) == true,
                    "The evacuation-cart route must place its physical landmark: " + landmarkId);

            var choiceQuest = QuestCatalogService.FindById(catalog, "side_ashfall_cart_policy");
            var sharedChoice = QuestCatalogService.FindChoice(choiceQuest, "shared_cart");
            var householdChoice = QuestCatalogService.FindChoice(choiceQuest, "household_kits");
            var sharedReport = QuestCatalogService.FindById(catalog, "side_ashfall_cart_communal_report");
            var householdReport = QuestCatalogService.FindById(catalog, "side_ashfall_cart_household_report");
            var afterword = QuestCatalogService.FindById(catalog, "side_ashfall_cart_afterword");
            var pinRecipe = RecipeCatalogService.FindById(recipeCatalog, "forge_ashfall_cart_axle_pin");
            var encounter = EncounterCatalogService.FindById(encounterCatalog, "ashfall_cart_road_goblin");
            var monster = MonsterCatalogService.FindById(monsterCatalog, encounter?.monsterId);
            Require(choiceQuest?.choiceFlag == "ashfall_cart_use" && sharedChoice?.flagValue == "shared" &&
                    householdChoice?.flagValue == "household" &&
                    sharedChoice.reward?.items?.Count == 1 &&
                    sharedChoice.reward.items[0].itemId == "ashfall_shared_cart_charm" &&
                    householdChoice.reward?.items?.Count == 1 &&
                    householdChoice.reward.items[0].itemId == "ashfall_household_repair_charm" &&
                    sharedReport?.branchValue == "shared" && householdReport?.branchValue == "household" &&
                    afterword?.prerequisiteGroups?.Exists(group => group != null && group.anyOfQuestIds != null &&
                        group.anyOfQuestIds.Contains(sharedReport.id) && group.anyOfQuestIds.Contains(householdReport.id)) == true,
                "The repair decision must expose two exclusive service routes that rejoin only after their own reports.");
            Require(pinRecipe?.stationId == "dawnkeep_forge" && pinRecipe.discipline == "smithing" &&
                    pinRecipe.outputItemId == "ashfall_cart_axle_pin" &&
                    pinRecipe.ingredients.Exists(entry => entry.itemId == "ashfall_cart_iron" && entry.quantity == 2) &&
                    pinRecipe.ingredients.Exists(entry => entry.itemId == "ashfall_cart_spoke" && entry.quantity == 1) &&
                    encounter?.requiredQuestId == "side_ashfall_cart_clear" && monster != null &&
                    monster.id == "tiny_af_ash_goblin" &&
                    ItemCatalog.Find("ashfall_shared_cart_charm")?.category == "equipment" &&
                    ItemCatalog.Find("ashfall_household_repair_charm")?.category == "equipment",
                "The route must gate its road encounter, riddle, repair recipe and equippable branch rewards to catalog assets.");

            var craftingRun = new GameSaveData { inventory = new List<InventoryStackData>() };
            InventoryService.Add(craftingRun, "ashfall_cart_iron", 2);
            InventoryService.Add(craftingRun, "ashfall_cart_spoke", 1);
            Require(!CraftingService.TryCraft(craftingRun, recipeCatalog, "forge_ashfall_cart_axle_pin",
                        "ashfall_herb_table", out _, out _) &&
                    InventoryService.Count(craftingRun, "ashfall_cart_iron") == 2 &&
                    CraftingService.TryCraft(craftingRun, recipeCatalog, "forge_ashfall_cart_axle_pin",
                        "dawnkeep_forge", out var craftedPin, out _) &&
                    craftedPin.outputItemId == "ashfall_cart_axle_pin" &&
                    InventoryService.Remove(craftingRun, "ashfall_cart_axle_pin", 1) &&
                    InventoryService.Count(craftingRun, "ashfall_cart_axle_pin") == 0,
                "A wrong forge must preserve the salvage, while the installed axle pin is crafted at Dawnkeep and consumed once.");

            var commonQuestIds = new[]
            {
                "side_ashfall_cart_offer", "side_ashfall_cart_wheel", "side_ashfall_cart_medicine",
                "side_ashfall_cart_rut", "side_ashfall_cart_clear", "side_ashfall_cart_salvage",
                "side_ashfall_cart_measure", "side_ashfall_cart_tomas", "side_ashfall_cart_spokes",
                "side_ashfall_cart_forge", "side_ashfall_cart_return", "side_ashfall_cart_install",
                "side_ashfall_cart_test", "side_ashfall_cart_load", "side_ashfall_cart_policy"
            };
            var routeValues = new[] { "shared", "household" };
            var branchQuestIds = new[]
            {
                new[] { "side_ashfall_cart_communal_bay", "side_ashfall_cart_communal_turn",
                        "side_ashfall_cart_communal_report" },
                new[] { "side_ashfall_cart_household_kits", "side_ashfall_cart_household_test",
                        "side_ashfall_cart_household_report" }
            };
            var routeCharmIds = new[] { "ashfall_shared_cart_charm", "ashfall_household_repair_charm" };
            var unchosenBranchIds = new[] { branchQuestIds[1], branchQuestIds[0] };
            for (var route = 0; route < routeValues.Length; route++)
            {
                var run = new GameSaveData
                {
                    locationId = "ashfall_village",
                    completedQuestIds = new List<string> { "side_ashfall_two_bells_choose" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>(),
                    inventory = new List<InventoryStackData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                foreach (var questId in commonQuestIds)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    run.locationId = quest.locationId;
                    if (questId == "side_ashfall_cart_policy")
                        QuestProgressService.SetStoryFlag(run, quest.choiceFlag, routeValues[route]);
                    CompleteAshfallCartRouteQuest(run, catalog, questId);
                }

                var selectedChoice = route == 0 ? sharedChoice : householdChoice;
                var charmId = routeCharmIds[route];
                Require(QuestProgressService.GetStoryFlag(run, choiceQuest.choiceFlag) == routeValues[route] &&
                        !QuestProgressService.IsActive(run, unchosenBranchIds[route][0]) &&
                        InventoryService.Add(run, selectedChoice.reward.items[0].itemId, 1) == 1 &&
                        InventoryService.TryEquip(run, charmId),
                    "The cart-use choice must activate one policy, leave the other route closed and grant usable equipment.");

                foreach (var questId in branchQuestIds[route])
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    run.locationId = quest.locationId;
                    CompleteAshfallCartRouteQuest(run, catalog, questId);
                }
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, "side_ashfall_cart_afterword",
                            "ashfall_village"),
                    "Either completed cart-use policy must unlock Gideon's shared afterword.");
                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                CompleteAshfallCartRouteQuest(run, catalog, "side_ashfall_cart_afterword");
                var records = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, "side_ashfall_cart_afterword") &&
                        QuestProgressService.IsCompleted(run, branchQuestIds[route][2]) &&
                        !QuestProgressService.IsCompleted(run, unchosenBranchIds[route][2]) &&
                        InventoryService.Count(run, charmId) == 1 &&
                        records.Exists(entry => entry.id == "ashfall_cart_afterword_record") &&
                        records.Exists(entry => entry.id == "ashfall_cart_" +
                            (route == 0 ? "communal_report" : "household_report") + "_record") &&
                        !records.Exists(entry => entry.id == "ashfall_cart_" +
                            (route == 0 ? "household_report" : "communal_report") + "_record"),
                    "The cart policy must survive save/resume and unlock only its branch record plus the shared afterword.");
            }
        }

        private static void CompleteAshfallCartRouteQuest(GameSaveData run, QuestCatalogData catalog, string questId)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            if (quest == null || !QuestProgressService.TryAcceptSideQuest(run, catalog, questId, quest.locationId))
                throw new System.InvalidOperationException("Ashfall cart route could not accept quest " + questId + ".");
            var objective = quest.objectives[0];
            Require(QuestProgressService.RecordObjectives(run, catalog, objective.kind, objective.targetId, 1,
                        out var completions) && completions.Exists(entry => entry.id == questId),
                "Ashfall cart route failed to complete objective for " + questId + ".");
        }

        private static void ValidateOuterwakeSignalReplyLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog)
        {
            var routeFlags = new[] { "bounded_echo", "listen_only" };
            var routeQuests = new[] { "side_outerwake_bounded_echo", "side_outerwake_listen_only" };
            var routeTargets = new[] { "outerwake_echo_receipt", "outerwake_passive_record" };
            var routeCodex = new[] { "outerwake_bounded_echo_protocol", "outerwake_passive_signal_record" };

            for (var route = 0; route < routeFlags.Length; route++)
            {
                var run = new GameSaveData
                {
                    locationId = "outerwake_archive",
                    inventory = new List<InventoryStackData>(),
                    activeSideQuestIds = new List<string>(),
                    completedQuestIds = new List<string> { "archive_return_report" },
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                var questIds = new[]
                {
                    "side_outerwake_repeat_signal", "side_outerwake_wind_clock", "side_outerwake_tide_record",
                    "side_outerwake_signal_phase", "side_outerwake_receiver_coil", "side_outerwake_reply_choice",
                    routeQuests[route]
                };
                var completedAllSteps = true;

                foreach (var questId in questIds)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    if (quest == null ||
                        !QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(available => available.id == questId) ||
                        !QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId))
                    {
                        completedAllSteps = false;
                        break;
                    }

                    if (quest.id == "side_outerwake_reply_choice")
                    {
                        var choice = QuestCatalogService.FindChoice(quest,
                            route == 0 ? "send_bounded_echo" : "listen_without_reply");
                        if (choice == null || choice.flagValue != routeFlags[route])
                        {
                            completedAllSteps = false;
                            break;
                        }
                        QuestProgressService.SetStoryFlag(run, quest.choiceFlag, choice.flagValue);
                    }
                    else if (!string.IsNullOrEmpty(quest.branchFlag))
                    {
                        QuestProgressService.SetStoryFlag(run, quest.branchFlag, quest.branchValue);
                    }

                    if (quest.id == "side_outerwake_tide_record")
                    {
                        InventoryService.Add(run, "farwake_carp", 1);
                        InventoryService.Add(run, "skyroot_sap", 1);
                    }
                    if (quest.id == "side_outerwake_receiver_coil")
                    {
                        InventoryService.Add(run, "astral_prism", 1);
                        if (!CraftingService.TryCraft(run, recipeCatalog, "forge_outerwake_receiver_coil",
                                "outerwake_forge", out var crafted, out _) ||
                            crafted.outputItemId != "outerwake_receiver_coil")
                        {
                            completedAllSteps = false;
                            break;
                        }
                    }

                    var matchedEveryObjective = true;
                    List<QuestDefinition> completed = null;
                    foreach (var objective in quest.objectives)
                        matchedEveryObjective &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                            objective.targetId, objective.requiredCount, out completed);
                    if (!matchedEveryObjective || completed == null ||
                        !completed.Exists(entry => entry.id == questId) || !run.completedQuestIds.Contains(questId))
                    {
                        completedAllSteps = false;
                        break;
                    }
                }

                var expectedRoute = QuestCatalogService.FindById(catalog, routeQuests[route]);
                var unchosenRoute = QuestCatalogService.FindById(catalog, routeQuests[1 - route]);
                Require(completedAllSteps && QuestProgressService.GetStoryFlag(run, "outerwake_reply") == routeFlags[route] &&
                        run.completedQuestIds.Contains(expectedRoute.id) &&
                        !QuestProgressService.GetAvailableSideQuests(run, catalog, run.locationId)
                            .Exists(available => available.id == unchosenRoute.id),
                    "The Outer-Wake choice must unlock only the selected signal handling route.");

                var unlockedRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(unlockedRecords.Exists(entry => entry.id == routeCodex[route]) &&
                        !unlockedRecords.Exists(entry => entry.id == routeCodex[1 - route]),
                    "Each Outer-Wake response choice must unlock its own record, not the alternate route's account.");

                var equipmentReward = expectedRoute.reward.items.Find(item => item.itemId == "outerwake_field_compass");
                Require(equipmentReward != null && InventoryService.Add(run, equipmentReward.itemId,
                            equipmentReward.quantity) == 1 &&
                        InventoryService.TryEquip(run, "outerwake_field_compass") &&
                        InventoryService.AttackBonus(run) == 1 && InventoryService.GuardBonus(run) == 1,
                    "Either completed reply route must award an equippable field compass with its authored stats.");
            }
        }

        private static void ValidateOuterwakeRoute(GameSaveData run, QuestCatalogData catalog, string choiceId,
            string testimony)
        {
            Require(!run.chapterComplete && QuestProgressService.IsActive(run, "archive_arrival"),
                "Either Hundredth Champion route must unlock Outer-Wake after the Greenwake star chart.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "evelyn_hart", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_briefing"),
                "Dr. Evelyn Hart must begin the Outer-Wake expedition briefing.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "jace_morrow", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "archive_broken_lens", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_rift_survey"),
                "The observatory lens survey must open the local rift investigation.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "rift_hound", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "rift_hound", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "star_leecher", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "star_leecher", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "archive_scribe", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_weather_records"),
                "Clearing the Outer-Wake threats must unlock the three weather records.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "archive_weather_north", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "archive_weather_south", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "archive_weather_buried", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_skyroot_lab"),
                "The three readings must lead into the Skyroot and Celestial Pool study.");
            QuestProgressService.RecordObjective(run, catalog, "grow", "skyroot", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "fish", "farwake_carp", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "craft", "astral_prism", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "interact", "archive_ring_north", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "interact", "archive_ring_south", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_asterion"),
                "Crafting the Astral Prism and aligning both anchors must reveal Asterion's threshold.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "asterion_threshold", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_far_silt", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_seed_imprint", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_evidence_choice"),
                "Asterion's remains and outer samples must unlock the testimony decision.");
            var choiceQuest = QuestProgressService.GetActiveQuest(run, catalog);
            var choice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
            Require(choice != null && choice.flagValue == testimony,
                "Each Outer-Wake testimony option must resolve to its authored persistent flag.");
            QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
            QuestProgressService.RecordObjective(run, catalog, "choice", "archive_evidence_choice", 1, out _);
            var branchId = testimony == "public" ? "archive_public_testimony" : "archive_private_testimony";
            var unchosenBranchId = testimony == "public" ? "archive_private_testimony" : "archive_public_testimony";
            var evidenceTarget = testimony == "public" ? "archive_public_beacon" : "archive_private_relay";
            Require(QuestProgressService.IsActive(run, branchId) &&
                    !QuestProgressService.IsActive(run, unchosenBranchId),
                "The evidence choice must activate one testimony route only.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", evidenceTarget, 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_world_will") &&
                    !run.completedQuestIds.Contains(unchosenBranchId),
                "Both testimony routes must independently open The World Will while preserving the unchosen route.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "world_will_outerwake", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "veilshard_drake", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_far_signal", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_signal_interval"),
                "The first Far-Wake reply must open a second-pass verification sequence before the expedition report.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_far_signal", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_wind_mast", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_tide_gauge", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "jace_morrow", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_passive_record", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "interact", "outerwake_reply_console", 1, out _);
            Require(QuestProgressService.IsActive(run, "archive_return_report"),
                "The report must remain locked until all six after-signal checks are complete.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "evelyn_hart", 1, out _);
            Require(!run.chapterComplete && run.completedQuestIds.Count == 94 &&
                    CountCompletedQuestType(run, catalog, "story") == 94 &&
                    QuestProgressService.IsActive(run, "last_oath_arrival") &&
                    run.storyFlags.Exists(flag => flag != null && flag.id == "archive_testimony" && flag.value == testimony) &&
                    !run.completedQuestIds.Contains(unchosenBranchId),
                "Both testimony routes must complete Arc 7 at 94 campaign story quests and unlock Arc 8 with the selected flag saved.");
        }

        private static void ValidateLastOathConsentArchive(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var rootQuestId = "side_last_oath_consent_audit";
            foreach (var route in new[] { "named", "sealed" })
            {
                var run = new GameSaveData
                {
                    locationId = "last_oath_reach",
                    completedQuestIds = new List<string> { "last_oath_arrival", "last_oath_records" }
                };
                QuestProgressService.Reconcile(run, catalog);
                Require(!QuestProgressService.CanAcceptSideQuest(run, catalog, rootQuestId, run.locationId),
                    "The consent archive must stay closed until the earlier roster, witness, directive and sword-mark records are checked.");
                run.completedQuestIds.AddRange(new[]
                {
                    "side_last_oath_names", "side_last_oath_witness", "side_last_oath_worldwill",
                    "side_last_oath_sword_mark"
                });
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.TryAcceptSideQuest(run, catalog, rootQuestId, run.locationId),
                    "Completing the four prerequisite records must open Alden's consent audit in Crownfall Reach.");

                foreach (var questId in new[]
                         {
                             rootQuestId, "side_last_oath_notice_dates", "side_last_oath_first_refusal",
                             "side_last_oath_emberroot_proof", "side_last_oath_starlit_sample",
                             "side_last_oath_signature_compare"
                         })
                {
                    if (questId != rootQuestId)
                        Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                            "Each completed consent-audit step must unlock the next regional record: " + questId);
                    CompleteLastOathConsentSideQuest(run, catalog, questId);
                }

                var choiceQuest = QuestCatalogService.FindById(catalog, "side_last_oath_consent_archive");
                var choiceId = route == "named" ? "publish_named_roll" : "seal_until_family_review";
                var selectedChoice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
                Require(selectedChoice != null && selectedChoice.flagValue == route &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The final archive review must expose its authored public or family-review choice.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, selectedChoice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice",
                            "last_oath_consent_archive", 1, out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "The consent archive choice must be recorded separately from Rowan's ending oath.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, selectedChoice.reward);

                var selectedQuestId = route == "named"
                    ? "side_last_oath_named_copy" : "side_last_oath_sealed_copy";
                var rejectedQuestId = route == "named"
                    ? "side_last_oath_sealed_copy" : "side_last_oath_named_copy";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedQuestId, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedQuestId, run.locationId),
                    "The archive choice must unlock only its matching review procedure.");
                Require(QuestProgressService.TryAcceptSideQuest(run, catalog, selectedQuestId, run.locationId),
                    "The selected archive review must be accepted in Crownfall Reach.");
                CompleteLastOathConsentSideQuest(run, catalog, selectedQuestId);

                var codexId = route == "named" ? "consent_named_archive" : "consent_sealed_archive";
                Require(CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry => entry.id == codexId),
                    "Each archive policy must unlock its own record and preserve the selected policy.");
                var resumed = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(resumed, catalog);
                Require(QuestProgressService.GetStoryFlag(resumed, "last_oath_consent_record") == route &&
                        resumed.completedQuestIds.Contains(selectedQuestId),
                    "The archive branch and its completed review must survive offline save serialization.");
            }
        }

        private static void ValidateCrownfallSharedTableLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog, RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog,
            FishingCatalogData fishingCatalog)
        {
            var meal = ItemCatalog.Find("crownfall_starlit_pottage");
            var recipe = RecipeCatalogService.FindById(recipeCatalog, "cook_crownfall_starlit_pottage");
            Require(meal?.category == "consumable" && meal.healAmount == 20 &&
                    recipe?.discipline == "cooking" && recipe.stationId == "last_oath_kitchen" &&
                    recipe.outputItemId == "crownfall_starlit_pottage" && recipe.outputQuantity == 1 &&
                    recipe.ingredients.Exists(item => item.itemId == "emberroot" && item.quantity == 1) &&
                    recipe.ingredients.Exists(item => item.itemId == "starlit_minnow" && item.quantity == 1),
                "The Crownfall field stove must cook one local Emberroot harvest and Starlit Minnow into the actual meal consumed by the open-table route.");

            var commonQuestIds = new[]
            {
                "side_crownfall_shared_table_open", "side_crownfall_shared_table_bowls",
                "side_crownfall_shared_table_portion", "side_crownfall_shared_table_alden",
                "side_crownfall_shared_table_rota", "side_crownfall_shared_table_emberroot",
                "side_crownfall_shared_table_bed", "side_crownfall_shared_table_minnow",
                "side_crownfall_shared_table_waterline", "side_crownfall_shared_table_cook",
                "side_crownfall_shared_table_warden", "side_crownfall_shared_table_reserve"
            };
            var postedBranch = new[]
            {
                "side_crownfall_shared_table_public_board", "side_crownfall_shared_table_public_forum",
                "side_crownfall_shared_table_public_receipt", "side_crownfall_shared_table_public_posting"
            };
            var openBranch = new[]
            {
                "side_crownfall_shared_table_quiet_room", "side_crownfall_shared_table_quiet_service",
                "side_crownfall_shared_table_quiet_return", "side_crownfall_shared_table_quiet_review"
            };
            var postedCodices = new[]
            {
                "crownfall_shared_table_public_board_record", "crownfall_shared_table_public_forum_record",
                "crownfall_shared_table_public_receipt_record", "crownfall_shared_table_public_posting_record"
            };
            var openCodices = new[]
            {
                "crownfall_shared_table_quiet_room_record", "crownfall_shared_table_quiet_service_record",
                "crownfall_shared_table_quiet_return_record", "crownfall_shared_table_quiet_review_record"
            };

            foreach (var policy in new[] { "posted_rule", "open_table" })
            {
                var run = new GameSaveData
                {
                    locationId = "last_oath_reach",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "last_oath_records" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    "side_crownfall_shared_table_choice", policy);
                Require(QuestProgressService.GetStoryFlag(run, "crownfall_shared_table_policy") == policy &&
                        InventoryService.Count(run, "crownfall_starlit_pottage") == 1,
                    "Ada's temporary meal policy must save independently from the prepared portion.");

                var selectedBranch = policy == "posted_rule" ? postedBranch : openBranch;
                var rejectedBranch = policy == "posted_rule" ? openBranch : postedBranch;
                var selectedCodices = policy == "posted_rule" ? postedCodices : openCodices;
                var rejectedCodices = policy == "posted_rule" ? openCodices : postedCodices;
                var selectedCharm = policy == "posted_rule" ? "open_hand_store_charm" : "quiet_table_charm";
                var rejectedCharm = policy == "posted_rule" ? "quiet_table_charm" : "open_hand_store_charm";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedBranch[0], run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedBranch[0], run.locationId),
                    "The Crownfall meal decision must open exactly one procedure.");
                foreach (var questId in selectedBranch)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                foreach (var codexId in selectedCodices)
                    Require(branchRecords.Exists(entry => entry.id == codexId),
                        "The chosen meal procedure must unlock each matching archive page: " + codexId);
                foreach (var codexId in rejectedCodices)
                    Require(!branchRecords.Exists(entry => entry.id == codexId),
                        "The unchosen meal procedure must remain locked: " + codexId);
                var expectedMealCount = policy == "posted_rule" ? 1 : 0;
                Require(InventoryService.Count(run, "crownfall_starlit_pottage") == expectedMealCount,
                    "The selected meal procedure must preserve or consume its cooked portion as authored: " + policy);
                Require(ItemCatalog.Find(selectedCharm)?.category == "equipment" &&
                        ItemCatalog.Find(selectedCharm)?.equipmentSlot == "charm",
                    "The selected meal procedure must award its authored charm equipment: " + selectedCharm);
                Require(InventoryService.Count(run, selectedCharm) == 1,
                    "The selected meal procedure must award exactly one matching charm: " + selectedCharm);
                Require(InventoryService.Count(run, rejectedCharm) == 0 &&
                        !QuestProgressService.IsCompleted(run, rejectedBranch[0]),
                    "The rejected meal procedure and its charm must remain unchosen: " + rejectedCharm);

                var convergence = new[]
                {
                    "side_crownfall_shared_table_shared_record", "side_crownfall_shared_table_warden_review",
                    "side_crownfall_shared_table_alden_review", "side_crownfall_shared_table_afterword"
                };
                foreach (var questId in convergence)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                var resumed = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(resumed, catalog);
                var finalRecords = CodexCatalogService.GetUnlocked(codexCatalog, resumed);
                var convergenceCompleted = true;
                foreach (var questId in convergence)
                    if (!resumed.completedQuestIds.Contains(questId)) convergenceCompleted = false;
                Require(convergenceCompleted &&
                        QuestProgressService.GetStoryFlag(resumed, "crownfall_shared_table_policy") == policy &&
                        finalRecords.Exists(entry => entry.id == "crownfall_shared_table_cook_record") &&
                        finalRecords.Exists(entry => entry.id == "crownfall_shared_table_afterword_record") &&
                        QuestProgressService.GetStoryFlag(resumed, "last_oath") == string.Empty,
                    "Both Crownfall meal procedures must converge after save/resume without choosing Rowan's campaign ending.");
            }
        }

        private static void ValidateCrownfallForecastLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var openRangeCharm = ItemCatalog.Find("crownfall_open_range_charm");
            var reviewIntervalCharm = ItemCatalog.Find("crownfall_review_interval_charm");
            Require(openRangeCharm?.category == "equipment" && openRangeCharm.equipmentSlot == "charm" &&
                    openRangeCharm.attackBonus == 2 && openRangeCharm.guardBonus == 2 &&
                    reviewIntervalCharm?.category == "equipment" && reviewIntervalCharm.equipmentSlot == "charm" &&
                    reviewIntervalCharm.attackBonus == 1 && reviewIntervalCharm.guardBonus == 4,
                "Each Crownfall reporting policy must award a distinct reviewed equippable charm.");
            var sharedQuestIds = new[]
            {
                "side_crownfall_forecast_arrival", "side_crownfall_forecast_folio",
                "side_crownfall_forecast_grain", "side_crownfall_forecast_waterline",
                "side_crownfall_forecast_signature", "side_crownfall_forecast_emberroot",
                "side_crownfall_forecast_emberroot_review", "side_crownfall_forecast_minnow",
                "side_crownfall_forecast_minnow_review", "side_crownfall_forecast_model",
                "side_crownfall_forecast_memory"
            };
            foreach (var route in new[] { "wide_range", "review" })
            {
                var run = new GameSaveData
                {
                    locationId = "last_oath_reach",
                    completedQuestIds = new List<string> { "last_oath_arrival", "last_oath_records" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                Require(!QuestProgressService.CanAcceptSideQuest(run, catalog,
                            sharedQuestIds[0], "outerwake_archive") &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, sharedQuestIds[0], run.locationId),
                    "Ada Sloane's forecast investigation must be region-locked and open after the final evidence review.");
                foreach (var questId in sharedQuestIds)
                {
                    if (questId != sharedQuestIds[0])
                        Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                            "Each completed measurement must unlock the next step in Ada's investigation: " + questId);
                    CompleteLastOathConsentSideQuest(run, catalog, questId);
                }

                const string choiceQuestId = "side_crownfall_forecast_choice";
                var choiceQuest = QuestCatalogService.FindById(catalog, choiceQuestId);
                var choiceId = route == "wide_range" ? "publish_wide_range" : "request_local_review";
                var selectedChoice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
                Require(choiceQuest != null && selectedChoice != null && selectedChoice.flagValue == route &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuestId, run.locationId),
                    "Ada's policy choice must expose a distinct public-method or affected-region review route.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, selectedChoice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice",
                            "crownfall_yield_choice", 1, out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuestId),
                    "The measurement policy must save separately from the final Crown or road oath.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, selectedChoice.reward);

                var selectedBranch = route == "wide_range"
                    ? new[] { "side_crownfall_forecast_publish_notice", "side_crownfall_forecast_publish_review",
                        "side_crownfall_forecast_publish_archive" }
                    : new[] { "side_crownfall_forecast_review_case", "side_crownfall_forecast_review_receipt",
                        "side_crownfall_forecast_review_meeting", "side_crownfall_forecast_review_archive" };
                var rejectedQuestId = route == "wide_range"
                    ? "side_crownfall_forecast_review_case" : "side_crownfall_forecast_publish_notice";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, selectedBranch[0], run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, rejectedQuestId, run.locationId),
                    "Only the selected method or review procedure may open after Ada's choice.");
                foreach (var questId in selectedBranch)
                {
                    Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                        "The chosen Crownfall report route must accept its next authored step: " + questId);
                    CompleteLastOathConsentSideQuest(run, catalog, questId);
                }

                var selectedCharm = route == "wide_range"
                    ? "crownfall_open_range_charm" : "crownfall_review_interval_charm";
                var rejectedCharm = route == "wide_range"
                    ? "crownfall_review_interval_charm" : "crownfall_open_range_charm";
                var sharedCodices = new[]
                {
                    "crownfall_forecast_provenance", "crownfall_granary_measure", "crownfall_lake_waterline",
                    "crownfall_signed_projection", "crownfall_emberroot_sample", "crownfall_starlit_sample",
                    "crownfall_model_provenance", "crownfall_warden_forecast_memory"
                };
                var unlocked = CodexCatalogService.GetUnlocked(codexCatalog, run);
                foreach (var codexId in sharedCodices)
                    Require(unlocked.Exists(entry => entry.id == codexId),
                        "The measured-yield evidence must unlock the corresponding shared record: " + codexId);
                var expectedBranchCodex = route == "wide_range"
                    ? "crownfall_public_range_record" : "crownfall_review_interval_record";
                var rejectedBranchCodex = route == "wide_range"
                    ? "crownfall_review_interval_record" : "crownfall_public_range_record";
                Require(unlocked.Exists(entry => entry.id == expectedBranchCodex) &&
                        !unlocked.Exists(entry => entry.id == rejectedBranchCodex) &&
                        run.inventory.Exists(item => item != null && item.itemId == selectedCharm && item.quantity == 1) &&
                        !run.inventory.Exists(item => item != null && item.itemId == rejectedCharm && item.quantity > 0) &&
                        QuestProgressService.GetStoryFlag(run, "last_oath") == string.Empty,
                    "Each report method must unlock only its own record and charm without silently choosing Rowan's ending.");
                var resumed = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(resumed, catalog);
                Require(QuestProgressService.GetStoryFlag(resumed, "crownfall_forecast_release") == route &&
                        resumed.completedQuestIds.Contains(selectedBranch[selectedBranch.Length - 1]) &&
                        !QuestProgressService.IsActive(resumed, rejectedQuestId),
                    "The measured-yield policy and mutually exclusive report route must survive offline save and resume.");
            }
        }

        private static void ValidateSaltEllisSignalLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var routeQuests = new[]
            {
                "side_salt_ellis_question", "side_salt_ellis_tag_test", "side_salt_ellis_signal",
                "side_salt_ellis_route_trace", "side_salt_ellis_ruth_statement",
                "side_salt_ellis_first_echo", "side_salt_ellis_whisper_sample",
                "side_salt_ellis_echo_compare"
            };
            foreach (var route in new[] { "send_limited", "wait_for_measurement" })
            {
                var run = new GameSaveData
                {
                    locationId = "salt_road",
                    completedQuestIds = new List<string> { "salt_route_handoff", "choir_reckoning" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.TryAcceptSideQuest(run, catalog, routeQuests[0], run.locationId),
                    "The Ellis evidence line must unlock only after the shared Salt Road and Choir resolutions.");

                foreach (var questId in routeQuests)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    Require(quest != null, "The Ellis evidence sequence must include " + questId + ".");
                    run.locationId = quest.locationId;
                    QuestProgressService.Reconcile(run, catalog);
                    if (questId != routeQuests[0])
                        Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                            "Each Ellis evidence step must unlock at its authored location: " + questId);
                    var matchedEveryObjective = quest.objectives != null;
                    foreach (var objective in quest.objectives ?? new List<QuestObjectiveDefinition>())
                        matchedEveryObjective &= QuestProgressService.RecordObjectives(run, catalog,
                            objective.kind, objective.targetId, objective.requiredCount, out _);
                    Require(matchedEveryObjective && run.completedQuestIds.Contains(questId) &&
                            run.activeSideQuestIds.Count == 0,
                        "Every Ellis evidence objective must complete through its authored world event: " + questId);
                    ApplyValidationReward(run, quest.reward);

                    run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                    QuestProgressService.Reconcile(run, catalog);
                    Require(run.completedQuestIds.Contains(questId),
                        "The Ellis evidence sequence must retain completed entries after save and resume: " + questId);
                }

                run.locationId = "choir_beneath_lake";
                var choiceQuest = QuestCatalogService.FindById(catalog, "side_salt_ellis_archive_choice");
                var selectedChoice = QuestCatalogService.FindChoice(choiceQuest,
                    route == "send_limited" ? "send_limited" : "wait_for_measurement");
                Require(choiceQuest != null && selectedChoice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The repeated chime and control sample must unlock the archive policy choice.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, selectedChoice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice",
                            "salt_ellis_archive_desk", 1, out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "The provisional-map policy must be recorded as a side-quest choice.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, selectedChoice.reward);

                var selectedQuestId = route == "send_limited"
                    ? "side_salt_ellis_send_ack" : "side_salt_ellis_hold_ack";
                var rejectedQuestId = route == "send_limited"
                    ? "side_salt_ellis_hold_ack" : "side_salt_ellis_send_ack";
                run.locationId = "salt_road";
                var resumedChoice = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(resumedChoice, catalog);
                Require(QuestProgressService.GetStoryFlag(resumedChoice, "salt_ellis_notice") == route &&
                        QuestProgressService.CanAcceptSideQuest(resumedChoice, catalog, selectedQuestId, run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(resumedChoice, catalog, rejectedQuestId, run.locationId),
                    "The map-delivery choice must save and unlock only its matching Nella follow-up.");
                Require(QuestProgressService.TryAcceptSideQuest(resumedChoice, catalog, selectedQuestId,
                            resumedChoice.locationId),
                    "The selected evidence policy must be playable as a Nella follow-up on Salt Road.");
                var finalQuest = QuestCatalogService.FindById(catalog, selectedQuestId);
                foreach (var objective in finalQuest.objectives)
                    QuestProgressService.RecordObjectives(resumedChoice, catalog, objective.kind,
                        objective.targetId, objective.requiredCount, out _);
                Require(resumedChoice.completedQuestIds.Contains(selectedQuestId) &&
                        CodexCatalogService.GetUnlocked(codexCatalog, resumedChoice)
                            .Exists(entry => entry.id == (route == "send_limited"
                                ? "ellis_limited_copy" : "ellis_deferred_copy")),
                    "Each Salt Road notice policy must finish and unlock its own codex record.");
            }
        }

        private static void ValidateGreenwakeChartLine(QuestCatalogData catalog,
            CodexCatalogData codexCatalog)
        {
            var routeQuests = new[]
            {
                "side_greenwake_chart_start", "side_greenwake_chart_rubbing",
                "side_greenwake_root_temperature", "side_greenwake_mara_account",
                "side_greenwake_wind_repeat", "side_greenwake_fish_control",
                "side_greenwake_star_overlay", "side_greenwake_return_copy"
            };
            foreach (var route in new[] { "publish_method", "private_copy" })
            {
                var run = new GameSaveData
                {
                    locationId = "greenwake_refuge",
                    completedQuestIds = new List<string> { "champion_star_map" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>()
                };
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.TryAcceptSideQuest(run, catalog, routeQuests[0], run.locationId),
                    "Owen's chart investigation must open after Rowan reaches the Greenwake star map.");

                foreach (var questId in routeQuests)
                {
                    var quest = QuestCatalogService.FindById(catalog, questId);
                    Require(quest != null, "The Greenwake chart investigation must include " + questId + ".");
                    run.locationId = quest.locationId;
                    QuestProgressService.Reconcile(run, catalog);
                    if (questId != routeQuests[0])
                        Require(QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                            "Each chart investigation step must unlock at its authored location: " + questId);
                    var matchedEveryObjective = quest.objectives != null;
                    foreach (var objective in quest.objectives ?? new List<QuestObjectiveDefinition>())
                        matchedEveryObjective &= QuestProgressService.RecordObjectives(run, catalog,
                            objective.kind, objective.targetId, objective.requiredCount, out _);
                    Require(matchedEveryObjective && run.completedQuestIds.Contains(questId) &&
                            run.activeSideQuestIds.Count == 0,
                        "Each map, temperature, wind and field-sample objective must complete from its authored event: " + questId);
                    ApplyValidationReward(run, quest.reward);
                    run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                    QuestProgressService.Reconcile(run, catalog);
                }

                run.locationId = "greenwake_refuge";
                var choiceQuest = QuestCatalogService.FindById(catalog, "side_greenwake_chart_policy");
                var selectedChoice = QuestCatalogService.FindChoice(choiceQuest, route);
                Require(choiceQuest != null && selectedChoice != null &&
                        QuestProgressService.TryAcceptSideQuest(run, catalog, choiceQuest.id, run.locationId),
                    "The tested chart must unlock its public-method or private-copy policy choice.");
                QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, selectedChoice.flagValue);
                Require(QuestProgressService.RecordObjectives(run, catalog, "choice",
                            "greenwake_chart_consultation", 1, out var choiceCompletions) &&
                        choiceCompletions.Exists(quest => quest.id == choiceQuest.id),
                    "The chart access decision must complete through its own consultation landmark.");
                ApplyValidationReward(run, choiceQuest.reward);
                ApplyValidationReward(run, selectedChoice.reward);

                var selectedQuestId = route == "publish_method"
                    ? "side_greenwake_public_method" : "side_greenwake_private_copy";
                var rejectedQuestId = route == "publish_method"
                    ? "side_greenwake_private_copy" : "side_greenwake_public_method";
                run.locationId = "greenwake_refuge";
                var resumed = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(resumed, catalog);
                Require(QuestProgressService.GetStoryFlag(resumed, "greenwake_chart_access") == route &&
                        QuestProgressService.CanAcceptSideQuest(resumed, catalog, selectedQuestId,
                            resumed.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(resumed, catalog, rejectedQuestId,
                            resumed.locationId),
                    "The chart access policy must save and unlock only its matching review procedure.");
                Require(QuestProgressService.TryAcceptSideQuest(resumed, catalog, selectedQuestId,
                            resumed.locationId),
                    "The chosen map-copy procedure must be playable in Greenwake.");
                var finalQuest = QuestCatalogService.FindById(catalog, selectedQuestId);
                foreach (var objective in finalQuest.objectives)
                    QuestProgressService.RecordObjectives(resumed, catalog, objective.kind,
                        objective.targetId, objective.requiredCount, out _);
                var codexId = route == "publish_method"
                    ? "greenwake_public_method" : "greenwake_private_method";
                Require(resumed.completedQuestIds.Contains(selectedQuestId) &&
                        CodexCatalogService.GetUnlocked(codexCatalog, resumed)
                            .Exists(entry => entry.id == codexId),
                    "Each chart-access route must finish and unlock only its own field record.");
            }
        }

        private static void CompleteLastOathConsentSideQuest(GameSaveData run, QuestCatalogData catalog,
            string questId)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            var matchedEveryObjective = quest?.objectives != null;
            foreach (var objective in quest?.objectives ?? new List<QuestObjectiveDefinition>())
                matchedEveryObjective &= QuestProgressService.RecordObjectives(run, catalog, objective.kind,
                    objective.targetId, objective.requiredCount, out _);
            Require(matchedEveryObjective && run.completedQuestIds.Contains(questId) &&
                    !QuestProgressService.IsActive(run, questId),
                "The consent archive quest must complete from its authored gameplay events: " + questId);
            ApplyValidationReward(run, quest.reward);
        }

        private static void ValidateLastOathRoute(GameSaveData run, QuestCatalogData catalog, string choiceId,
            string oath)
        {
            run.locationId = "last_oath_reach";
            QuestProgressService.Reconcile(run, catalog);
            Require(!run.chapterComplete && QuestProgressService.IsActive(run, "last_oath_arrival"),
                "Arc 8 must open after Evelyn receives the Outer-Wake expedition report.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "captain_alden_final", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "world_will_final_arrival", 1, out _);
            Require(QuestProgressService.IsActive(run, "last_oath_records"),
                "Both final witnesses must lead to the shared record review.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "last_oath_tablet", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "empty_crown_cradle", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_resonance", 1, out _);
            Require(QuestProgressService.IsActive(run, "last_oath_choice"),
                "The roster, Crown and Outer-Wake signal must open the final choice.");

            var choiceQuest = QuestProgressService.GetActiveQuest(run, catalog);
            var choice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
            Require(choice != null && choice.flagValue == oath,
                "Each final oath must resolve to its authored persistent route flag.");
            QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
            QuestProgressService.RecordObjective(run, catalog, "choice", "last_oath_choice", 1, out _);
            var selectedQuest = oath == "cycle" ? "last_oath_cycle_vow" : "last_oath_beyond_proofs";
            var unselectedQuest = oath == "cycle" ? "last_oath_beyond_proofs" : "last_oath_cycle_vow";
            Require(QuestProgressService.IsActive(run, selectedQuest) &&
                    !QuestProgressService.IsActive(run, unselectedQuest),
                "The final decision must activate only its matching oath route.");

            if (oath == "cycle")
            {
                QuestProgressService.RecordObjective(run, catalog, "talk", "captain_alden_final", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "inspect", "empty_crown_cradle", 1, out _);
                Require(QuestProgressService.IsActive(run, "last_oath_cycle_boss"),
                    "Alden's final vow must reveal only the Demon King encounter.");
                QuestProgressService.RecordObjective(run, catalog, "defeat", "demon_king_alden", 1, out _);
                Require(QuestProgressService.IsActive(run, "last_oath_cycle_epilogue"),
                    "Defeating Demon King Alden must open the Crown of Ash epilogue.");
                QuestProgressService.RecordObjective(run, catalog, "interact", "cycle_heart", 1, out _);
                Require(run.chapterComplete && !run.completedQuestIds.Contains("last_oath_beyond_epilogue"),
                    "The Crown of Ash route must conclude without completing the Beyond the Veil ending.");
            }
            else
            {
                QuestProgressService.RecordObjective(run, catalog, "inspect", "greenwake_root_testimony", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "inspect", "choir_cycle_testimony", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "inspect", "outerwake_star_testimony", 1, out _);
                Require(QuestProgressService.IsActive(run, "last_oath_world_boss"),
                    "The three independent records must reveal only The World Will's defense form.");
                QuestProgressService.RecordObjective(run, catalog, "defeat", "world_will_avatar", 1, out _);
                Require(QuestProgressService.IsActive(run, "last_oath_beyond_epilogue"),
                    "Defeating the defense form must open the Beyond the Veil epilogue.");
                QuestProgressService.RecordObjective(run, catalog, "interact", "outerwake_departure", 1, out _);
                Require(run.chapterComplete && !run.completedQuestIds.Contains("last_oath_cycle_epilogue"),
                    "The Beyond the Veil route must conclude without completing the Crown of Ash ending.");
            }

            Require(run.completedQuestIds.Count == 100 && CountCompletedQuestType(run, catalog, "story") == 100 &&
                    QuestProgressService.GetStoryFlag(run, "last_oath") == oath,
                "Either Arc 8 route must complete six new campaign quests and persist its final oath at 100 story quests.");
        }

        private static void ValidateCinderwellDepth(GameSaveData run, QuestCatalogData catalog, string waterRoute)
        {
            var branchId = waterRoute == "refugees" ? "cinder_cistern_refugee_roll" : "cinder_cistern_reserve_roll";
            var unchosenBranchId = waterRoute == "refugees" ? "cinder_cistern_reserve_roll" : "cinder_cistern_refugee_roll";
            var recordTarget = waterRoute == "refugees" ? "cinder_refugee_roll" : "cinder_reserve_roll";
            Require(QuestProgressService.IsActive(run, branchId) && !QuestProgressService.IsActive(run, unchosenBranchId),
                "The original water-rights decision must choose exactly one downstream Cinderwell evidence trail.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", recordTarget, 1, out var completed);
            Require(completed?.id == branchId && !run.completedQuestIds.Contains(unchosenBranchId) &&
                    QuestProgressService.IsActive(run, "cinder_cistern_entry"),
                "The selected water record must open the shared lower cistern while preserving the other route.");
            QuestProgressService.RecordObjective(run, catalog, "interact", "cinder_lower_hatch", 1, out completed);
            Require(completed?.id == "cinder_cistern_entry" && QuestProgressService.IsActive(run, "cinder_cistern_warden"),
                "Opening the lower hatch must activate the Cistern Warden encounter.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "cistern_warden", 1, out completed);
            Require(completed?.id == "cinder_cistern_warden" && QuestProgressService.IsActive(run, "cinder_transfer_docket"),
                "Defeating the siphoning Cistern Warden must expose its transfer docket.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "cinder_transfer_docket", 1, out completed);
            Require(completed?.id == "cinder_transfer_docket" && QuestProgressService.IsActive(run, "cinder_talia_testimony"),
                "The lower docket must send Rowan back to Talia to verify the Salt Road seal.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "talia_mercer", 1, out completed);
            Require(completed?.id == "cinder_talia_testimony" && QuestProgressService.IsActive(run, "cinder_june_report"),
                "Talia's seal check must unlock Sister June's report quest.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "sister_june", 1, out completed);
            Require(completed?.id == "cinder_june_report" && QuestProgressService.IsActive(run, "salt_arrival") &&
                    !run.completedQuestIds.Contains(unchosenBranchId) && run.completedQuestIds.Count == 33,
                "Either Cinderwell route must send its checked record to Salt Road and add six route quests.");
        }

        private static void ValidateSaltRoadRoute(GameSaveData run, QuestCatalogData catalog, string choiceId,
            string flagValue, string branchQuestId, string witnessId, string clueId, string unchosenBranchOne,
            string unchosenBranchTwo)
        {
            Require(QuestProgressService.IsActive(run, "salt_arrival"),
                "Completing Cinderwell must make the Salt Road arrival quest active.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "ruth_calder", 1, out _);
            Require(QuestProgressService.IsActive(run, "salt_caravan_manifest"),
                "Ruth Calder must open the tollhouse ledger investigation.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "salt_toll_ledger", 1, out _);
            Require(QuestProgressService.IsActive(run, "salt_massacre_signs"),
                "The old ledger must open the three-witness investigation.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "ruth_calder", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "nella_pike", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "silas_vane", 1, out _);
            Require(QuestProgressService.IsActive(run, "salt_route_choice"),
                "The three conflicting accounts must unlock the testimony choice.");
            var choiceQuest = QuestProgressService.GetActiveQuest(run, catalog);
            var choice = QuestCatalogService.FindChoice(choiceQuest, choiceId);
            Require(choice != null && choice.flagValue == flagValue,
                "Each Salt Road option must resolve to its authored stable story flag.");
            QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
            QuestProgressService.RecordObjective(run, catalog, "choice", "salt_road_testimony_choice", 1, out _);
            Require(QuestProgressService.IsActive(run, branchQuestId),
                "A Salt Road testimony choice must activate its corresponding branch only.");
            QuestProgressService.RecordObjective(run, catalog, "talk", witnessId, 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", clueId, 1, out _);
            Require(QuestProgressService.IsActive(run, "salt_bailiff") &&
                    !run.completedQuestIds.Contains(unchosenBranchOne) &&
                    !run.completedQuestIds.Contains(unchosenBranchTwo),
                "The selected account must expose its unique proof without completing the other witness routes.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "hollow_tollkeeper", 1, out var defeated);
            Require(defeated?.id == "salt_bailiff" && QuestProgressService.IsActive(run, "salt_reckoning"),
                "Defeating Hollow Tollkeeper must unlock the testimony report.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "ruth_calder", 1, out _);
            ValidateSaltRoadDepth(run, catalog, flagValue);
            Require(!run.chapterComplete && run.completedQuestIds.Count == 45 &&
                    QuestProgressService.IsActive(run, "choir_arrival") && run.completedQuestIds.Contains(branchQuestId) &&
                    run.storyFlags.Exists(flag => flag != null && flag.id == "salt_testimony" && flag.value == flagValue),
                "Each Salt Road witness route must unlock the Choir arrival quest with a persistent 45-quest path.");
        }

        private static void ValidateSaltRoadDepth(GameSaveData run, QuestCatalogData catalog, string testimony)
        {
            var branchId = testimony == "caravan" ? "salt_caravan_return_marks" :
                testimony == "refugees" ? "salt_refugee_wall_names" : "salt_hunter_impact_line";
            var unchosenOne = testimony == "caravan" ? "salt_refugee_wall_names" : "salt_caravan_return_marks";
            var unchosenTwo = testimony == "hunters" ? "salt_refugee_wall_names" : "salt_hunter_impact_line";
            var target = testimony == "caravan" ? "salt_return_route_marks" :
                testimony == "refugees" ? "salt_wall_name_slots" : "salt_hunter_impact_line";
            Require(QuestProgressService.IsActive(run, branchId) &&
                    !QuestProgressService.IsActive(run, unchosenOne) && !QuestProgressService.IsActive(run, unchosenTwo),
                "The saved Salt Road testimony must select exactly one aftermath clue route.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", target, 1, out var completed);
            Require(completed?.id == branchId && QuestProgressService.IsActive(run, "salt_underpass_access") &&
                    !run.completedQuestIds.Contains(unchosenOne) && !run.completedQuestIds.Contains(unchosenTwo),
                "The selected Salt Road clue must open the shared underpass without completing either unchosen route.");
            QuestProgressService.RecordObjective(run, catalog, "interact", "salt_tollhouse_floor", 1, out completed);
            Require(completed?.id == "salt_underpass_access" && QuestProgressService.IsActive(run, "salt_lockhouse_bailiff"),
                "Opening the tollhouse floor must unlock the Lockhouse Bailiff encounter.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "salt_lockhouse_bailiff", 1, out completed);
            Require(completed?.id == "salt_lockhouse_bailiff" && QuestProgressService.IsActive(run, "salt_lockhouse_docket"),
                "Defeating the chain-hook Bailiff must reveal the original transfer docket.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "salt_lockhouse_docket", 1, out completed);
            Require(completed?.id == "salt_lockhouse_docket" && QuestProgressService.IsActive(run, "salt_route_handoff"),
                "The original docket must return Rowan to Ruth for a signed handoff.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "ruth_calder", 1, out completed);
            Require(completed?.id == "salt_route_handoff" && QuestProgressService.IsActive(run, "choir_arrival") &&
                    !run.completedQuestIds.Contains(unchosenOne) && !run.completedQuestIds.Contains(unchosenTwo) &&
                    run.completedQuestIds.Count == 45,
                "All three testimony routes must hand a verified bell record to Choir after five unique path quests.");
        }

        private static void ValidateChoirRoute(GameSaveData run, QuestCatalogData catalog, string testimony)
        {
            Require(QuestProgressService.IsActive(run, "choir_arrival"),
                "Finishing any Salt Road branch must open the Choir arrival quest.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "first_warden", 1, out _);
            Require(QuestProgressService.IsActive(run, "choir_garden"),
                "The First Warden must begin the Echo Kelp garden activity.");
            QuestProgressService.RecordObjective(run, catalog, "grow", "echo_kelp", 1, out _);
            Require(QuestProgressService.IsActive(run, "choir_echo_records"),
                "Harvesting Echo Kelp must unlock the archive records.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "choir_archive_north", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "choir_archive_south", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "echo_moth", 1, out _);
            Require(QuestProgressService.IsActive(run, "choir_sonar"),
                "Both archive readings and Echo Moth must unlock the sonar objective.");
            QuestProgressService.RecordObjective(run, catalog, "fish", "whisper_koi", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "siltglass_eel", 1, out _);
            Require(QuestProgressService.IsActive(run, "choir_confrontation"),
                "Catching Whisper Koi and defeating Siltglass Eel must unlock Lyra's confrontation.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "lyra_moss", 1, out _);
            Require(QuestProgressService.IsActive(run, "choir_memory_choice"),
                "Lyra's account must lead to the archive memory choice.");
            QuestProgressService.SetStoryFlag(run, "choir_testimony", testimony);
            QuestProgressService.RecordObjective(run, catalog, "choice", "choir_memory_choice", 1, out _);
            var branchId = testimony == "preserve" ? "choir_preserve_records" : "choir_release_voices";
            var unchosenId = testimony == "preserve" ? "choir_release_voices" : "choir_preserve_records";
            Require(QuestProgressService.IsActive(run, branchId),
                "The Choir testimony choice must activate only its matching branch.");
            if (testimony == "preserve")
                QuestProgressService.RecordObjective(run, catalog, "craft", "resonance_lens", 1, out _);
            else
            {
                QuestProgressService.RecordObjective(run, catalog, "interact", "choir_resonance_north", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "interact", "choir_resonance_south", 1, out _);
            }
            Require(run.completedQuestIds.Contains(branchId) && !run.completedQuestIds.Contains(unchosenId) &&
                    QuestProgressService.IsActive(run, "choir_first_oath"),
                "Either archive branch must converge on the First Oath while leaving the alternate route uncompleted.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "choir_first_oath", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "aegis_cantor", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "world_will", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "talk", "first_warden", 1, out _);
            Require(!run.chapterComplete && run.completedQuestIds.Count == 56 &&
                    QuestProgressService.IsActive(run, "champion_arrival") &&
                    run.storyFlags.Exists(flag => flag != null && flag.id == "choir_testimony" && flag.value == testimony),
                "Each Arc 5 testimony route must activate Arc 6 after 45 quests while retaining its selected flag.");
        }

        private static void ValidateChampionRoute(GameSaveData run, QuestCatalogData catalog, string oath)
        {
            var unchosenBranch = oath == "accept" ? "champion_keep_name" : "champion_accept_oath";
            Require(QuestProgressService.IsActive(run, "champion_arrival"),
                "Completing the Choir report must activate the Greenwake arrival quest.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "mara_bell", 1, out _);
            Require(QuestProgressService.IsActive(run, "champion_garden_record"),
                "Mara Bell must open the two Greenwake resource records.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "greenwake_root_well", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "inspect", "greenwake_orchard_signal", 1, out _);
            Require(QuestProgressService.IsActive(run, "champion_offer"),
                "The root-well record must expose the Hundredth Champion decision.");
            var choiceQuest = QuestProgressService.GetActiveQuest(run, catalog);
            var choice = QuestCatalogService.FindChoice(choiceQuest, oath == "accept" ? "accept_oath" : "keep_name");
            Require(choice != null && choice.flagValue == oath,
                "The Champion decision must resolve to its authored oath flag.");
            QuestProgressService.SetStoryFlag(run, choiceQuest.choiceFlag, choice.flagValue);
            QuestProgressService.RecordObjective(run, catalog, "choice", "champion_offer", 1, out _);
            var branchQuest = oath == "accept" ? "champion_accept_oath" : "champion_keep_name";
            Require(QuestProgressService.IsActive(run, branchQuest) &&
                    !QuestProgressService.IsActive(run, unchosenBranch) &&
                    !run.completedQuestIds.Contains(unchosenBranch),
                "Only the accepted or refused Champion route may become active.");
            if (oath == "accept")
            {
                QuestProgressService.RecordObjective(run, catalog, "talk", "owen_reed", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "defeat", "seedbound_sentinel", 1, out _);
            }
            else
            {
                QuestProgressService.RecordObjective(run, catalog, "talk", "mara_bell", 1, out _);
                QuestProgressService.RecordObjective(run, catalog, "inspect", "greenwake_orchard_signal", 1, out _);
            }

            var branchContinuation = oath == "accept" ? "champion_accept_relay_test" : "champion_refusal_seed_plan";
            var unchosenContinuation = oath == "accept" ? "champion_refusal_seed_plan" : "champion_accept_relay_test";
            var branchEvidenceTarget = oath == "accept" ? "greenwake_crown_relay_seam" : "greenwake_seed_sharing_table";
            Require(run.completedQuestIds.Contains(branchQuest) &&
                    QuestProgressService.IsActive(run, branchContinuation) &&
                    !QuestProgressService.IsActive(run, unchosenContinuation) &&
                    !run.completedQuestIds.Contains(unchosenContinuation),
                "Each Champion choice must open only its matching follow-up testimony.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", branchEvidenceTarget, 1, out _);
            Require(run.completedQuestIds.Contains(branchContinuation) &&
                    QuestProgressService.IsActive(run, "champion_first_warden") &&
                    !run.completedQuestIds.Contains(unchosenBranch),
                "The selected relay or seed testimony must converge on the First Warden without completing the other route.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "first_warden_greenwake", 1, out _);
            var sharedEvidence = new[]
            {
                new { Quest = "champion_cycle_ring_records", Target = "greenwake_cycle_tablet" },
                new { Quest = "champion_lower_rill_trace", Target = "greenwake_lower_rill" },
                new { Quest = "champion_seed_calendar", Target = "greenwake_seed_calendar" },
                new { Quest = "champion_root_silt_sample", Target = "greenwake_root_silt" },
                new { Quest = "champion_caretaker_rota", Target = "greenwake_caretaker_rota" },
                new { Quest = "champion_trial_terms", Target = "greenwake_trial_terms" }
            };
            for (var index = 0; index < sharedEvidence.Length; index++)
            {
                var evidence = sharedEvidence[index];
                Require(QuestProgressService.IsActive(run, evidence.Quest),
                    "The Greenwake evidence chain must activate in order at " + evidence.Quest + ".");
                QuestProgressService.RecordObjective(run, catalog, "inspect", evidence.Target, 1, out var completed);
                var expectedNext = index + 1 < sharedEvidence.Length
                    ? sharedEvidence[index + 1].Quest : "champion_grove_trial";
                Require(completed?.id == evidence.Quest && QuestProgressService.IsActive(run, expectedNext),
                    "Each authored Greenwake investigation must complete and unlock the next story step: " + evidence.Quest + ".");
            }

            Require(run.completedQuestIds.Contains(branchQuest) && QuestProgressService.IsActive(run, "champion_grove_trial") &&
                    !run.completedQuestIds.Contains(unchosenBranch),
                "Both Champion decisions must pass through the evidence review and converge on the grove trial.");
            QuestProgressService.RecordObjective(run, catalog, "defeat", "briar_stalker", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "lantern_moth", 1, out _);
            QuestProgressService.RecordObjective(run, catalog, "defeat", "crownward_colossus", 1, out _);
            Require(QuestProgressService.IsActive(run, "champion_world_reply"),
                "Defeating the Crownward Colossus must open the World Will response.");
            QuestProgressService.RecordObjective(run, catalog, "talk", "world_will_greenwake", 1, out _);
            Require(QuestProgressService.IsActive(run, "champion_star_map"),
                "The World Will response must unlock the independently verifiable star chart.");
            QuestProgressService.RecordObjective(run, catalog, "inspect", "greenwake_star_chart", 1, out _);
            Require(!run.chapterComplete && run.completedQuestIds.Count == 72 &&
                    CountCompletedQuestType(run, catalog, "story") == 72 &&
                    QuestProgressService.IsActive(run, "archive_arrival") &&
                    run.storyFlags.Exists(flag => flag != null && flag.id == "champion_oath" && flag.value == oath) &&
                    !run.completedQuestIds.Contains(unchosenBranch),
                "Both Arc 6 routes must open Arc 7 after 72 completed campaign story quests and retain the Champion decision. Completed story quests: " +
                CountCompletedQuestType(run, catalog, "story") + ".");
        }

        private static void ValidateCharacterSideStories(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var requiredLandmarks = new[]
            {
                "jace_expedition_case", "jace_roster_cut", "jace_signed_draft", "jace_statement_desk",
                "jace_signed_copy", "jace_method_packet", "lyra_song_return_table", "lyra_public_stanza",
                "lyra_private_verse_case", "greenwake_glassplum_graft", "greenwake_graft_public_charter",
                "greenwake_graft_private_case", "alden_watch_ledger", "alden_watch_return_table",
                "alden_optin_roll", "alden_household_packet", "tamsin_wren", "choir_signal_bearing",
                "choir_signal_channel", "choir_signal_housing", "choir_signal_trial_table",
                "choir_signal_design_table", "choir_bell_pair_pattern", "choir_paired_light_pattern"
            };
            foreach (var targetId in requiredLandmarks)
                Require(landmarkCatalog?.entries?.Exists(entry => entry.targetId == targetId) == true,
                    "The three character stories must place their authored choice and evidence landmark: " + targetId);

            var lyraTool = ItemCatalog.Find("lyra_tuning_fork");
            var rootglassSyrup = ItemCatalog.Find("rootglass_syrup");
            Require(lyraTool?.category == "quest" && rootglassSyrup?.category == "consumable" &&
                    rootglassSyrup.healAmount == 24 &&
                    RecipeCatalogService.FindById(recipeCatalog, "forge_lyra_tuning_fork")?.stationId ==
                    "choir_harmonic_anvil" &&
                    RecipeCatalogService.FindById(recipeCatalog, "brew_jace_wind_diaphragm")?.stationId ==
                    "archive_alchemy_bench" &&
                    RecipeCatalogService.FindById(recipeCatalog, "brew_rootglass_syrup")?.stationId ==
                    "greenwake_alchemy_still",
                "The three new gameplay items and recipes must resolve to their authored regional workstations.");

            var signalBrace = ItemCatalog.Find("choir_pulse_brace");
            var pairedBellCharm = ItemCatalog.Find("choir_two_tone_emblem");
            var pairedLampCharm = ItemCatalog.Find("choir_light_echo_emblem");
            var signalBraceRecipe = RecipeCatalogService.FindById(recipeCatalog, "forge_choir_pulse_brace");
            Require(signalBrace?.category == "quest" && signalBraceRecipe?.stationId == "choir_harmonic_anvil" &&
                    signalBraceRecipe.outputItemId == "choir_pulse_brace" &&
                    signalBraceRecipe.ingredients.Exists(item => item.itemId == "echo_kelp") &&
                    signalBraceRecipe.ingredients.Exists(item => item.itemId == "whisper_koi") &&
                    pairedBellCharm?.category == "equipment" && pairedBellCharm.equipmentSlot == "charm" &&
                    pairedLampCharm?.category == "equipment" && pairedLampCharm.equipmentSlot == "charm" &&
                    QuestCatalogService.FindById(catalog, "side_choir_signal_open")?.reward?.items.Exists(
                        item => item.itemId == "earthworm_bait" && item.quantity >= 1) == true &&
                    QuestCatalogService.FindById(catalog, "side_choir_signal_policy")?.choices.Count == 2,
                "Tamsin Wren's Choir warning line must craft and install its local pulse brace and award two usable policy charms.");

            var aldenSpindle = ItemCatalog.Find("alden_watch_spindle");
            var aldenSpindleRecipe = RecipeCatalogService.FindById(recipeCatalog, "forge_alden_watch_spindle");
            var aldenOptInCharm = ItemCatalog.Find("alden_opt_in_ribbon");
            var aldenHouseholdCharm = ItemCatalog.Find("alden_household_mirror");
            Require(aldenSpindle?.category == "quest" && aldenSpindleRecipe?.stationId == "last_oath_forge" &&
                    aldenSpindleRecipe.outputItemId == "alden_watch_spindle" &&
                    aldenOptInCharm?.category == "equipment" && aldenOptInCharm.equipmentSlot == "charm" &&
                    aldenOptInCharm.attackBonus == 1 && aldenOptInCharm.guardBonus == 1 &&
                    aldenHouseholdCharm?.category == "equipment" && aldenHouseholdCharm.equipmentSlot == "charm" &&
                    aldenHouseholdCharm.guardBonus == 2,
                "Alden's watch story must craft its spindle at the Last Oath forge and award two usable policy charms.");

            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "outerwake_archive", "archive_return_report",
                new[]
                {
                    "side_outerwake_jace_open", "side_outerwake_jace_roster", "side_outerwake_jace_skyroot",
                    "side_outerwake_jace_clock", "side_outerwake_jace_carp", "side_outerwake_jace_first_talk",
                    "side_outerwake_jace_evelyn", "side_outerwake_jace_weather", "side_outerwake_jace_diaphragm",
                    "side_outerwake_jace_passive", "side_outerwake_jace_draft", "side_outerwake_jace_second_talk"
                },
                "side_outerwake_jace_choice",
                new[] { "signed_account", "method_only" },
                new[] { "side_outerwake_jace_named_copy", "side_outerwake_jace_method_copy" },
                "side_outerwake_jace_afterword",
                new[] { "jace_signed_knot", "jace_open_diaphragm_charm" },
                new[] { "jace_named_record", "jace_method_record" }, "jace_afterword_record");

            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "choir_beneath_lake", "choir_reckoning",
                new[]
                {
                    "side_choir_lyra_score", "side_choir_lyra_talk", "side_choir_lyra_fish",
                    "side_choir_lyra_log", "side_choir_lyra_grow", "side_choir_lyra_balm",
                    "side_choir_lyra_warden", "side_choir_lyra_rules"
                },
                "side_choir_lyra_choice",
                new[] { "offer", "keep" },
                new[] { "side_choir_lyra_offer_copy", "side_choir_lyra_private_copy" },
                "side_choir_lyra_song_afterword",
                new[] { "lyra_open_interval", "lyra_quiet_tuning_charm" },
                new[] { "lyra_offer_charter", "lyra_private_score" }, "lyra_after_song");

            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "choir_beneath_lake", "choir_reckoning",
                new[]
                {
                    "side_choir_signal_open", "side_choir_signal_bearing", "side_choir_signal_sample",
                    "side_choir_signal_channel", "side_choir_signal_lyra", "side_choir_signal_kelp",
                    "side_choir_signal_brace", "side_choir_signal_mount", "side_choir_signal_test",
                    "side_choir_signal_warden"
                },
                "side_choir_signal_policy",
                new[] { "paired_bells", "bell_and_lamp" },
                new[] { "side_choir_signal_bell_trial", "side_choir_signal_lamp_trial" },
                "side_choir_signal_afterword",
                new[] { "choir_two_tone_emblem", "choir_light_echo_emblem" },
                new[] { "choir_warning_bell_method", "choir_warning_lamp_method" },
                "choir_warning_return_record");

            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "dawnkeep_outpost", "order_cadet_oath",
                new[]
                {
                    "side_elara_garden_open", "side_elara_garden_shift_notes", "side_elara_garden_shift_talk",
                    "side_elara_garden_drain", "side_elara_garden_mint", "side_elara_garden_fish",
                    "side_elara_garden_waterline", "side_elara_garden_nia", "side_elara_garden_brace",
                    "side_elara_garden_install", "side_elara_garden_trial"
                },
                "side_elara_garden_policy",
                new[] { "common_bed", "short_rotation" },
                new[] { "side_elara_garden_shared_bed", "side_elara_garden_rotation_plan" },
                "side_elara_garden_afterword",
                new[] { "dawnkeep_common_soil_charm", "dawnkeep_rotating_bed_knot" },
                new[] { "dawnkeep_garden_shared_bed_record", "dawnkeep_garden_rotation_record" },
                "dawnkeep_garden_afterword");


            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "greenwake_refuge", "champion_star_map",
                new[]
                {
                    "side_greenwake_glassplum_open", "side_greenwake_glassplum_memory",
                    "side_greenwake_glassplum_first", "side_greenwake_glassplum_calendar",
                    "side_greenwake_glassplum_silt", "side_greenwake_glassplum_syrup",
                    "side_greenwake_glassplum_tasting", "side_greenwake_glassplum_second",
                    "side_greenwake_glassplum_graft_check"
                },
                "side_greenwake_glassplum_choice",
                new[] { "share", "hold" },
                new[] { "side_greenwake_glassplum_share_record", "side_greenwake_glassplum_hold_record" },
                "side_greenwake_glassplum_afterword",
                new[] { "mara_sunwire_charm", "mara_guarded_graft_ring" },
                new[] { "mara_share_charter", "mara_private_root_case" }, "mara_next_garden");

            ValidateCharacterSideStoryRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                "last_oath_reach", "last_oath_records",
                new[]
                {
                    "side_last_oath_watch_open", "side_last_oath_watch_ask", "side_last_oath_watch_emberroot",
                    "side_last_oath_watch_minnow", "side_last_oath_watch_spindle", "side_last_oath_watch_sword",
                    "side_last_oath_watch_roll", "side_last_oath_watch_warden"
                },
                "side_last_oath_watch_policy",
                new[] { "named_optin", "household_copy" },
                new[] { "side_last_oath_watch_named_copy", "side_last_oath_watch_household_copy" },
                "side_last_oath_watch_afterword",
                new[] { "alden_opt_in_ribbon", "alden_household_mirror" },
                new[] { "alden_named_optin_record", "alden_household_copy_record" },
                "alden_watch_afterword_record");

            ValidateHeroLegacyArchiveRoute(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog,
                landmarkCatalog);
            ValidateCarryingCapacityLine(catalog, codexCatalog, recipeCatalog, farmCatalog, fishingCatalog);
        }

        private static void ValidateHeroLegacyArchiveRoute(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var run = new GameSaveData
            {
                locationId = "last_oath_reach",
                inventory = new List<InventoryStackData>(),
                completedQuestIds = new List<string> { "last_oath_records" },
                activeSideQuestIds = new List<string>(),
                questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                storyFlags = new List<StoryFlagData>()
            };

            for (var number = 1; number <= 99; number++)
            {
                var suffix = number.ToString("000");
                var questId = "side_hero_legacy_" + suffix;
                var targetId = "hero_legacy_" + suffix + "_record";
                var quest = QuestCatalogService.FindById(catalog, questId);
                var record = codexCatalog.entries.Find(entry => entry != null && entry.id == targetId);
                var landmark = landmarkCatalog.entries.Find(entry => entry != null &&
                    entry.targetId == targetId && entry.locationId == quest?.locationId);
                Require(quest != null && quest.type == "side" && quest.objectives?.Count == 1 &&
                        quest.objectives[0].kind == "inspect" && quest.objectives[0].targetId == targetId &&
                        record != null && record.unlockQuestId == questId && landmark != null &&
                        (number == 1
                            ? quest.prerequisiteIds?.Contains("last_oath_records") == true
                            : quest.prerequisiteIds?.Contains("side_hero_legacy_" + (number - 1).ToString("000")) == true),
                    "Each named hero memorial must have a regional inspection, chained quest and matching field record: " +
                    suffix);

                run.locationId = quest.locationId;
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, questId, run.locationId),
                    "The next Hundredth Roll record must unlock from the previous memorial: " + questId);
                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog, questId, "");
                Require(CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry => entry.id == targetId),
                    "Reading each memorial must unlock its matching field record: " + targetId);

                if (number % 11 == 0 || number == 99)
                {
                    run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                    QuestProgressService.Reconcile(run, catalog);
                    Require(QuestProgressService.IsCompleted(run, questId) &&
                            CodexCatalogService.GetUnlocked(codexCatalog, run).Exists(entry => entry.id == targetId),
                        "The Hundredth Roll route must retain its latest quest and archive record after save/resume: " +
                        questId);
                }
            }
        }

        private static void ValidateCarryingCapacityLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog)
        {
            var skyrootBed = farmCatalog?.entries?.Find(plot => plot != null &&
                plot.id == "outerwake_skyroot_bed");
            var glassplumBed = farmCatalog?.entries?.Find(plot => plot != null &&
                plot.id == "greenwake_glassplum_bed");
            var echoKelpBed = farmCatalog?.entries?.Find(plot => plot != null &&
                plot.id == "choir_echo_kelp_bed");
            var saffronBed = farmCatalog?.entries?.Find(plot => plot != null &&
                plot.id == "cinderwell_saffron_bed");
            var echoBalmRecipe = RecipeCatalogService.FindById(recipeCatalog, "brew_echo_balm");
            var brineWickRecipe = RecipeCatalogService.FindById(recipeCatalog, "brew_cinderwell_brine_wick");
            var marginCompass = ItemCatalog.Find("outerwake_margin_compass");
            var reviewLocket = ItemCatalog.Find("outerwake_review_locket");
            Require(skyrootBed?.cropId == "skyroot" && glassplumBed?.cropId == "glassplum" &&
                    echoKelpBed?.cropId == "echo_kelp" && saffronBed?.cropId == "salt_saffron" &&
                    echoBalmRecipe?.stationId == "choir_archive_loom" &&
                    echoBalmRecipe.outputItemId == "echo_balm" &&
                    brineWickRecipe?.stationId == "cinderwell_assay_bench" &&
                    brineWickRecipe.outputItemId == "cinderwell_brine_wick" &&
                    marginCompass?.category == "equipment" && marginCompass.equipmentSlot == "charm" &&
                    marginCompass.guardBonus == 2 && reviewLocket?.category == "equipment" &&
                    reviewLocket.equipmentSlot == "charm" && reviewLocket.attackBonus == 1 &&
                    reviewLocket.guardBonus == 1,
                "The resource-model line must use its four regional crops, both local recipes and two distinct equippable report-policy charms.");

            var commonQuestIds = new[]
            {
                "side_capacity_open", "side_capacity_projection", "side_capacity_gauge",
                "side_capacity_skyroot", "side_capacity_farwake", "side_capacity_clock",
                "side_capacity_review", "side_capacity_garden", "side_capacity_seedledger",
                "side_capacity_glassplum", "side_capacity_wellmarks", "side_capacity_choir",
                "side_capacity_whisper", "side_capacity_kelp", "side_capacity_balm",
                "side_capacity_listening", "side_capacity_cinder", "side_capacity_saffron",
                "side_capacity_wick", "side_capacity_color", "side_capacity_dawnkeep",
                "side_capacity_blackreed", "side_capacity_waterline", "side_capacity_return",
                "side_capacity_compare"
            };
            var routeValues = new[] { "publish_ranges", "regional_review" };
            var branchQuestIds = new[] { "side_capacity_publish", "side_capacity_restricted" };
            var branchItems = new[] { "outerwake_margin_compass", "outerwake_review_locket" };
            var branchRecords = new[] { "capacity_publish_record", "capacity_restricted_record" };

            for (var routeIndex = 0; routeIndex < routeValues.Length; routeIndex++)
            {
                var rejectedIndex = 1 - routeIndex;
                var run = new GameSaveData
                {
                    locationId = "outerwake_archive",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "archive_return_report" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                {
                    run.locationId = QuestCatalogService.FindById(catalog, questId).locationId;
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");
                }

                run.locationId = "outerwake_archive";
                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    "side_capacity_policy", routeValues[routeIndex]);
                var policy = QuestCatalogService.FindById(catalog, "side_capacity_policy");
                Require(QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == routeValues[routeIndex] &&
                        InventoryService.Count(run, branchItems[routeIndex]) == 1 &&
                        InventoryService.Count(run, branchItems[rejectedIndex]) == 0 &&
                        InventoryService.TryEquip(run, branchItems[routeIndex]),
                    "The selected publication policy must award only its matching charm: " + routeValues[routeIndex]);

                run.locationId = "outerwake_archive";
                Require(QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex],
                            run.locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedIndex],
                            run.locationId),
                    "The resource-model choice must unlock only the selected report route: " + routeValues[routeIndex]);
                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    branchQuestIds[routeIndex], "");
                var unlockedBranchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(unlockedBranchRecords.Exists(entry => entry.id == branchRecords[routeIndex]) &&
                        !unlockedBranchRecords.Exists(entry => entry.id == branchRecords[rejectedIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "Each report policy must unlock only its own evidence record: " + routeValues[routeIndex]);

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.GetStoryFlag(run, "capacity_publication_policy") ==
                            routeValues[routeIndex] &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, "side_capacity_afterword",
                            "outerwake_archive"),
                    "The selected report and any-of afterword must survive save/resume: " + routeValues[routeIndex]);
                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    "side_capacity_afterword", "");
                var unlockedAfterword = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, "side_capacity_afterword") &&
                        unlockedAfterword.Exists(entry => entry.id == "capacity_afterword_record") &&
                        QuestProgressService.GetStoryFlag(run, "capacity_publication_policy") == routeValues[routeIndex],
                    "Both report policies must reach the archived afterword without changing the final story choice.");
            }
        }

        private static void ValidateCisternPressureWheelLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, EncounterCatalogData encounterCatalog,
            MonsterCatalogData monsterCatalog)
        {
            var routeValues = new[] { "shared_rill", "steward_shift" };
            var branchQuestIds = new[]
            {
                "side_cistern_wheel_shared_rill", "side_cistern_wheel_steward_shift"
            };
            var branchItemIds = new[] { "cinder_shared_rill_charm", "cinder_steward_shift_pin" };
            var branchCodexIds = new[] { "cinder_shared_rill_record", "cinder_steward_schedule_record" };
            var commonQuestIds = new[]
            {
                "side_cistern_wheel_bearing", "side_cistern_wheel_talia", "side_cistern_wheel_marks",
                "side_cistern_wheel_moss", "side_cistern_wheel_backwash", "side_cistern_wheel_wight",
                "side_cistern_wheel_lens", "side_cistern_wheel_report", "side_cistern_wheel_filter_craft",
                "side_cistern_wheel_filter_test", "side_cistern_wheel_dial", "side_cistern_wheel_account",
                "side_cistern_wheel_ratchet"
            };
            var brineglassBed = farmCatalog?.entries?.Find(entry => entry != null &&
                entry.id == "cinder_cistern_brineglass_bed");
            var filterRecipe = RecipeCatalogService.FindById(recipeCatalog, "brew_cinder_moss_filter");
            var pressureWight = MonsterCatalogService.FindById(monsterCatalog, "cinder_pressure_wight");
            var pressureWightEncounter = EncounterCatalogService.FindById(encounterCatalog,
                "cinder_pressure_wight_site");
            var sharedCharm = ItemCatalog.Find(branchItemIds[0]);
            var stewardPin = ItemCatalog.Find(branchItemIds[1]);
            Require(brineglassBed != null && brineglassBed.cropId == "brineglass_moss" &&
                    filterRecipe != null && filterRecipe.stationId == "cinderwell_assay_bench" &&
                    filterRecipe.outputItemId == "cinder_moss_filter" &&
                    pressureWight?.rank == "elite" && pressureWight.specialMoveId == "marked_strike" &&
                    pressureWightEncounter?.requiredQuestId == "side_cistern_wheel_wight" &&
                    sharedCharm?.category == "equipment" && sharedCharm.equipmentSlot == "charm" &&
                    sharedCharm.attackBonus == 1 && sharedCharm.guardBonus == 1 &&
                    stewardPin?.category == "equipment" && stewardPin.equipmentSlot == "charm" &&
                    stewardPin.guardBonus == 2,
                "The Cistern pressure-wheel line must use its local crop, gated elite, assay recipe and two equipable policy rewards.");

            for (var routeIndex = 0; routeIndex < routeValues.Length; routeIndex++)
            {
                var selectedValue = routeValues[routeIndex];
                var rejectedIndex = 1 - routeIndex;
                var run = new GameSaveData
                {
                    locationId = "cinder_cistern",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "cinder_cistern_warden" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteCisternPressureWheelQuest(run, catalog, recipeCatalog, farmCatalog, encounterCatalog,
                        monsterCatalog, questId, "");

                CompleteCisternPressureWheelQuest(run, catalog, recipeCatalog, farmCatalog, encounterCatalog,
                    monsterCatalog, "side_cistern_wheel_policy", selectedValue);
                var policyQuest = QuestCatalogService.FindById(catalog, "side_cistern_wheel_policy");
                Require(QuestProgressService.GetStoryFlag(run, policyQuest.choiceFlag) == selectedValue &&
                        InventoryService.Count(run, branchItemIds[routeIndex]) == 1 &&
                        InventoryService.Count(run, branchItemIds[rejectedIndex]) == 0 &&
                        InventoryService.TryEquip(run, branchItemIds[routeIndex]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex],
                            "cinder_cistern") &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedIndex],
                            "cinder_cistern"),
                    "The Cistern policy choice must equip one matching charm and unlock only its selected route: " +
                    selectedValue);

                CompleteCisternPressureWheelQuest(run, catalog, recipeCatalog, farmCatalog, encounterCatalog,
                    monsterCatalog, branchQuestIds[routeIndex], "");
                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(branchRecords.Exists(entry => entry.id == branchCodexIds[routeIndex]) &&
                        !branchRecords.Exists(entry => entry.id == branchCodexIds[rejectedIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "Each Cistern policy route must unlock only its own filed procedure: " + selectedValue);

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.GetStoryFlag(run, "cistern_bypass_policy") == selectedValue &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, "side_cistern_wheel_afterword",
                            "cinder_cistern"),
                    "The selected Cistern policy and its any-of afterword must survive a save/resume boundary.");
                CompleteCisternPressureWheelQuest(run, catalog, recipeCatalog, farmCatalog, encounterCatalog,
                    monsterCatalog, "side_cistern_wheel_afterword", "");
                var completedRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, "side_cistern_wheel_afterword") &&
                        completedRecords.Exists(entry => entry.id == "cinder_bypass_afterword_record") &&
                        QuestProgressService.GetStoryFlag(run, "cistern_bypass_policy") == selectedValue,
                    "Both pressure-wheel policies must reach the saved afterword and retain their route flag.");
            }
        }

        private static void ValidateSaltRoadMilepostLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var commonQuestIds = new[]
            {
                "side_saltroad_milepost_request", "side_saltroad_milepost_mounts", "side_saltroad_silas_measure",
                "side_saltroad_windglass_grow", "side_saltroad_spoolfin_sample", "side_saltroad_storm_register",
                "side_saltroad_roadglass_sentinel", "side_saltroad_ruth_interval", "side_saltroad_talia_review",
                "side_saltroad_beacon_lens", "side_saltroad_beacon_mount", "side_saltroad_beacon_range",
                "side_saltroad_nella_review"
            };
            var routeValues = new[] { "dayline", "night_call" };
            var branchQuestIds = new[] { "side_saltroad_dayline_record", "side_saltroad_callkeeper_rota" };
            var branchItemIds = new[] { "saltroad_dayline_compass_charm", "saltroad_callkeeper_whistle" };
            var branchCodexIds = new[] { "saltroad_dayline_result_record", "saltroad_callkeeper_result_record" };
            var windglassBed = farmCatalog?.entries?.Find(entry => entry != null &&
                entry.id == "saltroad_windglass_reed_bed");
            var shelteredPool = fishingCatalog?.entries?.Find(entry => entry != null &&
                entry.id == "saltroad_sheltered_pool");
            var beaconRecipe = RecipeCatalogService.FindById(recipeCatalog, "craft_saltroad_beacon_lens");
            var sentinel = MonsterCatalogService.FindById(monsterCatalog, "roadglass_sentinel");
            var sentinelEncounter = EncounterCatalogService.FindById(encounterCatalog,
                "saltroad_roadglass_sentinel_site");
            var starterQuest = QuestCatalogService.FindById(catalog, commonQuestIds[0]);
            var beaconLens = ItemCatalog.Find("saltroad_beacon_lens");
            var requiredTargets = new[]
            {
                "saltroad_milepost_cracks", "saltroad_storm_table", "saltroad_beacon_mount",
                "saltroad_beacon_range", "saltroad_signal_policy", "saltroad_dayline_sheet",
                "saltroad_callkeeper_rota"
            };
            Require(windglassBed != null && windglassBed.locationId == "salt_road" &&
                    windglassBed.cropId == "windglass_reed" && shelteredPool != null &&
                    shelteredPool.locationId == "salt_road" && shelteredPool.baitItemId == "earthworm_bait" &&
                    shelteredPool.catches.Exists(fish => fish != null && fish.itemId == "saltspool_skate") &&
                    beaconRecipe != null && beaconRecipe.stationId == "cinderwell_assay_bench" &&
                    beaconRecipe.outputItemId == "saltroad_beacon_lens" && sentinel?.rank == "elite" &&
                    sentinel.specialMoveId == "marked_strike" && sentinelEncounter != null &&
                    sentinelEncounter.requiredQuestId == "side_saltroad_roadglass_sentinel" &&
                    sentinelEncounter.defeatObjectiveTargetId == "roadglass_sentinel" &&
                    beaconLens?.category == "quest" && starterQuest?.reward?.items != null &&
                    starterQuest.reward.items.Exists(item => item != null && item.itemId == "earthworm_bait" &&
                                                              item.quantity >= 2),
                "The Salt Road milepost line must connect its local crop, baited pool, gated marked-strike elite and Cinderwell assay recipe, and supply retry bait.");
            foreach (var targetId in requiredTargets)
                Require(landmarkCatalog?.entries?.Exists(entry => entry != null && entry.locationId == "salt_road" &&
                    entry.targetId == targetId) == true,
                    "The Salt Road signal route must place an authored interactable for " + targetId + ".");
            foreach (var questId in commonQuestIds)
                Require(QuestCatalogService.FindById(catalog, questId) != null,
                    "The milepost chain must include its common quest step: " + questId);

            for (var routeIndex = 0; routeIndex < routeValues.Length; routeIndex++)
            {
                var selectedValue = routeValues[routeIndex];
                var rejectedIndex = 1 - routeIndex;
                var run = new GameSaveData
                {
                    locationId = "salt_road",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "salt_route_handoff" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        encounterCatalog, monsterCatalog, questId, "");

                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_saltroad_signal_policy", selectedValue);
                var policyQuest = QuestCatalogService.FindById(catalog, "side_saltroad_signal_policy");
                var selectedItem = ItemCatalog.Find(branchItemIds[routeIndex]);
                Require(QuestProgressService.GetStoryFlag(run, policyQuest.choiceFlag) == selectedValue &&
                        selectedItem?.category == "equipment" && selectedItem.equipmentSlot == "charm" &&
                        InventoryService.Count(run, branchItemIds[routeIndex]) == 1 &&
                        InventoryService.Count(run, branchItemIds[rejectedIndex]) == 0 &&
                        InventoryService.TryEquip(run, branchItemIds[routeIndex]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex], "salt_road") &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedIndex], "salt_road"),
                    "Each milepost policy must award its own equipable charm and unlock only the selected record: " +
                    selectedValue);

                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, branchQuestIds[routeIndex], "");
                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(branchRecords.Exists(entry => entry.id == branchCodexIds[routeIndex]) &&
                        !branchRecords.Exists(entry => entry.id == branchCodexIds[rejectedIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "The milepost route must unlock only its selected operating record: " + selectedValue);

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.GetStoryFlag(run, policyQuest.choiceFlag) == selectedValue &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog,
                            "side_saltroad_milepost_afterword", "salt_road"),
                    "The selected milepost policy and shared afterword must survive a save/resume boundary: " +
                    selectedValue);
                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_saltroad_milepost_afterword", "");
                var completedRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, "side_saltroad_milepost_afterword") &&
                        completedRecords.Exists(entry => entry.id == "saltroad_milepost_afterword_record") &&
                        QuestProgressService.GetStoryFlag(run, policyQuest.choiceFlag) == selectedValue,
                    "Both Salt Road signal policies must reach the saved afterword and retain the chosen route.");
            }
        }

        private static void ValidateRuthRecalledOrderLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var commonQuestIds = new[]
            {
                "side_ruth_recall_open", "side_ruth_recall_margin", "side_ruth_recall_nella",
                "side_ruth_recall_pass", "side_ruth_recall_skate", "side_ruth_recall_bell",
                "side_ruth_recall_guard", "side_ruth_recall_filament", "side_ruth_recall_reed",
                "side_ruth_recall_lens", "side_ruth_recall_june", "side_ruth_recall_lightbox",
                "side_ruth_recall_reverse", "side_ruth_recall_silas", "side_ruth_recall_signal",
                "side_ruth_recall_ruth"
            };
            var routeValues = new[] { "ruth_signs_first", "nella_countersigns" };
            var branchQuestIds = new[] { "side_ruth_recall_ruth_sign", "side_ruth_recall_joint_sign" };
            var branchItemIds = new[] { "ruth_signed_keel_charm", "nella_boundary_knot" };
            var branchCodexIds = new[]
            {
                "ruth_recall_ruth_sign_record", "ruth_recall_joint_sign_record"
            };
            var opening = QuestCatalogService.FindById(catalog, commonQuestIds[0]);
            var plateRecipe = RecipeCatalogService.FindById(recipeCatalog, "craft_saltroad_beacon_lens");
            var sentinelEncounter = EncounterCatalogService.FindById(encounterCatalog, "saltroad_ruth_cart_guard");
            var roadglass = MonsterCatalogService.FindById(monsterCatalog, "roadglass_sentinel");
            var requiredLandmarks = new[]
            {
                "ruth_axle_dispatch_margin", "nella_pass_card_notches", "ruth_toll_bell_shell",
                "ruth_roadglass_filament", "ruth_manifest_lightbox", "ruth_manifest_reverse",
                "silas_signal_sightline_gap", "ruth_signed_addendum", "nella_joint_witness_copy"
            };
            Require(opening?.prerequisiteIds.Contains("salt_route_handoff") == true &&
                    opening.reward.items.Exists(item => item != null && item.itemId == "windglass_reed_seed") &&
                    opening.reward.items.Exists(item => item != null && item.itemId == "earthworm_bait" &&
                                                         item.quantity >= 1) &&
                    plateRecipe?.stationId == "cinderwell_assay_bench" &&
                    plateRecipe.outputItemId == "saltroad_beacon_lens" &&
                    plateRecipe.ingredients.Exists(item => item != null && item.itemId == "windglass_reed") &&
                    plateRecipe.ingredients.Exists(item => item != null && item.itemId == "saltspool_skate") &&
                    plateRecipe.ingredients.Exists(item => item != null && item.itemId == "roadglass_filament") &&
                    roadglass?.rank == "elite" && sentinelEncounter?.requiredQuestId == "side_ruth_recall_guard" &&
                    sentinelEncounter.defeatObjectiveTargetId == "roadglass_sentinel" &&
                    ItemCatalog.Find("saltroad_beacon_lens")?.category == "quest",
                "Ruth's route must supply its seed and bait, gate the elite, and use the measured Cinderwell plate recipe.");
            foreach (var targetId in requiredLandmarks)
                Require(landmarkCatalog?.entries?.Exists(entry => entry != null &&
                            entry.targetId == targetId &&
                            (entry.locationId == "salt_road" || entry.locationId == "salt_lockhouse")) == true,
                    "Ruth's route must place a world interactable for " + targetId + ".");
            foreach (var questId in commonQuestIds)
                Require(QuestCatalogService.FindById(catalog, questId) != null,
                    "The recalled-order chain must include its common quest step: " + questId);

            for (var routeIndex = 0; routeIndex < routeValues.Length; routeIndex++)
            {
                var selectedValue = routeValues[routeIndex];
                var rejectedIndex = 1 - routeIndex;
                var run = new GameSaveData
                {
                    locationId = "salt_road",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "salt_route_handoff" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        encounterCatalog, monsterCatalog, questId, "");

                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_ruth_recall_policy", selectedValue);
                var policy = QuestCatalogService.FindById(catalog, "side_ruth_recall_policy");
                var selectedCharm = ItemCatalog.Find(branchItemIds[routeIndex]);
                Require(QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        selectedCharm?.category == "equipment" && selectedCharm.equipmentSlot == "charm" &&
                        InventoryService.Count(run, branchItemIds[routeIndex]) == 1 &&
                        InventoryService.Count(run, branchItemIds[rejectedIndex]) == 0 &&
                        InventoryService.TryEquip(run, branchItemIds[routeIndex]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex],
                            "salt_road") &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedIndex],
                            "salt_road"),
                    "The signature decision must award and equip its own charm and unlock only its matching account.");

                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, branchQuestIds[routeIndex], "");
                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(branchRecords.Exists(entry => entry.id == branchCodexIds[routeIndex]) &&
                        !branchRecords.Exists(entry => entry.id == branchCodexIds[rejectedIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "The archive must file only the signature policy the player chose.");

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog,
                            "side_ruth_recall_afterword", "salt_road"),
                    "The chosen correction and shared afterword must survive save and resume.");
                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_ruth_recall_afterword", "");
                Require(QuestProgressService.IsCompleted(run, "side_ruth_recall_afterword") &&
                        QuestProgressService.IsCompleted(run, "side_ruth_recall_lightbox") &&
                        InventoryService.Count(run, "saltroad_beacon_lens") == 0 &&
                        QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        QuestProgressService.IsCompleted(run, branchQuestIds[routeIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "The light-box must consume its plate and both filing routes must converge without erasing the choice.");
            }
        }

        private static void ValidateNellaMissingNameLine(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog,
            QuestLandmarkCatalogData landmarkCatalog)
        {
            var commonQuestIds = new[]
            {
                "side_nella_open", "side_nella_card", "side_nella_wall", "side_nella_ruth",
                "side_nella_docket", "side_nella_return_mark", "side_nella_skate", "side_nella_reed",
                "side_nella_fiber_check", "side_nella_craft", "side_nella_june", "side_nella_seal",
                "side_nella_install", "side_nella_chain", "side_nella_silas", "side_nella_sightline",
                "side_nella_nella"
            };
            var routeValues = new[] { "method_public", "family_review" };
            var branchQuestIds = new[] { "side_nella_public_margin", "side_nella_family_copy" };
            var branchItemIds = new[] { "pike_public_margin_compass", "pike_family_review_knot" };
            var branchCodexIds = new[]
            {
                "nella_missing_public_margin_record", "nella_missing_family_copy_record"
            };
            var opening = QuestCatalogService.FindById(catalog, commonQuestIds[0]);
            var sleeveRecipe = RecipeCatalogService.FindById(recipeCatalog, "craft_pike_tag_sleeve");
            var requiredLandmarks = new[]
            {
                "pike_tag_return_mark", "pike_windglass_fiber_sample", "pike_name_seal_rule",
                "pike_tag_sleeve_frame", "pike_signal_gap_sketch", "pike_archive_policy",
                "pike_public_margin", "pike_family_review_copy"
            };
            Require(opening?.prerequisiteIds.Contains("side_ruth_recall_afterword") == true &&
                    opening.reward.items.Exists(item => item != null && item.itemId == "windglass_reed_seed") &&
                    opening.reward.items.Exists(item => item != null && item.itemId == "earthworm_bait" &&
                                                         item.quantity >= 1) &&
                    sleeveRecipe?.outputItemId == "pike_tag_sleeve" &&
                    sleeveRecipe.stationId == "cinderwell_assay_bench" &&
                    sleeveRecipe.ingredients.Exists(item => item != null && item.itemId == "windglass_reed") &&
                    sleeveRecipe.ingredients.Exists(item => item != null && item.itemId == "saltspool_skate") &&
                    sleeveRecipe.ingredients.Exists(item => item != null && item.itemId == "dryglass_shard") &&
                    ItemCatalog.Find("pike_tag_sleeve")?.category == "quest" &&
                    QuestCatalogService.FindById(catalog, "side_nella_public_margin")?.prerequisiteIds
                        .Contains("side_nella_policy") == true &&
                    QuestCatalogService.FindById(catalog, "side_nella_family_copy")?.prerequisiteIds
                        .Contains("side_nella_policy") == true,
                "Nella's route must preserve the family record, supply a fresh crop and bait, and build a reversible tag sleeve from a real recipe.");
            foreach (var targetId in requiredLandmarks)
                Require(landmarkCatalog?.entries?.Exists(entry => entry != null &&
                            entry.targetId == targetId &&
                            (entry.locationId == "salt_road" || entry.locationId == "salt_lockhouse" ||
                             entry.locationId == "cinderwell_basin")) == true,
                    "Nella's route must place a world marker for " + targetId + ".");
            foreach (var questId in commonQuestIds)
                Require(QuestCatalogService.FindById(catalog, questId) != null,
                    "The blank-name chain must include its common quest step: " + questId);

            for (var routeIndex = 0; routeIndex < routeValues.Length; routeIndex++)
            {
                var selectedValue = routeValues[routeIndex];
                var rejectedIndex = 1 - routeIndex;
                var run = new GameSaveData
                {
                    locationId = "salt_road",
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { "salt_route_handoff", "side_ruth_recall_afterword" },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        encounterCatalog, monsterCatalog, questId, "");

                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_nella_policy", selectedValue);
                var policy = QuestCatalogService.FindById(catalog, "side_nella_policy");
                var selectedCharm = ItemCatalog.Find(branchItemIds[routeIndex]);
                Require(QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        selectedCharm?.category == "equipment" && selectedCharm.equipmentSlot == "charm" &&
                        InventoryService.Count(run, branchItemIds[routeIndex]) == 1 &&
                        InventoryService.Count(run, branchItemIds[rejectedIndex]) == 0 &&
                        InventoryService.TryEquip(run, branchItemIds[routeIndex]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex],
                            "salt_road") &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedIndex],
                            "salt_road"),
                    "Nella's choice must award and equip its selected charm and unlock only that access policy.");
                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, branchQuestIds[routeIndex], "");
                var branchRecords = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(branchRecords.Exists(entry => entry.id == branchCodexIds[routeIndex]) &&
                        !branchRecords.Exists(entry => entry.id == branchCodexIds[rejectedIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "The codex must reveal only Nella's selected disclosure policy.");

                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                Require(QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, "side_nella_afterword", "salt_road"),
                    "The family-access policy and shared afterword must survive save and resume.");
                CompleteSaltRoadMilepostQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    encounterCatalog, monsterCatalog, "side_nella_afterword", "");
                Require(QuestProgressService.IsCompleted(run, "side_nella_afterword") &&
                        QuestProgressService.IsCompleted(run, "side_nella_install") &&
                        InventoryService.Count(run, "pike_tag_sleeve") == 0 &&
                        QuestProgressService.GetStoryFlag(run, policy.choiceFlag) == selectedValue &&
                        QuestProgressService.IsCompleted(run, branchQuestIds[routeIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedIndex]),
                    "The family sleeve must be consumed on installation and both policies must preserve their distinct record.");
            }
        }

        private static void CompleteSaltRoadMilepostQuest(GameSaveData run, QuestCatalogData catalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            EncounterCatalogData encounterCatalog, MonsterCatalogData monsterCatalog, string questId,
            string choiceValue)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && GameLocationService.IsPlayable(quest.locationId),
                "Every milepost step must point to a playable map: " + questId);
            run.locationId = quest.locationId;
            if (!string.IsNullOrEmpty(quest.branchFlag))
                QuestProgressService.SetStoryFlag(run, quest.branchFlag, quest.branchValue);

            QuestChoiceDefinition selectedChoice = null;
            if (quest.choices != null && quest.choices.Count > 0)
            {
                foreach (var choice in quest.choices)
                    if (choice != null && choice.flagValue == choiceValue) selectedChoice = choice;
                Require(selectedChoice != null,
                    "The milepost policy must include the tested route: " + questId + "/" + choiceValue);
                QuestProgressService.SetStoryFlag(run, quest.choiceFlag, selectedChoice.flagValue);
            }

            Require(QuestProgressService.CanAcceptSideQuest(run, catalog, questId, run.locationId) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The milepost graph must unlock and accept each next step: " + questId);
            foreach (var objective in quest.objectives ?? new List<QuestObjectiveDefinition>())
            {
                if (objective.kind == "grow")
                {
                    var plot = farmCatalog.entries.Find(entry => entry != null && entry.locationId == run.locationId &&
                        entry.cropId == objective.targetId);
                    Require(plot != null && InventoryService.Count(run, plot.seedItemId) >= objective.requiredCount,
                        "The Windglass Reed task must provide and use its local crop seed: " + questId);
                    for (var count = 0; count < objective.requiredCount; count++)
                        Require(FarmPlotProgressService.TryPlant(run, plot) &&
                                FarmPlotProgressService.Tick(run, plot.growSeconds) &&
                                FarmPlotProgressService.TryHarvest(run, plot),
                            "The Windglass Reed task must plant, grow and harvest through the farm service.");
                }
                else if (objective.kind == "fish")
                {
                    var spot = fishingCatalog.entries.Find(entry => entry != null && entry.locationId == run.locationId &&
                        entry.catches.Exists(fish => fish != null && fish.itemId == objective.targetId));
                    var roll = FindCatchRoll(spot, objective.targetId);
                    Require(spot != null && roll >= 0 && InventoryService.Count(run, spot.baitItemId) >= objective.requiredCount,
                        "The Salt Road fishing task must have a local table and supplied bait: " + questId);
                    for (var count = 0; count < objective.requiredCount; count++)
                        Require(InventoryService.Remove(run, spot.baitItemId, 1) &&
                                FishingCatalogService.RollCatch(spot, roll) == objective.targetId &&
                                InventoryService.Add(run, objective.targetId, 1) == 1,
                            "A Salt Road catch must consume bait and add the weighted table result to inventory.");
                }
                else if (objective.kind == "defeat")
                {
                    var encounter = encounterCatalog.entries.Find(entry => entry != null &&
                        entry.requiredQuestId == questId && entry.defeatObjectiveTargetId == objective.targetId);
                    var monster = MonsterCatalogService.FindById(monsterCatalog, encounter?.monsterId);
                    var progress = EncounterProgressService.GetOrCreate(run, encounter, monster);
                    Require(encounter != null && encounter.locationId == run.locationId && progress != null &&
                            !progress.defeated,
                        "The Roadglass Sentinel must use its accepted side quest as the encounter gate.");
                    progress.health = 0;
                    progress.defeated = true;
                    ApplyValidationReward(run, encounter.reward);
                }
                else if (objective.kind == "craft")
                {
                    var recipe = recipeCatalog.entries.Find(entry => entry != null &&
                        entry.outputItemId == objective.targetId);
                    Require(recipe != null &&
                            recipe.stationId == "cinderwell_assay_bench" &&
                            CraftingService.TryCraft(run, recipeCatalog, recipe.id, recipe.stationId,
                                out var crafted, out _) && crafted.outputItemId == objective.targetId,
                        "A Salt Road character task must consume its collected materials at Talia's assay bench.");
                }
                else if (objective.kind == "interact" && objective.targetId == "saltroad_beacon_mount")
                {
                    Require(InventoryService.Count(run, "saltroad_beacon_lens") == 1 &&
                            InventoryService.Remove(run, "saltroad_beacon_lens", 1),
                        "Installing the Split-Light Plate must consume the crafted quest item exactly once.");
                }
                else if (objective.kind == "interact" && objective.targetId == "ruth_manifest_lightbox")
                {
                    Require(ItemCatalog.Find("saltroad_beacon_lens")?.category == "quest" &&
                            InventoryService.Count(run, "saltroad_beacon_lens") == 1 &&
                            InventoryService.Remove(run, "saltroad_beacon_lens", 1),
                        "The Lockhouse light-box must consume the crafted Split-Light Plate exactly once.");
                }
                else if (objective.kind == "interact" && objective.targetId == "pike_tag_sleeve_frame")
                {
                    Require(ItemCatalog.Find("pike_tag_sleeve")?.category == "quest" &&
                            InventoryService.Count(run, "pike_tag_sleeve") == 1 &&
                            InventoryService.Remove(run, "pike_tag_sleeve", 1),
                        "The Lockhouse display frame must consume the crafted Tag Sleeve exactly once.");
                }

                Require(QuestProgressService.RecordObjectives(run, catalog, objective.kind, objective.targetId,
                            objective.requiredCount, out var completed) &&
                        completed.Exists(entry => entry.id == questId),
                    "The authored milepost event must complete its quest: " + questId + "/" + objective.id);
                foreach (var completedQuest in completed) ApplyValidationReward(run, completedQuest.reward);
            }

            ApplyValidationReward(run, selectedChoice?.reward);
            Require(QuestProgressService.IsCompleted(run, questId),
                "Every Salt Road milepost step must persist as completed: " + questId);
        }

        private static void CompleteCisternPressureWheelQuest(GameSaveData run, QuestCatalogData catalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, EncounterCatalogData encounterCatalog,
            MonsterCatalogData monsterCatalog, string questId, string choiceValue)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && GameLocationService.IsPlayable(quest.locationId),
                "Every Cistern pressure-wheel step must point to a playable map: " + questId);
            run.locationId = quest.locationId;
            if (!string.IsNullOrEmpty(quest.branchFlag))
                QuestProgressService.SetStoryFlag(run, quest.branchFlag, quest.branchValue);

            QuestChoiceDefinition selectedChoice = null;
            if (quest.choices != null && quest.choices.Count > 0)
            {
                foreach (var choice in quest.choices)
                    if (choice != null && choice.flagValue == choiceValue) selectedChoice = choice;
                Require(selectedChoice != null,
                    "The Cistern pressure-wheel policy must include the tested choice: " + questId + "/" + choiceValue);
                QuestProgressService.SetStoryFlag(run, quest.choiceFlag, selectedChoice.flagValue);
            }

            Require(QuestProgressService.CanAcceptSideQuest(run, catalog, questId, run.locationId) &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "The Cistern pressure-wheel graph must make each next step available: " + questId);
            foreach (var objective in quest.objectives ?? new List<QuestObjectiveDefinition>())
            {
                if (objective.kind == "grow")
                {
                    var plot = farmCatalog.entries.Find(entry => entry != null && entry.locationId == run.locationId &&
                        entry.cropId == objective.targetId);
                    Require(plot != null && plot.id == "cinder_cistern_brineglass_bed" &&
                            FarmPlotProgressService.TryPlant(run, plot) &&
                            FarmPlotProgressService.Tick(run, plot.growSeconds) &&
                            FarmPlotProgressService.TryHarvest(run, plot),
                        "The Brineglass Moss objective must plant, grow and harvest from the real Cistern plot.");
                }
                else if (objective.kind == "defeat")
                {
                    var encounter = encounterCatalog.entries.Find(entry => entry != null &&
                        entry.requiredQuestId == questId && entry.defeatObjectiveTargetId == objective.targetId);
                    var monster = MonsterCatalogService.FindById(monsterCatalog, encounter?.monsterId);
                    var progress = EncounterProgressService.GetOrCreate(run, encounter, monster);
                    Require(encounter != null && encounter.locationId == run.locationId && progress != null &&
                            !progress.defeated,
                        "The pressure Wight must have its gated encounter state before victory is recorded.");
                    progress.health = 0;
                    progress.defeated = true;
                    ApplyValidationReward(run, encounter.reward);
                }
                else if (objective.kind == "craft")
                {
                    var recipe = recipeCatalog.entries.Find(entry => entry != null &&
                        entry.outputItemId == objective.targetId);
                    Require(recipe != null && recipe.stationId == "cinderwell_assay_bench" &&
                            CraftingService.TryCraft(run, recipeCatalog, recipe.id, recipe.stationId,
                                out var crafted, out _) && crafted.outputItemId == objective.targetId,
                        "The filter objective must consume its ingredients at the Cinderwell assay bench.");
                }
                else if (objective.kind == "interact" && objective.targetId == "cinder_filter_housing")
                {
                    Require(InventoryService.Count(run, "cinder_moss_filter") == 1 &&
                            InventoryService.Remove(run, "cinder_moss_filter", 1),
                        "The test housing must consume one crafted membrane only when the filter is installed.");
                }

                Require(QuestProgressService.RecordObjectives(run, catalog, objective.kind, objective.targetId,
                            objective.requiredCount, out var completed) &&
                        completed.Exists(entry => entry.id == questId),
                    "The authored Cistern objective event must complete its quest: " + questId + "/" + objective.id);
                foreach (var completedQuest in completed) ApplyValidationReward(run, completedQuest.reward);
            }

            ApplyValidationReward(run, selectedChoice?.reward);
            Require(QuestProgressService.IsCompleted(run, questId),
                "Every Cistern pressure-wheel quest must persist as completed: " + questId);
        }

        private static void ValidateCharacterSideStoryRoute(QuestCatalogData catalog, CodexCatalogData codexCatalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            string locationId, string prerequisiteId, string[] commonQuestIds, string choiceQuestId,
            string[] choiceValues, string[] branchQuestIds, string afterwordQuestId, string[] choiceItemIds,
            string[] branchCodexIds, string afterwordCodexId)
        {
            for (var routeIndex = 0; routeIndex < choiceValues.Length; routeIndex++)
            {
                var selectedValue = choiceValues[routeIndex];
                var rejectedBranchIndex = routeIndex == 0 ? 1 : 0;
                var run = new GameSaveData
                {
                    locationId = locationId,
                    inventory = new List<InventoryStackData>(),
                    completedQuestIds = new List<string> { prerequisiteId },
                    activeSideQuestIds = new List<string>(),
                    questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                    storyFlags = new List<StoryFlagData>()
                };

                foreach (var questId in commonQuestIds)
                    CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                        questId, "");

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    choiceQuestId, selectedValue);
                Require(QuestProgressService.GetStoryFlag(run,
                            QuestCatalogService.FindById(catalog, choiceQuestId).choiceFlag) == selectedValue &&
                        InventoryService.Count(run, choiceItemIds[routeIndex]) == 1 &&
                        InventoryService.Count(run, choiceItemIds[rejectedBranchIndex]) == 0 &&
                        InventoryService.TryEquip(run, choiceItemIds[routeIndex]) &&
                        QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[routeIndex], locationId) &&
                        !QuestProgressService.CanAcceptSideQuest(run, catalog, branchQuestIds[rejectedBranchIndex],
                            locationId),
                    "Each character choice must equip its own charm and unlock only its selected branch: " +
                    choiceQuestId + "/" + selectedValue);

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    branchQuestIds[routeIndex], "");
                var unlockedAfterBranch = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(unlockedAfterBranch.Exists(entry => entry.id == branchCodexIds[routeIndex]) &&
                        !unlockedAfterBranch.Exists(entry => entry.id == branchCodexIds[rejectedBranchIndex]) &&
                        !QuestProgressService.IsCompleted(run, branchQuestIds[rejectedBranchIndex]),
                    "Each character branch must unlock only its matching field record: " + branchQuestIds[routeIndex]);

                CompleteCharacterSideStoryQuest(run, catalog, recipeCatalog, farmCatalog, fishingCatalog,
                    afterwordQuestId, "");
                run = JsonUtility.FromJson<GameSaveData>(JsonUtility.ToJson(run));
                QuestProgressService.Reconcile(run, catalog);
                var unlockedAfterword = CodexCatalogService.GetUnlocked(codexCatalog, run);
                Require(QuestProgressService.IsCompleted(run, afterwordQuestId) &&
                        unlockedAfterword.Exists(entry => entry.id == afterwordCodexId) &&
                        QuestProgressService.GetStoryFlag(run,
                            QuestCatalogService.FindById(catalog, choiceQuestId).choiceFlag) == selectedValue,
                    "Each character story must converge on its afterword and preserve the chosen policy after save/resume: " +
                    afterwordQuestId);
            }
        }

        private static void CompleteCharacterSideStoryQuest(GameSaveData run, QuestCatalogData catalog,
            RecipeCatalogData recipeCatalog, FarmCatalogData farmCatalog, FishingCatalogData fishingCatalog,
            string questId, string choiceValue)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && quest.locationId == run.locationId &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, questId, run.locationId),
                "A character story must unlock and accept its next regional quest: " + questId);

            QuestChoiceDefinition selectedChoice = null;
            if (quest.choices != null && quest.choices.Count > 0)
            {
                foreach (var choice in quest.choices)
                    if (choice != null && choice.flagValue == choiceValue) selectedChoice = choice;
                Require(selectedChoice != null,
                    "The character story must offer the tested policy value: " + questId + "/" + choiceValue);
                QuestProgressService.SetStoryFlag(run, quest.choiceFlag, selectedChoice.flagValue);
            }

            foreach (var objective in quest.objectives ?? new List<QuestObjectiveDefinition>())
            {
                if (objective.kind == "grow")
                {
                    var plot = farmCatalog.entries.Find(entry => entry != null && entry.locationId == run.locationId &&
                        entry.cropId == objective.targetId);
                    Require(plot != null, "A character crop objective must have a local farm plot: " + questId);
                    for (var count = 0; count < objective.requiredCount; count++)
                        Require(FarmPlotProgressService.TryPlant(run, plot) &&
                                FarmPlotProgressService.Tick(run, plot.growSeconds) &&
                                FarmPlotProgressService.TryHarvest(run, plot),
                            "A character crop objective must use its offered seed and a real harvest: " + questId);
                }
                else if (objective.kind == "fish")
                {
                    var spot = fishingCatalog.entries.Find(entry => entry != null && entry.locationId == run.locationId &&
                        entry.catches.Exists(fish => fish != null && fish.itemId == objective.targetId));
                    var roll = FindCatchRoll(spot, objective.targetId);
                    if (questId == "side_choir_signal_sample" || questId == "side_elara_garden_fish" ||
                        questId == "side_june_pantry_fish" || questId == "side_oren_seed_tin_perch" ||
                        questId == "side_crownfall_shared_table_minnow" ||
                        questId == "side_capacity_farwake" || questId == "side_capacity_whisper" ||
                        questId == "side_capacity_blackreed")
                    {
                        Require(spot != null && InventoryService.Count(run, spot.baitItemId) >= objective.requiredCount,
                            "A character fishing survey must supply bait for its real regional catch: " + questId);
                        for (var count = 0; count < objective.requiredCount; count++)
                            Require(InventoryService.Remove(run, spot.baitItemId, 1),
                                "A character fishing survey must consume bait for each catch: " + questId);
                    }
                    Require(spot != null && roll >= 0 &&
                            FishingCatalogService.RollCatch(spot, roll) == objective.targetId &&
                            InventoryService.Add(run, objective.targetId, objective.requiredCount) ==
                            objective.requiredCount,
                        "A character fishing objective must catch its named regional fish: " + questId);
                }
                else if (objective.kind == "craft")
                {
                    var recipe = recipeCatalog.entries.Find(entry => entry != null &&
                        entry.outputItemId == objective.targetId);
                    Require(recipe != null, "A character crafting objective must have an authored recipe: " + questId);
                    for (var count = 0; count < objective.requiredCount; count++)
                        Require(CraftingService.TryCraft(run, recipeCatalog, recipe.id, recipe.stationId,
                                    out var craftedRecipe, out _) && craftedRecipe.outputItemId == objective.targetId,
                            "A character crafting objective must consume its real ingredients and make its output: " +
                            questId);
                }
                else if (objective.kind == "interact" && objective.targetId == "choir_signal_housing")
                {
                    Require(ItemCatalog.Find("choir_pulse_brace")?.category == "quest" &&
                            InventoryService.Count(run, "choir_pulse_brace") == 1 &&
                            InventoryService.Remove(run, "choir_pulse_brace", 1),
                        "The warning-frame interaction must consume the crafted pulse brace exactly once.");
                }
                else if (objective.kind == "interact" && objective.targetId == "elara_garden_rain_housing")
                {
                    Require(ItemCatalog.Find("dawnkeep_runoff_clip")?.category == "quest" &&
                            InventoryService.Count(run, "dawnkeep_runoff_clip") == 1 &&
                            InventoryService.Remove(run, "dawnkeep_runoff_clip", 1),
                        "The Dawnkeep gutter-frame interaction must consume the crafted runoff clip exactly once.");
                }
                else if (objective.kind == "interact" &&
                         (objective.targetId == "june_common_table" || objective.targetId == "june_departure_crate"))
                {
                    Require(InventoryService.Count(run, "cinderwell_stonepot_broth") >= 1 &&
                            InventoryService.Remove(run, "cinderwell_stonepot_broth", 1),
                        "Serving or packing the first bowl must consume exactly one crafted meal.");
                }
                else if (objective.kind == "interact" && objective.targetId == "crownfall_open_meal_table")
                {
                    Require(ItemCatalog.Find("crownfall_starlit_pottage")?.category == "consumable" &&
                            InventoryService.Count(run, "crownfall_starlit_pottage") == 1 &&
                            InventoryService.Remove(run, "crownfall_starlit_pottage", 1),
                        "The Crownfall open table must consume the actual cooked pottage exactly once.");
                }

                Require(QuestProgressService.RecordObjectives(run, catalog, objective.kind, objective.targetId,
                            objective.requiredCount, out _),
                    "A character side quest must advance from its authored gameplay event: " + questId + "/" +
                    objective.id);
            }

            Require(QuestProgressService.IsCompleted(run, questId),
                "All character side-story objectives must complete their owning quest: " + questId);
            ApplyValidationReward(run, quest.reward);
            ApplyValidationReward(run, selectedChoice?.reward);
        }

        private static float FindCatchRoll(FishingSpotDefinition spot, string itemId)
        {
            if (spot?.catches == null) return -1;
            var totalWeight = 0f;
            foreach (var fish in spot.catches) totalWeight += fish.weight;
            var passedWeight = 0f;
            foreach (var fish in spot.catches)
            {
                if (fish.itemId == itemId) return (passedWeight + fish.weight * 0.5f) / totalWeight;
                passedWeight += fish.weight;
            }
            return -1;
        }

        private static void ValidateGreenwakeSeedAccessRoutes(QuestCatalogData catalog)
        {
            ValidateGreenwakeSeedAccessRoute(catalog, "public", new[]
            {
                "side_greenwake_open_tallies", "side_greenwake_public_appeal"
            });
            ValidateGreenwakeSeedAccessRoute(catalog, "restricted", new[]
            {
                "side_greenwake_household_copies", "side_greenwake_private_corrections"
            });
        }

        private static void ValidateGreenwakeSeedAccessRoute(QuestCatalogData catalog, string selectedValue,
            string[] routeQuestIds)
        {
            var run = new GameSaveData
            {
                locationId = "greenwake_refuge",
                completedQuestIds = new List<string> { "champion_star_map" },
                activeSideQuestIds = new List<string>(),
                questObjectiveProgress = new List<QuestObjectiveProgressData>(),
                storyFlags = new List<StoryFlagData>()
            };
            var commonQuestIds = new[]
            {
                "side_greenwake_seed_calendar", "side_greenwake_root_readings",
                "side_greenwake_refusal_rota", "side_greenwake_access_choice"
            };
            foreach (var questId in commonQuestIds)
                CompleteGreenwakeSideQuestForValidation(run, catalog, questId, selectedValue);
            foreach (var questId in routeQuestIds)
                CompleteGreenwakeSideQuestForValidation(run, catalog, questId, selectedValue);
            CompleteGreenwakeSideQuestForValidation(run, catalog, "side_greenwake_seed_review", selectedValue);
            CompleteGreenwakeSideQuestForValidation(run, catalog, "side_greenwake_afterword", selectedValue);

            var endingQuest = QuestCatalogService.FindById(catalog, "side_greenwake_afterword");
            Require(QuestProgressService.IsCompleted(run, "side_greenwake_afterword") &&
                    endingQuest?.reward?.items != null && endingQuest.reward.items.Exists(item =>
                        item != null && item.itemId == "greenwake_open_sowing_charm" && item.quantity == 1) &&
                    QuestProgressService.GetStoryFlag(run, "greenwake_seed_access") == selectedValue,
                "Each Greenwake seed-record route must reach the shared afterword and preserve its choice.");
        }

        private static void CompleteGreenwakeSideQuestForValidation(GameSaveData run, QuestCatalogData catalog,
            string questId, string selectedValue)
        {
            var quest = QuestCatalogService.FindById(catalog, questId);
            Require(quest != null && quest.locationId == "greenwake_refuge" &&
                    QuestProgressService.TryAcceptSideQuest(run, catalog, questId, "greenwake_refuge"),
                "Greenwake seed-record progression must accept the next available side quest: " + questId);
            if (quest.choices != null && quest.choices.Count > 0)
            {
                QuestChoiceDefinition selectedChoice = null;
                foreach (var candidate in quest.choices)
                    if (candidate != null && candidate.flagValue == selectedValue) selectedChoice = candidate;
                Require(selectedChoice != null,
                    "The Greenwake seed-record choice must include the selected route: " + selectedValue);
                QuestProgressService.SetStoryFlag(run, quest.choiceFlag, selectedChoice.flagValue);
            }
            foreach (var objective in quest.objectives)
                Require(QuestProgressService.RecordObjective(run, catalog, objective.kind, objective.targetId,
                            objective.requiredCount, out _),
                    "Greenwake objective must be recordable by its authored kind and target: " + questId + "/" + objective.id);
            Require(QuestProgressService.IsCompleted(run, questId),
                "All Greenwake seed-record objectives must complete their owning quest: " + questId);
        }

        private static void Require(bool condition, string message)
        {
            if (!condition) throw new System.InvalidOperationException("Inventory validation failed: " + message);
        }

        private static void ValidatePlayerWalkAtlas()
        {
            const string path = "Assets/Resources/Art/rowan_hale_walk.png";
            var importer = AssetImporter.GetAtPath(path) as TextureImporter;
            var atlas = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
            Require(atlas != null && importer != null, "Rowan's four-direction walk atlas must be imported.");
            Require(importer.isReadable && !importer.mipmapEnabled && importer.filterMode == FilterMode.Point &&
                    importer.alphaIsTransparency,
                "Rowan's walk atlas must be readable, point-filtered, mipmap-free, and retain transparency.");

            var pixels = atlas.GetPixels32();
            for (var rowFromTop = 0; rowFromTop < 4; rowFromTop++)
            {
                var yMin = atlas.height - Mathf.RoundToInt(atlas.height * (rowFromTop + 1) / 4f);
                var yMax = atlas.height - Mathf.RoundToInt(atlas.height * rowFromTop / 4f);
                for (var column = 0; column < 4; column++)
                {
                    var xMin = Mathf.RoundToInt(atlas.width * column / 4f);
                    var xMax = Mathf.RoundToInt(atlas.width * (column + 1) / 4f);
                    var opaquePixels = 0;
                    for (var y = yMin; y < yMax; y++)
                    for (var x = xMin; x < xMax; x++)
                        if (pixels[y * atlas.width + x].a >= 16) opaquePixels++;

                    Require(opaquePixels > 0,
                        "Every cell in Rowan's walk atlas must contain a visible animation frame.");
                }
            }
        }

        private static void ValidateDialoguePortraitAssets()
        {
            ConfigureDialoguePortraitImporters();
            var portraits = new[]
            {
                new { Id = "rowan_hale", Width = 1254, Height = 1254 },
                new { Id = "mira_cole", Width = 1024, Height = 1536 },
                new { Id = "elara_wren", Width = 1254, Height = 1254 },
                new { Id = "evelyn_hart", Width = 1024, Height = 1536 },
                new { Id = "jace_morrow", Width = 1175, Height = 1338 },
                new { Id = "nia_porter", Width = 1024, Height = 1536 },
                new { Id = "ruth_calder", Width = 1024, Height = 1536 },
                new { Id = "mara_bell", Width = 1024, Height = 1536 },
                new { Id = "ada_sloane", Width = 1024, Height = 1536 }
            };
            foreach (var expected in portraits)
            {
                var path = "Assets/Resources/Art/" + expected.Id + ".png";
                var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                Require(texture != null && texture.width == expected.Width && texture.height == expected.Height &&
                        importer != null && importer.alphaIsTransparency && !importer.mipmapEnabled &&
                        importer.filterMode == FilterMode.Point &&
                        importer.textureCompression == TextureImporterCompression.Uncompressed,
                    "Every recurring campaign speaker must have an imported transparent pixel-art dialogue portrait: " +
                    expected.Id + ".");
            }
        }

        private static void ConfigureDialoguePortraitImporters()
        {
            var paths = new[]
            {
                "Assets/Resources/Art/rowan_hale.png",
                "Assets/Resources/Art/mira_cole.png",
                "Assets/Resources/Art/elara_wren.png",
                "Assets/Resources/Art/evelyn_hart.png",
                "Assets/Resources/Art/jace_morrow.png",
                "Assets/Resources/Art/nia_porter.png",
                "Assets/Resources/Art/ruth_calder.png",
                "Assets/Resources/Art/mara_bell.png",
                "Assets/Resources/Art/ada_sloane.png"
            };
            foreach (var path in paths)
            {
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer == null) continue;
                var changed = importer.textureType != TextureImporterType.Default || importer.mipmapEnabled ||
                              importer.filterMode != FilterMode.Point || importer.wrapMode != TextureWrapMode.Clamp ||
                              importer.isReadable || importer.textureCompression != TextureImporterCompression.Uncompressed ||
                              !importer.alphaIsTransparency || importer.maxTextureSize != 2048 ||
                              importer.npotScale != TextureImporterNPOTScale.None;
                if (!changed) continue;
                importer.textureType = TextureImporterType.Default;
                importer.mipmapEnabled = false;
                importer.filterMode = FilterMode.Point;
                importer.wrapMode = TextureWrapMode.Clamp;
                importer.isReadable = false;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.alphaIsTransparency = true;
                importer.maxTextureSize = 2048;
                importer.npotScale = TextureImporterNPOTScale.None;
                importer.SaveAndReimport();
            }
        }

        private static void ValidateAldenAnimationAtlases()
        {
            var atlases = new[]
            {
                new { Path = "Assets/Resources/Art/AldenKnight/Idle.png", Width = 1860, Height = 1440 },
                new { Path = "Assets/Resources/Art/AldenKnight/Run.png", Width = 1860, Height = 1440 },
                new { Path = "Assets/Resources/Art/AldenKnight/Attack.png", Width = 1860, Height = 1152 },
                new { Path = "Assets/Resources/Art/AldenKnight/Hit.png", Width = 1488, Height = 1152 },
                new { Path = "Assets/Resources/Art/AldenKnight/Death.png", Width = 1860, Height = 1440 }
            };
            ConfigureAldenAnimationImporters();
            foreach (var expected in atlases)
            {
                var atlas = AssetDatabase.LoadAssetAtPath<Texture2D>(expected.Path);
                Require(atlas != null && atlas.width == expected.Width && atlas.height == expected.Height,
                    "Alden's CC0 knight animation atlas must import at its authored dimensions: " + expected.Path);
            }
        }

        private static void ConfigureAldenAnimationImporters()
        {
            var paths = new[]
            {
                "Assets/Resources/Art/AldenKnight/Idle.png",
                "Assets/Resources/Art/AldenKnight/Run.png",
                "Assets/Resources/Art/AldenKnight/Attack.png",
                "Assets/Resources/Art/AldenKnight/Hit.png",
                "Assets/Resources/Art/AldenKnight/Death.png"
            };
            foreach (var path in paths)
            {
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer == null) continue;
                var changed = importer.textureType != TextureImporterType.Default || importer.mipmapEnabled ||
                              importer.filterMode != FilterMode.Point || importer.wrapMode != TextureWrapMode.Clamp ||
                              importer.isReadable || importer.npotScale != TextureImporterNPOTScale.None ||
                              importer.textureCompression != TextureImporterCompression.Uncompressed ||
                              !importer.alphaIsTransparency || importer.maxTextureSize != 2048;
                if (!changed) continue;
                importer.textureType = TextureImporterType.Default;
                importer.mipmapEnabled = false;
                importer.filterMode = FilterMode.Point;
                importer.wrapMode = TextureWrapMode.Clamp;
                importer.isReadable = false;
                importer.npotScale = TextureImporterNPOTScale.None;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.alphaIsTransparency = true;
                importer.maxTextureSize = 2048;
                importer.SaveAndReimport();
            }
        }

        private static void ValidateRegionalMusicTracks()
        {
            var tracks = new[]
            {
                "rpgchip01_title_screen", "rpgchip02_bittersweet_story", "rpgchip03_town",
                "rpgchip04_in_the_royal_court", "rpgchip05_pavane", "rpgchip06_dungeon",
                "rpgchip07_the_shrine_of_mysteries", "rpgchip08_castle_on_the_mountain",
                "rpgchip09_rainy_streets", "rpgchip10_fountain_of_the_fairies",
                "rpgchip11_airship", "rpgchip12_the_evil_one", "rpgchip13_battle_1",
                "rpgchip14_battle_2", "rpgchip15_game_over"
            };
            ConfigureAudioImporters();
            foreach (var track in tracks)
            {
                var path = "Assets/Resources/Audio/Music/" + track + ".ogg";
                var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(path);
                var importer = AssetImporter.GetAtPath(path) as AudioImporter;
                Require(clip != null && clip.length >= 8f && importer != null &&
                        importer.defaultSampleSettings.loadType == AudioClipLoadType.Streaming,
                    "Each CC0 OGA music cue must import as a valid streamed audio clip: " + track);
            }
        }

        private static void ValidateFieldAudioResources()
        {
            var paths = new[]
            {
                "Assets/Resources/Audio/Ambience/night_crickets.wav",
                "Assets/Resources/Audio/Ambience/ticking_clock.wav",
                "Assets/Resources/Audio/Ambience/vistula_river.mp3",
                "Assets/Resources/Audio/Ambience/park_ambience_birds.wav",
                "Assets/Resources/Audio/Ambience/park_ambience_river.wav",
                "Assets/Resources/Audio/Ambience/park_ambience_wind.wav",
                "Assets/Resources/Audio/SFX/Fishing/water.ogg",
                "Assets/Resources/Audio/SFX/Fishing/bubbles.ogg",
                "Assets/Resources/Audio/SFX/Fishing/swim.ogg",
                "Assets/Resources/Audio/SFX/Fishing/waterReentry.ogg",
                "Assets/Resources/Audio/World/grass_footstep_1.wav",
                "Assets/Resources/Audio/World/grass_footstep_2.wav",
                "Assets/Resources/Audio/World/grass_footstep_3.wav",
                "Assets/Resources/Audio/World/stone_footstep_1.wav",
                "Assets/Resources/Audio/World/stone_footstep_2.wav",
                "Assets/Resources/Audio/World/stone_footstep_3.wav",
                "Assets/Resources/Audio/World/stone_footstep_4.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_04.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_06.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/potion_bottle.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/armor_light.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/cloth.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/metal_ringing.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_06.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_09.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_10.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_04.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_08.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_03.wav"
            };
            ConfigureAudioImporters();
            foreach (var path in paths)
            {
                var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(path);
                var importer = AssetImporter.GetAtPath(path) as AudioImporter;
                var expectedLoadType = path.StartsWith("Assets/Resources/Audio/Ambience/",
                    System.StringComparison.Ordinal) ? AudioClipLoadType.Streaming : AudioClipLoadType.DecompressOnLoad;
                var fullFidelityParkAmbience = IsFullFidelityParkAmbience(path);
                var expectedFormat = fullFidelityParkAmbience
                    ? AudioCompressionFormat.PCM : AudioCompressionFormat.Vorbis;
                var androidSettings = importer == null
                    ? default(AudioImporterSampleSettings)
                    : importer.GetOverrideSampleSettings(BuildTargetGroup.Android);
                Require(clip != null && clip.length > 0.04f && importer != null &&
                        importer.defaultSampleSettings.compressionFormat == expectedFormat &&
                        importer.defaultSampleSettings.loadType == expectedLoadType &&
                        (!fullFidelityParkAmbience ||
                         (clip.length > 120f && clip.frequency == 48000 && clip.channels == 2 &&
                          importer.defaultSampleSettings.sampleRateSetting == AudioSampleRateSetting.PreserveSampleRate)) &&
                        (!fullFidelityParkAmbience ||
                         (importer.ContainsSampleSettingsOverride(BuildTargetGroup.Android) &&
                          androidSettings.compressionFormat == AudioCompressionFormat.PCM &&
                          androidSettings.loadType == AudioClipLoadType.Streaming &&
                          androidSettings.sampleRateSetting == AudioSampleRateSetting.PreserveSampleRate)),
                    "Reviewed CC0 audio samples must import with their intended load and compression mode: " + path);
            }
        }

        private static bool IsFullFidelityParkAmbience(string path)
        {
            return path == "Assets/Resources/Audio/Ambience/park_ambience_birds.wav" ||
                   path == "Assets/Resources/Audio/Ambience/park_ambience_river.wav" ||
                   path == "Assets/Resources/Audio/Ambience/park_ambience_wind.wav";
        }

        [MenuItem("Ashen Oath/Build Main Scene")]
        public static void CreateMainScene()
        {
            ConfigurePixelArtImporters();
            ConfigureAudioImporters();
            var scenesDirectory = Path.GetDirectoryName(MainScenePath);
            if (!string.IsNullOrEmpty(scenesDirectory)) Directory.CreateDirectory(scenesDirectory);

            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var root = new GameObject("Ashen Oath — Runtime");
            root.AddComponent<GameRuntime>();
            EditorSceneManager.SaveScene(scene, MainScenePath);

            EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(MainScenePath, true) };
            PlayerSettings.productName = "Ashen Oath";
            PlayerSettings.companyName = "Ashen Oath Studio";
            PlayerSettings.bundleVersion = "0.1.0";
            PlayerSettings.defaultScreenWidth = 1920;
            PlayerSettings.defaultScreenHeight = 1080;
            PlayerSettings.SetApplicationIdentifier(NamedBuildTarget.Android, "com.ashen.oath");
            AssetDatabase.SaveAssets();
            Debug.Log("Created " + MainScenePath + " and registered it in Build Settings.");
        }

        [MenuItem("Ashen Oath/Build Android Offline Preview APK")]
        public static void BuildAndroidOfflinePreviewApk()
        {
            if (!EditorUserBuildSettings.SwitchActiveBuildTarget(BuildTargetGroup.Android, BuildTarget.Android))
                throw new System.InvalidOperationException("Could not switch the active build target to Android.");

            ConfigurePixelArtImporters();
            ConfigureAudioImporters();
            var outputDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Build");
            Directory.CreateDirectory(outputDirectory);
            var scenes = System.Array.FindAll(EditorBuildSettings.scenes, scene => scene.enabled);
            var options = new BuildPlayerOptions
            {
                scenes = System.Array.ConvertAll(scenes, scene => scene.path),
                locationPathName = Path.Combine(outputDirectory, "AshenOath-Offline-Preview.apk"),
                target = BuildTarget.Android,
                options = BuildOptions.None
            };

            var report = BuildPipeline.BuildPlayer(options);
            if (report.summary.result != BuildResult.Succeeded)
                throw new System.InvalidOperationException("Android build failed: " + report.summary.result);

            var apkFile = new FileInfo(report.summary.outputPath);
            Debug.Log("Android offline preview APK built: " + report.summary.outputPath + " (" +
                      apkFile.Length + " bytes on disk). ");
        }

        private static void ConfigurePixelArtImporters()
        {
            ConfigureDialoguePortraitImporters();
            var paths = new[]
            {
                "Assets/Resources/Art/ashfall_village.png",
                "Assets/Resources/Art/rowan_hale.png",
                "Assets/Resources/Art/rowan_hale_walk.png",
                "Assets/Resources/Art/mira_cole.png",
                "Assets/Resources/Art/ash_warg.png",
                "Assets/Resources/Art/ash_warg_lunge.png",
                "Assets/Resources/Art/dawnkeep_outpost.png",
                "Assets/Resources/Art/dawnkeep_barracks.png",
                "Assets/Resources/Art/cinderwell_basin.png",
                "Assets/Resources/Art/salt_road.png",
                "Assets/Resources/Art/choir_beneath_lake.png",
                "Assets/Resources/Art/greenwake_refuge.png",
                "Assets/Resources/Art/veil_archive.png",
                "Assets/Resources/Art/last_oath_reach.png",
                "Assets/Resources/Art/elara_wren.png",
                "Assets/Resources/Art/AldenKnight/Idle.png",
                "Assets/Resources/Art/AldenKnight/Run.png",
                "Assets/Resources/Art/AldenKnight/Attack.png",
                "Assets/Resources/Art/AldenKnight/Hit.png",
                "Assets/Resources/Art/AldenKnight/Death.png"
            };

            foreach (var path in paths)
            {
                var importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer == null) continue;
                importer.textureType = TextureImporterType.Default;
                importer.mipmapEnabled = false;
                importer.filterMode = FilterMode.Point;
                importer.wrapMode = TextureWrapMode.Clamp;
                importer.isReadable = path == "Assets/Resources/Art/rowan_hale_walk.png";
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.alphaIsTransparency = path != "Assets/Resources/Art/ashfall_village.png" &&
                                              path != "Assets/Resources/Art/dawnkeep_barracks.png";
                if (path.StartsWith("Assets/Resources/Art/AldenKnight/", System.StringComparison.Ordinal))
                    importer.npotScale = TextureImporterNPOTScale.None;
                importer.maxTextureSize = 2048;
                importer.SaveAndReimport();
            }
        }

        private static void ConfigureAudioImporters()
        {
            var paths = new[]
            {
                "Assets/Resources/Audio/exploration_theme.ogg",
                "Assets/Resources/Audio/battle_theme.ogg",
                "Assets/Resources/Audio/Music/rpgchip01_title_screen.ogg",
                "Assets/Resources/Audio/Music/rpgchip02_bittersweet_story.ogg",
                "Assets/Resources/Audio/Music/rpgchip03_town.ogg",
                "Assets/Resources/Audio/Music/rpgchip04_in_the_royal_court.ogg",
                "Assets/Resources/Audio/Music/rpgchip05_pavane.ogg",
                "Assets/Resources/Audio/Music/rpgchip06_dungeon.ogg",
                "Assets/Resources/Audio/Music/rpgchip07_the_shrine_of_mysteries.ogg",
                "Assets/Resources/Audio/Music/rpgchip08_castle_on_the_mountain.ogg",
                "Assets/Resources/Audio/Music/rpgchip09_rainy_streets.ogg",
                "Assets/Resources/Audio/Music/rpgchip10_fountain_of_the_fairies.ogg",
                "Assets/Resources/Audio/Music/rpgchip11_airship.ogg",
                "Assets/Resources/Audio/Music/rpgchip12_the_evil_one.ogg",
                "Assets/Resources/Audio/Music/rpgchip13_battle_1.ogg",
                "Assets/Resources/Audio/Music/rpgchip14_battle_2.ogg",
                "Assets/Resources/Audio/Music/rpgchip15_game_over.ogg",
                "Assets/Resources/Audio/Ambience/night_crickets.wav",
                "Assets/Resources/Audio/Ambience/ticking_clock.wav",
                "Assets/Resources/Audio/Ambience/vistula_river.mp3",
                "Assets/Resources/Audio/Ambience/park_ambience_birds.wav",
                "Assets/Resources/Audio/Ambience/park_ambience_river.wav",
                "Assets/Resources/Audio/Ambience/park_ambience_wind.wav",
                "Assets/Resources/Audio/World/grass_footstep_1.wav",
                "Assets/Resources/Audio/World/grass_footstep_2.wav",
                "Assets/Resources/Audio/World/grass_footstep_3.wav",
                "Assets/Resources/Audio/World/stone_footstep_1.wav",
                "Assets/Resources/Audio/World/stone_footstep_2.wav",
                "Assets/Resources/Audio/World/stone_footstep_3.wav",
                "Assets/Resources/Audio/World/stone_footstep_4.wav",
                "Assets/Resources/Audio/SFX/player_attack.ogg",
                "Assets/Resources/Audio/SFX/player_impact.ogg",
                "Assets/Resources/Audio/SFX/loot_coins.ogg",
                "Assets/Resources/Audio/SFX/Fishing/water.ogg",
                "Assets/Resources/Audio/SFX/Fishing/bubbles.ogg",
                "Assets/Resources/Audio/SFX/Fishing/swim.ogg",
                "Assets/Resources/Audio/SFX/Fishing/waterReentry.ogg",
                "Assets/Resources/Audio/SFX/footstep_1.ogg",
                "Assets/Resources/Audio/SFX/footstep_2.ogg",
                "Assets/Resources/Audio/SFX/footstep_3.ogg",
                "Assets/Resources/Audio/SFX/footstep_4.ogg",
                "Assets/Resources/Audio/SFX/footstep_5.ogg",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/swing_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Battle/sword_draw_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_04.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Interface/interface_06.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/potion_bottle.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/armor_light.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/cloth.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Items/metal_ringing.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_06.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beast_09.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/giant_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_03.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/ogre_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_05.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/shade_10.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_04.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/slime_08.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_01.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_02.wav",
                "Assets/Resources/Audio/SFX/RpgPack/Creatures/beetle_03.wav"
            };

            foreach (var path in paths)
            {
                var importer = AssetImporter.GetAtPath(path) as AudioImporter;
                if (importer == null) continue;
                var isMusic = path == "Assets/Resources/Audio/exploration_theme.ogg" ||
                              path == "Assets/Resources/Audio/battle_theme.ogg" ||
                              path.StartsWith("Assets/Resources/Audio/Music/", System.StringComparison.Ordinal) ||
                              path.StartsWith("Assets/Resources/Audio/Ambience/", System.StringComparison.Ordinal);
                var fullFidelityParkAmbience = IsFullFidelityParkAmbience(path);
                var isLongAmbient = path == "Assets/Resources/Audio/Ambience/vistula_river.mp3" ||
                                    fullFidelityParkAmbience;
                var targetQuality = fullFidelityParkAmbience ? 1f :
                    path == "Assets/Resources/Audio/Ambience/vistula_river.mp3" ? 0.8f : 0.7f;
                var targetFormat = fullFidelityParkAmbience
                    ? AudioCompressionFormat.PCM : AudioCompressionFormat.Vorbis;
                var settings = importer.defaultSampleSettings;
                var loadType = isMusic ? AudioClipLoadType.Streaming : AudioClipLoadType.DecompressOnLoad;
                var changed = settings.loadType != loadType ||
                              settings.compressionFormat != targetFormat ||
                              !Mathf.Approximately(settings.quality, targetQuality) ||
                              !settings.preloadAudioData || importer.loadInBackground != isLongAmbient ||
                              importer.forceToMono;
                var androidSettings = importer.GetOverrideSampleSettings(BuildTargetGroup.Android);
                var androidOverrideChanged = fullFidelityParkAmbience &&
                    (!importer.ContainsSampleSettingsOverride(BuildTargetGroup.Android) ||
                     androidSettings.loadType != AudioClipLoadType.Streaming ||
                     androidSettings.compressionFormat != AudioCompressionFormat.PCM ||
                     androidSettings.sampleRateSetting != AudioSampleRateSetting.PreserveSampleRate ||
                     !Mathf.Approximately(androidSettings.quality, targetQuality));
                if (!changed && !androidOverrideChanged) continue;

                settings.loadType = loadType;
                settings.compressionFormat = targetFormat;
                settings.quality = targetQuality;
                if (fullFidelityParkAmbience)
                    settings.sampleRateSetting = AudioSampleRateSetting.PreserveSampleRate;
                settings.preloadAudioData = true;
                importer.defaultSampleSettings = settings;
                importer.forceToMono = false;
                importer.loadInBackground = isLongAmbient;
                if (fullFidelityParkAmbience &&
                    !importer.SetOverrideSampleSettings(BuildTargetGroup.Android, settings))
                    throw new System.InvalidOperationException("Could not preserve PCM streaming for Android ambience: " + path);
                importer.SaveAndReimport();
            }
        }
    }
}
