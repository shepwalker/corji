from collections import OrderedDict
from operator import itemgetter
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
    if settings.Config.DASHBOARD_ENABLED:
        results = api.get_all()['results']
        results = sorted(results, key=itemgetter('emoji')) 

        return render_template("html/admin/list_all.html", data=results)
    else:
        return redirect("/")
