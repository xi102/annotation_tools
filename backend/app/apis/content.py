from flask import request, jsonify

from app.apis import api
from app.models.content import Content


@api.route('/getContent', methods=['GET', 'POST'])
def get_content():
    this_id = request.json.get("fileId")
    result = Content.query.filter_by(id=this_id).first()
    # return jsonify({'result': str(result.chief_complaint), 'fileId': result.id})
    return jsonify({'result': str(result.medical_treatment), 'fileId': result.id})
