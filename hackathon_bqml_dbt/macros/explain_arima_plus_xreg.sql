{% macro explain_arima_plus_xreg_model(utility) %}
    SELECT *
    FROM ML.EXPLAIN_FORECAST(
      MODEL `project_id.hackathon_q1_2024.{{ utility }}_arima_plus_xreg`,
      STRUCT(100 AS horizon, 0.9 AS confidence_level),
      (
        SELECT
          `Datetime` AS `datetime`,
          utility,
          SAFE_CAST(demand AS FLOAT64) AS demand
        FROM
          `project_id.hackathon_q1_2024.hourly_energy_pjm`
        UNPIVOT (
          demand FOR utility IN (
            AEP, COMED, DAYTON, DEOK, DOM, DUQ, EKPC, FE, NI, PJME, PJMW
          )
        )
        WHERE utility = '{{ utility }}'
          AND Datetime > '2018-01-01 00:00:00'
      )
    )
{% endmacro %}
