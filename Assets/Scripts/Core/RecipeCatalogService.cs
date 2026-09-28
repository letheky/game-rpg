using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace AshenOath.Core
{
    [Serializable]
    public sealed class RecipeCatalogData
    {
        public int schemaVersion;
        public List<RecipeDefinition> entries;
    }

    [Serializable]
    public sealed class RecipeDefinition
    {
        public string id;
        public string displayName;
        public string stationId;
        public string discipline;
        public string outputItemId;
        public int outputQuantity;
        public List<RecipeIngredient> ingredients;
    }

    [Serializable]
    public sealed class RecipeIngredient
    {
        public string itemId;
        public int quantity;
    }

    public static class RecipeCatalogService
    {
        public static RecipeCatalogData Load()
        {
            var asset = Resources.Load<TextAsset>("Content/recipe_catalog");
            if (asset == null)
            {
                Debug.LogError("Missing Resources/Content/recipe_catalog.json.");
                return null;
            }

            try
            {
                var catalog = JsonUtility.FromJson<RecipeCatalogData>(asset.text);
                Validate(catalog);
                return catalog;
            }
            catch (Exception exception)
            {
                Debug.LogError("Could not load recipe catalog: " + exception.Message);
                return null;
            }
        }

        public static RecipeDefinition FindById(RecipeCatalogData catalog, string recipeId)
        {
            if (catalog?.entries == null || string.IsNullOrEmpty(recipeId)) return null;
            foreach (var recipe in catalog.entries)
                if (recipe != null && recipe.id == recipeId) return recipe;
            return null;
        }

        public static List<RecipeDefinition> FindForStation(RecipeCatalogData catalog, string stationId)
        {
            var recipes = new List<RecipeDefinition>();
            if (catalog?.entries == null || string.IsNullOrEmpty(stationId)) return recipes;
            foreach (var recipe in catalog.entries)
                if (recipe != null && recipe.stationId == stationId) recipes.Add(recipe);
            return recipes;
        }

        public static void Validate(RecipeCatalogData catalog)
        {
            if (catalog == null || catalog.schemaVersion != 1 || catalog.entries == null || catalog.entries.Count == 0)
                throw new FormatException("Recipe catalog schema or entries are invalid.");

            var ids = new HashSet<string>();
            foreach (var recipe in catalog.entries)
            {
                if (recipe == null || !IsStableId(recipe.id) || !ids.Add(recipe.id) ||
                    string.IsNullOrWhiteSpace(recipe.displayName) || !IsStableId(recipe.stationId) ||
                    (recipe.discipline != "alchemy" && recipe.discipline != "smithing" &&
                     recipe.discipline != "cooking") ||
                    !IsStableId(recipe.outputItemId) || recipe.outputQuantity < 1 ||
                    recipe.ingredients == null || recipe.ingredients.Count < 1 || recipe.ingredients.Count > 4)
                    throw new FormatException("Invalid recipe definition or duplicate ID.");

                var ingredientIds = new HashSet<string>();
                foreach (var ingredient in recipe.ingredients)
                    if (ingredient == null || !IsStableId(ingredient.itemId) || !ingredientIds.Add(ingredient.itemId) ||
                        ingredient.quantity < 1)
                        throw new FormatException("Invalid ingredient contract on " + recipe.id + ".");
            }
        }

        private static bool IsStableId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 64 || value[0] < 'a' || value[0] > 'z') return false;
            foreach (var character in value)
                if (!((character >= 'a' && character <= 'z') || (character >= '0' && character <= '9') || character == '_'))
                    return false;
            return true;
        }
    }

    public static class CraftingService
    {
        public static bool TryCraft(GameSaveData save, RecipeCatalogData catalog, string recipeId, string stationId,
            out RecipeDefinition craftedRecipe, out string missingItemId)
        {
            craftedRecipe = RecipeCatalogService.FindById(catalog, recipeId);
            missingItemId = "";
            if (save == null || craftedRecipe == null || craftedRecipe.stationId != stationId || save.inventory == null ||
                ItemCatalog.Find(craftedRecipe.outputItemId) == null)
                return false;

            foreach (var ingredient in craftedRecipe.ingredients)
            {
                if (InventoryService.Count(save, ingredient.itemId) >= ingredient.quantity) continue;
                missingItemId = ingredient.itemId;
                return false;
            }

            var removedCount = 0;
            foreach (var ingredient in craftedRecipe.ingredients)
            {
                if (!InventoryService.Remove(save, ingredient.itemId, ingredient.quantity))
                {
                    for (var i = 0; i < removedCount; i++)
                        InventoryService.Add(save, craftedRecipe.ingredients[i].itemId,
                            craftedRecipe.ingredients[i].quantity);
                    return false;
                }
                removedCount++;
            }

            if (InventoryService.Add(save, craftedRecipe.outputItemId, craftedRecipe.outputQuantity) ==
                craftedRecipe.outputQuantity) return true;

            foreach (var ingredient in craftedRecipe.ingredients)
                InventoryService.Add(save, ingredient.itemId, ingredient.quantity);
            missingItemId = craftedRecipe.outputItemId;
            return false;
        }

        public static string DescribeIngredients(RecipeDefinition recipe)
        {
            if (recipe?.ingredients == null) return "";
            var builder = new StringBuilder();
            for (var i = 0; i < recipe.ingredients.Count; i++)
            {
                var ingredient = recipe.ingredients[i];
                var definition = ItemCatalog.Find(ingredient.itemId);
                if (i > 0) builder.Append(" + ");
                builder.Append(ingredient.quantity).Append(' ')
                    .Append(definition == null ? ingredient.itemId : definition.name);
            }
            return builder.ToString();
        }
    }
}
