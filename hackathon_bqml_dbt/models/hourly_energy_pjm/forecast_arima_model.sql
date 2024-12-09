{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}

SELECT *
FROM {{ dbt_ml.forecast(ref('arima_model'), 100, 0.9) }}
