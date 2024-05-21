import logging
import os.path
import subprocess
import uuid

from flask import Flask, request, make_response, send_file

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

app = Flask(__name__)


@app.route("/video/swap-face", methods=["POST"])
def video_swap_face():
	source_file_name = f"{uuid.uuid4().hex}.jpg"
	target_file_name = f"{uuid.uuid4().hex}.mp4"
	result_file_name = f"{uuid.uuid4().hex}.mp4"

	try:
		source_file = request.files["source"]
		source_file.save(source_file_name)

		target_file = request.files["target"]
		target_file.save(target_file_name)

		commands = ['python3', 'run.py',
					'--frame-processors', 'face_swapper',
					'-s', source_file_name,
					'-t', target_file_name,
					'-o', result_file_name,
					'--headless']
		run = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		if run.returncode != 0:
			return make_response({
				'succeed': False,
				"message": "Server Internal Error"
			}, 500)
		return send_file(result_file_name, mimetype='video/mp4')
	finally:
		if os.path.exists(source_file_name):
			os.remove(source_file_name)
		if os.path.exists(target_file_name):
			os.remove(target_file_name)
		if os.path.exists(result_file_name):
			os.remove(result_file_name)
		logging.info("remove all")


@app.route("/image/swap-face", methods=["POST"])
def image_swap_face():
	source_file_name = f"{uuid.uuid4().hex}.jpg"
	target_file_name = f"{uuid.uuid4().hex}.jpg"
	result_file_name = f"{uuid.uuid4().hex}.jpg"

	try:
		source_file = request.files["source"]
		source_file.save(source_file_name)

		target_file = request.files["target"]
		target_file.save(target_file_name)

		commands = ['python3', 'run.py',
					'--frame-processors', 'face_swapper',
					'-s', source_file_name,
					'-t', target_file_name,
					'-o', result_file_name,
					'--headless']
		run = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		if run.returncode != 0:
			return make_response({
				'succeed': False,
				"message": "Server Internal Error"
			}, 500)
		return send_file(result_file_name, mimetype='image/jpg')
	finally:
		if os.path.exists(source_file_name):
			os.remove(source_file_name)
		if os.path.exists(target_file_name):
			os.remove(target_file_name)
		if os.path.exists(result_file_name):
			os.remove(result_file_name)
		logging.info("remove all")


@app.route("/health", methods=["GET"])
def health():
	return {
		"status": 1
	}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
