SELECT COUNT(card_id) AS count
FROM patient
WHERE YEAR(card_date) = '$year'
GROUP BY MONTH(card_date);
