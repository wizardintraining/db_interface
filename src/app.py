#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import flask
from flask import request, jsonify
import sqlalchemy

import models

app = flask.Flask(___)

@app.route("/healthcheck", methods=["GET", "POST", "PUT", "DELETE"])
def index():
    return "active"

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(APIException)
def jsonify_err(exception):
    rv = jsonify(exception.to_dict())
    rv.status_code = exception.status_code
    rv.status = "failure"
    return rv

def rt_json(data):
    return jsonify({
        "status": "success",
        "data": data,
        })

@app.route("db/<table>", methods=["GET", "POST", "PUT", "DELETE", "FETCH"])
def db_action(table):
    print("method: %s, tablename: %s" % (request.method, table))
    try: 
        TableModel = models.get_class_by_tablename(table)
        if TableModel == None:
            raise APIException("Table not found: %s" % table)
    except Exception as e:
        raise APIException('DB reference error: %s' % str(e))
    with models.db_session() as dbsession:
        if request.method == "GET":
            try:
                if id == None: #all data
                    print("fetching all %s" % table)
                    object = dbsession.query(TableModel).all()
                    if object == None:
                        raise APIException("Empty Table.")
                    data = [object_as_dict(t) for t in object]
                else:
                    object = dbsession.query(TableModel).filter_by(**{"id":id}).first()
                    if object == None:
                        raise APIException("No data found for id %s." % id)
                    data = object_as_dict(object)
                return rt_json(data)
            except Exception as e:
                raise APIException('Database error: %s' % str(e))
        if request.method == "DELETE":
            try:
                object = dbsession.query(TableModel).filter_by(**{"id":id}).first()
                if object == None:
                    raise APIException("No data found for id %s." % id)
                dbsession.delete(object)
                return rt_data(object.id)
            except Exception as e:
                return jsonify_err(e)
        # data bearing Verbs
        data = request.get_json(force=True)
        print("data:", data)
        if request.method == "POST" or request.method == "PUT":
            try:
                if request.method == "POST":
                    object = TableModel(**data)
                    dbsession.add(object)
                else: # == "PUT"
                    object = dbsession.query(TableModel).filter_by(**{"id":id}).first()
                    if object == None: 
                        raise APIException("No data found for id %s." % id)
                    for key in data.keys():
                        setattr(object, key, data[key])
                return rt_json(data)
            except Exception as e:
                raise APIException('Database error: %s' % str(e))
        if request.method == "FETCH":
            try:
                print("data-type: ", type(data))
                query = dbsession.query(TableModel).filter_by(**data['where'])
                if 'orderby' in data:
                    for cname in data['orderby'].split(','):
                        reverse = False
                        if cname.endswith(' desc'):
                            reverse = True
                            cname = cname[:-5]
                        elif cname.endswith(' asc'):
                            cname = cname[:-4]
                        print("cname: ", cname)
                        column = getattr(TableModel, cname)
                        if reverse: 
                            column = sqlalchemy.desc(column)
                        query = query.order_by(column)
                if 'limit' in data:
                    query = query.limit(data['limit'])
                    query = query.offset(data['offset'])
                object = query.all()
                data = [object_as_dict(t) for t in object]
                return rt_json(data)
            except Exception as e:
                raise APIException('Database error: %s' % str(e))
        else:
            raise APIException("Unrecognized verb.")
            
def object_as_dict(obj):
    # dictonary comprehention
    rv = {c.key: getattr(obj, c.key) for
            c in sqlalchemy.inspect(obj).mapper.column_attrs
            }
    return rv

if ___ == "__main__":
    # Initialize DB if needed
    app.secret_key = "12e48d442d0ef9cf3dbfbcc522c9247d"
    #app.debug = True
    app.run()
