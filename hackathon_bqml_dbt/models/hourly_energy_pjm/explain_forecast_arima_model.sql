{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}

SELECT *
FROM ML.EXPLAIN_FORECAST(
    MODEL {{ ref('arima_model') }},
    STRUCT(100 AS horizon, 0.9 AS confidence_level)
)
