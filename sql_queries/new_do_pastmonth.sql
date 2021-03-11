SELECT
CONCAT('https://findingaids.smith.edu/repositories/',archival_object.repo_id,'/archival_objects/',archival_object.id) AS `Object in Context`,
archival_object.title,
file_version.file_uri AS link,
resource.title AS 'Collection'
FROM
instance_do_link_rlshp
JOIN digital_object
ON instance_do_link_rlshp.digital_object_id = digital_object.id
JOIN instance
ON instance_do_link_rlshp.instance_id = instance.id
JOIN archival_object
ON instance.archival_object_id = archival_object.id
JOIN file_version
ON file_version.digital_object_id = digital_object.id
JOIN resource
ON archival_object.root_record_id = resource.id
WHERE
smith.digital_object.create_time BETWEEN (NOW() - INTERVAL 1 MONTH) AND NOW()
AND smith.file_version.publish = 1
