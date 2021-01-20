import time
from operator import itemgetter

from flask import request, jsonify

from app import db
from app.apis import api
from app.models.entity import Entity
from app.models.user import User


@api.route('/getEntity', methods=['POST'])
def get_entity():
    thisId = request.json.get("fileId")
    editUser = request.json.get("editUser")
    is_user_exist = User.query.filter_by(username=editUser).first()
    results = Entity.query.filter_by(content_id=thisId, editUser=editUser).all()
    if editUser is None or is_user_exist is None:
        return jsonify({
            "flag": 0,
            "errorText": "用户名不合法"
        })
    if results is None:
        return jsonify({
            "flag": 0,
            "errorText": "未添加实体或该条病历不存在"
        })
    entityList = [''] * len(results)
    n = 0
    for result in results:
        # 生成实体json数据
        entityList[n] = {
            "name": result.mention,
            "startPosition": int(result.pos_b),
            "endPosition": result.pos_e,
            "category": result.category,
            "decoration": result.decoration
        }
        n = n + 1
    entityList = sorted(entityList, key=itemgetter("startPosition"), reverse=False)
    return jsonify({
        "flag": 1,
        "entityList": entityList
    })


@api.route('/', methods=['GET', 'POST'])
def entity_edit():
    content_id = request.json.get('fileId')
    edit_user = request.json.get('editUser')
    entityRemove = request.json.get('entityRemove')
    for entity in entityRemove:
        mention = entity["name"]
        pos_b = entity["startPosition"]
        result = Entity.query.filter_by(content_id=content_id, editUser=edit_user, mention=mention,
                                        pos_b=pos_b).first()
        if result is not None:
            db.session.delete(result)
            db.session.commit()
    for entity in request.json.get('entities'):
        mention = entity['name']
        pos_b = entity['startPosition']
        pos_e = entity['endPosition']
        category = entity['category']
        decoration = entity['decoration']
        result = Entity.query.filter_by(editUser=edit_user, content_id=content_id, mention=mention,
                                        pos_b=pos_b).all()
        if mention is None or category is None or pos_b is None or pos_e is None:
            return jsonify({
                "flag": 0,
                "errorText": "实体格式不合要求"
            })
        if len(result) == 0:
            # 新建实体
            newEntity = Entity(mention=mention)
            newEntity.pos_b = pos_b
            newEntity.pos_e = pos_e
            newEntity.category = category
            newEntity.decoration = decoration
            newEntity.content_id = content_id
            newEntity.editUser = edit_user
            newEntity.editTime = int(round(time.time() * 1000))
            db.session.add(newEntity)
            db.session.commit()
        else:
            # 修改实体
            result[0].category = category
            result[0].decoration = decoration
            result[0].pos_e = pos_e
            result[0].pos_b = pos_b
            result[0].mention = mention
            result[0].edit_user = edit_user
            result[0].editTime = int(round(time.time() * 1000))
    return jsonify({'flag': 1})


@api.route('/refreshEntityList', methods=["POST"])
def refreshEntityList():
    content_id = request.json.get('fileId')
    edit_user = request.json.get('editUser')
    result = Entity.query.filter_by(content_id=content_id, editUser=edit_user).all()
    # print(result)
    for x in result:
        db.session.delete(x)
    for entity in request.json.get('entities'):
        mention = entity['name']
        pos_b = entity['startPosition']
        pos_e = entity['endPosition']
        category = entity['category']
        decoration = entity['decoration']
        if mention is None or category is None or pos_b is None or pos_e is None:
            return jsonify({
                "flag": 0,
                "errorText": "实体格式不合要求"
            })
        # 新建实体
        newEntity = Entity(mention=mention)
        newEntity.pos_b = pos_b
        newEntity.pos_e = pos_e
        newEntity.category = category
        newEntity.decoration = decoration
        newEntity.content_id = content_id
        newEntity.editUser = edit_user
        newEntity.editTime = int(round(time.time() * 1000))
        db.session.add(newEntity)
        db.session.commit()
    return jsonify({'flag': 1})


@api.route('/reviewEntity', methods=['POST'])
def reviewEntity():
    thisId = request.json.get("content_id")
    # print(thisId)
    results = Entity.query.filter(Entity.content_id == thisId, Entity.editUser != "admin").all()
    entityList = [''] * len(results)
    n = 0
    for result in results:
        # 生成实体json数据
        entityList[n] = {
            "name": result.mention,
            "startPosition": int(result.pos_b),
            "endPosition": result.pos_e,
            "category": result.category,
            "decoration": result.decoration
        }
        n = n + 1
    a = {}
    entities = []
    for x in entityList:
        if x not in entities:
            entities.append(x)
    # print(entities)
    for i in range(0, len(entities)):
        a[i] = entityList.count(entities[i])
    for i in range(0, len(entities)):
        entities[i]["nums"] = a[i]
    final_entities = []
    entities_confirmed = []
    for i in range(0, len(entities)):
        if entities[i]["nums"] != 3:
            final_entities.append(entities[i])
        else:
            entities_confirmed.append(entities[i])
    final_entities.sort(key=itemgetter("startPosition"), reverse=False)
    return jsonify({
        "flag": 1,
        "entityList": final_entities,
        "entities_confirmed": entities_confirmed
    })
