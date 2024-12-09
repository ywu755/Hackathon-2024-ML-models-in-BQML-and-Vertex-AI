{{
    config(
        schema='hackathon_q1_2024',
        materialized='table'
    )
}}

SELECT *
FROM ML.ARIMA_EVALUATE(
    MODEL {{ ref('arima_model') }},
    STRUCT(TRUE AS show_all_candidate_models)
)
