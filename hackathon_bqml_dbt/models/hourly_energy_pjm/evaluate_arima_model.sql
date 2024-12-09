
{{
    config(
        schema='hackathon_q1_2024',
        materialized='model',
        ml_config={
            'model_type': 'ARIMA_PLUS',
            'time_series_timestamp_col' : 'datetime',
            'time_series_id_col' : 'utility',
            'time_series_data_col' : 'demand',
            'auto_arima_max_order' : 5
        }
    )
}}

SELECT
  `Datetime` AS `datetime`,
  utility,
  SAFE_CAST(demand AS FLOAT64) AS demand
FROM `kv-ds-lder-der.hackathon_q1_2024.hourly_energy_pjm`
UNPIVOT (
  demand FOR utility IN (
    AEP, COMED, DAYTON, DEOK, DOM, DUQ, EKPC, FE, NI, PJME, PJMW
  )
)
WHERE Datetime > '2016-01-01 00:00:00'
ORDER BY datetime
