{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}

SELECT *
FROM ML.ARIMA_COEFFICIENTS(MODEL {{ ref('arima_model') }})
