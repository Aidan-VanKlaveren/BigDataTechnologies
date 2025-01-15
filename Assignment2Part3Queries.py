# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:29:44 2022

@author: aidan
"""

Question 1
MATCH (t) - [:USING] -> (s) 
RETURN s.displayName AS Source, count(s.displayName) AS Count
ORDER BY count(s.displayName)  DESC
LIMIT 5

Question 2
MATCH (t) - [:TAGS] -> (h)
WITH t.postedTimestamp as Date, h.hashtag AS Hashtag
WHERE Date >= datetime("2016-03-26") AND Date <= datetime("2016-03-31") AND Hashtag IS NOT NULL
WITH date(Date) as Day, Hashtag as Hashtags, count(Hashtag) AS counts
ORDER BY  Day DESC, counts DESC
RETURN Day, collect(Hashtags)[0..5] as Hashtags

Question 3
MATCH (me:User {username:"m_mrezamm"}) - [:POSTS] -> (t) - [:TAGS] -> (h) 
WITH DISTINCT  h.hashtag as hashtag, me
MATCH (sugg:User) - [:POSTS] -> (t) - [:TAGS] -> (h:Hashtag {hashtag:hashtag})
WHERE sugg <> me
WITH sugg, COUNT(hashtag) as Common
RETURN sugg.username as User, Common
ORDER BY Common DESC

Question 4
MATCH (u1:User) - [:POSTS] -> (t) - [:MENTIONS] -> (friend:User)
WITH u1, friend
MERGE (u1) - [:FOLLOWS] -> (friend)
SET u1.weight = 1
MERGE (friend) - [:FOLLOWS] -> (u1) 
SET friend.weight = 1
Return u1, friend

Question 5
CALL gds.graph.project(
    'follows-weighted',
    'User',
    'FOLLOWS',
    {
        relationshipProperties: 'weight'
    }
) YIELD
    graphName, nodeProjection, nodeCount, relationshipProjection, relationshipCount

CALL gds.pageRank.stream('follows-weighted')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS n, score AS pageRank
RETURN n.username AS User, pageRank
ORDER BY pageRank DESC
LIMIT 5