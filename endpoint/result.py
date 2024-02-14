from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from datetime import date
from enum import Enum, IntEnum

router=APIRouter(tags=["result"])


# #1 result read
# @router.get("/result/test/user/{user_id}/form/{form_id}")
# async def result_read(request:Request,user_id:int,form_id:int):
#    #query set
#    query="""
#          with
#          user_sum_final_score as (
#                select sum(final_score) as user_sum_final_score from view_user_answer where user_id=:user_id and form_id=:form_id  group by user_id),

#          sum_score as (select sum(score) as sum_score 
#                   from question
#                   where form_id=:form_id and parent_question_id is null and is_active='true' 
#                   group by form_id),
#          max_weightage as (select total_weightage as max_weightage 
#                      from view_question_option where form_id=:form_id
#                      group by total_weightage order by total_weightage desc limit 1)

#          select user_sum_final_score.*, sum_score.*,max_weightage.* from user_sum_final_score, sum_score,max_weightage
#       """
#    values={"form_id":form_id, "user_id":user_id}
#    #query run
#    response=await database_fetch_all(query,values)
   
#    if response["status"]=="false":
#       raise HTTPException(status_code=400,detail=response)
   
#    try:
#       user_sum_final_score = response['message'][0]['user_sum_final_score']
#       max_weightage = response['message'][0]['max_weightage']
#       sum_score = response['message'][0]['sum_score']
#       user_result = (user_sum_final_score*100)/(sum_score*max_weightage)
#       print(user_result)
#       if user_result < 50:
#          risk = 'low'
#       if user_result > 66:
#          risk = 'high'
#       if user_result <= 66 and user_result >= 50:
#          risk = 'medium'

#       response = {
#          "status":"succes",
#          "message":{
#             "result":user_result/10,
#             "risk":risk
#          }
#       }
#    except:
#       response = {
#          "status":"failed",
#          "message":"somthing error!"
#       }
#       raise HTTPException(status_code=400,detail=response)
#    return response






#1 result read
# @router.get("/result/user/{user_id}/form/{form_id}")
# async def result_read(request:Request,user_id:int,form_id:int):
#    query="""
#          select 
#          a.*,
#          q.id as qid, q.title as qt, q.score, 
#          o.id,  o.title, o.weightage 
#          from answer as a 
#          left join "option" as o on o.id=a.option_id
#          left join question as q on q.id=o.question_id
#          where a.created_by_id=:user_id and flag is null and q.form_id=:form_id
#          order by q.id asc
#          """
#    values={"form_id":form_id, "user_id":user_id}
#    #query run
#    response=await database_fetch_all(query,values)

#    user_sum_final_score = 0
#    q_final_score = 0
#    i=1
#    for x in  response['message']:
#       if int(x['score']):
#          user_sum_final_score=user_sum_final_score+q_final_score
#          q_score =int(x['score'])
#          q_final_score=q_score*int(x['weightage'])
#          if i == len(response['message']):
#             user_sum_final_score=user_sum_final_score+q_final_score
#       if int(x['score']) == 0:
#          q_final_score = q_final_score * int(x['weightage'])
#          if i == len(response['message']):
#             user_sum_final_score=user_sum_final_score+q_final_score
#       i=i+1
        
#    # query set
#    query="""
#          with
#          sum_score as (select sum(score) as sum_score 
#                   from question
#                   where form_id=:form_id and parent_question_id is null and is_active='true' 
#                   group by form_id),
#          max_weightage as (select total_weightage as max_weightage 
#                      from view_question_option where form_id=:form_id
#                      group by total_weightage order by total_weightage desc limit 1)

#          select  sum_score.*,max_weightage.* from  sum_score,max_weightage
#       """
#    values={"form_id":form_id}
#    #query run
#    response=await database_fetch_all(query,values)
   
#    if response["status"]=="false":
#       raise HTTPException(status_code=400,detail=response)
   
#    try:
#       max_weightage = response['message'][0]['max_weightage']
#       sum_score = response['message'][0]['sum_score']
#       print("mw",max_weightage)
#       print("usc",user_sum_final_score)
#       print("sc",sum_score)
#       user_result = (user_sum_final_score*100)/(sum_score*max_weightage)
#       if user_result < 5:
#          risk = 'low'
#       if user_result > 9:
#          risk = 'high'
#       if user_result <= 9 and user_result >= 5:
#          risk = 'medium'

#       response = {
#          "status":"succes",
#          "message":{
#             "result":user_result/10,
#             "risk":risk
#          }
#       }
#    except:
#       response = {
#          "status":"failed",
#          "message":"somthing error!"
#       }
#       raise HTTPException(status_code=400,detail=response)
#    return response

@router.get("/result/user/{user_id}/form/{form_id}")
async def result_read(request:Request,user_id:int,form_id:int):
    # Fetch latest answers for the user for the given form
    query = """
        WITH latest_answers AS (
            SELECT 
                a.*,
                q.id AS question_id,
                q.score AS question_score,
                o.weightage AS option_weightage,
                ROW_NUMBER() OVER (PARTITION BY q.id, a.option_id ORDER BY a.created_at DESC) AS rn
            FROM 
                answer AS a
            LEFT JOIN 
                option AS o ON o.id = a.option_id
            LEFT JOIN 
                question AS q ON q.id = o.question_id
            WHERE 
                q.form_id = :form_id 
                AND a.created_by_id = :user_id 
                AND a.flag IS NULL
        )
        SELECT 
            question_id,
            question_score,
            option_weightage
        FROM 
            latest_answers
        WHERE 
            rn = 1;
    """

    values = {"form_id": form_id, "user_id": user_id}
    response = await database_fetch_all(query, values)

    # Calculate the total score and total question score
    total_score = 0
    total_question_score = 0
    map = {}
    
    for row in response['message']:    
        total_score += row['question_score'] * row['option_weightage'] / 100
        map[row['question_id']] = row['question_score'] # for storing total of all unique questions

    total_question_score = sum(map.values())

    # Ensure total_question_score is not zero to avoid division by zero
    if total_question_score == 0:
        raise HTTPException(status_code=400, detail="Total question score is zero")

    # Calculate the final result
    user_result = (total_score / total_question_score) * 100

    if user_result < 5:
        risk = 'low'
    if user_result > 9:
        risk = 'high'
    if user_result <= 9 and user_result >= 5:
        risk = 'medium'

    response = {
        "status":"success",
        "message":{
            "result": user_result,
            "risk": risk
        }
    }

    # Return the result
    return response

