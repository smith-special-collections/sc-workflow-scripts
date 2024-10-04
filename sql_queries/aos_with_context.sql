SELECT
archival_object.title,
archival_object.level_id,
date.`begin`,
date.`end`,
date.expression,
date.certainty_id,
date.date_type_id,
archival_object_alias1.title AS Parent,
archival_object_alias2.title AS Grandparent,
archival_object_alias3.title AS `Great-Grandparent`,
extent.portion_id,
extent.number,
extent.extent_type_id,
extent.container_summary,
extent.physical_details,
extent.dimensions,
top_container.type_id,
top_container.indicator,
sub_container.type_2_id,
sub_container.indicator_2,
sub_container.type_3_id,
sub_container.indicator_3
FROM
date
RIGHT JOIN archival_object
ON date.archival_object_id = archival_object.id 
LEFT JOIN archival_object AS archival_object_alias1
ON archival_object.parent_id = archival_object_alias1.id 
LEFT JOIN archival_object AS archival_object_alias2
ON archival_object_alias1.parent_id = archival_object_alias2.id 
LEFT JOIN archival_object AS archival_object_alias3
ON archival_object_alias2.parent_id = archival_object_alias3.id 
LEFT JOIN extent
ON extent.archival_object_id = archival_object.id 
LEFT JOIN instance
ON instance.archival_object_id = archival_object.id 
LEFT JOIN sub_container
ON sub_container.instance_id = instance.id 
LEFT JOIN top_container_link_rlshp
ON top_container_link_rlshp.sub_container_id = sub_container.id 
LEFT JOIN top_container
ON top_container_link_rlshp.top_container_id = top_container.id
WHERE
smith.archival_object.root_record_id = '[INSERT NUMBER FROM COLLECTION URI HERE]'
