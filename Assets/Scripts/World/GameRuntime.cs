using System;
using System.Collections;
using System.Collections.Generic;
using AshenOath.Core;
using AshenOath.UI;
using UnityEngine;

namespace AshenOath.World
{
    public sealed class GameRuntime : MonoBehaviour
    {
        private enum PlayMode { Exploring, Dialogue, Combat, Fishing, Inventory, Ending }
        private enum ActorKind { Mira, SurvivorWitness, SealClue, CaptainAlden, Encounter, FishingSpot, FarmPlot, Workstation, RoadGate, ElaraWren, DawnkeepRoster, SisterJune, TaliaMercer, OrenBell, StoryLandmark, SaltRoadWitness }
        private enum MonsterAttackPhase { ClosingIn, Telegraph, Lunging, Recovery }
        private enum EnemyVisualAnimation { None, Idle, Run, Attack, Hit }

        private sealed class AldenAnimationSet
        {
            public Sprite[] Idle;
            public Sprite[] Run;
            public Sprite[] Attack;
            public Sprite[] Hit;
            public Sprite[] Death;
        }

        private sealed class WorldActor
        {
            public string Name;
            public ActorKind Kind;
            public Transform Transform;
            public Vector3 BasePosition;
            public EncounterDefinition Encounter;
            public MonsterDefinition Monster;
            public EncounterProgressData Progress;
            public Sprite IdleSprite;
            public Sprite LungeSprite;
            public Sprite[] IdleAnimationFrames;
            public Sprite[] RunAnimationFrames;
            public Sprite[] AttackAnimationFrames;
            public Sprite[] HitAnimationFrames;
            public Sprite[] DeathAnimationFrames;
            public FishingSpotDefinition FishingSpot;
            public FarmPlotDefinition FarmPlot;
            public string WorkstationId;
            public SpriteRenderer Renderer;
            public Sprite FarmBedSprite;
            public Sprite CropGrowingSprite;
            public Sprite CropReadySprite;
            public string DestinationLocationId;
            public Vector2 DestinationPosition;
            public string RequiredQuestId;
            public string ObjectiveTargetId;
            public string InteractionDialogueId;
            public bool RequiresAcceptedSideQuest;
            public bool IsQuestCatalogLandmark;
        }

        private const int MaxHealth = 48;
        private const float MoveSpeed = 3.3f;
        private const float InteractRange = 2.4f;

        private static GameRuntime instance;
        private static AldenAnimationSet aldenAnimationSet;
        private readonly List<WorldActor> actors = new List<WorldActor>();
        private readonly System.Random sfxRandom = new System.Random();
        private GameSaveData save;
        private QuestCatalogData questCatalog;
        private QuestLandmarkCatalogData questLandmarkCatalog;
        private CodexCatalogData codexCatalog;
        private DialogueCatalogData dialogueCatalog;
        private MonsterCatalogData monsterCatalog;
        private EncounterCatalogData encounterCatalog;
        private FishingCatalogData fishingCatalog;
        private RecipeCatalogData recipeCatalog;
        private FarmCatalogData farmCatalog;
        private MonsterDefinition activeMonsterDefinition;
        private EncounterDefinition activeEncounterDefinition;
        private EncounterProgressData activeEncounterProgress;
        private GameHud hud;
        private AudioSource musicSource;
        private AudioSource effectsSource;
        private AudioSource ambienceSource;
        private AudioClip explorationTheme;
        private AudioClip battleTheme;
        private AudioClip playerAttackSfx;
        private AudioClip playerImpactSfx;
        private AudioClip lootCoinsSfx;
        private AudioClip[] attackSwingSfx;
        private AudioClip[] swordDrawSfx;
        private AudioClip[] interfaceSfx;
        private AudioClip potionBottleSfx;
        private AudioClip[] armorEquipSfx;
        private AudioClip metalEquipSfx;
        private AudioClip[] beastVocalSfx;
        private AudioClip[] giantVocalSfx;
        private AudioClip[] ogreVocalSfx;
        private AudioClip[] shadeVocalSfx;
        private AudioClip[] slimeVocalSfx;
        private AudioClip[] beetleVocalSfx;
        private AudioClip[] footstepSfx;
        private AudioClip[] grassFootstepSfx;
        private AudioClip[] stoneFootstepSfx;
        private AudioClip nightCricketsAmbience;
        private AudioClip tickingClockAmbience;
        private AudioClip riverAmbience;
        private AudioClip parkBirdsAmbience;
        private AudioClip parkRiverAmbience;
        private AudioClip parkWindAmbience;
        private AudioClip fishingCastSfx;
        private AudioClip fishingBiteSfx;
        private AudioClip fishingCatchSfx;
        private AudioClip fishingMissSfx;
        private Sprite telegraphRingVfx;
        private Sprite hitSlashVfx;
        private Sprite dodgeFlashVfx;
        private Sprite rewardGlintVfx;
        private Sprite healingBurstVfx;
        private Sprite craftingFlareVfx;
        private Sprite harvestGlintVfx;
        private Sprite fishingRippleVfx;
        private Sprite cadetFlowCharmIcon;
        private Sprite cisternLedgerClaspIcon;
        private Sprite outerwakeFieldCompassIcon;
        private Sprite greenwakeOpenSowingCharmIcon;
        private readonly Dictionary<string, Sprite> fieldGearIconCache = new Dictionary<string, Sprite>();
        private Sprite lineTelegraphSprite;
        private Transform worldRoot;
        private Transform player;
        private SpriteRenderer playerRenderer;
        private Sprite[][] playerWalkFrames;
        private int playerFacingRow;
        private int playerWalkFrame;
        private float playerWalkFrameTimer;
        private Transform enemyRoot;
        private SpriteRenderer enemyRenderer;
        private WorldActor enemyActor;
        private Sprite enemyIdleSprite;
        private Sprite enemyLungeSprite;
        private EnemyVisualAnimation enemyVisualAnimation;
        private Sprite[] enemyAnimationFrames;
        private float enemyAnimationFrameTimer;
        private float enemyAnimationFps;
        private float enemyHitAnimationUntil;
        private float enemyAttackAnimationUntil;
        private int enemyAnimationFrameIndex;
        private bool enemyAnimationLoops;
        private PlayMode mode;
        private float hitReadyAt;
        private float dodgeReadyAt;
        private float dodgeDuration;
        private float invulnerableUntil;
        private float monsterPhaseTimer;
        private Vector2 dodgeDirection;
        private Vector2 enemyLungeTarget;
        private Vector2 monsterAttackOrigin;
        private Vector2 monsterAttackDirection;
        private Vector2 monsterAttackTarget;
        private MonsterAttackPhase monsterAttackPhase;
        private float uiRefreshTimer;
        private float footstepTimer;
        private bool enemyHitFlash;
        private WorldActor activeFishingSpot;
        private float fishingWaitRemaining;
        private float fishingBiteRemaining;
        private bool fishingBiteActive;
        private float farmSaveTimer;
        private float monsterVocalReadyAt;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void EnsureGameRuntime()
        {
            if (FindAnyObjectByType<GameRuntime>() != null) return;
            new GameObject("Ashen Oath Runtime").AddComponent<GameRuntime>();
        }

        private void Awake()
        {
            if (instance != null && instance != this)
            {
                Destroy(gameObject);
                return;
            }

            instance = this;
            Application.targetFrameRate = 60;
            Screen.orientation = ScreenOrientation.LandscapeLeft;
            musicSource = gameObject.AddComponent<AudioSource>();
            musicSource.playOnAwake = false;
            musicSource.loop = true;
            musicSource.spatialBlend = 0;
            musicSource.volume = 0.28f;
            explorationTheme = Resources.Load<AudioClip>("Audio/exploration_theme");
            battleTheme = Resources.Load<AudioClip>("Audio/battle_theme");
            effectsSource = gameObject.AddComponent<AudioSource>();
            effectsSource.playOnAwake = false;
            effectsSource.spatialBlend = 0;
            effectsSource.volume = 0.65f;
            playerAttackSfx = Resources.Load<AudioClip>("Audio/SFX/player_attack");
            playerImpactSfx = Resources.Load<AudioClip>("Audio/SFX/player_impact");
            lootCoinsSfx = Resources.Load<AudioClip>("Audio/SFX/loot_coins");
            attackSwingSfx = LoadAudioVariants("Audio/SFX/RpgPack/Battle/swing_", 3);
            swordDrawSfx = LoadAudioVariants("Audio/SFX/RpgPack/Battle/sword_draw_", 3);
            interfaceSfx = LoadAudioVariants("Audio/SFX/RpgPack/Interface/interface_", 6);
            potionBottleSfx = Resources.Load<AudioClip>("Audio/SFX/RpgPack/Items/potion_bottle");
            armorEquipSfx = new[]
            {
                Resources.Load<AudioClip>("Audio/SFX/RpgPack/Items/armor_light"),
                Resources.Load<AudioClip>("Audio/SFX/RpgPack/Items/cloth")
            };
            metalEquipSfx = Resources.Load<AudioClip>("Audio/SFX/RpgPack/Items/metal_ringing");
            beastVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/beast_", 4);
            giantVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/giant_", 3);
            ogreVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/ogre_", 3);
            shadeVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/shade_", 3);
            slimeVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/slime_", 3);
            beetleVocalSfx = LoadAudioVariants("Audio/SFX/RpgPack/Creatures/beetle_", 3);
            footstepSfx = new[]
            {
                Resources.Load<AudioClip>("Audio/SFX/footstep_1"),
                Resources.Load<AudioClip>("Audio/SFX/footstep_2"),
                Resources.Load<AudioClip>("Audio/SFX/footstep_3"),
                Resources.Load<AudioClip>("Audio/SFX/footstep_4"),
                Resources.Load<AudioClip>("Audio/SFX/footstep_5")
            };
            grassFootstepSfx = new[]
            {
                Resources.Load<AudioClip>("Audio/World/grass_footstep_1"),
                Resources.Load<AudioClip>("Audio/World/grass_footstep_2"),
                Resources.Load<AudioClip>("Audio/World/grass_footstep_3")
            };
            stoneFootstepSfx = new[]
            {
                Resources.Load<AudioClip>("Audio/World/stone_footstep_1"),
                Resources.Load<AudioClip>("Audio/World/stone_footstep_2"),
                Resources.Load<AudioClip>("Audio/World/stone_footstep_3"),
                Resources.Load<AudioClip>("Audio/World/stone_footstep_4")
            };
            nightCricketsAmbience = Resources.Load<AudioClip>("Audio/Ambience/night_crickets");
            tickingClockAmbience = Resources.Load<AudioClip>("Audio/Ambience/ticking_clock");
            riverAmbience = Resources.Load<AudioClip>("Audio/Ambience/vistula_river");
            parkBirdsAmbience = Resources.Load<AudioClip>("Audio/Ambience/park_ambience_birds");
            parkRiverAmbience = Resources.Load<AudioClip>("Audio/Ambience/park_ambience_river");
            parkWindAmbience = Resources.Load<AudioClip>("Audio/Ambience/park_ambience_wind");
            fishingCastSfx = Resources.Load<AudioClip>("Audio/SFX/Fishing/water");
            fishingBiteSfx = Resources.Load<AudioClip>("Audio/SFX/Fishing/bubbles");
            fishingCatchSfx = Resources.Load<AudioClip>("Audio/SFX/Fishing/waterReentry");
            fishingMissSfx = Resources.Load<AudioClip>("Audio/SFX/Fishing/swim");
            ambienceSource = gameObject.AddComponent<AudioSource>();
            ambienceSource.playOnAwake = false;
            ambienceSource.loop = true;
            ambienceSource.spatialBlend = 0;
            ambienceSource.volume = 0.1f;
            telegraphRingVfx = LoadVfxSprite("telegraph_ring");
            hitSlashVfx = LoadVfxSprite("hit_slash");
            dodgeFlashVfx = LoadVfxSprite("dodge_flash");
            rewardGlintVfx = LoadVfxSprite("reward_glint");
            healingBurstVfx = LoadVfxSprite("healing_burst");
            craftingFlareVfx = LoadVfxSprite("craft_flare");
            harvestGlintVfx = LoadVfxSprite("harvest_glint");
            fishingRippleVfx = LoadVfxSprite("fishing_ripple");
            save = SaveService.Load();
            ItemCatalog.Load();
            LoadQuestCatalog();
            codexCatalog = CodexCatalogService.Load(questCatalog);
            LoadDialogueCatalog();
            questLandmarkCatalog = QuestLandmarkCatalogService.Load(questCatalog, dialogueCatalog);
            LoadMonsterCatalog();
            encounterCatalog = EncounterCatalogService.Load();
            fishingCatalog = FishingCatalogService.Load();
            recipeCatalog = RecipeCatalogService.Load();
            farmCatalog = FarmCatalogService.Load();
            var progressMigrated = QuestProgressService.Reconcile(save, questCatalog);
            BuildWorld();
            hud = gameObject.AddComponent<GameHud>();
            hud.Build(this);
            if (progressMigrated) SaveNow();
            RefreshHud();
            mode = PlayMode.Dialogue;
            PlayOpeningMusic();
            hud.ShowTitleScreen(save.started, () =>
            {
                if (!save.started)
                {
                    ShowDialogue("rowan_opening", () =>
                    {
                        save.started = true;
                        mode = PlayMode.Exploring;
                        PlayExplorationMusic();
                        SaveNow();
                        RefreshHud();
                    });
                    return;
                }

                mode = PlayMode.Exploring;
                PlayExplorationMusic();
                Debug.Log("Ashen Oath save loaded from " + SaveService.SavePath);
            });
        }

        private void Update()
        {
            UpdateFarmProgress();
            if (mode == PlayMode.Exploring) UpdateExploration();
            else if (mode == PlayMode.Combat) UpdateCombat();
            else if (mode == PlayMode.Fishing) UpdateFishing();
            else if (mode == PlayMode.Inventory && (Input.GetKeyDown(KeyCode.I) || Input.GetKeyDown(KeyCode.Escape)))
                CloseInventory();
            else if (mode == PlayMode.Dialogue && hud != null && !hud.IsChoosing &&
                     (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.Space)))
                hud.ConfirmDialogue();

            if (mode != PlayMode.Exploring && mode != PlayMode.Combat)
                UpdatePlayerAnimation(Vector2.zero);

            uiRefreshTimer -= Time.deltaTime;
            if (uiRefreshTimer <= 0)
            {
                uiRefreshTimer = 0.15f;
                RefreshHud();
            }

            AnimateActors();
        }

        private void UpdateExploration()
        {
            var input = Vector2.zero;
            if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow)) input.x -= 1;
            if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow)) input.x += 1;
            if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) input.y -= 1;
            if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow)) input.y += 1;
            if (hud != null && hud.Stick != null) input += hud.Stick.Value;

            if (input.sqrMagnitude > 1) input.Normalize();
            footstepTimer -= Time.deltaTime;
            if (input.sqrMagnitude > 0.04f && footstepTimer <= 0)
            {
                var steps = GetFootstepSounds(save.locationId);
                if (steps == null || steps.Length == 0) steps = footstepSfx;
                if (steps != null && steps.Length > 0)
                    PlaySfx(steps[sfxRandom.Next(steps.Length)], 0.22f);
                footstepTimer = 0.34f;
            }
            player.position += (Vector3)(input * (MoveSpeed * Time.deltaTime));
            player.position = new Vector3(Mathf.Clamp(player.position.x, -11.3f, 11.3f),
                Mathf.Clamp(player.position.y, -5.2f, 5.0f), player.position.z);
            UpdatePlayerAnimation(input);

            if (Input.GetKeyDown(KeyCode.E)) Interact();
            if (Input.GetKeyDown(KeyCode.Space)) Attack();
            if (Input.GetKeyDown(KeyCode.Alpha1)) UsePotion();
            if (Input.GetKeyDown(KeyCode.I)) ToggleInventory();
        }

        public void ToggleInventory()
        {
            if (mode == PlayMode.Inventory)
            {
                CloseInventory();
                return;
            }

            if (mode != PlayMode.Exploring || hud == null) return;
            mode = PlayMode.Inventory;
            PlayRandomSfx(interfaceSfx, 0.24f);
            ShowInventory();
        }

        public void ToggleQuestJournal()
        {
            if (mode == PlayMode.Inventory)
            {
                CloseInventory();
                return;
            }

            if (mode != PlayMode.Exploring || hud == null) return;
            mode = PlayMode.Inventory;
            PlayRandomSfx(interfaceSfx, 0.24f);
            ShowQuestJournal();
        }

        public void AcceptSideQuest(string questId)
        {
            if (mode != PlayMode.Inventory || questCatalog == null || save == null) return;
            if (!QuestProgressService.TryAcceptSideQuest(save, questCatalog, questId, save.locationId)) return;
            PlayRandomSfx(interfaceSfx, 0.28f);
            RefreshSideQuestEncounterVisibility();
            SaveNow();
            ShowQuestJournal();
            RefreshHud();
        }

        public void OpenCredits()
        {
            if (mode != PlayMode.Exploring || hud == null) return;
            mode = PlayMode.Inventory;
            PlayRandomSfx(interfaceSfx, 0.24f);
            hud.ShowCredits();
        }

        public void OpenCodex()
        {
            if (mode == PlayMode.Inventory)
            {
                CloseInventory();
                return;
            }

            if (mode != PlayMode.Exploring || hud == null) return;
            mode = PlayMode.Inventory;
            PlayRandomSfx(interfaceSfx, 0.24f);
            hud.ShowCodex(CodexCatalogService.GetUnlocked(codexCatalog, save));
        }

        public void CloseInventory()
        {
            if (mode != PlayMode.Inventory) return;
            PlayRandomSfx(interfaceSfx, 0.2f);
            mode = PlayMode.Exploring;
            hud.CloseInventory();
            RefreshHud();
        }

        public void EquipItem(string itemId)
        {
            if (mode != PlayMode.Inventory || !InventoryService.TryEquip(save, itemId)) return;
            var item = ItemCatalog.Find(itemId);
            if (item != null && item.equipmentSlot == "armor") PlayRandomSfx(armorEquipSfx, 0.3f);
            else PlaySfx(metalEquipSfx, 0.3f);
            SaveNow();
            ShowInventory();
            RefreshHud();
        }

        private void ShowInventory()
        {
            if (hud == null) return;
            var rows = new List<InventoryItemRow>();
            var seen = new HashSet<string>();
            if (save.inventory != null)
            {
                foreach (var stack in save.inventory)
                {
                    if (stack == null || stack.quantity <= 0 || !seen.Add(stack.itemId)) continue;
                    var definition = ItemCatalog.Find(stack.itemId);
                    if (definition == null)
                    {
                        rows.Add(new InventoryItemRow(stack.itemId,
                            stack.itemId + "  × " + InventoryService.Count(save, stack.itemId), false));
                        continue;
                    }

                    var equipped = InventoryService.IsEquipped(save, definition);
                    var detail = definition.name + "  × " + InventoryService.Count(save, stack.itemId) +
                                 (equipped ? "  •  ĐANG MẶC" : "") + "\n" + definition.description;
                    rows.Add(new InventoryItemRow(stack.itemId, detail, definition.category == "equipment",
                        GetInventoryIcon(stack.itemId)));
                }
            }

            if (rows.Count == 0) rows.Add(new InventoryItemRow("", "Hành trang đang trống.", false));
            hud.ShowInventory(rows, BuildEquipmentSummary(), EquipItem);
        }

        private void ShowQuestJournal()
        {
            if (hud == null || save == null || questCatalog == null) return;
            var rows = new List<QuestJournalRow>();
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
                rows.Add(CreateQuestJournalRow(quest,
                    quest.type == "side" ? "NHIỆM VỤ PHỤ · ĐANG LÀM" : "TUYẾN TRUYỆN · ĐANG LÀM", false));

            var availableSideQuests = QuestProgressService.GetAvailableSideQuests(save, questCatalog, save.locationId);
            var hasCapacity = (save.activeSideQuestIds?.Count ?? 0) < QuestProgressService.MaxActiveSideQuests;
            foreach (var quest in availableSideQuests)
                rows.Add(CreateQuestJournalRow(quest, hasCapacity ? "NHIỆM VỤ PHỤ · CÓ THỂ NHẬN" :
                    "NHIỆM VỤ PHỤ · ĐẦY KHE", hasCapacity));

            if (save.completedQuestIds != null)
                foreach (var quest in questCatalog.entries)
                    if (quest != null && quest.type == "side" && save.completedQuestIds.Contains(quest.id))
                        rows.Add(CreateQuestJournalRow(quest, "NHIỆM VỤ PHỤ · HOÀN TẤT", false));

            hud.ShowQuestJournal(rows, AcceptSideQuest);
        }

        private QuestJournalRow CreateQuestJournalRow(QuestDefinition quest, string state, bool canAccept)
        {
            var lines = new List<string> { state + "\n" + quest.title, quest.objective };
            if (!string.IsNullOrEmpty(quest.giverId)) lines.Add("Người giao: " + FormatQuestGiver(quest.giverId));
            if (quest.objectives != null)
                foreach (var objective in quest.objectives)
                {
                    if (objective == null) continue;
                    var count = QuestProgressService.GetObjectiveProgress(save, quest, objective);
                    lines.Add("• " + objective.description + "  [" + count + "/" + objective.requiredCount + "]");
                }
            return new QuestJournalRow(quest.id, string.Join("\n", lines), canAccept);
        }

        private static string FormatQuestGiver(string giverId)
        {
            var words = giverId.Replace('_', ' ').Split(' ');
            for (var i = 0; i < words.Length; i++)
                if (words[i].Length > 0)
                    words[i] = char.ToUpperInvariant(words[i][0]) + words[i].Substring(1);
            return string.Join(" ", words);
        }

        private string BuildEquipmentSummary()
        {
            var weapon = ItemCatalog.Find(save.weaponId);
            var armor = ItemCatalog.Find(save.armorId);
            var charm = ItemCatalog.Find(save.charmId);
            return "VŨ KHÍ  " + (weapon == null ? "Trống" : weapon.name + "  (Công +" + weapon.attackBonus + ")") +
                   "     •     GIÁP  " + (armor == null ? "Trống" : armor.name + "  (Giáp +" + armor.guardBonus + ")") +
                   "     •     BÙA  " + (charm == null ? "Trống" : charm.name);
        }

        private void UpdateCombat()
        {
            var movement = Vector2.zero;
            if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow)) movement.x -= 1;
            if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow)) movement.x += 1;
            if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) movement.y -= 1;
            if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow)) movement.y += 1;
            if (hud != null && hud.Stick != null) movement += hud.Stick.Value;
            if (movement.sqrMagnitude > 1) movement.Normalize();

            if (Input.GetKeyDown(KeyCode.LeftShift) || Input.GetKeyDown(KeyCode.RightShift)) Dodge();

            var velocity = movement * MoveSpeed;
            if (dodgeDuration > 0)
            {
                velocity += dodgeDirection * 10f;
                dodgeDuration -= Time.deltaTime;
            }

            player.position += (Vector3)(velocity * Time.deltaTime);
            player.position = new Vector3(Mathf.Clamp(player.position.x, -11.3f, 11.3f),
                Mathf.Clamp(player.position.y, -5.2f, 5.0f), player.position.z);
            UpdatePlayerAnimation(velocity);

            monsterPhaseTimer -= Time.deltaTime;
            if (monsterAttackPhase == MonsterAttackPhase.ClosingIn)
            {
                ApproachWithMonster();
                if (monsterPhaseTimer <= 0)
                {
                    monsterAttackPhase = MonsterAttackPhase.Telegraph;
                    monsterPhaseTimer = activeMonsterDefinition.telegraphSeconds;
                    monsterAttackOrigin = enemyRoot == null ? player.position : enemyRoot.position;
                    var aim = (Vector2)player.position - monsterAttackOrigin;
                    monsterAttackDirection = aim.sqrMagnitude > 0.001f ? aim.normalized : Vector2.right;
                    monsterAttackTarget = player.position;
                    if (MonsterCombatRules.IsLaneAttack(activeMonsterDefinition.specialMoveId))
                        SpawnBossChargeTelegraph(monsterAttackOrigin, monsterAttackDirection,
                            activeMonsterDefinition.specialMoveReach, activeMonsterDefinition.telegraphSeconds);
                    else if (MonsterCombatRules.IsMarkedStrike(activeMonsterDefinition.specialMoveId))
                        SpawnTargetStrikeTelegraph(monsterAttackTarget,
                            activeMonsterDefinition.specialMoveReach, activeMonsterDefinition.telegraphSeconds);
                    else
                    {
                        var radius = MonsterCombatRules.IsAreaAttack(activeMonsterDefinition.specialMoveId)
                            ? activeMonsterDefinition.specialMoveReach : activeMonsterDefinition.attackReach;
                        SpawnTelegraphRing(radius, activeMonsterDefinition.telegraphSeconds);
                    }
                }
            }
            else if (monsterAttackPhase == MonsterAttackPhase.Telegraph)
            {
                if (enemyRenderer != null)
                {
                    var pulse = 0.45f + Mathf.PingPong(Time.time * 3.4f, 0.45f);
                    var telegraphColor = activeMonsterDefinition.specialMoveId == "siphon"
                        ? new Color(0.22f, 0.9f, 0.78f) : activeMonsterDefinition.specialMoveId == "hook"
                            ? new Color(1f, 0.68f, 0.2f) : activeMonsterDefinition.specialMoveId == "marked_strike"
                                ? new Color(0.82f, 0.42f, 0.96f) : new Color(1f, 0.38f, 0.25f);
                    enemyRenderer.color = Color.Lerp(Color.white, telegraphColor, pulse);
                }

                if (monsterPhaseTimer <= 0) BeginMonsterLeap();
            }
            else if (monsterAttackPhase == MonsterAttackPhase.Lunging)
            {
                if (activeMonsterDefinition.specialMoveId == "hook" && enemyRoot != null &&
                    Time.time >= invulnerableUntil)
                {
                    var pullDirection = (Vector2)(enemyRoot.position - player.position);
                    if (pullDirection.sqrMagnitude > 0.01f)
                    {
                        var pulledPosition = Vector2.MoveTowards(player.position, enemyRoot.position,
                            7.0f * Time.deltaTime);
                        player.position = new Vector3(Mathf.Clamp(pulledPosition.x, -11.3f, 11.3f),
                            Mathf.Clamp(pulledPosition.y, -5.2f, 5.0f), player.position.z);
                    }
                }

                if (enemyRoot != null)
                {
                    var speed = activeMonsterDefinition.lungeDistance / activeMonsterDefinition.lungeSeconds;
                    var position = Vector2.MoveTowards(enemyRoot.position, enemyLungeTarget, speed * Time.deltaTime);
                    enemyRoot.position = new Vector3(position.x, position.y, enemyRoot.position.z);
                    if (enemyActor != null) enemyActor.BasePosition = enemyRoot.position;
                }

                if (monsterPhaseTimer <= 0 || enemyRoot == null ||
                    Vector2.Distance(enemyRoot.position, enemyLungeTarget) <= 0.05f)
                    ResolveMonsterLeap();
            }
            else if (monsterAttackPhase == MonsterAttackPhase.Recovery && monsterPhaseTimer <= 0)
            {
                monsterAttackPhase = MonsterAttackPhase.ClosingIn;
                monsterPhaseTimer = activeMonsterDefinition.closingSeconds;
                if (enemyRenderer != null && !enemyHitFlash) enemyRenderer.color = Color.white;
            }

            UpdateEnemyAnimation();
        }

        public void Dodge()
        {
            if (mode != PlayMode.Combat || Time.time < dodgeReadyAt) return;

            var direction = Vector2.zero;
            if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow)) direction.x -= 1;
            if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow)) direction.x += 1;
            if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) direction.y -= 1;
            if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow)) direction.y += 1;
            if (hud != null && hud.Stick != null) direction += hud.Stick.Value;

            if (direction.sqrMagnitude < 0.01f && enemyRoot != null)
                direction = (Vector2)(player.position - enemyRoot.position);
            if (direction.sqrMagnitude < 0.01f) direction = Vector2.left;

            dodgeDirection = direction.normalized;
            dodgeDuration = 0.16f;
            invulnerableUntil = Time.time + 0.36f;
            dodgeReadyAt = Time.time + 1.15f;
            SpawnPixelEffect(dodgeFlashVfx, player.position, new Color(0.45f, 0.92f, 0.96f, 0.92f),
                0.28f, 1.35f, 0.24f, 6);
        }

        private void ResolveMonsterLeap()
        {
            monsterAttackPhase = MonsterAttackPhase.Recovery;
            monsterPhaseTimer = activeMonsterDefinition.recoverySeconds;
            if (Time.time >= monsterVocalReadyAt)
            {
                PlayRandomSfx(GetMonsterVocalSet(activeMonsterDefinition), 0.2f);
                monsterVocalReadyAt = Time.time + 4f;
            }
            var playerDodged = Time.time < invulnerableUntil;
            var attackReach = MonsterCombatRules.EffectiveReach(activeMonsterDefinition);
            var outsideReach = enemyRoot == null || (MonsterCombatRules.IsLaneAttack(activeMonsterDefinition.specialMoveId)
                ? !PlayerInsideChargedLane()
                : MonsterCombatRules.IsMarkedStrike(activeMonsterDefinition.specialMoveId)
                    ? !MonsterCombatRules.IsPointInsideMarkedStrike(player.position, monsterAttackTarget, attackReach)
                    : Vector2.Distance(player.position, enemyRoot.position) > attackReach);

            if (!playerDodged && !outsideReach)
            {
                PlaySfx(playerImpactSfx, 0.45f);
                SpawnPixelEffect(hitSlashVfx, player.position + Vector3.up * 0.25f,
                    new Color(1f, 0.37f, 0.33f, 0.94f), 0.42f, 1.15f, 0.2f, 7);
                var damage = Mathf.Max(1, activeMonsterDefinition.attackDamage - InventoryService.GuardBonus(save));
                save.health = Mathf.Max(0, save.health - damage);
                if (activeMonsterDefinition.specialMoveId == "siphon")
                    activeEncounterProgress.health = Mathf.Min(ActiveMonsterMaxHealth,
                        activeEncounterProgress.health + Mathf.Clamp(damage / 2, 2, 6));
                SaveNow();
                if (save.health <= 0)
                {
                    save.health = 1;
                    mode = PlayMode.Dialogue;
                    SetMonsterCombatHud(false);
                    PlayDownedMusic();
                    ShowDialogue(activeEncounterDefinition.downDialogueId, () =>
                    {
                        save.health = 30;
                        dodgeDuration = 0;
                        mode = PlayMode.Exploring;
                        PlayExplorationMusic();
                        SaveNow();
                        RefreshHud();
                    });
                    SaveNow();
                    return;
                }
            }

            if (enemyRenderer != null && !enemyHitFlash)
                enemyRenderer.color = new Color32(185, 218, 170, 255);
            RefreshHud();
        }

        private bool PlayerInsideChargedLane()
        {
            return MonsterCombatRules.IsPointInsideLane(player.position, monsterAttackOrigin,
                monsterAttackDirection, activeMonsterDefinition.specialMoveReach,
                activeMonsterDefinition.attackReach);
        }

        private void ApproachWithMonster()
        {
            if (enemyRoot == null) return;
            var offset = (Vector2)(player.position - enemyRoot.position);
            var distance = offset.magnitude;
            var stopMultiplier = activeMonsterDefinition.specialMoveId == "ranged_bolt" ? 0.92f : 0.72f;
            var stopDistance = Mathf.Max(0.9f, activeMonsterDefinition.attackReach * stopMultiplier);
            if (distance <= stopDistance) return;

            var position = Vector2.MoveTowards(enemyRoot.position, player.position,
                activeMonsterDefinition.approachSpeed * Time.deltaTime);
            enemyRoot.position = new Vector3(position.x, position.y, enemyRoot.position.z);
            if (enemyActor != null) enemyActor.BasePosition = enemyRoot.position;
        }

        private void BeginMonsterLeap()
        {
            monsterAttackPhase = MonsterAttackPhase.Lunging;
            monsterPhaseTimer = activeMonsterDefinition.lungeSeconds;
            if (enemyRoot == null)
            {
                enemyLungeTarget = player.position;
                return;
            }

            var offset = (Vector2)(player.position - enemyRoot.position);
            var distance = offset.magnitude;
            if (distance <= 0.001f)
            {
                enemyLungeTarget = enemyRoot.position;
                return;
            }

            if (MonsterCombatRules.HoldsPositionDuringAttack(activeMonsterDefinition.specialMoveId))
            {
                enemyLungeTarget = enemyRoot.position;
                return;
            }

            if (activeMonsterDefinition.specialMoveId == "line_charge")
            {
                var endpoint = monsterAttackOrigin + monsterAttackDirection * activeMonsterDefinition.specialMoveReach;
                enemyLungeTarget = new Vector2(Mathf.Clamp(endpoint.x, -11.3f, 11.3f),
                    Mathf.Clamp(endpoint.y, -5.2f, 5.0f));
                return;
            }

            var travelDistance = Mathf.Min(activeMonsterDefinition.lungeDistance,
                Mathf.Max(0, distance - activeMonsterDefinition.lungeStopDistance));
            var target = (Vector2)enemyRoot.position + offset.normalized * travelDistance;
            enemyLungeTarget = target;
        }

        private void BuildWorld()
        {
            var atBarracks = save.locationId == "dawnkeep_barracks";
            var atDawnkeep = save.locationId == "dawnkeep_outpost";
            var atCinderwell = save.locationId == "cinderwell_basin";
            var atCinderCistern = save.locationId == "cinder_cistern";
            var atSaltRoad = save.locationId == "salt_road";
            var atSaltLockhouse = save.locationId == "salt_lockhouse";
            var atChoir = save.locationId == "choir_beneath_lake";
            var atGreenwake = save.locationId == "greenwake_refuge";
            var atOuterwake = save.locationId == "outerwake_archive";
            var atLastOath = save.locationId == "last_oath_reach";
            enemyRoot = null;
            enemyRenderer = null;
            enemyActor = null;
            activeMonsterDefinition = null;
            activeEncounterDefinition = null;
            activeEncounterProgress = null;
            actors.Clear();
            var locationName = atBarracks ? "Dawnkeep Cadet Barracks" : atDawnkeep ? "Dawnkeep Outpost" : atCinderwell ? "Cinderwell Basin" :
                atCinderCistern ? "Cinderwell Lower Cistern" : atSaltLockhouse ? "Salt Road Lockhouse" :
                atSaltRoad ? "Salt Road" :
                atChoir ? "Choir Beneath the Lake" :
                atGreenwake ? "Greenwake Refuge" : atOuterwake ? "The Outer-Wake Archive" :
                atLastOath ? "Crownfall Reach" : "Ashfall Village";
            worldRoot = new GameObject("World — " + locationName).transform;

            var cameraObject = new GameObject("Main Camera", typeof(Camera), typeof(AudioListener));
            cameraObject.transform.SetParent(worldRoot, false);
            cameraObject.tag = "MainCamera";
            cameraObject.transform.position = new Vector3(0, 0, -10);
            var camera = cameraObject.GetComponent<Camera>();
            camera.orthographic = true;
            camera.orthographicSize = 7.5f;
            camera.backgroundColor = new Color32(19, 25, 37, 255);
            camera.clearFlags = CameraClearFlags.SolidColor;

            var backgroundResource = atBarracks ? "Art/dawnkeep_barracks" : atDawnkeep ? "Art/dawnkeep_outpost" :
                atCinderwell ? "Art/cinderwell_basin" : atCinderCistern ? "Art/cinder_cistern" :
                atSaltLockhouse ? "Art/salt_lockhouse" : atSaltRoad ? "Art/salt_road" :
                atChoir ? "Art/choir_beneath_lake" : atGreenwake ? "Art/greenwake_refuge" :
                atOuterwake ? "Art/veil_archive" :
                atLastOath ? "Art/last_oath_reach" :
                "Art/ashfall_village";
            var backgroundTexture = Resources.Load<Texture2D>(backgroundResource);
            if (backgroundTexture != null)
            {
                backgroundTexture.filterMode = FilterMode.Point;
                var background = new GameObject(locationName + " — pixel background");
                background.transform.SetParent(worldRoot, false);
                var renderer = background.AddComponent<SpriteRenderer>();
                renderer.sprite = SpriteFromTexture(backgroundTexture, 128, new Vector2(0.5f, 0.5f));
                renderer.sortingOrder = -10;
                var desiredWidth = camera.orthographicSize * 2 * 16f / 9f * 1.04f;
                var spriteWidth = renderer.sprite.bounds.size.x;
                background.transform.localScale = Vector3.one * (desiredWidth / spriteWidth);
            }
            else
            {
                Debug.LogError("Missing Resources/" + backgroundResource + ".png");
            }

            var heroTexture = Resources.Load<Texture2D>("Art/rowan_hale");
            var heroWalkTexture = Resources.Load<Texture2D>("Art/rowan_hale_walk");
            if (heroTexture != null)
            {
                heroTexture.filterMode = FilterMode.Point;
                player = new GameObject("Rowan Hale").transform;
                player.position = new Vector3(save.playerX, save.playerY, 0);
                playerRenderer = player.gameObject.AddComponent<SpriteRenderer>();
                playerRenderer.sprite = SpriteFromTexture(heroTexture, 256, new Vector2(0.5f, 0.06f));
                playerRenderer.sortingOrder = 5;
                player.localScale = Vector3.one * 0.42f;
            }
            else
            {
                Debug.LogError("Missing Resources/Art/rowan_hale.png");
                player = new GameObject("Rowan Hale fallback").transform;
                playerRenderer = player.gameObject.AddComponent<SpriteRenderer>();
                playerRenderer.sprite = CreatePixelSprite("Rowan pixel placeholder", 24, 36, DrawRowanPixelArt);
                playerRenderer.sortingOrder = 5;
                player.position = new Vector3(save.playerX, save.playerY, 0);
                player.localScale = Vector3.one * 0.065f;
            }

            if (playerWalkFrames == null && heroWalkTexture != null)
                playerWalkFrames = CreatePlayerWalkFrames(heroWalkTexture);
            if (playerWalkFrames != null)
            {
                playerFacingRow = 0;
                playerWalkFrame = 0;
                playerWalkFrameTimer = 0;
                playerRenderer.flipX = false;
                playerRenderer.sprite = playerWalkFrames[playerFacingRow][playerWalkFrame];
                player.localScale = Vector3.one * 0.42f;
            }
            else
            {
                Debug.LogWarning("Missing Resources/Art/rowan_hale_walk.png; Rowan will use the static portrait.");
            }

            player.SetParent(worldRoot, true);

            if (atBarracks) BuildDawnkeepBarracksActors();
            else if (atDawnkeep) BuildDawnkeepActors();
            else if (atCinderwell) BuildCinderwellActors();
            else if (atCinderCistern) BuildCinderCisternActors();
            else if (atSaltLockhouse) BuildSaltLockhouseActors();
            else if (atSaltRoad) BuildSaltRoadActors();
            else if (atChoir) BuildChoirActors();
            else if (atGreenwake) BuildGreenwakeActors();
            else if (atOuterwake) BuildOuterwakeActors();
            else if (atLastOath) BuildLastOathActors();
            else BuildAshfallActors();
            BuildQuestLandmarkActors(save.locationId);
        }

        private void BuildAshfallActors()
        {
            var miraTexture = Resources.Load<Texture2D>("Art/mira_cole");
            var miraSprite = miraTexture != null
                ? SpriteFromTexture(miraTexture, 256, new Vector2(0.5f, 0.06f))
                : CreatePixelSprite("Mira Cole fallback", 32, 42, DrawMiraPixelArt);
            var mira = CreateActor("Mira Cole", ActorKind.Mira, new Vector2(-5.7f, 0.4f),
                miraSprite, miraTexture != null ? 0.36f : 0.075f);
            actors.Add(mira);

            actors.Add(CreateActor("Gideon Park", ActorKind.SurvivorWitness, new Vector2(-2.5f, 1.0f),
                CreatePixelSprite("Gideon Park pixel sprite", 32, 42, DrawGideonPixelArt), 0.075f));
            actors.Add(CreateActor("Dấu ấn cháy", ActorKind.SealClue, new Vector2(2.8f, -3.0f),
                CreatePixelSprite("Ashfall seal fragment sprite", 20, 20, DrawBurnedSealPixelArt), 0.085f));
            actors.Add(CreateActor("Captain Alden Vale", ActorKind.CaptainAlden, new Vector2(8.0f, -3.1f),
                CreatePixelSprite("Captain Alden Vale pixel sprite", 32, 42, DrawAldenPixelArt), 0.075f));

            var easternRoad = CreateActor("Eastern Road", ActorKind.RoadGate, new Vector2(0.2f, 4.25f),
                CreatePixelSprite("Eastern Road marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            easternRoad.DestinationLocationId = "dawnkeep_outpost";
            easternRoad.DestinationPosition = new Vector2(0, -4.4f);
            actors.Add(easternRoad);

            BuildFarmPlotActors("ashfall_village");
            actors.Add(CreateActor("Mira Cole's Herb Table", ActorKind.Workstation, new Vector2(-7.6f, -3.3f),
                CreatePixelSprite("Ashfall alchemy table", 36, 32, DrawAlchemyTablePixelArt), 0.085f));
            actors[actors.Count - 1].WorkstationId = "ashfall_herb_table";
            BuildEncounterActors("ashfall_village");
        }

        private void BuildQuestLandmarkActors(string locationId)
        {
            foreach (var definition in QuestLandmarkCatalogService.FindByLocation(questLandmarkCatalog, locationId))
            {
                if (definition == null) continue;
                if (definition.visualId == "witness")
                {
                    var witness = actors.Find(actor => actor != null && actor.Kind == ActorKind.SurvivorWitness);
                    if (witness == null) continue;
                    witness.BasePosition = new Vector3(definition.positionX, definition.positionY, 0);
                    witness.Transform.position = witness.BasePosition;
                    witness.ObjectiveTargetId = definition.targetId;
                    witness.InteractionDialogueId = FindLandmarkDialogue(definition.targetId);
                    continue;
                }

                PixelDrawer draw;
                var width = 32;
                var height = 36;
                switch (definition.visualId)
                {
                    case "cart_wheel": draw = DrawAshfallCartWheelPixelArt; width = 44; height = 38; break;
                    case "cart_rut": draw = DrawAshfallCartRutPixelArt; width = 40; height = 26; break;
                    case "cart_spokes": draw = DrawAshfallCartSpokesPixelArt; width = 36; height = 34; break;
                    case "cart_test": draw = DrawAshfallCartTestPixelArt; width = 42; height = 32; break;
                    case "cart_bay": draw = DrawAshfallCartBayPixelArt; width = 42; height = 32; break;
                    case "cart_kit": draw = DrawAshfallCartKitTablePixelArt; width = 40; height = 34; break;
                    case "tomas_reed": draw = DrawTomasReedPixelArt; width = 36; height = 44; break;
                    case "wind_keeper": draw = DrawHarperWillsPixelArt; width = 32; height = 44; break;
                    case "signal_frame": draw = DrawAshfallSignalFramePixelArt; width = 36; height = 42; break;
                    case "signal_vane": draw = DrawAshfallSignalVanePixelArt; width = 36; height = 42; break;
                    case "signal_mark": draw = DrawAshfallSignalMarkPixelArt; width = 36; height = 28; break;
                    case "signal_well": draw = DrawAshfallSignalWellPixelArt; width = 36; height = 32; break;
                    case "signal_ridge": draw = DrawAshfallSignalRidgePixelArt; width = 36; height = 42; break;
                    case "signal_bell_test": draw = DrawAshfallSignalBellTestPixelArt; width = 32; height = 38; break;
                    case "signal_flag_test": draw = DrawAshfallSignalFlagTestPixelArt; width = 40; height = 38; break;
                    case "chalk_tally": draw = DrawAshfallHerbLedgerPixelArt; width = 28; height = 34; break;
                    case "waymarker": draw = DrawWaymarkerPixelArt; width = 32; height = 42; break;
                    case "door_brace": draw = DrawAshfallDoorBracePixelArt; width = 32; height = 28; break;
                    case "document": draw = DrawDawnkeepDocketPixelArt; break;
                    case "noticeboard": draw = DrawDawnkeepNoticeBoardPixelArt; width = 36; height = 40; break;
                    case "sealed_case": draw = DrawDawnkeepSealedDossierPixelArt; width = 36; height = 40; break;
                    case "herb_ledger": draw = DrawAshfallHerbLedgerPixelArt; width = 28; height = 34; break;
                    case "remedy_shelf": draw = DrawAshfallRemedyShelfPixelArt; width = 36; height = 32; break;
                    case "root_graft": draw = DrawGreenwakeRootGraftPixelArt; width = 40; height = 46; break;
                    case "seed_cradle": draw = DrawGreenwakeSeedCradlePixelArt; width = 40; height = 38; break;
                    case "cycle_tablet": draw = DrawGreenwakeCycleTabletPixelArt; width = 40; height = 42; break;
                    case "stone_rill": draw = DrawGreenwakeStoneRillPixelArt; width = 42; height = 34; break;
                    case "choir_diver": draw = DrawChoirDiverPixelArt; width = 32; height = 42; break;
                    case "sluice_wheel": draw = DrawCinderSluiceWheelPixelArt; width = 40; height = 40; break;
                    case "pressure_gauge": draw = DrawCinderPressureGaugePixelArt; width = 36; height = 36; break;
                    case "filter_housing": draw = DrawCinderFilterHousingPixelArt; width = 38; height = 32; break;
                    case "clinic_house": draw = DrawMiraClinicPixelArt; width = 42; height = 38; break;
                    case "field_satchel": draw = DrawMiraFieldSatchelPixelArt; width = 34; height = 32; break;
                    case "pella_quinn": draw = DrawPellaQuinnPixelArt; width = 32; height = 44; break;
                    case "rootwall_joint": draw = DrawGreenwakeRootwallJointPixelArt; width = 48; height = 40; break;
                    case "kitchen_hearth": draw = DrawCinderKitchenHearthPixelArt; width = 38; height = 34; break;
                    case "kitchen_millstone": draw = DrawCinderKitchenMillstonePixelArt; width = 36; height = 34; break;
                    case "broth_sample": draw = DrawCinderBrothSamplePixelArt; width = 34; height = 32; break;
                    case "common_table": draw = DrawCinderCommonTablePixelArt; width = 40; height = 34; break;
                    case "glassplum_tree": draw = DrawGlassplumTreePixelArt; width = 38; height = 40; break;
                    default: continue;
                }

                var actor = CreateActor(definition.displayName, ActorKind.StoryLandmark,
                    new Vector2(definition.positionX, definition.positionY),
                    CreatePixelSprite(definition.displayName + " pixel marker", width, height, draw), definition.scale);
                actor.ObjectiveTargetId = definition.targetId;
                actor.InteractionDialogueId = FindLandmarkDialogue(definition.targetId);
                actor.IsQuestCatalogLandmark = true;
                if (definition.targetId == "pella_rootwall_joint" &&
                    IsQuestCompleted("side_greenwake_rootwall_hinge_install"))
                {
                    actor.Renderer.sprite = CreatePixelSprite("Greenwake breathing rootwall joint", 48, 40,
                        DrawGreenwakeBreathingRootwallPixelArt);
                    actor.Renderer.enabled = true;
                }
                else if (definition.targetId == "pella_rootwall_joint" &&
                         IsQuestCompleted("side_greenwake_rootwall_slot_install"))
                {
                    actor.Renderer.sprite = CreatePixelSprite("Greenwake seasonal rootwall shim", 48, 40,
                        DrawGreenwakeSeasonalRootwallPixelArt);
                    actor.Renderer.enabled = true;
                }
                else if (definition.targetId == "ashfall_cart_wheel" &&
                    IsQuestCompleted("side_ashfall_cart_install"))
                {
                    actor.Renderer.sprite = CreatePixelSprite("Repaired Ashfall cart", 48, 42,
                        DrawAshfallCartRepairedPixelArt);
                    actor.Renderer.enabled = true;
                }
                else
                {
                    actor.Renderer.enabled = HasActiveObjectiveTarget(definition.targetId);
                }
                actors.Add(actor);
            }
        }

        private void RefreshQuestLandmarkVisibility()
        {
            foreach (var actor in actors)
            {
                if (actor == null || !actor.IsQuestCatalogLandmark || actor.Renderer == null) continue;
                if (actor.ObjectiveTargetId == "pella_rootwall_joint" &&
                    IsQuestCompleted("side_greenwake_rootwall_hinge_install"))
                {
                    actor.Renderer.sprite = CreatePixelSprite("Greenwake breathing rootwall joint", 48, 40,
                        DrawGreenwakeBreathingRootwallPixelArt);
                    actor.Renderer.enabled = true;
                    continue;
                }
                if (actor.ObjectiveTargetId == "pella_rootwall_joint" &&
                    IsQuestCompleted("side_greenwake_rootwall_slot_install"))
                {
                    actor.Renderer.sprite = CreatePixelSprite("Greenwake seasonal rootwall shim", 48, 40,
                        DrawGreenwakeSeasonalRootwallPixelArt);
                    actor.Renderer.enabled = true;
                    continue;
                }
                if (actor.ObjectiveTargetId == "ashfall_cart_wheel" &&
                    IsQuestCompleted("side_ashfall_cart_install"))
                {
                    actor.Renderer.enabled = true;
                    continue;
                }
                var clinicPolicy = QuestProgressService.GetStoryFlag(save, "mira_clinic_policy");
                if (actor.ObjectiveTargetId == "mira_house_open_sign" && clinicPolicy == "open_room")
                {
                    actor.Renderer.enabled = true;
                    continue;
                }
                if (actor.ObjectiveTargetId == "mira_field_satchel_station" && clinicPolicy == "field_kit")
                {
                    actor.Renderer.enabled = true;
                    continue;
                }
                actor.Renderer.enabled = HasActiveObjectiveTarget(actor.ObjectiveTargetId);
            }
        }

        private string FindLandmarkDialogue(string targetId)
        {
            foreach (var quest in questCatalog?.entries ?? new List<QuestDefinition>())
            {
                if (quest?.objectives == null) continue;
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || objective.targetId != targetId) continue;
                    if (!string.IsNullOrEmpty(objective.dialogueId)) return objective.dialogueId;
                    var firstChoice = quest.choices != null && quest.choices.Count > 0 ? quest.choices[0] : null;
                    if (firstChoice != null && !string.IsNullOrEmpty(firstChoice.dialogueId))
                        return firstChoice.dialogueId;
                }
            }
            return string.Empty;
        }

        private void BuildDawnkeepActors()
        {
            var elaraTexture = Resources.Load<Texture2D>("Art/elara_wren");
            var elaraSprite = elaraTexture != null
                ? SpriteFromTexture(elaraTexture, 256, new Vector2(0.5f, 0.035f))
                : CreatePixelSprite("Elara Wren fallback", 32, 44, DrawElaraPixelArt);
            actors.Add(CreateActor("Elara Wren", ActorKind.ElaraWren, new Vector2(-5.6f, 0.2f),
                elaraSprite, elaraTexture != null ? 0.34f : 0.075f));
            actors.Add(CreateActor("Captain Alden Vale", ActorKind.CaptainAlden, new Vector2(-1.4f, 0.7f),
                CreatePixelSprite("Captain Alden Vale outpost sprite", 32, 42, DrawAldenPixelArt), 0.075f));
            actors.Add(CreateActor("Dawnkeep Roster", ActorKind.DawnkeepRoster, new Vector2(8.1f, -0.25f),
                CreatePixelSprite("Dawnkeep stone roster", 32, 42, DrawRosterStonePixelArt), 0.085f));
            AddOuterwakeWitness("Nia Porter", new Vector2(-8.3f, -2.25f), DrawNiaPorterPixelArt,
                "nia_porter", "nia_order_testimony");
            AddQuestLandmark("Empty Cadet Bunks", new Vector2(-9.1f, 1.8f), DrawDawnkeepCotsPixelArt,
                "dawnkeep_empty_cots", "rowan_order_empty_cots", 36, 34);
            AddQuestLandmark("Transfer Docket", new Vector2(-4.1f, 3.0f), DrawDawnkeepDocketPixelArt,
                "dawnkeep_transfer_ledger", "rowan_order_transfer_ledger", 32, 36);
            AddQuestLandmark("Public Notice Board", new Vector2(2.8f, -2.9f), DrawDawnkeepNoticeBoardPixelArt,
                "order_public_noticeboard", "rowan_order_public_record", 36, 40);
            AddQuestLandmark("Sealed Archive Drawer", new Vector2(7.2f, -2.4f), DrawDawnkeepSealedDossierPixelArt,
                "order_sealed_dossier", "rowan_order_sealed_record", 36, 40);
            AddQuestLandmark("Southern Aqueduct Orders", new Vector2(2.9f, 3.7f), DrawAqueductDispatchPixelArt,
                "order_cinderwell_dispatch", "rowan_order_cinderwell_dispatch", 36, 40);
            AddQuestLandmark("Inlet Waterline Notches", new Vector2(4.7f, 0.8f), DrawDawnkeepInletMarksPixelArt,
                "dawnkeep_inlet_notches", "rowan_waterline_inlet_marks", 36, 40);
            AddQuestLandmark("Lower Waterline Post", new Vector2(7.8f, -2.8f), DrawDawnkeepLowerFlowPostPixelArt,
                "dawnkeep_lower_flow_post", "rowan_waterline_second_reading", 32, 40);
            var returnRoad = CreateActor("Return to Ashfall", ActorKind.RoadGate, new Vector2(0.0f, -4.4f),
                CreatePixelSprite("Ashfall return marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "ashfall_village";
            returnRoad.DestinationPosition = new Vector2(0.2f, 3.6f);
            actors.Add(returnRoad);
            var cinderRoad = CreateActor("Cinderwell Aqueduct Road", ActorKind.RoadGate, new Vector2(10.2f, 4.0f),
                CreatePixelSprite("Cinderwell road marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            cinderRoad.DestinationLocationId = "cinderwell_basin";
            cinderRoad.DestinationPosition = new Vector2(-7.8f, -3.7f);
            cinderRoad.RequiredQuestId = "order_cadet_oath";
            actors.Add(cinderRoad);
            var barracksDoor = CreateActor("Cadet Barracks", ActorKind.RoadGate, new Vector2(9.8f, -4.0f),
                CreatePixelSprite("Dawnkeep barracks entrance", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            barracksDoor.DestinationLocationId = "dawnkeep_barracks";
            barracksDoor.DestinationPosition = new Vector2(1.0f, -2.0f);
            barracksDoor.RequiredQuestId = "order_cadet_oath";
            actors.Add(barracksDoor);
            var forge = CreateActor("Tomas Reed", ActorKind.Workstation, new Vector2(6.6f, 2.4f),
                CreatePixelSprite("Tomas Reed at the Dawnkeep forge", 36, 44, DrawTomasReedPixelArt), 0.075f);
            forge.WorkstationId = "dawnkeep_forge";
            actors.Add(forge);
            BuildEncounterActors("dawnkeep_outpost");
            BuildFishingSpotActors("dawnkeep_outpost");
            BuildFarmPlotActors("dawnkeep_outpost");
        }

        private void BuildDawnkeepBarracksActors()
        {
            AddQuestLandmark("Morning Roll Slate", new Vector2(-5.2f, 2.0f), DrawDawnkeepDocketPixelArt,
                "barracks_morning_roll", "rowan_barracks_morning_roll", 36, 40);
            AddQuestLandmark("Returned Letter Shelf", new Vector2(5.4f, 2.7f), DrawDawnkeepSealedDossierPixelArt,
                "barracks_return_shelf", "rowan_barracks_return_shelf", 36, 40);
            AddOuterwakeWitness("Nia Porter", new Vector2(2.4f, 0.2f), DrawNiaPorterPixelArt,
                "nia_porter", "nia_barracks_roll_review");
            var returnRoad = CreateActor("Return to Dawnkeep Outpost", ActorKind.RoadGate, new Vector2(0.0f, -5.1f),
                CreatePixelSprite("Dawnkeep return marker from barracks", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "dawnkeep_outpost";
            returnRoad.DestinationPosition = new Vector2(9.2f, -3.2f);
            actors.Add(returnRoad);
        }

        private void BuildCinderwellActors()
        {
            actors.Add(CreateActor("Sister June", ActorKind.SisterJune, new Vector2(-7.2f, -2.4f),
                CreatePixelSprite("Sister June pixel sprite", 32, 44, DrawSisterJunePixelArt), 0.075f));
            actors.Add(CreateActor("Talia Mercer", ActorKind.TaliaMercer, new Vector2(-0.7f, 0.7f),
                CreatePixelSprite("Talia Mercer pixel sprite", 32, 44, DrawTaliaMercerPixelArt), 0.075f));
            actors.Add(CreateActor("Oren Bell", ActorKind.OrenBell, new Vector2(7.2f, 1.6f),
                CreatePixelSprite("Oren Bell pixel sprite", 32, 44, DrawOrenBellPixelArt), 0.075f));
            AddQuestLandmark("Grain Ledger", new Vector2(-7.6f, 1.2f), DrawCinderLedgerPixelArt,
                "cinder_grain_ledger", "rowan_cinder_grain_ledger");
            AddQuestLandmark("East Sluice", new Vector2(2.7f, 2.3f), DrawCinderSluicePixelArt,
                "cinder_east_sluice", "rowan_cinder_sluice_inspection");
            AddQuestLandmark("Refugee Field Valve", new Vector2(-3.8f, -2.6f), DrawCinderValvePixelArt,
                "basin_refugee_channel", "rowan_water_to_refugees");
            AddQuestLandmark("Seed Archive", new Vector2(7.2f, -2.6f), DrawCinderLedgerPixelArt,
                "cinder_seed_archive", "rowan_cinder_seed_archive");
            AddQuestLandmark("Refugee Water Roll", new Vector2(-4.7f, -3.6f), DrawCinderLedgerPixelArt,
                "cinder_refugee_roll", "rowan_cinder_refugee_roll");
            AddQuestLandmark("Reserve Weight Roll", new Vector2(7.9f, -2.8f), DrawCinderLedgerPixelArt,
                "cinder_reserve_roll", "rowan_cinder_reserve_roll");
            AddQuestLandmark("Shared Cup Rail", new Vector2(-5.8f, -0.5f), DrawCinderCupRailPixelArt,
                "cinder_shared_cup_rail", "rowan_cinder_cup_rail", 36, 34);
            AddQuestLandmark("Seed Store Hanging Scale", new Vector2(6.0f, -0.3f), DrawCinderSeedScalePixelArt,
                "cinderwell_seed_scale", "rowan_cinder_seed_scale", 34, 38);
            AddQuestLandmark("Household Water Schedule", new Vector2(-2.6f, -4.2f), DrawCinderLedgerPixelArt,
                "cinderwell_named_schedule", "rowan_cinder_named_schedule");
            AddQuestLandmark("Daily Volume Schedule", new Vector2(2.8f, -4.2f), DrawCinderLedgerPixelArt,
                "cinderwell_aggregate_schedule", "rowan_cinder_aggregate_schedule");
            AddQuestLandmark("Lower Cistern Hatch", new Vector2(0.4f, 4.0f), DrawCinderSluicePixelArt,
                "cinder_lower_hatch", "rowan_cinder_lower_hatch", 34, 38);
            var returnRoad = CreateActor("Dawnkeep Road", ActorKind.RoadGate, new Vector2(-10.4f, 4.2f),
                CreatePixelSprite("Dawnkeep road marker from Cinderwell", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "dawnkeep_outpost";
            returnRoad.DestinationPosition = new Vector2(9.6f, 3.8f);
            actors.Add(returnRoad);
            var assayBench = CreateActor("Salt Saffron Assay Bench", ActorKind.Workstation, new Vector2(3.8f, -0.7f),
                CreatePixelSprite("Cinderwell wick assay bench", 36, 34, DrawCinderCupRailPixelArt), 0.08f);
            assayBench.WorkstationId = "cinderwell_assay_bench";
            actors.Add(assayBench);
            var kitchen = CreateActor("Sister June's Camp Kitchen", ActorKind.Workstation,
                new Vector2(-8.8f, -0.8f),
                CreatePixelSprite("Sister June's camp kitchen", 38, 34, DrawCinderCupRailPixelArt), 0.085f);
            kitchen.WorkstationId = "cinderwell_kitchen";
            actors.Add(kitchen);
            AddQuestLandmark("Split Kitchen Hearth", new Vector2(4.8f, 3.8f), DrawCinderCupRailPixelArt,
                "june_kitchen_hearth", "june_stonepot_hearth");
            AddQuestLandmark("Kitchen Millstone", new Vector2(-9.1f, -4.5f), DrawCinderCupRailPixelArt,
                "june_kitchen_millstone", "june_stonepot_grindstone");
            AddQuestLandmark("Stone-Pot Sample", new Vector2(9.2f, -0.6f), DrawCinderCupRailPixelArt,
                "june_broth_sample", "june_stonepot_sample");
            AddQuestLandmark("Common Meal Table", new Vector2(-0.5f, -4.4f), DrawCinderCupRailPixelArt,
                "june_common_table", "june_stonepot_table");
            AddQuestLandmark("Road Crew Provision Crate", new Vector2(9.2f, 3.0f), DrawDawnkeepSealedDossierPixelArt,
                "june_departure_crate", "june_stonepot_departure");
            AddQuestLandmark("First-Bowl Slate", new Vector2(0.2f, -4.3f), DrawDawnkeepNoticeBoardPixelArt,
                "june_service_priority", "june_stonepot_choice_table");
            var saltRoad = CreateActor("Salt Road Pass", ActorKind.RoadGate, new Vector2(10.3f, -3.5f),
                CreatePixelSprite("Salt Road pass marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            saltRoad.DestinationLocationId = "salt_road";
            saltRoad.DestinationPosition = new Vector2(-8.4f, -3.5f);
            saltRoad.RequiredQuestId = "cinder_june_report";
            actors.Add(saltRoad);
            var cisternGate = CreateActor("Lower Cistern Stair", ActorKind.RoadGate, new Vector2(10.2f, -3.5f),
                CreatePixelSprite("Cinderwell lower cistern marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            cisternGate.DestinationLocationId = "cinder_cistern";
            cisternGate.DestinationPosition = new Vector2(-8.7f, -3.5f);
            cisternGate.RequiredQuestId = "cinder_cistern_entry";
            actors.Add(cisternGate);
            BuildFarmPlotActors("cinderwell_basin");
            BuildFishingSpotActors("cinderwell_basin");
            BuildEncounterActors("cinderwell_basin");
        }

        private void BuildCinderCisternActors()
        {
            actors.Add(CreateActor("Talia Mercer", ActorKind.TaliaMercer, new Vector2(-7.0f, -2.0f),
                CreatePixelSprite("Talia Mercer lower cistern pixel sprite", 32, 44, DrawTaliaMercerPixelArt), 0.075f));
            AddQuestLandmark("Transfer Docket", new Vector2(-1.8f, 2.8f), DrawCinderLedgerPixelArt,
                "cinder_transfer_docket", "rowan_cinder_transfer_docket", 34, 38);
            var returnRoad = CreateActor("Return to Cinderwell Basin", ActorKind.RoadGate,
                new Vector2(-10.0f, -4.1f), CreatePixelSprite("Cinderwell lower cistern exit", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "cinderwell_basin";
            returnRoad.DestinationPosition = new Vector2(8.4f, 3.6f);
            actors.Add(returnRoad);
            BuildEncounterActors("cinder_cistern");
        }

        private void BuildSaltRoadActors()
        {
            AddSaltRoadWitness("Ruth Calder", new Vector2(-5.4f, -1.2f), DrawRuthCalderPixelArt,
                "ruth_calder", "ruth_salt_arrival");
            AddSaltRoadWitness("Nella Pike", new Vector2(3.0f, 1.3f), DrawNellaPikePixelArt,
                "nella_pike", "nella_salt_testimony");
            AddSaltRoadWitness("Silas Vane", new Vector2(7.0f, 1.6f), DrawSilasVanePixelArt,
                "silas_vane", "silas_salt_testimony");
            AddQuestLandmark("Tollhouse Ledger", new Vector2(-0.8f, 1.5f), DrawSaltLedgerPixelArt,
                "salt_toll_ledger", "rowan_salt_ledger");
            AddQuestLandmark("Caravan Dispatch Seal", new Vector2(-7.2f, 1.2f), DrawSaltSealPixelArt,
                "salt_caravan_seal", "rowan_caravan_seal");
            AddQuestLandmark("Crossing Token", new Vector2(2.0f, -2.4f), DrawSaltTokenPixelArt,
                "salt_refugee_token", "rowan_refugee_token");
            AddQuestLandmark("Hunter Signal Map", new Vector2(7.2f, -2.5f), DrawSaltMapPixelArt,
                "salt_hunter_map", "rowan_hunter_map");
            AddQuestLandmark("Return Route Scrape", new Vector2(-3.6f, 3.0f), DrawSaltMapPixelArt,
                "salt_return_route_marks", "rowan_salt_caravan_return_marks");
            AddQuestLandmark("Wall of Missing Tags", new Vector2(2.9f, -3.5f), DrawSaltLedgerPixelArt,
                "salt_wall_name_slots", "rowan_salt_refugee_wall_names");
            AddQuestLandmark("First Arrow Impact", new Vector2(6.4f, -2.4f), DrawSaltMapPixelArt,
                "salt_hunter_impact_line", "rowan_salt_hunter_impact_line");
            AddQuestLandmark("Tollhouse Trapdoor", new Vector2(3.4f, -4.6f), DrawSaltSealPixelArt,
                "salt_tollhouse_floor", "rowan_salt_tollhouse_floor", 34, 36);
            var returnRoad = CreateActor("Cinderwell Return Pass", ActorKind.RoadGate,
                new Vector2(-10.3f, 4.0f), CreatePixelSprite("Cinderwell return marker from Salt Road", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "cinderwell_basin";
            returnRoad.DestinationPosition = new Vector2(8.7f, -3.1f);
            actors.Add(returnRoad);
            var choirRoad = CreateActor("Choir Beneath the Lake Pass", ActorKind.RoadGate,
                new Vector2(10.1f, 3.5f), CreatePixelSprite("Choir road marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            choirRoad.DestinationLocationId = "choir_beneath_lake";
            choirRoad.DestinationPosition = new Vector2(-9.2f, -3.5f);
            choirRoad.RequiredQuestId = "salt_route_handoff";
            actors.Add(choirRoad);
            var lockhouseStair = CreateActor("Lockhouse Underpass", ActorKind.RoadGate,
                new Vector2(10.0f, -3.7f), CreatePixelSprite("Salt Road lockhouse marker", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            lockhouseStair.DestinationLocationId = "salt_lockhouse";
            lockhouseStair.DestinationPosition = new Vector2(-8.8f, -3.5f);
            lockhouseStair.RequiredQuestId = "salt_underpass_access";
            actors.Add(lockhouseStair);
            AddQuestLandmark("Three Bent Milepost Pins", new Vector2(-1.2f, 3.9f), DrawSaltMapPixelArt,
                "saltroad_milepost_cracks", "rowan_saltroad_milepost_mounts");
            AddQuestLandmark("Incomplete Storm Dial", new Vector2(1.0f, 4.2f), DrawCinderPressureGaugePixelArt,
                "saltroad_storm_table", "rowan_saltroad_storm_register");
            AddQuestLandmark("Dry Signal Bracket", new Vector2(9.0f, -0.7f), DrawAshfallSignalFramePixelArt,
                "saltroad_beacon_mount", "rowan_saltroad_beacon_mount");
            AddQuestLandmark("Ridge Observation Point", new Vector2(-9.1f, -0.4f), DrawAshfallSignalVanePixelArt,
                "saltroad_beacon_range", "rowan_saltroad_beacon_range");
            AddQuestLandmark("Milepost Operating Board", new Vector2(4.8f, 4.1f), DrawDawnkeepNoticeBoardPixelArt,
                "saltroad_signal_policy", "rowan_saltroad_signal_policy");
            AddQuestLandmark("Public Dayline Sheet", new Vector2(-8.1f, -3.8f), DrawSaltMapPixelArt,
                "saltroad_dayline_sheet", "rowan_saltroad_dayline_record");
            AddQuestLandmark("Night Callkeeper Rota", new Vector2(7.3f, -4.2f), DrawDawnkeepNoticeBoardPixelArt,
                "saltroad_callkeeper_rota", "rowan_saltroad_callkeeper_rota");
            BuildFarmPlotActors("salt_road");
            BuildFishingSpotActors("salt_road");
            BuildEncounterActors("salt_road");
        }

        private void BuildSaltLockhouseActors()
        {
            AddQuestLandmark("Lockhouse Transfer Docket", new Vector2(-2.7f, 2.8f), DrawSaltLedgerPixelArt,
                "salt_lockhouse_docket", "rowan_salt_lockhouse_docket", 36, 40);
            AddQuestLandmark("Unmarked Chain Tags", new Vector2(-5.4f, -2.6f), DrawSaltTokenPixelArt,
                "salt_lockhouse_chain_tags", "rowan_salt_chain_tags", 30, 34);
            AddQuestLandmark("Separated Tag Tally", new Vector2(6.4f, -2.7f), DrawSaltLedgerPixelArt,
                "salt_ellis_chain_tally", "rowan_ellis_tag_test", 34, 36);
            var returnRoad = CreateActor("Return to Salt Road", ActorKind.RoadGate,
                new Vector2(-10.0f, 4.0f), CreatePixelSprite("Salt Road lockhouse exit", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "salt_road";
            returnRoad.DestinationPosition = new Vector2(8.7f, -3.5f);
            actors.Add(returnRoad);
            BuildEncounterActors("salt_lockhouse");
        }

        private void BuildChoirActors()
        {
            AddQuestLandmark("The First Warden", new Vector2(-7.8f, -0.4f), DrawFirstWardenPixelArt,
                "first_warden", "warden_choir_arrival");
            AddQuestLandmark("Lyra Moss", new Vector2(-1.1f, 0.35f), DrawLyraMossPixelArt,
                "lyra_moss", "lyra_choir_confrontation");
            AddQuestLandmark("The World Will", new Vector2(7.8f, -0.2f), DrawWorldWillPixelArt,
                "world_will", "world_will_first_contact");
            AddQuestLandmark("Northern Archive Record", new Vector2(-4.1f, 2.35f), DrawChoirRecordPixelArt,
                "choir_archive_north", "rowan_choir_archive_north");
            AddQuestLandmark("Southern Archive Record", new Vector2(0.5f, -2.6f), DrawChoirRecordPixelArt,
                "choir_archive_south", "rowan_choir_archive_south");
            AddQuestLandmark("First Oath Bell", new Vector2(7.7f, 3.5f), DrawChoirBellPixelArt,
                "choir_first_oath", "rowan_choir_oath");
            AddQuestLandmark("North Resonance Anchor", new Vector2(-6.6f, 2.4f), DrawChoirAnchorPixelArt,
                "choir_resonance_north", "rowan_anchor_north");
            AddQuestLandmark("South Resonance Anchor", new Vector2(3.0f, -3.6f), DrawChoirAnchorPixelArt,
                "choir_resonance_south", "rowan_anchor_south");
            AddQuestLandmark("Unnumbered Chime Rubbing", new Vector2(5.0f, 3.6f), DrawChoirBellPixelArt,
                "choir_unnumbered_chime", "rowan_choir_margin_marks", 36, 36);
            AddQuestLandmark("South Marginal Notation", new Vector2(-3.8f, -3.2f), DrawChoirRecordPixelArt,
                "choir_voice_margin", "rowan_choir_echo_margin", 36, 32);
            AddQuestLandmark("Unnumbered Tow Chime", new Vector2(-8.1f, -2.7f), DrawChoirBellPixelArt,
                "salt_ellis_choir_chime", "rowan_ellis_first_echo", 36, 36);
            AddQuestLandmark("Salt Road Archive Desk", new Vector2(0.2f, 4.1f), DrawChoirRecordPixelArt,
                "salt_ellis_archive_desk", "rowan_ellis_map_choice_limited", 38, 34);
            var loom = CreateActor("Lyra Moss's Archive Loom", ActorKind.Workstation,
                new Vector2(-1.2f, -2.6f), CreatePixelSprite("Choir alchemy loom", 36, 32, DrawEchoLoomPixelArt), 0.085f);
            loom.WorkstationId = "choir_archive_loom";
            actors.Add(loom);
            var anvil = CreateActor("Choir Harmonic Anvil", ActorKind.Workstation,
                new Vector2(5.4f, 2.9f), CreatePixelSprite("Choir harmonic anvil", 36, 32, DrawChoirAnvilPixelArt), 0.085f);
            anvil.WorkstationId = "choir_harmonic_anvil";
            actors.Add(anvil);
            var returnRoad = CreateActor("Return to Salt Road", ActorKind.RoadGate,
                new Vector2(-10.1f, -3.5f), CreatePixelSprite("Salt Road return marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "salt_road";
            returnRoad.DestinationPosition = new Vector2(8.4f, 3.0f);
            actors.Add(returnRoad);
            var greenwakeRoad = CreateActor("Greenwake Refuge Trail", ActorKind.RoadGate,
                new Vector2(10.0f, 3.8f), CreatePixelSprite("Greenwake trail marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            greenwakeRoad.DestinationLocationId = "greenwake_refuge";
            greenwakeRoad.DestinationPosition = new Vector2(-9.1f, -3.3f);
            greenwakeRoad.RequiredQuestId = "choir_reckoning";
            actors.Add(greenwakeRoad);
            BuildFarmPlotActors("choir_beneath_lake");
            BuildFishingSpotActors("choir_beneath_lake");
            BuildEncounterActors("choir_beneath_lake");
        }

        private void BuildGreenwakeActors()
        {
            AddQuestLandmark("Mara Bell", new Vector2(-6.3f, -0.8f), DrawMaraBellPixelArt,
                "mara_bell", "mara_greenwake_arrival");
            AddQuestLandmark("Owen Reed", new Vector2(8.0f, -3.2f), DrawOwenReedPixelArt,
                "owen_reed", "owen_greenwake_courier");
            AddQuestLandmark("The First Warden", new Vector2(-0.5f, 3.25f), DrawFirstWardenPixelArt,
                "first_warden_greenwake", "first_warden_hundredth_champion");
            AddQuestLandmark("Root-Well Ledger", new Vector2(-2.8f, -2.4f), DrawGreenwakeLedgerPixelArt,
                "greenwake_root_well", "greenwake_root_record");
            AddQuestLandmark("The Empty Crown", new Vector2(6.4f, 2.4f), DrawGreenwakeCrownPixelArt,
                "champion_offer", "greenwake_crown_offer");
            AddQuestLandmark("Outer-Wake Star Chart", new Vector2(7.5f, -2.6f), DrawGreenwakeStarChartPixelArt,
                "greenwake_star_chart", "greenwake_star_chart");
            AddQuestLandmark("East Orchard Signal", new Vector2(8.5f, -4.6f), DrawGreenwakeSignalPixelArt,
                "greenwake_orchard_signal", "greenwake_signal_record");

            var returnRoad = CreateActor("Return to Choir Beneath the Lake", ActorKind.RoadGate,
                new Vector2(-10.1f, -3.5f), CreatePixelSprite("Choir return marker", 28, 36, DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "choir_beneath_lake";
            returnRoad.DestinationPosition = new Vector2(8.7f, 3.0f);
            actors.Add(returnRoad);

            var outerwakeRoad = CreateActor("Outer-Wake Aperture", ActorKind.RoadGate,
                new Vector2(10.0f, 3.8f), CreatePixelSprite("Outer-Wake passage marker", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            outerwakeRoad.DestinationLocationId = "outerwake_archive";
            outerwakeRoad.DestinationPosition = new Vector2(-9.0f, -3.2f);
            outerwakeRoad.RequiredQuestId = "champion_star_map";
            actors.Add(outerwakeRoad);

            var lastOathRoad = CreateActor("The Last Threshold", ActorKind.RoadGate,
                new Vector2(-1.4f, 4.5f), CreatePixelSprite("Last oath passage marker", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            lastOathRoad.DestinationLocationId = "last_oath_reach";
            lastOathRoad.DestinationPosition = new Vector2(0.0f, -3.5f);
            lastOathRoad.RequiredQuestId = "archive_return_report";
            actors.Add(lastOathRoad);

            BuildEncounterActors("greenwake_refuge");
            var still = CreateActor("Mara Bell's Still House", ActorKind.Workstation, new Vector2(3.2f, -0.9f),
                CreatePixelSprite("Greenwake alchemy still", 36, 32, DrawAlchemyTablePixelArt), 0.085f);
            still.WorkstationId = "greenwake_alchemy_still";
            actors.Add(still);
        }

        private void BuildOuterwakeActors()
        {
            AddOuterwakeWitness("Dr. Evelyn Hart", new Vector2(-7.2f, 0.1f), DrawEvelynHartPixelArt,
                "evelyn_hart", "evelyn_outerwake_arrival");
            AddOuterwakeWitness("Jace Morrow", new Vector2(7.0f, -0.3f), DrawJaceMorrowPixelArt,
                "jace_morrow", "jace_outerwake_briefing");
            AddQuestLandmark("Broken Observatory Lens", new Vector2(-1.8f, 1.2f), DrawOuterwakeLensPixelArt,
                "archive_broken_lens", "rowan_outerwake_lens");
            AddQuestLandmark("Northern Weather Record", new Vector2(-7.7f, 3.0f), DrawOuterwakeRecordPixelArt,
                "archive_weather_north", "rowan_outerwake_weather_record");
            AddQuestLandmark("Southern Weather Record", new Vector2(5.5f, 3.0f), DrawOuterwakeRecordPixelArt,
                "archive_weather_south", "rowan_outerwake_weather_record");
            AddQuestLandmark("Buried Weather Record", new Vector2(-5.7f, -2.7f), DrawOuterwakeRecordPixelArt,
                "archive_weather_buried", "rowan_outerwake_weather_record");
            AddQuestLandmark("North Aperture Anchor", new Vector2(3.9f, 1.8f), DrawOuterwakeAnchorPixelArt,
                "archive_ring_north", "rowan_outerwake_alignment");
            AddQuestLandmark("South Aperture Anchor", new Vector2(1.1f, -3.2f), DrawOuterwakeAnchorPixelArt,
                "archive_ring_south", "rowan_outerwake_alignment");
            AddQuestLandmark("Far-Wake Silt Sample", new Vector2(8.4f, -3.4f), DrawOuterwakeSamplePixelArt,
                "outerwake_far_silt", "rowan_outerwake_sample");
            AddQuestLandmark("Unknown Seed Imprint", new Vector2(-3.5f, -3.4f), DrawGreenwakeLedgerPixelArt,
                "outerwake_seed_imprint", "rowan_outerwake_sample");
            AddQuestLandmark("Public Signal Beacon", new Vector2(-9.1f, 2.3f), DrawOuterwakeTransmitterPixelArt,
                "archive_public_beacon", "rowan_outerwake_public_beacon");
            AddQuestLandmark("Encrypted Signal Relay", new Vector2(9.0f, 1.6f), DrawOuterwakeTransmitterPixelArt,
                "archive_private_relay", "rowan_outerwake_private_relay");
            AddQuestLandmark("Evidence Console", new Vector2(0.0f, -0.5f), DrawOuterwakeTransmitterPixelArt,
                "archive_evidence_choice", "rowan_outerwake_console");
            AddQuestLandmark("The World Will", new Vector2(-0.4f, 3.8f), DrawWorldWillPixelArt,
                "world_will_outerwake", "world_will_outerwake_contact");
            AddQuestLandmark("Outer-Wake Message Plate", new Vector2(1.6f, -2.1f), DrawOuterwakeRecordPixelArt,
                "outerwake_far_signal", "rowan_outerwake_far_signal");
            AddQuestLandmark("Copy of the Star Rubbing", new Vector2(-8.5f, -3.8f), DrawGreenwakeStarChartPixelArt,
                "outerwake_star_copy", "rowan_outerwake_star_copy");
            AddQuestLandmark("Resonant Stone", new Vector2(8.7f, 4.3f), DrawOuterwakeAnchorPixelArt,
                "outerwake_ringing_stone", "rowan_outerwake_ring_sound");
            AddQuestLandmark("Wind Mast Clock", new Vector2(-2.6f, 4.0f), DrawOuterwakeWindMastPixelArt,
                "outerwake_wind_mast", "rowan_outerwake_wind_mast", 34, 42);
            AddQuestLandmark("Celestial Pool Tide Gauge", new Vector2(-4.4f, 0.2f), DrawOuterwakeTideGaugePixelArt,
                "outerwake_tide_gauge", "rowan_outerwake_tide_gauge", 36, 32);
            AddQuestLandmark("Receiver Reply Console", new Vector2(3.3f, 0.0f), DrawOuterwakeReplyConsolePixelArt,
                "outerwake_reply_console", "rowan_outerwake_far_signal", 36, 36);
            AddQuestLandmark("Public Echo Terminal", new Vector2(-5.0f, -4.25f), DrawOuterwakeTransmitterPixelArt,
                "outerwake_echo_receipt", "rowan_outerwake_echo_receipt", 36, 36);
            AddQuestLandmark("Passive Signal Recorder", new Vector2(4.4f, -4.2f), DrawOuterwakeRecordPixelArt,
                "outerwake_passive_record", "rowan_outerwake_passive_record", 36, 36);

            var alchemyBench = CreateActor("Outer-Wake Alchemy Bench", ActorKind.Workstation,
                new Vector2(-8.8f, -0.7f), CreatePixelSprite("Outer-Wake alchemy bench", 36, 32,
                    DrawAlchemyTablePixelArt), 0.085f);
            alchemyBench.WorkstationId = "archive_alchemy_bench";
            actors.Add(alchemyBench);
            var forge = CreateActor("Aperture Forge", ActorKind.Workstation,
                new Vector2(8.5f, -0.7f), CreatePixelSprite("Aperture forge", 36, 32,
                    DrawOuterwakeForgePixelArt), 0.085f);
            forge.WorkstationId = "outerwake_forge";
            actors.Add(forge);

            var returnRoad = CreateActor("Return to Greenwake Refuge", ActorKind.RoadGate,
                new Vector2(-10.0f, -4.4f), CreatePixelSprite("Greenwake return marker", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "greenwake_refuge";
            returnRoad.DestinationPosition = new Vector2(8.5f, 3.0f);
            actors.Add(returnRoad);

            BuildFarmPlotActors("outerwake_archive");
            BuildFishingSpotActors("outerwake_archive");
            BuildEncounterActors("outerwake_archive");
        }

        private void BuildLastOathActors()
        {
            AddOuterwakeWitness("Captain Alden Vale", new Vector2(-7.4f, 0.8f), DrawAldenPixelArt,
                "captain_alden_final", "alden_last_oath_arrival");
            AddOuterwakeWitness("Ada Sloane", new Vector2(8.4f, 2.7f), DrawAdaSloanePixelArt,
                "ada_sloane", "ada_forecast_intro");
            AddQuestLandmark("The World Will", new Vector2(7.3f, 0.8f), DrawWorldWillPixelArt,
                "world_will_final_arrival", "world_will_final_arrival");
            AddQuestLandmark("Last Names Tablet", new Vector2(-4.8f, 2.8f), DrawOuterwakeRecordPixelArt,
                "last_oath_tablet", "rowan_last_oath_records");
            AddQuestLandmark("Empty Crown Cradle", new Vector2(-8.7f, 3.5f), DrawGreenwakeCrownPixelArt,
                "empty_crown_cradle", "rowan_last_oath_records");
            AddQuestLandmark("Outer-Wake Resonance", new Vector2(4.8f, 2.8f), DrawOuterwakeAnchorPixelArt,
                "outerwake_resonance", "rowan_last_oath_records");
            AddQuestLandmark("Oath Cairn", new Vector2(0.0f, 0.2f), DrawOuterwakeTransmitterPixelArt,
                "last_oath_choice", "rowan_last_oath_records");
            AddQuestLandmark("Greenwake Root Testimony", new Vector2(-8.4f, -1.2f), DrawGreenwakeLedgerPixelArt,
                "greenwake_root_testimony", "mara_final_record");
            AddQuestLandmark("Choir Cycle Testimony", new Vector2(-3.7f, -2.7f), DrawOuterwakeRecordPixelArt,
                "choir_cycle_testimony", "lyra_final_record");
            AddQuestLandmark("Outer-Wake Star Testimony", new Vector2(8.2f, -1.3f), DrawGreenwakeStarChartPixelArt,
                "outerwake_star_testimony", "owen_final_record");
            AddQuestLandmark("Cycle Heart", new Vector2(-7.0f, -3.4f), DrawOuterwakeAnchorPixelArt,
                "cycle_heart", "rowan_cycle_epilogue");
            AddQuestLandmark("Departure Beacon", new Vector2(7.2f, -3.4f), DrawOuterwakeTransmitterPixelArt,
                "outerwake_departure", "rowan_beyond_epilogue");
            AddQuestLandmark("Final Roll of Names", new Vector2(-1.8f, -3.8f), DrawOuterwakeRecordPixelArt,
                "final_roster_stone", "rowan_final_roster_stone");
            AddQuestLandmark("Oath Lanterns", new Vector2(2.1f, -3.8f), DrawOuterwakeForgePixelArt,
                "final_oath_lantern", "rowan_final_oath_lantern");
            AddQuestLandmark("Folded Directive", new Vector2(9.0f, 3.5f), DrawOuterwakeRecordPixelArt,
                "worldwill_fold", "rowan_worldwill_fold");
            AddQuestLandmark("Alden's Sword Mark", new Vector2(-9.0f, 0.1f), DrawOuterwakeLensPixelArt,
                "alden_sword_mark", "rowan_alden_sword_mark");
            AddQuestLandmark("Consent Archive Copy Desk", new Vector2(2.6f, -1.7f),
                DrawOuterwakeRecordPixelArt, "last_oath_consent_archive", "");
            AddOuterwakeWitness("The First Warden", new Vector2(0.1f, 3.0f), DrawFirstWardenPixelArt,
                "first_warden_final", "warden_final_memory");

            var forge = CreateActor("Last Oath Anvil", ActorKind.Workstation,
                new Vector2(8.7f, -0.5f), CreatePixelSprite("Last oath anvil", 36, 32,
                    DrawOuterwakeForgePixelArt), 0.085f);
            forge.WorkstationId = "last_oath_forge";
            actors.Add(forge);

            var fieldKitchen = CreateActor("Crownfall Field Stove", ActorKind.Workstation,
                new Vector2(-1.3f, -3.15f), CreatePixelSprite("Crownfall field stove", 38, 34,
                    DrawCinderCupRailPixelArt), 0.085f);
            fieldKitchen.WorkstationId = "last_oath_kitchen";
            actors.Add(fieldKitchen);

            var returnRoad = CreateActor("Return to Outer-Wake Archive", ActorKind.RoadGate,
                new Vector2(0.0f, -4.6f), CreatePixelSprite("Outer-Wake return marker", 28, 36,
                    DrawTravelBeaconPixelArt), 0.08f);
            returnRoad.DestinationLocationId = "outerwake_archive";
            returnRoad.DestinationPosition = new Vector2(-9.0f, -3.2f);
            actors.Add(returnRoad);

            BuildFarmPlotActors("last_oath_reach");
            BuildFishingSpotActors("last_oath_reach");
            BuildEncounterActors("last_oath_reach");
            UpdateLastOathBossVisibility();
        }

        private void AddSaltRoadWitness(string name, Vector2 position, PixelDrawer draw, string targetId,
            string dialogueId)
        {
            var actor = CreateActor(name, ActorKind.SaltRoadWitness, position,
                CreatePixelSprite(name + " pixel sprite", 32, 44, draw), 0.075f);
            actor.ObjectiveTargetId = targetId;
            actor.InteractionDialogueId = dialogueId;
            actors.Add(actor);
        }

        private void AddOuterwakeWitness(string name, Vector2 position, PixelDrawer draw, string targetId,
            string dialogueId)
        {
            var actor = CreateActor(name, ActorKind.StoryLandmark, position,
                CreatePixelSprite(name + " pixel sprite", 32, 44, draw), 0.075f);
            actor.ObjectiveTargetId = targetId;
            actor.InteractionDialogueId = dialogueId;
            actors.Add(actor);
        }

        private void AddQuestLandmark(string name, Vector2 position, PixelDrawer draw, string targetId,
            string dialogueId, int width = 32, int height = 34)
        {
            var actor = CreateActor(name, ActorKind.StoryLandmark, position,
                CreatePixelSprite(name + " pixel marker", width, height, draw), 0.085f);
            actor.ObjectiveTargetId = targetId;
            actor.InteractionDialogueId = dialogueId;
            actors.Add(actor);
        }

        private void BuildEncounterActors(string locationId)
        {
            if (encounterCatalog?.entries == null) return;
            foreach (var encounter in encounterCatalog.entries)
            {
                if (encounter == null || encounter.locationId != locationId) continue;
                var monster = FindMonsterDefinition(encounter.monsterId);
                if (monster == null)
                {
                    Debug.LogError("Encounter " + encounter.id + " refers to a missing monster " + encounter.monsterId + ".");
                    continue;
                }

                var progress = EncounterProgressService.GetOrCreate(save, encounter, monster);
                if (progress == null || progress.defeated) continue;
                var texture = Resources.Load<Texture2D>("Art/" + monster.spriteResource);
                Sprite idleSprite;
                var spritePixelsPerUnit = monster.spritePixelsPerUnit > 0
                    ? monster.spritePixelsPerUnit : 256f;
                if (texture != null)
                    idleSprite = SpriteFromTexture(texture, spritePixelsPerUnit, new Vector2(0.5f, 0.045f));
                else if (monster.id == "ash_warg")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 36, 32, DrawWargPixelArt);
                else if (monster.id == "salt_hound")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 34, DrawSaltHoundPixelArt);
                else if (monster.id == "rustwing_harrier")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 36, DrawRustwingHarrierPixelArt);
                else if (monster.id == "sluice_mite")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 36, 28, DrawSluiceMitePixelArt);
                else if (monster.id == "granary_sentinel")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 38, 46, DrawGranarySentinelPixelArt);
                else if (monster.id == "mold_crowned_reeve")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 44, 48, DrawMoldCrownedReevePixelArt);
                else if (monster.id == "cistern_warden")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 48, 54, DrawCisternWardenPixelArt);
                else if (monster.id == "cinder_pressure_wight")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 44, 48, DrawCinderPressureWightPixelArt);
                else if (monster.id == "glassback_scuttler")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 32, DrawGlassbackScuttlerPixelArt);
                else if (monster.id == "saltroad_scavenger")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 32, DrawSaltroadScavengerPixelArt);
                else if (monster.id == "dune_kite")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 36, DrawDuneKitePixelArt);
                else if (monster.id == "quarry_hollow")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 36, 36, DrawQuarryHollowPixelArt);
                else if (monster.id == "redpass_enforcer")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 46, DrawRedpassEnforcerPixelArt);
                else if (monster.id == "hollow_tollkeeper")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 48, 50, DrawHollowTollkeeperPixelArt);
                else if (monster.id == "salt_lockhouse_ratchet")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 34, DrawSaltLockhouseRatchetPixelArt);
                else if (monster.id == "brineglass_latcher")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 38, 34, DrawBrineglassLatcherPixelArt);
                else if (monster.id == "salt_slag_inspector")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 44, 48, DrawSaltSlagInspectorPixelArt);
                else if (monster.id == "roadglass_sentinel")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 46, 52, DrawRoadglassSentinelPixelArt);
                else if (monster.id == "salt_lockhouse_bailiff")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 50, 54, DrawSaltLockhouseBailiffPixelArt);
                else if (monster.id == "echo_moth")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 36, DrawEchoMothPixelArt);
                else if (monster.id == "siltglass_eel")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 44, 32, DrawSiltglassEelPixelArt);
                else if (monster.id == "bell_crab")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 32, DrawBellCrabPixelArt);
                else if (monster.id == "echo_wisp")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 32, 40, DrawEchoWispPixelArt);
                else if (monster.id == "drowned_cantor")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 48, DrawDrownedCantorPixelArt);
                else if (monster.id == "aegis_cantor")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 48, 52, DrawAegisCantorPixelArt);
                else if (monster.id == "briar_stalker")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 42, 36, DrawBriarStalkerPixelArt);
                else if (monster.id == "lantern_moth")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 40, 36, DrawLanternMothPixelArt);
                else if (monster.id == "seedbound_sentinel")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 42, 48, DrawSeedboundSentinelPixelArt);
                else if (monster.id == "crownward_colossus")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 52, 54, DrawCrownwardColossusPixelArt);
                else if (monster.id == "rift_hound")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 44, 36, DrawRiftHoundPixelArt);
                else if (monster.id == "star_leecher")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 36, 44, DrawStarLeecherPixelArt);
                else if (monster.id == "archive_scribe")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 42, 50, DrawArchiveScribePixelArt);
                else if (monster.id == "asterion_threshold")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 52, 56, DrawAsterionPixelArt);
                else if (monster.id == "veilshard_drake")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 56, 50, DrawVeilshardDrakePixelArt);
                else if (monster.id == "cycle_remnant")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 42, 48, DrawCycleRemnantPixelArt);
                else if (monster.id == "demon_king_alden")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 54, 60, DrawDemonKingAldenPixelArt);
                else if (monster.id == "world_will_avatar")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 54, 58, DrawWorldWillAvatarPixelArt);
                else if (monster.id == "embermaw_matriarch")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 50, 46, DrawEmbermawMatriarchPixelArt);
                else if (monster.id == "ironward_sentinel")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 46, 52, DrawIronwardSentinelPixelArt);
                else if (monster.id == "sluicewheel_colossus")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 52, 54, DrawSluicewheelColossusPixelArt);
                else if (monster.id == "redpass_harrower")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 54, 48, DrawRedpassHarrowerPixelArt);
                else if (monster.id == "deepbell_herald")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 48, 54, DrawDeepbellHeraldPixelArt);
                else if (monster.id == "seedvault_keeper")
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 54, 56, DrawSeedvaultKeeperPixelArt);
                else
                    idleSprite = CreatePixelSprite(monster.displayName + " pixel art", 32, 44, DrawWardenPixelArt);

                var lungeTexture = string.IsNullOrWhiteSpace(monster.lungeSpriteResource)
                    ? null
                    : Resources.Load<Texture2D>("Art/" + monster.lungeSpriteResource);
                var lungeSprite = lungeTexture != null
                    ? SpriteFromTexture(lungeTexture, spritePixelsPerUnit, new Vector2(0.5f, 0.045f))
                    : idleSprite;
                var actor = CreateActor(monster.displayName, ActorKind.Encounter,
                    new Vector2(encounter.positionX, encounter.positionY), idleSprite,
                    texture != null ? monster.spriteScale : 0.085f);
                if (monster.id == "demon_king_alden")
                {
                    var animation = GetAldenAnimationSet();
                    if (animation != null)
                    {
                        actor.IdleAnimationFrames = animation.Idle;
                        actor.RunAnimationFrames = animation.Run;
                        actor.AttackAnimationFrames = animation.Attack;
                        actor.HitAnimationFrames = animation.Hit;
                        actor.DeathAnimationFrames = animation.Death;
                        idleSprite = animation.Idle[0];
                        lungeSprite = animation.Attack[0];
                        actor.IdleSprite = idleSprite;
                        actor.LungeSprite = lungeSprite;
                        actor.Renderer.sprite = idleSprite;
                        actor.Transform.localScale = Vector3.one * monster.spriteScale;
                    }
                }
                actor.Encounter = encounter;
                actor.Monster = monster;
                actor.Progress = progress;
                actor.IdleSprite = idleSprite;
                actor.LungeSprite = lungeSprite;
                actor.RequiresAcceptedSideQuest =
                    QuestCatalogService.FindById(questCatalog, encounter.requiredQuestId)?.type == "side";
                actor.Transform.gameObject.SetActive(!actor.RequiresAcceptedSideQuest ||
                    QuestProgressService.IsActive(save, encounter.requiredQuestId));
                actors.Add(actor);
            }
        }

        private void RefreshSideQuestEncounterVisibility()
        {
            foreach (var actor in actors)
            {
                if (actor == null || !actor.RequiresAcceptedSideQuest || actor.Encounter == null ||
                    actor.Progress == null || actor.Transform == null) continue;
                actor.Transform.gameObject.SetActive(!actor.Progress.defeated &&
                    QuestProgressService.IsActive(save, actor.Encounter.requiredQuestId));
            }
        }

        private void BuildFishingSpotActors(string locationId)
        {
            if (fishingCatalog?.entries == null) return;
            foreach (var spot in fishingCatalog.entries)
            {
                if (spot == null || spot.locationId != locationId) continue;
                var displayName = string.IsNullOrEmpty(spot.displayName) ? "Dawnkeep Lakeshore" : spot.displayName;
                var actor = CreateActor(displayName, ActorKind.FishingSpot,
                    new Vector2(spot.positionX, spot.positionY),
                    CreatePixelSprite(displayName + " fishing marker", 32, 28, DrawFishingSpotPixelArt), 0.085f);
                actor.FishingSpot = spot;
                actors.Add(actor);
            }
        }

        private void BuildFarmPlotActors(string locationId)
        {
            if (farmCatalog?.entries == null) return;
            foreach (var plot in farmCatalog.entries)
            {
                if (plot == null || plot.locationId != locationId) continue;
                var actor = CreateActor(plot.cropDisplayName + " Bed", ActorKind.FarmPlot,
                    new Vector2(plot.positionX, plot.positionY),
                    CreatePixelSprite(plot.cropDisplayName + " garden bed", 36, 24, DrawFarmBedPixelArt), 0.08f);
                actor.FarmPlot = plot;
                actor.FarmBedSprite = actor.Renderer.sprite;
                actor.CropGrowingSprite = plot.cropId == "echo_kelp"
                    ? CreatePixelSprite("Growing " + plot.cropDisplayName, 32, 32, DrawEchoKelpGrowingPixelArt)
                    : plot.cropId == "emberlily"
                        ? CreatePixelSprite("Growing " + plot.cropDisplayName, 32, 32, DrawEmberlilyGrowingPixelArt)
                    : CreatePixelSprite("Growing " + plot.cropDisplayName, 32, 32, DrawFarmGrowingPixelArt);
                actor.CropReadySprite = plot.cropId == "echo_kelp"
                    ? CreatePixelSprite("Harvest ready " + plot.cropDisplayName, 32, 36, DrawEchoKelpReadyPixelArt)
                    : plot.cropId == "emberlily"
                        ? CreatePixelSprite("Harvest ready " + plot.cropDisplayName, 32, 36, DrawEmberlilyReadyPixelArt)
                    : CreatePixelSprite("Harvest ready " + plot.cropDisplayName, 32, 36, DrawFarmReadyPixelArt);
                RefreshFarmPlotVisual(actor);
                actors.Add(actor);
            }
        }

        private WorldActor CreateActor(string name, ActorKind kind, Vector2 position, Sprite sprite, float scale)
        {
            var actor = new GameObject(name);
            actor.transform.SetParent(worldRoot, false);
            actor.transform.position = new Vector3(position.x, position.y, 0);
            actor.transform.localScale = Vector3.one * scale;
            var renderer = actor.AddComponent<SpriteRenderer>();
            renderer.sprite = sprite;
            renderer.sortingOrder = 3;
            return new WorldActor
            {
                Name = name,
                Kind = kind,
                Transform = actor.transform,
                BasePosition = actor.transform.position,
                Renderer = renderer
            };
        }

        public void Interact()
        {
            if (mode == PlayMode.Fishing)
            {
                CancelFishing();
                return;
            }
            if (mode != PlayMode.Exploring) return;
            var actor = FindClosestActor();
            if (actor == null)
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_no_nearby", () => mode = PlayMode.Exploring);
                return;
            }

            if (actor.Kind == ActorKind.RoadGate)
            {
                if (!string.IsNullOrEmpty(actor.RequiredQuestId) && !IsQuestCompleted(actor.RequiredQuestId)) return;
                if (!string.IsNullOrEmpty(actor.DestinationLocationId))
                    TravelTo(actor.DestinationLocationId, actor.DestinationPosition);
                return;
            }

            if (actor.Kind == ActorKind.Workstation)
            {
                OpenCraftMenu(actor);
                return;
            }

            if (actor.Kind == ActorKind.FarmPlot)
            {
                OpenFarmMenu(actor);
                return;
            }

            if (actor.Kind == ActorKind.SisterJune)
            {
                InteractWithSisterJune();
                return;
            }

            if (actor.Kind == ActorKind.TaliaMercer)
            {
                if (QuestProgressService.IsActive(save, "side_saltroad_talia_review"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("talia_saltroadglass_review", () =>
                        CompleteBranchObjective("talk", "talia_mercer"));
                }
                else if (QuestProgressService.IsActive(save, "side_cinderwell_valve_intervals"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("talia_cinder_measure_intervals", () =>
                        CompleteBranchObjective("talk", "talia_mercer"));
                }
                else if (QuestProgressService.IsActive(save, "cinder_sluice_map"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("talia_mercer_sluice_map", () => CompleteBranchObjective("talk", "talia_mercer"));
                }
                else if (QuestProgressService.IsActive(save, "cinder_talia_testimony"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("talia_mercer_cistern_testimony", () =>
                        CompleteBranchObjective("talk", "talia_mercer"));
                }
                else
                {
                    TryInteractWithQuestTalker("talia_mercer");
                }
                return;
            }

            if (actor.Kind == ActorKind.OrenBell)
            {
                if (QuestProgressService.IsActive(save, "side_cinderwell_seed_weights"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("oren_cinder_seed_weight", () =>
                        CompleteBranchObjective("talk", "oren_bell"));
                }
                else if (QuestProgressService.IsActive(save, "cinder_water_reserve"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("oren_bell_seed_reserve", () => CompleteBranchObjective("talk", "oren_bell"));
                }
                else
                {
                    TryInteractWithQuestTalker("oren_bell");
                }
                return;
            }

            if (actor.Kind == ActorKind.SaltRoadWitness)
            {
                InteractWithSaltRoadWitness(actor);
                return;
            }

            if (actor.Kind == ActorKind.StoryLandmark)
            {
                if (QuestProgressService.IsActive(save, "champion_offer"))
                {
                    ShowChampionOfferChoice();
                    return;
                }
                InteractWithQuestLandmark(actor);
                return;
            }

            if (actor.Kind == ActorKind.Mira)
            {
                if (TryInteractWithMiraAshfallHouseRoute()) return;
                if (TryInteractWithQuestTalker("mira_cole"))
                {
                    return;
                }
                if (QuestProgressService.IsActive(save, "ashfall_survivors"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("mira_survivors", () =>
                    {
                        mode = PlayMode.Exploring;
                        RecordCurrentObjective("talk", "mira_cole");
                    });
                }
                else if (QuestProgressService.IsActive(save, "ashfall_warg"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("mira_warg", () => mode = PlayMode.Exploring);
                }
                else if (QuestProgressService.IsActive(save, "ashfall_choice"))
                {
                    ShowVillageChoice();
                }
                else if (QuestProgressService.IsActive(save, "ashfall_shelter_witness") ||
                         QuestProgressService.IsActive(save, "ashfall_trail_evidence"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue(QuestProgressService.GetStoryFlag(save, "first_choice") == "shelter"
                        ? "mira_shelter_hint" : "mira_trail_hint", () => mode = PlayMode.Exploring);
                }
                else if (QuestProgressService.IsActive(save, "ashfall_shelter_report") ||
                         QuestProgressService.IsActive(save, "ashfall_trail_report"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("mira_report_hint", () => mode = PlayMode.Exploring);
                }
                else if (IsOrderArcUnlocked() || save.chapterComplete)
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue(IsQuestCompleted("salt_reckoning") ? "mira_salt_reckoning" :
                        IsQuestCompleted("cinder_recovery") ? "mira_cinder_recovery" : "mira_chapter_end",
                        () => mode = PlayMode.Exploring);
                }
                else
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("mira_pending", () => mode = PlayMode.Exploring);
                }
            }
            else if (actor.Kind == ActorKind.SurvivorWitness)
            {
                if (QuestProgressService.IsActive(save, "ashfall_shelter_witness"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("gideon_evidence", () => CompleteBranchObjective("talk", "gideon_park"));
                }
                else if (HasActiveObjectiveTarget(actor.ObjectiveTargetId))
                {
                    InteractWithQuestLandmark(actor);
                }
            }
            else if (actor.Kind == ActorKind.SealClue)
            {
                if (!QuestProgressService.IsActive(save, "ashfall_trail_evidence")) return;
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_seal_inspection", () => CompleteBranchObjective("inspect", "ashfall_burned_seal"));
            }
            else if (actor.Kind == ActorKind.CaptainAlden)
            {
                if (QuestProgressService.IsActive(save, "order_alden_reckoning"))
                {
                    var dialogueId = QuestProgressService.GetStoryFlag(save, "order_testimony") == "publish"
                        ? "alden_order_reckoning_publish" : "alden_order_reckoning_seal";
                    mode = PlayMode.Dialogue;
                    ShowDialogue(dialogueId, () => CompleteBranchObjective("talk", "captain_alden_vale"));
                    return;
                }

                if (QuestProgressService.IsActive(save, "order_trial_report"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("captain_trial_report", () => CompleteBranchObjective("talk", "captain_alden_vale"));
                    return;
                }

                if (QuestProgressService.IsActive(save, "order_record_choice"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("captain_roster_brief", ShowOrderDisclosureChoice);
                    return;
                }

                var isShelterReport = QuestProgressService.IsActive(save, "ashfall_shelter_report");
                var isTrailReport = QuestProgressService.IsActive(save, "ashfall_trail_report");
                if (!isShelterReport && !isTrailReport) return;
                mode = PlayMode.Dialogue;
                ShowDialogue(isShelterReport ? "captain_shelter_report" : "captain_trail_report",
                    CompleteAshfallPrologue);
            }
            else if (actor.Kind == ActorKind.ElaraWren)
            {
                if (QuestProgressService.IsActive(save, "order_evidence_choice"))
                {
                    ShowOrderTestimonyChoice();
                    return;
                }

                if (QuestProgressService.IsActive(save, "order_arrival"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("elara_arrival", () => CompleteBranchObjective("talk", "elara_wren"));
                }
                else if (QuestProgressService.IsActive(save, "order_roster"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("elara_roster_hint", () => mode = PlayMode.Exploring);
                }
                else if (QuestProgressService.IsActive(save, "order_archive_public"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("elara_public_response", () => CompleteBranchObjective("talk", "elara_wren"));
                }
                else if (QuestProgressService.IsActive(save, "order_archive_private"))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("elara_private_response", () => CompleteBranchObjective("talk", "elara_wren"));
                }
                else
                {
                    TryInteractWithQuestTalker("elara_wren");
                }
            }
            else if (actor.Kind == ActorKind.DawnkeepRoster)
            {
                mode = PlayMode.Dialogue;
                var isOriginQuestion = QuestProgressService.IsActive(save, "order_roster_origin");
                ShowDialogue(isOriginQuestion ? "rowan_roster_origin_inspection" : "rowan_roster_inspection", () =>
                    CompleteBranchObjective("inspect", isOriginQuestion ? "dawnkeep_roster_origin" : "dawnkeep_roster"));
            }
            else if (actor.Kind == ActorKind.FishingSpot)
            {
                BeginFishing(actor);
            }
            else if (actor.Kind == ActorKind.Encounter)
            {
                if (!string.IsNullOrEmpty(actor.Encounter.blockedQuestId) &&
                    QuestProgressService.IsActive(save, actor.Encounter.blockedQuestId))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue(actor.Encounter.blockedDialogueId, () => mode = PlayMode.Exploring);
                    return;
                }

                if (QuestProgressService.IsActive(save, actor.Encounter.requiredQuestId)) BeginCombat(actor);
            }
        }

        private void CompleteBranchObjective(string kind, string targetId)
        {
            mode = PlayMode.Exploring;
            if (kind == "interact" && targetId == "ashfall_signal_mark" &&
                !InventoryService.Remove(save, "rainmark_chalk", 1))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("mira_two_bells_chalk_missing", () => mode = PlayMode.Exploring);
                return;
            }
            RecordCurrentObjective(kind, targetId);
            if (save.chapterComplete && string.IsNullOrEmpty(save.endingId)) ShowFinalEnding();
        }

        private void ShowFinalEnding()
        {
            var oath = QuestProgressService.GetStoryFlag(save, "last_oath");
            if (oath == "cycle")
            {
                save.endingId = "crown_of_ash";
                SaveNow();
                mode = PlayMode.Ending;
                hud.ShowEnding("CROWN OF ASH", "Rowan nhận chiếc Crown và đối đầu Captain Alden Vale để chấm dứt lời thề cũ bằng một lời thề mới. Chu kỳ tiếp tục, nhưng danh sách tên được giữ nguyên. Bình minh trở lại; món nợ vẫn thuộc về những người còn sống.", ContinueAfterEnding);
            }
            else if (oath == "beyond")
            {
                save.endingId = "beyond_the_veil";
                SaveNow();
                mode = PlayMode.Ending;
                hud.ShowEnding("BEYOND THE VEIL", "Rowan giữ được hiện trạng và rời Asterra bằng bản đồ sao đã được kiểm chứng. The World Will không hứa rằng miền ngoài Veil có thể cứu thế giới. Người ở lại sẽ tự quyết định cách chia nước, đất và tương lai.", ContinueAfterEnding);
            }
        }

        private void ContinueAfterEnding()
        {
            mode = PlayMode.Exploring;
            PlayExplorationMusic();
            SaveNow();
            RefreshHud();
        }

        private void CompleteAshfallPrologue()
        {
            mode = PlayMode.Exploring;
            RecordCurrentObjective("talk", "captain_alden_vale");
        }

        private void InteractWithSisterJune()
        {
            if (QuestProgressService.IsActive(save, "side_june_pantry_open"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("june_stonepot_open", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "side_june_pantry_table_report"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("june_stonepot_table_report", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "side_june_pantry_departure_report"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("june_stonepot_departure_report", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "side_june_pantry_afterword"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("june_stonepot_afterword", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "cinder_arrival"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("sister_june_cinder_arrival", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "cinder_water_rights"))
            {
                ShowCinderWaterChoice();
            }
            else if (QuestProgressService.IsActive(save, "cinder_water_refugees"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("sister_june_refugee_route", () => mode = PlayMode.Exploring);
            }
            else if (QuestProgressService.IsActive(save, "cinder_recovery"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("sister_june_cinder_recovery", () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "cinder_june_report"))
            {
                var dialogueId = QuestProgressService.GetStoryFlag(save, "basin_water_rights") == "refugees"
                    ? "sister_june_cistern_report_refugees" : "sister_june_cistern_report_reserve";
                mode = PlayMode.Dialogue;
                ShowDialogue(dialogueId, () => CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "side_cinderwell_measure_start"))
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("june_cinderwell_measure_start", () =>
                    CompleteBranchObjective("talk", "sister_june"));
            }
            else if (QuestProgressService.IsActive(save, "side_cinderwell_record_choice"))
            {
                ShowCinderwellRecordChoice();
            }
            else
            {
                TryInteractWithQuestTalker("sister_june");
            }
        }

        private void InteractWithQuestLandmark(WorldActor actor)
        {
            if (actor == null || string.IsNullOrEmpty(actor.ObjectiveTargetId)) return;
            if (actor.ObjectiveTargetId == "crownfall_open_meal_table" &&
                HasActiveObjective("interact", "crownfall_open_meal_table") &&
                InventoryService.Count(save, "crownfall_starlit_pottage") < 1)
            {
                var meal = ItemCatalog.Find("crownfall_starlit_pottage");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    meal == null ? "Crownfall Emberroot Pottage" : meal.name);
                return;
            }
            if (actor.ObjectiveTargetId == "cinder_filter_housing" &&
                HasActiveObjective("interact", "cinder_filter_housing") &&
                InventoryService.Count(save, "cinder_moss_filter") < 1)
            {
                var filter = ItemCatalog.Find("cinder_moss_filter");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    filter == null ? "Màng Lọc Rêu Kính" : filter.name);
                return;
            }
            if ((actor.ObjectiveTargetId == "saltroad_beacon_mount" ||
                 actor.ObjectiveTargetId == "ruth_manifest_lightbox") &&
                HasActiveObjective("interact", actor.ObjectiveTargetId) &&
                InventoryService.Count(save, "saltroad_beacon_lens") < 1)
            {
                var lens = ItemCatalog.Find("saltroad_beacon_lens");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    lens == null ? "Tấm Kính Chia Tia" : lens.name);
                return;
            }
            if (actor.ObjectiveTargetId == "pike_tag_sleeve_frame" &&
                HasActiveObjective("interact", "pike_tag_sleeve_frame") &&
                InventoryService.Count(save, "pike_tag_sleeve") < 1)
            {
                var sleeve = ItemCatalog.Find("pike_tag_sleeve");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    sleeve == null ? "Removable Tag Sleeve" : sleeve.name);
                return;
            }
            if (actor.ObjectiveTargetId == "choir_signal_housing" &&
                HasActiveObjective("interact", "choir_signal_housing") &&
                InventoryService.Count(save, "choir_pulse_brace") < 1)
            {
                var brace = ItemCatalog.Find("choir_pulse_brace");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    brace == null ? "Bộ Chặn Xung" : brace.name);
                return;
            }
            if (actor.ObjectiveTargetId == "elara_garden_rain_housing" &&
                HasActiveObjective("interact", "elara_garden_rain_housing") &&
                InventoryService.Count(save, "dawnkeep_runoff_clip") < 1)
            {
                var clip = ItemCatalog.Find("dawnkeep_runoff_clip");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    clip == null ? "East Gutter Runoff Clip" : clip.name);
                return;
            }
            if (actor.ObjectiveTargetId == "ashfall_cart_wheel" &&
                HasActiveObjective("interact", "ashfall_cart_wheel") &&
                InventoryService.Count(save, "ashfall_cart_axle_pin") < 1)
            {
                var pin = ItemCatalog.Find("ashfall_cart_axle_pin");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    pin == null ? "Ashfall Cart Axle Pin" : pin.name);
                return;
            }
            if (actor.ObjectiveTargetId == "regional_jaw_test" &&
                HasActiveObjective("interact", "regional_jaw_test") &&
                InventoryService.Count(save, "regional_fit_gauge") < 1)
            {
                var gauge = ItemCatalog.Find("regional_fit_gauge");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    gauge == null ? "Adjustable Field Jaw Gauge" : gauge.name);
                return;
            }
            if (actor.ObjectiveTargetId == "pella_rootwall_joint" &&
                HasActiveObjective("interact", "pella_rootwall_joint") &&
                InventoryService.Count(save, "greenwake_rootwall_resin") < 1)
            {
                var resin = ItemCatalog.Find("greenwake_rootwall_resin");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    resin == null ? "Nhựa Mấu Rễ" : resin.name);
                return;
            }
            if ((actor.ObjectiveTargetId == "june_common_table" ||
                 actor.ObjectiveTargetId == "june_departure_crate") &&
                HasActiveObjective("interact", actor.ObjectiveTargetId) &&
                InventoryService.Count(save, "cinderwell_stonepot_broth") < 1)
            {
                var broth = ItemCatalog.Find("cinderwell_stonepot_broth");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    broth == null ? "Stone-Pot Broth" : broth.name);
                return;
            }
            if (actor.ObjectiveTargetId == "ashfall_signal_mark" &&
                HasActiveObjective("interact", "ashfall_signal_mark") &&
                InventoryService.Count(save, "rainmark_chalk") < 1)
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("mira_two_bells_chalk_missing", () => mode = PlayMode.Exploring);
                return;
            }
            if (actor.ObjectiveTargetId == "outerwake_reply_console" &&
                QuestProgressService.IsActive(save, "side_outerwake_reply_choice"))
            {
                ShowOuterwakeReplyChoice();
                return;
            }
            var storyQuest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (storyQuest?.id == "choir_memory_choice" && actor.ObjectiveTargetId == "lyra_moss")
            {
                ShowChoirChoice();
                return;
            }
            if (storyQuest?.id == "archive_evidence_choice" &&
                actor.ObjectiveTargetId == "archive_evidence_choice")
            {
                ShowOuterwakeEvidenceChoice();
                return;
            }
            if (storyQuest?.id == "last_oath_choice" && actor.ObjectiveTargetId == "last_oath_choice")
            {
                ShowLastOathChoice();
                return;
            }
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
            {
                if (quest.objectives == null) continue;
                var dialogueId = ResolveLandmarkDialogue(quest, actor);
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || objective.targetId != actor.ObjectiveTargetId ||
                        IsObjectiveComplete(quest, objective)) continue;
                    if (objective.kind == "choice" && quest.choices != null && quest.choices.Count >= 2)
                    {
                        var options = new List<DialogueChoiceOption>();
                        foreach (var choice in quest.choices)
                            options.Add(new DialogueChoiceOption(choice.id, choice.label));
                        mode = PlayMode.Dialogue;
                        hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options,
                            choiceId => CompleteLandmarkChoice(quest.id, objective.targetId, choiceId));
                        return;
                    }

                    var objectiveDialogueId = !string.IsNullOrEmpty(objective.dialogueId)
                        ? objective.dialogueId : dialogueId;
                    mode = PlayMode.Dialogue;
                    ShowDialogue(objectiveDialogueId, objective.kind == "interact" &&
                        actor.ObjectiveTargetId == "cinder_filter_housing"
                            ? CompleteCinderFilterTest
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "saltroad_beacon_mount"
                                ? CompleteSaltRoadBeaconInstallation
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "ruth_manifest_lightbox"
                                ? CompleteRuthManifestLightbox
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "pike_tag_sleeve_frame"
                                ? CompleteNellaTagSleeveInstall
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "choir_signal_housing"
                                    ? CompleteChoirSignalHousing
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "elara_garden_rain_housing"
                                    ? CompleteDawnkeepGardenClipInstall
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "ashfall_cart_wheel"
                                    ? () => CompleteAshfallCartWheelRepair(actor)
                            : objective.kind == "interact" &&
                                  (actor.ObjectiveTargetId == "june_common_table" ||
                                   actor.ObjectiveTargetId == "june_departure_crate")
                                    ? () => CompleteJuneMealService(actor.ObjectiveTargetId)
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "mira_emberlily_handoff"
                                    ? CompleteMiraBalmHandoff
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "crownfall_open_meal_table"
                                    ? CompleteCrownfallOpenMealService
                            : objective.kind == "interact" && actor.ObjectiveTargetId == "pella_rootwall_joint"
                                ? () => CompleteGreenwakeRootwallInstallation(actor)
                                : (Action)(() => CompleteBranchObjective(objective.kind, actor.ObjectiveTargetId)));
                    return;
                }
            }
        }

        private void CompleteCinderFilterTest()
        {
            if (!InventoryService.Remove(save, "cinder_moss_filter", 1))
            {
                var filter = ItemCatalog.Find("cinder_moss_filter");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    filter == null ? "Màng Lọc Rêu Kính" : filter.name);
                return;
            }
            CompleteBranchObjective("interact", "cinder_filter_housing");
        }

        private void CompleteSaltRoadBeaconInstallation()
        {
            if (!InventoryService.Remove(save, "saltroad_beacon_lens", 1))
            {
                var lens = ItemCatalog.Find("saltroad_beacon_lens");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    lens == null ? "Tấm Kính Chia Tia" : lens.name);
                return;
            }
            CompleteBranchObjective("interact", "saltroad_beacon_mount");
        }

        private void CompleteRuthManifestLightbox()
        {
            if (!InventoryService.Remove(save, "saltroad_beacon_lens", 1))
            {
                var lens = ItemCatalog.Find("saltroad_beacon_lens");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    lens == null ? "Tấm Kính Chia Tia" : lens.name);
                return;
            }
            CompleteBranchObjective("interact", "ruth_manifest_lightbox");
        }

        private void CompleteNellaTagSleeveInstall()
        {
            if (!InventoryService.Remove(save, "pike_tag_sleeve", 1))
            {
                var sleeve = ItemCatalog.Find("pike_tag_sleeve");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    sleeve == null ? "Removable Tag Sleeve" : sleeve.name);
                return;
            }
            CompleteBranchObjective("interact", "pike_tag_sleeve_frame");
        }

        private void CompleteChoirSignalHousing()
        {
            if (!InventoryService.Remove(save, "choir_pulse_brace", 1))
            {
                var brace = ItemCatalog.Find("choir_pulse_brace");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    brace == null ? "Bộ Chặn Xung" : brace.name);
                return;
            }
            CompleteBranchObjective("interact", "choir_signal_housing");
        }

        private void CompleteDawnkeepGardenClipInstall()
        {
            if (!InventoryService.Remove(save, "dawnkeep_runoff_clip", 1))
            {
                var clip = ItemCatalog.Find("dawnkeep_runoff_clip");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    clip == null ? "East Gutter Runoff Clip" : clip.name);
                return;
            }
            CompleteBranchObjective("interact", "elara_garden_rain_housing");
        }

        private void CompleteAshfallCartWheelRepair(WorldActor actor)
        {
            if (!InventoryService.Remove(save, "ashfall_cart_axle_pin", 1))
            {
                var pin = ItemCatalog.Find("ashfall_cart_axle_pin");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    pin == null ? "Ashfall Cart Axle Pin" : pin.name);
                return;
            }

            if (actor != null && actor.Renderer != null)
            {
                actor.Renderer.sprite = CreatePixelSprite("Repaired Ashfall cart", 48, 42,
                    DrawAshfallCartRepairedPixelArt);
                actor.Renderer.enabled = true;
            }
            CompleteBranchObjective("interact", "ashfall_cart_wheel");
        }

        private void CompleteGreenwakeRootwallInstallation(WorldActor actor)
        {
            if (!InventoryService.Remove(save, "greenwake_rootwall_resin", 1))
            {
                var resin = ItemCatalog.Find("greenwake_rootwall_resin");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    resin == null ? "Nhựa Mấu Rễ" : resin.name);
                return;
            }

            var hingeMethod = QuestProgressService.GetStoryFlag(save, "greenwake_rootwall_method") == "breathing_hinge";
            if (actor != null && actor.Renderer != null)
            {
                actor.Renderer.sprite = CreatePixelSprite(
                    hingeMethod ? "Greenwake breathing rootwall joint" : "Greenwake seasonal rootwall shim",
                    48, 40, hingeMethod ? DrawGreenwakeBreathingRootwallPixelArt : DrawGreenwakeSeasonalRootwallPixelArt);
                actor.Renderer.enabled = true;
            }
            CompleteBranchObjective("interact", "pella_rootwall_joint");
        }

        private void CompleteJuneMealService(string targetId)
        {
            if (!InventoryService.Remove(save, "cinderwell_stonepot_broth", 1))
            {
                var broth = ItemCatalog.Find("cinderwell_stonepot_broth");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    broth == null ? "Stone-Pot Broth" : broth.name);
                return;
            }
            CompleteBranchObjective("interact", targetId);
        }

        private void CompleteCrownfallOpenMealService()
        {
            if (!InventoryService.Remove(save, "crownfall_starlit_pottage", 1))
            {
                var meal = ItemCatalog.Find("crownfall_starlit_pottage");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    meal == null ? "Crownfall Emberroot Pottage" : meal.name);
                return;
            }

            CompleteBranchObjective("interact", "crownfall_open_meal_table");
        }

        private void CompleteMiraBalmHandoff()
        {
            if (!InventoryService.Remove(save, "mira_emberlily_balm", 1))
            {
                var balm = ItemCatalog.Find("mira_emberlily_balm");
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring, "{item}",
                    balm == null ? "Emberlily Balm" : balm.name);
                return;
            }
            CompleteBranchObjective("interact", "mira_emberlily_handoff");
        }

        private void CompleteLandmarkChoice(string questId, string targetId, string choiceId)
        {
            var quest = QuestCatalogService.FindById(questCatalog, questId);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null || !QuestProgressService.IsActive(save, questId))
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", targetId, choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.dialogueId, () => mode = PlayMode.Exploring);
        }

        private string ResolveLandmarkDialogue(QuestDefinition quest, WorldActor actor)
        {
            if (quest == null || actor == null) return actor?.InteractionDialogueId ?? "";
            if (quest.id == "side_dawnkeep_waterline" && actor.ObjectiveTargetId == "nia_porter")
                return "nia_waterline_start";
            if (quest.id == "side_dawnkeep_nia_report" && actor.ObjectiveTargetId == "nia_porter")
                return "nia_waterline_report";
            if (quest.id == "side_cinderwell_cup_rail") return "rowan_cinder_cup_rail";
            if (quest.id == "side_cinderwell_seed_weights") return "rowan_cinder_seed_scale";
            if (quest.id == "side_cinderwell_named_schedule") return "rowan_cinder_named_schedule";
            if (quest.id == "side_cinderwell_aggregate_schedule") return "rowan_cinder_aggregate_schedule";
            if (quest.id == "side_outerwake_repeat_signal") return "evelyn_outerwake_repeat_signal";
            if (quest.id == "side_outerwake_wind_clock")
                return actor.ObjectiveTargetId == "jace_morrow" ? "jace_outerwake_wind_clock" : "rowan_outerwake_wind_mast";
            if (quest.id == "side_outerwake_tide_record") return "rowan_outerwake_tide_gauge";
            if (quest.id == "side_outerwake_signal_phase")
                return actor.ObjectiveTargetId == "evelyn_hart" ? "evelyn_outerwake_phase_report" : "rowan_outerwake_signal_phase";
            if (quest.id == "side_outerwake_bounded_echo") return "rowan_outerwake_echo_receipt";
            if (quest.id == "side_outerwake_listen_only") return "rowan_outerwake_passive_record";
            if (quest.id == "choir_reckoning" && actor.ObjectiveTargetId == "first_warden")
                return "first_warden_choir_reckoning";
            if (quest.id == "champion_accept_oath" && actor.ObjectiveTargetId == "owen_reed")
                return "owen_accept_power";
            if (quest.id == "champion_keep_name" && actor.ObjectiveTargetId == "mara_bell")
                return "mara_keep_name";
            switch (quest.id)
            {
                case "order_empty_cots": return "rowan_order_empty_cots";
                case "order_cadet_testimony": return "nia_order_testimony";
                case "order_transfer_ledger": return "rowan_order_transfer_ledger";
                case "order_open_testimony": return "rowan_order_public_record";
                case "order_sealed_record": return "rowan_order_sealed_record";
                case "order_cinderwell_dispatch": return "rowan_order_cinderwell_dispatch";
                case "order_alden_reckoning":
                    return QuestProgressService.GetStoryFlag(save, "order_testimony") == "publish"
                        ? "alden_order_reckoning_publish" : "alden_order_reckoning_seal";
                case "order_cadet_oath":
                    return QuestProgressService.GetStoryFlag(save, "order_testimony") == "publish"
                        ? "nia_order_oath_publish" : "nia_order_oath_seal";
                case "archive_arrival": return "evelyn_outerwake_arrival";
                case "archive_briefing": return "jace_outerwake_briefing";
                case "archive_lens_survey": return "rowan_outerwake_lens";
                case "archive_weather_records": return "rowan_outerwake_weather_record";
                case "archive_alignment": return "rowan_outerwake_alignment";
                case "archive_outer_samples": return "rowan_outerwake_sample";
                case "archive_public_testimony": return "rowan_outerwake_public_beacon";
                case "archive_private_testimony": return "rowan_outerwake_private_relay";
                case "archive_world_will": return "world_will_outerwake_contact";
                case "archive_star_message": return "rowan_outerwake_far_signal";
                case "archive_return_report": return "evelyn_outerwake_report";
                case "last_oath_arrival":
                    return actor.ObjectiveTargetId == "captain_alden_final" ? "alden_last_oath_arrival" :
                        "world_will_final_arrival";
                case "last_oath_records": return "rowan_last_oath_records";
                case "last_oath_cycle_vow": return "alden_final_vow";
                case "last_oath_cycle_epilogue": return "rowan_cycle_epilogue";
                case "last_oath_beyond_epilogue": return "rowan_beyond_epilogue";
                default: return actor.InteractionDialogueId;
            }
        }

        private void ShowOuterwakeEvidenceChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseOuterwakeEvidence);
        }

        private void ChooseOuterwakeEvidence(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "archive_evidence_choice", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "public" ? "rowan_outerwake_choice_public" :
                "rowan_outerwake_choice_private", () => mode = PlayMode.Exploring);
        }

        private void ShowOuterwakeReplyChoice()
        {
            var quest = QuestCatalogService.FindById(questCatalog, "side_outerwake_reply_choice");
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseOuterwakeReply);
        }

        private void ChooseOuterwakeReply(string choiceId)
        {
            var quest = QuestCatalogService.FindById(questCatalog, "side_outerwake_reply_choice");
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null || !QuestProgressService.IsActive(save, quest.id))
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "outerwake_reply_console", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "bounded_echo" ? "rowan_outerwake_bounded_choice" :
                "rowan_outerwake_listen_choice", () => mode = PlayMode.Exploring);
        }

        private void ShowLastOathChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseLastOath);
        }

        private void ChooseLastOath(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "last_oath_choice", choice.reward);
            UpdateLastOathBossVisibility();
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "cycle" ? "rowan_last_oath_choice_cycle" :
                "rowan_last_oath_choice_beyond", () => mode = PlayMode.Exploring);
        }

        private void UpdateLastOathBossVisibility()
        {
            if (save == null || save.locationId != "last_oath_reach") return;
            var oath = QuestProgressService.GetStoryFlag(save, "last_oath");
            foreach (var actor in actors)
            {
                if (actor?.Encounter == null || actor.Transform == null) continue;
                if (actor.Encounter.id == "last_oath_demon_king")
                    actor.Transform.gameObject.SetActive(oath == "cycle" && !actor.Progress.defeated);
                else if (actor.Encounter.id == "last_oath_world_will")
                    actor.Transform.gameObject.SetActive(oath == "beyond" && !actor.Progress.defeated);
            }
        }

        private void ShowChampionOfferChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseChampionOffer);
        }

        private void ChooseChampionOffer(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "champion_offer", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "accept" ? "rowan_champion_accept_choice" :
                "rowan_champion_refuse_choice", () => mode = PlayMode.Exploring);
        }

        private void InteractWithSaltRoadWitness(WorldActor actor)
        {
            if (actor == null) return;
            if (QuestProgressService.IsActive(save, "salt_route_choice") && actor.ObjectiveTargetId == "ruth_calder")
            {
                ShowSaltRoadChoice();
                return;
            }
            if (!HasActiveObjective("talk", actor.ObjectiveTargetId)) return;

            var dialogueId = actor.InteractionDialogueId;
            if (QuestProgressService.IsActive(save, "salt_account_caravan"))
                dialogueId = "ruth_caravan_account";
            else if (QuestProgressService.IsActive(save, "salt_account_refugees"))
                dialogueId = "nella_refugee_account";
            else if (QuestProgressService.IsActive(save, "salt_account_hunters"))
                dialogueId = "silas_hunter_account";
            else if (QuestProgressService.IsActive(save, "salt_reckoning"))
            {
                var testimony = QuestProgressService.GetStoryFlag(save, "salt_testimony");
                dialogueId = testimony == "refugees" ? "ruth_reckoning_refugees" :
                    testimony == "hunters" ? "ruth_reckoning_hunters" : "ruth_reckoning_caravan";
            }
            else if (QuestProgressService.IsActive(save, "salt_route_handoff"))
                dialogueId = "ruth_salt_handoff";

            var authoredSideDialogue = FindActiveSideObjectiveDialogueId(actor.ObjectiveTargetId);
            if (!string.IsNullOrEmpty(authoredSideDialogue)) dialogueId = authoredSideDialogue;

            mode = PlayMode.Dialogue;
            ShowDialogue(dialogueId, () => CompleteBranchObjective("talk", actor.ObjectiveTargetId));
        }

        private string FindActiveSideObjectiveDialogueId(string targetId)
        {
            if (save?.activeSideQuestIds == null || string.IsNullOrEmpty(targetId)) return string.Empty;
            foreach (var questId in save.activeSideQuestIds)
            {
                if (string.IsNullOrEmpty(questId)) continue;
                var quest = QuestCatalogService.FindById(questCatalog, questId);
                foreach (var objective in quest?.objectives ?? new List<QuestObjectiveDefinition>())
                    if (objective != null && objective.kind == "talk" && objective.targetId == targetId &&
                        !IsObjectiveComplete(quest, objective) && !string.IsNullOrEmpty(objective.dialogueId))
                        return objective.dialogueId;
            }
            return string.Empty;
        }

        private void ShowCinderWaterChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseCinderWaterRight);
        }

        private void ShowCinderwellRecordChoice()
        {
            var quest = QuestCatalogService.FindById(questCatalog, "side_cinderwell_record_choice");
            if (!QuestProgressService.IsActive(save, quest?.id) || quest?.choices == null || quest.choices.Count < 2)
                return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseCinderwellRecordFormat);
        }

        private void ChooseCinderwellRecordFormat(string choiceId)
        {
            var quest = QuestCatalogService.FindById(questCatalog, "side_cinderwell_record_choice");
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (!QuestProgressService.IsActive(save, quest?.id) || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "cinderwell_record_format", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "consented_households" ? "rowan_cinder_names_choice" :
                "rowan_cinder_totals_choice", () => mode = PlayMode.Exploring);
        }

        private void ChooseCinderWaterRight(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "cinder_water_rights_choice", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "refugees" ? "rowan_choice_water_refugees" : "rowan_choice_water_reserve",
                () => mode = PlayMode.Exploring);
        }

        private void ShowSaltRoadChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseSaltRoadTestimony);
        }

        private void ShowChoirChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2) return;
            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseChoirTestimony);
        }

        private void ChooseChoirTestimony(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "choir_memory_choice", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "preserve" ? "rowan_memory_preserve" : "rowan_memory_release",
                () => mode = PlayMode.Exploring);
        }

        private void ChooseSaltRoadTestimony(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "salt_road_testimony_choice", choice.reward);
            mode = PlayMode.Dialogue;
            var dialogueId = choice.flagValue == "refugees" ? "rowan_salt_choice_refugees" :
                choice.flagValue == "hunters" ? "rowan_salt_choice_hunters" : "rowan_salt_choice_caravan";
            ShowDialogue(dialogueId, () => mode = PlayMode.Exploring);
        }

        private bool RecordCurrentObjective(string kind, string targetId, QuestRewardDefinition extraReward = null)
        {
            if (!QuestProgressService.RecordObjectives(save, questCatalog, kind, targetId, 1,
                    out var completedQuests))
            {
                Debug.LogWarning("Ignored objective event without a matching contract: " + kind + "/" + targetId);
                return false;
            }

            foreach (var quest in completedQuests) ApplyReward(quest.reward);
            ApplyReward(extraReward);
            SaveNow();
            RefreshHud();
            return completedQuests.Count > 0;
        }

        public void Attack()
        {
            if (mode == PlayMode.Fishing)
            {
                HookFishingLine();
                return;
            }

            if (mode == PlayMode.Exploring)
            {
                var actor = FindClosestActor();
                if (actor != null && actor.Kind == ActorKind.Encounter &&
                    QuestProgressService.IsActive(save, actor.Encounter.requiredQuestId)) BeginCombat(actor);
                return;
            }

            if (mode != PlayMode.Combat || Time.time < hitReadyAt) return;
            hitReadyAt = Time.time + activeMonsterDefinition.hitCooldown;
            PlaySfx(SelectRandomSfx(attackSwingSfx) ?? playerAttackSfx, 0.55f);
            var counterHit = monsterAttackPhase == MonsterAttackPhase.Recovery;
            if (enemyRoot != null)
            {
                var hitColor = counterHit ? new Color(0.53f, 0.95f, 0.78f, 1f) :
                    new Color(1f, 0.72f, 0.39f, 0.98f);
                SpawnPixelEffect(hitSlashVfx, enemyRoot.position + new Vector3(0f, 0.55f, 0f),
                    hitColor, 0.45f, counterHit ? 1.6f : 1.22f, 0.22f, 7);
            }
            var damage = 12 + InventoryService.AttackBonus(save) +
                         (counterHit ? activeMonsterDefinition.counterBonusDamage : 0);
            activeEncounterProgress.health = Mathf.Max(0, activeEncounterProgress.health - damage);
            if (enemyRenderer != null)
            {
                enemyRenderer.color = new Color(1f, 0.55f, 0.42f, 1f);
                enemyHitFlash = true;
                Invoke(nameof(ClearMonsterHitFlash), 0.12f);
            }
            if (enemyActor?.HitAnimationFrames != null)
            {
                SetEnemyAnimation(EnemyVisualAnimation.Hit, enemyActor.HitAnimationFrames, false, 30f);
                enemyHitAnimationUntil = Time.time + 0.34f;
            }
            SaveNow();
            SetMonsterCombatHud(true, MonsterPhaseHint());
            if (activeEncounterProgress.health <= 0) DefeatEncounter();
        }

        public void UsePotion()
        {
            if (mode == PlayMode.Dialogue || mode == PlayMode.Fishing) return;
            ItemDefinition usable = null;
            foreach (var item in ItemCatalog.Entries)
                if (item != null && item.category == "consumable" && item.healAmount > 0 &&
                    InventoryService.Count(save, item.id) > 0 &&
                    (usable == null || item.healAmount > usable.healAmount)) usable = item;

            if (usable == null || save.health >= MaxHealth)
            {
                if (mode == PlayMode.Exploring)
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue(usable == null ? "rowan_potion_empty" : "rowan_potion_full",
                        () => mode = PlayMode.Exploring);
                }
                return;
            }

            InventoryService.Remove(save, usable.id, 1);
            save.health = Mathf.Min(MaxHealth, save.health + usable.healAmount);
            PlaySfx(potionBottleSfx, 0.35f);
            SpawnPixelEffect(healingBurstVfx != null ? healingBurstVfx : dodgeFlashVfx,
                player.position + Vector3.up * 0.24f, new Color(0.55f, 1f, 0.72f, 0.9f),
                0.2f, 0.92f, 0.38f, 6);
            SaveNow();
            RefreshHud();
        }

        private void BeginCombat(WorldActor actor)
        {
            if (actor?.Encounter == null || actor.Progress == null || actor.Monster == null || actor.Progress.defeated)
                return;
            enemyActor = actor;
            enemyRoot = actor.Transform;
            enemyRenderer = enemyRoot.GetComponent<SpriteRenderer>();
            enemyIdleSprite = actor.IdleSprite;
            enemyLungeSprite = actor.LungeSprite;
            activeEncounterDefinition = actor.Encounter;
            activeMonsterDefinition = actor.Monster;
            activeEncounterProgress = actor.Progress;
            enemyVisualAnimation = EnemyVisualAnimation.None;
            enemyAnimationFrames = null;
            enemyAnimationFrameTimer = 0;
            enemyAnimationFrameIndex = 0;
            enemyHitAnimationUntil = 0;
            enemyAttackAnimationUntil = 0;
            monsterVocalReadyAt = 0;
            mode = PlayMode.Combat;
            PlayRandomSfx(swordDrawSfx, 0.3f);
            PlayBattleMusic();
            monsterAttackPhase = MonsterAttackPhase.ClosingIn;
            monsterPhaseTimer = activeMonsterDefinition.openingDelay;
            dodgeDuration = 0;
            if (enemyRenderer != null) enemyRenderer.color = Color.white;
            hud.SetExploringControls(true);
            SetMonsterCombatHud(true, MonsterPhaseHint());
            SaveNow();
        }

        private void DefeatEncounter()
        {
            mode = PlayMode.Dialogue;
            if (enemyRoot != null)
                SpawnPixelEffect(rewardGlintVfx, enemyRoot.position + Vector3.up * 0.4f,
                    new Color(1f, 0.84f, 0.47f, 1f), 0.32f, 1.8f, 0.42f, 7);
            activeEncounterProgress.health = 0;
            activeEncounterProgress.defeated = true;
            if (activeEncounterDefinition.contributesToQuest)
                RecordCurrentObjective("defeat", activeEncounterDefinition.defeatObjectiveTargetId);
            if (activeEncounterDefinition.reward != null && activeEncounterDefinition.reward.gold > 0)
                PlaySfx(lootCoinsSfx, 0.55f);
            ApplyReward(activeEncounterDefinition.reward);
            SaveNow();
            SetMonsterCombatHud(false);
            if (enemyActor?.DeathAnimationFrames != null && enemyRenderer != null)
            {
                enemyRenderer.color = Color.white;
                StartCoroutine(PlayAldenDefeatAnimation());
                return;
            }

            FinishEncounterDefeat();
        }

        private IEnumerator PlayAldenDefeatAnimation()
        {
            var frames = enemyActor.DeathAnimationFrames;
            for (var i = 0; i < frames.Length; i++)
            {
                if (enemyRenderer != null) enemyRenderer.sprite = frames[i];
                yield return new WaitForSeconds(1f / 30f);
            }
            FinishEncounterDefeat();
        }

        private void FinishEncounterDefeat()
        {
            if (enemyRoot != null) enemyRoot.gameObject.SetActive(false);
            ShowDialogue(activeEncounterDefinition.defeatDialogueId, () =>
            {
                mode = PlayMode.Exploring;
                PlayExplorationMusic();
                if (save.locationId == "ashfall_village") ShowVillageChoice();
                RefreshHud();
            }, "{monster}", activeMonsterDefinition.displayName);
        }

        private void UpdateEnemyAnimation()
        {
            if (enemyRenderer == null) return;
            if (enemyActor?.IdleAnimationFrames == null)
            {
                enemyRenderer.sprite = monsterAttackPhase == MonsterAttackPhase.Lunging
                    ? enemyLungeSprite : enemyIdleSprite;
                return;
            }

            if (Time.time >= enemyHitAnimationUntil)
            {
                if (monsterAttackPhase == MonsterAttackPhase.Lunging)
                {
                    if (enemyVisualAnimation != EnemyVisualAnimation.Attack)
                    {
                        SetEnemyAnimation(EnemyVisualAnimation.Attack,
                            enemyActor.AttackAnimationFrames, false, 30f);
                        enemyAttackAnimationUntil = Time.time +
                            enemyActor.AttackAnimationFrames.Length / 30f;
                    }
                }
                else if (monsterAttackPhase == MonsterAttackPhase.ClosingIn)
                {
                    SetEnemyAnimation(EnemyVisualAnimation.Run, enemyActor.RunAnimationFrames, true, 30f);
                }
                else if (monsterAttackPhase == MonsterAttackPhase.Telegraph)
                {
                    SetEnemyAnimation(EnemyVisualAnimation.Idle, enemyActor.IdleAnimationFrames, true, 18f);
                }
                else if (enemyVisualAnimation != EnemyVisualAnimation.Attack ||
                         Time.time >= enemyAttackAnimationUntil)
                {
                    SetEnemyAnimation(EnemyVisualAnimation.Idle, enemyActor.IdleAnimationFrames, true, 18f);
                }
            }

            if (enemyAnimationFrames == null || enemyAnimationFrames.Length < 2 || enemyAnimationFps <= 0) return;
            enemyAnimationFrameTimer += Time.deltaTime;
            var frameDuration = 1f / enemyAnimationFps;
            while (enemyAnimationFrameTimer >= frameDuration)
            {
                enemyAnimationFrameTimer -= frameDuration;
                if (enemyAnimationLoops)
                    enemyAnimationFrameIndex = (enemyAnimationFrameIndex + 1) % enemyAnimationFrames.Length;
                else if (enemyAnimationFrameIndex < enemyAnimationFrames.Length - 1)
                    enemyAnimationFrameIndex++;
                else
                    break;
            }

            var frame = enemyAnimationFrames[enemyAnimationFrameIndex];
            if (enemyRenderer.sprite != frame) enemyRenderer.sprite = frame;
        }

        private void SetEnemyAnimation(EnemyVisualAnimation animation, Sprite[] frames, bool loop, float fps)
        {
            if (frames == null || frames.Length == 0 || enemyRenderer == null) return;
            if (enemyVisualAnimation == animation && enemyAnimationFrames == frames) return;

            enemyVisualAnimation = animation;
            enemyAnimationFrames = frames;
            enemyAnimationFrameIndex = 0;
            enemyAnimationFrameTimer = 0;
            enemyAnimationFps = fps;
            enemyAnimationLoops = loop;
            enemyRenderer.sprite = frames[0];
        }

        private static AldenAnimationSet GetAldenAnimationSet()
        {
            if (aldenAnimationSet != null) return aldenAnimationSet;
            var idle = Resources.Load<Texture2D>("Art/AldenKnight/Idle");
            var run = Resources.Load<Texture2D>("Art/AldenKnight/Run");
            var attack = Resources.Load<Texture2D>("Art/AldenKnight/Attack");
            var hit = Resources.Load<Texture2D>("Art/AldenKnight/Hit");
            var death = Resources.Load<Texture2D>("Art/AldenKnight/Death");
            if (idle == null || run == null || attack == null || hit == null || death == null)
            {
                Debug.LogWarning("Alden's optional knight animation sheets are incomplete; using the procedural sprite.");
                return null;
            }

            var set = new AldenAnimationSet
            {
                Idle = CreateSpriteAtlas(idle, 5, 5, 18f),
                Run = CreateSpriteAtlas(run, 5, 5, 18f),
                Attack = CreateSpriteAtlas(attack, 5, 4, 18f),
                Hit = CreateSpriteAtlas(hit, 4, 4, 18f),
                Death = CreateSpriteAtlas(death, 5, 5, 18f)
            };
            if (set.Idle == null || set.Run == null || set.Attack == null || set.Hit == null || set.Death == null)
            {
                Debug.LogWarning("Alden's knight animation sheets have unexpected dimensions; using the procedural sprite.");
                return null;
            }

            aldenAnimationSet = set;
            return set;
        }

        private static Sprite[] CreateSpriteAtlas(Texture2D texture, int columns, int rows, float pixelsPerUnit)
        {
            if (texture == null || columns < 1 || rows < 1 ||
                texture.width % columns != 0 || texture.height % rows != 0) return null;

            texture.filterMode = FilterMode.Point;
            texture.wrapMode = TextureWrapMode.Clamp;
            var frameWidth = texture.width / columns;
            var frameHeight = texture.height / rows;
            var frames = new Sprite[columns * rows];
            for (var row = 0; row < rows; row++)
            {
                for (var column = 0; column < columns; column++)
                {
                    var rect = new Rect(column * frameWidth,
                        texture.height - (row + 1) * frameHeight, frameWidth, frameHeight);
                    frames[row * columns + column] = Sprite.Create(texture, rect,
                        new Vector2(0.5f, 0.045f), pixelsPerUnit, 0, SpriteMeshType.FullRect);
                }
            }
            return frames;
        }

        private void BeginFishing(WorldActor actor)
        {
            if (actor?.FishingSpot == null) return;
            var baitCount = InventoryService.Count(save, actor.FishingSpot.baitItemId);
            if (baitCount < 1)
            {
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_fishing_no_bait", () => mode = PlayMode.Exploring);
                return;
            }

            activeFishingSpot = actor;
            fishingWaitRemaining = UnityEngine.Random.Range(actor.FishingSpot.biteDelayMinSeconds,
                actor.FishingSpot.biteDelayMaxSeconds);
            fishingBiteRemaining = 0;
            fishingBiteActive = false;
            mode = PlayMode.Fishing;
            PlaySfx(fishingCastSfx, 0.26f);
            hud.SetFishingControls(true);
            SaveNow();
            RefreshHud();
        }

        private void OpenCraftMenu(WorldActor actor)
        {
            var recipes = RecipeCatalogService.FindForStation(recipeCatalog, actor.WorkstationId);
            if (actor.WorkstationId == "cinderwell_kitchen" &&
                !QuestProgressService.IsActive(save, "side_june_pantry_cook"))
                recipes.RemoveAll(recipe => recipe.id == "cook_cinderwell_stonepot_broth");
            if (actor.WorkstationId == "last_oath_kitchen" &&
                !QuestProgressService.IsActive(save, "side_crownfall_shared_table_cook"))
                recipes.RemoveAll(recipe => recipe.id == "cook_crownfall_starlit_pottage");
            if (actor.WorkstationId == "dawnkeep_forge" &&
                !QuestProgressService.IsActive(save, "side_ashfall_cart_forge"))
                recipes.RemoveAll(recipe => recipe.id == "forge_ashfall_cart_axle_pin");
            if (actor.WorkstationId == "dawnkeep_forge" &&
                !QuestProgressService.IsActive(save, "side_atlas_forge"))
                recipes.RemoveAll(recipe => recipe.id == "forge_regional_fit_gauge");
            if (actor.WorkstationId == "dawnkeep_forge" &&
                !QuestProgressService.IsActive(save, "side_silas_arrow_forge"))
                recipes.RemoveAll(recipe => recipe.id == "forge_silas_windline_charm");
            if (actor.WorkstationId == "cinderwell_assay_bench" &&
                !QuestProgressService.IsActive(save, "side_cinderwell_wick_craft"))
                recipes.RemoveAll(recipe => recipe.id == "brew_cinderwell_brine_wick");
            if (actor.WorkstationId == "cinderwell_assay_bench" &&
                !QuestProgressService.IsActive(save, "side_cistern_wheel_filter_craft"))
                recipes.RemoveAll(recipe => recipe.id == "brew_cinder_moss_filter");
            if (actor.WorkstationId == "cinderwell_assay_bench" &&
                !QuestProgressService.IsActive(save, "side_saltroad_beacon_lens"))
                recipes.RemoveAll(recipe => recipe.id == "craft_saltroad_beacon_lens");
            if (actor.WorkstationId == "archive_alchemy_bench")
            {
                if (!QuestProgressService.IsActive(save, "side_outerwake_jace_diaphragm"))
                    recipes.RemoveAll(recipe => recipe.id == "brew_jace_wind_diaphragm");
            }
            if (actor.WorkstationId == "greenwake_alchemy_still")
            {
                if (!QuestProgressService.IsActive(save, "side_greenwake_glassplum_syrup"))
                    recipes.RemoveAll(recipe => recipe.id == "brew_rootglass_syrup");
                if (!QuestProgressService.IsActive(save, "side_greenwake_rootwall_craft_resin"))
                    recipes.RemoveAll(recipe => recipe.id == "brew_greenwake_rootwall_resin");
            }
            if (actor.WorkstationId == "choir_harmonic_anvil")
            {
                if (!QuestProgressService.IsActive(save, "side_choir_lyra_balm"))
                    recipes.RemoveAll(recipe => recipe.id == "forge_lyra_tuning_fork");
                if (!QuestProgressService.IsActive(save, "side_choir_signal_brace"))
                    recipes.RemoveAll(recipe => recipe.id == "forge_choir_pulse_brace");
                if (!QuestProgressService.IsActive(save, "side_choir_first_oath_craft"))
                    recipes.RemoveAll(recipe => recipe.id == "forge_first_oath_memory_charm");
            }
            if (actor.WorkstationId == "last_oath_forge" &&
                !QuestProgressService.IsActive(save, "side_last_oath_watch_spindle"))
                recipes.RemoveAll(recipe => recipe.id == "forge_alden_watch_spindle");
            if (actor.WorkstationId == "choir_archive_loom")
            {
                if (QuestProgressService.IsActive(save, "choir_preserve_records"))
                    recipes.RemoveAll(recipe => recipe.id != "craft_resonance_lens");
                if (QuestProgressService.IsActive(save, "side_choir_unbound_index"))
                    recipes.RemoveAll(recipe => recipe.id != "craft_unbound_voice_index");
                else
                    recipes.RemoveAll(recipe => recipe.id == "craft_unbound_voice_index");
            }
            if (actor.WorkstationId == "dawnkeep_forge")
            {
                if (QuestProgressService.IsActive(save, "side_dawnkeep_gauge"))
                    recipes.RemoveAll(recipe => recipe.id != "forge_cadet_flow_charm" &&
                        !(recipe.id == "forge_ashfall_cart_axle_pin" &&
                          QuestProgressService.IsActive(save, "side_ashfall_cart_forge")) &&
                        !(recipe.id == "forge_regional_fit_gauge" &&
                          QuestProgressService.IsActive(save, "side_atlas_forge")));
                else
                    recipes.RemoveAll(recipe => recipe.id == "forge_cadet_flow_charm");

                var hasCinderwellLedgerPattern = IsQuestCompleted("side_cinderwell_named_schedule") ||
                                                 IsQuestCompleted("side_cinderwell_aggregate_schedule");
                if (!hasCinderwellLedgerPattern)
                    recipes.RemoveAll(recipe => recipe.id == "forge_cistern_ledger_clasp");

                if (!QuestProgressService.IsActive(save, "side_elara_garden_brace"))
                    recipes.RemoveAll(recipe => recipe.id == "forge_dawnkeep_runoff_clip");
            }
            if (actor.WorkstationId == "outerwake_forge")
            {
                if (QuestProgressService.IsActive(save, "side_outerwake_receiver_coil"))
                    recipes.RemoveAll(recipe => recipe.id != "forge_outerwake_receiver_coil");
                else
                    recipes.RemoveAll(recipe => recipe.id == "forge_outerwake_receiver_coil");
            }
            if (recipes.Count == 0) return;
            var isOuterwake = actor.WorkstationId.StartsWith("archive_") || actor.WorkstationId == "outerwake_forge";
            var isLastOath = actor.WorkstationId == "last_oath_forge";
            var isLastOathKitchen = actor.WorkstationId == "last_oath_kitchen";
            var isCinderwellAssay = actor.WorkstationId == "cinderwell_assay_bench";
            var isCinderwellKitchen = actor.WorkstationId == "cinderwell_kitchen";
            var isGreenwake = actor.WorkstationId.StartsWith("greenwake_");
            var speaker = isCinderwellKitchen ? "SISTER JUNE" : isLastOathKitchen ? "ADA SLOANE" : isCinderwellAssay ? "TALIA MERCER" : isGreenwake ? "MARA BELL" : actor.WorkstationId.StartsWith("choir_") ? "LYRA MOSS" : isLastOath ? "CAPTAIN ALDEN VALE" : isOuterwake ?
                recipes[0].discipline == "smithing" ? "JACE MORROW" : "DR. EVELYN HART" :
                recipes[0].discipline == "smithing" ? "TOMAS REED" : "MIRA COLE";
            var prompt = isCinderwellKitchen
                ? "Sister June: use the barley and Emberscale Perch together; the recipe makes two bowls so one can be shared."
                : isLastOathKitchen
                ? "Ada Sloane: cook one Emberroot and one Starlit Minnow into a single trial portion. The reserve seed stays untouched."
                : isCinderwellAssay
                ? recipes.Exists(recipe => recipe.id == "craft_saltroad_beacon_lens")
                    ? "Talia Mercer: mài Tấm Kính Chia Tia theo vạch mẫu. Đây là thử nghiệm phản quang cho Salt Road, không phải chứng nhận đường an toàn."
                    : "Talia Mercer: pha bấc thử theo đúng lượng ghi trên phiếu. Mẻ thuốc thử này chỉ giúp so sắc độ mẫu."
                : isGreenwake
                ? "Mara Bell: nấu một mẻ Siro Rootglass nhỏ để hồi phục. Thức uống này không phải thuốc chữa bệnh."
                : actor.WorkstationId.StartsWith("choir_")
                ? "Lyra Moss: chọn công thức cộng hưởng. Vật liệu chỉ được dùng khi chế tác thành công."
                : isLastOath
                    ? recipes.Exists(recipe => recipe.id == "forge_alden_watch_spindle")
                        ? "Áo giáp vẫn sẵn. Bản vẽ Con Suốt Đổi Gác cần Emberroot và Starlit Minnow; nguyên liệu chỉ trừ khi rèn thành công."
                        : "Alden giữ lò rèn mở cho bất kỳ ai muốn chuẩn bị áo giáp bảo vệ người ở lại."
                : isOuterwake
                    ? "Vật liệu thu được từ phía bên kia Veil có thể được rèn hoặc phân tích tại đây."
                    : recipes[0].discipline == "smithing"
                    ? "Tomas Reed: chọn bản vẽ. Vật liệu sẽ được dùng khi rèn thành công."
                    : "Mira Cole: chọn công thức. Vật liệu sẽ được dùng khi pha thành công.";
            var options = new List<DialogueChoiceOption>();
            foreach (var recipe in recipes)
                options.Add(new DialogueChoiceOption(recipe.id, BuildRecipeChoiceLabel(recipe)));
            options.Add(new DialogueChoiceOption("leave", "Để sau"));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(speaker, prompt, options, recipeId => SelectCraftRecipe(recipeId, actor.WorkstationId));
        }

        private string BuildRecipeChoiceLabel(RecipeDefinition recipe)
        {
            var costs = new List<string>();
            foreach (var ingredient in recipe.ingredients)
            {
                var item = ItemCatalog.Find(ingredient.itemId);
                costs.Add(ingredient.quantity + " " + (item == null ? ingredient.itemId : item.name) +
                          " (" + InventoryService.Count(save, ingredient.itemId) + ")");
            }
            return recipe.displayName + "\n" + string.Join(" + ", costs);
        }

        private void SelectCraftRecipe(string recipeId, string stationId)
        {
            if (recipeId == "leave")
            {
                mode = PlayMode.Exploring;
                return;
            }

            if (!CraftingService.TryCraft(save, recipeCatalog, recipeId, stationId,
                    out var craftedRecipe, out var missingItemId))
            {
                var missingItem = ItemCatalog.Find(missingItemId);
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_recipe_missing", () => mode = PlayMode.Exploring,
                    "{item}", missingItem == null ? "nguyên liệu cần thiết" : missingItem.name);
                return;
            }

            PlaySfx(craftedRecipe.discipline == "cooking" ? potionBottleSfx : metalEquipSfx, 0.28f);
            var craftTint = craftedRecipe.discipline == "cooking"
                ? new Color(1f, 0.78f, 0.42f, 0.9f)
                : new Color(0.65f, 0.9f, 1f, 0.92f);
            SpawnPixelEffect(craftingFlareVfx, player.position + Vector3.up * 0.42f,
                craftTint, 0.12f, 0.82f, 0.3f, 7);
            var output = ItemCatalog.Find(craftedRecipe.outputItemId);
            if (HasActiveObjective("craft", craftedRecipe.outputItemId))
                RecordCurrentObjective("craft", craftedRecipe.outputItemId);
            SaveNow();
            mode = PlayMode.Dialogue;
            var completionDialogueId = craftedRecipe.id == "cook_cinderwell_stonepot_broth"
                ? "june_stonepot_cook"
                : craftedRecipe.id == "craft_unbound_voice_index"
                ? "lyra_choir_index_complete"
                : craftedRecipe.id == "forge_choir_pulse_brace"
                    ? "tamsin_signal_brace_complete"
                : craftedRecipe.id == "forge_alden_watch_spindle"
                    ? "alden_watch_spindle_complete"
                : craftedRecipe.id == "forge_lyra_tuning_fork"
                    ? "lyra_tuning_fork_complete"
                : craftedRecipe.id == "brew_jace_wind_diaphragm"
                    ? "jace_diaphragm_complete"
                : craftedRecipe.id == "brew_rootglass_syrup"
                    ? "mara_rootglass_complete"
                : craftedRecipe.id == "brew_cinderwell_brine_wick"
                    ? "talia_cinderwell_assay_complete"
                : craftedRecipe.id == "brew_cinder_moss_filter"
                    ? "talia_cistern_filter_complete"
                : craftedRecipe.id == "craft_saltroad_beacon_lens"
                    ? "talia_saltroad_beacon_complete"
                : craftedRecipe.id == "forge_cadet_flow_charm"
                    ? "tomas_waterline_charm_complete"
                : craftedRecipe.id == "forge_dawnkeep_runoff_clip"
                    ? "elara_garden_brace_complete"
                : craftedRecipe.id == "forge_cistern_ledger_clasp"
                        ? "tomas_cinder_clasp_complete"
                        : craftedRecipe.id == "forge_outerwake_receiver_coil"
                            ? "evelyn_outerwake_coil_complete"
                            : craftedRecipe.id == "brew_moonlight_tonic" &&
                              IsQuestCompleted("side_ashfall_brew_moonlight")
                                ? "mira_ashfall_tonic_brewed" : "rowan_recipe_complete";
            ShowDialogue(completionDialogueId, () => mode = PlayMode.Exploring,
                "{item}", output == null ? craftedRecipe.outputItemId : output.name);
        }

        private void OpenFarmMenu(WorldActor actor)
        {
            var plot = actor.FarmPlot;
            if (plot == null) return;
            var progress = FarmPlotProgressService.Find(save, plot.id);
            var options = new List<DialogueChoiceOption>();
            string prompt;
            string speaker = "ROWAN HALE";
            if (progress == null)
            {
                prompt = "Luống " + plot.cropDisplayName + " • Hạt giống: " + InventoryService.Count(save, plot.seedItemId) +
                         ". Cây lớn dần trong lúc chơi.";
                options.Add(new DialogueChoiceOption("plant", "Gieo " + plot.cropDisplayName));
            }
            else if (progress.remainingSeconds > 0)
            {
                prompt = plot.cropDisplayName + " đang lớn. Còn khoảng " + Mathf.CeilToInt(progress.remainingSeconds) +
                         " giây chơi trước khi thu hoạch.";
                options.Add(new DialogueChoiceOption("wait", "Để cây lớn tiếp"));
            }
            else
            {
                prompt = plot.cropDisplayName + " đã trưởng thành. Mỗi lần thu hoạch nhận " + plot.harvestQuantity + " phần.";
                options.Add(new DialogueChoiceOption("harvest", "Thu hoạch " + plot.cropDisplayName));
            }

            options.Add(new DialogueChoiceOption("leave", "Để sau"));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(speaker, prompt, options, choice => SelectFarmAction(actor, choice));
        }

        private void SelectFarmAction(WorldActor actor, string choice)
        {
            var plot = actor.FarmPlot;
            if (plot == null || choice == "leave")
            {
                mode = PlayMode.Exploring;
                return;
            }

            if (choice == "wait")
            {
                var progress = FarmPlotProgressService.Find(save, plot.id);
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_farm_growing", () => mode = PlayMode.Exploring,
                    "{time}", Mathf.CeilToInt(progress == null ? 0 : progress.remainingSeconds).ToString());
                return;
            }

            if (choice == "plant")
            {
                if (!FarmPlotProgressService.TryPlant(save, plot))
                {
                    mode = PlayMode.Dialogue;
                    ShowDialogue("rowan_farm_no_seeds", () => mode = PlayMode.Exploring,
                        "{crop}", plot.cropDisplayName);
                    return;
                }

                RefreshFarmPlotVisual(actor);
                SaveNow();
                mode = PlayMode.Dialogue;
                ShowDialogue("rowan_farm_planted", () => mode = PlayMode.Exploring,
                    "{crop}", plot.cropDisplayName);
                return;
            }

            if (choice == "harvest" && FarmPlotProgressService.TryHarvest(save, plot))
            {
                RefreshFarmPlotVisual(actor);
                var cropId = plot.cropId ?? string.Empty;
                var harvestTint = cropId.Contains("emberlily")
                    ? new Color(1f, 0.47f, 0.28f, 0.94f)
                    : cropId.Contains("moonwort")
                        ? new Color(0.66f, 0.94f, 0.78f, 0.94f)
                        : new Color(0.92f, 1f, 0.58f, 0.9f);
                SpawnPixelEffect(harvestGlintVfx, actor.Transform.position + Vector3.up * 0.28f,
                    harvestTint, 0.12f, 0.72f, 0.36f, 6);
                var ashfallSecondCrop = QuestProgressService.IsActive(save, "side_ashfall_replant_moonwort");
                if (HasActiveObjective("grow", plot.cropId))
                    RecordCurrentObjective("grow", plot.cropId);
                SaveNow();
                mode = PlayMode.Dialogue;
                if (ashfallSecondCrop && IsQuestCompleted("side_ashfall_replant_moonwort"))
                    ShowDialogue("rowan_ashfall_second_harvest", () => mode = PlayMode.Exploring);
                else
                    ShowDialogue("rowan_farm_harvested", () => mode = PlayMode.Exploring,
                        "{crop}", plot.cropDisplayName);
                return;
            }

            mode = PlayMode.Exploring;
        }

        private void UpdateFarmProgress()
        {
            if (save?.farmProgress == null || save.farmProgress.Count == 0 ||
                (mode != PlayMode.Exploring && mode != PlayMode.Combat && mode != PlayMode.Fishing)) return;

            var becameReady = FarmPlotProgressService.Tick(save, Mathf.Min(Time.deltaTime, 0.25f));
            farmSaveTimer -= Time.deltaTime;
            if (becameReady || farmSaveTimer <= 0)
            {
                farmSaveTimer = 5f;
                if (becameReady) RefreshAllFarmPlotVisuals();
                SaveNow();
            }
        }

        private void RefreshAllFarmPlotVisuals()
        {
            foreach (var actor in actors)
                if (actor.Kind == ActorKind.FarmPlot) RefreshFarmPlotVisual(actor);
        }

        private void RefreshFarmPlotVisual(WorldActor actor)
        {
            if (actor?.Renderer == null || actor.FarmPlot == null) return;
            var progress = FarmPlotProgressService.Find(save, actor.FarmPlot.id);
            actor.Renderer.sprite = progress == null
                ? actor.FarmBedSprite
                : progress.remainingSeconds > 0 ? actor.CropGrowingSprite : actor.CropReadySprite;
        }

        private void UpdateFishing()
        {
            if (Input.GetKeyDown(KeyCode.Space))
            {
                HookFishingLine();
                return;
            }
            if (Input.GetKeyDown(KeyCode.E))
            {
                CancelFishing();
                return;
            }
            if (activeFishingSpot?.FishingSpot == null)
            {
                CancelFishing();
                return;
            }

            if (fishingBiteActive)
            {
                fishingBiteRemaining -= Time.deltaTime;
                if (fishingBiteRemaining <= 0)
                {
                    InventoryService.Remove(save, activeFishingSpot.FishingSpot.baitItemId, 1);
                    SaveNow();
                    EndFishingWithDialogue("rowan_fishing_missed");
                }
            }
            else
            {
                fishingWaitRemaining -= Time.deltaTime;
                if (fishingWaitRemaining <= 0)
                {
                    fishingBiteActive = true;
                    fishingBiteRemaining = activeFishingSpot.FishingSpot.biteWindowSeconds;
                    PlaySfx(fishingBiteSfx, 0.28f);
                }
            }
        }

        private void HookFishingLine()
        {
            if (mode != PlayMode.Fishing || activeFishingSpot?.FishingSpot == null) return;
            if (!fishingBiteActive)
            {
                EndFishingWithDialogue("rowan_fishing_missed");
                return;
            }

            var spot = activeFishingSpot.FishingSpot;
            if (!InventoryService.Remove(save, spot.baitItemId, 1))
            {
                EndFishingWithDialogue("rowan_fishing_no_bait");
                return;
            }

            var fishId = FishingCatalogService.RollCatch(spot, UnityEngine.Random.value);
            var fish = ItemCatalog.Find(fishId);
            if (fish == null || InventoryService.Add(save, fishId, 1) != 1)
            {
                EndFishingWithDialogue("rowan_fishing_missed");
                return;
            }

            var fishingQuestObjective = HasActiveObjective("fish", fishId);
            var elaraGardenCatch = fishId == "blackreed_trout" &&
                                   QuestProgressService.IsActive(save, "side_elara_garden_fish");
            var ashfallRemedyCatch = fishId == "blackreed_trout" &&
                                     QuestProgressService.IsActive(save, "side_ashfall_blackreed_record");
            if (fishingQuestObjective) RecordCurrentObjective("fish", fishId);
            PlaySfx(fishingCatchSfx, 0.3f);
            if (activeFishingSpot?.Transform != null)
                SpawnPixelEffect(fishingRippleVfx, activeFishingSpot.Transform.position + Vector3.up * 0.08f,
                    new Color(0.4f, 0.88f, 1f, 0.82f), 0.12f, 0.8f, 0.46f, 5);
            SaveNow();
            activeFishingSpot = null;
            fishingBiteActive = false;
            mode = PlayMode.Dialogue;
            hud.SetFishingControls(false);
            var catchDialogueId = ashfallRemedyCatch ? "rowan_ashfall_blackreed_trout" :
                elaraGardenCatch ? "rowan_garden_trout" :
                fishingQuestObjective && fishId == "whisper_koi" && IsQuestCompleted("side_choir_resonance_map")
                    ? "rowan_choir_whisper_koi" : "rowan_fishing_catch";
            ShowDialogue(catchDialogueId, () =>
            {
                mode = PlayMode.Exploring;
                RefreshHud();
            }, "{fish}", fish.name);
        }

        private void CancelFishing()
        {
            if (mode != PlayMode.Fishing) return;
            activeFishingSpot = null;
            fishingBiteActive = false;
            mode = PlayMode.Exploring;
            hud.SetFishingControls(false);
            RefreshHud();
            SaveNow();
        }

        private void EndFishingWithDialogue(string dialogueId)
        {
            if (dialogueId == "rowan_fishing_missed") PlaySfx(fishingMissSfx, 0.22f);
            activeFishingSpot = null;
            fishingBiteActive = false;
            mode = PlayMode.Dialogue;
            hud.SetFishingControls(false);
            ShowDialogue(dialogueId, () =>
            {
                mode = PlayMode.Exploring;
                RefreshHud();
            });
        }

        private void ShowVillageChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest == null || quest.choices == null || quest.choices.Count < 2 || quest.choices.Count > 4)
            {
                Debug.LogError("Ashfall choice quest is invalid; cannot continue the prologue.");
                return;
            }

            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseFirstAction);
        }

        private void ChooseFirstAction(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (choice == null)
            {
                Debug.LogError("Unknown Ashfall story choice: " + choiceId);
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "ashfall_first_action", choice.reward);
            mode = PlayMode.Dialogue;
            RefreshHud();
            ShowDialogue(choice.flagValue == "shelter" ? "rowan_choice_shelter" : "rowan_choice_trail",
                () => mode = PlayMode.Exploring);
        }

        private void ShowOrderDisclosureChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2)
            {
                Debug.LogError("Order disclosure choice is missing from the active quest.");
                mode = PlayMode.Exploring;
                return;
            }

            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseOrderDisclosure);
        }

        private void ShowOrderTestimonyChoice()
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest?.choices == null || quest.choices.Count < 2)
            {
                Debug.LogError("Order testimony choice is missing from the active quest.");
                mode = PlayMode.Exploring;
                return;
            }

            var options = new List<DialogueChoiceOption>();
            foreach (var choice in quest.choices)
                options.Add(new DialogueChoiceOption(choice.id, choice.label));
            mode = PlayMode.Dialogue;
            hud.ShowChoice(quest.choiceSpeaker, quest.choicePrompt, options, ChooseOrderTestimony);
        }

        private void ChooseOrderTestimony(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (quest == null || choice == null)
            {
                Debug.LogError("Unknown Order testimony choice: " + choiceId);
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", "order_testimony_choice", choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "publish" ? "rowan_order_testimony_publish" :
                "rowan_order_testimony_seal", () => mode = PlayMode.Exploring);
        }

        private void ChooseOrderDisclosure(string choiceId)
        {
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            var choice = QuestCatalogService.FindChoice(quest, choiceId);
            if (choice == null)
            {
                Debug.LogError("Unknown Order disclosure choice: " + choiceId);
                mode = PlayMode.Exploring;
                return;
            }

            var targetId = "";
            if (quest.objectives != null)
                foreach (var objective in quest.objectives)
                    if (objective != null && objective.kind == "choice")
                    {
                        targetId = objective.targetId;
                        break;
                    }
            if (string.IsNullOrEmpty(targetId))
            {
                Debug.LogError("Order disclosure quest has no choice objective target.");
                mode = PlayMode.Exploring;
                return;
            }

            QuestProgressService.SetStoryFlag(save, quest.choiceFlag, choice.flagValue);
            RecordCurrentObjective("choice", targetId, choice.reward);
            mode = PlayMode.Dialogue;
            ShowDialogue(choice.flagValue == "public" ? "rowan_disclosure_public" : "rowan_disclosure_private",
                () => mode = PlayMode.Exploring);
        }

        private void TravelTo(string locationId, Vector2 arrivalPosition)
        {
            if (!GameLocationService.IsPlayable(locationId)) return;
            save.locationId = locationId;
            save.playerX = arrivalPosition.x;
            save.playerY = arrivalPosition.y;
            mode = PlayMode.Exploring;
            if (worldRoot != null)
            {
                worldRoot.gameObject.SetActive(false);
                Destroy(worldRoot.gameObject);
            }

            BuildWorld();
            PlayExplorationMusic();
            SaveNow();
            RefreshHud();
        }

        private void PlayMusic(AudioClip clip)
        {
            if (musicSource == null || clip == null) return;
            if (musicSource.clip == clip && musicSource.isPlaying) return;
            musicSource.clip = clip;
            musicSource.loop = true;
            musicSource.Play();
        }

        private void PlayOpeningMusic()
        {
            PlayMusic(LoadOptionalMusic("rpgchip01_title_screen") ?? explorationTheme);
        }

        private void PlayExplorationMusic()
        {
            string track;
            switch (save?.locationId)
            {
                case "ashfall_village": track = "rpgchip03_town"; break;
                case "dawnkeep_outpost": track = "rpgchip05_pavane"; break;
                case "dawnkeep_barracks": track = "rpgchip04_in_the_royal_court"; break;
                case "cinderwell_basin": track = "rpgchip02_bittersweet_story"; break;
                case "cinder_cistern": track = "rpgchip06_dungeon"; break;
                case "salt_road": track = "rpgchip09_rainy_streets"; break;
                case "salt_lockhouse": track = "rpgchip06_dungeon"; break;
                case "choir_beneath_lake": track = "rpgchip07_the_shrine_of_mysteries"; break;
                case "greenwake_refuge": track = "rpgchip10_fountain_of_the_fairies"; break;
                case "outerwake_archive": track = "rpgchip11_airship"; break;
                case "last_oath_reach": track = "rpgchip08_castle_on_the_mountain"; break;
                default: track = null; break;
            }
            PlayMusic(LoadOptionalMusic(track) ?? explorationTheme);
            PlayLocationAmbience();
        }

        private AudioClip[] GetFootstepSounds(string locationId)
        {
            switch (locationId)
            {
                case "ashfall_village":
                case "dawnkeep_outpost":
                case "cinderwell_basin":
                case "greenwake_refuge":
                    return grassFootstepSfx;
                case "dawnkeep_barracks":
                case "cinder_cistern":
                case "salt_lockhouse":
                case "choir_beneath_lake":
                case "outerwake_archive":
                case "last_oath_reach":
                    return stoneFootstepSfx;
                default:
                    return footstepSfx;
            }
        }

        private void PlayLocationAmbience()
        {
            if (ambienceSource == null) return;
            AudioClip ambience;
            switch (save?.locationId)
            {
                case "ashfall_village":
                    ambience = nightCricketsAmbience;
                    break;
                case "greenwake_refuge":
                    ambience = parkBirdsAmbience;
                    break;
                case "dawnkeep_barracks":
                    ambience = tickingClockAmbience;
                    break;
                case "cinderwell_basin":
                    ambience = parkRiverAmbience;
                    break;
                case "salt_road":
                case "outerwake_archive":
                    ambience = parkWindAmbience;
                    break;
                case "dawnkeep_outpost":
                case "choir_beneath_lake":
                case "last_oath_reach":
                    ambience = riverAmbience;
                    break;
                default:
                    ambience = null;
                    break;
            }

            if (ambience == null)
            {
                ambienceSource.Stop();
                ambienceSource.clip = null;
                return;
            }
            if (ambienceSource.clip == ambience && ambienceSource.isPlaying) return;
            ambienceSource.clip = ambience;
            ambienceSource.loop = true;
            ambienceSource.Play();
        }

        private void PlayBattleMusic()
        {
            var track = activeMonsterDefinition == null ? null : activeMonsterDefinition.id == "demon_king_alden"
                ? "rpgchip12_the_evil_one" : activeMonsterDefinition.rank == "boss"
                    ? "rpgchip14_battle_2" : "rpgchip13_battle_1";
            PlayMusic(LoadOptionalMusic(track) ?? battleTheme);
        }

        private void PlayDownedMusic()
        {
            PlayMusic(LoadOptionalMusic("rpgchip15_game_over") ?? battleTheme);
        }

        private static AudioClip LoadOptionalMusic(string track)
        {
            return string.IsNullOrEmpty(track) ? null : Resources.Load<AudioClip>("Audio/Music/" + track);
        }

        private void PlaySfx(AudioClip clip, float volume)
        {
            if (effectsSource == null || clip == null) return;
            effectsSource.PlayOneShot(clip, Mathf.Clamp01(volume));
        }

        private void PlayRandomSfx(AudioClip[] clips, float volume)
        {
            PlaySfx(SelectRandomSfx(clips), volume);
        }

        private AudioClip SelectRandomSfx(AudioClip[] clips)
        {
            if (clips == null || clips.Length == 0) return null;
            var validCount = 0;
            foreach (var clip in clips)
                if (clip != null) validCount++;
            if (validCount == 0) return null;

            var selected = sfxRandom.Next(validCount);
            foreach (var clip in clips)
            {
                if (clip == null) continue;
                if (selected-- == 0) return clip;
            }
            return null;
        }

        private static AudioClip[] LoadAudioVariants(string resourcePrefix, int count)
        {
            var clips = new AudioClip[count];
            for (var i = 0; i < count; i++)
                clips[i] = Resources.Load<AudioClip>(resourcePrefix + (i + 1).ToString("00"));
            return clips;
        }

        private AudioClip[] GetMonsterVocalSet(MonsterDefinition monster)
        {
            if (monster == null) return null;
            var identity = (monster.id + " " + monster.displayName).ToLowerInvariant();
            if (ContainsAny(identity, "slime", "ooze", "blob", "gel cube", "muck", "jelly"))
                return slimeVocalSfx;
            if (ContainsAny(identity, "beetle", "scuttler", "crab", "spider", "mite", "cockroach"))
                return beetleVocalSfx;
            if (ContainsAny(identity, "ghost", "wraith", "shade", "spectral", "wisp", "soul eater",
                    "phantasmal", "banshee", "eidolon", "revenant", "phantom", "hollow"))
                return shadeVocalSfx;
            if (ContainsAny(identity, "ogre", "troll")) return ogreVocalSfx;
            if (ContainsAny(identity, "giant", "colossus", "dragon", "drake", "hydra", "cyclops", "yeti"))
                return giantVocalSfx;
            if (ContainsAny(identity, "sentinel", "warden", "knight", "cadet", "enforcer", "bailiff",
                    "inspector", "keeper", "mage", "scribe", "elf", "orc", "goblin", "vampire",
                    "zombie", "skeleton", "ghoul", "demon", "devil", "angel", "seraph", "golem",
                    "elemental", "sphinx", "guard", "ratchet", "cantor", "herald", "world will"))
                return null;
            return beastVocalSfx;
        }

        private static bool ContainsAny(string value, params string[] fragments)
        {
            foreach (var fragment in fragments)
                if (value.IndexOf(fragment, StringComparison.Ordinal) >= 0) return true;
            return false;
        }

        private bool IsOrderArcUnlocked()
        {
            if (save == null) return false;
            if (!string.IsNullOrEmpty(save.activeQuestId) && save.activeQuestId.StartsWith("order_")) return true;
            if (save.completedQuestIds == null) return false;
            foreach (var questId in save.completedQuestIds)
                if (questId == "ashfall_shelter_report" || questId == "ashfall_trail_report" ||
                    questId.StartsWith("order_")) return true;
            return false;
        }

        private void ApplyReward(QuestRewardDefinition reward)
        {
            if (reward == null) return;
            save.gold += Mathf.Max(0, reward.gold);
            if (reward.items == null) return;
            foreach (var item in reward.items)
                if (item != null) InventoryService.Add(save, item.itemId, item.quantity);
        }

        private WorldActor FindClosestActor()
        {
            WorldActor nearest = null;
            var nearestDistance = InteractRange;
            foreach (var actor in actors)
            {
                if (actor.Transform == null || !actor.Transform.gameObject.activeInHierarchy) continue;
                if (actor.Kind == ActorKind.Encounter)
                {
                    if (actor.Encounter == null || actor.Progress == null || actor.Progress.defeated) continue;
                    var isBlocked = !string.IsNullOrEmpty(actor.Encounter.blockedQuestId) &&
                                    QuestProgressService.IsActive(save, actor.Encounter.blockedQuestId);
                    if (!isBlocked && !QuestProgressService.IsActive(save, actor.Encounter.requiredQuestId)) continue;
                }
                if (actor.Kind == ActorKind.SurvivorWitness &&
                    !QuestProgressService.IsActive(save, "ashfall_shelter_witness") &&
                    !HasActiveObjectiveTarget(actor.ObjectiveTargetId)) continue;
                if (actor.Kind == ActorKind.SealClue &&
                    !QuestProgressService.IsActive(save, "ashfall_trail_evidence")) continue;
                if (actor.Kind == ActorKind.CaptainAlden &&
                    !QuestProgressService.IsActive(save, "ashfall_shelter_report") &&
                    !QuestProgressService.IsActive(save, "ashfall_trail_report") &&
                    !QuestProgressService.IsActive(save, "order_record_choice") &&
                    !QuestProgressService.IsActive(save, "order_trial_report") &&
                    !QuestProgressService.IsActive(save, "order_alden_reckoning")) continue;
                if (actor.Kind == ActorKind.ElaraWren &&
                    !QuestProgressService.IsActive(save, "order_arrival") &&
                    !QuestProgressService.IsActive(save, "order_roster") &&
                    !QuestProgressService.IsActive(save, "order_archive_public") &&
                    !QuestProgressService.IsActive(save, "order_archive_private") &&
                    !QuestProgressService.IsActive(save, "order_evidence_choice")) continue;
                if (actor.Kind == ActorKind.DawnkeepRoster &&
                    !QuestProgressService.IsActive(save, "order_roster") &&
                    !QuestProgressService.IsActive(save, "order_roster_origin")) continue;
                if (actor.Kind == ActorKind.SisterJune &&
                    !QuestProgressService.IsActive(save, "cinder_arrival") &&
                    !QuestProgressService.IsActive(save, "cinder_water_rights") &&
                    !QuestProgressService.IsActive(save, "cinder_water_refugees") &&
                    !QuestProgressService.IsActive(save, "cinder_recovery") &&
                    !QuestProgressService.IsActive(save, "cinder_june_report") &&
                    !QuestProgressService.IsActive(save, "side_cinderwell_measure_start") &&
                    !QuestProgressService.IsActive(save, "side_cinderwell_record_choice") &&
                    !HasActiveObjective("talk", "sister_june")) continue;
            if (actor.Kind == ActorKind.TaliaMercer && !HasActiveObjective("talk", "talia_mercer")) continue;
            if (actor.Kind == ActorKind.OrenBell && !HasActiveObjective("talk", "oren_bell")) continue;
                if (actor.Kind == ActorKind.StoryLandmark && !HasActiveObjectiveTarget(actor.ObjectiveTargetId) &&
                    !(QuestProgressService.IsActive(save, "choir_memory_choice") && actor.Name == "Lyra Moss")) continue;
                if (actor.Kind == ActorKind.SaltRoadWitness &&
                    !HasActiveObjective("talk", actor.ObjectiveTargetId) &&
                    !(QuestProgressService.IsActive(save, "salt_route_choice") && actor.ObjectiveTargetId == "ruth_calder"))
                    continue;
                if (actor.Kind == ActorKind.RoadGate && save.locationId == "ashfall_village" &&
                    !IsOrderArcUnlocked()) continue;
                if (actor.Kind == ActorKind.RoadGate && !string.IsNullOrEmpty(actor.RequiredQuestId) &&
                    !IsQuestCompleted(actor.RequiredQuestId)) continue;
                var distance = Vector2.Distance(player.position, actor.Transform.position);
                if (distance <= nearestDistance)
                {
                    nearest = actor;
                    nearestDistance = distance;
                }
            }

            return nearest;
        }

        private bool HasActiveObjective(string kind, string targetId)
        {
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
            {
                if (quest.objectives == null) continue;
                foreach (var objective in quest.objectives)
                    if (objective != null && objective.kind == kind && objective.targetId == targetId &&
                        !IsObjectiveComplete(quest, objective)) return true;
            }
            return false;
        }

        private bool TryInteractWithQuestTalker(string targetId)
        {
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
            {
                if (quest?.objectives == null) continue;
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || objective.kind != "talk" || objective.targetId != targetId ||
                        IsObjectiveComplete(quest, objective) || string.IsNullOrEmpty(objective.dialogueId)) continue;
                    mode = PlayMode.Dialogue;
                    ShowDialogue(objective.dialogueId, () => CompleteBranchObjective("talk", targetId));
                    return true;
                }
            }
            return false;
        }

        private bool TryInteractWithMiraAshfallHouseRoute()
        {
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
            {
                if (quest == null || !quest.id.StartsWith("side_mira_ash_house_") || quest.objectives == null) continue;
                foreach (var objective in quest.objectives)
                {
                    if (objective == null || objective.kind != "talk" || objective.targetId != "mira_cole" ||
                        IsObjectiveComplete(quest, objective) || string.IsNullOrEmpty(objective.dialogueId)) continue;
                    mode = PlayMode.Dialogue;
                    ShowDialogue(objective.dialogueId, () => CompleteBranchObjective("talk", "mira_cole"));
                    return true;
                }
            }
            return false;
        }

        private bool HasActiveObjectiveTarget(string targetId)
        {
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
            {
                if (quest.objectives == null) continue;
                foreach (var objective in quest.objectives)
                    if (objective != null && objective.targetId == targetId && !IsObjectiveComplete(quest, objective))
                        return true;
            }
            return false;
        }

        private bool IsObjectiveComplete(QuestDefinition quest, QuestObjectiveDefinition objective)
        {
            if (quest == null || objective == null || save?.questObjectiveProgress == null) return false;
            foreach (var progress in save.questObjectiveProgress)
                if (progress != null && progress.questId == quest.id && progress.objectiveId == objective.id &&
                    progress.count >= objective.requiredCount) return true;
            return false;
        }

        private bool IsQuestCompleted(string questId)
        {
            return save?.completedQuestIds != null && save.completedQuestIds.Contains(questId);
        }

        private void RefreshHud()
        {
            if (hud == null || save == null) return;
            RefreshQuestLandmarkVisibility();
            var objective = CurrentObjective();
            var title = CurrentQuestTitle();
            var nearest = FindClosestActor();
            var action = mode == PlayMode.Fishing ? "DỪNG CÂU" : nearest == null ? "XEM QUANH" :
                nearest.Kind == ActorKind.Workstation ? "CHẾ TẠO" : nearest.Kind == ActorKind.FarmPlot ?
                FarmPlotProgressService.Find(save, nearest.FarmPlot.id) == null ? "TRỒNG" :
                FarmPlotProgressService.Find(save, nearest.FarmPlot.id).remainingSeconds > 0 ? "XEM VƯỜN" : "THU HOẠCH" :
                nearest.Kind == ActorKind.FishingSpot ? "CÂU CÁ" : nearest.Kind == ActorKind.Encounter &&
                QuestProgressService.IsActive(save, nearest.Encounter.requiredQuestId) ? "ĐỐI ĐẦU" :
                nearest.Kind == ActorKind.SealClue || nearest.Kind == ActorKind.DawnkeepRoster ? "ĐIỀU TRA" :
                nearest.Kind == ActorKind.RoadGate ? "ĐI TỚI" : "NÓI";
            hud.SetHud("MÁU " + save.health + " / " + MaxHealth,
                "VÀNG " + save.gold + "   •   NANH " + InventoryService.Count(save, "ash_warg_fang") +
                "   •   THUỐC " + CountHealingConsumables(),
                title.ToUpperInvariant(), objective, action);
            SetMonsterCombatHud(mode == PlayMode.Combat, MonsterPhaseHint());
        }

        private string CurrentQuestTitle()
        {
            if (mode == PlayMode.Fishing) return activeFishingSpot?.FishingSpot?.locationId == "choir_beneath_lake"
                ? "CÂU CÁ — WHISPER POOL"
                : activeFishingSpot?.FishingSpot?.locationId == "salt_road"
                    ? "CÂU CÁ — SALT ROAD" : "CÂU CÁ — BỜ HỒ DAWNKEEP";
            if (save.chapterComplete)
            {
                var sideQuest = CurrentActiveSideQuest();
                if (sideQuest != null) return sideQuest.title;
                if (IsQuestCompleted("champion_star_map")) return "Ngôi sao ngoài bầu trời Asterra";
                if (IsQuestCompleted("choir_reckoning")) return "Tiếng vọng thứ chín mươi chín";
                if (IsQuestCompleted("salt_reckoning")) return "Ba lời kể trên Salt Road";
                if (IsQuestCompleted("cinder_recovery")) return "Mùa vụ tiếp theo — Cinderwell Basin";
                return IsOrderArcUnlocked() ? "Hồ sơ Dawnkeep đã khép lại" : "Bình minh sau tro tàn";
            }
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest != null) return quest.title;
            return "Đang chờ nhiệm vụ khả dụng";
        }

        private QuestDefinition CurrentActiveSideQuest()
        {
            foreach (var quest in QuestProgressService.GetActiveQuests(save, questCatalog))
                if (quest.type == "side") return quest;
            return null;
        }

        private int CountHealingConsumables()
        {
            var total = 0;
            foreach (var item in ItemCatalog.Entries)
                if (item != null && item.category == "consumable" && item.healAmount > 0)
                    total += InventoryService.Count(save, item.id);
            return total;
        }

        private string CurrentObjective()
        {
            if (mode == PlayMode.Fishing)
                return fishingBiteActive
                    ? "PHAO RUNG! GIẬT CẦN trong " + Mathf.CeilToInt(fishingBiteRemaining) + " giây!"
                    : "Đợi phao rung rồi GIẬT CẦN. E để hủy.";
            if (save.chapterComplete)
            {
                var sideQuest = CurrentActiveSideQuest();
                if (sideQuest != null)
                {
                    var objectiveLines = new List<string>();
                    foreach (var sideObjective in sideQuest.objectives)
                    {
                        var progress = QuestProgressService.GetObjectiveProgress(save, sideQuest, sideObjective);
                        objectiveLines.Add(sideObjective.description + "  [" + progress + "/" +
                                           sideObjective.requiredCount + "]");
                    }
                    return string.Join("\n", objectiveLines);
                }
                if (IsQuestCompleted("choir_reckoning"))
                    return "Chín mươi chín chu kỳ đã để lại dấu vết. Kho bản đồ phía bắc có thể chứng minh còn một con đường khác.";
                if (IsQuestCompleted("salt_reckoning"))
                    return "Ba nhân chứng đã ký vào cùng một biên bản. Con đường phía tây dẫn tới mặt nước phát ra tiếng chuông.";
                if (IsQuestCompleted("cinder_recovery"))
                    return "Cửa hồ đã mở. Người dân quyết định cách chia nguồn nước còn lại.";
                return IsOrderArcUnlocked()
                    ? "Những hồ sơ phía đông đã khép lại. Hành trình còn tiếp tục ngoài Dawnkeep."
                    : "Chương Ashfall đã khép lại. Hành trình tiếp tục theo con đường phía đông.";
            }
            var quest = QuestProgressService.GetActiveQuest(save, questCatalog);
            if (quest != null) return quest.objective;
            return "Chưa có nhiệm vụ nào đủ điều kiện mở.";
        }

        private void LoadQuestCatalog()
        {
            questCatalog = QuestCatalogService.Load();
        }

        private void LoadDialogueCatalog()
        {
            dialogueCatalog = DialogueCatalogService.Load();
        }

        private void LoadMonsterCatalog()
        {
            monsterCatalog = MonsterCatalogService.Load();
        }

        private MonsterDefinition FindMonsterDefinition(string monsterId)
        {
            var definition = MonsterCatalogService.FindById(monsterCatalog, monsterId);
            if (definition != null) return definition;
            if (monsterId != "ash_warg") return null;
            Debug.LogError("Monster catalog has no ash_warg definition; using the built-in slice fallback.");
            return CreateAshWargFallback();
        }

        private static MonsterDefinition CreateAshWargFallback()
        {
            return new MonsterDefinition
            {
                id = "ash_warg",
                displayName = "Ash Warg",
                maxHealth = 36,
                attackDamage = 6,
                attackReach = 2.8f,
                approachSpeed = 1.8f,
                lungeDistance = 2.4f,
                lungeSeconds = 0.18f,
                lungeStopDistance = 0.7f,
                openingDelay = 1.05f,
                closingSeconds = 1.25f,
                telegraphSeconds = 0.82f,
                recoverySeconds = 0.78f,
                counterBonusDamage = 6,
                hitCooldown = 0.36f,
                spriteResource = "ash_warg",
                lungeSpriteResource = "ash_warg_lunge",
                spriteScale = 0.36f
            };
        }

        private int ActiveMonsterMaxHealth => activeMonsterDefinition != null ? activeMonsterDefinition.maxHealth : 0;

        private string MonsterPhaseHint()
        {
            if (activeMonsterDefinition == null) return "";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "ranged_bolt")
                return "ĐẠN ĐANG NGẮM THEO LÀN — LƯỚT RA KHỎI VỆT SÁNG";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "marked_strike")
                return "DẤU NỔ ĐÃ KHÓA VỊ TRÍ — RỜI KHỎI VÒNG TÍM";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "line_charge")
                return "ĐƯỜNG LAO ĐÃ KHÓA — LƯỚT NGANG RA KHỎI VỆT SÁNG";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "shockwave")
                return "SÓNG CHẤN ĐANG TÍCH TỤ — LƯỚT RA XA";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "siphon")
                return "DÒNG NƯỚC RÚT LỰC — LƯỚT RA NGOÀI VÒNG HÚT";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph && activeMonsterDefinition.specialMoveId == "hook")
                return "MÓC XÍCH ĐÃ KHÓA — LƯỚT NGANG ĐỂ THOÁT";
            if (monsterAttackPhase == MonsterAttackPhase.Telegraph) return "ĐÒN TỚI GẦN — LƯỚT NÉ";
            if (monsterAttackPhase == MonsterAttackPhase.Lunging)
            {
                if (activeMonsterDefinition.specialMoveId == "ranged_bolt") return activeMonsterDefinition.displayName.ToUpperInvariant() + " BẮN ĐẠN!";
                if (activeMonsterDefinition.specialMoveId == "marked_strike") return "VÙNG NỔ SẮP KÍCH HOẠT!";
                return activeMonsterDefinition.displayName.ToUpperInvariant() + " LAO TỚI!";
            }
            if (monsterAttackPhase == MonsterAttackPhase.Recovery) return activeMonsterDefinition.displayName.ToUpperInvariant() + " LỘ SƠ HỞ — TẤN CÔNG";
            return activeMonsterDefinition.displayName.ToUpperInvariant() + " ĐANG ÁP SÁT";
        }

        private void SetMonsterCombatHud(bool visible, string hint = "")
        {
            if (hud == null) return;
            var enemyName = activeMonsterDefinition == null ? "" :
                (activeMonsterDefinition.rank == "boss" ? "BOSS • " :
                    activeMonsterDefinition.rank == "elite" ? "ELITE • " : "") +
                activeMonsterDefinition.displayName.ToUpperInvariant();
            hud.SetCombat(visible, activeEncounterProgress != null ? activeEncounterProgress.health : 0, hint,
                enemyName, ActiveMonsterMaxHealth);
        }

        private void ShowDialogue(string dialogueId, Action onComplete, string token = "", string replacement = "")
        {
            var dialogue = DialogueCatalogService.Find(dialogueCatalog, dialogueId);
            if (dialogue == null)
            {
                Debug.LogError("Missing dialogue ID: " + dialogueId);
                mode = PlayMode.Exploring;
                hud.SetExploringControls(true);
                return;
            }

            var lines = dialogue.lines.ToArray();
            if (!string.IsNullOrEmpty(token))
                for (var i = 0; i < lines.Length; i++) lines[i] = lines[i].Replace(token, replacement ?? "");
            hud.ShowLines(dialogue.speakerName, lines, onComplete);
        }

        private void AnimateActors()
        {
            var time = Time.time;
            foreach (var actor in actors)
            {
                if (actor.Transform == null || !actor.Transform.gameObject.activeInHierarchy) continue;
                if (actor.Kind == ActorKind.Encounter && mode == PlayMode.Combat) continue;
                var offset = actor.Kind == ActorKind.Encounter ? 0.04f : 0.025f;
                var period = actor.Kind == ActorKind.Encounter ? 3.0f : 2.5f;
                var idleOffset = Mathf.Round(Mathf.Sin(time * period) * offset * 16f) / 16f;
                actor.Transform.position = new Vector3(actor.BasePosition.x, actor.BasePosition.y + idleOffset,
                    actor.BasePosition.z);
            }
        }

        private void UpdatePlayerAnimation(Vector2 movement)
        {
            if (playerRenderer == null) return;
            if (playerWalkFrames == null)
            {
                if (Mathf.Abs(movement.x) > 0.05f) playerRenderer.flipX = movement.x < 0;
                return;
            }

            var moving = movement.sqrMagnitude > 0.04f;
            if (moving)
            {
                if (Mathf.Abs(movement.y) > Mathf.Abs(movement.x))
                    playerFacingRow = movement.y > 0 ? 3 : 0;
                else
                    playerFacingRow = movement.x < 0 ? 1 : 2;

                playerWalkFrameTimer -= Time.deltaTime;
                if (playerWalkFrameTimer <= 0)
                {
                    playerWalkFrame = (playerWalkFrame + 1) % playerWalkFrames[playerFacingRow].Length;
                    playerWalkFrameTimer = 0.13f;
                }
            }
            else
            {
                playerWalkFrame = 0;
                playerWalkFrameTimer = 0;
            }

            playerRenderer.flipX = false;
            var nextFrame = playerWalkFrames[playerFacingRow][playerWalkFrame];
            if (playerRenderer.sprite != nextFrame) playerRenderer.sprite = nextFrame;
        }

        private static Sprite[][] CreatePlayerWalkFrames(Texture2D texture)
        {
            if (texture == null || texture.width < 4 || texture.height < 4 || !texture.isReadable)
            {
                Debug.LogWarning("Rowan's walk atlas must be a readable 4 by 4 sprite sheet.");
                return null;
            }

            texture.filterMode = FilterMode.Point;
            texture.wrapMode = TextureWrapMode.Clamp;
            var xBounds = new int[5];
            var yBounds = new int[5];
            for (var i = 0; i <= 4; i++)
            {
                xBounds[i] = Mathf.RoundToInt(texture.width * i / 4f);
                yBounds[i] = Mathf.RoundToInt(texture.height * i / 4f);
            }

            var pixels = texture.GetPixels32();
            var result = new Sprite[4][];
            for (var rowFromTop = 0; rowFromTop < 4; rowFromTop++)
            {
                var cellYMin = texture.height - yBounds[rowFromTop + 1];
                var cellYMax = texture.height - yBounds[rowFromTop];
                var baselineY = cellYMax - 1;
                var foundOpaquePixel = false;
                for (var column = 0; column < 4; column++)
                {
                    for (var y = cellYMin; y < cellYMax; y++)
                    {
                        for (var x = xBounds[column]; x < xBounds[column + 1]; x++)
                        {
                            if (pixels[y * texture.width + x].a < 16) continue;
                            baselineY = Mathf.Min(baselineY, y);
                            foundOpaquePixel = true;
                        }
                    }
                }

                result[rowFromTop] = new Sprite[4];
                for (var column = 0; column < 4; column++)
                {
                    var cellXMin = xBounds[column];
                    var cellWidth = xBounds[column + 1] - cellXMin;
                    var cellHeight = cellYMax - cellYMin;
                    var pivotY = foundOpaquePixel
                        ? Mathf.Clamp01((baselineY - cellYMin + 0.5f) / cellHeight)
                        : 0.04f;
                    var rect = new Rect(cellXMin, cellYMin, cellWidth, cellHeight);
                    result[rowFromTop][column] = Sprite.Create(texture, rect,
                        new Vector2(0.5f, pivotY), 64f, 0, SpriteMeshType.FullRect);
                    result[rowFromTop][column].name = "Rowan walk " + rowFromTop + " " + column;
                }
            }

            return result;
        }

        private void ClearMonsterHitFlash()
        {
            if (!enemyHitFlash || enemyRenderer == null) return;
            enemyRenderer.color = Color.white;
            enemyHitFlash = false;
        }

        private Sprite LoadVfxSprite(string resourceName)
        {
            var texture = Resources.Load<Texture2D>("VFX/" + resourceName);
            if (texture == null)
            {
                Debug.LogWarning("Optional combat VFX texture is missing: VFX/" + resourceName);
                return null;
            }
            return SpriteFromTexture(texture, texture.width, new Vector2(0.5f, 0.5f));
        }

        private void SpawnTelegraphRing(float radius, float duration)
        {
            if (enemyRoot == null || telegraphRingVfx == null) return;
            var color = activeMonsterDefinition.specialMoveId == "siphon"
                ? new Color(0.24f, 0.93f, 0.82f, 0.82f)
                : activeMonsterDefinition.specialMoveId == "hook"
                    ? new Color(1f, 0.68f, 0.2f, 0.82f)
                    : new Color(1f, 0.37f, 0.28f, 0.82f);
            SpawnPixelEffect(telegraphRingVfx, enemyRoot.position, color, 0.22f,
                Mathf.Max(0.9f, radius * 2f), duration, 2);
        }

        private void SpawnBossChargeTelegraph(Vector2 origin, Vector2 direction, float length, float duration)
        {
            if (worldRoot == null || direction.sqrMagnitude <= 0.001f) return;
            if (lineTelegraphSprite == null)
                lineTelegraphSprite = CreatePixelSprite("Boss charge lane", 64, 6, DrawChargeLanePixelArt);
            var telegraph = new GameObject("Monster attack lane telegraph");
            telegraph.transform.SetParent(worldRoot, false);
            telegraph.transform.position = origin + direction.normalized * (length * 0.5f);
            telegraph.transform.rotation = Quaternion.Euler(0, 0,
                Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg);
            telegraph.transform.localScale = new Vector3(length / 64f, 0.13f, 1f);
            var renderer = telegraph.AddComponent<SpriteRenderer>();
            renderer.sprite = lineTelegraphSprite;
            renderer.color = activeMonsterDefinition != null && activeMonsterDefinition.specialMoveId == "ranged_bolt"
                ? new Color(0.86f, 0.5f, 1f, 0.94f) : new Color(1f, 0.55f, 0.2f, 0.9f);
            renderer.sortingOrder = 2;
            StartCoroutine(RemoveBossChargeTelegraph(telegraph, duration));
        }

        private void SpawnTargetStrikeTelegraph(Vector2 target, float radius, float duration)
        {
            if (telegraphRingVfx == null || worldRoot == null) return;
            SpawnPixelEffect(telegraphRingVfx, target, new Color(0.82f, 0.42f, 0.96f, 0.9f),
                0.28f, Mathf.Max(1.1f, radius * 2f), duration, 3);
        }

        private static IEnumerator RemoveBossChargeTelegraph(GameObject telegraph, float duration)
        {
            yield return new WaitForSeconds(Mathf.Max(0.05f, duration));
            if (telegraph != null) Destroy(telegraph);
        }

        private void SpawnPixelEffect(Sprite sprite, Vector3 position, Color tint, float startScale,
            float endScale, float duration, int sortingOrder)
        {
            if (sprite == null || worldRoot == null) return;
            var effect = new GameObject("Ashen Oath combat VFX");
            effect.transform.SetParent(worldRoot, false);
            effect.transform.position = position;
            effect.transform.localScale = Vector3.one * startScale;
            var renderer = effect.AddComponent<SpriteRenderer>();
            renderer.sprite = sprite;
            renderer.color = tint;
            renderer.sortingOrder = sortingOrder;
            StartCoroutine(AnimatePixelEffect(effect.transform, renderer, tint, startScale, endScale,
                Mathf.Max(0.06f, duration)));
        }

        private static IEnumerator AnimatePixelEffect(Transform effect, SpriteRenderer renderer, Color tint,
            float startScale, float endScale, float duration)
        {
            var elapsed = 0f;
            var baseAlpha = tint.a;
            while (elapsed < duration && effect != null && renderer != null)
            {
                elapsed += Time.deltaTime;
                var progress = Mathf.Clamp01(elapsed / duration);
                var eased = Mathf.SmoothStep(0f, 1f, progress);
                effect.localScale = Vector3.one * Mathf.Lerp(startScale, endScale, eased);
                tint.a = baseAlpha * (1f - eased);
                renderer.color = tint;
                yield return null;
            }
            if (effect != null) Destroy(effect.gameObject);
        }

        private void SaveNow()
        {
            if (save == null || player == null) return;
            save.playerX = player.position.x;
            save.playerY = player.position.y;
            SaveService.Save(save);
        }

        private void OnApplicationPause(bool paused)
        {
            if (paused) SaveNow();
        }

        private void OnApplicationQuit() => SaveNow();

        private static Sprite SpriteFromTexture(Texture2D texture, float pixelsPerUnit, Vector2 pivot)
        {
            texture.wrapMode = TextureWrapMode.Clamp;
            texture.filterMode = FilterMode.Point;
            return Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), pivot, pixelsPerUnit,
                0, SpriteMeshType.FullRect);
        }

        private delegate void PixelDrawer(Color32[] pixels, int width, int height);

        private static Sprite CreatePixelSprite(string name, int width, int height, PixelDrawer draw)
        {
            var texture = new Texture2D(width, height, TextureFormat.RGBA32, false)
            {
                name = name + " texture",
                filterMode = FilterMode.Point,
                wrapMode = TextureWrapMode.Clamp
            };
            var pixels = new Color32[width * height];
            draw(pixels, width, height);
            texture.SetPixels32(pixels);
            texture.Apply(false, false);
            return Sprite.Create(texture, new Rect(0, 0, width, height), new Vector2(0.5f, 0.04f), 1,
                0, SpriteMeshType.FullRect);
        }

        private Sprite GetInventoryIcon(string itemId)
        {
            if (itemId != null && itemId.StartsWith("fieldgear_", StringComparison.Ordinal))
            {
                if (fieldGearIconCache.TryGetValue(itemId, out var cachedIcon)) return cachedIcon;
                var item = ItemCatalog.Find(itemId);
                if (item == null || item.category != "equipment") return null;
                var accent = FieldGearAccent(itemId);
                var icon = CreatePixelSprite(itemId + " inventory icon", 32, 32,
                    (pixels, width, height) => DrawFieldGearIconPixelArt(
                        pixels, width, height, item.equipmentSlot, accent));
                fieldGearIconCache.Add(itemId, icon);
                return icon;
            }
            if (itemId == "outerwake_field_compass")
            {
                if (outerwakeFieldCompassIcon == null)
                    outerwakeFieldCompassIcon = CreatePixelSprite("Outer-Wake field compass inventory icon", 32, 32,
                        DrawOuterwakeFieldCompassPixelArt);
                return outerwakeFieldCompassIcon;
            }
            if (itemId == "cistern_ledger_clasp")
            {
                if (cisternLedgerClaspIcon == null)
                    cisternLedgerClaspIcon = CreatePixelSprite("Cistern ledger clasp inventory icon", 32, 32,
                        DrawCisternLedgerClaspPixelArt);
                return cisternLedgerClaspIcon;
            }
            if (itemId == "greenwake_open_sowing_charm")
            {
                if (greenwakeOpenSowingCharmIcon == null)
                    greenwakeOpenSowingCharmIcon = CreatePixelSprite("Greenwake open-sowing charm inventory icon", 32, 32,
                        DrawGreenwakeOpenSowingCharmPixelArt);
                return greenwakeOpenSowingCharmIcon;
            }
            if (itemId != "cadet_flow_charm") return null;
            if (cadetFlowCharmIcon == null)
                cadetFlowCharmIcon = CreatePixelSprite("Cadet waterline charm inventory icon", 32, 32,
                    DrawCadetFlowCharmPixelArt);
            return cadetFlowCharmIcon;
        }

        private static Color32 FieldGearAccent(string itemId)
        {
            if (itemId.Contains("_af_")) return new Color32(203, 115, 80, 255);
            if (itemId.Contains("_do_") || itemId.Contains("_db_")) return new Color32(165, 183, 191, 255);
            if (itemId.Contains("_cw_")) return new Color32(226, 146, 76, 255);
            if (itemId.Contains("_cc_")) return new Color32(103, 197, 166, 255);
            if (itemId.Contains("_sr_")) return new Color32(220, 188, 119, 255);
            if (itemId.Contains("_sl_")) return new Color32(132, 181, 207, 255);
            if (itemId.Contains("_ch_")) return new Color32(155, 165, 236, 255);
            if (itemId.Contains("_gw_")) return new Color32(132, 196, 112, 255);
            if (itemId.Contains("_ow_")) return new Color32(204, 148, 231, 255);
            return new Color32(232, 117, 104, 255);
        }

        private static void DrawFieldGearIconPixelArt(Color32[] pixels, int width, int height,
            string equipmentSlot, Color32 accent)
        {
            var outline = new Color32(28, 29, 45, 255);
            var backing = new Color32(53, 56, 76, 255);
            var light = new Color32(239, 222, 177, 255);
            Fill(pixels, width, height, 3, 3, 26, 26, outline);
            Fill(pixels, width, height, 5, 5, 22, 22, backing);

            if (equipmentSlot == "weapon")
            {
                for (var step = 0; step < 12; step++)
                {
                    var x = 8 + step;
                    var y = 20 - step;
                    SetGearIconPixel(pixels, width, height, x - 1, y, outline);
                    SetGearIconPixel(pixels, width, height, x, y, light);
                    SetGearIconPixel(pixels, width, height, x, y - 1, accent);
                }
                Fill(pixels, width, height, 8, 18, 8, 3, outline);
                Fill(pixels, width, height, 9, 18, 6, 1, accent);
                Fill(pixels, width, height, 7, 22, 3, 6, outline);
                Fill(pixels, width, height, 8, 23, 1, 4, light);
                return;
            }

            if (equipmentSlot == "armor")
            {
                Fill(pixels, width, height, 9, 8, 14, 3, outline);
                Fill(pixels, width, height, 7, 11, 18, 8, outline);
                Fill(pixels, width, height, 9, 12, 14, 6, accent);
                Fill(pixels, width, height, 10, 18, 12, 6, outline);
                Fill(pixels, width, height, 12, 19, 8, 3, accent);
                Fill(pixels, width, height, 14, 12, 3, 8, light);
                Fill(pixels, width, height, 10, 23, 4, 3, outline);
                Fill(pixels, width, height, 18, 23, 4, 3, outline);
                return;
            }

            for (var step = 0; step < 8; step++)
            {
                SetGearIconPixel(pixels, width, height, 10 + step, 9, outline);
                SetGearIconPixel(pixels, width, height, 10 + step, 8, accent);
            }
            Fill(pixels, width, height, 12, 14, 8, 9, outline);
            Fill(pixels, width, height, 13, 15, 6, 7, accent);
            Fill(pixels, width, height, 14, 17, 4, 3, light);
        }

        private static void SetGearIconPixel(Color32[] pixels, int width, int height, int x, int y,
            Color32 color)
        {
            if (x < 0 || y < 0 || x >= width || y >= height) return;
            pixels[y * width + x] = color;
        }

        private static void DrawMiraPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var hair = new Color32(94, 54, 42, 255);
            var skin = new Color32(231, 177, 137, 255);
            var coat = new Color32(55, 111, 90, 255);
            var lightCoat = new Color32(92, 157, 120, 255);
            var cloth = new Color32(208, 194, 151, 255);
            var boot = new Color32(74, 52, 47, 255);
            Fill(p, w, h, 8, 0, 6, 8, outline); Fill(p, w, h, 9, 1, 4, 6, boot);
            Fill(p, w, h, 7, 7, 8, 15, outline); Fill(p, w, h, 8, 8, 6, 13, coat);
            Fill(p, w, h, 9, 9, 3, 10, lightCoat); Fill(p, w, h, 5, 10, 3, 8, outline);
            Fill(p, w, h, 6, 11, 2, 6, skin); Fill(p, w, h, 14, 10, 3, 8, outline);
            Fill(p, w, h, 15, 11, 2, 6, skin); Fill(p, w, h, 9, 11, 4, 6, cloth);
            Fill(p, w, h, 8, 21, 7, 3, outline); Fill(p, w, h, 8, 22, 7, 2, skin);
            Fill(p, w, h, 7, 24, 10, 9, outline); Fill(p, w, h, 8, 25, 8, 7, skin);
            Fill(p, w, h, 7, 30, 10, 4, hair); Fill(p, w, h, 6, 26, 3, 7, hair);
            Fill(p, w, h, 16, 27, 2, 8, hair); Fill(p, w, h, 9, 29, 1, 1, outline);
            Fill(p, w, h, 14, 29, 1, 1, outline); Fill(p, w, h, 4, 13, 2, 4, outline);
        }

        private static void DrawElaraPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var coat = new Color32(61, 76, 104, 255);
            var light = new Color32(211, 202, 173, 255);
            var skin = new Color32(226, 177, 143, 255);
            var hair = new Color32(73, 48, 43, 255);
            var brass = new Color32(207, 159, 73, 255);
            Fill(p, w, h, 8, 0, 15, 6, outline); Fill(p, w, h, 9, 1, 12, 4, new Color32(82, 61, 50, 255));
            Fill(p, w, h, 9, 6, 13, 15, outline); Fill(p, w, h, 10, 7, 11, 12, skin);
            Fill(p, w, h, 8, 16, 15, 5, hair); Fill(p, w, h, 7, 8, 4, 18, hair);
            Fill(p, w, h, 19, 15, 4, 13, hair); Fill(p, w, h, 5, 21, 21, 16, outline);
            Fill(p, w, h, 6, 22, 19, 14, coat); Fill(p, w, h, 12, 22, 7, 14, light);
            Fill(p, w, h, 13, 19, 5, 4, brass); Fill(p, w, h, 19, 23, 8, 10, outline);
            Fill(p, w, h, 20, 24, 6, 8, new Color32(105, 75, 50, 255));
            Fill(p, w, h, 7, 35, 7, 7, outline); Fill(p, w, h, 17, 35, 7, 7, outline);
            Fill(p, w, h, 8, 36, 5, 5, new Color32(90, 68, 58, 255));
            Fill(p, w, h, 18, 36, 5, 5, new Color32(90, 68, 58, 255));
            Fill(p, w, h, 11, 12, 2, 1, outline); Fill(p, w, h, 18, 12, 2, 1, outline);
        }

        private static void DrawGideonPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var skin = new Color32(194, 145, 111, 255);
            var coat = new Color32(113, 84, 62, 255);
            var cloth = new Color32(190, 178, 149, 255);
            var gray = new Color32(111, 112, 120, 255);
            Fill(p, w, h, 7, 0, 11, 8, outline); Fill(p, w, h, 8, 1, 9, 6, coat);
            Fill(p, w, h, 8, 8, 10, 14, outline); Fill(p, w, h, 9, 9, 8, 12, skin);
            Fill(p, w, h, 7, 14, 12, 4, gray); Fill(p, w, h, 9, 12, 2, 1, outline);
            Fill(p, w, h, 15, 12, 2, 1, outline); Fill(p, w, h, 6, 21, 14, 14, outline);
            Fill(p, w, h, 7, 22, 12, 12, coat); Fill(p, w, h, 11, 22, 4, 10, cloth);
            Fill(p, w, h, 7, 33, 5, 4, outline); Fill(p, w, h, 14, 33, 5, 4, outline);
            Fill(p, w, h, 4, 24, 3, 9, outline); Fill(p, w, h, 19, 24, 3, 9, outline);
        }

        private static void DrawAldenPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var skin = new Color32(205, 151, 115, 255);
            var armor = new Color32(64, 72, 91, 255);
            var steel = new Color32(153, 164, 172, 255);
            var gold = new Color32(225, 174, 79, 255);
            Fill(p, w, h, 6, 0, 13, 8, outline); Fill(p, w, h, 7, 1, 11, 6, armor);
            Fill(p, w, h, 8, 8, 10, 14, outline); Fill(p, w, h, 9, 9, 8, 12, skin);
            Fill(p, w, h, 9, 9, 8, 3, steel); Fill(p, w, h, 9, 12, 2, 1, outline);
            Fill(p, w, h, 15, 12, 2, 1, outline); Fill(p, w, h, 6, 21, 14, 14, outline);
            Fill(p, w, h, 7, 22, 12, 12, armor); Fill(p, w, h, 8, 23, 10, 3, steel);
            Fill(p, w, h, 12, 24, 3, 7, gold); Fill(p, w, h, 11, 31, 5, 4, outline);
            Fill(p, w, h, 7, 34, 5, 3, outline); Fill(p, w, h, 14, 34, 5, 3, outline);
            Fill(p, w, h, 3, 23, 4, 10, outline); Fill(p, w, h, 19, 23, 4, 10, outline);
        }

        private static void DrawBurnedSealPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var ash = new Color32(70, 63, 63, 255);
            var bronze = new Color32(169, 111, 55, 255);
            var ember = new Color32(229, 151, 67, 255);
            Fill(p, w, h, 1, 2, 17, 16, outline); Fill(p, w, h, 3, 4, 13, 12, ash);
            Fill(p, w, h, 5, 6, 9, 8, bronze); Fill(p, w, h, 7, 8, 5, 4, outline);
            Fill(p, w, h, 8, 5, 2, 10, ember); Fill(p, w, h, 5, 9, 8, 2, ember);
            Fill(p, w, h, 2, 3, 3, 2, ember); Fill(p, w, h, 14, 14, 3, 2, ember);
        }

        private static void DrawAshfallHerbLedgerPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(35, 29, 35, 255);
            var leather = new Color32(102, 62, 46, 255);
            var paper = new Color32(227, 207, 157, 255);
            var ink = new Color32(78, 64, 52, 255);
            var ember = new Color32(205, 106, 55, 255);
            Fill(p, w, h, 2, 2, 24, 30, outline); Fill(p, w, h, 4, 4, 20, 26, leather);
            Fill(p, w, h, 7, 6, 15, 21, paper); Fill(p, w, h, 9, 10, 10, 2, ink);
            Fill(p, w, h, 9, 15, 11, 2, ink); Fill(p, w, h, 9, 20, 8, 2, ink);
            Fill(p, w, h, 18, 23, 3, 3, ember); Fill(p, w, h, 4, 30, 20, 2, outline);
        }

        private static void DrawWaymarkerPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 38, 255);
            var wood = new Color32(112, 73, 47, 255);
            var lightWood = new Color32(180, 129, 77, 255);
            var paleBoard = new Color32(220, 205, 164, 255);
            var blueMark = new Color32(87, 132, 151, 255);
            var brass = new Color32(220, 176, 82, 255);
            Fill(p, w, h, 13, 14, 6, 24, outline);
            Fill(p, w, h, 15, 16, 2, 20, wood);
            Fill(p, w, h, 4, 4, 24, 11, outline);
            Fill(p, w, h, 6, 6, 20, 7, paleBoard);
            Fill(p, w, h, 7, 8, 7, 2, blueMark);
            Fill(p, w, h, 18, 8, 6, 2, blueMark);
            Fill(p, w, h, 2, 14, 19, 10, outline);
            Fill(p, w, h, 4, 16, 15, 6, wood);
            Fill(p, w, h, 8, 18, 8, 2, brass);
            Fill(p, w, h, 11, 21, 3, 2, paleBoard);
            Fill(p, w, h, 9, 37, 14, 3, outline);
            Fill(p, w, h, 11, 38, 10, 1, lightWood);
        }

        private static void DrawAshfallDoorBracePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(33, 28, 35, 255);
            var wood = new Color32(116, 74, 48, 255);
            var wornWood = new Color32(176, 122, 73, 255);
            var iron = new Color32(77, 83, 91, 255);
            var chalk = new Color32(211, 199, 162, 255);
            Fill(p, w, h, 2, 19, 28, 6, outline);
            Fill(p, w, h, 4, 20, 24, 3, wood);
            Fill(p, w, h, 7, 15, 18, 5, outline);
            Fill(p, w, h, 9, 16, 14, 3, wornWood);
            Fill(p, w, h, 11, 13, 10, 3, iron);
            Fill(p, w, h, 13, 10, 7, 4, wood);
            Fill(p, w, h, 15, 8, 3, 3, chalk);
            Fill(p, w, h, 5, 22, 3, 1, iron);
            Fill(p, w, h, 24, 22, 3, 1, iron);
        }

        private static void DrawAshfallCartWheelPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 37, 255);
            var wood = new Color32(131, 78, 45, 255);
            var wornWood = new Color32(190, 132, 76, 255);
            var iron = new Color32(86, 91, 94, 255);
            var brightIron = new Color32(170, 174, 162, 255);
            var ash = new Color32(70, 58, 53, 255);
            Fill(p, w, h, 4, 5, 37, 18, outline);
            Fill(p, w, h, 7, 7, 31, 13, wood);
            Fill(p, w, h, 10, 9, 24, 4, wornWood);
            Fill(p, w, h, 8, 18, 29, 4, iron);
            Fill(p, w, h, 9, 19, 25, 2, brightIron);
            Fill(p, w, h, 2, 18, 7, 18, outline);
            Fill(p, w, h, 4, 20, 3, 13, iron);
            Fill(p, w, h, 29, 20, 10, 17, outline);
            Fill(p, w, h, 31, 22, 6, 13, ash);
            Fill(p, w, h, 32, 23, 3, 11, iron);
            Fill(p, w, h, 2, 35, 39, 3, outline);
            Fill(p, w, h, 5, 36, 33, 1, wornWood);
            Fill(p, w, h, 32, 27, 3, 3, brightIron);
            Fill(p, w, h, 29, 31, 8, 3, outline);
        }

        private static void DrawAshfallCartRutPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(40, 33, 35, 255);
            var soil = new Color32(120, 72, 47, 255);
            var dust = new Color32(196, 142, 84, 255);
            var stone = new Color32(93, 83, 70, 255);
            Fill(p, w, h, 2, 6, 36, 16, outline);
            Fill(p, w, h, 4, 8, 32, 11, soil);
            Fill(p, w, h, 5, 11, 30, 3, dust);
            Fill(p, w, h, 7, 15, 26, 3, outline);
            Fill(p, w, h, 9, 16, 22, 1, soil);
            Fill(p, w, h, 3, 18, 5, 5, stone);
            Fill(p, w, h, 30, 17, 7, 6, stone);
            Fill(p, w, h, 13, 4, 10, 3, dust);
            Fill(p, w, h, 17, 2, 6, 2, stone);
        }

        private static void DrawAshfallCartSpokesPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 37, 255);
            var wood = new Color32(141, 86, 49, 255);
            var paleWood = new Color32(211, 159, 94, 255);
            var iron = new Color32(87, 91, 93, 255);
            var brass = new Color32(226, 175, 78, 255);
            Fill(p, w, h, 4, 4, 27, 26, outline);
            Fill(p, w, h, 6, 6, 23, 22, wood);
            Fill(p, w, h, 8, 8, 19, 18, outline);
            Fill(p, w, h, 10, 10, 15, 14, iron);
            Fill(p, w, h, 12, 12, 11, 10, paleWood);
            Fill(p, w, h, 16, 7, 3, 20, outline);
            Fill(p, w, h, 17, 8, 1, 18, paleWood);
            Fill(p, w, h, 8, 15, 19, 3, outline);
            Fill(p, w, h, 9, 16, 17, 1, paleWood);
            Fill(p, w, h, 12, 11, 11, 11, outline);
            Fill(p, w, h, 13, 12, 9, 9, brass);
            Fill(p, w, h, 30, 18, 5, 4, wood);
        }

        private static void DrawAshfallCartTestPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(35, 30, 37, 255);
            var wood = new Color32(134, 81, 47, 255);
            var gold = new Color32(221, 169, 77, 255);
            var stone = new Color32(99, 91, 77, 255);
            var green = new Color32(112, 149, 83, 255);
            Fill(p, w, h, 1, 26, 40, 5, outline);
            Fill(p, w, h, 3, 27, 36, 2, stone);
            Fill(p, w, h, 4, 12, 23, 12, outline);
            Fill(p, w, h, 6, 14, 19, 8, wood);
            Fill(p, w, h, 7, 15, 17, 2, gold);
            Fill(p, w, h, 8, 23, 5, 7, outline);
            Fill(p, w, h, 9, 24, 3, 4, stone);
            Fill(p, w, h, 20, 23, 5, 7, outline);
            Fill(p, w, h, 21, 24, 3, 4, stone);
            Fill(p, w, h, 28, 10, 11, 3, outline);
            Fill(p, w, h, 30, 11, 8, 1, green);
            Fill(p, w, h, 33, 5, 2, 14, gold);
            Fill(p, w, h, 31, 5, 6, 2, outline);
            Fill(p, w, h, 31, 17, 6, 2, outline);
        }

        private static void DrawAshfallCartBayPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(35, 29, 37, 255);
            var wood = new Color32(119, 72, 46, 255);
            var paleWood = new Color32(192, 139, 79, 255);
            var canvas = new Color32(218, 204, 162, 255);
            var blue = new Color32(81, 126, 146, 255);
            Fill(p, w, h, 3, 8, 36, 23, outline);
            Fill(p, w, h, 5, 10, 32, 19, wood);
            Fill(p, w, h, 7, 13, 28, 12, paleWood);
            Fill(p, w, h, 9, 14, 24, 3, canvas);
            Fill(p, w, h, 11, 18, 20, 2, blue);
            Fill(p, w, h, 13, 22, 16, 2, canvas);
            Fill(p, w, h, 7, 4, 4, 8, outline);
            Fill(p, w, h, 31, 4, 4, 8, outline);
            Fill(p, w, h, 8, 5, 2, 5, wood);
            Fill(p, w, h, 32, 5, 2, 5, wood);
            Fill(p, w, h, 4, 30, 34, 2, outline);
            Fill(p, w, h, 9, 32, 4, 1, paleWood);
            Fill(p, w, h, 29, 32, 4, 1, paleWood);
        }

        private static void DrawAshfallCartKitTablePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(36, 29, 37, 255);
            var wood = new Color32(130, 81, 49, 255);
            var paleWood = new Color32(197, 145, 83, 255);
            var cloth = new Color32(215, 202, 166, 255);
            var iron = new Color32(94, 100, 103, 255);
            var green = new Color32(126, 151, 91, 255);
            Fill(p, w, h, 3, 13, 34, 5, outline);
            Fill(p, w, h, 5, 14, 30, 3, wood);
            Fill(p, w, h, 7, 17, 4, 14, outline);
            Fill(p, w, h, 9, 18, 2, 11, paleWood);
            Fill(p, w, h, 29, 17, 4, 14, outline);
            Fill(p, w, h, 30, 18, 2, 11, paleWood);
            Fill(p, w, h, 9, 6, 9, 7, outline);
            Fill(p, w, h, 10, 7, 7, 5, cloth);
            Fill(p, w, h, 20, 8, 8, 5, outline);
            Fill(p, w, h, 21, 9, 6, 3, iron);
            Fill(p, w, h, 23, 9, 2, 3, green);
            Fill(p, w, h, 13, 23, 13, 3, wood);
        }

        private static void DrawAshfallCartRepairedPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(33, 28, 36, 255);
            var wood = new Color32(139, 84, 48, 255);
            var freshWood = new Color32(213, 157, 88, 255);
            var iron = new Color32(93, 99, 102, 255);
            var brightIron = new Color32(180, 185, 174, 255);
            var brass = new Color32(229, 181, 83, 255);
            Fill(p, w, h, 6, 8, 36, 17, outline);
            Fill(p, w, h, 8, 10, 32, 13, wood);
            Fill(p, w, h, 11, 12, 26, 4, freshWood);
            Fill(p, w, h, 10, 20, 29, 4, iron);
            Fill(p, w, h, 12, 21, 25, 2, brightIron);
            Fill(p, w, h, 4, 22, 12, 16, outline);
            Fill(p, w, h, 6, 24, 8, 12, iron);
            Fill(p, w, h, 32, 22, 12, 16, outline);
            Fill(p, w, h, 34, 24, 8, 12, iron);
            Fill(p, w, h, 7, 29, 10, 3, brass);
            Fill(p, w, h, 33, 29, 10, 3, brass);
            Fill(p, w, h, 1, 37, 46, 4, outline);
            Fill(p, w, h, 4, 38, 40, 2, freshWood);
            Fill(p, w, h, 22, 23, 3, 5, brightIron);
            Fill(p, w, h, 21, 24, 5, 3, brass);
        }

        private static void DrawHarperWillsPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var skin = new Color32(220, 160, 119, 255);
            var hair = new Color32(145, 65, 42, 255);
            var braid = new Color32(91, 47, 39, 255);
            var coat = new Color32(69, 83, 91, 255);
            var apron = new Color32(111, 72, 47, 255);
            var brass = new Color32(222, 170, 77, 255);
            var cloth = new Color32(204, 190, 151, 255);
            Fill(p,w,h,8,0,15,7,outline); Fill(p,w,h,10,1,11,5,hair);
            Fill(p,w,h,8,6,16,15,outline); Fill(p,w,h,10,7,12,12,skin);
            Fill(p,w,h,8,7,3,9,hair); Fill(p,w,h,21,8,4,13,hair);
            Fill(p,w,h,12,6,8,3,braid); Fill(p,w,h,12,12,2,1,outline); Fill(p,w,h,19,12,2,1,outline);
            Fill(p,w,h,6,21,20,16,outline); Fill(p,w,h,8,22,16,13,coat);
            Fill(p,w,h,11,22,10,13,apron); Fill(p,w,h,13,24,6,2,brass);
            Fill(p,w,h,8,35,7,7,outline); Fill(p,w,h,18,35,7,7,outline);
            Fill(p,w,h,9,36,5,5,braid); Fill(p,w,h,19,36,5,5,braid);
            Fill(p,w,h,22,9,2,2,brass); Fill(p,w,h,5,25,3,8,outline); Fill(p,w,h,24,25,3,8,outline);
            Fill(p,w,h,6,26,2,6,cloth); Fill(p,w,h,24,26,2,6,cloth);
        }

        private static void DrawAshfallSignalFramePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(33, 29, 38, 255);
            var timber = new Color32(105, 67, 46, 255);
            var worn = new Color32(173, 118, 70, 255);
            var iron = new Color32(76, 82, 88, 255);
            var brass = new Color32(203, 148, 63, 255);
            var ash = new Color32(122, 106, 91, 255);
            Fill(p,w,h,5,5,6,34,outline); Fill(p,w,h,7,7,3,30,timber);
            Fill(p,w,h,25,5,6,34,outline); Fill(p,w,h,27,7,3,30,timber);
            Fill(p,w,h,7,5,22,6,outline); Fill(p,w,h,9,7,18,3,worn);
            Fill(p,w,h,9,9,17,4,iron); Fill(p,w,h,13,13,10,4,outline);
            Fill(p,w,h,15,17,6,5,ash); Fill(p,w,h,12,21,12,3,outline);
            Fill(p,w,h,14,24,8,2,brass); Fill(p,w,h,8,34,20,5,outline);
            Fill(p,w,h,10,36,16,2,timber); Fill(p,w,h,10,11,3,3,ash);
            Fill(p,w,h,24,10,3,3,ash); Fill(p,w,h,17,14,2,2,brass);
        }

        private static void DrawAshfallSignalVanePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 29, 39, 255);
            var wood = new Color32(118, 77, 49, 255);
            var brass = new Color32(213, 164, 71, 255);
            var pale = new Color32(226, 209, 161, 255);
            var dark = new Color32(74, 76, 80, 255);
            Fill(p,w,h,16,12,5,26,outline); Fill(p,w,h,18,14,2,22,wood);
            Fill(p,w,h,6,16,24,4,outline); Fill(p,w,h,8,17,20,2,brass);
            Fill(p,w,h,5,17,7,3,outline); Fill(p,w,h,2,18,5,2,outline);
            Fill(p,w,h,22,12,10,12,outline); Fill(p,w,h,24,14,6,8,pale);
            Fill(p,w,h,26,16,2,4,brass); Fill(p,w,h,17,10,3,4,dark);
            Fill(p,w,h,12,21,5,3,outline); Fill(p,w,h,9,23,4,3,brass);
            Fill(p,w,h,15,35,7,4,outline); Fill(p,w,h,12,38,13,3,wood);
        }

        private static void DrawAshfallSignalMarkPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(33, 29, 39, 255);
            var slate = new Color32(98, 108, 106, 255);
            var lightSlate = new Color32(153, 158, 142, 255);
            var chalk = new Color32(228, 205, 143, 255);
            var ember = new Color32(185, 91, 58, 255);
            Fill(p,w,h,2,8,32,17,outline); Fill(p,w,h,4,10,28,13,slate);
            Fill(p,w,h,7,14,9,3,chalk); Fill(p,w,h,16,14,10,3,ember);
            Fill(p,w,h,11,12,3,7,chalk); Fill(p,w,h,22,12,3,7,chalk);
            Fill(p,w,h,7,22,23,2,lightSlate); Fill(p,w,h,5,6,4,3,lightSlate);
            Fill(p,w,h,26,4,3,4,lightSlate); Fill(p,w,h,18,3,2,3,lightSlate);
        }

        private static void DrawAshfallSignalWellPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 30, 39, 255);
            var stone = new Color32(122, 124, 119, 255);
            var pale = new Color32(178, 169, 143, 255);
            var water = new Color32(61, 121, 142, 255);
            var chalk = new Color32(226, 201, 141, 255);
            Fill(p,w,h,3,8,30,21,outline); Fill(p,w,h,6,11,24,14,stone);
            Fill(p,w,h,11,15,14,13,outline); Fill(p,w,h,13,18,10,9,water);
            Fill(p,w,h,8,12,6,3,pale); Fill(p,w,h,22,12,6,3,pale);
            Fill(p,w,h,10,14,5,2,chalk); Fill(p,w,h,4,7,28,4,outline);
            Fill(p,w,h,6,8,24,2,pale); Fill(p,w,h,14,23,8,2,chalk);
        }

        private static void DrawAshfallSignalRidgePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 30, 40, 255);
            var timber = new Color32(112, 74, 47, 255);
            var pale = new Color32(225, 209, 165, 255);
            var dark = new Color32(67, 74, 80, 255);
            var brass = new Color32(211, 166, 76, 255);
            Fill(p,w,h,15,8,6,32,outline); Fill(p,w,h,17,10,2,28,timber);
            Fill(p,w,h,18,12,13,4,outline); Fill(p,w,h,20,14,9,2,pale);
            Fill(p,w,h,7,20,20,5,outline); Fill(p,w,h,9,22,16,2,dark);
            Fill(p,w,h,4,30,28,8,outline); Fill(p,w,h,6,32,24,5,timber);
            Fill(p,w,h,9,29,5,3,brass); Fill(p,w,h,24,27,5,3,brass);
            Fill(p,w,h,13,7,10,3,outline); Fill(p,w,h,16,4,4,4,brass);
        }

        private static void DrawAshfallSignalBellTestPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 29, 39, 255);
            var brass = new Color32(177, 119, 48, 255);
            var gold = new Color32(229, 179, 77, 255);
            var light = new Color32(250, 218, 137, 255);
            var wood = new Color32(105, 69, 47, 255);
            Fill(p,w,h,5,3,22,5,outline); Fill(p,w,h,7,5,18,2,wood);
            Fill(p,w,h,14,8,5,7,outline); Fill(p,w,h,9,14,15,13,outline);
            Fill(p,w,h,11,15,11,10,brass); Fill(p,w,h,13,16,7,5,gold);
            Fill(p,w,h,14,18,4,2,light); Fill(p,w,h,14,26,5,5,outline);
            Fill(p,w,h,16,30,2,3,gold); Fill(p,w,h,12,34,9,3,outline);
            Fill(p,w,h,15,37,3,1,wood); Fill(p,w,h,2,18,4,2,gold);
            Fill(p,w,h,26,19,4,2,gold);
        }

        private static void DrawAshfallSignalFlagTestPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 29, 40, 255);
            var timber = new Color32(110, 72, 48, 255);
            var cloth = new Color32(227, 211, 170, 255);
            var darkCloth = new Color32(69, 77, 82, 255);
            var brass = new Color32(212, 164, 70, 255);
            Fill(p,w,h,5,4,6,31,outline); Fill(p,w,h,7,6,2,27,timber);
            Fill(p,w,h,10,6,27,4,outline); Fill(p,w,h,12,8,22,2,brass);
            Fill(p,w,h,11,10,21,18,outline); Fill(p,w,h,13,12,17,14,cloth);
            Fill(p,w,h,30,12,3,14,darkCloth); Fill(p,w,h,26,12,3,14,darkCloth);
            Fill(p,w,h,22,14,3,10,darkCloth); Fill(p,w,h,13,25,7,2,brass);
            Fill(p,w,h,2,35,17,3,outline); Fill(p,w,h,4,36,13,1,timber);
        }

        private static void DrawAshfallRemedyShelfPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 37, 255);
            var wood = new Color32(117, 73, 48, 255);
            var lightWood = new Color32(177, 119, 65, 255);
            var glass = new Color32(130, 187, 178, 255);
            var cork = new Color32(191, 151, 88, 255);
            var tonic = new Color32(191, 126, 63, 255);
            var card = new Color32(227, 207, 157, 255);
            Fill(p, w, h, 2, 5, 32, 23, outline); Fill(p, w, h, 4, 7, 28, 19, wood);
            Fill(p, w, h, 6, 10, 24, 3, lightWood); Fill(p, w, h, 6, 21, 24, 3, lightWood);
            Fill(p, w, h, 11, 3, 9, 3, outline); Fill(p, w, h, 12, 4, 7, 2, cork);
            Fill(p, w, h, 10, 7, 11, 12, outline); Fill(p, w, h, 12, 9, 7, 9, glass);
            Fill(p, w, h, 13, 13, 5, 4, tonic); Fill(p, w, h, 23, 13, 6, 3, card);
        }

        private static void DrawTravelBeaconPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var bronze = new Color32(127, 81, 48, 255);
            var gold = new Color32(240, 178, 77, 255);
            var glow = new Color32(255, 221, 133, 255);
            Fill(p, w, h, 9, 2, 14, 4, outline); Fill(p, w, h, 11, 6, 10, 4, bronze);
            Fill(p, w, h, 13, 10, 6, 13, outline); Fill(p, w, h, 14, 11, 4, 10, gold);
            Fill(p, w, h, 15, 12, 2, 6, glow); Fill(p, w, h, 7, 23, 18, 5, outline);
            Fill(p, w, h, 9, 24, 14, 3, bronze); Fill(p, w, h, 5, 29, 22, 4, outline);
            Fill(p, w, h, 7, 30, 18, 2, gold);
        }

        private static void DrawRosterStonePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var stone = new Color32(91, 98, 105, 255);
            var lightStone = new Color32(132, 137, 137, 255);
            var inscription = new Color32(208, 167, 89, 255);
            Fill(p, w, h, 3, 4, 26, 35, outline); Fill(p, w, h, 5, 6, 22, 31, stone);
            Fill(p, w, h, 8, 9, 16, 3, lightStone);
            Fill(p, w, h, 9, 16, 14, 2, inscription); Fill(p, w, h, 9, 22, 12, 2, inscription);
            Fill(p, w, h, 11, 28, 10, 2, new Color32(95, 82, 67, 255));
            Fill(p, w, h, 2, 38, 28, 4, outline); Fill(p, w, h, 4, 39, 24, 2, lightStone);
        }

        private static void DrawNiaPorterPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 29, 39, 255);
            var hair = new Color32(59, 41, 39, 255);
            var skin = new Color32(218, 163, 128, 255);
            var coat = new Color32(60, 83, 112, 255);
            var coatLight = new Color32(103, 132, 151, 255);
            var leather = new Color32(136, 91, 53, 255);
            var brass = new Color32(218, 176, 80, 255);
            Fill(p,w,h,8,2,17,5,outline); Fill(p,w,h,9,3,15,3,hair);
            Fill(p,w,h,7,7,19,15,outline); Fill(p,w,h,9,9,15,11,skin);
            Fill(p,w,h,7,8,4,15,hair); Fill(p,w,h,22,8,4,12,hair);
            Fill(p,w,h,11,14,2,2,outline); Fill(p,w,h,20,14,2,2,outline);
            Fill(p,w,h,6,22,21,17,outline); Fill(p,w,h,8,24,17,14,coat);
            Fill(p,w,h,15,24,4,14,coatLight); Fill(p,w,h,7,25,19,3,leather);
            Fill(p,w,h,20,26,5,11,leather); Fill(p,w,h,21,29,3,3,brass);
            Fill(p,w,h,8,38,7,4,outline); Fill(p,w,h,19,38,7,4,outline);
            Fill(p,w,h,15,27,2,2,brass); Fill(p,w,h,15,32,2,2,brass);
        }

        private static void DrawAdaSloanePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 29, 37, 255);
            var hair = new Color32(163, 157, 143, 255);
            var skin = new Color32(222, 169, 132, 255);
            var coat = new Color32(67, 84, 67, 255);
            var vest = new Color32(144, 73, 53, 255);
            var leather = new Color32(105, 73, 53, 255);
            var brass = new Color32(220, 175, 77, 255);
            var paper = new Color32(225, 208, 169, 255);
            Fill(p, w, h, 8, 2, 16, 6, outline); Fill(p, w, h, 9, 3, 14, 4, hair);
            Fill(p, w, h, 7, 8, 19, 15, outline); Fill(p, w, h, 9, 10, 15, 11, skin);
            Fill(p, w, h, 7, 8, 4, 13, hair); Fill(p, w, h, 22, 8, 4, 13, hair);
            Fill(p, w, h, 12, 14, 2, 2, outline); Fill(p, w, h, 20, 14, 2, 2, outline);
            Fill(p, w, h, 6, 22, 21, 18, outline); Fill(p, w, h, 8, 24, 17, 14, coat);
            Fill(p, w, h, 13, 24, 7, 14, vest); Fill(p, w, h, 7, 26, 19, 3, leather);
            Fill(p, w, h, 19, 29, 7, 9, leather); Fill(p, w, h, 20, 30, 5, 6, paper);
            Fill(p, w, h, 12, 28, 2, 2, brass); Fill(p, w, h, 15, 32, 2, 8, brass);
            Fill(p, w, h, 8, 39, 7, 4, outline); Fill(p, w, h, 19, 39, 7, 4, outline);
        }

        private static void DrawDawnkeepCotsPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 27, 37, 255);
            var wood = new Color32(107, 72, 49, 255);
            var lightWood = new Color32(165, 116, 68, 255);
            var linen = new Color32(190, 185, 163, 255);
            var shadow = new Color32(112, 121, 132, 255);
            Fill(p,w,h,2,8,32,4,outline); Fill(p,w,h,4,9,28,2,lightWood);
            Fill(p,w,h,3,13,4,14,outline); Fill(p,w,h,29,13,4,14,outline);
            Fill(p,w,h,5,13,26,10,outline); Fill(p,w,h,7,14,22,7,linen);
            Fill(p,w,h,7,14,8,5,shadow); Fill(p,w,h,4,25,4,5,wood);
            Fill(p,w,h,28,25,4,5,wood); Fill(p,w,h,2,29,32,3,outline);
            Fill(p,w,h,5,30,26,2,lightWood); Fill(p,w,h,15,5,6,2,outline);
        }

        private static void DrawDawnkeepDocketPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(36, 30, 37, 255);
            var paper = new Color32(218, 190, 134, 255);
            var lightPaper = new Color32(243, 220, 164, 255);
            var ink = new Color32(86, 59, 48, 255);
            var brass = new Color32(190, 133, 58, 255);
            Fill(p,w,h,5,2,25,32,outline); Fill(p,w,h,7,4,21,28,paper);
            Fill(p,w,h,10,7,15,2,lightPaper); Fill(p,w,h,10,13,14,2,ink);
            Fill(p,w,h,10,18,12,2,ink); Fill(p,w,h,10,23,15,2,ink);
            Fill(p,w,h,10,28,9,2,ink); Fill(p,w,h,22,7,4,4,brass);
            Fill(p,w,h,2,31,28,4,outline); Fill(p,w,h,4,32,24,2,brass);
        }

        private static void DrawDawnkeepNoticeBoardPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 28, 38, 255);
            var wood = new Color32(112, 73, 45, 255);
            var lightWood = new Color32(171, 116, 64, 255);
            var paper = new Color32(226, 205, 157, 255);
            var red = new Color32(164, 65, 58, 255);
            var brass = new Color32(230, 187, 82, 255);
            Fill(p,w,h,3,4,30,25,outline); Fill(p,w,h,5,6,26,21,wood);
            Fill(p,w,h,8,9,8,13,paper); Fill(p,w,h,19,8,9,15,paper);
            Fill(p,w,h,9,12,6,2,red); Fill(p,w,h,20,11,6,2,red);
            Fill(p,w,h,9,17,5,2,wood); Fill(p,w,h,20,16,6,2,wood);
            Fill(p,w,h,9,21,6,2,wood); Fill(p,w,h,20,21,5,2,wood);
            Fill(p,w,h,9,8,2,2,brass); Fill(p,w,h,25,8,2,2,brass);
            Fill(p,w,h,12,29,3,7,outline); Fill(p,w,h,21,29,3,7,outline);
            Fill(p,w,h,5,35,22,3,lightWood);
        }

        private static void DrawDawnkeepSealedDossierPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 28, 37, 255);
            var wood = new Color32(91, 65, 53, 255);
            var darkWood = new Color32(59, 49, 48, 255);
            var paper = new Color32(205, 183, 136, 255);
            var wax = new Color32(154, 48, 51, 255);
            var gold = new Color32(225, 180, 83, 255);
            Fill(p,w,h,3,7,30,27,outline); Fill(p,w,h,6,10,24,20,wood);
            Fill(p,w,h,9,13,18,13,darkWood); Fill(p,w,h,11,15,14,9,paper);
            Fill(p,w,h,12,17,12,2,wood); Fill(p,w,h,12,21,10,2,wood);
            Fill(p,w,h,14,23,8,7,outline); Fill(p,w,h,15,24,6,5,wax);
            Fill(p,w,h,17,25,2,3,gold); Fill(p,w,h,6,5,24,3,gold);
            Fill(p,w,h,2,34,32,4,outline); Fill(p,w,h,5,35,26,2,wood);
        }

        private static void DrawAqueductDispatchPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 30, 40, 255);
            var parchment = new Color32(222, 202, 159, 255);
            var ink = new Color32(85, 70, 57, 255);
            var water = new Color32(64, 143, 171, 255);
            var brass = new Color32(195, 142, 61, 255);
            Fill(p,w,h,3,5,30,28,outline); Fill(p,w,h,6,8,24,22,parchment);
            Fill(p,w,h,9,11,7,2,ink); Fill(p,w,h,9,27,15,2,ink);
            Fill(p,w,h,15,12,3,8,water); Fill(p,w,h,13,19,11,3,water);
            Fill(p,w,h,22,14,3,9,water); Fill(p,w,h,17,24,3,5,water);
            Fill(p,w,h,9,16,6,2,ink); Fill(p,w,h,23,24,5,2,ink);
            Fill(p,w,h,15,17,4,4,brass); Fill(p,w,h,2,33,32,4,outline);
            Fill(p,w,h,6,34,24,2,brass);
        }

        private static void DrawDawnkeepInletMarksPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 31, 39, 255);
            var stone = new Color32(116, 125, 128, 255);
            var paleStone = new Color32(171, 177, 160, 255);
            var water = new Color32(59, 139, 167, 255);
            var brass = new Color32(203, 154, 71, 255);
            Fill(p,w,h,5,3,26,33,outline); Fill(p,w,h,8,5,20,28,stone);
            Fill(p,w,h,10,8,8,21,paleStone); Fill(p,w,h,19,8,6,21,water);
            Fill(p,w,h,11,12,8,2,outline); Fill(p,w,h,11,20,8,2,outline);
            Fill(p,w,h,11,27,8,2,outline); Fill(p,w,h,10,12,7,1,brass);
            Fill(p,w,h,10,20,7,1,brass); Fill(p,w,h,10,27,7,1,brass);
            Fill(p,w,h,3,2,28,3,outline); Fill(p,w,h,7,1,20,2,brass);
        }

        private static void DrawDawnkeepLowerFlowPostPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 38, 255);
            var stone = new Color32(130, 136, 132, 255);
            var brass = new Color32(199, 146, 66, 255);
            var water = new Color32(55, 137, 168, 255);
            var light = new Color32(220, 198, 137, 255);
            Fill(p,w,h,8,3,17,34,outline); Fill(p,w,h,11,6,11,29,stone);
            Fill(p,w,h,14,8,7,23,water); Fill(p,w,h,10,13,6,3,outline);
            Fill(p,w,h,10,21,6,3,outline); Fill(p,w,h,10,29,6,3,outline);
            Fill(p,w,h,10,14,5,1,brass); Fill(p,w,h,10,22,5,1,brass);
            Fill(p,w,h,10,30,5,1,brass); Fill(p,w,h,9,2,15,4,outline);
            Fill(p,w,h,11,3,11,2,light); Fill(p,w,h,4,0,25,3,outline);
            Fill(p,w,h,2,0,29,2,brass);
        }

        private static void DrawCadetFlowCharmPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 28, 38, 255);
            var brass = new Color32(190, 133, 58, 255);
            var gold = new Color32(230, 185, 85, 255);
            var light = new Color32(248, 222, 145, 255);
            var water = new Color32(69, 157, 181, 255);
            Fill(p,w,h,12,2,8,3,outline); Fill(p,w,h,8,5,16,3,outline);
            Fill(p,w,h,5,8,22,16,outline); Fill(p,w,h,8,24,16,3,outline);
            Fill(p,w,h,12,27,8,3,outline); Fill(p,w,h,12,5,8,2,gold);
            Fill(p,w,h,8,8,16,16,brass); Fill(p,w,h,10,10,12,12,water);
            Fill(p,w,h,11,11,10,2,light); Fill(p,w,h,11,19,10,2,gold);
            Fill(p,w,h,12,14,8,3,brass); Fill(p,w,h,13,15,6,1,light);
            Fill(p,w,h,3,13,4,6,gold); Fill(p,w,h,25,13,4,6,gold);
        }

        private static void DrawGreenwakeOpenSowingCharmPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var backing = new Color32(50, 66, 52, 255);
            var brass = new Color32(220, 176, 84, 255);
            var brassLight = new Color32(244, 221, 153, 255);
            var leaf = new Color32(110, 181, 89, 255);
            var seed = new Color32(191, 137, 69, 255);
            Fill(p, w, h, 3, 4, 26, 25, outline);
            Fill(p, w, h, 5, 6, 22, 21, backing);

            for (var y = 4; y <= 15; y++)
            for (var x = 8; x <= 23; x++)
            {
                var dx = x - 16;
                var dy = y - 9;
                var distance = dx * dx + dy * dy;
                if (distance >= 16 && distance <= 32)
                    SetGearIconPixel(p, w, h, x, y, distance < 24 ? brassLight : brass);
            }

            Fill(p, w, h, 15, 16, 3, 8, outline);
            Fill(p, w, h, 16, 17, 1, 6, leaf);
            Fill(p, w, h, 10, 18, 7, 5, outline);
            Fill(p, w, h, 11, 19, 5, 3, seed);
            Fill(p, w, h, 9, 14, 7, 2, outline);
            Fill(p, w, h, 10, 14, 5, 1, leaf);
            Fill(p, w, h, 16, 13, 7, 2, outline);
            Fill(p, w, h, 17, 13, 5, 1, leaf);
            Fill(p, w, h, 11, 24, 11, 2, outline);
            Fill(p, w, h, 13, 25, 7, 1, brass);
        }

        private static void DrawCisternLedgerClaspPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 29, 40, 255);
            var brass = new Color32(157, 103, 54, 255);
            var gold = new Color32(224, 177, 91, 255);
            var paper = new Color32(229, 214, 169, 255);
            var blue = new Color32(73, 143, 165, 255);
            Fill(p, w, h, 7, 4, 18, 24, outline); Fill(p, w, h, 9, 6, 14, 20, brass);
            Fill(p, w, h, 11, 8, 10, 16, outline); Fill(p, w, h, 12, 9, 8, 14, paper);
            Fill(p, w, h, 13, 12, 6, 2, blue); Fill(p, w, h, 13, 16, 6, 1, brass);
            Fill(p, w, h, 13, 19, 5, 1, blue); Fill(p, w, h, 4, 13, 4, 6, gold);
            Fill(p, w, h, 24, 13, 4, 6, gold); Fill(p, w, h, 11, 2, 10, 3, outline);
            Fill(p, w, h, 13, 3, 6, 1, gold);
        }

        private static void DrawCinderCupRailPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(32, 28, 38, 255);
            var wood = new Color32(112, 76, 52, 255);
            var clay = new Color32(174, 116, 79, 255);
            var water = new Color32(79, 155, 173, 255);
            var chalk = new Color32(221, 201, 157, 255);
            Fill(p, w, h, 2, 6, 32, 22, outline); Fill(p, w, h, 4, 8, 28, 18, wood);
            Fill(p, w, h, 6, 6, 24, 3, outline); Fill(p, w, h, 7, 7, 22, 1, chalk);
            Fill(p, w, h, 7, 13, 6, 12, outline); Fill(p, w, h, 8, 15, 4, 8, clay);
            Fill(p, w, h, 8, 17, 4, 2, water); Fill(p, w, h, 19, 11, 7, 14, outline);
            Fill(p, w, h, 20, 13, 5, 10, clay); Fill(p, w, h, 20, 17, 5, 2, water);
            Fill(p, w, h, 10, 4, 1, 3, chalk); Fill(p, w, h, 18, 4, 1, 3, chalk);
            Fill(p, w, h, 27, 4, 1, 3, chalk);
        }

        private static void DrawCinderKitchenHearthPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(35, 30, 37, 255);
            var stone = new Color32(105, 101, 92, 255);
            var lightStone = new Color32(157, 148, 126, 255);
            var ember = new Color32(221, 99, 51, 255);
            var flame = new Color32(247, 183, 76, 255);
            Fill(p, w, h, 4, 4, 30, 25, outline); Fill(p, w, h, 6, 6, 26, 20, stone);
            Fill(p, w, h, 8, 9, 22, 14, outline); Fill(p, w, h, 11, 17, 16, 6, ember);
            Fill(p, w, h, 15, 12, 3, 9, flame); Fill(p, w, h, 20, 14, 3, 7, flame);
            Fill(p, w, h, 8, 29, 22, 3, outline); Fill(p, w, h, 10, 30, 18, 1, lightStone);
            Fill(p, w, h, 2, 12, 3, 10, outline); Fill(p, w, h, 33, 12, 3, 10, outline);
        }

        private static void DrawCinderKitchenMillstonePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 30, 38, 255);
            var stone = new Color32(132, 132, 122, 255);
            var stoneLight = new Color32(183, 174, 148, 255);
            var wood = new Color32(111, 75, 49, 255);
            Fill(p, w, h, 3, 25, 30, 5, outline); Fill(p, w, h, 5, 26, 26, 3, wood);
            Fill(p, w, h, 7, 7, 22, 18, outline); Fill(p, w, h, 9, 9, 18, 14, stone);
            Fill(p, w, h, 12, 11, 12, 2, stoneLight); Fill(p, w, h, 16, 5, 4, 6, outline);
            Fill(p, w, h, 17, 3, 2, 5, wood); Fill(p, w, h, 13, 15, 10, 2, outline);
            Fill(p, w, h, 17, 20, 2, 5, wood);
        }

        private static void DrawCinderBrothSamplePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 39, 255);
            var iron = new Color32(80, 94, 102, 255);
            var broth = new Color32(208, 145, 65, 255);
            var steam = new Color32(207, 211, 197, 255);
            Fill(p, w, h, 5, 15, 24, 14, outline); Fill(p, w, h, 7, 17, 20, 9, iron);
            Fill(p, w, h, 9, 19, 16, 5, broth); Fill(p, w, h, 2, 13, 30, 3, outline);
            Fill(p, w, h, 10, 8, 2, 5, steam); Fill(p, w, h, 17, 6, 2, 7, steam);
            Fill(p, w, h, 24, 9, 2, 4, steam); Fill(p, w, h, 8, 30, 18, 2, outline);
        }

        private static void DrawCinderCommonTablePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 29, 38, 255);
            var wood = new Color32(126, 82, 51, 255);
            var lightWood = new Color32(177, 120, 68, 255);
            var clay = new Color32(182, 122, 83, 255);
            var bowl = new Color32(226, 180, 100, 255);
            Fill(p, w, h, 3, 9, 34, 17, outline); Fill(p, w, h, 5, 11, 30, 12, wood);
            Fill(p, w, h, 7, 13, 26, 2, lightWood); Fill(p, w, h, 7, 26, 4, 6, outline);
            Fill(p, w, h, 29, 26, 4, 6, outline); Fill(p, w, h, 10, 5, 8, 5, outline);
            Fill(p, w, h, 11, 6, 6, 3, clay); Fill(p, w, h, 12, 6, 4, 1, bowl);
            Fill(p, w, h, 22, 5, 8, 5, outline); Fill(p, w, h, 23, 6, 6, 3, clay);
            Fill(p, w, h, 24, 6, 4, 1, bowl);
        }

        private static void DrawGlassplumTreePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(34, 31, 41, 255);
            var bark = new Color32(115, 77, 54, 255);
            var leaf = new Color32(91, 139, 81, 255);
            var leafLight = new Color32(142, 174, 91, 255);
            var plum = new Color32(183, 102, 148, 255);
            var plumLight = new Color32(235, 174, 176, 255);
            Fill(p, w, h, 17, 18, 5, 18, outline); Fill(p, w, h, 18, 19, 3, 16, bark);
            Fill(p, w, h, 8, 31, 22, 4, outline); Fill(p, w, h, 10, 32, 18, 2, leaf);
            Fill(p, w, h, 7, 10, 24, 14, outline); Fill(p, w, h, 9, 8, 20, 14, leaf);
            Fill(p, w, h, 4, 13, 12, 8, leaf); Fill(p, w, h, 22, 12, 12, 9, leafLight);
            Fill(p, w, h, 11, 12, 4, 4, plum); Fill(p, w, h, 23, 10, 4, 4, plum);
            Fill(p, w, h, 18, 17, 4, 4, plum); Fill(p, w, h, 28, 18, 4, 4, plum);
            Fill(p, w, h, 12, 13, 1, 1, plumLight); Fill(p, w, h, 24, 11, 1, 1, plumLight);
            Fill(p, w, h, 19, 18, 1, 1, plumLight); Fill(p, w, h, 29, 19, 1, 1, plumLight);
            Fill(p, w, h, 13, 22, 8, 3, outline); Fill(p, w, h, 14, 23, 6, 1, bark);
        }

        private static void DrawCinderSeedScalePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 40, 255);
            var stone = new Color32(119, 105, 82, 255);
            var brass = new Color32(202, 151, 69, 255);
            var light = new Color32(241, 207, 127, 255);
            var blue = new Color32(82, 143, 159, 255);
            Fill(p, w, h, 5, 30, 24, 4, outline); Fill(p, w, h, 15, 4, 4, 26, outline);
            Fill(p, w, h, 16, 6, 2, 22, brass); Fill(p, w, h, 5, 8, 22, 4, outline);
            Fill(p, w, h, 7, 9, 18, 2, brass); Fill(p, w, h, 6, 10, 2, 11, outline);
            Fill(p, w, h, 24, 10, 2, 11, outline); Fill(p, w, h, 3, 19, 8, 3, outline);
            Fill(p, w, h, 19, 19, 8, 3, outline); Fill(p, w, h, 4, 16, 6, 3, stone);
            Fill(p, w, h, 20, 16, 6, 3, blue); Fill(p, w, h, 11, 2, 12, 3, light);
            Fill(p, w, h, 13, 25, 8, 3, stone);
        }

        private static void DrawWardenPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var stone = new Color32(133, 139, 144, 255);
            var lightStone = new Color32(184, 184, 170, 255);
            var darkStone = new Color32(83, 91, 102, 255);
            var brass = new Color32(173, 117, 58, 255);
            var gold = new Color32(244, 198, 102, 255);
            var glow = new Color32(255, 230, 147, 255);
            Fill(p, w, h, 4, 0, 10, 7, outline); Fill(p, w, h, 5, 1, 8, 5, darkStone);
            Fill(p, w, h, 18, 0, 10, 7, outline); Fill(p, w, h, 19, 1, 8, 5, darkStone);
            Fill(p, w, h, 5, 6, 23, 27, outline); Fill(p, w, h, 6, 7, 21, 24, stone);
            Fill(p, w, h, 8, 8, 6, 18, lightStone); Fill(p, w, h, 19, 9, 6, 14, darkStone);
            Fill(p, w, h, 7, 29, 20, 7, outline); Fill(p, w, h, 8, 30, 18, 5, darkStone);
            Fill(p, w, h, 10, 33, 12, 9, outline); Fill(p, w, h, 11, 34, 10, 7, stone);
            Fill(p, w, h, 11, 23, 10, 10, outline); Fill(p, w, h, 12, 24, 8, 8, brass);
            Fill(p, w, h, 14, 26, 4, 4, gold); Fill(p, w, h, 15, 27, 2, 2, glow);
            Fill(p, w, h, 9, 36, 14, 2, darkStone);
            Fill(p, w, h, 25, 4, 3, 3, outline); Fill(p, w, h, 27, 7, 3, 3, brass);
            Fill(p, w, h, 28, 10, 3, 3, outline); Fill(p, w, h, 29, 13, 3, 3, brass);
            Fill(p, w, h, 29, 16, 3, 3, outline); Fill(p, w, h, 30, 19, 2, 3, brass);
            Fill(p, w, h, 11, 17, 3, 2, outline); Fill(p, w, h, 19, 17, 3, 2, outline);
            Fill(p, w, h, 12, 18, 2, 1, glow); Fill(p, w, h, 19, 18, 2, 1, glow);
        }

        private static void DrawFishingSpotPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 31, 43, 255);
            var water = new Color32(55, 113, 133, 255);
            var lightWater = new Color32(111, 169, 173, 255);
            var wood = new Color32(110, 75, 51, 255);
            var lightWood = new Color32(173, 125, 73, 255);
            Fill(p, w, h, 1, 2, 30, 13, outline); Fill(p, w, h, 3, 4, 26, 9, water);
            Fill(p, w, h, 6, 7, 9, 2, lightWater); Fill(p, w, h, 19, 10, 8, 2, lightWater);
            Fill(p, w, h, 4, 15, 24, 6, outline); Fill(p, w, h, 6, 16, 20, 3, wood);
            Fill(p, w, h, 7, 17, 6, 1, lightWood); Fill(p, w, h, 19, 17, 6, 1, lightWood);
            Fill(p, w, h, 8, 20, 2, 6, outline); Fill(p, w, h, 22, 20, 2, 6, outline);
            Fill(p, w, h, 9, 21, 1, 4, wood); Fill(p, w, h, 22, 21, 1, 4, wood);
            Fill(p, w, h, 11, 11, 2, 5, outline); Fill(p, w, h, 13, 9, 2, 2, outline);
            Fill(p, w, h, 15, 8, 2, 2, wood); Fill(p, w, h, 17, 9, 1, 3, lightWood);
            Fill(p, w, h, 17, 12, 2, 2, outline); Fill(p, w, h, 18, 14, 1, 2, lightWood);
        }

        private static void DrawFarmBedPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 42, 255);
            var wood = new Color32(111, 72, 47, 255);
            var lightWood = new Color32(173, 119, 66, 255);
            var soil = new Color32(68, 54, 48, 255);
            Fill(p, w, h, 1, 4, 34, 17, outline); Fill(p, w, h, 3, 6, 30, 12, soil);
            Fill(p, w, h, 4, 7, 28, 3, new Color32(102, 73, 53, 255));
            Fill(p, w, h, 3, 18, 30, 2, wood); Fill(p, w, h, 2, 20, 32, 3, outline);
            Fill(p, w, h, 4, 21, 28, 1, lightWood);
            Fill(p, w, h, 7, 10, 3, 4, new Color32(80, 61, 47, 255));
            Fill(p, w, h, 16, 10, 3, 4, new Color32(80, 61, 47, 255));
            Fill(p, w, h, 25, 10, 3, 4, new Color32(80, 61, 47, 255));
        }

        private static void DrawFarmGrowingPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var leaf = new Color32(77, 138, 91, 255);
            var lightLeaf = new Color32(139, 190, 112, 255);
            var stem = new Color32(98, 122, 75, 255);
            Fill(p, w, h, 3, 0, 26, 13, outline); Fill(p, w, h, 5, 2, 22, 9, new Color32(84, 66, 50, 255));
            Fill(p, w, h, 15, 8, 3, 17, outline); Fill(p, w, h, 16, 9, 1, 16, stem);
            Fill(p, w, h, 7, 16, 11, 8, outline); Fill(p, w, h, 9, 17, 8, 6, leaf);
            Fill(p, w, h, 18, 21, 9, 8, outline); Fill(p, w, h, 19, 22, 7, 6, leaf);
            Fill(p, w, h, 10, 18, 3, 3, lightLeaf); Fill(p, w, h, 21, 23, 3, 3, lightLeaf);
            Fill(p, w, h, 3, 29, 26, 3, outline); Fill(p, w, h, 5, 30, 22, 1, new Color32(115, 79, 49, 255));
        }

        private static void DrawFarmReadyPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var leaf = new Color32(91, 152, 91, 255);
            var lightLeaf = new Color32(160, 199, 112, 255);
            var gold = new Color32(247, 205, 106, 255);
            Fill(p, w, h, 3, 0, 26, 13, outline); Fill(p, w, h, 5, 2, 22, 9, new Color32(84, 66, 50, 255));
            Fill(p, w, h, 15, 8, 3, 17, outline); Fill(p, w, h, 16, 9, 1, 17, leaf);
            Fill(p, w, h, 5, 16, 13, 9, outline); Fill(p, w, h, 7, 17, 10, 7, leaf);
            Fill(p, w, h, 17, 20, 11, 9, outline); Fill(p, w, h, 18, 21, 9, 7, leaf);
            Fill(p, w, h, 9, 18, 3, 3, lightLeaf); Fill(p, w, h, 21, 22, 3, 3, lightLeaf);
            Fill(p, w, h, 12, 26, 8, 8, outline); Fill(p, w, h, 14, 27, 4, 5, gold);
            Fill(p, w, h, 15, 28, 2, 3, new Color32(255, 239, 174, 255));
            Fill(p, w, h, 2, 32, 5, 2, gold); Fill(p, w, h, 25, 31, 5, 2, gold);
        }

        private static void DrawEmberlilyGrowingPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 27, 40, 255);
            var soil = new Color32(84, 66, 50, 255);
            var stem = new Color32(76, 114, 69, 255);
            var leaf = new Color32(78, 147, 87, 255);
            var lightLeaf = new Color32(140, 190, 103, 255);
            var bud = new Color32(192, 75, 74, 255);
            Fill(p, w, h, 3, 0, 26, 13, outline); Fill(p, w, h, 5, 2, 22, 9, soil);
            Fill(p, w, h, 15, 9, 3, 20, outline); Fill(p, w, h, 16, 10, 1, 18, stem);
            Fill(p, w, h, 5, 17, 12, 9, outline); Fill(p, w, h, 7, 18, 9, 7, leaf);
            Fill(p, w, h, 18, 21, 10, 8, outline); Fill(p, w, h, 19, 22, 8, 6, leaf);
            Fill(p, w, h, 9, 19, 3, 3, lightLeaf); Fill(p, w, h, 22, 23, 3, 3, lightLeaf);
            Fill(p, w, h, 13, 5, 7, 7, outline); Fill(p, w, h, 14, 6, 5, 5, bud);
            Fill(p, w, h, 3, 29, 26, 3, outline); Fill(p, w, h, 5, 30, 22, 1, soil);
        }

        private static void DrawEmberlilyReadyPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var stem = new Color32(70, 113, 69, 255);
            var leaf = new Color32(72, 139, 80, 255);
            var lightLeaf = new Color32(131, 182, 98, 255);
            var petal = new Color32(190, 72, 75, 255);
            var warmPetal = new Color32(232, 121, 72, 255);
            var gold = new Color32(245, 190, 82, 255);
            Fill(p, w, h, 3, 0, 26, 13, outline); Fill(p, w, h, 5, 2, 22, 9, new Color32(84, 66, 50, 255));
            Fill(p, w, h, 15, 8, 3, 20, outline); Fill(p, w, h, 16, 9, 1, 18, stem);
            Fill(p, w, h, 3, 18, 14, 8, outline); Fill(p, w, h, 5, 19, 11, 6, leaf);
            Fill(p, w, h, 18, 22, 11, 7, outline); Fill(p, w, h, 19, 23, 9, 5, leaf);
            Fill(p, w, h, 7, 20, 3, 3, lightLeaf); Fill(p, w, h, 22, 24, 3, 2, lightLeaf);
            Fill(p, w, h, 10, 1, 13, 13, outline); Fill(p, w, h, 12, 0, 9, 3, petal);
            Fill(p, w, h, 8, 3, 5, 7, petal); Fill(p, w, h, 20, 3, 5, 7, warmPetal);
            Fill(p, w, h, 11, 4, 4, 8, warmPetal); Fill(p, w, h, 17, 4, 4, 8, petal);
            Fill(p, w, h, 14, 5, 5, 5, gold); Fill(p, w, h, 15, 6, 3, 3, new Color32(255, 227, 133, 255));
            Fill(p, w, h, 2, 32, 5, 2, gold); Fill(p, w, h, 25, 31, 5, 2, gold);
        }

        private static void DrawMiraClinicPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 27, 41, 255);
            var timber = new Color32(121, 78, 54, 255);
            var lightTimber = new Color32(182, 129, 77, 255);
            var plaster = new Color32(216, 198, 157, 255);
            var roof = new Color32(88, 72, 77, 255);
            var leafRed = new Color32(181, 72, 75, 255);
            Fill(p, w, h, 4, 12, 34, 23, outline); Fill(p, w, h, 6, 14, 30, 19, plaster);
            Fill(p, w, h, 2, 10, 38, 7, outline); Fill(p, w, h, 5, 11, 32, 4, roof);
            Fill(p, w, h, 8, 18, 8, 9, outline); Fill(p, w, h, 10, 20, 4, 5, new Color32(113, 155, 171, 255));
            Fill(p, w, h, 24, 18, 9, 15, outline); Fill(p, w, h, 26, 20, 5, 13, timber);
            Fill(p, w, h, 14, 22, 7, 2, leafRed); Fill(p, w, h, 16, 19, 3, 8, leafRed);
            Fill(p, w, h, 12, 34, 18, 3, outline); Fill(p, w, h, 14, 35, 14, 1, lightTimber);
        }

        private static void DrawMiraFieldSatchelPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 27, 41, 255);
            var leather = new Color32(137, 87, 52, 255);
            var lightLeather = new Color32(190, 133, 71, 255);
            var strap = new Color32(79, 55, 48, 255);
            var leafRed = new Color32(188, 74, 76, 255);
            Fill(p, w, h, 5, 8, 24, 21, outline); Fill(p, w, h, 7, 10, 20, 17, leather);
            Fill(p, w, h, 10, 3, 14, 8, outline); Fill(p, w, h, 12, 5, 10, 6, strap);
            Fill(p, w, h, 11, 9, 2, 19, strap); Fill(p, w, h, 21, 9, 2, 19, strap);
            Fill(p, w, h, 9, 15, 16, 3, outline); Fill(p, w, h, 11, 16, 12, 1, lightLeather);
            Fill(p, w, h, 14, 19, 6, 2, leafRed); Fill(p, w, h, 16, 17, 2, 6, leafRed);
            Fill(p, w, h, 2, 29, 30, 3, outline); Fill(p, w, h, 5, 30, 24, 1, lightLeather);
        }

        private static void DrawAlchemyTablePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var wood = new Color32(105, 70, 51, 255);
            var lightWood = new Color32(173, 119, 66, 255);
            var glass = new Color32(111, 166, 160, 255);
            var tonic = new Color32(181, 93, 97, 255);
            Fill(p, w, h, 2, 13, 32, 7, outline); Fill(p, w, h, 4, 14, 28, 4, wood);
            Fill(p, w, h, 6, 21, 4, 10, outline); Fill(p, w, h, 7, 22, 2, 8, lightWood);
            Fill(p, w, h, 26, 21, 4, 10, outline); Fill(p, w, h, 27, 22, 2, 8, lightWood);
            Fill(p, w, h, 8, 2, 11, 11, outline); Fill(p, w, h, 9, 4, 9, 7, glass);
            Fill(p, w, h, 11, 1, 5, 3, outline); Fill(p, w, h, 11, 7, 5, 3, tonic);
            Fill(p, w, h, 22, 5, 8, 8, outline); Fill(p, w, h, 23, 7, 6, 5, new Color32(190, 147, 75, 255));
            Fill(p, w, h, 24, 3, 4, 3, outline); Fill(p, w, h, 25, 1, 2, 3, lightWood);
            Fill(p, w, h, 5, 15, 7, 2, lightWood);
        }

        private static void DrawTomasReedPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var skin = new Color32(188, 127, 92, 255);
            var hair = new Color32(102, 65, 48, 255);
            var apron = new Color32(85, 104, 104, 255);
            var leather = new Color32(128, 80, 50, 255);
            var steel = new Color32(189, 192, 177, 255);
            Fill(p, w, h, 11, 2, 14, 4, outline); Fill(p, w, h, 12, 3, 12, 2, hair);
            Fill(p, w, h, 10, 6, 16, 15, outline); Fill(p, w, h, 12, 7, 12, 11, skin);
            Fill(p, w, h, 12, 8, 12, 4, hair); Fill(p, w, h, 14, 13, 2, 1, outline);
            Fill(p, w, h, 21, 13, 2, 1, outline); Fill(p, w, h, 9, 20, 18, 19, outline);
            Fill(p, w, h, 11, 22, 14, 14, apron); Fill(p, w, h, 12, 24, 12, 3, leather);
            Fill(p, w, h, 15, 29, 6, 7, new Color32(112, 124, 111, 255));
            Fill(p, w, h, 5, 23, 5, 12, outline); Fill(p, w, h, 26, 22, 4, 13, outline);
            Fill(p, w, h, 4, 13, 3, 19, outline); Fill(p, w, h, 3, 8, 5, 7, steel);
            Fill(p, w, h, 5, 4, 2, 8, outline); Fill(p, w, h, 3, 3, 6, 2, steel);
            Fill(p, w, h, 11, 37, 6, 5, outline); Fill(p, w, h, 20, 37, 6, 5, outline);
        }

        private static void DrawSisterJunePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 43, 255);
            var veil = new Color32(188, 177, 155, 255);
            var robe = new Color32(75, 91, 95, 255);
            var skin = new Color32(211, 157, 121, 255);
            var brass = new Color32(190, 145, 80, 255);
            Fill(p, w, h, 7, 2, 18, 10, outline); Fill(p, w, h, 9, 3, 14, 8, veil);
            Fill(p, w, h, 8, 10, 16, 14, outline); Fill(p, w, h, 10, 11, 12, 11, skin);
            Fill(p, w, h, 8, 17, 16, 6, veil); Fill(p, w, h, 5, 23, 22, 15, outline);
            Fill(p, w, h, 7, 24, 18, 12, robe); Fill(p, w, h, 12, 24, 8, 12, veil);
            Fill(p, w, h, 14, 27, 4, 6, brass); Fill(p, w, h, 15, 28, 2, 4, new Color32(234, 196, 113, 255));
            Fill(p, w, h, 6, 38, 8, 5, outline); Fill(p, w, h, 18, 38, 8, 5, outline);
            Fill(p, w, h, 12, 15, 2, 1, outline); Fill(p, w, h, 18, 15, 2, 1, outline);
        }

        private static void DrawTaliaMercerPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 28, 41, 255);
            var hair = new Color32(117, 70, 48, 255);
            var skin = new Color32(221, 165, 127, 255);
            var shirt = new Color32(89, 120, 117, 255);
            var leather = new Color32(117, 78, 49, 255);
            var brass = new Color32(199, 151, 75, 255);
            Fill(p, w, h, 8, 3, 16, 7, outline); Fill(p, w, h, 10, 4, 12, 5, hair);
            Fill(p, w, h, 9, 9, 15, 13, outline); Fill(p, w, h, 11, 10, 11, 10, skin);
            Fill(p, w, h, 9, 10, 4, 12, hair); Fill(p, w, h, 20, 10, 4, 10, hair);
            Fill(p, w, h, 12, 14, 2, 1, outline); Fill(p, w, h, 19, 14, 2, 1, outline);
            Fill(p, w, h, 5, 22, 22, 16, outline); Fill(p, w, h, 7, 23, 18, 13, shirt);
            Fill(p, w, h, 12, 23, 8, 13, leather); Fill(p, w, h, 14, 27, 4, 5, brass);
            Fill(p, w, h, 4, 24, 4, 12, outline); Fill(p, w, h, 24, 24, 4, 12, outline);
            Fill(p, w, h, 11, 38, 6, 5, outline); Fill(p, w, h, 20, 38, 6, 5, outline);
            Fill(p, w, h, 26, 7, 2, 20, outline); Fill(p, w, h, 27, 5, 1, 3, brass);
        }

        private static void DrawOrenBellPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var skin = new Color32(186, 139, 106, 255);
            var robe = new Color32(91, 76, 64, 255);
            var cloth = new Color32(158, 137, 104, 255);
            var gray = new Color32(156, 153, 141, 255);
            Fill(p, w, h, 8, 2, 16, 8, outline); Fill(p, w, h, 10, 3, 12, 6, gray);
            Fill(p, w, h, 8, 9, 16, 14, outline); Fill(p, w, h, 10, 10, 12, 11, skin);
            Fill(p, w, h, 10, 10, 3, 5, gray); Fill(p, w, h, 17, 10, 5, 5, gray);
            Fill(p, w, h, 6, 23, 20, 15, outline); Fill(p, w, h, 8, 24, 16, 12, robe);
            Fill(p, w, h, 12, 24, 8, 12, cloth); Fill(p, w, h, 14, 27, 4, 5, new Color32(103, 82, 61, 255));
            Fill(p, w, h, 5, 26, 4, 11, outline); Fill(p, w, h, 23, 26, 4, 11, outline);
            Fill(p, w, h, 9, 38, 7, 5, outline); Fill(p, w, h, 18, 38, 7, 5, outline);
            Fill(p, w, h, 12, 16, 2, 1, outline); Fill(p, w, h, 19, 16, 2, 1, outline);
        }

        private static void DrawCinderLedgerPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(31, 29, 42, 255);
            var leather = new Color32(111, 68, 47, 255);
            var paper = new Color32(217, 195, 145, 255);
            var ink = new Color32(77, 71, 61, 255);
            var brass = new Color32(206, 158, 77, 255);
            Fill(p, w, h, 3, 3, 26, 29, outline); Fill(p, w, h, 5, 5, 22, 25, leather);
            Fill(p, w, h, 9, 6, 17, 22, outline); Fill(p, w, h, 10, 7, 14, 20, paper);
            Fill(p, w, h, 12, 11, 10, 2, ink); Fill(p, w, h, 12, 16, 10, 1, ink);
            Fill(p, w, h, 12, 20, 9, 1, ink); Fill(p, w, h, 12, 24, 7, 1, ink);
            Fill(p, w, h, 4, 14, 4, 7, brass); Fill(p, w, h, 5, 16, 2, 3, new Color32(250, 221, 139, 255));
        }

        private static void DrawCinderSluicePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var stone = new Color32(102, 103, 99, 255);
            var darkStone = new Color32(63, 67, 70, 255);
            var brass = new Color32(176, 125, 63, 255);
            var seal = new Color32(192, 78, 60, 255);
            Fill(p, w, h, 2, 1, 28, 32, outline); Fill(p, w, h, 5, 4, 22, 26, stone);
            Fill(p, w, h, 9, 7, 14, 20, outline); Fill(p, w, h, 11, 9, 10, 16, darkStone);
            Fill(p, w, h, 5, 25, 22, 4, brass); Fill(p, w, h, 8, 11, 16, 2, brass);
            Fill(p, w, h, 9, 16, 14, 2, brass); Fill(p, w, h, 12, 21, 8, 4, seal);
            Fill(p, w, h, 4, 30, 24, 3, outline);
        }

        private static void DrawCinderValvePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var stone = new Color32(92, 94, 89, 255);
            var brass = new Color32(200, 151, 72, 255);
            var water = new Color32(84, 153, 165, 255);
            Fill(p, w, h, 4, 8, 24, 23, outline); Fill(p, w, h, 6, 10, 20, 19, stone);
            Fill(p, w, h, 12, 14, 8, 10, outline); Fill(p, w, h, 14, 16, 4, 6, water);
            Fill(p, w, h, 15, 2, 2, 13, outline); Fill(p, w, h, 7, 3, 18, 3, outline);
            Fill(p, w, h, 8, 4, 16, 1, brass); Fill(p, w, h, 12, 0, 8, 5, brass);
            Fill(p, w, h, 13, 30, 6, 4, brass);
        }

        private static void DrawSaltHoundPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var fur = new Color32(125, 93, 66, 255);
            var pale = new Color32(188, 153, 102, 255);
            var salt = new Color32(210, 198, 170, 255);
            var eye = new Color32(242, 177, 68, 255);
            Fill(p, w, h, 4, 11, 26, 15, outline); Fill(p, w, h, 6, 13, 22, 11, fur);
            Fill(p, w, h, 23, 17, 14, 11, outline); Fill(p, w, h, 26, 19, 10, 7, pale);
            Fill(p, w, h, 32, 23, 8, 4, outline); Fill(p, w, h, 34, 24, 5, 2, fur);
            Fill(p, w, h, 27, 17, 4, 3, outline); Fill(p, w, h, 34, 17, 4, 3, outline);
            Fill(p, w, h, 29, 20, 2, 2, eye); Fill(p, w, h, 35, 20, 2, 2, eye);
            Fill(p, w, h, 7, 23, 4, 8, outline); Fill(p, w, h, 13, 23, 4, 9, outline);
            Fill(p, w, h, 24, 25, 4, 8, outline); Fill(p, w, h, 31, 25, 4, 8, outline);
            Fill(p, w, h, 1, 14, 8, 4, outline); Fill(p, w, h, 0, 11, 7, 4, fur);
            Fill(p, w, h, 8, 14, 8, 2, salt); Fill(p, w, h, 15, 17, 7, 2, salt);
            Fill(p, w, h, 5, 31, 8, 2, salt); Fill(p, w, h, 24, 33, 13, 2, outline);
        }

        private static void DrawRustwingHarrierPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var rust = new Color32(145, 75, 51, 255);
            var wing = new Color32(189, 113, 66, 255);
            var pale = new Color32(222, 173, 107, 255);
            var gold = new Color32(242, 184, 72, 255);
            Fill(p, w, h, 15, 11, 13, 18, outline); Fill(p, w, h, 17, 13, 9, 14, rust);
            Fill(p, w, h, 1, 6, 19, 14, outline); Fill(p, w, h, 3, 8, 16, 10, wing);
            Fill(p, w, h, 21, 6, 18, 14, outline); Fill(p, w, h, 23, 8, 14, 10, wing);
            Fill(p, w, h, 5, 9, 8, 2, pale); Fill(p, w, h, 27, 9, 8, 2, pale);
            Fill(p, w, h, 23, 18, 11, 8, outline); Fill(p, w, h, 25, 20, 7, 4, rust);
            Fill(p, w, h, 32, 20, 7, 3, gold); Fill(p, w, h, 28, 18, 3, 2, gold);
            Fill(p, w, h, 19, 28, 3, 7, outline); Fill(p, w, h, 24, 28, 3, 7, outline);
            Fill(p, w, h, 16, 34, 7, 2, gold); Fill(p, w, h, 23, 34, 7, 2, gold);
            Fill(p, w, h, 18, 16, 2, 2, gold); Fill(p, w, h, 24, 16, 2, 2, gold);
            Fill(p, w, h, 4, 3, 9, 4, outline); Fill(p, w, h, 28, 3, 8, 4, outline);
        }

        private static void DrawSluiceMitePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 31, 42, 255);
            var shell = new Color32(88, 123, 119, 255);
            var teal = new Color32(128, 169, 153, 255);
            var amber = new Color32(228, 171, 74, 255);
            var claw = new Color32(163, 117, 66, 255);
            Fill(p, w, h, 6, 7, 24, 17, outline); Fill(p, w, h, 8, 9, 20, 13, shell);
            Fill(p, w, h, 12, 11, 13, 9, teal); Fill(p, w, h, 16, 4, 2, 7, outline);
            Fill(p, w, h, 22, 3, 2, 8, outline); Fill(p, w, h, 5, 10, 5, 6, amber);
            Fill(p, w, h, 26, 10, 5, 6, amber); Fill(p, w, h, 1, 8, 8, 5, outline);
            Fill(p, w, h, 29, 8, 7, 5, outline); Fill(p, w, h, 0, 6, 7, 3, claw);
            Fill(p, w, h, 31, 6, 5, 3, claw);
            Fill(p, w, h, 5, 22, 4, 4, outline); Fill(p, w, h, 11, 23, 4, 5, outline);
            Fill(p, w, h, 21, 23, 4, 5, outline); Fill(p, w, h, 27, 22, 4, 4, outline);
            Fill(p, w, h, 2, 17, 6, 2, teal); Fill(p, w, h, 28, 17, 6, 2, teal);
        }

        private static void DrawGranarySentinelPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 28, 40, 255);
            var stone = new Color32(124, 117, 98, 255);
            var darkStone = new Color32(73, 75, 70, 255);
            var brass = new Color32(186, 132, 68, 255);
            var grain = new Color32(193, 155, 82, 255);
            Fill(p, w, h, 3, 2, 10, 10, outline); Fill(p, w, h, 5, 4, 6, 7, grain);
            Fill(p, w, h, 16, 1, 10, 12, outline); Fill(p, w, h, 18, 3, 6, 8, stone);
            Fill(p, w, h, 27, 3, 8, 8, outline); Fill(p, w, h, 29, 5, 4, 5, grain);
            Fill(p, w, h, 9, 11, 24, 29, outline); Fill(p, w, h, 11, 13, 20, 25, stone);
            Fill(p, w, h, 15, 14, 12, 8, darkStone); Fill(p, w, h, 18, 16, 3, 2, brass);
            Fill(p, w, h, 24, 16, 3, 2, brass); Fill(p, w, h, 16, 24, 11, 9, outline);
            Fill(p, w, h, 18, 26, 7, 5, brass); Fill(p, w, h, 12, 35, 7, 8, outline);
            Fill(p, w, h, 25, 35, 7, 8, outline); Fill(p, w, h, 4, 18, 7, 17, outline);
            Fill(p, w, h, 2, 23, 4, 12, darkStone); Fill(p, w, h, 34, 17, 4, 18, outline);
            Fill(p, w, h, 32, 22, 5, 12, darkStone);
        }

        private static void DrawMoldCrownedReevePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 29, 40, 255);
            var clay = new Color32(111, 90, 76, 255);
            var paleClay = new Color32(157, 128, 98, 255);
            var mold = new Color32(105, 142, 91, 255);
            var gold = new Color32(219, 168, 74, 255);
            var glow = new Color32(245, 215, 132, 255);
            Fill(p, w, h, 5, 1, 8, 13, outline); Fill(p, w, h, 7, 3, 4, 10, mold);
            Fill(p, w, h, 16, 0, 9, 15, outline); Fill(p, w, h, 18, 2, 5, 12, paleClay);
            Fill(p, w, h, 28, 2, 10, 12, outline); Fill(p, w, h, 30, 4, 6, 8, mold);
            Fill(p, w, h, 8, 12, 29, 34, outline); Fill(p, w, h, 10, 14, 25, 30, clay);
            Fill(p, w, h, 14, 16, 17, 10, paleClay); Fill(p, w, h, 16, 18, 4, 3, glow);
            Fill(p, w, h, 25, 18, 4, 3, glow); Fill(p, w, h, 16, 29, 15, 12, outline);
            Fill(p, w, h, 18, 31, 11, 8, gold); Fill(p, w, h, 20, 33, 7, 4, glow);
            Fill(p, w, h, 12, 41, 8, 7, outline); Fill(p, w, h, 25, 41, 8, 7, outline);
            Fill(p, w, h, 2, 23, 8, 18, outline); Fill(p, w, h, 0, 27, 9, 8, paleClay);
            Fill(p, w, h, 34, 22, 8, 20, outline); Fill(p, w, h, 36, 25, 6, 10, paleClay);
            Fill(p, w, h, 10, 12, 26, 3, mold); Fill(p, w, h, 19, 9, 10, 4, mold);
        }

        private static void DrawCisternWardenPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(22, 29, 40, 255);
            var iron = new Color32(67, 80, 89, 255);
            var steel = new Color32(119, 135, 136, 255);
            var brass = new Color32(190, 143, 67, 255);
            var deepWater = new Color32(25, 105, 121, 255);
            var water = new Color32(57, 178, 177, 255);
            var glow = new Color32(151, 240, 211, 255);
            Fill(p, w, h, 8, 0, 10, 15, outline); Fill(p, w, h, 11, 3, 5, 10, brass);
            Fill(p, w, h, 23, 0, 14, 15, outline); Fill(p, w, h, 26, 3, 8, 10, brass);
            Fill(p, w, h, 13, 7, 21, 14, outline); Fill(p, w, h, 16, 9, 15, 10, steel);
            Fill(p, w, h, 17, 13, 13, 5, deepWater); Fill(p, w, h, 20, 14, 8, 3, water);
            Fill(p, w, h, 22, 14, 4, 2, glow);
            Fill(p, w, h, 9, 19, 30, 24, outline); Fill(p, w, h, 12, 21, 24, 19, iron);
            Fill(p, w, h, 16, 24, 16, 12, outline); Fill(p, w, h, 19, 26, 10, 8, brass);
            Fill(p, w, h, 21, 27, 6, 6, deepWater); Fill(p, w, h, 23, 28, 3, 4, water);
            Fill(p, w, h, 13, 40, 9, 8, outline); Fill(p, w, h, 27, 40, 9, 8, outline);
            Fill(p, w, h, 16, 42, 4, 5, steel); Fill(p, w, h, 29, 42, 4, 5, steel);
            Fill(p, w, h, 3, 23, 10, 7, outline); Fill(p, w, h, 0, 25, 12, 3, steel);
            Fill(p, w, h, 35, 23, 10, 7, outline); Fill(p, w, h, 36, 25, 12, 3, steel);
            Fill(p, w, h, 1, 20, 4, 13, brass); Fill(p, w, h, 43, 20, 4, 13, brass);
        }

        private static void DrawCinderSluiceWheelPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 32, 42, 255);
            var iron = new Color32(75, 91, 98, 255);
            var brass = new Color32(194, 145, 70, 255);
            var bright = new Color32(235, 197, 112, 255);
            var water = new Color32(44, 137, 150, 255);
            Fill(p, w, h, 14, 0, 12, 7, outline); Fill(p, w, h, 17, 2, 6, 4, brass);
            Fill(p, w, h, 14, 33, 12, 7, outline); Fill(p, w, h, 17, 35, 6, 4, brass);
            Fill(p, w, h, 0, 14, 7, 12, outline); Fill(p, w, h, 2, 17, 4, 6, brass);
            Fill(p, w, h, 33, 14, 7, 12, outline); Fill(p, w, h, 35, 17, 4, 6, brass);
            Fill(p, w, h, 6, 6, 7, 7, outline); Fill(p, w, h, 8, 8, 4, 4, iron);
            Fill(p, w, h, 27, 6, 7, 7, outline); Fill(p, w, h, 29, 8, 4, 4, iron);
            Fill(p, w, h, 6, 27, 7, 7, outline); Fill(p, w, h, 8, 29, 4, 4, iron);
            Fill(p, w, h, 27, 27, 7, 7, outline); Fill(p, w, h, 29, 29, 4, 4, iron);
            Fill(p, w, h, 10, 10, 20, 20, outline); Fill(p, w, h, 13, 13, 14, 14, iron);
            Fill(p, w, h, 18, 9, 4, 22, outline); Fill(p, w, h, 19, 11, 2, 18, brass);
            Fill(p, w, h, 9, 18, 22, 4, outline); Fill(p, w, h, 11, 19, 18, 2, bright);
            Fill(p, w, h, 16, 16, 8, 8, outline); Fill(p, w, h, 18, 18, 4, 4, water);
        }

        private static void DrawCinderPressureGaugePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(25, 33, 42, 255);
            var steel = new Color32(94, 118, 121, 255);
            var brass = new Color32(193, 149, 76, 255);
            var face = new Color32(210, 203, 171, 255);
            var ink = new Color32(58, 66, 68, 255);
            var glow = new Color32(89, 188, 177, 255);
            Fill(p, w, h, 15, 0, 7, 5, outline); Fill(p, w, h, 17, 2, 3, 3, brass);
            Fill(p, w, h, 13, 4, 12, 4, outline); Fill(p, w, h, 15, 5, 8, 2, steel);
            Fill(p, w, h, 4, 7, 28, 25, outline); Fill(p, w, h, 7, 9, 22, 21, brass);
            Fill(p, w, h, 9, 11, 18, 17, outline); Fill(p, w, h, 11, 13, 14, 13, face);
            Fill(p, w, h, 16, 14, 2, 3, ink); Fill(p, w, h, 21, 15, 2, 3, ink);
            Fill(p, w, h, 13, 19, 11, 2, ink); Fill(p, w, h, 17, 17, 3, 7, glow);
            Fill(p, w, h, 17, 22, 3, 3, brass);
            Fill(p, w, h, 11, 32, 14, 4, outline); Fill(p, w, h, 13, 34, 10, 2, steel);
        }

        private static void DrawCinderFilterHousingPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(25, 34, 44, 255);
            var iron = new Color32(74, 91, 100, 255);
            var steel = new Color32(137, 158, 154, 255);
            var moss = new Color32(110, 159, 111, 255);
            var glow = new Color32(81, 190, 180, 255);
            Fill(p, w, h, 0, 11, 9, 10, outline); Fill(p, w, h, 2, 14, 8, 4, steel);
            Fill(p, w, h, 29, 11, 9, 10, outline); Fill(p, w, h, 28, 14, 8, 4, steel);
            Fill(p, w, h, 8, 5, 22, 23, outline); Fill(p, w, h, 11, 8, 16, 17, iron);
            Fill(p, w, h, 14, 10, 10, 13, outline); Fill(p, w, h, 16, 12, 6, 9, moss);
            Fill(p, w, h, 17, 13, 4, 7, glow); Fill(p, w, h, 12, 24, 14, 5, steel);
            Fill(p, w, h, 5, 7, 5, 5, outline); Fill(p, w, h, 7, 9, 2, 2, steel);
            Fill(p, w, h, 28, 7, 5, 5, outline); Fill(p, w, h, 30, 9, 2, 2, steel);
            Fill(p, w, h, 14, 29, 10, 3, outline); Fill(p, w, h, 16, 30, 6, 2, steel);
        }

        private static void DrawCinderPressureWightPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(21, 31, 43, 255);
            var iron = new Color32(70, 88, 98, 255);
            var shell = new Color32(115, 143, 145, 255);
            var brass = new Color32(187, 136, 63, 255);
            var deepWater = new Color32(24, 94, 116, 255);
            var brine = new Color32(58, 173, 174, 255);
            var glow = new Color32(158, 245, 214, 255);
            Fill(p, w, h, 7, 6, 10, 19, outline); Fill(p, w, h, 10, 9, 5, 13, brass);
            Fill(p, w, h, 27, 4, 11, 22, outline); Fill(p, w, h, 30, 8, 5, 14, brass);
            Fill(p, w, h, 11, 10, 23, 17, outline); Fill(p, w, h, 14, 13, 17, 12, shell);
            Fill(p, w, h, 17, 18, 13, 5, deepWater); Fill(p, w, h, 20, 19, 8, 3, brine);
            Fill(p, w, h, 22, 19, 4, 2, glow);
            Fill(p, w, h, 8, 24, 29, 18, outline); Fill(p, w, h, 11, 27, 23, 13, iron);
            Fill(p, w, h, 15, 29, 15, 10, outline); Fill(p, w, h, 18, 31, 9, 6, brass);
            Fill(p, w, h, 20, 32, 5, 4, deepWater); Fill(p, w, h, 22, 32, 2, 3, glow);
            Fill(p, w, h, 12, 39, 10, 8, outline); Fill(p, w, h, 25, 39, 10, 8, outline);
            Fill(p, w, h, 15, 41, 5, 5, shell); Fill(p, w, h, 28, 41, 5, 5, shell);
            Fill(p, w, h, 2, 27, 11, 7, outline); Fill(p, w, h, 0, 29, 12, 3, brass);
            Fill(p, w, h, 34, 27, 10, 7, outline); Fill(p, w, h, 35, 29, 9, 3, brass);
            Fill(p, w, h, 3, 24, 4, 14, brass); Fill(p, w, h, 38, 24, 4, 14, brass);
        }

        private static void DrawSaltLockhouseRatchetPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 31, 42, 255); var salt = new Color32(170, 160, 138, 255);
            var rust = new Color32(142, 70, 50, 255); var brass = new Color32(207, 157, 73, 255);
            var eye = new Color32(250, 205, 93, 255);
            Fill(p,w,h,5,9,12,15,outline); Fill(p,w,h,7,11,8,11,salt);
            Fill(p,w,h,20,7,15,16,outline); Fill(p,w,h,23,10,10,11,rust);
            Fill(p,w,h,17,12,8,5,outline); Fill(p,w,h,20,13,4,2,brass);
            Fill(p,w,h,26,13,3,3,eye); Fill(p,w,h,34,9,5,12,outline);
            Fill(p,w,h,8,22,23,8,outline); Fill(p,w,h,11,24,17,5,salt);
            Fill(p,w,h,11,29,5,5,outline); Fill(p,w,h,27,29,5,5,outline);
            Fill(p,w,h,12,32,3,2,rust); Fill(p,w,h,28,32,3,2,rust);
            Fill(p,w,h,2,17,8,3,outline); Fill(p,w,h,0,16,4,5,brass);
        }

        private static void DrawBrineglassLatcherPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 35, 47, 255); var shell = new Color32(65, 111, 129, 255);
            var pale = new Color32(143, 189, 191, 255); var brine = new Color32(52, 172, 177, 255);
            Fill(p,w,h,4,10,30,16,outline); Fill(p,w,h,8,12,22,11,shell);
            Fill(p,w,h,12,14,14,6,pale); Fill(p,w,h,17,16,8,4,brine);
            Fill(p,w,h,4,8,6,13,outline); Fill(p,w,h,1,5,7,7,pale);
            Fill(p,w,h,28,8,6,13,outline); Fill(p,w,h,30,5,7,7,pale);
            Fill(p,w,h,8,24,4,7,outline); Fill(p,w,h,24,24,4,7,outline);
            Fill(p,w,h,1,26,8,3,outline); Fill(p,w,h,29,26,8,3,outline);
            Fill(p,w,h,14,23,3,4,new Color32(240,205,123,255));
        }

        private static void DrawSaltSlagInspectorPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 29, 39, 255); var slag = new Color32(92, 100, 104, 255);
            var salt = new Color32(179, 174, 151, 255); var red = new Color32(153, 59, 47, 255);
            var brass = new Color32(207, 161, 80, 255);
            Fill(p,w,h,8,3,27,14,outline); Fill(p,w,h,11,6,21,9,slag);
            Fill(p,w,h,14,10,14,4,red); Fill(p,w,h,10,18,25,24,outline);
            Fill(p,w,h,13,21,19,18,salt); Fill(p,w,h,16,23,13,12,slag);
            Fill(p,w,h,19,25,7,7,brass); Fill(p,w,h,9,40,10,7,outline);
            Fill(p,w,h,28,40,10,7,outline); Fill(p,w,h,1,22,10,11,outline);
            Fill(p,w,h,3,25,7,5,red); Fill(p,w,h,35,21,8,13,outline);
            Fill(p,w,h,37,24,5,7,brass); Fill(p,w,h,15,14,3,2,outline);
            Fill(p,w,h,28,14,3,2,outline);
        }

        private static void DrawRoadglassSentinelPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 34, 42, 255); var salt = new Color32(194, 190, 169, 255);
            var shadow = new Color32(91, 103, 109, 255); var glass = new Color32(104, 194, 197, 255);
            var bright = new Color32(204, 248, 225, 255); var rust = new Color32(154, 77, 53, 255);
            var brass = new Color32(220, 166, 77, 255);
            Fill(p,w,h,13,2,7,12,outline); Fill(p,w,h,16,0,6,13,glass);
            Fill(p,w,h,25,3,8,12,outline); Fill(p,w,h,28,1,5,13,salt);
            Fill(p,w,h,10,10,27,18,outline); Fill(p,w,h,13,13,21,13,salt);
            Fill(p,w,h,16,16,15,7,shadow); Fill(p,w,h,18,18,11,3,glass);
            Fill(p,w,h,20,18,7,2,bright); Fill(p,w,h,8,13,6,14,outline);
            Fill(p,w,h,4,16,8,8,rust); Fill(p,w,h,34,13,7,15,outline);
            Fill(p,w,h,35,16,9,5,brass); Fill(p,w,h,11,27,25,16,outline);
            Fill(p,w,h,14,30,19,11,shadow); Fill(p,w,h,19,31,10,9,salt);
            Fill(p,w,h,12,40,9,10,outline); Fill(p,w,h,15,43,5,7,rust);
            Fill(p,w,h,28,40,10,10,outline); Fill(p,w,h,31,43,5,7,rust);
            Fill(p,w,h,17,34,3,3,brass); Fill(p,w,h,28,34,3,3,brass);
            Fill(p,w,h,6,25,8,4,brass); Fill(p,w,h,36,25,8,4,glass);
        }

        private static void DrawSaltLockhouseBailiffPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(21, 27, 39, 255); var iron = new Color32(63, 77, 88, 255);
            var steel = new Color32(123, 137, 139, 255); var salt = new Color32(191, 177, 145, 255);
            var rust = new Color32(144, 66, 47, 255); var amber = new Color32(236, 168, 57, 255);
            Fill(p,w,h,8,2,12,15,outline); Fill(p,w,h,11,5,7,10,steel);
            Fill(p,w,h,28,2,12,15,outline); Fill(p,w,h,31,5,7,10,rust);
            Fill(p,w,h,15,8,21,16,outline); Fill(p,w,h,18,11,15,10,iron);
            Fill(p,w,h,21,15,4,3,amber); Fill(p,w,h,28,15,4,3,amber);
            Fill(p,w,h,13,23,25,25,outline); Fill(p,w,h,16,26,19,18,salt);
            Fill(p,w,h,18,29,15,12,iron); Fill(p,w,h,21,32,9,6,rust);
            Fill(p,w,h,15,47,10,7,outline); Fill(p,w,h,29,47,10,7,outline);
            Fill(p,w,h,0,26,15,5,outline); Fill(p,w,h,0,24,6,9,steel);
            Fill(p,w,h,37,27,11,4,outline); Fill(p,w,h,42,26,7,6,steel);
            Fill(p,w,h,45,31,3,14,outline); Fill(p,w,h,43,43,7,5,amber);
            Fill(p,w,h,19,5,12,4,outline); Fill(p,w,h,22,2,6,7,amber);
        }

        private static void DrawRuthCalderPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255); var skin = new Color32(194, 139, 103, 255);
            var coat = new Color32(81, 72, 83, 255); var red = new Color32(165, 70, 59, 255);
            var brass = new Color32(221, 171, 81, 255);
            Fill(p,w,h,9,2,15,4,outline); Fill(p,w,h,11,3,11,2,new Color32(117,78,57,255));
            Fill(p,w,h,8,6,17,17,outline); Fill(p,w,h,10,7,13,13,skin); Fill(p,w,h,10,7,13,4,new Color32(111,71,55,255));
            Fill(p,w,h,7,22,20,18,outline); Fill(p,w,h,9,24,16,13,coat); Fill(p,w,h,9,25,5,12,red);
            Fill(p,w,h,15,25,4,3,brass); Fill(p,w,h,16,26,2,1,new Color32(255,220,131,255));
            Fill(p,w,h,3,23,5,11,outline); Fill(p,w,h,25,23,5,11,outline);
            Fill(p,w,h,9,39,6,4,outline); Fill(p,w,h,20,39,6,4,outline);
            Fill(p,w,h,12,14,2,2,outline); Fill(p,w,h,20,14,2,2,outline);
        }

        private static void DrawNellaPikePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255); var skin = new Color32(206, 151, 119, 255);
            var hood = new Color32(82, 112, 116, 255); var cloak = new Color32(181, 165, 133, 255);
            var blue = new Color32(81, 138, 153, 255);
            Fill(p,w,h,7,2,19,11,outline); Fill(p,w,h,9,3,15,8,hood); Fill(p,w,h,11,7,11,12,skin);
            Fill(p,w,h,8,6,17,5,hood); Fill(p,w,h,7,19,20,21,outline); Fill(p,w,h,9,21,16,17,cloak);
            Fill(p,w,h,13,22,8,16,blue); Fill(p,w,h,5,24,6,12,outline); Fill(p,w,h,24,23,6,13,outline);
            Fill(p,w,h,12,14,2,2,outline); Fill(p,w,h,20,14,2,2,outline);
            Fill(p,w,h,11,39,7,4,outline); Fill(p,w,h,21,39,7,4,outline);
        }

        private static void DrawSilasVanePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 29, 38, 255); var leather = new Color32(91, 76, 59, 255);
            var green = new Color32(89, 111, 76, 255); var skin = new Color32(181, 127, 95, 255);
            var steel = new Color32(179, 177, 157, 255);
            Fill(p,w,h,7,3,18,10,outline); Fill(p,w,h,9,4,14,7,green); Fill(p,w,h,11,7,11,11,skin);
            Fill(p,w,h,7,5,5,10,green); Fill(p,w,h,8,19,18,21,outline); Fill(p,w,h,10,21,14,16,leather);
            Fill(p,w,h,6,21,6,15,outline); Fill(p,w,h,25,20,5,15,outline);
            Fill(p,w,h,4,24,3,12,steel); Fill(p,w,h,27,8,2,23,outline); Fill(p,w,h,25,7,6,2,steel);
            Fill(p,w,h,13,13,2,2,outline); Fill(p,w,h,20,13,2,2,outline);
            Fill(p,w,h,10,39,7,4,outline); Fill(p,w,h,21,39,7,4,outline);
        }

        private static void DrawSaltLedgerPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29,27,40,255); var paper = new Color32(212,190,144,255);
            var ink = new Color32(91,67,54,255); var seal = new Color32(157,61,52,255);
            Fill(p,w,h,3,3,26,29,outline); Fill(p,w,h,5,5,22,25,paper);
            Fill(p,w,h,9,9,14,2,ink); Fill(p,w,h,8,14,16,1,ink); Fill(p,w,h,8,18,12,1,ink);
            Fill(p,w,h,8,22,15,1,ink); Fill(p,w,h,9,26,10,1,ink); Fill(p,w,h,21,20,6,6,seal);
            Fill(p,w,h,23,22,2,2,new Color32(238,187,91,255));
        }

        private static void DrawSaltSealPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29,27,40,255); var parchment = new Color32(181,143,92,255);
            var red = new Color32(152,57,51,255); var brass = new Color32(221,173,84,255);
            Fill(p,w,h,3,8,26,19,outline); Fill(p,w,h,5,10,22,15,parchment);
            Fill(p,w,h,7,13,18,2,new Color32(219,190,139,255)); Fill(p,w,h,7,18,12,2,new Color32(91,68,53,255));
            Fill(p,w,h,13,21,10,9,outline); Fill(p,w,h,15,22,6,7,red); Fill(p,w,h,17,24,2,3,brass);
            Fill(p,w,h,7,5,18,4,outline); Fill(p,w,h,9,6,14,2,brass);
        }

        private static void DrawSaltTokenPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29,27,40,255); var silver = new Color32(157,173,173,255);
            var blue = new Color32(63,114,133,255); var light = new Color32(220,203,145,255);
            Fill(p,w,h,7,3,18,28,outline); Fill(p,w,h,9,5,14,24,silver); Fill(p,w,h,11,7,10,20,blue);
            Fill(p,w,h,14,10,4,3,light); Fill(p,w,h,12,16,8,2,light); Fill(p,w,h,14,21,4,2,light);
            Fill(p,w,h,12,31,8,3,outline); Fill(p,w,h,14,32,4,2,new Color32(111,80,54,255));
        }

        private static void DrawSaltMapPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29,27,40,255); var vellum = new Color32(214,195,151,255);
            var rust = new Color32(152,84,59,255); var blue = new Color32(70,123,137,255);
            Fill(p,w,h,2,5,28,23,outline); Fill(p,w,h,4,7,24,19,vellum);
            Fill(p,w,h,7,10,15,2,rust); Fill(p,w,h,8,14,11,2,new Color32(177,131,77,255));
            Fill(p,w,h,19,16,7,2,blue); Fill(p,w,h,21,12,2,12,blue);
            Fill(p,w,h,15,21,3,3,new Color32(197,60,48,255)); Fill(p,w,h,16,22,1,1,new Color32(255,215,105,255));
            Fill(p,w,h,3,3,4,5,outline); Fill(p,w,h,25,25,4,5,outline);
        }

        private static void DrawGlassbackScuttlerPixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(28,29,39,255); var shell=new Color32(104,154,154,255); var salt=new Color32(207,187,139,255);
            var glow=new Color32(244,209,111,255);
            Fill(p,w,h,8,6,25,20,o); Fill(p,w,h,10,8,21,15,shell); Fill(p,w,h,13,10,14,8,new Color32(152,191,174,255));
            Fill(p,w,h,17,12,7,6,salt); Fill(p,w,h,19,14,3,3,glow);
            Fill(p,w,h,2,5,9,4,o); Fill(p,w,h,0,2,8,4,salt); Fill(p,w,h,2,24,10,5,o); Fill(p,w,h,29,24,9,5,o);
            Fill(p,w,h,9,23,4,7,o); Fill(p,w,h,17,24,4,7,o); Fill(p,w,h,27,23,4,7,o); Fill(p,w,h,34,22,4,7,o);
            Fill(p,w,h,5,8,5,2,glow); Fill(p,w,h,10,9,3,2,o);
        }

        private static void DrawSaltroadScavengerPixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(29,27,40,255); var fur=new Color32(111,82,68,255); var light=new Color32(179,129,83,255);
            var bone=new Color32(220,202,160,255); var eye=new Color32(244,192,83,255);
            Fill(p,w,h,4,9,25,16,o); Fill(p,w,h,6,11,21,12,fur); Fill(p,w,h,22,11,13,12,o);
            Fill(p,w,h,24,13,10,8,light); Fill(p,w,h,31,15,7,5,o); Fill(p,w,h,34,16,4,3,bone);
            Fill(p,w,h,23,6,6,9,o); Fill(p,w,h,25,7,3,7,fur); Fill(p,w,h,29,5,7,10,o); Fill(p,w,h,31,7,4,7,fur);
            Fill(p,w,h,27,15,2,2,eye); Fill(p,w,h,31,14,2,2,o);
            Fill(p,w,h,7,22,4,8,o); Fill(p,w,h,13,23,4,7,o); Fill(p,w,h,25,22,4,8,o); Fill(p,w,h,32,21,4,8,o);
            Fill(p,w,h,4,12,5,5,light); Fill(p,w,h,0,10,7,3,o);
        }

        private static void DrawDuneKitePixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(29,27,40,255); var feather=new Color32(139,99,79,255); var wing=new Color32(201,154,98,255);
            var ivory=new Color32(225,207,164,255); var eye=new Color32(247,197,86,255);
            Fill(p,w,h,1,9,17,10,o); Fill(p,w,h,2,11,15,6,wing); Fill(p,w,h,21,9,18,10,o); Fill(p,w,h,23,11,15,6,feather);
            Fill(p,w,h,12,12,17,14,o); Fill(p,w,h,14,14,13,10,feather); Fill(p,w,h,25,8,11,12,o);
            Fill(p,w,h,27,10,8,8,wing); Fill(p,w,h,33,14,6,3,ivory); Fill(p,w,h,29,12,2,2,eye);
            Fill(p,w,h,15,22,3,8,o); Fill(p,w,h,22,22,3,8,o); Fill(p,w,h,14,28,7,3,ivory); Fill(p,w,h,21,28,7,3,ivory);
            Fill(p,w,h,5,15,8,2,feather); Fill(p,w,h,26,15,8,2,wing);
        }

        private static void DrawQuarryHollowPixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(28,30,41,255); var crystal=new Color32(91,143,151,255); var pale=new Color32(193,204,183,255);
            var glow=new Color32(247,213,126,255); var salt=new Color32(205,183,138,255);
            Fill(p,w,h,7,2,22,31,o); Fill(p,w,h,9,5,18,25,crystal); Fill(p,w,h,13,8,10,18,pale);
            Fill(p,w,h,15,12,7,11,o); Fill(p,w,h,17,14,3,7,glow); Fill(p,w,h,5,12,5,7,o);
            Fill(p,w,h,26,9,6,10,o); Fill(p,w,h,28,11,3,6,salt); Fill(p,w,h,3,28,30,5,o);
            Fill(p,w,h,0,18,8,3,crystal); Fill(p,w,h,29,20,7,3,crystal);
        }

        private static void DrawRedpassEnforcerPixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(27,28,40,255); var steel=new Color32(115,124,128,255); var red=new Color32(150,59,51,255);
            var brass=new Color32(221,169,74,255); var dark=new Color32(66,69,79,255);
            Fill(p,w,h,9,2,22,13,o); Fill(p,w,h,11,4,18,9,steel); Fill(p,w,h,14,8,12,5,dark);
            Fill(p,w,h,6,15,29,24,o); Fill(p,w,h,8,17,25,19,steel); Fill(p,w,h,13,18,15,18,red);
            Fill(p,w,h,16,22,10,9,o); Fill(p,w,h,18,24,6,5,brass);
            Fill(p,w,h,1,17,9,20,o); Fill(p,w,h,2,19,7,15,dark); Fill(p,w,h,31,16,8,21,o); Fill(p,w,h,33,18,5,16,dark);
            Fill(p,w,h,4,38,10,7,o); Fill(p,w,h,26,38,10,7,o); Fill(p,w,h,13,11,4,2,brass); Fill(p,w,h,23,11,4,2,brass);
        }

        private static void DrawHollowTollkeeperPixelArt(Color32[] p, int w, int h)
        {
            var o=new Color32(25,27,39,255); var basalt=new Color32(85,94,105,255); var light=new Color32(143,149,143,255);
            var brass=new Color32(184,126,57,255); var glow=new Color32(248,207,105,255); var salt=new Color32(213,198,157,255);
            Fill(p,w,h,5,2,11,10,o); Fill(p,w,h,8,4,7,7,basalt); Fill(p,w,h,30,2,11,10,o); Fill(p,w,h,32,4,7,7,basalt);
            Fill(p,w,h,8,10,32,32,o); Fill(p,w,h,10,12,28,27,basalt); Fill(p,w,h,14,15,20,7,light);
            Fill(p,w,h,17,24,14,12,o); Fill(p,w,h,19,26,10,8,brass); Fill(p,w,h,22,28,4,4,glow);
            Fill(p,w,h,18,17,4,3,glow); Fill(p,w,h,29,17,4,3,glow); Fill(p,w,h,4,20,7,21,o); Fill(p,w,h,1,25,8,13,light);
            Fill(p,w,h,37,19,8,22,o); Fill(p,w,h,39,24,8,14,light); Fill(p,w,h,15,40,9,8,o); Fill(p,w,h,30,40,9,8,o);
            Fill(p,w,h,21,2,7,11,o); Fill(p,w,h,23,4,3,7,salt); Fill(p,w,h,15,12,3,12,salt); Fill(p,w,h,33,12,3,12,salt);
        }

        private static void DrawWargPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            var fur = new Color32(76, 58, 62, 255);
            var ember = new Color32(142, 74, 56, 255);
            var bright = new Color32(198, 111, 63, 255);
            var gold = new Color32(241, 186, 83, 255);
            var claw = new Color32(206, 202, 185, 255);
            Fill(p, w, h, 4, 7, 26, 17, outline); Fill(p, w, h, 5, 9, 22, 13, fur);
            Fill(p, w, h, 7, 14, 15, 7, ember); Fill(p, w, h, 9, 16, 10, 4, bright);
            Fill(p, w, h, 20, 17, 11, 10, outline); Fill(p, w, h, 22, 19, 8, 7, fur);
            Fill(p, w, h, 28, 17, 7, 5, outline); Fill(p, w, h, 30, 18, 5, 3, skinTone());
            Fill(p, w, h, 22, 24, 3, 6, outline); Fill(p, w, h, 27, 24, 3, 5, outline);
            Fill(p, w, h, 23, 26, 1, 3, fur); Fill(p, w, h, 28, 25, 1, 3, fur);
            Fill(p, w, h, 7, 8, 4, 9, outline); Fill(p, w, h, 13, 8, 4, 9, outline);
            Fill(p, w, h, 8, 0, 3, 9, fur); Fill(p, w, h, 14, 0, 3, 9, fur);
            Fill(p, w, h, 7, 0, 4, 2, claw); Fill(p, w, h, 13, 0, 4, 2, claw);
            Fill(p, w, h, 23, 21, 2, 2, gold); Fill(p, w, h, 29, 19, 1, 1, outline);
            Fill(p, w, h, 11, 21, 2, 5, gold); Fill(p, w, h, 12, 22, 1, 4, outline);
            Fill(p, w, h, 1, 13, 6, 3, outline); Fill(p, w, h, 0, 11, 4, 3, fur);
        }

        private static Color32 skinTone() => new Color32(181, 123, 92, 255);

        private static void DrawRowanPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(29, 27, 40, 255);
            Fill(p, w, h, 6, 0, 12, 8, outline); Fill(p, w, h, 7, 1, 10, 6, new Color32(61, 47, 45, 255));
            Fill(p, w, h, 5, 8, 14, 17, outline); Fill(p, w, h, 6, 9, 12, 15, new Color32(54, 81, 137, 255));
            Fill(p, w, h, 8, 11, 8, 9, new Color32(55, 54, 59, 255));
            Fill(p, w, h, 8, 25, 8, 8, outline); Fill(p, w, h, 9, 26, 6, 6, new Color32(229, 175, 135, 255));
            Fill(p, w, h, 7, 31, 10, 4, new Color32(80, 57, 46, 255));
            Fill(p, w, h, 7, 1, 5, 7, new Color32(65, 55, 49, 255)); Fill(p, w, h, 13, 1, 5, 7, new Color32(65, 55, 49, 255));
            Fill(p, w, h, 18, 8, 3, 24, new Color32(111, 88, 64, 255));
        }

        private static void DrawFirstWardenPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var cloak = new Color32(55, 73, 78, 255);
            var pale = new Color32(175, 188, 170, 255); var brass = new Color32(171, 126, 63, 255);
            var skin = new Color32(207, 161, 127, 255); var glow = new Color32(111, 209, 197, 255);
            Fill(p,w,h,8,1,16,7,o); Fill(p,w,h,10,2,12,5,pale); Fill(p,w,h,8,8,17,14,o);
            Fill(p,w,h,10,9,13,11,skin); Fill(p,w,h,10,8,13,4,pale); Fill(p,w,h,11,14,3,1,o); Fill(p,w,h,19,14,3,1,o);
            Fill(p,w,h,5,21,23,20,o); Fill(p,w,h,7,23,19,16,cloak); Fill(p,w,h,14,23,7,15,brass);
            Fill(p,w,h,15,26,5,4,glow); Fill(p,w,h,8,39,7,4,o); Fill(p,w,h,19,39,7,4,o);
            Fill(p,w,h,3,26,5,12,o); Fill(p,w,h,25,26,5,12,o);
        }

        private static void DrawLyraMossPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var hair = new Color32(43, 73, 70, 255);
            var skin = new Color32(225, 176, 139, 255); var teal = new Color32(58, 133, 127, 255);
            var pale = new Color32(180, 213, 193, 255); var gold = new Color32(222, 181, 97, 255);
            Fill(p,w,h,8,2,16,7,o); Fill(p,w,h,10,3,12,5,hair); Fill(p,w,h,8,8,16,14,o);
            Fill(p,w,h,10,9,12,11,skin); Fill(p,w,h,8,8,5,14,hair); Fill(p,w,h,19,8,5,14,hair);
            Fill(p,w,h,11,14,2,1,o); Fill(p,w,h,19,14,2,1,o); Fill(p,w,h,6,22,21,18,o);
            Fill(p,w,h,8,24,17,15,teal); Fill(p,w,h,13,24,7,14,pale); Fill(p,w,h,15,27,4,5,gold);
            Fill(p,w,h,8,39,7,4,o); Fill(p,w,h,19,39,7,4,o); Fill(p,w,h,4,25,5,11,o); Fill(p,w,h,25,25,5,11,o);
        }

        private static void DrawChoirDiverPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 31, 43, 255);
            var suit = new Color32(43, 91, 111, 255);
            var deep = new Color32(31, 60, 78, 255);
            var brass = new Color32(191, 137, 69, 255);
            var glass = new Color32(111, 214, 210, 255);
            var rust = new Color32(173, 83, 64, 255);
            var skin = new Color32(218, 167, 130, 255);
            Fill(p,w,h,9,1,14,2,outline); Fill(p,w,h,6,3,20,12,outline);
            Fill(p,w,h,8,4,16,8,brass); Fill(p,w,h,10,6,12,5,deep);
            Fill(p,w,h,12,7,9,3,glass); Fill(p,w,h,19,7,2,3,new Color32(205,245,229,255));
            Fill(p,w,h,8,12,16,3,outline); Fill(p,w,h,13,13,8,2,skin);
            Fill(p,w,h,5,16,23,18,outline); Fill(p,w,h,7,18,19,14,suit);
            Fill(p,w,h,8,20,5,10,deep); Fill(p,w,h,20,20,4,9,deep);
            Fill(p,w,h,12,19,9,11,rust); Fill(p,w,h,12,20,9,3,brass);
            Fill(p,w,h,9,25,14,3,glass); Fill(p,w,h,11,31,10,3,outline);
            Fill(p,w,h,8,34,7,5,outline); Fill(p,w,h,18,34,7,5,outline);
            Fill(p,w,h,6,38,10,3,brass); Fill(p,w,h,17,38,10,3,brass);
            Fill(p,w,h,3,19,4,12,outline); Fill(p,w,h,4,21,3,8,rust);
        }

        private static void DrawWorldWillPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var deep = new Color32(36, 85, 108, 255);
            var teal = new Color32(69, 184, 181, 255); var pale = new Color32(183, 236, 223, 255);
            var gold = new Color32(214, 176, 98, 255);
            Fill(p,w,h,13,0,12,8,o); Fill(p,w,h,10,5,18,31,o); Fill(p,w,h,12,7,14,27,deep);
            Fill(p,w,h,15,9,8,22,teal); Fill(p,w,h,17,12,4,14,pale); Fill(p,w,h,7,14,7,13,o); Fill(p,w,h,24,14,7,13,o);
            Fill(p,w,h,9,17,6,7,gold); Fill(p,w,h,23,17,6,7,gold); Fill(p,w,h,15,32,8,7,o);
            Fill(p,w,h,17,34,4,4,pale); Fill(p,w,h,11,37,17,4,o); Fill(p,w,h,13,39,13,2,gold);
        }

        private static void DrawChoirRecordPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 28, 40, 255); var stone = new Color32(77, 111, 121, 255);
            var pale = new Color32(161, 196, 182, 255); var glow = new Color32(93, 218, 205, 255);
            Fill(p,w,h,4,2,24,36,o); Fill(p,w,h,7,5,18,30,stone); Fill(p,w,h,9,8,14,3,pale);
            Fill(p,w,h,10,15,12,2,glow); Fill(p,w,h,10,21,9,2,pale); Fill(p,w,h,10,27,12,2,glow);
            Fill(p,w,h,14,33,4,3,o); Fill(p,w,h,1,38,30,4,o);
        }

        private static void DrawChoirBellPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var brass = new Color32(152, 128, 73, 255);
            var light = new Color32(224, 204, 130, 255); var teal = new Color32(83, 187, 174, 255);
            Fill(p,w,h,13,1,8,4,o); Fill(p,w,h,10,5,14,3,brass); Fill(p,w,h,6,8,22,19,o);
            Fill(p,w,h,8,10,18,14,brass); Fill(p,w,h,11,13,12,7,light); Fill(p,w,h,15,16,4,5,teal);
            Fill(p,w,h,3,27,26,4,o); Fill(p,w,h,9,31,14,3,light); Fill(p,w,h,13,34,6,4,o);
        }

        private static void DrawChoirAnchorPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var steel = new Color32(94, 136, 146, 255);
            var glow = new Color32(101, 227, 211, 255); var pale = new Color32(204, 235, 208, 255);
            Fill(p,w,h,13,2,6,5,o); Fill(p,w,h,9,6,14,21,o); Fill(p,w,h,11,8,10,17,steel);
            Fill(p,w,h,14,10,4,13,glow); Fill(p,w,h,6,14,6,5,o); Fill(p,w,h,20,14,6,5,o);
            Fill(p,w,h,3,27,26,4,o); Fill(p,w,h,6,29,20,2,pale); Fill(p,w,h,13,24,6,6,pale);
        }

        private static void DrawEchoLoomPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var wood = new Color32(99, 80, 62, 255);
            var teal = new Color32(66, 155, 147, 255); var pale = new Color32(176, 224, 204, 255);
            Fill(p,w,h,4,5,28,5,o); Fill(p,w,h,6,7,24,2,wood); Fill(p,w,h,7,10,4,15,o); Fill(p,w,h,25,10,4,15,o);
            Fill(p,w,h,11,10,14,14,o); Fill(p,w,h,13,12,10,10,teal); Fill(p,w,h,15,12,2,10,pale); Fill(p,w,h,19,12,2,10,pale);
            Fill(p,w,h,3,25,30,5,o); Fill(p,w,h,6,27,24,2,wood); Fill(p,w,h,14,16,8,3,pale);
        }

        private static void DrawChoirAnvilPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var steel = new Color32(111, 148, 155, 255);
            var light = new Color32(192, 224, 206, 255); var gold = new Color32(213, 176, 96, 255);
            Fill(p,w,h,7,5,22,8,o); Fill(p,w,h,9,7,18,4,steel); Fill(p,w,h,3,13,30,8,o);
            Fill(p,w,h,5,15,26,4,light); Fill(p,w,h,13,21,10,7,o); Fill(p,w,h,15,23,6,5,steel);
            Fill(p,w,h,9,28,18,3,o); Fill(p,w,h,13,10,10,3,gold);
        }

        private static void DrawEchoMothPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var wing = new Color32(64, 134, 143, 255);
            var pale = new Color32(155, 224, 206, 255); var glow = new Color32(231, 212, 126, 255);
            Fill(p,w,h,2,3,15,13,o); Fill(p,w,h,4,5,11,9,wing); Fill(p,w,h,23,3,15,13,o); Fill(p,w,h,25,5,11,9,wing);
            Fill(p,w,h,5,18,11,12,o); Fill(p,w,h,7,20,8,8,pale); Fill(p,w,h,24,18,11,12,o); Fill(p,w,h,26,20,8,8,pale);
            Fill(p,w,h,17,7,6,23,o); Fill(p,w,h,18,9,4,19,glow); Fill(p,w,h,13,14,5,3,o); Fill(p,w,h,22,14,5,3,o);
            Fill(p,w,h,13,2,3,7,o); Fill(p,w,h,24,2,3,7,o); Fill(p,w,h,10,28,8,3,o); Fill(p,w,h,22,28,8,3,o);
        }

        private static void DrawSiltglassEelPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var teal = new Color32(58, 132, 142, 255);
            var glass = new Color32(126, 205, 196, 255); var gold = new Color32(236, 202, 116, 255);
            Fill(p,w,h,2,12,32,12,o); Fill(p,w,h,5,14,27,8,teal); Fill(p,w,h,26,8,14,17,o);
            Fill(p,w,h,28,10,10,13,glass); Fill(p,w,h,32,13,3,3,gold); Fill(p,w,h,10,15,17,2,glass);
            Fill(p,w,h,4,9,7,5,o); Fill(p,w,h,0,7,8,5,teal); Fill(p,w,h,3,21,8,5,o); Fill(p,w,h,0,23,9,5,teal);
            Fill(p,w,h,18,10,7,4,o); Fill(p,w,h,20,6,4,6,glass);
        }

        private static void DrawBellCrabPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var shell = new Color32(104, 119, 105, 255);
            var brass = new Color32(190, 157, 86, 255); var glow = new Color32(91, 220, 202, 255);
            Fill(p,w,h,9,8,22,16,o); Fill(p,w,h,11,10,18,12,shell); Fill(p,w,h,15,12,10,7,brass);
            Fill(p,w,h,18,14,4,4,glow); Fill(p,w,h,3,7,8,5,o); Fill(p,w,h,1,3,8,7,shell);
            Fill(p,w,h,29,7,8,5,o); Fill(p,w,h,31,3,8,7,shell);
            Fill(p,w,h,6,21,5,7,o); Fill(p,w,h,13,22,4,7,o); Fill(p,w,h,23,22,4,7,o); Fill(p,w,h,30,21,5,7,o);
            Fill(p,w,h,11,26,19,3,brass);
        }

        private static void DrawEchoWispPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var deep = new Color32(53, 105, 129, 255);
            var teal = new Color32(89, 209, 194, 255); var pale = new Color32(200, 240, 216, 255);
            Fill(p,w,h,8,5,17,24,o); Fill(p,w,h,10,7,13,20,deep); Fill(p,w,h,13,10,7,14,teal);
            Fill(p,w,h,15,12,3,9,pale); Fill(p,w,h,5,12,6,11,o); Fill(p,w,h,22,12,6,11,o);
            Fill(p,w,h,11,27,11,8,o); Fill(p,w,h,13,29,7,7,deep); Fill(p,w,h,8,35,5,4,teal); Fill(p,w,h,21,35,5,4,teal);
            Fill(p,w,h,10,14,3,2,pale); Fill(p,w,h,20,14,3,2,pale);
        }

        private static void DrawDrownedCantorPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var robe = new Color32(49, 82, 91, 255);
            var armor = new Color32(105, 133, 136, 255); var gold = new Color32(184, 145, 76, 255);
            var glow = new Color32(93, 221, 205, 255);
            Fill(p,w,h,13,1,14,10,o); Fill(p,w,h,16,3,8,6,armor); Fill(p,w,h,7,11,25,29,o);
            Fill(p,w,h,9,13,21,24,robe); Fill(p,w,h,14,15,11,18,armor); Fill(p,w,h,17,20,5,8,glow);
            Fill(p,w,h,10,14,5,3,gold); Fill(p,w,h,25,14,5,3,gold); Fill(p,w,h,5,20,6,18,o); Fill(p,w,h,28,20,6,18,o);
            Fill(p,w,h,10,39,8,7,o); Fill(p,w,h,22,39,8,7,o); Fill(p,w,h,18,2,4,8,gold);
        }

        private static void DrawAegisCantorPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var stone = new Color32(88, 129, 137, 255);
            var plate = new Color32(157, 176, 157, 255); var brass = new Color32(197, 150, 67, 255);
            var glow = new Color32(95, 228, 208, 255);
            Fill(p,w,h,7,1,12,10,o); Fill(p,w,h,29,1,12,10,o); Fill(p,w,h,9,3,8,6,stone); Fill(p,w,h,31,3,8,6,stone);
            Fill(p,w,h,8,10,32,32,o); Fill(p,w,h,11,12,26,27,stone); Fill(p,w,h,15,14,18,8,plate);
            Fill(p,w,h,17,24,14,13,o); Fill(p,w,h,19,26,10,9,brass); Fill(p,w,h,22,28,4,5,glow);
            Fill(p,w,h,5,18,8,22,o); Fill(p,w,h,2,23,10,13,plate); Fill(p,w,h,35,18,8,22,o); Fill(p,w,h,37,23,9,13,plate);
            Fill(p,w,h,15,40,9,8,o); Fill(p,w,h,29,40,9,8,o); Fill(p,w,h,21,2,7,13,o); Fill(p,w,h,23,5,3,8,brass);
            Fill(p,w,h,17,17,4,3,glow); Fill(p,w,h,28,17,4,3,glow);
        }

        private static void DrawEchoKelpGrowingPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var leaf = new Color32(57, 139, 128, 255);
            var light = new Color32(106, 220, 194, 255); var sand = new Color32(126, 106, 78, 255);
            Fill(p,w,h,5,27,22,4,o); Fill(p,w,h,7,29,18,1,sand); Fill(p,w,h,14,9,4,20,o); Fill(p,w,h,15,10,2,19,light);
            Fill(p,w,h,4,15,14,8,o); Fill(p,w,h,6,16,11,6,leaf); Fill(p,w,h,17,19,11,9,o); Fill(p,w,h,18,20,9,7,leaf);
            Fill(p,w,h,5,17,4,3,light); Fill(p,w,h,20,22,4,3,light); Fill(p,w,h,14,6,4,4,light);
        }

        private static void DrawEchoKelpReadyPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 27, 39, 255); var leaf = new Color32(57, 139, 128, 255);
            var light = new Color32(106, 220, 194, 255); var pearl = new Color32(237, 219, 145, 255);
            Fill(p,w,h,4,30,24,4,o); Fill(p,w,h,6,32,20,1,new Color32(126,106,78,255));
            Fill(p,w,h,14,9,4,23,o); Fill(p,w,h,15,10,2,22,light);
            Fill(p,w,h,2,15,15,10,o); Fill(p,w,h,4,17,11,6,leaf); Fill(p,w,h,16,18,14,12,o); Fill(p,w,h,18,20,10,8,leaf);
            Fill(p,w,h,4,18,4,3,light); Fill(p,w,h,21,21,4,3,light); Fill(p,w,h,12,26,8,7,o); Fill(p,w,h,14,27,4,5,pearl);
            Fill(p,w,h,13,28,2,3,light); Fill(p,w,h,2,29,5,2,pearl); Fill(p,w,h,25,27,5,2,pearl);
        }

        private static void DrawMaraBellPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(29, 30, 38, 255); var hair = new Color32(89, 62, 47, 255);
            var skin = new Color32(223, 171, 132, 255); var coat = new Color32(75, 110, 72, 255);
            var light = new Color32(133, 163, 93, 255); var seed = new Color32(225, 191, 88, 255);
            Fill(p,w,h,7,0,18,7,o); Fill(p,w,h,9,2,14,4,hair); Fill(p,w,h,8,7,16,13,o);
            Fill(p,w,h,10,9,12,9,skin); Fill(p,w,h,6,8,5,17,hair); Fill(p,w,h,20,8,6,14,hair);
            Fill(p,w,h,12,13,2,2,o); Fill(p,w,h,19,13,2,2,o); Fill(p,w,h,5,21,22,19,o);
            Fill(p,w,h,7,23,18,15,coat); Fill(p,w,h,11,23,8,15,light); Fill(p,w,h,22,25,7,10,o);
            Fill(p,w,h,24,27,4,6,seed); Fill(p,w,h,9,39,6,4,o); Fill(p,w,h,19,39,6,4,o);
        }

        private static void DrawOwenReedPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(28, 29, 39, 255); var hat = new Color32(109, 78, 50, 255);
            var skin = new Color32(207, 153, 116, 255); var coat = new Color32(57, 91, 111, 255);
            var light = new Color32(116, 157, 169, 255); var rope = new Color32(207, 172, 106, 255);
            Fill(p,w,h,7,4,18,5,o); Fill(p,w,h,9,5,14,3,hat); Fill(p,w,h,10,8,13,5,hat);
            Fill(p,w,h,8,13,17,13,o); Fill(p,w,h,10,15,13,9,skin); Fill(p,w,h,9,15,3,8,hat);
            Fill(p,w,h,20,15,4,8,hat); Fill(p,w,h,6,27,23,15,o); Fill(p,w,h,8,29,19,13,coat);
            Fill(p,w,h,14,29,7,12,light); Fill(p,w,h,11,34,14,3,rope); Fill(p,w,h,9,41,6,3,o); Fill(p,w,h,21,41,6,3,o);
        }

        private static void DrawPellaQuinnPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 31, 38, 255); var silver = new Color32(184, 190, 176, 255);
            var skin = new Color32(223, 170, 132, 255); var coat = new Color32(104, 70, 73, 255);
            var scarf = new Color32(74, 119, 92, 255); var brass = new Color32(218, 177, 85, 255);
            Fill(p,w,h,7,3,19,5,outline); Fill(p,w,h,9,5,15,4,silver); Fill(p,w,h,7,8,19,15,outline);
            Fill(p,w,h,10,10,13,10,skin); Fill(p,w,h,7,9,4,15,silver); Fill(p,w,h,22,10,5,16,silver);
            Fill(p,w,h,12,15,2,2,outline); Fill(p,w,h,19,15,2,2,outline); Fill(p,w,h,5,22,23,19,outline);
            Fill(p,w,h,8,24,17,15,coat); Fill(p,w,h,9,25,15,5,scarf); Fill(p,w,h,17,24,3,14,brass);
            Fill(p,w,h,2,26,5,11,outline); Fill(p,w,h,27,25,4,12,outline);
            Fill(p,w,h,9,40,6,4,outline); Fill(p,w,h,20,40,6,4,outline);
        }

        private static void DrawGreenwakeRootwallJointPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 34, 34, 255); var stone = new Color32(112, 132, 102, 255);
            var light = new Color32(171, 183, 136, 255); var soil = new Color32(98, 73, 52, 255);
            var root = new Color32(121, 151, 78, 255);
            Fill(p,w,h,4,5,40,28,outline); Fill(p,w,h,7,8,34,21,stone); Fill(p,w,h,8,18,32,2,outline);
            Fill(p,w,h,8,9,11,8,light); Fill(p,w,h,23,9,17,8,light); Fill(p,w,h,15,9,8,8,soil);
            Fill(p,w,h,17,10,4,7,root); Fill(p,w,h,19,5,3,8,root); Fill(p,w,h,16,2,3,8,root);
            Fill(p,w,h,1,3,46,3,outline); Fill(p,w,h,3,2,42,2,soil);
            Fill(p,w,h,6,29,7,3,light); Fill(p,w,h,28,29,9,3,light);
        }

        private static void DrawGreenwakeBreathingRootwallPixelArt(Color32[] p, int w, int h)
        {
            DrawGreenwakeRootwallJointPixelArt(p, w, h);
            var outline = new Color32(27, 34, 34, 255); var brass = new Color32(218, 177, 85, 255);
            var mint = new Color32(111, 208, 151, 255);
            Fill(p,w,h,15,7,4,16,outline); Fill(p,w,h,16,8,2,13,mint);
            Fill(p,w,h,12,13,4,3,brass); Fill(p,w,h,18,13,5,3,brass); Fill(p,w,h,16,22,4,3,brass);
        }

        private static void DrawGreenwakeSeasonalRootwallPixelArt(Color32[] p, int w, int h)
        {
            DrawGreenwakeRootwallJointPixelArt(p, w, h);
            var outline = new Color32(27, 34, 34, 255); var brass = new Color32(218, 177, 85, 255);
            var rust = new Color32(190, 112, 70, 255);
            Fill(p,w,h,13,8,9,5,outline); Fill(p,w,h,14,9,7,3,rust); Fill(p,w,h,17,8,3,5,brass);
            Fill(p,w,h,12,15,4,2,brass); Fill(p,w,h,21,15,4,2,brass); Fill(p,w,h,17,25,3,4,rust);
        }

        private static void DrawGreenwakeLedgerPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(27, 35, 35, 255); var stone = new Color32(87, 115, 88, 255);
            var pale = new Color32(181, 193, 138, 255); var gold = new Color32(221, 183, 83, 255);
            Fill(p,w,h,5,3,26,33,o); Fill(p,w,h,8,6,20,26,stone); Fill(p,w,h,11,10,14,3,pale);
            Fill(p,w,h,12,17,12,2,gold); Fill(p,w,h,12,23,10,2,pale); Fill(p,w,h,12,29,13,2,gold);
            Fill(p,w,h,2,35,32,4,o); Fill(p,w,h,8,37,20,2,pale);
        }

        private static void DrawGreenwakeCrownPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(28, 34, 34, 255); var bronze = new Color32(124, 95, 55, 255);
            var gold = new Color32(219, 185, 91, 255); var green = new Color32(98, 159, 100, 255);
            Fill(p,w,h,5,7,26,29,o); Fill(p,w,h,8,10,20,22,bronze); Fill(p,w,h,8,8,20,5,gold);
            Fill(p,w,h,8,4,5,8,gold); Fill(p,w,h,15,2,6,10,gold); Fill(p,w,h,23,4,5,8,gold);
            Fill(p,w,h,13,14,10,12,o); Fill(p,w,h,15,16,6,8,green); Fill(p,w,h,3,36,30,4,o);
        }

        private static void DrawGreenwakeStarChartPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(25, 31, 39, 255); var wood = new Color32(100, 72, 53, 255);
            var paper = new Color32(215, 198, 147, 255); var ink = new Color32(67, 81, 97, 255);
            Fill(p,w,h,3,4,32,23,o); Fill(p,w,h,6,7,26,17,wood); Fill(p,w,h,8,9,22,13,paper);
            Fill(p,w,h,12,12,4,2,ink); Fill(p,w,h,19,15,3,2,ink); Fill(p,w,h,25,11,2,2,ink);
            Fill(p,w,h,14,13,9,1,ink); Fill(p,w,h,20,15,5,1,ink); Fill(p,w,h,16,12,1,4,ink);
            Fill(p,w,h,1,28,36,3,o); Fill(p,w,h,7,31,24,3,wood);
        }

        private static void DrawGreenwakeSignalPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(29, 34, 34, 255); var wood = new Color32(107, 75, 49, 255);
            var gold = new Color32(231, 191, 83, 255); var leaf = new Color32(109, 163, 92, 255);
            Fill(p,w,h,12,6,5,21,o); Fill(p,w,h,14,8,2,18,wood); Fill(p,w,h,4,7,13,8,o);
            Fill(p,w,h,6,9,9,4,gold); Fill(p,w,h,17,11,9,5,o); Fill(p,w,h,19,13,5,2,leaf);
            Fill(p,w,h,6,28,19,3,o); Fill(p,w,h,3,31,25,2,wood);
        }

        private static void DrawGreenwakeRootGraftPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 35, 32, 255);
            var bark = new Color32(91, 75, 48, 255);
            var leaf = new Color32(83, 144, 77, 255);
            var bronze = new Color32(157, 124, 62, 255);
            var pale = new Color32(225, 198, 119, 255);
            Fill(p,w,h,5,4,30,34,outline); Fill(p,w,h,8,7,24,28,bark);
            Fill(p,w,h,16,5,8,31,outline); Fill(p,w,h,19,7,3,26,bronze);
            Fill(p,w,h,2,11,17,7,outline); Fill(p,w,h,4,13,14,3,bark);
            Fill(p,w,h,22,17,16,7,outline); Fill(p,w,h,24,19,13,3,bark);
            Fill(p,w,h,6,26,13,7,outline); Fill(p,w,h,8,28,11,3,leaf);
            Fill(p,w,h,21,29,13,6,outline); Fill(p,w,h,23,31,10,3,leaf);
            Fill(p,w,h,18,15,5,3,pale); Fill(p,w,h,18,23,5,2,pale);
            Fill(p,w,h,4,38,32,4,outline); Fill(p,w,h,9,40,22,2,bark);
        }

        private static void DrawGreenwakeSeedCradlePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 35, 32, 255);
            var wood = new Color32(104, 75, 48, 255);
            var soil = new Color32(83, 77, 48, 255);
            var green = new Color32(100, 166, 83, 255);
            var gold = new Color32(222, 189, 88, 255);
            Fill(p,w,h,4,11,32,21,outline); Fill(p,w,h,7,14,26,15,wood);
            Fill(p,w,h,9,17,22,9,soil); Fill(p,w,h,12,9,16,4,outline);
            Fill(p,w,h,14,6,12,4,wood); Fill(p,w,h,18,4,5,8,green);
            Fill(p,w,h,19,1,3,7,gold); Fill(p,w,h,14,18,4,4,green);
            Fill(p,w,h,21,17,5,5,green); Fill(p,w,h,29,16,3,6,gold);
            Fill(p,w,h,8,32,3,5,outline); Fill(p,w,h,29,32,3,5,outline);
            Fill(p,w,h,3,36,34,2,outline);
        }

        private static void DrawGreenwakeCycleTabletPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(25, 34, 34, 255);
            var stone = new Color32(93, 115, 82, 255);
            var light = new Color32(153, 167, 114, 255);
            var gold = new Color32(218, 180, 82, 255);
            Fill(p,w,h,7,3,26,34,outline); Fill(p,w,h,10,6,20,28,stone);
            Fill(p,w,h,13,9,14,22,light); Fill(p,w,h,17,11,6,18,stone);
            Fill(p,w,h,12,13,4,3,gold); Fill(p,w,h,24,17,4,3,gold);
            Fill(p,w,h,12,24,4,3,gold); Fill(p,w,h,21,28,4,3,gold);
            Fill(p,w,h,4,36,32,4,outline); Fill(p,w,h,9,38,22,2,stone);
            Fill(p,w,h,18,4,4,3,gold);
        }

        private static void DrawGreenwakeStoneRillPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(25, 34, 35, 255);
            var stone = new Color32(96, 115, 85, 255);
            var pale = new Color32(158, 177, 128, 255);
            var water = new Color32(72, 156, 166, 255);
            var glint = new Color32(165, 221, 202, 255);
            var gold = new Color32(218, 180, 82, 255);
            Fill(p,w,h,2,10,38,19,outline); Fill(p,w,h,5,13,32,13,stone);
            Fill(p,w,h,8,17,26,7,outline); Fill(p,w,h,10,19,22,3,water);
            Fill(p,w,h,13,19,5,1,glint); Fill(p,w,h,25,21,4,1,glint);
            Fill(p,w,h,4,7,34,4,outline); Fill(p,w,h,6,8,30,2,pale);
            Fill(p,w,h,10,4,3,8,gold); Fill(p,w,h,10,3,3,2,outline);
            Fill(p,w,h,3,29,36,4,outline); Fill(p,w,h,7,31,28,2,stone);
        }

        private static void DrawBriarStalkerPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(23, 37, 35, 255); var bark = new Color32(93, 79, 53, 255);
            var leaf = new Color32(71, 133, 70, 255); var light = new Color32(150, 188, 85, 255);
            Fill(p,w,h,8,11,24,17,o); Fill(p,w,h,11,13,18,12,bark); Fill(p,w,h,16,16,11,7,leaf);
            Fill(p,w,h,5,7,13,10,o); Fill(p,w,h,7,9,9,6,leaf); Fill(p,w,h,24,6,13,11,o); Fill(p,w,h,26,8,9,7,leaf);
            Fill(p,w,h,12,19,5,4,light); Fill(p,w,h,25,19,5,4,light); Fill(p,w,h,2,25,7,5,o);
            Fill(p,w,h,33,24,7,6,o); Fill(p,w,h,11,27,5,8,o); Fill(p,w,h,25,27,5,8,o);
            Fill(p,w,h,8,33,10,3,o); Fill(p,w,h,24,33,10,3,o);
        }

        private static void DrawLanternMothPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(31, 37, 42, 255); var wing = new Color32(82, 132, 106, 255);
            var pale = new Color32(160, 185, 132, 255); var glow = new Color32(240, 199, 102, 255);
            Fill(p,w,h,1,5,16,12,o); Fill(p,w,h,3,7,12,8,wing); Fill(p,w,h,23,4,16,13,o);
            Fill(p,w,h,25,6,12,9,pale); Fill(p,w,h,15,10,11,19,o); Fill(p,w,h,18,12,5,15,glow);
            Fill(p,w,h,11,15,8,3,o); Fill(p,w,h,21,15,8,3,o); Fill(p,w,h,8,24,10,8,o);
            Fill(p,w,h,23,24,10,8,o); Fill(p,w,h,18,5,2,6,o); Fill(p,w,h,22,5,2,6,o);
        }

        private static void DrawSeedboundSentinelPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(27, 34, 32, 255); var wood = new Color32(105, 82, 53, 255);
            var stone = new Color32(115, 128, 84, 255); var green = new Color32(93, 175, 97, 255);
            var gold = new Color32(227, 187, 91, 255);
            Fill(p,w,h,11,2,20,15,o); Fill(p,w,h,14,5,14,10,wood); Fill(p,w,h,8,17,27,24,o);
            Fill(p,w,h,11,19,21,20,stone); Fill(p,w,h,17,21,10,11,green); Fill(p,w,h,7,22,7,16,o);
            Fill(p,w,h,1,26,10,12,wood); Fill(p,w,h,30,22,7,16,o); Fill(p,w,h,32,26,9,12,wood);
            Fill(p,w,h,16,25,3,3,gold); Fill(p,w,h,26,25,3,3,gold); Fill(p,w,h,12,39,8,6,o);
            Fill(p,w,h,24,39,8,6,o); Fill(p,w,h,14,0,4,8,green); Fill(p,w,h,24,0,4,8,green);
        }

        private static void DrawCrownwardColossusPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(23, 34, 34, 255); var bark = new Color32(93, 82, 59, 255);
            var stone = new Color32(116, 135, 83, 255); var gold = new Color32(231, 190, 84, 255);
            var green = new Color32(68, 160, 104, 255);
            Fill(p,w,h,9,2,34,20,o); Fill(p,w,h,12,5,28,14,bark); Fill(p,w,h,15,1,7,10,green);
            Fill(p,w,h,29,0,8,12,green); Fill(p,w,h,9,19,35,29,o); Fill(p,w,h,13,22,27,23,stone);
            Fill(p,w,h,19,24,15,17,bark); Fill(p,w,h,21,28,11,9,green); Fill(p,w,h,16,26,5,4,gold);
            Fill(p,w,h,30,26,5,4,gold); Fill(p,w,h,4,24,11,20,o); Fill(p,w,h,0,29,10,12,bark);
            Fill(p,w,h,38,24,11,20,o); Fill(p,w,h,42,29,10,12,bark); Fill(p,w,h,14,47,10,5,o);
            Fill(p,w,h,30,47,10,5,o);
        }

        private static void DrawEvelynHartPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 27, 43, 255); var silver = new Color32(197, 207, 217, 255);
            var skin = new Color32(224, 174, 139, 255); var robe = new Color32(62, 66, 119, 255);
            var light = new Color32(114, 120, 180, 255); var gold = new Color32(232, 190, 91, 255);
            Fill(p,w,h,7,1,18,8,outline); Fill(p,w,h,9,3,14,5,silver); Fill(p,w,h,8,9,17,13,outline);
            Fill(p,w,h,10,11,13,9,skin); Fill(p,w,h,7,10,4,14,silver); Fill(p,w,h,22,10,4,14,silver);
            Fill(p,w,h,12,15,2,2,outline); Fill(p,w,h,20,15,2,2,outline); Fill(p,w,h,7,22,20,18,outline);
            Fill(p,w,h,9,24,16,14,robe); Fill(p,w,h,13,24,8,14,light); Fill(p,w,h,15,26,4,6,gold);
            Fill(p,w,h,10,39,7,4,outline); Fill(p,w,h,20,39,7,4,outline);
        }

        private static void DrawJaceMorrowPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 28, 37, 255); var hair = new Color32(67, 53, 46, 255);
            var skin = new Color32(204, 151, 112, 255); var coat = new Color32(48, 91, 97, 255);
            var light = new Color32(102, 148, 146, 255); var brass = new Color32(201, 157, 73, 255);
            Fill(p,w,h,8,4,17,7,outline); Fill(p,w,h,10,6,13,4,hair); Fill(p,w,h,8,11,18,13,outline);
            Fill(p,w,h,10,13,14,9,skin); Fill(p,w,h,7,12,4,11,hair); Fill(p,w,h,21,12,5,12,hair);
            Fill(p,w,h,12,17,2,2,outline); Fill(p,w,h,20,17,2,2,outline); Fill(p,w,h,5,24,23,17,outline);
            Fill(p,w,h,7,26,19,13,coat); Fill(p,w,h,12,26,9,13,light); Fill(p,w,h,17,29,8,3,brass);
            Fill(p,w,h,9,40,7,4,outline); Fill(p,w,h,20,40,7,4,outline);
        }

        private static void DrawOuterwakeLensPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(25, 30, 46, 255); var steel = new Color32(102, 124, 158, 255);
            var pale = new Color32(163, 202, 216, 255); var glow = new Color32(104, 238, 227, 255);
            Fill(p,w,h,4,4,28,26,outline); Fill(p,w,h,7,7,22,20,steel); Fill(p,w,h,10,10,16,14,outline);
            Fill(p,w,h,13,12,10,10,glow); Fill(p,w,h,15,13,5,7,pale); Fill(p,w,h,16,30,4,4,outline);
            Fill(p,w,h,9,34,18,3,outline); Fill(p,w,h,12,37,12,4,steel);
        }

        private static void DrawOuterwakeRecordPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 29, 44, 255); var stone = new Color32(92, 107, 139, 255);
            var pale = new Color32(177, 190, 203, 255); var cyan = new Color32(101, 220, 218, 255);
            Fill(p,w,h,7,2,22,31,outline); Fill(p,w,h,10,5,16,25,stone); Fill(p,w,h,13,10,10,2,pale);
            Fill(p,w,h,13,16,9,2,cyan); Fill(p,w,h,13,22,10,2,pale); Fill(p,w,h,13,28,7,2,cyan);
            Fill(p,w,h,3,33,30,4,outline); Fill(p,w,h,9,37,18,3,stone);
        }

        private static void DrawOuterwakeSamplePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 28, 43, 255); var glass = new Color32(92, 140, 160, 255);
            var silt = new Color32(72, 63, 112, 255); var cyan = new Color32(106, 228, 221, 255);
            var brass = new Color32(211, 171, 83, 255);
            Fill(p,w,h,12,3,12,7,outline); Fill(p,w,h,14,5,8,4,brass); Fill(p,w,h,8,9,20,23,outline);
            Fill(p,w,h,11,12,14,17,glass); Fill(p,w,h,12,22,12,5,silt); Fill(p,w,h,14,18,4,3,cyan);
            Fill(p,w,h,22,15,3,3,cyan); Fill(p,w,h,5,32,26,4,outline); Fill(p,w,h,10,36,16,3,glass);
        }

        private static void DrawOuterwakeAnchorPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(26, 29, 44, 255); var steel = new Color32(91, 111, 151, 255);
            var gold = new Color32(225, 185, 94, 255); var glow = new Color32(112, 237, 218, 255);
            Fill(p,w,h,11,2,14,29,outline); Fill(p,w,h,14,5,8,23,steel); Fill(p,w,h,4,11,10,12,outline);
            Fill(p,w,h,6,13,8,8,gold); Fill(p,w,h,22,11,10,12,outline); Fill(p,w,h,24,13,7,8,gold);
            Fill(p,w,h,15,12,6,9,glow); Fill(p,w,h,5,32,26,4,outline); Fill(p,w,h,9,36,18,3,steel);
        }

        private static void DrawOuterwakeTransmitterPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 28, 42, 255); var steel = new Color32(89, 107, 144, 255);
            var gold = new Color32(226, 183, 82, 255); var cyan = new Color32(103, 235, 220, 255);
            Fill(p,w,h,13,5,6,28,outline); Fill(p,w,h,15,8,2,22,steel); Fill(p,w,h,5,8,15,10,outline);
            Fill(p,w,h,8,11,9,4,gold); Fill(p,w,h,18,12,10,11,outline); Fill(p,w,h,20,14,6,6,cyan);
            Fill(p,w,h,6,33,23,4,outline); Fill(p,w,h,10,37,15,3,steel);
        }

        private static void DrawOuterwakeForgePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(28, 30, 42, 255); var iron = new Color32(94, 104, 125, 255);
            var stone = new Color32(115, 95, 76, 255); var flame = new Color32(239, 163, 76, 255);
            var cyan = new Color32(99, 210, 219, 255);
            Fill(p,w,h,3,9,30,20,outline); Fill(p,w,h,6,12,24,14,stone); Fill(p,w,h,9,16,8,10,flame);
            Fill(p,w,h,10,19,6,7,cyan); Fill(p,w,h,20,16,9,8,iron); Fill(p,w,h,5,29,27,4,outline);
            Fill(p,w,h,9,33,5,7,outline); Fill(p,w,h,23,33,5,7,outline);
        }

        private static void DrawOuterwakeWindMastPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(27, 30, 44, 255); var bronze = new Color32(154, 112, 65, 255);
            var steel = new Color32(131, 150, 164, 255); var cyan = new Color32(98, 225, 222, 255);
            var gold = new Color32(224, 185, 92, 255);
            Fill(p,w,h,14,5,7,28,outline); Fill(p,w,h,16,7,3,25,bronze); Fill(p,w,h,7,12,23,4,outline);
            Fill(p,w,h,2,8,11,9,outline); Fill(p,w,h,4,10,8,5,steel); Fill(p,w,h,23,8,10,9,outline);
            Fill(p,w,h,25,10,7,5,steel); Fill(p,w,h,11,17,13,11,outline); Fill(p,w,h,13,19,9,7,cyan);
            Fill(p,w,h,17,21,1,3,gold); Fill(p,w,h,5,34,24,4,outline); Fill(p,w,h,8,37,18,3,bronze);
        }

        private static void DrawOuterwakeTideGaugePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(26, 34, 47, 255); var stone = new Color32(102, 115, 129, 255);
            var light = new Color32(158, 172, 178, 255); var cyan = new Color32(73, 190, 206, 255);
            var gold = new Color32(225, 187, 95, 255);
            Fill(p,w,h,3,4,30,24,outline); Fill(p,w,h,6,7,24,18,stone); Fill(p,w,h,8,19,20,5,cyan);
            Fill(p,w,h,10,16,5,1,light); Fill(p,w,h,20,13,5,1,light); Fill(p,w,h,10,11,5,1,light);
            Fill(p,w,h,9,7,2,12,gold); Fill(p,w,h,8,4,4,3,outline); Fill(p,w,h,2,28,32,3,outline);
        }

        private static void DrawOuterwakeReplyConsolePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(24, 29, 43, 255); var iron = new Color32(88, 105, 131, 255);
            var silver = new Color32(167, 181, 194, 255); var cyan = new Color32(87, 224, 220, 255);
            var gold = new Color32(221, 178, 84, 255);
            Fill(p,w,h,4,7,28,24,outline); Fill(p,w,h,7,10,22,18,iron); Fill(p,w,h,10,13,16,9,outline);
            Fill(p,w,h,12,15,12,5,cyan); Fill(p,w,h,14,16,8,2,silver); Fill(p,w,h,8,23,4,3,gold);
            Fill(p,w,h,15,23,4,3,gold); Fill(p,w,h,23,23,4,3,gold); Fill(p,w,h,9,31,5,4,outline);
            Fill(p,w,h,22,31,5,4,outline); Fill(p,w,h,2,34,32,3,outline);
        }

        private static void DrawOuterwakeFieldCompassPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(26, 31, 44, 255); var bronze = new Color32(159, 112, 57, 255);
            var gold = new Color32(232, 190, 86, 255); var cyan = new Color32(77, 216, 217, 255);
            var pale = new Color32(187, 219, 216, 255);
            Fill(p,w,h,11,2,10,3,outline); Fill(p,w,h,8,5,16,3,outline); Fill(p,w,h,5,8,22,16,outline);
            Fill(p,w,h,7,10,18,12,bronze); Fill(p,w,h,10,13,12,6,outline); Fill(p,w,h,14,14,4,4,pale);
            Fill(p,w,h,15,9,2,6,gold); Fill(p,w,h,15,18,2,7,cyan); Fill(p,w,h,9,15,7,2,gold);
            Fill(p,w,h,17,15,7,2,cyan); Fill(p,w,h,9,24,14,4,outline); Fill(p,w,h,12,28,8,2,bronze);
        }

        private static void DrawRiftHoundPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(20, 23, 41, 255); var hide = new Color32(75, 65, 117, 255);
            var light = new Color32(126, 111, 186, 255); var cyan = new Color32(99, 235, 232, 255);
            Fill(p,w,h,7,10,30,18,outline); Fill(p,w,h,10,12,24,13,hide); Fill(p,w,h,27,4,13,13,outline);
            Fill(p,w,h,30,7,8,8,light); Fill(p,w,h,32,10,3,3,cyan); Fill(p,w,h,37,13,7,6,outline);
            Fill(p,w,h,2,9,13,12,outline); Fill(p,w,h,4,11,8,7,light); Fill(p,w,h,12,25,7,8,outline);
            Fill(p,w,h,30,25,7,8,outline); Fill(p,w,h,6,29,12,4,outline); Fill(p,w,h,29,29,11,4,outline);
            Fill(p,w,h,16,17,8,4,cyan); Fill(p,w,h,22,15,5,7,outline);
        }

        private static void DrawStarLeecherPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(22, 30, 49, 255); var body = new Color32(57, 90, 132, 255);
            var cyan = new Color32(101, 224, 235, 255); var white = new Color32(209, 227, 236, 255);
            Fill(p,w,h,12,3,12,12,outline); Fill(p,w,h,14,5,8,8,body); Fill(p,w,h,14,14,8,15,outline);
            Fill(p,w,h,16,16,4,10,cyan); Fill(p,w,h,5,12,10,6,outline); Fill(p,w,h,3,14,9,3,body);
            Fill(p,w,h,21,12,10,6,outline); Fill(p,w,h,24,14,9,3,body); Fill(p,w,h,8,26,6,11,outline);
            Fill(p,w,h,21,26,7,11,outline); Fill(p,w,h,2,35,12,5,body); Fill(p,w,h,21,35,13,5,body);
            Fill(p,w,h,16,2,4,4,white);
        }

        private static void DrawArchiveScribePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(22, 25, 42, 255); var robe = new Color32(70, 71, 112, 255);
            var pale = new Color32(150, 179, 204, 255); var gold = new Color32(229, 190, 95, 255);
            var cyan = new Color32(103, 226, 225, 255);
            Fill(p,w,h,10,3,22,17,outline); Fill(p,w,h,13,6,16,11,robe); Fill(p,w,h,15,10,13,6,outline);
            Fill(p,w,h,17,12,8,3,cyan); Fill(p,w,h,6,19,30,23,outline); Fill(p,w,h,9,22,24,18,robe);
            Fill(p,w,h,13,24,4,10,pale); Fill(p,w,h,24,24,4,10,pale); Fill(p,w,h,17,24,8,8,gold);
            Fill(p,w,h,3,27,8,14,outline); Fill(p,w,h,31,27,8,14,outline); Fill(p,w,h,10,41,7,6,outline);
            Fill(p,w,h,26,41,7,6,outline);
        }

        private static void DrawAsterionPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(23, 27, 43, 255); var steel = new Color32(87, 111, 151, 255);
            var pale = new Color32(166, 194, 213, 255); var gold = new Color32(228, 187, 88, 255);
            var cyan = new Color32(91, 229, 224, 255);
            Fill(p,w,h,17,0,18,13,gold); Fill(p,w,h,20,3,12,7,outline); Fill(p,w,h,9,12,34,18,outline);
            Fill(p,w,h,12,15,28,12,steel); Fill(p,w,h,17,18,18,7,outline); Fill(p,w,h,19,20,14,3,cyan);
            Fill(p,w,h,5,23,12,19,outline); Fill(p,w,h,7,26,8,13,pale); Fill(p,w,h,35,23,12,19,outline);
            Fill(p,w,h,37,26,8,13,pale); Fill(p,w,h,15,29,22,19,outline); Fill(p,w,h,18,32,16,12,steel);
            Fill(p,w,h,21,34,10,8,gold); Fill(p,w,h,18,47,9,8,outline); Fill(p,w,h,31,47,9,8,outline);
            Fill(p,w,h,0,18,13,3,gold); Fill(p,w,h,39,18,13,3,gold);
        }

        private static void DrawVeilshardDrakePixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(21, 24, 42, 255); var hide = new Color32(67, 87, 135, 255);
            var pale = new Color32(130, 161, 201, 255); var cyan = new Color32(101, 230, 235, 255);
            var gold = new Color32(227, 183, 89, 255);
            Fill(p,w,h,5,9,28,18,outline); Fill(p,w,h,9,12,21,12,hide); Fill(p,w,h,28,6,19,16,outline);
            Fill(p,w,h,32,9,13,10,hide); Fill(p,w,h,39,13,3,3,cyan); Fill(p,w,h,45,17,10,5,outline);
            Fill(p,w,h,2,1,23,18,outline); Fill(p,w,h,5,4,15,11,pale); Fill(p,w,h,29,0,23,18,outline);
            Fill(p,w,h,33,3,15,11,hide); Fill(p,w,h,13,20,13,8,gold); Fill(p,w,h,10,27,7,13,outline);
            Fill(p,w,h,30,26,8,14,outline); Fill(p,w,h,5,37,14,5,outline); Fill(p,w,h,30,38,15,5,outline);
            Fill(p,w,h,22,25,5,7,cyan); Fill(p,w,h,0,15,9,4,outline);
        }

        private static void DrawCycleRemnantPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(30, 28, 42, 255); var armor = new Color32(109, 91, 81, 255);
            var pale = new Color32(172, 152, 121, 255); var ember = new Color32(228, 116, 65, 255);
            var cyan = new Color32(109, 205, 188, 255);
            Fill(p,w,h,11,2,20,18,outline); Fill(p,w,h,14,5,14,12,armor); Fill(p,w,h,17,11,9,4,ember);
            Fill(p,w,h,8,20,27,24,outline); Fill(p,w,h,11,23,21,18,armor); Fill(p,w,h,18,24,8,13,pale);
            Fill(p,w,h,4,22,9,17,outline); Fill(p,w,h,0,25,13,8,armor); Fill(p,w,h,30,20,9,19,outline);
            Fill(p,w,h,32,23,9,13,pale); Fill(p,w,h,12,42,8,5,outline); Fill(p,w,h,25,42,8,5,outline);
            Fill(p,w,h,14,28,4,4,cyan); Fill(p,w,h,25,28,4,4,ember); Fill(p,w,h,18,0,5,7,pale);
        }

        private static void DrawDemonKingAldenPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(22, 21, 35, 255); var armor = new Color32(82, 48, 56, 255);
            var crimson = new Color32(153, 62, 62, 255); var gold = new Color32(225, 174, 78, 255);
            var ember = new Color32(247, 119, 57, 255);
            Fill(p,w,h,15,2,25,18,outline); Fill(p,w,h,18,5,19,12,armor); Fill(p,w,h,12,0,9,12,outline);
            Fill(p,w,h,15,2,4,7,gold); Fill(p,w,h,34,0,10,12,outline); Fill(p,w,h,37,2,4,7,gold);
            Fill(p,w,h,20,13,16,4,ember); Fill(p,w,h,10,20,36,28,outline); Fill(p,w,h,14,23,28,21,crimson);
            Fill(p,w,h,23,24,14,22,armor); Fill(p,w,h,25,27,10,11,ember); Fill(p,w,h,4,22,13,25,outline);
            Fill(p,w,h,0,26,14,15,armor); Fill(p,w,h,39,21,13,25,outline); Fill(p,w,h,41,25,13,16,crimson);
            Fill(p,w,h,15,47,10,10,outline); Fill(p,w,h,32,47,10,10,outline); Fill(p,w,h,17,54,7,4,gold);
            Fill(p,w,h,33,54,7,4,gold); Fill(p,w,h,5,13,8,3,ember); Fill(p,w,h,42,13,8,3,ember);
        }

        private static void DrawWorldWillAvatarPixelArt(Color32[] p, int w, int h)
        {
            var outline = new Color32(22, 31, 49, 255); var mantle = new Color32(64, 105, 134, 255);
            var silver = new Color32(172, 208, 220, 255); var cyan = new Color32(104, 231, 228, 255);
            var gold = new Color32(235, 194, 110, 255);
            Fill(p,w,h,16,2,23,16,outline); Fill(p,w,h,19,5,17,10,mantle); Fill(p,w,h,22,9,11,5,cyan);
            Fill(p,w,h,12,18,31,29,outline); Fill(p,w,h,16,21,23,22,mantle); Fill(p,w,h,23,22,10,19,silver);
            Fill(p,w,h,25,26,6,10,cyan); Fill(p,w,h,4,21,13,20,outline); Fill(p,w,h,0,25,13,12,silver);
            Fill(p,w,h,38,19,13,22,outline); Fill(p,w,h,41,23,10,13,mantle); Fill(p,w,h,14,45,11,9,outline);
            Fill(p,w,h,31,45,11,9,outline); Fill(p,w,h,17,52,7,5,gold); Fill(p,w,h,33,52,7,5,gold);
            Fill(p,w,h,19,0,6,7,gold); Fill(p,w,h,32,0,6,7,gold); Fill(p,w,h,22,32,12,3,gold);
        }

        private static void DrawEmbermawMatriarchPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(39, 27, 35, 255); var hide = new Color32(105, 56, 48, 255);
            var ash = new Color32(177, 121, 83, 255); var ember = new Color32(248, 133, 55, 255);
            var gold = new Color32(255, 212, 115, 255);
            Fill(p,w,h,4,13,40,23,o); Fill(p,w,h,8,16,33,16,hide); Fill(p,w,h,28,6,16,18,o);
            Fill(p,w,h,32,9,10,12,ash); Fill(p,w,h,38,14,3,3,ember); Fill(p,w,h,44,18,6,5,o);
            Fill(p,w,h,5,8,9,13,o); Fill(p,w,h,8,9,4,9,ember); Fill(p,w,h,0,5,8,9,o);
            Fill(p,w,h,13,30,8,12,o); Fill(p,w,h,32,30,8,12,o); Fill(p,w,h,19,20,8,5,ember);
            Fill(p,w,h,0,27,12,4,ash); Fill(p,w,h,39,27,9,4,ash); Fill(p,w,h,21,21,3,3,gold);
        }

        private static void DrawIronwardSentinelPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(24, 31, 43, 255); var iron = new Color32(91, 113, 137, 255);
            var plate = new Color32(157, 180, 191, 255); var blue = new Color32(57, 112, 164, 255);
            var brass = new Color32(225, 180, 84, 255);
            Fill(p,w,h,10,1,25,13,o); Fill(p,w,h,13,4,19,8,iron); Fill(p,w,h,17,8,11,4,blue);
            Fill(p,w,h,8,14,30,24,o); Fill(p,w,h,11,17,24,18,plate); Fill(p,w,h,19,17,9,19,blue);
            Fill(p,w,h,4,15,9,24,o); Fill(p,w,h,0,18,12,16,iron); Fill(p,w,h,33,15,9,24,o);
            Fill(p,w,h,36,19,9,16,iron); Fill(p,w,h,12,37,9,10,o); Fill(p,w,h,26,37,9,10,o);
            Fill(p,w,h,14,42,7,8,blue); Fill(p,w,h,28,42,7,8,blue); Fill(p,w,h,20,21,7,5,brass);
        }

        private static void DrawSluicewheelColossusPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(29, 36, 42, 255); var bronze = new Color32(139, 103, 62, 255);
            var steel = new Color32(105, 129, 132, 255); var water = new Color32(52, 159, 173, 255);
            var foam = new Color32(165, 221, 208, 255);
            Fill(p,w,h,12,2,28,13,o); Fill(p,w,h,15,5,22,8,bronze); Fill(p,w,h,20,8,12,4,water);
            Fill(p,w,h,6,15,40,31,o); Fill(p,w,h,10,18,32,25,steel); Fill(p,w,h,18,20,16,20,bronze);
            Fill(p,w,h,21,24,10,12,water); Fill(p,w,h,0,19,14,10,o); Fill(p,w,h,2,22,9,5,foam);
            Fill(p,w,h,38,16,14,11,o); Fill(p,w,h,42,19,9,5,water); Fill(p,w,h,13,43,9,8,o);
            Fill(p,w,h,31,43,9,8,o); Fill(p,w,h,0,31,10,4,foam); Fill(p,w,h,43,30,9,4,foam);
        }

        private static void DrawRedpassHarrowerPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(35, 29, 34, 255); var leather = new Color32(108, 66, 48, 255);
            var rust = new Color32(169, 83, 57, 255); var iron = new Color32(113, 122, 126, 255);
            var brass = new Color32(225, 170, 79, 255);
            Fill(p,w,h,13,2,26,13,o); Fill(p,w,h,16,5,20,8,iron); Fill(p,w,h,19,10,14,4,rust);
            Fill(p,w,h,8,15,39,24,o); Fill(p,w,h,12,18,31,17,leather); Fill(p,w,h,21,18,15,19,iron);
            Fill(p,w,h,4,17,12,20,o); Fill(p,w,h,0,20,14,12,rust); Fill(p,w,h,36,16,12,9,o);
            Fill(p,w,h,43,15,8,5,iron); Fill(p,w,h,47,12,6,4,o); Fill(p,w,h,39,22,5,14,o);
            Fill(p,w,h,13,37,10,9,o); Fill(p,w,h,32,37,10,9,o); Fill(p,w,h,24,22,7,5,brass);
        }

        private static void DrawDeepbellHeraldPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(23, 36, 48, 255); var shell = new Color32(75, 111, 133, 255);
            var silver = new Color32(164, 190, 190, 255); var cyan = new Color32(99, 223, 215, 255);
            var gold = new Color32(227, 187, 93, 255);
            Fill(p,w,h,13,2,22,8,o); Fill(p,w,h,16,5,16,3,gold); Fill(p,w,h,8,10,32,29,o);
            Fill(p,w,h,12,13,24,21,shell); Fill(p,w,h,18,17,12,15,silver); Fill(p,w,h,22,19,5,10,cyan);
            Fill(p,w,h,3,16,10,22,o); Fill(p,w,h,0,20,13,13,shell); Fill(p,w,h,35,16,10,22,o);
            Fill(p,w,h,37,20,11,13,shell); Fill(p,w,h,16,37,6,12,o); Fill(p,w,h,29,37,6,12,o);
            Fill(p,w,h,5,43,14,4,o); Fill(p,w,h,29,43,14,4,o); Fill(p,w,h,20,11,4,5,gold);
        }

        private static void DrawSeedvaultKeeperPixelArt(Color32[] p, int w, int h)
        {
            var o = new Color32(26, 38, 34, 255); var bark = new Color32(99, 92, 57, 255);
            var moss = new Color32(91, 157, 89, 255); var stone = new Color32(136, 148, 102, 255);
            var gold = new Color32(235, 193, 92, 255);
            Fill(p,w,h,12,15,30,17,o); Fill(p,w,h,15,18,24,11,stone); Fill(p,w,h,19,22,16,8,bark);
            Fill(p,w,h,7,30,41,19,o); Fill(p,w,h,11,33,33,15,bark); Fill(p,w,h,21,34,14,12,moss);
            Fill(p,w,h,8,4,8,15,o); Fill(p,w,h,4,0,13,9,moss); Fill(p,w,h,37,4,8,15,o);
            Fill(p,w,h,36,0,14,9,moss); Fill(p,w,h,0,26,14,16,o); Fill(p,w,h,2,29,11,10,stone);
            Fill(p,w,h,40,25,14,17,o); Fill(p,w,h,42,28,11,11,stone); Fill(p,w,h,15,42,9,11,o);
            Fill(p,w,h,31,42,9,11,o); Fill(p,w,h,19,37,5,5,gold); Fill(p,w,h,31,37,5,5,gold);
        }

        private static void DrawChargeLanePixelArt(Color32[] p, int w, int h)
        {
            var dark = new Color32(104, 45, 34, 255); var orange = new Color32(255, 139, 57, 255);
            var bright = new Color32(255, 224, 143, 255);
            Fill(p,w,h,0,0,w,h,dark); Fill(p,w,h,2,2,w-4,h-4,orange); Fill(p,w,h,8,3,w-16,h-6,bright);
        }

        private static void Fill(Color32[] pixels, int width, int height, int x, int y, int rectWidth, int rectHeight, Color32 color)
        {
            var x0 = Mathf.Clamp(x, 0, width);
            var y0 = Mathf.Clamp(y, 0, height);
            var x1 = Mathf.Clamp(x + rectWidth, 0, width);
            var y1 = Mathf.Clamp(y + rectHeight, 0, height);
            for (var py = y0; py < y1; py++)
                for (var px = x0; px < x1; px++)
                    pixels[py * width + px] = color;
        }
    }
}
