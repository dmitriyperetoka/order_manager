import os
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase, override_settings
from PIL import Image

from ..models import Ingredient, IngredientInRecipe, Recipe, Tag
from foodgram.settings import BASE_DIR

User = get_user_model()


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'media'))
class RecipeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='someuser')
        self.client.force_login(self.user)

        ingredient_titles = ['Ingredient 1', 'Ingredient 2', 'Ingredient 3']
        ingredient_dimensions = ['g', 'l', 'm']
        ingredients = []
        for title, dimension in zip(ingredient_titles, ingredient_dimensions):
            ingredients.append(Ingredient(title=title, dimension=dimension))
        Ingredient.objects.bulk_create(ingredients)

    def test_form_errors(self):
        initial_recipes_count = Recipe.objects.count()
        initial_iir_count = IngredientInRecipe.objects.count()

        response = self.client.post(
            reverse('recipes:recipe_create'), follow=True)

        fields = [
            'title', 'tags', 'description', 'cooking_time_minutes', 'image']

        for field in fields:
            with self.subTest():
                self.assertFormError(
                    response, 'form', field, 'Обязательное поле.')

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'Нужно выбрать минимум один ингредиент.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={'nameIngredient': ['ingredient 1']}, follow=True)

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'У каждого ингредиента должны быть и название, и количество.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={'valueIngredient': [1]}, follow=True)

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'У каждого ингредиента должны быть и название, и количество.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={
                'nameIngredient': ['Ingredient 1', 'Ingredient 1'],
                'valueIngredient': [1, 2]
            },
            follow=True,
        )

        with self.subTest():
            self.assertFormError(
                response, 'form', None, 'Ингредиенты не должны повторяться.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={
                'nameIngredient': ['Ingredient 1', 'Some other ingredient'],
                'valueIngredient': [1, 2]
            },
            follow=True,
        )

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'В базе данных нет ингредиента "Some other ingredient".')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={
                'nameIngredient': ['Ingredient 1', 'Ingredient 2'],
                'valueIngredient': [1, 0]
            },
            follow=True,
        )

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'Количество ингредиента должно быть '
                'целым положительным числом.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={
                'nameIngredient': ['Ingredient 1', 'Ingredient 2'],
                'valueIngredient': [1, 1.5]
            },
            follow=True,
        )

        with self.subTest():
            self.assertFormError(
                response, 'form', None,
                'Количество ингредиента должно быть '
                'целым положительным числом.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={'cooking_time_minutes': 0}, follow=True)

        with self.subTest():
            self.assertFormError(
                response, 'form', 'cooking_time_minutes',
                'Убедитесь, что это значение больше либо равно 1.')

        response = self.client.post(
            reverse('recipes:recipe_create'),
            data={'cooking_time_minutes': 1.5}, follow=True)

        with self.subTest():
            self.assertFormError(
                response, 'form', 'cooking_time_minutes',
                'Введите целое число.')

        with self.subTest():
            self.assertEqual(Recipe.objects.count(), initial_recipes_count)

        with self.subTest():
            self.assertEqual(
                IngredientInRecipe.objects.count(), initial_iir_count)

    def test_create_recipe(self):
        fd, path = tempfile.mkstemp(suffix='.jpg')
        Image.new("RGB", (1, 1), "#000").save(path)
        with open(path, 'rb') as file:
            image = SimpleUploadedFile(
                path, file.read(), content_type='image/jpeg')

        tag_titles = ['Завтрак', 'Обед', 'Ужин']
        tag_slugs = ['breakfast', 'lunch', 'dinner']
        tags = []
        for title, slug in zip(tag_titles, tag_slugs):
            tags.append(Tag(title=title, slug=slug))
        Tag.objects.bulk_create(tags)

        all_tags = [tag.slug for tag in Tag.objects.all()]
        all_ingredients = [
            ingredient.title for ingredient in Ingredient.objects.all()]

        form_data = {
            'title': 'Some Title',
            'tags': all_tags,
            'description': 'Some description.',
            'cooking_time_minutes': 50,
            'image': image,
            'nameIngredient': all_ingredients,
            'valueIngredient': [1, 2, 3]
        }
        initial_recipes_count = Recipe.objects.count()
        initial_iir_count = IngredientInRecipe.objects.count()

        self.client.post(reverse('recipes:recipe_create'), data=form_data)
        with self.subTest():
            self.assertEqual(Recipe.objects.count(), initial_recipes_count + 1)
        with self.subTest():
            self.assertEqual(
                IngredientInRecipe.objects.count(),
                initial_iir_count + len(form_data['valueIngredient']))

        os.close(fd)
        os.remove(path)
