from collections import OrderedDict
import logging

from flask import (
    Blueprint,
    redirect,
    render_template,
)

from corji.api import CorgiResource
import corji.settings as settings

admin_blueprint = Blueprint('admin', __name__,
                             template_folder='templates')
logger = logging.getLogger(settings.Config.LOGGER_NAME)

api = CorgiResource()


@admin_blueprint.route("/corgi/all", methods=['GET'])
def list_all():
    """Dump out ALL OUR CORGI PICTURES"""
    if(settings.Config.DASHBOARD_ENABLED):
        data = api.get_all()
        data = OrderedDict(sorted(data.items()))
        return render_template("html/corgi/list_all.html", data=data)
    else:
        return redirect("/")
