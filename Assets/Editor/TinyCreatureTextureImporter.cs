using UnityEditor;
using UnityEngine;

namespace AshenOath.Editor
{
    /// <summary>Keeps imported CC0 creature families crisp at their authored pixel scales.</summary>
    public sealed class TinyCreatureTextureImporter : AssetPostprocessor
    {
        private void OnPreprocessTexture()
        {
            var tinyCreature = assetPath.Contains("/Resources/Art/tiny_");
            var verdantCreature = assetPath.Contains("/Resources/Art/verdant_");
            var crawlCreature = assetPath.Contains("/Resources/Art/crawl_");
            if (!tinyCreature && !verdantCreature && !crawlCreature) return;
            var importer = (TextureImporter)assetImporter;
            importer.textureType = TextureImporterType.Default;
            importer.mipmapEnabled = false;
            importer.filterMode = FilterMode.Point;
            importer.wrapMode = TextureWrapMode.Clamp;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.maxTextureSize = verdantCreature || crawlCreature ? 32 : 16;
            importer.alphaIsTransparency = true;
        }
    }
}
