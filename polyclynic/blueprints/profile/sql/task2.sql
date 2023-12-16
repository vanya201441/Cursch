SELECT*
FROM patient
WHERE (YEAR(card_date) >= '$year_start') AND (YEAR(card_date) <= '$year_end');
