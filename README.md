# Nutrireader

Nutrireader is program that will grade the nutritional value of a food based on its ingredients. In addition, it will explain reasons for a grade and offer potential alternatives to the given food. Nutritional information about a food can be automatically filled through scanning a Nutrition Facts label as well.

Users access the program through Python Tkinter GUI. The label scanner is performed through optical character recognition (OCR) from the [Mindee](https://mindee.com/) API. Its OCR algorithms were trained on several images of Nutrition Facts labels. The algorithm for grading food is inspired by that of [Nutri-Score](https://en.wikipedia.org/wiki/Nutri-Score). However, it is modified to produce a grade ranging from 0 to 100. The elaboration for a grade is performed through the [OpenAI](https://platform.openai.com/docs/api-reference) API and uses the GPT-3.5-Turbo model for text generation.

This is our submission for the 2023 Steel City Spring Hackathon. View a demonstration of the project [here](https://youtu.be/dQw4w9WgXcQ).

## License

[MIT](https://choosealicense.com/licenses/mit/)