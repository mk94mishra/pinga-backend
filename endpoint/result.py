from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["result"])


#1 result read
@router.get("/result/test/user/{user_id}/form/{form_id}")
async def result_read(request:Request,user_id:int,form_id:int):
   #query set
   query="""
         with
         user_sum_final_score as (
               select sum(final_score) as user_sum_final_score from view_user_answer where user_id=:user_id and form_id=:form_id  group by user_id),

         sum_score as (select sum(score) as sum_score 
                  from question
                  where form_id=:form_id and parent_question_id is null and is_active='true' 
                  group by form_id),
         max_weightage as (select total_weightage as max_weightage 
                     from view_question_option where form_id=:form_id
                     group by total_weightage order by total_weightage desc limit 1)

         select user_sum_final_score.*, sum_score.*,max_weightage.* from user_sum_final_score, sum_score,max_weightage
      """
   values={"form_id":form_id, "user_id":user_id}
   #query run
   response=await database_fetch_all(query,values)
   
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   
   try:
      user_sum_final_score = response['message'][0]['user_sum_final_score']
      max_weightage = response['message'][0]['max_weightage']
      sum_score = response['message'][0]['sum_score']
      user_result = (user_sum_final_score*100)/(sum_score*max_weightage)
      print(user_result)
      if user_result < 50:
         risk = 'low'
      if user_result > 66:
         risk = 'high'
      if user_result <= 66 and user_result >= 50:
         risk = 'medium'

      response = {
         "status":"succes",
         "message":{
            "result":user_result/10,
            "risk":risk
         }
      }
   except:
      response = {
         "status":"failed",
         "message":"somthing error!"
      }
      raise HTTPException(status_code=400,detail=response)
   return response






#1 result read
@router.get("/result/user/{user_id}/form/{form_id}")
async def result_read(request:Request,user_id:int,form_id:int):
   query="""
         select 
         a.*,
         q.id as qid, q.title as qt, q.score, 
         o.id,  o.title, o.weightage 
         from answer as a 
         left join "option" as o on o.id=a.option_id
         left join question as q on q.id=o.question_id
         where a.created_by_id=:user_id and flag is null and q.form_id=:form_id
         order by q.id asc
         """
   values={"form_id":form_id, "user_id":user_id}
   #query run
   response=await database_fetch_all(query,values)

   user_sum_final_score = 0
   q_final_score = 0
   i=1
   for x in  response['message']:
      
      if x['score']:
         user_sum_final_score=user_sum_final_score+q_final_score
         q_score =x['score']
         q_final_score=q_score*x['weightage']
         if i == len(response['message']):
            user_sum_final_score=user_sum_final_score+q_final_score
      if x['score'] == 0:
         q_final_score = q_final_score * x['weightage']
         if i == len(response['message']):
            user_sum_final_score=user_sum_final_score+q_final_score
      i=i+1
   print(user_sum_final_score)
   # query set
   query="""
         with
         sum_score as (select sum(score) as sum_score 
                  from question
                  where form_id=:form_id and parent_question_id is null and is_active='true' 
                  group by form_id),
         max_weightage as (select total_weightage as max_weightage 
                     from view_question_option where form_id=:form_id
                     group by total_weightage order by total_weightage desc limit 1)

         select  sum_score.*,max_weightage.* from  sum_score,max_weightage
      """
   values={"form_id":form_id}
   #query run
   response=await database_fetch_all(query,values)
   
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   
   try:
      max_weightage = response['message'][0]['max_weightage']
      sum_score = response['message'][0]['sum_score']
      user_result = (user_sum_final_score*100)/(sum_score*max_weightage)
      if user_result < 50:
         risk = 'low'
      if user_result > 66:
         risk = 'high'
      if user_result <= 66 and user_result >= 50:
         risk = 'medium'

      response = {
         "status":"succes",
         "message":{
            "result":user_result/10,
            "risk":risk
         }
      }
   except:
      response = {
         "status":"failed",
         "message":"somthing error!"
      }
      raise HTTPException(status_code=400,detail=response)
   return response
