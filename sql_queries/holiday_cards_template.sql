	#this template includes all sources for all accession types. Consider whether we want to have only donors rather than donors & sellers.
    ( SELECT
	accession.identifier AS 'Accession ID',
	accession.title AS 'Accession Title',
	accession.content_description AS 'Accession Description',
	accession.accession_date AS 'Accession Date',
	accession.created_by AS 'Accession record created by',
	accession.provenance AS 'Provenance',
	name_corporate_entity.primary_name AS 'Primary Name',
	name_corporate_entity.qualifier AS 'Rest of Name',
	agent_contact.email,
	agent_contact.`name`,
	agent_contact.address_1 AS 'Address Line 1',
	agent_contact.address_2 AS 'Address Line 2',
	agent_contact.address_3 AS 'Address Line 3',
	agent_contact.city AS 'City',
	agent_contact.region AS 'Region',
	agent_contact.country AS 'Country',
	agent_contact.post_code AS 'ZIP',
	agent_contact.note
	FROM
		linked_agents_rlshp
		JOIN accession ON linked_agents_rlshp.accession_id = accession.id
		JOIN name_corporate_entity ON linked_agents_rlshp.agent_corporate_entity_id = name_corporate_entity.agent_corporate_entity_id
		LEFT JOIN agent_contact ON agent_contact.agent_corporate_entity_id = name_corporate_entity.agent_corporate_entity_id
	WHERE
		accession_date >= '2015-01-01'
		AND role_id = '879'
		AND name_corporate_entity.authorized = '1'
		AND accession.identifier LIKE '%null%'
	) UNION
	(
	SELECT
accession.identifier AS 'Accession ID',
accession.title AS 'Accession Title',
accession.content_description AS 'Accession Description',
accession.accession_date AS 'Accession Date',
accession.created_by AS 'Accession record created by',
accession.provenance AS 'Provenance',
name_person.primary_name AS 'Primary Name',
name_person.rest_of_name AS 'Rest of Name',
agent_contact.email,
agent_contact.`name`,
	agent_contact.address_1 AS 'Address Line 1',
	agent_contact.address_2 AS 'Address Line 2',
	agent_contact.address_3 AS 'Address Line 3',
	agent_contact.city AS 'City',
	agent_contact.region AS 'Region',
	agent_contact.country AS 'Country',
	agent_contact.post_code AS 'ZIP',
agent_contact.note
FROM
agent_contact
RIGHT JOIN name_person
ON agent_contact.agent_person_id = name_person.agent_person_id
JOIN linked_agents_rlshp
ON name_person.agent_person_id = linked_agents_rlshp.agent_person_id
JOIN accession
ON linked_agents_rlshp.accession_id = accession.id
WHERE
accession_date >= '2015-01-01'
	AND role_id = '879'
	AND name_person.authorized = '1'
			AND accession.identifier LIKE '%null%'
	)
