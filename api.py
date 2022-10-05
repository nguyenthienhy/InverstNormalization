from flask import Flask, request, jsonify
import time
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

app = Flask(__name__)

inverse_normalizer = InverseNormalizer(lang='vi', cache_dir="fst_model", overwrite_cache=False)

@app.route('/normText', methods=['POST'])
def norm_text():
    data = request.form['text']
    start = time.time()
    text_normed = inverse_normalizer.inverse_normalize(data, verbose=False)
    return jsonify({"text": data, "text_normed": text_normed, "timeProcessed": str(time.time() - start) + "s"})

if __name__ == '__main__':
    app.run(host="localhost", port=9999, use_reloader=True)