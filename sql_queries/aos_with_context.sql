SELECT
archival_object.title,
enumeration_value.`value` AS `level of description`,
enumeration_value_alias1.`value` AS `date type`,
date.`begin`,
date.`end`,
date.expression,
enumeration_value_alias2.`value` AS `date certainty`,
archival_object_alias1.title AS Parent,
archival_object_alias2.title AS Grandparent,
archival_object_alias3.title AS `Great-Grandparent`,
enumeration_value_alias3.`value` AS `extent portion`,
extent.number,
enumeration_value_alias5.`value` AS `extent type`,
extent.container_summary,
extent.physical_details,
extent.dimensions,
enumeration_value_alias4.`value` AS `top container type`,
top_container.indicator,
enumeration_value_alias7.`value` AS 'child type',
sub_container.indicator_2,
enumeration_value_alias6.`value` AS 'grandchild type',
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
LEFT JOIN enumeration_value
ON enumeration_value.id = archival_object.level_id 
LEFT JOIN enumeration_value AS enumeration_value_alias1
ON date.date_type_id = enumeration_value_alias1.id 
LEFT JOIN enumeration_value AS enumeration_value_alias2
ON date.certainty_id = enumeration_value_alias2.id 
LEFT JOIN enumeration_value AS enumeration_value_alias3
ON extent.portion_id = enumeration_value_alias3.id 
LEFT JOIN enumeration_value AS enumeration_value_alias5
ON extent.extent_type_id = enumeration_value_alias5.id 
LEFT JOIN enumeration_value AS enumeration_value_alias4
ON top_container.type_id = enumeration_value_alias4.id 
LEFT JOIN enumeration_value AS enumeration_value_alias7
ON sub_container.type_2_id = enumeration_value_alias7.id 
LEFT JOIN enumeration_value AS enumeration_value_alias6
ON sub_container.type_3_id = enumeration_value_alias6.id
WHERE
smith.archival_object.root_record_id = '[INSERT COLLECTION NUMBER FROM URI HERE]'
