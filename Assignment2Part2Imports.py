# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 18:14:03 2022

@author: aidan
"""

CALL apoc.periodic.iterate("CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value",
'WITH 
value.id AS id
 ,datetime({ epochMillis: apoc.date.parse(value.actor.postedTime, "ms",
 "yyyy-MM-dd\'T\'HH:mm:ss.SSS\'Z\'")}) AS postedTimestamp
 ,value.text AS text
 ,value.actor.languages AS language
 ,value.retweetCount AS retweetCount
 ,value.favoritesCount AS favoritesCount
 ,value.verb AS verb
 MERGE (t:Tweet{id:id})
 ON CREATE SET
 t.postedTimestamp = postedTimestamp
 ,t.text = text
 ,t.language = language
 ,t.retweetCount = retweetCount
 ,t.favoritesCount = favoritesCount
 ,t.verb = verb 
',
{batchSize:500})
YIELD * ; 

CALL apoc.periodic.iterate("CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value",
'WITH 
  value.link AS link
 ,value.id AS id
 MATCH(t:Tweet{id:id})
 MERGE (l:Link{link:link})
 MERGE (t)-[:CONTAINS]->(l)',
{batchSize:500})
YIELD * ; 

CALL apoc.periodic.iterate("CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value",
'WITH 
  value.generator.displayName AS displayName
 ,value.id AS id
 MATCH(t:Tweet{id:id})
 MERGE (s:Source{displayName:displayName})
 MERGE (t)-[:USING]->(s)',
{batchSize:500})
YIELD * ; 

CALL apoc.periodic.iterate("CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value",
'WITH 
  value.actor.preferredUsername AS preferredUsername
 ,value.id AS id
 MATCH(t:Tweet{id:id})
 MERGE (u:User{username:preferredUsername})
 MERGE (u)-[:POSTS]->(t)',
{batchSize:500})
YIELD * ; 

CALL apoc.periodic.iterate("
CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value return value
","
MATCH (t:Tweet{id:value.id})
WITH t, value.twitter_entities.hashtags AS hashtags
UNWIND hashtags AS hashtag
FOREACH (tag in hashtags |
    MERGE (h:Hashtag{hashtag:toLower(tag.text)})
    MERGE (t)-[:TAGS]->(h)
)
",{batchSize: 500, iterateList: true});

CALL apoc.periodic.iterate("
CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value return value
","
MATCH (t:Tweet{id:value.id})
WITH t, value.twitter_entities.user_mentions AS usermentions
UNWIND usermentions AS usermention
FOREACH (mention in usermention |
    MERGE (u:User{username:mention.screen_name})
    MERGE (t)-[:MENTIONS]->(u)
)
",{batchSize: 500, iterateList: true});

CALL apoc.periodic.iterate("
CALL apoc.load.json('file:///10000TweetsCleaned.json') YIELD value return value
","
MATCH (t:Tweet{id:value.id})
WHERE t.verb = 'share'
WITH value.object.actor.id AS retweetid
MERGE (rt:Retweet{retweetid:retweetid})
MERGE (t)-[:RETWEETS]->(rt)
",{batchSize: 500})
YIELD *;