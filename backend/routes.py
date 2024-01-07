from pydoc import describe
from . import app
import os
import json
from flask import Flask, jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture)
    else:
        return jsonify({"Error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():

    # get data from the json body
    picture_in = request.json
    print(picture_in)

    # if the id is already there, return 303 with the URL for the resource
    for picture in data:
        if picture_in["id"] == picture["id"]:
            return {
                "Message": f"picture with id {picture_in['id']} already present"
            }, 302

    data.append(picture_in)
    return picture_in, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_to_update = next((item for item in data if item["id"] == id), None)
    if picture_to_update:
        request_data = request.get_json()
        
        if not request_data or 'pic_url' not in request_data:
            abort(400, description = "Missing picture url")
        
        picture_to_update["pic_url"] = request_data["pic_url"]
        picture_to_update["event_country"] = request_data.get("event_country", "")
        picture_to_update["event_state"] = request_data.get("event_state", "")
        picture_to_update["event_city"] = request_data.get("event_city", "")
        picture_to_update["event_date"] = request_data.get("event_date", "")

        return jsonify(picture_to_update), 200
    else:
        return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
        else:
            return jsonify({"message": "picture not found"}), 404