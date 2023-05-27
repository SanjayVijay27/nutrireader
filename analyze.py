import openai
import os
from dotenv import load_dotenv

#Load .env
load_dotenv()
openai.api_key = os.getenv("GPT_KEY")

def get_info(serv_size, cals, sat_fat, sodium, fiber, sugar, protein, beverage):
    #Get preliminary subscore for each food item
    features = {}
    
    if beverage:
        #Convert ingredients into unit per hundred milliliters and divide by constant
        features["energy_density"] = cals / serv_size * 100 / 7.15    #kilocalories
        features["sugar"] = sugar / serv_size * 100 / 1.5   #grams
    else:
        #Convert ingredients into unit per hundred grams and divide by constant
        features["energy_density"] = cals / serv_size * 100 / 80    #kilocalories
        features["sugar"] = sugar / serv_size * 100 / 4.5   #grams

    #Constant is the same for beverages and non-beverages
    features["sat_fat"] = sat_fat / serv_size * 100 #grams
    features["salt"] = sodium / serv_size * 100 / 90    #grams

    features["fiber"] = fiber / serv_size * 100 / 0.7   #grams
    features["protein"] = protein / serv_size * 100 / 1.6   #grams

    #Cap subscores to maximum values
    for key in features:
        if key in ["fiber", "protein"]:
            if features[key] > 5:
                features[key] = 5
        else:
            print("cap")
            if features[key] > 10:
                features[key] = 10
    
    #Calculate final nutrition score
    nutrition_score = int(((features["fiber"] + features["protein"] - features["energy_density"] - features["sugar"] - features["sat_fat"] - features["salt"]) + 40) * 2)

    #Build and submit prompt to OpenAI
    message = "Explain the nutrition information of a food item with a score of " + str(nutrition_score) + "/100 which has "  + str(cals) + " calories, "  + str(sat_fat) + " grams of saturated fat, " + str(sodium) + " milligrams of sodium, "  + str(fiber) + " grams of fiber, " + str(sugar) + " grams of sugar, and " + str(protein) + " grams of protein in a " + str(serv_size) + " gram serving. Briefly explain potential alternatives."
    output = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
    
    #Return score and message result
    return nutrition_score, output.choices[0].message.content