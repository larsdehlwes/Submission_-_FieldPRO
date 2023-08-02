from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api

from marshmallow import Schema, fields

import numpy as np

app = Flask(__name__)
api = Api(app)

# Argument parsing

class FieldProQuerySchema(Schema):
    piezo_temperature = fields.Float(required=True)
    piezo_charge_decrease = fields.Int(required=True)
    # Think about requiring the following parameters as well, in order to ensure that future changes do not break compatibility with tools that our engineers build from here on.
    air_humidity_100 = fields.Float(required=False)
    air_temperature_100 = fields.Float(required=False)
    atm_pressure_main = fields.Float(required=False)
    num_of_resets = fields.Int(required=False)

schema = FieldProQuerySchema()

output = {}

class PrecipitationPrediction(Resource):
    def get(self):
        # Validate parameters
        errors = schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        piezo_charge_decrease_prediction = np.exp(3.328721 + 0.040634 * float(request.args.get('piezo_temperature')))
        piezo_charge_decrease_offset = int(request.args.get('piezo_charge_decrease')) - piezo_charge_decrease_prediction - 69.41
        output['precipitation'] = np.max([0,piezo_charge_decrease_offset])/37.52
        output['piezo_charge_decrease_prediction'] = piezo_charge_decrease_prediction
        output['piezo_charge_decrease_offset'] = piezo_charge_decrease_offset
        return jsonify(output)
    
api.add_resource(PrecipitationPrediction, '/fieldpro')

if __name__ == '__main__':
    app.run(debug=True)
