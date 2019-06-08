SELECT mem.id, sum(case when value then 1 else 0 end) as votes_for, count(value) as votes 
FROM MEMBER as mem LEFT JOIN
(SELECT member.id, vote.value, action.id as actionid, project.id as projectid, project.authorityid as authorityid
FROM member
    LEFT JOIN vote ON(member.id = vote.memberID)
    LEFT JOIN action ON(vote.actionid = action.id)
    LEFT JOIN project ON(action.projectid = project.id)
-- WHERE
) as foo ON(mem.id = foo.id)
GROUP BY mem.id ORDER BY mem.id;

SELECT action.id, action.type, action.projectID, project.authorityID, positive_votes, negative_votes FROM action
JOIN project ON(action.projectID = project.id)
--WHERE
ORDER BY action.id;

