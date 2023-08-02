# Submission_-_FieldPRO

This repository contains:
1. the Juypter notebook containing the detailed calibration rationale,
2. the input and output data files ([data/](data/) directory),
3. and the directory with the deployment files for GCP deployment ([deploy/](deploy/) directory).

## Calibration results
First, we predicted the leakage current (in the given units) of piezo crystal as a function of the piezo crystal temperature using least squared linear regression as
$$\text{hourly discharge through leakage (given units)} = 3.331^{\pm 0.026} + 0.04053^{\pm 0.00095} \cdot \frac{\theta_{\text{piezo}}}{{}^\circ C}, $$
where the confidence interval of the parameters was chosen to be $99\\%$.

Second, we could fit the actual precipitation measure by the reference weather station against the surplus of discharge. We obtained the relation
$$\text{precipitation (in mm)} = \frac{\text{actual hourly discharge (given units)} - \text{hourly discharge through leakage (given units)} - 59.3^{\pm 89.2}}{37.8^{\pm 5.4}} ,$$
where the confidence interval of the parameters was chosen to be $95\\%$.

## Deployment
Set up a Google Cloud Project and write down the `<project-id>`. Then, authenticate and deploy using:
```
gcloud app create --project=<project-id>
gcloud components install app-engine-python
gcloud app create --project=<project-id>
```

## API
The result of the calibration was deployed on GCP and can be tested [here](https://piezoelectric-rain-gauge.rj.r.appspot.com/fieldpro)

Address: https://piezoelectric-rain-gauge.rj.r.appspot.com

Method: GET

Endpoint: fieldpro

Parameters:
* piezo_charge_decrease (required: True)
* piezo_temperature (required: True)
* air_humidity_100 (required: False)
* air_temperature_100 (required: False)
* atm_pressure_main (required: False)

Example:
https://piezoelectric-rain-gauge.rj.r.appspot.com/fieldpro?piezo_charge_decrease=150&piezo_temperature=15&air_humidity_100=82&air_temperature_100=28&atm_pressure_main=92400&num_of_resets=5

Output: JSON object with the following keys:
* piezo_charge_decrease_offset
* piezo_charge_decrease_prediction (calculated based on the piezo_temperature)
* precipitation (in mm)

## Observations
* **Obviously, I had to mess up the time zones. Pretty big mistake. Will fix tomorrow. The way that I handled the analysis, however, this effectively does not change my results. For future endeavours, I certainly should fix this.** (Just fixed this. Refer to the corresponding [issue](https://github.com/larsdehlwes/Submission_-_FieldPRO/issues/1).)
* In favor of development speed I disregarded the minor data gaps and treated the row index as a measure of time. In production, it may be worth to handle this issue with more care. However, as there are only a few (<1%) gaps or irregularities in the data, I preferred coding speed over detail for this challenge.
