# Nutrireader

Nutrireader is program that will grade the nutritional value of a food based on its ingredients. In addition, it will explain reasons for a grade and offer potential alternatives to the given food. Nutritional information about a food can be automatically filled through scanning a Nutrition Facts label as well.

Users access the program through Python Tkinter GUI. The label scanner is performed through optical character recognition (OCR) from the [Mindee](https://mindee.com/) API. Its OCR algorithms were trained on several images of Nutrition Facts labels. The algorithm for grading food is inspired by that of [Nutri-Score](https://en.wikipedia.org/wiki/Nutri-Score). However, it is modified to produce a grade ranging from 0 to 100. The elaboration for a grade is performed through the [OpenAI](https://platform.openai.com/docs/api-reference) API and uses the GPT-3.5-Turbo model for text generation.

This is our submission for the 2023 Steel City Spring Hackathon. View a demonstration of the project [here](https://youtu.be/N12WAx2Q-94).

## Try it Out

Clone the repository with the following terminal command:
```
git clone https://github.com/SanjayVijay27/nutrireader.git
```

Create a virtual environment and install requirements on it:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a .env file and assign your OpenAI API key to GPT_KEY:
```
GPT_KEY="[API Key]"
```
Unfortunately, we will not be sharing our Mindee API key, so you will have to run the program without the OCR. Comment out lines 16-19 of analyze.py.

Install all files under Satoshi_Complete\Fonts\OTF in order to use the Satoshi font.

Running the program should now open the Nutrireader window. The demonstration video covers its functionality.

## License

[MIT](https://choosealicense.com/licenses/mit/)