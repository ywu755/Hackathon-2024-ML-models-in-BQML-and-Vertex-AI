utilities = [
    "AEP",
    "COMED",
    "DAYTON",
    "DEOK",
    "DOM",
    "DUQ",
    "EKPC",
    "FE",
    "NI",
    "PJME",
    "PJMW",
]

template = "{{{{ generate_arima_plus_xreg_model('{}') }}}}"
for utility in utilities:
    filename = (
        f"models/hourly_energy_pjm/arima_plus_xreg_{utility.lower()}.sql"
    )
    with open(filename, "w") as file:
        file.write(template.format(utility))

# forecast
forecast_template = """
{{{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}}}

{{{{ forecast_arima_plus_xreg_model('{}') }}}}
"""

for utility in utilities:
    filename = f"models/hourly_energy_pjm/forecast_{utility.lower()}.sql"
    with open(filename, "w") as file:
        file.write(forecast_template.format(utility))

# evaluate
evaluate_template = """
{{{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}}}
{{{{ evaluate_arima_plus_xreg_model('{}') }}}}
"""
for utility in utilities:
    filename = f"models/hourly_energy_pjm/evaluate_{utility.lower()}.sql"
    with open(filename, "w") as file:
        file.write(evaluate_template.format(utility))

# explain
explain_template = """
{{{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}}}
{{{{ explain_arima_plus_xreg_model('{}') }}}}
"""
for utility in utilities:
    filename = f"models/hourly_energy_pjm/explain_{utility.lower()}.sql"
    with open(filename, "w") as file:
        file.write(explain_template.format(utility))
