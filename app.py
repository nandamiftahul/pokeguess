from flask import Flask, render_template, jsonify, url_for
import random
import os
from gtts import gTTS

app = Flask(__name__)

# Text file listing Pokémon images
LIST_PATH = os.path.join(os.path.dirname(__file__), "name_pokemon.txt")

with open(LIST_PATH, "r") as f:
    POKEMON_LIST = [line.strip() for line in f if line.strip().endswith(".png")]

# Folder to store generated sounds
SOUNDS_DIR = os.path.join("static", "sounds")
os.makedirs(SOUNDS_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_random_pokemon")
def get_random_pokemon():
    pokemon_file = random.choice(POKEMON_LIST)
    pokemon_name = os.path.splitext(pokemon_file)[0].capitalize()

    image_path = url_for("static", filename=f"images/{pokemon_file}")
    sound_filename = f"{pokemon_name.lower()}.mp3"
    sound_path = os.path.join(SOUNDS_DIR, sound_filename)

    # Generate the sound if it doesn’t exist
    if not os.path.exists(sound_path):
        tts = gTTS(text=f"It's {pokemon_name}!", lang="en", slow=True)
        tts.save(sound_path)

    sound_url = url_for("static", filename=f"sounds/{sound_filename}")

    return jsonify({"name": pokemon_name, "image": image_path, "sound": sound_url})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
