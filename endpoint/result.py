from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["result"])


#1 result read
@router.get("/result/member/{member_id}/form/{form_id}")
async def result_read(request:Request,member_id:int,form_id:int):
   #query set
   query="""
         with
         user_sum_final_score as (
               select sum(final_score) as user_sum_final_score from view_member_answer where member_id=:member_id and form_id=:form_id group by member_id),

         sum_score as (select sum(score) as sum_score 
                  from question
                  where form_id=:form_id and parent_question_id is null  
                  group by form_id),
         max_weightage as (select total_weightage as max_weightage 
                     from view_question_option where form_id=:form_id
                     group by total_weightage order by total_weightage desc limit 1)

         select user_sum_final_score.*, sum_score.*,max_weightage.* from user_sum_final_score, sum_score,max_weightage
      """
   values={"form_id":form_id, "member_id":member_id}
   #query run
   response=await database_fetch_all(query,values)
   
   if response["status"]=="false":
      raise HTTPException(status_code=400,detail=response)
   
   try:
      user_sum_final_score = response['message'][0]['user_sum_final_score']
      max_weightage = response['message'][0]['max_weightage']
      sum_score = response['message'][0]['sum_score']
      member_result = (user_sum_final_score*100)/(sum_score*max_weightage)
      print(member_result)
      if member_result < 50:
         risk = 'low'
      if member_result > 66:
         risk = 'high'
      if member_result <= 66 and member_result >= 50:
         risk = 'medium'

      response = {
         "status":"succes",
         "message":{
            "result":member_result,
            "risk":risk
         }
      }
   except:
      response = {
         "status":"failed",
         "message":"somthing error!"
      }

   return response


