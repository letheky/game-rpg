using UnityEditor;
using UnityEngine;

namespace AshenOath.Editor
{
    /// <summary>Keeps derived CC0 VFX masks crisp and small when imported into Unity.</summary>
    public sealed class PixelVfxTextureImporter : AssetPostprocessor
    {
        private void OnPreprocessTexture()
        {
            if (!assetPath.StartsWith("Assets/Resources/VFX/")) return;

            var importer = (TextureImporter)assetImporter;
            importer.textureType = TextureImporterType.Default;
            importer.mipmapEnabled = false;
            importer.filterMode = FilterMode.Point;
            importer.wrapMode = TextureWrapMode.Clamp;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.maxTextureSize = 128;
            importer.alphaIsTransparency = true;
        }
    }
}
