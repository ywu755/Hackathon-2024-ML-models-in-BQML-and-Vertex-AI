{% macro generate_arima_plus_xreg_model(utility) %}
{{ config(
    schema='hackathon_q1_2024',
    materialized='model',
    alias=utility ~ '_arima_plus_xreg',
    ml_config={
        'MODEL_TYPE': 'ARIMA_PLUS_XREG',
        'TIME_SERIES_TIMESTAMP_COL': 'datetime',
        'TIME_SERIES_DATA_COL': 'demand',
        'TIME_SERIES_LENGTH_FRACTION': 0.8,
        'MIN_TIME_SERIES_LENGTH': 24,
        'AUTO_ARIMA': true,
    }
) }}

SELECT
  `Datetime` AS `datetime`,  
  '{{ utility }}' AS utility,
  SAFE_CAST(demand AS FLOAT64) AS demand
FROM `project_id.hackathon_q1_2024.hourly_energy_pjm`
UNPIVOT (
  demand FOR utility IN (
    AEP, COMED, DAYTON, DEOK, DOM, DUQ, EKPC, FE, NI, PJME, PJMW
  )
)
WHERE utility = '{{ utility }}'
and Datetime > '2016-01-01 00:00:00'
ORDER BY datetime
{% endmacro %}

