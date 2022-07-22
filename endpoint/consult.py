from lib2to3.pgen2.token import OP
from fastapi import APIRouter, Request, HTTPException
from setting import *
from utility import *
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum, IntEnum
import uuid

router=APIRouter(tags=["consult"])


#validation
#1 status:type
class status_type(str, Enum):
    open='open'
    succesfully_closed='succesfully_closed'
    unsuccesfully_closed ='unsuccesfully_closed'


#scehema
#1 followup
class followup(BaseModel):
    patient_id:int
    created_by:Optional[int]=0
    status:status_type
    next_followup_at:Optional[datetime] = None
    closed_at:Optional[date] = None
    data:dict



#1 followup_notification
class followup_notification(BaseModel):
    notification_type:str
    patient_id:int
    created_by:Optional[int]=0
    status:status_type
    next_followup_at:Optional[datetime] = None
    closed_at:Optional[date] = None
    data:dict

#scehema
#1 consult
class consult(BaseModel):
    patient_id:int
    created_by:Optional[int]
    private_observation:Optional[str]=None
    prescription_lifestyle:Optional[str]=None
    prescription_medical:Optional[str]=None
    general:Optional[str]=None
    next_appointment:Optional[str]=None


#  report
class report(BaseModel):
    patient_id:int
    assesment_completed:Optional[list]
    health_step:Optional[dict]
    health_goal:Optional[list]
    assesment_list:Optional[list]
    consult_data:Optional[dict]


#scehema
#1 consult
class consult_filter(BaseModel):
    patient_id:Optional[int]=0
    patient_mobile:Optional[str]=None
    patient_name:Optional[str]=None
    created_by:Optional[int]=0


#1 consult
class report_filter(BaseModel):
    report_id:Optional[int]=0
    patient_id:Optional[int]=0
    patient_mobile:Optional[str]=None
    patient_name:Optional[str]=None
    doctor_consult_id:Optional[int]=0
    created_by:Optional[int]=0
    
#scehema
# meeting
class meeting(BaseModel):
    doctor_id:int
    patient_id:int
    meeting_link:str
    payment_link:str
    date_time:datetime
    created_by:Optional[int]=0
    type:Optional[str]=None
    data:dict


# meeting
class meeting_filter(BaseModel):
    doctor_id:Optional[int]=0
    patient_id:Optional[int]=0
    date_time:Optional[datetime]
    created_by:Optional[int]=0
    type:Optional[str]=None




   
#1 followup create
@router.post("/followup")
async def followup_create(request:Request,payload:followup):
    #prework
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)
    
    #query set
    query="""insert into followup (created_by,patient_id,status,next_followup_at,closed_at,data)
        values (:created_by,:patient_id,:status,:next_followup_at,:closed_at,:data)
        returning *"""
    values={"created_by":user_id,"patient_id":payload['patient_id'],"status":payload['status'],"next_followup_at":payload['next_followup_at'],"closed_at":payload['closed_at'],"data":json.dumps(payload['data'])}
    
    #query run
    response = await database_execute(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)

    return response


#2 followup filter
@router.post("/followup/filter")
async def followup_filter(request:Request,payload:followup):
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)
    #query set
    query="""select u.name, u.email, u.mobile, fp.* from "user" as u 
        left join followup as fp on fp.patient_id=u.id where fp.is_active='true' and fp.status='open'"""
    
        
    if payload['patient_id'] and payload['notification_type'] == 'old':
        query = query + " and fp.patient_id=:patient_id"
    if payload['closed_at'] and payload['notification_type'] == 'old':
        query = query + " and fp.closed_at=:closed_at"
    if payload['next_followup_at'] and payload['notification_type'] == 'old':
        query = query + " and fp.next_followup_at=:next_followup_at"
    if payload['status'] and payload['notification_type'] == 'old':
        query = query + " and fp.status=:status"
    if payload['created_by'] and payload['notification_type'] == 'old':
        query = query + " and fp.created_by=:created_by"
        
    values={"created_by":payload['created_by'],"patient_id":payload['patient_id'],"status":payload['status'],"next_followup_at":payload['next_followup_at'],"closed_at":payload['closed_at']}
    #query run
    response=await database_fetch_all(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)
    row=response["message"]
    #finally
    response=row
    return response


#2 followup filter
@router.post("/followup/notification")
async def followup_notification(request:Request,payload:followup_notification):
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)
    #query set
    query="""select u.name, u.email, u.mobile, fp.* from "user" as u 
        left join followup as fp on fp.patient_id=u.id"""
    
    if payload['notification_type'] == 'old':
        query = query + " where fp.is_active='true' and fp.status='open'"
    if payload['notification_type'] == 'new':
        query = query + " where fp.patient_id is null order by u.id desc"
        
    if payload['patient_id'] and payload['notification_type'] == 'old':
        query = query + " and fp.patient_id=:patient_id"
    if payload['closed_at'] and payload['notification_type'] == 'old':
        query = query + " and fp.closed_at=:closed_at"
    if payload['next_followup_at'] and payload['notification_type'] == 'old':
        query = query + " and fp.next_followup_at=:next_followup_at"
    if payload['status'] and payload['notification_type'] == 'old':
        query = query + " and fp.status=:status"
    if payload['created_by'] and payload['notification_type'] == 'old':
        query = query + " and fp.created_by=:created_by"
        
    values={"created_by":payload['created_by'],"patient_id":payload['patient_id'],"status":payload['status'],"next_followup_at":payload['next_followup_at'],"closed_at":payload['closed_at']}
    #query run
    response=await database_fetch_all(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)
    row=response["message"]
    #finally
    response=row
    return response




#----------------------------------------------------------------------------------------


#1 consult create
@router.post("/consult")
async def consult_create(request:Request,payload:consult):
    #prework
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)

    payload['data'] = json.dumps({"private_observation":payload['private_observation'],"prescription_lifestyle":payload['prescription_lifestyle'],"prescription_medical":payload['prescription_medical'],"general":payload['general'],"next_appointment":payload['next_appointment']})
    #query set
    query="""insert into consult (created_by,patient_id,data)
        values (:created_by,:patient_id,:data)
        returning *"""
    values={"created_by":user_id,"patient_id":payload['patient_id'],"data":payload['data']}
    
    #query run
    response = await database_execute(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)

    return response


#2 consult filter
@router.post("/consult/filter")
async def consult_filter(request:Request,payload:consult_filter):
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)

    #query set
    query="""select p.mobile, p.name, d.name as dr_name, d.mobile as dr_mobile, c.* from consult as c 
    left join patient as p on p.id=c.patient_id 
    left join "user" as d on d.id=c.created_by
    where p.is_active='true'"""

    if payload['patient_id']:
        query = query+" and p.id="+str(payload['patient_id'])
    if payload['patient_mobile']:
        query = query+" and p.mobile like '%"+payload['patient_mobile']+"%'"
    if payload['patient_name']:
        query = query+" and p.name like '%"+payload['patient_name']+"%'"
    if payload['created_by']:
        query = query + " and p.created_by='"+str(payload['created_by'])+"'"
        
    values={}
    #query run
    response=await database_fetch_all(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)
    row=response["message"]
    #finally
    response=row
    return response


# -------------------------------------------------------------------------------------
#report
#1 report create

@router.post("/report")
async def report_create(request:Request,payload:report):
    #prework
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)

    payload['data'] = json.dumps({
        "assesment_completed":payload['assesment_completed'],
        "health_step":payload['health_step'],
        "health_goal":payload['health_goal'],
        "assesment_list":payload['assesment_list'],
        "consult_data":payload['consult_data'],
        })
    #query set
    query="""insert into consult (created_by,patient_id,data,type)
        values (:created_by,:patient_id,:data,:type)
        returning *"""
    values={"created_by":user_id,"patient_id":payload['patient_id'],"data":payload['data'],"type":'report'}
    
    #query run
    response = await database_execute(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)

    return response



#2 consult filter
@router.post("/report/filter")
async def consult_filter(request:Request,payload:report_filter):
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)

    #query set
    query="""select p.mobile, p.name,p.email, p.height, p.weight,(p.data->'bmi')::TEXT as bmi, d.name as dr_name, d.mobile as dr_mobile, c.* from consult as c 
    left join patient as p on p.id=c.patient_id 
    left join "user" as d on d.id=c.created_by
    where p.is_active='true'"""

    if payload['patient_id']:
        query = query+" and p.id="+str(payload['patient_id'])
    if payload['patient_mobile']:
        query = query+" and p.mobile like '%"+payload['patient_mobile']+"%'"
    if payload['patient_name']:
        query = query+" and p.name like '%"+payload['patient_name']+"%'"
    if payload['created_by']:
        query = query + " and c.created_by='"+str(payload['created_by'])+"'"    
    if payload['doctor_consult_id']:
        query = query+" and c.doctor_consult_id ='"+str(payload['doctor_consult_id'])+"'"
    if payload['report_id']:
        query = query+" and c.id ='"+str(payload['report_id'])+"'"

    values={}
    #query run
    response=await database_fetch_all(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)
    row=response["message"]
    #finally
    response=row
    return response

#----------------------------------------------------------------------------------------


#1 meeting create
@router.post("/meeting")
async def meeting_create(request:Request,payload:meeting):
    #prework
    user_id = request.state.user_id
    payload=payload.dict()
    #admin user check
    response = await is_admin(user_id)
    if response['status'] != "true":
        raise HTTPException(status_code=400,detail=response)
    
    #query set
    query="""insert into meeting (created_by, patient_id, doctor_id, type, meeting_link,        payment_link, date_time, data )
    values (:created_by, :patient_id, :doctor_id, :type, :meeting_link, :payment_link, :date_time, :data )
    returning *"""
    values={"created_by":user_id,"patient_id":payload['patient_id'],"doctor_id":payload['doctor_id'],"type":payload['type'],"meeting_link":payload['meeting_link'],"payment_link":payload['payment_link'],"date_time":payload['date_time'],"data":json.dumps(payload['data'])}
    
    #query run
    response = await database_execute(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)

    return response


#2 meeting filter
@router.post("/meeting/filter")
async def meeting_filter(request:Request,payload:meeting_filter):
    #query set
    query="select * from meeting where is_active='true'"
    if payload['patient_id']:
        query = query + " and patient_id=:patient_id"
    if payload['created_by']:
        query = query + " and created_by=:created_by"
    if payload['doctor_id']:
        query = query + " and doctor_id=:doctor_id"
        
    values={"created_by":payload['created_by'],"patient_id":payload['patient_id'],"doctor_id":payload['doctor_id']}
    #query run
    response=await database_fetch_all(query,values)
    if response["status"]=="false":
        raise HTTPException(status_code=400,detail=response)
    row=response["message"]
    #finally
    response=row
    return response


