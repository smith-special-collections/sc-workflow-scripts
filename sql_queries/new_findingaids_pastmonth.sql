SELECT
resource.title,
CONCAT('https://findingaids.smith.edu/repositories/',resource.repo_id,'/resources/',resource.id) AS `Finding Aid Link`,
resource.finding_aid_date,
resource.finding_aid_status_id,
CAST(note.notes AS CHAR (10000) CHARACTER SET UTF8) AS 'abstract',
date.begin,
date.end
FROM
note
RIGHT JOIN resource
ON note.resource_id = resource.id
LEFT JOIN date
ON date.resource_id = resource.id
WHERE
smith.resource.finding_aid_date LIKE '%2021%'
AND smith.resource.user_mtime BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()
AND smith.note.notes LIKE '%abstract%'
