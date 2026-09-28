using System;
using System.Collections.Generic;
using AshenOath.Core;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using AshenOath.World;

namespace AshenOath.UI
{
    public sealed class DialogueChoiceOption
    {
        public string Id { get; }
        public string Label { get; }

        public DialogueChoiceOption(string id, string label)
        {
            Id = id;
            Label = label;
        }
    }

    public sealed class InventoryItemRow
    {
        public string ItemId { get; }
        public string Label { get; }
        public bool CanEquip { get; }
        public Sprite Icon { get; }

        public InventoryItemRow(string itemId, string label, bool canEquip, Sprite icon = null)
        {
            ItemId = itemId;
            Label = label;
            CanEquip = canEquip;
            Icon = icon;
        }
    }

    public sealed class QuestJournalRow
    {
        public string QuestId { get; }
        public string Label { get; }
        public bool CanAccept { get; }

        public QuestJournalRow(string questId, string label, bool canAccept)
        {
            QuestId = questId;
            Label = label;
            CanAccept = canAccept;
        }
    }

    public sealed class GameHud : MonoBehaviour
    {
        private Canvas canvas;
        private Text heroText;
        private Text healthText;
        private Text inventoryText;
        private Text questTitleText;
        private Text questObjectiveText;
        private Text actionText;
        private Text attackText;
        private Text combatText;
        private GameObject dialoguePanel;
        private GameObject controlsRoot;
        private GameObject choicesRoot;
        private GameObject inventoryPanel;
        private GameObject questJournalPanel;
        private GameObject codexPanel;
        private GameObject creditsPanel;
        private GameObject endingPanel;
        private GameObject titleScreen;
        private GameObject dialoguePortraitFrame;
        private RectTransform inventoryContent;
        private RectTransform questJournalContent;
        private RectTransform codexListContent;
        private RectTransform codexDetailContent;
        private Text equipmentSummaryText;
        private Button nextButton;
        private Text speakerText;
        private Text dialogueText;
        private RectTransform dialogueScrollContent;
        private RectTransform dialogueViewportRect;
        private ScrollRect dialogueScrollRect;
        private Image dialoguePortraitImage;
        private string[] dialogueLines;
        private int dialogueIndex;
        private Action dialogueComplete;
        private Action<string> choiceSelected;
        private Action endingContinue;
        private Action titleStartAction;
        private Text endingTitleText;
        private Text endingBodyText;
        private Text titleActionText;
        private Text titleCaptionText;
        private bool choosing;
        private static readonly Dictionary<string, Sprite> dialoguePortraits = new Dictionary<string, Sprite>();

        public VirtualStick Stick { get; private set; }
        public bool IsChoosing => choosing;

        public void ConfirmDialogue()
        {
            if (!choosing && dialoguePanel != null && dialoguePanel.activeSelf) AdvanceDialogue();
        }

        public void Build(GameRuntime game)
        {
            EnsureEventSystem();

            var canvasObject = new GameObject("HUD Canvas", typeof(RectTransform), typeof(Canvas),
                typeof(CanvasScaler), typeof(GraphicRaycaster));
            canvas = canvasObject.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 20;
            var scaler = canvasObject.GetComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1920, 1080);
            scaler.screenMatchMode = CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
            scaler.matchWidthOrHeight = 0.5f;

            BuildTopHud(canvas.transform, game);
            BuildControls(canvas.transform, game);
            BuildDialogue(canvas.transform);
            BuildCombat(canvas.transform);
            BuildInventory(canvas.transform, game);
            BuildQuestJournal(canvas.transform, game);
            BuildCodex(canvas.transform, game);
            BuildCredits(canvas.transform, game);
            BuildEnding(canvas.transform, game);
            BuildTitleScreen(canvas.transform);
        }

        private void BuildTitleScreen(Transform parent)
        {
            titleScreen = new GameObject("Title screen", typeof(RectTransform), typeof(Image));
            titleScreen.transform.SetParent(parent, false);
            var rootRect = titleScreen.GetComponent<RectTransform>();
            Stretch(rootRect);
            var background = titleScreen.GetComponent<Image>();
            background.raycastTarget = false;
            background.color = new Color(0.025f, 0.04f, 0.07f, 1f);
            var titleTexture = Resources.Load<Texture2D>("Art/ashen_oath_title");
            if (titleTexture != null)
            {
                titleTexture.filterMode = FilterMode.Bilinear;
                background.sprite = Sprite.Create(titleTexture,
                    new Rect(0, 0, titleTexture.width, titleTexture.height), new Vector2(0.5f, 0.5f), 100f);
                background.type = Image.Type.Simple;
                background.color = Color.white;
            }

            var shade = MakePanel("Title shade", titleScreen.transform, Vector2.zero, Vector2.one,
                Vector2.zero, Vector2.zero, new Color(0.015f, 0.025f, 0.05f, 0.2f));
            var shadeRect = shade.GetComponent<RectTransform>();
            shadeRect.pivot = new Vector2(0.5f, 0.5f);
            Stretch(shadeRect);
            shade.GetComponent<Image>().raycastTarget = false;

            var title = MakeText("Title logo", titleScreen.transform, "ASHEN OATH", 76,
                new Color(0.96f, 0.82f, 0.56f), TextAnchor.MiddleCenter,
                new Vector2(0, -178), new Vector2(1080, 122), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            title.fontStyle = FontStyle.Bold;
            var titleShadow = title.gameObject.AddComponent<Shadow>();
            titleShadow.effectColor = new Color(0, 0, 0, 0.9f);
            titleShadow.effectDistance = new Vector2(3, -3);
            MakeText("Title tagline", titleScreen.transform, "A WORLD HELD FOR ONE HUNDRED YEARS", 25,
                new Color(0.88f, 0.9f, 0.93f), TextAnchor.MiddleCenter,
                new Vector2(0, -282), new Vector2(980, 50), new Vector2(0.5f, 1), new Vector2(0.5f, 1));

            var button = MakeButton("Begin or continue", titleScreen.transform, "BẮT ĐẦU HÀNH TRÌNH",
                new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0, 142),
                new Vector2(480, 88), StartFromTitle);
            button.GetComponent<RectTransform>().pivot = new Vector2(0.5f, 0);
            button.GetComponent<Image>().color = new Color(0.19f, 0.16f, 0.11f, 0.97f);
            titleActionText = button.GetComponentInChildren<Text>();
            titleActionText.fontSize = 29;
            titleActionText.fontStyle = FontStyle.Bold;
            titleActionText.color = new Color(0.97f, 0.85f, 0.61f);
            titleCaptionText = MakeText("Title save caption", titleScreen.transform,
                "OFFLINE ADVENTURE  ·  SAVE STORED ON THIS DEVICE", 18,
                new Color(0.84f, 0.86f, 0.89f), TextAnchor.MiddleCenter,
                new Vector2(0, 31), new Vector2(900, 40), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            titleScreen.SetActive(false);
        }

        public void ShowTitleScreen(bool hasSave, Action onStart)
        {
            titleStartAction = onStart;
            if (titleActionText != null)
                titleActionText.text = hasSave ? "TIẾP TỤC HÀNH TRÌNH" : "BẮT ĐẦU HÀNH TRÌNH";
            if (titleCaptionText != null)
                titleCaptionText.text = hasSave
                    ? "OFFLINE ADVENTURE  ·  TIẾN ĐỘ ĐƯỢC LƯU TRÊN THIẾT BỊ NÀY"
                    : "OFFLINE ADVENTURE  ·  SAVE STORED ON THIS DEVICE";
            controlsRoot?.SetActive(false);
            titleScreen?.SetActive(true);
        }

        private void StartFromTitle()
        {
            titleScreen?.SetActive(false);
            var action = titleStartAction;
            titleStartAction = null;
            action?.Invoke();
        }

        private void BuildTopHud(Transform parent, GameRuntime game)
        {
            var panel = MakePanel("Quest and status", parent, new Vector2(0, 1), new Vector2(0, 1),
                new Vector2(22, -22), new Vector2(620, 186), new Color(0.055f, 0.075f, 0.105f, 0.91f));
            heroText = MakeText("Hero", panel.transform, "ROWAN HALE  •  CẤP 01", 34,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(22, -20), new Vector2(575, 44), new Vector2(0, 1), new Vector2(0, 1));
            healthText = MakeText("Health", panel.transform, "MÁU 48 / 48", 22, Color.white,
                TextAnchor.MiddleLeft, new Vector2(22, -65), new Vector2(270, 34), new Vector2(0, 1), new Vector2(0, 1));
            inventoryText = MakeText("Inventory", panel.transform, "VÀNG 12 • NANH 0 • THUỐC 1", 20,
                new Color(0.82f, 0.83f, 0.8f), TextAnchor.MiddleRight,
                new Vector2(-22, -65), new Vector2(300, 34), new Vector2(1, 1), new Vector2(1, 1));
            questTitleText = MakeText("Quest title", panel.transform, "TRO BỤI ASHFALL", 22,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(22, -108), new Vector2(575, 28), new Vector2(0, 1), new Vector2(0, 1));
            questObjectiveText = MakeText("Quest objective", panel.transform, "Tìm Mira Cole bên giếng cũ.", 22,
                Color.white, TextAnchor.MiddleLeft,
                new Vector2(22, -140), new Vector2(575, 34), new Vector2(0, 1), new Vector2(0, 1));

            MakeText("Game title", parent, "ASHEN OATH", 33, new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleCenter,
                Vector2.zero, new Vector2(410, 54), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            MakeButton("Open inventory", parent, "HÀNH TRANG", new Vector2(1, 1), new Vector2(1, 1),
                new Vector2(-32, -112), new Vector2(220, 78), game.ToggleInventory);
            MakeButton("Open quest journal", parent, "SỔ NHIỆM VỤ", new Vector2(1, 1), new Vector2(1, 1),
                new Vector2(-32, -202), new Vector2(220, 78), game.ToggleQuestJournal);
            MakeButton("Open credits", parent, "CREDITS", new Vector2(1, 1), new Vector2(1, 1),
                new Vector2(-32, -292), new Vector2(220, 64), game.OpenCredits);
            MakeButton("Open field archive", parent, "TƯ LIỆU", new Vector2(1, 1), new Vector2(1, 1),
                new Vector2(-32, -366), new Vector2(220, 64), game.OpenCodex);
        }

        private void BuildControls(Transform parent, GameRuntime game)
        {
            controlsRoot = new GameObject("Touch controls", typeof(RectTransform));
            controlsRoot.transform.SetParent(parent, false);
            var rootRect = controlsRoot.GetComponent<RectTransform>();
            Stretch(rootRect);

            var pad = MakePanel("Movement pad", controlsRoot.transform, new Vector2(0, 0), new Vector2(0, 0),
                new Vector2(72, 68), new Vector2(246, 246), new Color(0.055f, 0.075f, 0.105f, 0.64f));
            var padRect = pad.GetComponent<RectTransform>();
            padRect.pivot = new Vector2(0, 0);
            var knob = MakePanel("Movement knob", pad.transform, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                Vector2.zero, new Vector2(92, 92), new Color(0.84f, 0.71f, 0.45f, 0.84f));
            var stick = pad.AddComponent<VirtualStick>();
            stick.Initialize(padRect, knob.GetComponent<RectTransform>());
            Stick = stick;

            var interact = MakeButton("Interact", controlsRoot.transform, "TƯƠNG TÁC", new Vector2(1, 0),
                new Vector2(1, 0), new Vector2(-258, 82), new Vector2(202, 112), () => game.Interact());
            actionText = interact.GetComponentInChildren<Text>();
            var attack = MakeButton("Attack", controlsRoot.transform, "TẤN CÔNG", new Vector2(1, 0), new Vector2(1, 0),
                new Vector2(-72, 205), new Vector2(202, 112), () => game.Attack());
            attackText = attack.GetComponentInChildren<Text>();
            MakeButton("Dodge", controlsRoot.transform, "LƯỚT NÉ", new Vector2(1, 0), new Vector2(1, 0),
                new Vector2(-286, 205), new Vector2(202, 112), () => game.Dodge());
            MakeButton("Potion", controlsRoot.transform, "THUỐC", new Vector2(1, 0), new Vector2(1, 0),
                new Vector2(-72, 78), new Vector2(160, 94), () => game.UsePotion());
        }

        private void BuildDialogue(Transform parent)
        {
            dialoguePanel = MakePanel("Dialogue panel", parent, new Vector2(0, 0), new Vector2(1, 0),
                new Vector2(0, 22), new Vector2(0, 332), new Color(0.035f, 0.05f, 0.075f, 0.97f));
            var rect = dialoguePanel.GetComponent<RectTransform>();
            rect.offsetMin = new Vector2(28, 22);
            rect.offsetMax = new Vector2(-28, 354);

            dialoguePortraitFrame = MakePanel("Dialogue portrait frame", dialoguePanel.transform,
                Vector2.zero, Vector2.zero, new Vector2(38, 304), new Vector2(252, 276),
                new Color(0.75f, 0.58f, 0.32f, 0.96f));
            dialoguePortraitFrame.GetComponent<Image>().raycastTarget = false;
            var portraitObject = new GameObject("Dialogue portrait", typeof(RectTransform), typeof(Image));
            portraitObject.transform.SetParent(dialoguePortraitFrame.transform, false);
            var portraitRect = portraitObject.GetComponent<RectTransform>();
            portraitRect.anchorMin = Vector2.zero;
            portraitRect.anchorMax = Vector2.one;
            portraitRect.pivot = new Vector2(0.5f, 0.5f);
            portraitRect.offsetMin = new Vector2(5, 5);
            portraitRect.offsetMax = new Vector2(-5, -5);
            dialoguePortraitImage = portraitObject.GetComponent<Image>();
            dialoguePortraitImage.preserveAspect = true;
            dialoguePortraitImage.raycastTarget = false;

            speakerText = MakeText("Speaker", dialoguePanel.transform, "ROWAN HALE", 30,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(292, -24), new Vector2(-320, 52), new Vector2(0, 1), new Vector2(1, 1));

            var dialogueViewportObject = MakePanel("Dialogue text viewport", dialoguePanel.transform,
                Vector2.zero, Vector2.one, Vector2.zero, Vector2.zero,
                new Color(0.025f, 0.035f, 0.05f, 0.42f));
            dialogueViewportRect = dialogueViewportObject.GetComponent<RectTransform>();
            dialogueViewportRect.offsetMin = new Vector2(292, 110);
            dialogueViewportRect.offsetMax = new Vector2(-286, -82);
            dialogueViewportObject.AddComponent<RectMask2D>();
            dialogueScrollRect = dialogueViewportObject.AddComponent<ScrollRect>();
            dialogueScrollRect.viewport = dialogueViewportRect;
            dialogueScrollRect.horizontal = false;
            dialogueScrollRect.vertical = true;
            dialogueScrollRect.inertia = false;
            dialogueScrollRect.scrollSensitivity = 36f;
            dialogueScrollRect.movementType = ScrollRect.MovementType.Clamped;

            var dialogueContentObject = new GameObject("Dialogue text content", typeof(RectTransform));
            dialogueContentObject.transform.SetParent(dialogueViewportObject.transform, false);
            dialogueScrollContent = dialogueContentObject.GetComponent<RectTransform>();
            dialogueScrollContent.anchorMin = new Vector2(0, 1);
            dialogueScrollContent.anchorMax = new Vector2(1, 1);
            dialogueScrollContent.pivot = new Vector2(0.5f, 1);
            dialogueScrollContent.anchoredPosition = Vector2.zero;
            dialogueScrollContent.sizeDelta = Vector2.zero;
            dialogueScrollRect.content = dialogueScrollContent;
            dialogueText = MakeText("Dialogue", dialogueContentObject.transform, "", 27, Color.white,
                TextAnchor.UpperLeft, Vector2.zero, new Vector2(0, 150), new Vector2(0, 1), new Vector2(1, 1));
            dialogueText.rectTransform.pivot = new Vector2(0.5f, 1);

            var scrollTrackObject = MakePanel("Dialogue scroll track", dialoguePanel.transform,
                new Vector2(1, 0), Vector2.one, Vector2.zero, Vector2.zero,
                new Color(0.25f, 0.19f, 0.1f, 0.85f));
            var scrollTrack = scrollTrackObject.GetComponent<RectTransform>();
            scrollTrack.offsetMin = new Vector2(-278, 110);
            scrollTrack.offsetMax = new Vector2(-266, -82);
            var scrollHandleObject = MakePanel("Dialogue scroll handle", scrollTrackObject.transform,
                new Vector2(0, 1), Vector2.one, Vector2.zero, Vector2.zero,
                new Color(0.91f, 0.77f, 0.48f, 0.9f));
            var scrollHandle = scrollHandleObject.GetComponent<RectTransform>();
            scrollHandle.anchorMin = Vector2.zero;
            scrollHandle.anchorMax = Vector2.one;
            scrollHandle.offsetMin = new Vector2(1, 1);
            scrollHandle.offsetMax = new Vector2(-1, -1);
            var dialogueScrollbar = scrollTrackObject.AddComponent<Scrollbar>();
            dialogueScrollbar.handleRect = scrollHandle;
            dialogueScrollbar.targetGraphic = scrollHandleObject.GetComponent<Image>();
            dialogueScrollbar.direction = Scrollbar.Direction.BottomToTop;
            dialogueScrollRect.verticalScrollbar = dialogueScrollbar;
            dialogueScrollRect.verticalScrollbarVisibility = ScrollRect.ScrollbarVisibility.AutoHideAndExpandViewport;
            dialogueScrollRect.verticalScrollbarSpacing = 4f;

            nextButton = MakeButton("Continue", dialoguePanel.transform, "TIẾP TỤC", new Vector2(1, 0),
                new Vector2(1, 0), new Vector2(-34, 28), new Vector2(232, 80), AdvanceDialogue);

            choicesRoot = new GameObject("Story choices", typeof(RectTransform));
            choicesRoot.transform.SetParent(dialoguePanel.transform, false);
            var choiceRect = choicesRoot.GetComponent<RectTransform>();
            choiceRect.anchorMin = new Vector2(1, 0);
            choiceRect.anchorMax = new Vector2(1, 0);
            choiceRect.pivot = new Vector2(1, 0);
            choiceRect.anchoredPosition = new Vector2(-28, 27);
            choiceRect.sizeDelta = new Vector2(900, 92);
            choicesRoot.SetActive(false);
            dialoguePanel.SetActive(false);
        }

        private void BuildCombat(Transform parent)
        {
            var panel = MakePanel("Combat status", parent, new Vector2(1, 1), new Vector2(1, 1),
                new Vector2(-32, -32), new Vector2(390, 102), new Color(0.055f, 0.075f, 0.105f, 0.88f));
            panel.GetComponent<RectTransform>().pivot = new Vector2(1, 1);
            combatText = MakeText("Combat enemy", panel.transform, "", 25, Color.white, TextAnchor.MiddleCenter,
                Vector2.zero, new Vector2(350, 82), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panel.SetActive(false);
            combatPanel = panel;
        }

        private void BuildInventory(Transform parent, GameRuntime game)
        {
            inventoryPanel = MakePanel("Inventory window", parent, new Vector2(0.5f, 0.5f),
                new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1180, 740),
                new Color(0.035f, 0.05f, 0.075f, 0.98f));
            var panelRect = inventoryPanel.GetComponent<RectTransform>();
            panelRect.pivot = new Vector2(0.5f, 0.5f);

            MakeText("Inventory title", inventoryPanel.transform, "HÀNH TRANG", 34,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(32, -22), new Vector2(650, 54), new Vector2(0, 1), new Vector2(0, 1));
            equipmentSummaryText = MakeText("Equipment slots", inventoryPanel.transform, "", 21,
                Color.white, TextAnchor.MiddleLeft,
                new Vector2(32, -82), new Vector2(1080, 44), new Vector2(0, 1), new Vector2(0, 1));
            MakeButton("Close inventory", inventoryPanel.transform, "ĐÓNG", new Vector2(1, 0),
                new Vector2(1, 0), new Vector2(-28, 22), new Vector2(180, 72), game.CloseInventory);

            var viewportObject = new GameObject("Inventory scroll viewport", typeof(RectTransform),
                typeof(Image), typeof(RectMask2D), typeof(ScrollRect));
            viewportObject.transform.SetParent(inventoryPanel.transform, false);
            var viewportRect = viewportObject.GetComponent<RectTransform>();
            viewportRect.anchorMin = Vector2.zero;
            viewportRect.anchorMax = Vector2.one;
            viewportRect.offsetMin = new Vector2(28, 112);
            viewportRect.offsetMax = new Vector2(-28, -144);
            viewportObject.GetComponent<Image>().color = new Color(0.08f, 0.095f, 0.12f, 0.95f);

            var contentObject = new GameObject("Inventory item list", typeof(RectTransform),
                typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentObject.transform.SetParent(viewportObject.transform, false);
            inventoryContent = contentObject.GetComponent<RectTransform>();
            inventoryContent.anchorMin = new Vector2(0, 1);
            inventoryContent.anchorMax = new Vector2(1, 1);
            inventoryContent.pivot = new Vector2(0.5f, 1);
            inventoryContent.anchoredPosition = Vector2.zero;
            inventoryContent.sizeDelta = Vector2.zero;
            var layout = contentObject.GetComponent<VerticalLayoutGroup>();
            layout.padding = new RectOffset(12, 12, 12, 12);
            layout.spacing = 8;
            layout.childControlWidth = true;
            layout.childControlHeight = true;
            layout.childForceExpandWidth = true;
            layout.childForceExpandHeight = false;
            var fitter = contentObject.GetComponent<ContentSizeFitter>();
            fitter.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
            fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = viewportObject.GetComponent<ScrollRect>();
            scroll.content = inventoryContent;
            scroll.viewport = viewportRect;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            inventoryPanel.SetActive(false);
        }

        private void BuildCredits(Transform parent, GameRuntime game)
        {
            creditsPanel = MakePanel("Audio credits", parent, new Vector2(0.5f, 0.5f),
                new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1260, 650),
                new Color(0.035f, 0.05f, 0.075f, 0.98f));
            MakeText("Credits title", creditsPanel.transform, "ÂM NHẠC, HÌNH ẢNH & HIỆU ỨNG", 34,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(38, -28), new Vector2(1000, 54), new Vector2(0, 1), new Vector2(0, 1));
            var viewportObject = new GameObject("Credits scroll viewport", typeof(RectTransform),
                typeof(Image), typeof(RectMask2D), typeof(ScrollRect));
            viewportObject.transform.SetParent(creditsPanel.transform, false);
            var viewportRect = viewportObject.GetComponent<RectTransform>();
            viewportRect.anchorMin = Vector2.zero;
            viewportRect.anchorMax = Vector2.one;
            viewportRect.offsetMin = new Vector2(28, 104);
            viewportRect.offsetMax = new Vector2(-28, -94);
            viewportObject.GetComponent<Image>().color = new Color(0.08f, 0.095f, 0.12f, 0.95f);

            var contentObject = new GameObject("Credits text content", typeof(RectTransform));
            contentObject.transform.SetParent(viewportObject.transform, false);
            var contentRect = contentObject.GetComponent<RectTransform>();
            contentRect.anchorMin = new Vector2(0, 1);
            contentRect.anchorMax = new Vector2(1, 1);
            contentRect.pivot = new Vector2(0.5f, 1);
            contentRect.anchoredPosition = Vector2.zero;
            contentRect.sizeDelta = new Vector2(0, 1740);

            var credits = MakeText("Audio attribution", contentObject.transform,
                "Nhạc khám phá: “RPG Village Exploration Music” — Hitctrl (OpenGameArt.org), CC BY 3.0.\n" +
                "https://opengameart.org/content/rpgvillageexplorationmusic\n" +
                "https://creativecommons.org/licenses/by/3.0/\n\n" +
                "Nhạc chiến đấu: “Chiptune Battle Music” — pmiller (OpenGameArt.org), CC0.\n" +
                "https://opengameart.org/content/chiptune-battle-music\n\n" +
                "Tranh màn tiêu đề: tác phẩm tạo riêng cho Ashen Oath bằng OpenAI image generation, 2026.\n\n" +
                "Âm thanh môi trường theo vùng: “Park ambiences” — Thimras (OpenGameArt.org), CC0.\n" +
                "https://opengameart.org/content/park-ambiences\n\n" +
                "Hiệu ứng tấn công, va chạm, bước chân và tiền thưởng: RPG Audio — Kenney Vleugels (Kenney.nl), CC0.\n" +
                "https://kenney.nl/assets/rpg-audio\n\n" +
                "Cảnh nền Greenwake Refuge: Sample1.png — Roguelike/RPG pack, Kenney Vleugels (Kenney.nl), CC0.\n" +
                "https://kenney.nl/assets/roguelike-rpg-pack\n\n" +
                "58 quái và sinh vật trong Field Bestiary: Tiny Creatures — Clint Bellanger, CC0; ghi công tùy chọn.\n" +
                "https://opengameart.org/content/tiny-creatures",
                23, Color.white, TextAnchor.UpperLeft, Vector2.zero,
                new Vector2(1170, 1740), new Vector2(0, 1), new Vector2(0, 1));
            credits.horizontalOverflow = HorizontalWrapMode.Wrap;
            credits.verticalOverflow = VerticalWrapMode.Overflow;
            var creditsScroll = viewportObject.GetComponent<ScrollRect>();
            creditsScroll.content = contentRect;
            creditsScroll.viewport = viewportRect;
            creditsScroll.horizontal = false;
            creditsScroll.vertical = true;
            creditsScroll.movementType = ScrollRect.MovementType.Clamped;
            MakeButton("Close credits", creditsPanel.transform, "ĐÓNG", new Vector2(1, 0),
                new Vector2(1, 0), new Vector2(-28, 22), new Vector2(180, 72), game.CloseInventory);
            creditsPanel.SetActive(false);
        }

        private void BuildEnding(Transform parent, GameRuntime game)
        {
            endingPanel = MakePanel("Ending panel", parent, new Vector2(0.5f, 0.5f),
                new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1500, 790),
                new Color(0.025f, 0.035f, 0.06f, 0.985f));
            endingPanel.GetComponent<RectTransform>().pivot = new Vector2(0.5f, 0.5f);
            endingTitleText = MakeText("Ending title", endingPanel.transform, "ASHEN OATH", 42,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleCenter,
                new Vector2(0, -72), new Vector2(1360, 88), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            endingBodyText = MakeText("Ending epilogue", endingPanel.transform, "", 27,
                Color.white, TextAnchor.UpperCenter,
                new Vector2(0, -198), new Vector2(1260, 390), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            MakeButton("Continue after ending", endingPanel.transform, "TIẾP TỤC KHÁM PHÁ", new Vector2(0.5f, 0),
                new Vector2(0.5f, 0), new Vector2(0, 48), new Vector2(310, 82), () =>
                {
                    var action = endingContinue;
                    endingContinue = null;
                    endingPanel.SetActive(false);
                    if (controlsRoot != null) controlsRoot.SetActive(true);
                    action?.Invoke();
                });
            endingPanel.SetActive(false);
        }

        private void BuildQuestJournal(Transform parent, GameRuntime game)
        {
            questJournalPanel = MakePanel("Quest journal window", parent, new Vector2(0.5f, 0.5f),
                new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1480, 850),
                new Color(0.035f, 0.05f, 0.075f, 0.985f));
            questJournalPanel.GetComponent<RectTransform>().pivot = new Vector2(0.5f, 0.5f);
            MakeText("Quest journal title", questJournalPanel.transform, "SỔ HÀNH TRÌNH", 34,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(32, -22), new Vector2(900, 54), new Vector2(0, 1), new Vector2(0, 1));
            MakeText("Quest journal hint", questJournalPanel.transform,
                "Theo dõi tuyến truyện, nhiệm vụ phụ đang làm và việc có thể nhận tại vùng này. Tối đa 3 nhiệm vụ phụ cùng lúc.",
                19, new Color(0.78f, 0.8f, 0.8f), TextAnchor.MiddleLeft,
                new Vector2(34, -76), new Vector2(1320, 34), new Vector2(0, 1), new Vector2(0, 1));
            MakeButton("Close quest journal", questJournalPanel.transform, "ĐÓNG", new Vector2(1, 0),
                new Vector2(1, 0), new Vector2(-28, 20), new Vector2(180, 72), game.CloseInventory);

            var viewportObject = new GameObject("Quest journal scroll viewport", typeof(RectTransform),
                typeof(Image), typeof(RectMask2D), typeof(ScrollRect));
            viewportObject.transform.SetParent(questJournalPanel.transform, false);
            var viewportRect = viewportObject.GetComponent<RectTransform>();
            viewportRect.anchorMin = Vector2.zero;
            viewportRect.anchorMax = Vector2.one;
            viewportRect.offsetMin = new Vector2(28, 112);
            viewportRect.offsetMax = new Vector2(-28, -124);
            viewportObject.GetComponent<Image>().color = new Color(0.08f, 0.095f, 0.12f, 0.95f);

            var contentObject = new GameObject("Quest journal entries", typeof(RectTransform),
                typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentObject.transform.SetParent(viewportObject.transform, false);
            questJournalContent = contentObject.GetComponent<RectTransform>();
            questJournalContent.anchorMin = new Vector2(0, 1);
            questJournalContent.anchorMax = new Vector2(1, 1);
            questJournalContent.pivot = new Vector2(0.5f, 1);
            questJournalContent.anchoredPosition = Vector2.zero;
            questJournalContent.sizeDelta = Vector2.zero;
            var layout = contentObject.GetComponent<VerticalLayoutGroup>();
            layout.padding = new RectOffset(12, 12, 12, 12);
            layout.spacing = 9;
            layout.childControlWidth = true;
            layout.childControlHeight = true;
            layout.childForceExpandWidth = true;
            layout.childForceExpandHeight = false;
            var fitter = contentObject.GetComponent<ContentSizeFitter>();
            fitter.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
            fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = viewportObject.GetComponent<ScrollRect>();
            scroll.content = questJournalContent;
            scroll.viewport = viewportRect;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            questJournalPanel.SetActive(false);
        }

        private void BuildCodex(Transform parent, GameRuntime game)
        {
            codexPanel = MakePanel("Field archive", parent, new Vector2(0.5f, 0.5f),
                new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1480, 850),
                new Color(0.035f, 0.05f, 0.075f, 0.985f));
            codexPanel.GetComponent<RectTransform>().pivot = new Vector2(0.5f, 0.5f);
            MakeText("Field archive title", codexPanel.transform, "SỔ CHỨNG CỨ", 34,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(32, -22), new Vector2(900, 54), new Vector2(0, 1), new Vector2(0, 1));
            MakeText("Field archive hint", codexPanel.transform,
                "Chọn một tư liệu để đọc. Mỗi bản ghi giữ nguồn chứng cứ và phần chưa thể kết luận.",
                19, new Color(0.78f, 0.8f, 0.8f), TextAnchor.MiddleLeft,
                new Vector2(34, -76), new Vector2(1200, 34), new Vector2(0, 1), new Vector2(0, 1));
            MakeButton("Close field archive", codexPanel.transform, "ĐÓNG", new Vector2(1, 1),
                new Vector2(1, 1), new Vector2(-28, -24), new Vector2(180, 64), game.CloseInventory);

            codexListContent = CreateCodexScrollArea("Field archive index", codexPanel.transform,
                new Vector2(28, 112), new Vector2(-1092, -124));
            codexDetailContent = CreateCodexScrollArea("Field archive reader", codexPanel.transform,
                new Vector2(408, 112), new Vector2(-28, -124));
            codexPanel.SetActive(false);
        }

        private RectTransform CreateCodexScrollArea(string name, Transform parent,
            Vector2 offsetMin, Vector2 offsetMax)
        {
            var viewportObject = new GameObject(name + " viewport", typeof(RectTransform),
                typeof(Image), typeof(RectMask2D), typeof(ScrollRect));
            viewportObject.transform.SetParent(parent, false);
            var viewportRect = viewportObject.GetComponent<RectTransform>();
            viewportRect.anchorMin = Vector2.zero;
            viewportRect.anchorMax = Vector2.one;
            viewportRect.offsetMin = offsetMin;
            viewportRect.offsetMax = offsetMax;
            viewportObject.GetComponent<Image>().color = new Color(0.08f, 0.095f, 0.12f, 0.95f);

            var contentObject = new GameObject(name + " content", typeof(RectTransform),
                typeof(VerticalLayoutGroup), typeof(ContentSizeFitter));
            contentObject.transform.SetParent(viewportObject.transform, false);
            var content = contentObject.GetComponent<RectTransform>();
            content.anchorMin = new Vector2(0, 1);
            content.anchorMax = new Vector2(1, 1);
            content.pivot = new Vector2(0.5f, 1);
            content.anchoredPosition = Vector2.zero;
            content.sizeDelta = Vector2.zero;
            var layout = contentObject.GetComponent<VerticalLayoutGroup>();
            layout.padding = new RectOffset(10, 10, 10, 10);
            layout.spacing = 10;
            layout.childControlWidth = true;
            layout.childControlHeight = true;
            layout.childForceExpandWidth = true;
            layout.childForceExpandHeight = false;
            var fitter = contentObject.GetComponent<ContentSizeFitter>();
            fitter.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
            fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var scroll = viewportObject.GetComponent<ScrollRect>();
            scroll.content = content;
            scroll.viewport = viewportRect;
            scroll.horizontal = false;
            scroll.vertical = true;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            return content;
        }

        private GameObject combatPanel;

        public void SetHud(string health, string inventory, string questTitle, string objective, string actionLabel)
        {
            if (healthText != null) healthText.text = health;
            if (inventoryText != null) inventoryText.text = inventory;
            if (questTitleText != null) questTitleText.text = questTitle;
            if (questObjectiveText != null) questObjectiveText.text = objective;
            if (actionText != null) actionText.text = actionLabel;
        }

        public void SetCombat(bool visible, int enemyHealth, string hint = "", string enemyName = "ASH WARG",
            int maxEnemyHealth = 36)
        {
            if (combatPanel == null) return;
            combatPanel.SetActive(visible);
            if (combatText != null)
                combatText.text = enemyName + "  •  MÁU " + Mathf.Max(0, enemyHealth) + " / " +
                                  Mathf.Max(1, maxEnemyHealth) + "\n" + hint;
        }

        public void ShowInventory(System.Collections.Generic.IReadOnlyList<InventoryItemRow> rows,
            string equipmentSummary, Action<string> onEquip)
        {
            equipmentSummaryText.text = equipmentSummary;
            for (var i = inventoryContent.childCount - 1; i >= 0; i--)
                Destroy(inventoryContent.GetChild(i).gameObject);

            if (rows != null)
            {
                foreach (var row in rows)
                {
                    var itemButton = new GameObject("Inventory item", typeof(RectTransform), typeof(Image),
                        typeof(Button), typeof(LayoutElement));
                    itemButton.transform.SetParent(inventoryContent, false);
                    itemButton.GetComponent<LayoutElement>().preferredHeight = 100;
                    itemButton.GetComponent<Image>().color = row.CanEquip
                        ? new Color(0.16f, 0.20f, 0.23f, 1f)
                        : new Color(0.12f, 0.14f, 0.17f, 1f);
                    var button = itemButton.GetComponent<Button>();
                    button.targetGraphic = itemButton.GetComponent<Image>();
                    button.interactable = row.CanEquip;
                    button.onClick.AddListener(() => onEquip?.Invoke(row.ItemId));

                    if (row.Icon != null)
                    {
                        var iconObject = new GameObject("Item pixel icon", typeof(RectTransform), typeof(Image));
                        iconObject.transform.SetParent(itemButton.transform, false);
                        var iconRect = iconObject.GetComponent<RectTransform>();
                        iconRect.anchorMin = new Vector2(0, 0.5f);
                        iconRect.anchorMax = new Vector2(0, 0.5f);
                        iconRect.pivot = new Vector2(0, 0.5f);
                        iconRect.anchoredPosition = new Vector2(18, 0);
                        iconRect.sizeDelta = new Vector2(64, 64);
                        var iconImage = iconObject.GetComponent<Image>();
                        iconImage.sprite = row.Icon;
                        iconImage.preserveAspect = true;
                        iconImage.raycastTarget = false;
                    }

                    var label = MakeText("Item details", itemButton.transform, row.Label, 22,
                        row.CanEquip ? Color.white : new Color(0.79f, 0.8f, 0.79f), TextAnchor.MiddleLeft,
                        Vector2.zero, new Vector2(-32, -12), Vector2.zero, Vector2.one);
                    label.rectTransform.offsetMin = new Vector2(row.Icon == null ? 18 : 96, 12);
                    label.rectTransform.offsetMax = new Vector2(-18, -12);
                    label.raycastTarget = false;
                }
            }

            controlsRoot.SetActive(false);
            questJournalPanel.SetActive(false);
            codexPanel.SetActive(false);
            creditsPanel.SetActive(false);
            inventoryPanel.SetActive(true);
            Canvas.ForceUpdateCanvases();
        }

        public void ShowQuestJournal(System.Collections.Generic.IReadOnlyList<QuestJournalRow> rows,
            Action<string> onAccept)
        {
            for (var i = questJournalContent.childCount - 1; i >= 0; i--)
                Destroy(questJournalContent.GetChild(i).gameObject);

            if (rows == null || rows.Count == 0)
            {
                AddQuestJournalRow("Chưa có nhiệm vụ\nHãy tiếp tục hành trình hoặc khám phá vùng mới để tìm thêm việc cần giúp.",
                    false, null);
            }
            else
            {
                foreach (var row in rows)
                    AddQuestJournalRow(row.Label, row.CanAccept,
                        row.CanAccept ? () => onAccept?.Invoke(row.QuestId) : null);
            }

            controlsRoot.SetActive(false);
            inventoryPanel.SetActive(false);
            codexPanel.SetActive(false);
            creditsPanel.SetActive(false);
            questJournalPanel.SetActive(true);
            Canvas.ForceUpdateCanvases();
        }

        public void ShowCodex(System.Collections.Generic.IReadOnlyList<CodexEntryDefinition> entries)
        {
            if (codexListContent == null || codexDetailContent == null) return;
            ClearChildren(codexListContent);

            if (entries == null || entries.Count == 0)
            {
                var emptyRow = MakeButton("No field records", codexListContent, "Chưa mở được bản ghi",
                    Vector2.zero, Vector2.one, Vector2.zero, Vector2.zero, null);
                var emptyLayout = emptyRow.GetComponent<LayoutElement>() ?? emptyRow.gameObject.AddComponent<LayoutElement>();
                emptyLayout.preferredHeight = 76;
                emptyLayout.minHeight = 76;
                ShowCodexArticle("SỔ CHỨNG CỨ", "FIELD ARCHIVE",
                    "Hoàn tất nhiệm vụ điều tra để mở tư liệu gắn với chứng cứ đã tìm thấy.");
            }
            else
            {
                CodexEntryDefinition first = null;
                foreach (var entry in entries)
                {
                    if (entry == null) continue;
                    if (first == null) first = entry;
                    var selectedEntry = entry;
                    var row = MakeButton("Record: " + selectedEntry.id, codexListContent,
                        selectedEntry.title, Vector2.zero, Vector2.one, Vector2.zero, Vector2.zero,
                        () => ShowCodexArticle(selectedEntry.title,
                            selectedEntry.category + "  ·  " + selectedEntry.writtenBy, selectedEntry.body));
                    var rowLayout = row.GetComponent<LayoutElement>() ?? row.gameObject.AddComponent<LayoutElement>();
                    rowLayout.preferredHeight = 82;
                    rowLayout.minHeight = 82;
                }

                if (first != null)
                    ShowCodexArticle(first.title, first.category + "  ·  " + first.writtenBy, first.body);
            }

            controlsRoot.SetActive(false);
            inventoryPanel.SetActive(false);
            questJournalPanel.SetActive(false);
            creditsPanel.SetActive(false);
            codexPanel.SetActive(true);
            Canvas.ForceUpdateCanvases();
        }

        private static void ClearChildren(Transform parent)
        {
            for (var i = parent.childCount - 1; i >= 0; i--)
                Destroy(parent.GetChild(i).gameObject);
        }

        private void ShowCodexArticle(string title, string attribution, string body)
        {
            ClearChildren(codexDetailContent);
            var article = new GameObject("Field record", typeof(RectTransform), typeof(Image),
                typeof(LayoutElement));
            article.transform.SetParent(codexDetailContent, false);
            article.GetComponent<Image>().color = new Color(0.13f, 0.15f, 0.18f, 1f);
            var articleHeight = Mathf.Max(280f, 150f + (body?.Length ?? 0) * 0.23f);
            article.GetComponent<LayoutElement>().preferredHeight = articleHeight;

            MakeText("Record title", article.transform, title, 24,
                new Color(0.91f, 0.77f, 0.48f), TextAnchor.MiddleLeft,
                new Vector2(18, -14), new Vector2(-36, 38), new Vector2(0, 1), new Vector2(1, 1));
            MakeText("Record attribution", article.transform, attribution, 16,
                new Color(0.67f, 0.76f, 0.78f), TextAnchor.MiddleLeft,
                new Vector2(18, -54), new Vector2(-36, 28), new Vector2(0, 1), new Vector2(1, 1));
            var bodyText = MakeText("Record body", article.transform, body, 19, Color.white,
                TextAnchor.UpperLeft, new Vector2(0, -90), new Vector2(-36, -108), Vector2.zero, Vector2.one);
            bodyText.rectTransform.offsetMin = new Vector2(18, 14);
            bodyText.rectTransform.offsetMax = new Vector2(-18, -94);
            Canvas.ForceUpdateCanvases();
            var readerViewport = codexDetailContent.parent.GetComponent<ScrollRect>();
            if (readerViewport != null) readerViewport.verticalNormalizedPosition = 1;
        }

        private void AddQuestJournalRow(string title, bool canAccept, Action accept)
        {
            var item = new GameObject("Quest journal entry", typeof(RectTransform), typeof(Image),
                typeof(LayoutElement));
            item.transform.SetParent(questJournalContent, false);
            item.GetComponent<LayoutElement>().preferredHeight = 202;
            item.GetComponent<Image>().color = canAccept
                ? new Color(0.14f, 0.2f, 0.21f, 1f)
                : new Color(0.13f, 0.15f, 0.18f, 1f);
            var label = MakeText("Quest details", item.transform, title, 20,
                Color.white, TextAnchor.UpperLeft, Vector2.zero, Vector2.zero, Vector2.zero, Vector2.one);
            label.rectTransform.offsetMin = new Vector2(18, 12);
            label.rectTransform.offsetMax = new Vector2(canAccept ? -174 : -18, -12);
            if (!canAccept) return;

            var button = MakeButton("Accept side quest", item.transform, "NHẬN", new Vector2(1, 0.5f),
                new Vector2(1, 0.5f), new Vector2(-18, 0), new Vector2(138, 62), accept);
            button.GetComponent<RectTransform>().pivot = new Vector2(1, 0.5f);
        }

        public void CloseInventory()
        {
            if (inventoryPanel != null) inventoryPanel.SetActive(false);
            if (questJournalPanel != null) questJournalPanel.SetActive(false);
            if (codexPanel != null) codexPanel.SetActive(false);
            if (creditsPanel != null) creditsPanel.SetActive(false);
            if (controlsRoot != null) controlsRoot.SetActive(true);
        }

        public void ShowCredits()
        {
            if (controlsRoot != null) controlsRoot.SetActive(false);
            if (inventoryPanel != null) inventoryPanel.SetActive(false);
            if (questJournalPanel != null) questJournalPanel.SetActive(false);
            if (codexPanel != null) codexPanel.SetActive(false);
            if (creditsPanel != null) creditsPanel.SetActive(true);
        }

        public void ShowEnding(string title, string body, Action onContinue)
        {
            if (controlsRoot != null) controlsRoot.SetActive(false);
            if (dialoguePanel != null) dialoguePanel.SetActive(false);
            if (inventoryPanel != null) inventoryPanel.SetActive(false);
            if (questJournalPanel != null) questJournalPanel.SetActive(false);
            if (codexPanel != null) codexPanel.SetActive(false);
            if (creditsPanel != null) creditsPanel.SetActive(false);
            endingTitleText.text = title ?? "ASHEN OATH";
            endingBodyText.text = body ?? "";
            endingContinue = onContinue;
            endingPanel.SetActive(true);
        }

        public void ShowLines(string speaker, string[] lines, Action onComplete)
        {
            dialogueLines = lines ?? Array.Empty<string>();
            dialogueIndex = 0;
            dialogueComplete = onComplete;
            choosing = false;
            choiceSelected = null;
            choicesRoot.SetActive(false);
            nextButton.gameObject.SetActive(true);
            controlsRoot.SetActive(false);
            dialoguePanel.SetActive(true);
            speakerText.text = speaker;
            SetDialoguePortrait(speaker);
            if (dialogueLines.Length == 0) AdvanceDialogue();
            else SetDialogueText(dialogueLines[0]);
        }

        public void ShowChoice(string speaker, string prompt,
            System.Collections.Generic.IReadOnlyList<DialogueChoiceOption> options, Action<string> onSelected)
        {
            if (options == null || options.Count < 2 || options.Count > 4) return;
            choosing = true;
            choiceSelected = onSelected;
            speakerText.text = speaker;
            SetDialoguePortrait(speaker);
            dialoguePanel.SetActive(true);
            SetDialogueText(prompt);
            choicesRoot.SetActive(true);
            nextButton.gameObject.SetActive(false);
            controlsRoot.SetActive(false);

            for (var i = choicesRoot.transform.childCount - 1; i >= 0; i--)
                Destroy(choicesRoot.transform.GetChild(i).gameObject);

            const float panelWidth = 1260f;
            const float buttonHeight = 76f;
            const float horizontalGap = 12f;
            const float verticalGap = 8f;
            var columns = Mathf.Min(options.Count, 4);
            var rows = Mathf.CeilToInt(options.Count / (float)columns);
            var panelHeight = rows * buttonHeight + (rows - 1) * verticalGap;
            var rootRect = choicesRoot.GetComponent<RectTransform>();
            rootRect.sizeDelta = new Vector2(panelWidth, panelHeight);
            var buttonWidth = (panelWidth - (columns - 1) * horizontalGap) / columns;

            for (var i = 0; i < options.Count; i++)
            {
                var option = options[i];
                var column = i % columns;
                var row = i / columns;
                var position = new Vector2(column * (buttonWidth + horizontalGap),
                    panelHeight - (row + 1) * buttonHeight - row * verticalGap);
                var button = MakeButton("Choice: " + option.Id, choicesRoot.transform, option.Label,
                    Vector2.zero, Vector2.zero, position, new Vector2(buttonWidth, buttonHeight),
                    () => ChooseOption(option.Id));
                var label = button.GetComponentInChildren<Text>();
                label.fontSize = options.Count >= 4 ? 19 : 22;
            }
        }

        public void CloseDialogue()
        {
            dialoguePanel.SetActive(false);
            choicesRoot.SetActive(false);
            choosing = false;
            controlsRoot.SetActive(true);
        }

        public void SetExploringControls(bool visible) => controlsRoot.SetActive(visible);

        public void SetFishingControls(bool fishing)
        {
            if (actionText != null) actionText.text = fishing ? "DỪNG CÂU" : "TƯƠNG TÁC";
            if (attackText != null) attackText.text = fishing ? "GIẬT CẦN" : "TẤN CÔNG";
        }

        private void AdvanceDialogue()
        {
            if (choosing) return;
            dialogueIndex++;
            if (dialogueLines != null && dialogueIndex < dialogueLines.Length)
            {
                SetDialogueText(dialogueLines[dialogueIndex]);
                return;
            }

            var complete = dialogueComplete;
            dialogueComplete = null;
            CloseDialogue();
            complete?.Invoke();
        }

        private void SetDialogueText(string value)
        {
            if (dialogueText == null) return;
            dialogueText.text = value ?? string.Empty;
            if (dialogueScrollContent == null || dialogueViewportRect == null || dialogueScrollRect == null) return;

            Canvas.ForceUpdateCanvases();
            var viewportHeight = Mathf.Max(1f, dialogueViewportRect.rect.height);
            var textHeight = Mathf.Max(viewportHeight, dialogueText.preferredHeight + 8f);
            dialogueText.rectTransform.sizeDelta = new Vector2(0, textHeight);
            dialogueScrollContent.sizeDelta = new Vector2(0, textHeight);
            Canvas.ForceUpdateCanvases();
            dialogueScrollRect.verticalNormalizedPosition = 1f;
        }

        private void ChooseOption(string optionId)
        {
            var callback = choiceSelected;
            choiceSelected = null;
            CloseDialogue();
            callback?.Invoke(optionId);
        }

        private void SetDialoguePortrait(string speaker)
        {
            var portraitId = ResolveDialoguePortraitId(speaker);
            Sprite portrait = null;
            if (!string.IsNullOrEmpty(portraitId))
            {
                dialoguePortraits.TryGetValue(portraitId, out portrait);
                if (portrait == null)
                {
                    var texture = Resources.Load<Texture2D>("Art/" + portraitId);
                    if (texture != null)
                    {
                        texture.filterMode = FilterMode.Point;
                        texture.wrapMode = TextureWrapMode.Clamp;
                        portrait = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height),
                            new Vector2(0.5f, 0.5f), 100f);
                        dialoguePortraits[portraitId] = portrait;
                    }
                }
            }

            var visible = portrait != null;
            dialoguePortraitFrame.SetActive(visible);
            dialoguePortraitImage.sprite = portrait;
            speakerText.rectTransform.anchoredPosition = new Vector2(visible ? 316 : 42, -27);
            speakerText.rectTransform.sizeDelta = new Vector2(visible ? 1150 : 830, 52);
            dialogueText.rectTransform.anchoredPosition = new Vector2(visible ? 316 : 42, -90);
            dialogueText.rectTransform.sizeDelta = new Vector2(1370, 156);
        }

        private static string ResolveDialoguePortraitId(string speaker)
        {
            switch ((speaker ?? "").Trim().ToUpperInvariant())
            {
                case "ROWAN HALE": return "rowan_hale";
                case "MIRA COLE": return "mira_cole";
                case "ELARA WREN": return "elara_wren";
                case "DR. EVELYN HART": return "evelyn_hart";
                case "JACE MORROW": return "jace_morrow";
                case "NIA PORTER": return "nia_porter";
                case "RUTH CALDER": return "ruth_calder";
                case "MARA BELL": return "mara_bell";
                case "ADA SLOANE": return "ada_sloane";
                default: return "";
            }
        }

        private static void EnsureEventSystem()
        {
            if (EventSystem.current != null) return;
            var eventSystem = new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
            DontDestroyOnLoad(eventSystem);
        }

        private static GameObject MakePanel(string name, Transform parent, Vector2 anchorMin, Vector2 anchorMax,
            Vector2 position, Vector2 size, Color color)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var rect = go.GetComponent<RectTransform>();
            rect.anchorMin = anchorMin;
            rect.anchorMax = anchorMax;
            rect.pivot = new Vector2(0, 1);
            rect.anchoredPosition = position;
            rect.sizeDelta = size;
            go.GetComponent<Image>().color = color;
            return go;
        }

        private static Text MakeText(string name, Transform parent, string value, int size, Color color,
            TextAnchor alignment, Vector2 position, Vector2 dimensions, Vector2 anchorMin, Vector2 anchorMax)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Text));
            go.transform.SetParent(parent, false);
            var rect = go.GetComponent<RectTransform>();
            rect.anchorMin = anchorMin;
            rect.anchorMax = anchorMax;
            var pivotX = anchorMin.x < 0.25f ? 0f : anchorMin.x > 0.75f ? 1f : 0.5f;
            var pivotY = anchorMin.y < 0.25f ? 0f : anchorMin.y > 0.75f ? 1f : 0.5f;
            rect.pivot = new Vector2(pivotX, pivotY);
            rect.anchoredPosition = position;
            rect.sizeDelta = dimensions;
            var text = go.GetComponent<Text>();
            text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            text.text = value;
            text.fontSize = size;
            text.color = color;
            text.alignment = alignment;
            text.horizontalOverflow = HorizontalWrapMode.Wrap;
            text.verticalOverflow = VerticalWrapMode.Overflow;
            text.raycastTarget = false;
            return text;
        }

        private static Button MakeButton(string name, Transform parent, string label, Vector2 anchorMin,
            Vector2 anchorMax, Vector2 position, Vector2 size, Action action)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image), typeof(Button));
            go.transform.SetParent(parent, false);
            var rect = go.GetComponent<RectTransform>();
            rect.anchorMin = anchorMin;
            rect.anchorMax = anchorMax;
            rect.pivot = new Vector2(anchorMin.x < 0.5f ? 0 : 1, anchorMin.y < 0.5f ? 0 : 1);
            rect.anchoredPosition = position;
            rect.sizeDelta = size;
            var image = go.GetComponent<Image>();
            image.color = new Color(0.19f, 0.22f, 0.26f, 0.96f);
            var button = go.GetComponent<Button>();
            button.targetGraphic = image;
            button.onClick.AddListener(() => action?.Invoke());
            var labelText = MakeText("Label", go.transform, label, 23, Color.white, TextAnchor.MiddleCenter,
                Vector2.zero, size - new Vector2(18, 10), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            labelText.rectTransform.pivot = new Vector2(0.5f, 0.5f);
            return button;
        }

        private static void Stretch(RectTransform rect)
        {
            rect.anchorMin = Vector2.zero;
            rect.anchorMax = Vector2.one;
            rect.offsetMin = Vector2.zero;
            rect.offsetMax = Vector2.zero;
        }
    }
}
