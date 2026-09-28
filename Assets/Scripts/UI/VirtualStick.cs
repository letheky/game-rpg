using UnityEngine;
using UnityEngine.EventSystems;

namespace AshenOath.UI
{
    public sealed class VirtualStick : MonoBehaviour, IPointerDownHandler, IDragHandler, IPointerUpHandler
    {
        [SerializeField] private RectTransform knob;
        private RectTransform bounds;
        public Vector2 Value { get; private set; }

        public void Initialize(RectTransform stickBounds, RectTransform stickKnob)
        {
            bounds = stickBounds;
            knob = stickKnob;
        }

        public void OnPointerDown(PointerEventData eventData) => UpdateValue(eventData);
        public void OnDrag(PointerEventData eventData) => UpdateValue(eventData);

        public void OnPointerUp(PointerEventData eventData)
        {
            Value = Vector2.zero;
            if (knob != null) knob.anchoredPosition = Vector2.zero;
        }

        private void UpdateValue(PointerEventData eventData)
        {
            if (bounds == null || knob == null) return;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(bounds, eventData.position,
                    eventData.pressEventCamera, out var localPoint)) return;

            var radius = Mathf.Min(bounds.rect.width, bounds.rect.height) * 0.34f;
            var offset = Vector2.ClampMagnitude(localPoint, radius);
            Value = radius > 0 ? offset / radius : Vector2.zero;
            knob.anchoredPosition = offset;
        }
    }
}
