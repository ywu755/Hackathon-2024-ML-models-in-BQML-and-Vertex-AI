{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}

SELECT *
FROM
  ML.DETECT_ANOMALIES(
    MODEL {{ ref('arima_model') }},
    STRUCT(0.9 AS anomaly_prob_threshold)
)
