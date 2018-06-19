from uuid import uuid4
from flask_login import login_required

from flask import (
    make_response,
    abort
)

from stock_app import db
from stock_app.models import Item


@login_required
def read_all(length=None, offset=0):
    return [{
        "vendor_code": item.vendor_code,
        "uuid": item.uuid,
    } for item in Item.query.all()]


@login_required
def read_one(uuid):
    item = Item.query.filter_by(uuid=uuid).first()
    if not item:
        abort(404, 'Item with UUID {uuid} not found'.format(
            uuid=uuid))
    return {
        "vendor_code": item.vendor_code,
        "uuid": item.uuid,
    }


@login_required
def create(item):
    vendor_code = item.get('vendor_code', None)
    if not Item.query.filter_by(vendor_code=vendor_code).first():
        uuid = str(uuid4())
        add_item = Item(
            uuid=uuid,
            vendor_code=vendor_code,
        )
        db.session.add(add_item)
        db.session.commit()
        item = Item.query.filter_by(uuid=uuid).first()
        return {
            "vendor_code": item.vendor_code,
            "uuid": item.uuid,
        }, 201
    else:
        abort(406, 'Item with vendor code {vendor_code} already exists'.format(
            vendor_code=vendor_code))


@login_required
def update(uuid, item):
    update_item = Item.query.filter_by(uuid=uuid).first()
    if update_item:
        update_item.vendor_code = item.get('vendor_code')
        db.session.commit()
        item = Item.query.filter_by(uuid=uuid).first()
        return {
            "vendor_code": item.vendor_code,
            "uuid": item.uuid,
        }
    else:
        abort(404, 'Item with UUID {uuid} not found'.format(
            uuid=uuid))


@login_required
def delete(uuid):
    item = Item.query.filter_by(uuid=uuid).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return make_response('{uuid} successfully deleted'.format(
            uuid=uuid), 200)
    else:
        abort(404, 'Item with UUID {uuid} not found'.format(
            uuid=uuid))
