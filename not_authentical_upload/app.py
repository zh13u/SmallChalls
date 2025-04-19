from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, make_response
import os
import aiohttp
import asyncio
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

upload_images = {}

upload_folder = './uploads'
os.makedirs(upload_folder, exist_ok=True)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
async def upload_file():

    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    image_id = str(uuid.uuid4())
    upload_images[image_id] = filename

    return redirect(url_for('process_image', id=image_id))

@app.route('/process', methods=['GET', 'POST'])
async def process_image():

    image_id = request.args.get('id')
    if not image_id or image_id not in upload_images:
        error = "Image ID is invalid or missing."
        return render_template('process.html', error=error)

    image_url = url_for('get_uploaded_file', image_id=image_id)

    if request.method == 'POST':
        image_url_file = request.form.get('image_url_file', '')
        if image_url_file:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url_file) as response:
                        content_type = response.headers.get('Content-Type', '')
                        content_length = response.headers.get('Content-Length', 'Unknown')
                        status_code = response.status

                        file_metadata = {
                            "URL": image_url_file,
                            "Content-Type": content_type,
                            "Content-Length": content_length,
                            "Status": status_code
                        }

                        if "application/json" in content_type:
                            try:
                                json_data = await response.json()
                                resp = make_response(jsonify({
                                    "status": "success",
                                    "message": "JSON content retrieved successfully.",
                                    "metadata": file_metadata,
                                    "data": json_data
                                }))
                                resp.headers['Access-Control-Allow-Origin'] = request.host_url
                                return resp
                            except Exception as e:
                                return render_template('process.html', error=f"Failed to parse JSON: {str(e)}", image_url=image_url)

                        elif "text/html" in content_type:
                            html_data = await response.text()
                            resp = make_response(jsonify({
                                "status": "success",
                                "message": "HTML content retrieved successfully.",
                                "metadata": file_metadata,
                                "html_content": html_data
                            }))
                            resp.headers['Access-Control-Allow-Origin'] = request.host_url
                            return resp
                        elif content_type == "text/html":
                            dummy_data = {
                                "status": "success",
                                "message": "This is JSON data returned when Content-Type is text/html.",
                                "data": {
                                    "key1": "value1",
                                    "key2": "value2"
                                }
                            }
                            return jsonify(dummy_data)
                        else:
                            return render_template(
                                'process.html',
                                error="Unsupported Content-Type.",
                                image_url=image_url
                            )
            except Exception as e:
                return render_template('process.html', error=f"Failed to fetch the resource: {str(e)}", image_url=image_url)

    return render_template('process.html', image_url=image_url, image_id=image_id)

@app.route('/uploads/<image_id>')
def get_uploaded_file(image_id):

    if image_id not in upload_images:
        return "File not found!", 404

    filename = upload_images[image_id]
    return send_from_directory(upload_folder, filename)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4505)
